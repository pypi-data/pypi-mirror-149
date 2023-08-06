# This file is part of Build Your Own Virtual machine.
#
# Copyright 2018 Vincent Ladeuil.
# Copyright 2015, 2016, 2017 Canonical Ltd.
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 3, as published by the
# Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranties of MERCHANTABILITY,
# SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.
from __future__ import unicode_literals

import errno
import hashlib
import logging
import os
import time


from novaclient import exceptions
from novaclient import client

# v2 is available from wily and the python3 client from xenial
try:
    from novaclient import v2 as nova_api
    nova_api.version = '2'
except ImportError:
    from novaclient import v1_1 as nova_api
    nova_api.version = '1'

from byov import (
    errors,
    timeouts,
    vms,
)


logger = logging.getLogger(__name__)


def byov_image_name(domain, series, architecture):
    """Returns an image name.

    The images are uploaded to glance for specific needs.

    :param domain: 'cloudimg' or 'britney'.

    :param series: The ubuntu series (precise, trusty, etc).

    :param architecture: The processor architecture ('amd64', i386, etc).
    """
    if domain not in ('cloudimg', 'britney'):
        raise ValueError('Invalid image domain')
    return 'byov/{}/{}-{}.img'.format(domain, series, architecture)


def get_os_nova_client(conf):
    os_nova_client = client.Client(
        nova_api.version,
        conf.get('nova.username'), conf.get('nova.password'),
        conf.get('nova.tenant_name'),
        conf.get('nova.auth_url'),
        region_name=conf.get('nova.region_name'),
        service_type='compute')
    return os_nova_client


class NovaServerException(errors.ByovError):
    pass


class NovaClient(object):
    """A nova client re-trying requests on known transient failures."""

    def __init__(self, conf, **kwargs):
        self.first_wait = kwargs.pop('first_wait', 30)
        self.wait_up_to = kwargs.pop('wait_up_to', 600)
        self.retries = kwargs.pop('retries', 8)
        self.nova = get_os_nova_client(conf)

    def retry(self, func, *args, **kwargs):
        no_404_retry = kwargs.pop('no_404_retry', False)
        sleeps = timeouts.ExponentialBackoff(
            self.first_wait, self.wait_up_to, self.retries)
        for attempt, sleep in enumerate(sleeps, start=1):
            try:
                if attempt > 1:
                    logger.warning('Re-trying {} {}/{}'.format(
                        func.__name__, attempt, self.retries))
                return func(*args, **kwargs)
            except client.requests.ConnectionError:
                # Most common transient failure: the API server is unreachable
                msg = 'Connection error for {}, will sleep for {:.2f} seconds'
                logger.warning(msg.format(func.__name__, sleep))
            except (exceptions.OverLimit, exceptions.RateLimit):
                msg = ('Rate limit reached for {},'
                       ' will sleep for {:.2f} seconds')
                # This happens rarely but breaks badly if not caught. elmo
                # recommended a 30 seconds nap in that case.
                sleep += 30
                logger.warning(msg.format(func.__name__, sleep))
            except exceptions.ClientException as e:
                if no_404_retry and e.http_status == 404:
                    raise
                msg = '{} failed will sleep for {:.2f} seconds'
                logger.warning(msg.format(func.__name__, sleep))
            except Exception:
                # All other exceptions are raised
                logger.error('{} failed'.format(func.__name__), exc_info=True)
                raise NovaServerException('{name} failed', name=func.__name__)
            # Take a nap before retrying
            logger.info('Sleeping {:.2f} seconds for {} {}/{}'.format(
                sleep, func.__name__, attempt, self.retries))
            time.sleep(sleep)
        # Raise if we didn't succeed at all
        raise NovaServerException("Failed to '{name}' after {attempt} retries",
                                  name=func.__name__, attempt=attempt)

    def flavors_list(self):
        return self.retry(self.nova.flavors.list)

    def images_list(self):
        return self.retry(self.nova.images.list)

    def create_server(self, name, flavor, image, user_data, nics,
                      availability_zone):
        return self.retry(self.nova.servers.create, name=name,
                          flavor=flavor, image=image, userdata=user_data,
                          nics=nics, availability_zone=availability_zone)

    def delete_server(self, server_id):
        # FIXME: 404 shouldn't be retried, if it's not there anymore, there is
        # nothing to delete. -- vila 2015-07-16
        return self.retry(self.nova.servers.delete, server_id)

    def start_server(self, instance):
        return self.retry(instance.start)

    def stop_server(self, instance):
        return self.retry(instance.stop)

    def create_floating_ip(self):
        return self.retry(self.nova.floating_ips.create)

    def delete_floating_ip(self, floating_ip):
        return self.retry(self.nova.floating_ips.delete, floating_ip)

    def add_floating_ip(self, instance, floating_ip):
        return self.retry(instance.add_floating_ip, floating_ip)

    def get_server_details(self, server_id):
        return self.retry(self.nova.servers.get, server_id,
                          no_404_retry=True)

    def get_server_console(self, server, length=None):
        return self.retry(server.get_console_output, length)


