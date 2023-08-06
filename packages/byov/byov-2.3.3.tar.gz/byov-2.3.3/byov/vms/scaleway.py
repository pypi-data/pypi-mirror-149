# This file is part of Build Your Own Virtual machine.
#
# Copyright 2018 Vincent Ladeuil.
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

import hashlib
import json
import logging
import sys
import time

try:
    import urlparse  # python2
except ImportError:
    from urllib import parse as urlparse

import byov
from byov import (
    errors,
    vms,
)

# FIXME: These are dependencies that need to remain optional so the scaleway
# backend requires them but byov doesn't -- vila 2018-01-14
import requests

logger = logging.getLogger(__name__)


# scaleway uses a different nomenclature. Probably closer to linux than ubuntu
# or lxd.
scaleway_architectures = dict(
    armhf='arm',
    amd64='x86_64',
    arm64='arm64',
)


class ScalewayComputeException(errors.ByovError):
    pass


class Client(object):
    """A client for the scaleway API.

    This is a simple wrapper around requests.Session so we inherit all good
    bits while providing a simple point for tests to override when needed.
    """

    user_agent = 'byov-{} python {}'.format(byov.version(),
                                            sys.version.split()[0])

    session_class = requests.Session

    def __init__(self, conf, root_url, timeouts):
        self.conf = conf
        self.root_url = root_url
        self.timeouts = timeouts
        self.session = self.session_class()

    def request(self, method, url, params=None, headers=None, **kwargs):
        """Overriding base class to handle the root url."""
        # Note that url may be absolute in which case 'root_url' is ignored by
        # urljoin.
        sent_headers = {'User-Agent': self.user_agent,
                        'X-Auth-Token': self.conf.get('scaleway.token'),
                        'Content-Type': 'application/json'}
        if headers is not None:
            sent_headers.update(headers)
        final_url = urlparse.urljoin(self.root_url,
                                     self.conf.expand_options(url))
        response = self.session.request(
            method, final_url, headers=sent_headers, params=params, **kwargs)
        return response

    def get(self, url, **kwargs):
        return self.request('GET', url, **kwargs)

    def post(self, url, data=None, **kwargs):
        if data is not None:
            data = json.dumps(data)
        return self.request('POST', url, data=data, **kwargs)

    def patch(self, url, **kwargs):
        return self.request('PATCH', url, **kwargs)

    def delete(self, url, **kwargs):
        return self.request('DELETE', url, **kwargs)

    def close(self):
        self.session.close()

    def retry(self, func, url, *args, **kwargs):
        req_path = '{} {}'.format(func.__name__.upper(), url)
        no_404_retry = kwargs.pop('no_404_retry', False)
        tmouts = self.timeouts
        for attempt, sleep in enumerate(tmouts, start=1):
            try:
                response = None
                if attempt > 1:
                    logger.debug('Re-trying {} {}/{}'.format(
                        req_path, attempt, tmouts.retries))
                response = func(url, *args, **kwargs)
            except requests.ConnectionError:
                # Most common transient failure: the API server is unreachable
                # (server, network or client may be the cause).
                msg = 'Connection error for {}, will sleep for {:.2f} seconds'
                logger.warning(msg.format(req_path, sleep))
            except Exception:
                # All other exceptions are raised
                logger.error('{} failed'.format(req_path), exc_info=True)
                raise ScalewayComputeException('{req} failed', req=req_path)
            # If the request succeeded return the response (also for the 404
            # special case as instructed).
            if (response is not None and
                (response.ok or (response.status_code == 404 and
                                 no_404_retry))):
                return response
            if response is not None and not response.ok:
                if response.status_code == 429:
                    msg = ('Rate limit reached for {},'
                           ' will sleep for {:.2f} seconds')
                    # This happens rarely but breaks badly if not caught. elmo
                    # recommended a 30 seconds nap in that case.
                    sleep += 30
                    logger.warning(msg.format(req_path, sleep))
                else:
                    # All other errors are raised
                    msg = '{req} failed {status}: {resp}'
                    # Nice spot to debug the API usage
                    logger.error(msg.format(req=req_path,
                                            status=response.status_code,
                                            resp=response),
                                 exc_info=True)
                    # FIXME: Debug, should not land -- vila 2018-01-18
                    sys.stderr.write(
                        msg.format(req=req_path,
                                   status=response.status_code,
                                   resp=response) + '\n')
                    raise ScalewayComputeException(msg, req=req_path,
                                                   status=response.status_code,
                                                   resp=response)
            # Take a nap before retrying
            logger.debug('Sleeping {:.2f} seconds for {} {}/{}'.format(
                sleep, req_path, attempt, tmouts.retries))
            time.sleep(sleep)
        # Raise if we didn't succeed at all
        raise ScalewayComputeException(
            "Failed to '{}' after {} retries".format(req_path, attempt))