class NovaServer(vms.VM):

    nova_client_class = NovaClient
    setup_ip_timeouts = 'nova.setup_ip.timeouts'
    setup_ssh_timeouts = 'nova.setup_ssh.timeouts'

    def __init__(self, conf):
        super(NovaServer, self).__init__(conf)
        self.instance = None
        self.floating_ip = None
        self.nova = self.build_nova_client()
        self.econf.set('vm.final_message', 'testbed setup completed.')

    # MISSINGTEST
    def state(self):
        try:
            with open(self.nova_id_path()) as f:
                nova_id = f.read().strip()
        except IOError as e:
            # python2 does not provide FileNotFoundError
            if e.errno == errno.ENOENT:
                # Unknown interface
                return 'UNKNOWN'
        try:
            self.instance = self.nova.get_server_details(nova_id)
        except exceptions.NotFound:
            return 'UNKNOWN'
        # The instance may remain in the DELETED state for some time.
        nova_states = dict(BUILD='STARTING',
                           ACTIVE='RUNNING',
                           SHUTOFF='STOPPED',
                           DELETED='UNKNOWN')
        return nova_states[self.instance.status]

    def build_nova_client(self):
        nova_client = self.nova_client_class(self.conf)
        return nova_client

    def find_flavor(self):
        flavors = self.conf.get('nova.flavors')
        if not flavors:
            raise NovaServerException('nova.flavors must be set')
        logger.debug('Searching for a valid flavor in {}'.format(
            ' '.join(flavors)))
        existing_flavors = self.nova.flavors_list()
        for flavor in flavors:
            for existing in existing_flavors:
                if flavor == existing.name:
                    return existing
        raise NovaServerException(
            'None of [{flavors}] can be found', flavors=','.join(flavors))

    def find_nova_image(self):
        image_name = self.conf.get('nova.image')
        logger.debug('Searching for image {}...'.format(image_name))
        existing_images = self.nova.images_list()
        for existing in existing_images:
            if image_name == existing.name:
                return existing
        raise NovaServerException(
            'Image "{name}" cannot be found', name=image_name)

    def find_nics(self):
        net_id = self.conf.get('nova.net_id')
        if net_id:
            return [{'net-id': self.conf.get('nova.net_id')}]
        return None

    # FIXME: This should save the console whether or not the setup fails
    # -- vila 2015-08-26
    def setup(self):
        logger.info('Setting up {} nova server...'.format(
            self.conf.get('vm.name')))
        flavor = self.find_flavor()
        image = self.find_nova_image()
        nics = self.find_nics()
        self.create_user_data()
        with open(self._user_data_path) as f:
            user_data = f.read()
        logger.debug('Creating {} nova server...'.format(
            self.conf.get('vm.name')))
        self.instance = self.nova.create_server(
            name=self.conf.get('vm.name'), flavor=flavor, image=image,
            user_data=user_data, nics=nics,
            # FIXME: We probably want at least a vm.az_name option. And get
            # that option from higher levels too -- vila 2014-10-13
            availability_zone=None)
        self.create_nova_id_file(self.instance.id)
        self.wait_for_active_instance()