class ComputeClient(object):
    """Client for the scaleway compute API."""

    http_class = Client

    def __init__(self, conf, root_url, timeouts):
        self.conf = conf
        self.http = self.http_class(conf, root_url, timeouts)

    def create_server(self, image_id, ip):
        data = dict(name=self.conf.get('vm.name'),
                    organization=self.conf.get('scaleway.access_key'),
                    image=image_id,
                    commercial_type=self.conf.get('scaleway.flavor'),
                    dynamic_ip_required=True,
                    volumes={})
        if ip:
            data['dynamic_ip_required'] = False
            data['public_ip'] = ip['id']
        else:
            data['dynamic_ip_required'] = True
        if self.conf.get('scaleway.boot.local'):
            # MISSINGTESTS: It works and is tested by being the only way to get
            # zfs working on some configurations :-/ No idea (yet) on how to
            # detect it on a running system -- vila 2018-10-15
            data['boot_type'] = 'local'
        response = self.http.retry(self.http.post, 'servers', data=data)
        return response.json()['server']

    def get_server_details(self):
        server_id = self.conf.get('scaleway.server_id')
        if server_id is None:
            # We can't ask about a server that doesn't exist yet
            return None
        response = self.http.retry(
            self.http.get, 'servers/{}'.format(server_id), no_404_retry=True)
        if response.status_code == 404:
            return dict(state='UNKNOWN')
        return response.json()['server']

    def set_user_data(self, key, data):
        return self.http.retry(
            self.http.patch,
            'servers/{}/user_data/{}'.format(
                self.conf.get('scaleway.server_id'), key),
            headers={'Content-Type': 'text/plain'},
            data=data)

    def start_server(self):
        self.action('poweron')

    def stop_server(self):
        # FIXME: Attempting to stop a stopped server 400's.
        self.action('poweroff')

    def terminate_server(self):
        # FIXME: Attempting to stop a stopped server 400's.
        self.action('terminate')

    def action(self, action):
        server_id = self.conf.get('scaleway.server_id')
        if server_id is None:
            # We can't act on a server that doesn't exist
            # FIXME: Building a 404 seems overkill -- vila 2018-01-15
            return None
        response = self.http.retry(
            self.http.post, 'servers/{}/action'.format(server_id),
            data=dict(action=action))
        return response

    def delete_server(self):
        server_id = self.conf.get('scaleway.server_id')
        if server_id is None:
            # We can't delete a server that doesn't exist
            # FIXME: Building a 404 seems overkill -- vila 2018-01-15
            return None
        response = self.http.retry(
            self.http.delete, 'servers/{}'.format(server_id))
        return response

    def delete_volume(self, volume_id):
        # FIXME: no_404_retry ? -- vila 2018-01-17
        response = self.http.retry(
            self.http.delete, 'volumes/{}'.format(volume_id))
        return response

    def create_snapshot(self, volume_id):
        response = self.http.retry(
            self.http.post, 'snapshots',
            data=dict(name=self.conf.get('vm.name'),
                      organization=self.conf.get('scaleway.access_key'),
                      volume_id=volume_id))
        return response.json()['snapshot']

    def delete_snapshot(self, snapshot_id):
        # FIXME: no_404_retry ? -- vila 2018-01-23
        response = self.http.retry(
            self.http.delete, 'snapshots/{}'.format(snapshot_id))
        return response

    def images_list(self):
        response = self.http.retry(self.http.get, 'images')
        while True:
            for image in response.json()['images']:
                yield image
            next_link = response.links.get('next', None)
            if next_link is None:
                break
            response = self.http.retry(self.http.get, next_link['url'])

    def create_image(self, name, arch, snapshot_id):
        response = self.http.retry(
            self.http.post, 'images',
            data=dict(name=name,
                      arch=arch,
                      organization=self.conf.get('scaleway.access_key'),
                      root_volume=snapshot_id))
        return response.json()['image']

    def delete_image(self, image_id):
        # FIXME: no_404_retry ? -- vila 2018-01-23
        response = self.http.retry(
            self.http.delete, 'images/{}'.format(image_id))
        return response

    def ips_list(self):
        response = self.http.retry(self.http.get, 'ips')
        return response.json()['ips']

    def create_ip(self):
        response = self.http.retry(
            self.http.post, 'ips',
            data=dict(organization=self.conf.get('scaleway.access_key')))
        return response.json()['ip']

    def delete_ip(self, ip_id):
        # FIXME: no_404_retry ? -- vila 2018-01-23
        response = self.http.retry(
            self.http.delete, 'ips/{}'.format(ip_id))
        return response


class Scaleway(vms.VM):

    setup_ip_timeouts = 'scaleway.setup_ip.timeouts'
    setup_ssh_timeouts = 'scaleway.setup_ssh.timeouts'

    compute_class = ComputeClient

    def __init__(self, conf):
        super(Scaleway, self).__init__(conf)
        self.compute = self.compute_class(
            self.conf,
            self.conf.get('scaleway.compute.url'),
            self.conf.get('scaleway.compute.timeouts'))
        self.server_id = None

    def state(self):
        # FIXME: The possible values need to be discovered and mapped
        # -- vila 20180-01-14
        # scw inspect can fail IRL just before the server starts and after it
        # shuts down (and can't be used while it's off :-/)
        # Seen IRL:
        # "state": "starting",
        # "state_detail": "provisioning node",
        # "state": "starting",
        # "state_detail": "booting kernel",
        # "state": "running",
        # "state_detail": "booted",
        # "state": "stopping",
        # "state_detail": "rebooting",
        # "state": "stopping",
        # "state_detail": "stopping",
        # curl to the rescue:
        # "state": "stopped"
        # "state_detail": ""
        server = self.compute.get_server_details()
        if server is None:
            return 'UNKNOWN'
        else:
            return server['state'].upper()

    def find_scaleway_image(self, image_name, arch):
        logger.debug('Searching for image {}...'.format(image_name))
        # First match wins
        existing_images = self.compute.images_list()
        for existing in existing_images:
            # FIXME: For convenience/debug, the image id can be used to select
            # a specific image. Beware though that this would allow an attacker
            # to use more recent images similarly named and a different id. In
            # other words: more work is needed to better select images. The
            # hidden assumption here is that the anti-chronological order is
            # convenient ;) -- # vila 2018-05-30
            if ((image_name == existing['name'] or
                 image_name == existing['id']) and arch == existing['arch']):
                logger.debug('Found image {}'.format(existing['id']))
                # More recent images come first. Picking the first match should
                # be the Right Thing.
                return existing
        raise ScalewayComputeException(
            'Image "{}" cannot be found'.format(image_name))

    def find_scaleway_reserved_ip(self, ip):
        logger.debug('Searching for ip {}...'.format(ip))
        # First match wins
        ips = self.compute.ips_list()
        for existing in ips:
            if ip == existing['address'] and existing['server'] is None:
                return existing
        raise ScalewayComputeException(
            'IP "{}" cannot be found'.format(ip))

    def create(self):
        logger.debug('Creating scaleway server {}'.format(
            self.conf.get('vm.name')))
        arch = scaleway_architectures[self.conf.get('vm.architecture')]
        image = self.find_scaleway_image(self.conf.get('scaleway.image'), arch)
        wanted_ip = self.conf.get('scaleway.public_ip')
        if wanted_ip:
            ip = self.find_scaleway_reserved_ip(wanted_ip)
        else:
            ip = None
        server = self.compute.create_server(image['id'], ip)
        self.econf.set('scaleway.server_id', server['id'])

    def set_cloud_init_config(self):
        self.create_user_data()
        logger.debug('Configuring scaleway server {}'.format(
            self.conf.get('vm.name')))
        self.compute.set_user_data('cloud-init', self.ci_user_data.dump())

    def setup(self):
        # We'll save the econf.store often so that when the setup fails, there
        # is something to debug.
        logger.info('Setting up scaleway server {}...'.format(
            self.conf.get('vm.name')))
        self.create()
        self.set_cloud_init_config()
        self.econf.set('scaleway.region_name',
                       self.conf.get('scaleway.region_name'))
        self.econf.store.save_changes()
        self.start()
        self.econf.store.save_changes()
        # MISSINGTEST: with bootstrap=True (though building the images count as
        # a manual but mandatory test to get anywhere -- vila 2018-01-24
        if not self.conf.get('scaleway.image.bootstrap'):
            self.wait_for_cloud_init()
        self.setup_over_ssh()

    def hash_setup(self):
        hasher = hashlib.md5()
        # Seed with the digest from the base class to capture common options
        hasher.update(super(Scaleway, self).hash_setup().encode('utf8'))
        options = self.conf.get('scaleway.setup.digest.options')
        if options:
            for opt in options:
                value = self.conf.get(opt, convert=False)
                self.hash_value(hasher, value)
        return hasher.hexdigest()

    def discover_ip(self):
        ip = None
        server = self.compute.get_server_details()
        state = server['state'].upper()
        public_ip = server.get('public_ip')
        if public_ip:
            ip = public_ip.get('address')
        if state != 'RUNNING' or not ip:
            raise ScalewayComputeException(
                'scaleway server {name} has not provided an IP yet: {state}',
                name=self.conf.get('vm.name'), state=state)
        return ip

    def wait_for_server_reaching(self, expected_states, how_long):
        logger.debug('Waiting for the server {} to reach {} state...'.format(
            self.conf.get('vm.name'), expected_states))
        # An amd64 (but this seems to be the same for all arches) server is in
        # the 'starting' state including 'allocating node' (up to a min),
        # 'provisioning node' (up to a min), 'booting kernel' (10s),
        # 'kernel-started' (5s), 'booted'. It then reaches the 'running' state.
        server = self.compute.get_server_details()
        timeout_limit = time.time() + how_long
        while (time.time() < timeout_limit and
               server['state'].upper() not in expected_states):
            logger.debug(
                'Server state: {state}/{state_detail}'.format(**server))
            time.sleep(5)
            server = self.compute.get_server_details()
        if server['state'].upper() not in expected_states:
            msg = ('Server {id} never reach state {expected_states}'
                   ' (last status: {state}/{state_detail})'.format(
                       expected_states=expected_states, **server))
            raise ScalewayComputeException(msg)
        return server

    def wait_for_cloud_init(self):
        self._wait_for_cloud_init('scaleway.cloud_init.timeouts')

    def start(self):
        super(Scaleway, self).start()
        logger.info('Starting scaleway server {}...'.format(
            self.conf.get('vm.name')))
        self.econf.store.save_changes()  # Recovery checkpoint
        how_long = self.conf.get('scaleway.poweron_timeout')
        timeout_limit = time.time() + how_long
        server = self.compute.get_server_details()
        attempts = 0
        while time.time() < timeout_limit:
            attempts += 1
            self.compute.start_server()
            server = self.wait_for_server_reaching(
                ['RUNNING', 'STOPPED'], how_long)
            if server['state'].upper() == 'STOPPED':
                # It may happen that the 'allocating node' step ends without
                # starting the server (it's just stopped: allocation failed
                # silently). Try again.
                logger.warning(
                    'Server {} allocation failed silently, re-trying'.format(
                        self.conf.get('vm.name')))
                continue
            else:
                break
        if server['state'].upper() != 'RUNNING':
            msg = ('Server {id} never reach state RUNNING'
                   ' (last status: {state}/{state_detail})'
                   ' after {attempts} attempts'.format(attempts=attempts,
                                                       **server))
            raise ScalewayComputeException(msg)

        self.wait_for_ip()
        self.econf.store.save_changes()  # Recovery checkpoint
        self.wait_for_ssh()
        self.save_existing_config()

    def stop(self):
        logger.info('Stopping scaleway server {}...'.format(
            self.conf.get('vm.name')))
        self.compute.stop_server()
        self.wait_for_server_reaching(
            ['STOPPED'], self.conf.get('scaleway.poweroff_timeout'))

        # FIXME: Hmm, volumes are archived by default but when tearing down
        # it's worth skipping the volume archive step as it takes a significant
        # time compared to 'stop --terminate'. In any case, it's probably a
        # good idea to keep track of the existing volumes in self.econf to be
        # able to clean them up by default (the only workflow that needs to
        # keep a boot volume is publish' AFAICS) -- vila 2018-01-14

    def publish(self):
        image_name = self.conf.get('vm.published_as')
        logger.info('Publishing scaleway image {} from {}...'.format(
            image_name, self.conf.get('vm.name')))
        server = self.compute.get_server_details()
        vol0 = server['volumes']['0']
        snapshot = self.compute.create_snapshot(vol0['id'])
        arch = scaleway_architectures[self.conf.get('vm.architecture')]
        image = self.compute.create_image(image_name, arch, snapshot['id'])
        return image

    def unpublish(self):
        image_name = self.conf.get('vm.published_as')
        logger.info('Un-publishing scaleway image {} from {}...'.format(
            image_name, self.conf.get('vm.name')))
        arch = scaleway_architectures[self.conf.get('vm.architecture')]
        image = self.find_scaleway_image(image_name, arch)
        snapshot_id = image['root_volume']['id']
        self.compute.delete_image(image['id'])
        self.compute.delete_snapshot(snapshot_id)

    def teardown(self, force=False):
        logger.info('Tearing down {} scaleway server...'.format(
            self.conf.get('vm.name')))
        if force and self.state() == 'RUNNING':
            self.compute.terminate_server()
            self.wait_for_server_reaching(
                ['UNKNOWN'], self.conf.get('scaleway.terminate_timeout'))
        else:
            # Get the server description before deletion
            server = self.compute.get_server_details()
            self.compute.delete_server()
            # Clean up the volumes
            # MISSINGTEST: race with server deletion ? what if server deletion
            # somehow deleted some volumes ? -- vila 2018-01-17
            if server['volumes']:
                for volume in server['volumes'].values():
                    self.compute.delete_volume(volume['id'])
        super(Scaleway, self).teardown()
        # FIXME: Beware of volume leaks -- vila 2018-01-14