# FIXME: We want a vm.create_floating_ip option ? -- vila 2015-08-24
#        if unit_config.is_hpcloud(self.conf.get('os.auth_url')):
#            self.floating_ip = self.nova.create_floating_ip()
#            self.nova.add_floating_ip(self.instance, self.floating_ip)
        self.wait_for_ip()
        self.wait_for_cloud_init()
        self.wait_for_ssh()
        self.setup_over_ssh()

    def hash_setup(self):
        hasher = hashlib.md5()
        # Seed with the digest from the base class to capture common options
        hasher.update(super(NovaServer, self).hash_setup().encode('utf8'))
        options = self.conf.get('nova.setup.digest.options')
        if options:
            for opt in options:
                value = self.conf.get(opt, convert=False)
                self.hash_value(hasher, value)
        return hasher.hexdigest()

    def update_instance(self, nova_id=None):
        if nova_id is None:
            nova_id = self.instance.id
        try:
            # Always query nova to get updated data about the instance
            self.instance = self.nova.get_server_details(nova_id)
            return True
        except Exception:
            logger.debug('Cannot update instance {}'.format(nova_id),
                         exc_info=True)
            # But catch exceptions if something goes wrong. Higher levels will
            # deal with the instance not replying.
            return False

    def wait_for_active_instance(self):
        logger.debug('Waiting for the instance to become active...')
        timeout_limit = time.time() + self.conf.get('nova.boot_timeout')
        while (time.time() < timeout_limit and
               self.instance.status not in ('ACTIVE', 'ERROR')):
            time.sleep(5)
            self.update_instance()
        if self.instance.status != 'ACTIVE':
            msg = 'Instance {instance} never came up (last status: {status})'
            raise NovaServerException(msg, instance=self.instance.id,
                                      status=self.instance.status)

    def nova_id_path(self):
        # FIXME: This should be in self.econf -- vila 2018-01-14
        return os.path.join(self.config_dir_path(), 'nova_id')

    def create_nova_id_file(self, nova_id):
        nova_id_path = self.nova_id_path()
        self.ensure_dir(self.config_dir_path())
        with open(nova_id_path, 'w') as f:
            f.write(nova_id + '\n')

    def discover_ip(self):
        networks = self.instance.networks.values()
        if not networks:
            raise NovaServerException('No network for {instance}',
                                      instance=self.instance.id)
        # The network name is arbitrary, can vary for different clouds
        # but there should be only one network so we get the first one
        # and avoid the need for a config option for the network name.
        # We take the last IP address so it's either the only one or
        # the floating one. In both cases that gives us a reachable IP.
        return networks[0][-1]

    def get_cloud_init_console(self, length=None):
        return self.nova.get_server_console(self.instance, length)

    # FIXME: ~Duplicated with lxc, refactor to extract discovering cloud-init
    # completion (success/failure may be refined later if at least ssh access
    # is provided. In this case, the cloud-init log files can be
    # acquired/analyzed more precisely. This will require refactoring
    # setup(). -- vila 2015-10-25
    def wait_for_cloud_init(self):
        logger.info('Waiting for cloud-init...')
        timeout_limit = (time.time() +
                         self.conf.get('nova.cloud_init_timeout'))
        final_message = self.conf.get('vm.final_message')
        while time.time() < timeout_limit:
            # A relatively cheap way to catch cloud-init completion is to watch
            # the console for the specific message we specified in user-data).
            # FIXME: or at least check that we don't miss when we sleep a
            # significant time between two calls (like on canonistack where we
            # can sleep for minute(s) -- vila 2015-07-17
            console = self.get_cloud_init_console(20)
            if final_message in console:
                # We're good to go
                logger.info(
                    'cloud-init completed for {}'.format(self.instance.id))
                return
            time.sleep(5)
        raise NovaServerException(
            'Instance {instance} never completed cloud-init',
            instance=self.instance.id)

    def start(self):
        super(NovaServer, self).start()
        logger.info('Starting {} nova server...'.format(
            self.conf.get('vm.name')))
        self.nova.start_server(self.instance)
        self.wait_for_ip()
        self.wait_for_ssh()
        self.save_existing_config()

    # MISSINGTEST
    def stop(self):
        logger.info('Stopping {} nova server...'.format(
            self.conf.get('vm.name')))
        self.nova.stop_server(self.instance)
        # FIXME: Should wait for the instance to be shut off -- vila 2016-07-01
        # With a wait parameter defaulting to True ? -- vila 2017-01-20

    def teardown(self, force=False):
        logger.info('Tearing down {} nova server...'.format(
            self.conf.get('vm.name')))
        if force and self.state() == 'RUNNING':
            self.stop()
        if self.instance is not None:
            logger.info('Deleting instance {}'.format(self.instance.id))
            self.nova.delete_server(self.instance.id)
            # FIXME: Should wait for the instance to disappear
            # -- vila 2016-07-01
            self.instance = None
            os.remove(self.nova_id_path())
        if self.floating_ip is not None:
            self.nova.delete_floating_ip(self.floating_ip)
            self.floating_ip = None
        super(NovaServer, self).teardown()
