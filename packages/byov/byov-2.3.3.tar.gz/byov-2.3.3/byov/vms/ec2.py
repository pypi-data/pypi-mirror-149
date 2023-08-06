# This file is part of Build Your Own Virtual machine.
#
# Copyright 2021 Vincent Ladeuil.
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

import hashlib
import logging
import re
import time

import boto3
import botocore

from byov import (
    errors,
    options,
    vms,
)

logger = logging.getLogger(__name__)

# FIXME: There is a x86_64_mac arch but nothing for m1 -- vila 2021-11-29

# aws uses a different nomenclature. Probably closer to linux than ubuntu
# or lxd.
ec2_architectures = dict(
    i386='i386',
    amd64='x86_64',
    arm64='arm64',
)
# Which owners are responsible for producing AMIs
# This is used to filter the huge number of available images.
# 'self' refers to the user creating images
ec2_image_owners = dict(
    # Canonical https://cloud-images.ubuntu.com/locator/ec2/
    ubuntu=['self', '099720109477'],
    # debian-cloud https://wiki.debian.org/Cloud/AmazonEC2Image/
    debian=['self', '136693071363'],
    # alias for several owners
    amazon=['self', 'amazon'],
)


def get_ec2_client(conf):
    session = boto3.session.Session()
    ec2_client = session.client(
        "ec2",
        aws_access_key_id=conf.get('aws.key'),
        aws_secret_access_key=conf.get('aws.secret'),
        aws_session_token=conf.get('aws.token'),
        region_name=conf.get('aws.region'))
    return ec2_client


class Ec2ServerException(errors.ByovError):
    pass


class Ec2Client(object):
    """An ec2 client re-trying requests on known transient failures."""

    def __init__(self, conf, **kwargs):
        self.ec2 = get_ec2_client(conf)

    def retry(self, func, *args, **kwargs):
        # No known transient failures at this point so no retry
        try:
            return func(*args, **kwargs)
        except botocore.exceptions.ClientError as e:
            logger.error('{} failed'.format(func.__name__), exc_info=True)
            raise Ec2ServerException('{name} failed: {boto_exc}',
                                     name=func.__name__, boto_exc=e)

    def instance(self, instance_id):
        res = self.retry(self.ec2.describe_instances,
                         InstanceIds=[instance_id])
        return res['Reservations'][0]['Instances'][0]

    def instance_types(self, types, free_tier):
        func_name = self.instance_types.__name__
        valid_types = []
        pager = self.retry(self.ec2.get_paginator, 'describe_instance_types')
        more = True
        # MISSINGTEST: the NextToken trick requires reducing the number of
        # types response to trigger more calls -- vila 1021-11-26

        # Be prepared to receive a StartingToken.
        pconf = dict()
        while more:
            try:
                for res in self.retry(pager.paginate, InstanceTypes=types,
                                      PaginationConfig=pconf):
                    rtypes = res['InstanceTypes']
                    if not rtypes:
                        more = False
                        break
                    for t in rtypes:
                        if t['FreeTierEligible'] != free_tier:
                            continue
                        valid_types.append(t['InstanceType'])
            except botocore.exceptions.ClientError as e:
                logger.error('{} failed'.format(func_name), exc_info=True)
                raise Ec2ServerException('boto failed: {boto_exc}',
                                         name=func_name, boto_exc=e)
            next_token = res.get('NextToken', None)
            if next_token is None:
                more = False
            else:
                # If there is a NextToken in the last received response, go one
                # more round
                pconf['StartingToken'] = next_token
        return valid_types

    def images(self, arch, owners, image_id=None):
        valid_images = []
        filters = []
        # Reduce the number of images returned by filtering on some known
        # constraints
        filters.append(dict(Name='state', Values=['available']))
        filters.append(dict(Name='virtualization-type', Values=['hvm']))
        filters.append(dict(Name='architecture', Values=[arch]))
        filters.append(dict(Name='image-type', Values=['machine']))
        kwargs = dict(Filters=filters)
        # amazon (an alias for several owners) produces Amazon Linux images
        # Canonical (099720109477) produces ubuntu images
        # RedHat (309956199498) produces RedHat images
        # debian (136693071363) produces Debian 11 (bullseye, stable) and
        # Debian 10 (buster, oldstable)
        # https://wiki.debian.org/Cloud/AmazonEC2Image/

        kwargs['Owners'] = owners
        if image_id is not None:
            kwargs['ImageIds'] = [image_id]

        res = self.retry(self.ec2.describe_images, **kwargs)
        rimgs = res['Images']
        for i in rimgs:
            valid_images.append(i)
        return valid_images

    def create_server(self, name, itype, image_id, user_data, sec_groups,
                      subnet, tags):
        kwargs = dict(MinCount=1, MaxCount=1,
                      TagSpecifications=tags,
                      InstanceType=itype, ImageId=image_id,
                      SecurityGroupIds=sec_groups,
                      SubnetId=subnet,
                      UserData=user_data)
        res = self.retry(self.ec2.run_instances, **kwargs)
        if res['ResponseMetadata']['HTTPStatusCode'] != 200:
            raise Ec2ServerException('{name} creation failed: {res}',
                                     name=name, res=res)
        return res['Instances'][0]['InstanceId']

    def terminate_server(self, instance_id):
        res = self.retry(self.ec2.terminate_instances,
                         InstanceIds=[instance_id])
        if res['ResponseMetadata']['HTTPStatusCode'] != 200:
            raise Ec2ServerException('{id} terminate failed : {res}',
                                     id=instance_id, res=res)

    def start_server(self, instance_id):
        res = self.retry(self.ec2.start_instances,
                         InstanceIds=[instance_id])
        if res['ResponseMetadata']['HTTPStatusCode'] != 200:
            raise Ec2ServerException('{id} start failed : {res}',
                                     id=instance_id, res=res)

    def stop_server(self, instance_id):
        res = self.retry(self.ec2.stop_instances,
                         InstanceIds=[instance_id])
        if res['ResponseMetadata']['HTTPStatusCode'] != 200:
            raise Ec2ServerException('{id} stop failed : {res}',
                                     id=instance_id, res=res)

    def create_image(self, instance_id, image_name, tags):
        res = self.retry(
            self.ec2.create_image, InstanceId=instance_id, Name=image_name,
            TagSpecifications=tags)
        image_id = res['ImageId']
        return image_id

    def deregister_image(self, image_id):
        self.retry(
            self.ec2.deregister_image, ImageId=image_id)

    def delete_snapshot(self, snapshot_id):
        self.retry(self.ec2.delete_snapshot, SnapshotId=snapshot_id)


class Ec2Server(vms.VM):

    ec2_client_class = Ec2Client
    setup_ip_timeouts = 'ec2.setup_ip.timeouts'
    setup_ssh_timeouts = 'ec2.setup_ssh.timeouts'
    existing_vm_options = vms.VM.existing_vm_options + [
        'ec2.image',
        'ec2.image.id',
        'ec2.instance.id',
        'ec2.security.groups',
        'ec2.subnet',
    ]

    def __init__(self, conf):
        super().__init__(conf)
        self.ec2 = self.build_ec2_client()
        self.econf.set('vm.final_message', 'testbed setup completed.')

    def build_ec2_client(self):
        ec2_client = self.ec2_client_class(self.conf)
        return ec2_client

    def state(self):
        instance_id = self.conf.get('ec2.instance.id')
        if instance_id is None:
            return 'UNKNOWN'

        try:
            instance = self.ec2.instance(instance_id)
        except Ec2ServerException:
            logger.error('{} raised'.format(instance_id), exc_info=True)
            return 'UNKNOWN'
        # The instance may remain in the terminated state for some
        # time. stopping and shutting down are transient states but the vm is
        # still running.
        ec2_states = dict(pending='STARTING',
                          running='RUNNING',
                          stopping='STOPPING',
                          stopped='STOPPED',
                          terminated='UNKNOWN')
        ec2_states['shutting-down'] = 'RUNNING'
        return ec2_states[instance['State']['Name']]

    def find_instance_type(self):
        free = self.conf.get('ec2.free_tier')
        wanted_types = self.conf.get('ec2.instance.types')
        if not wanted_types:
            raise Ec2ServerException('ec2.instance.types must be set')
        logger.debug('Searching for a valid instance type in {}'.format(
            ' '.join(wanted_types)))
        existing_types = self.ec2.instance_types(wanted_types, free)
        for t in wanted_types:
            for existing in existing_types:
                if t == existing:
                    return existing
        raise Ec2ServerException(
            'None of [{types}] can be found', types=','.join(wanted_types))

    def find_ec2_image(self, image_id=None):
        """Find the most recent image matching a given name.

        If image_id is set and exists take it even if it doesn't match
        {ec2.image}.
        """
        if image_id is None:
            # Default to the one set by the user if any
            image_id = self.conf.get('ec2.image.id')
        # We want to select an image either by its name, its AMI id or from a
        # combination distribution/release/arch. If several matches are found,
        # the most recent is taken.
        ec2_image_name = self.conf.get('ec2.image')
        if ec2_image_name:
            image_re = re.compile(ec2_image_name)
        else:
            # Use the distribution default
            distro = self.conf.get('vm.distribution')
            regexp = options.ec2_image_re_registry.get(distro)
            image_re = re.compile(self.conf.expand_options(regexp))

        arch = ec2_architectures[self.conf.get('vm.architecture')]
        logger.debug('Searching for image {} {}...'.format(image_re, image_id))
        owners = ec2_image_owners.get(self.conf.get('vm.distribution'),
                                      ['self'])
        existing_images = self.ec2.images(arch, owners, image_id=image_id)
        logger.debug("{} existing images".format(len(existing_images)))
        candidates = []
        for existing in existing_images:
            if image_id and image_id == existing['ImageId']:
                # Shortcut name based selection, user knows better.
                return existing
            m = image_re.search(existing['Name'])
            if m is not None:
                candidates.append(existing)
        if candidates:
            logger.debug("{} candidate images".format(len(candidates)))
            # Use the most recent one
            candidates.sort(key=lambda c: c['CreationDate'], reverse=True)
            return candidates[0]
        if image_id:
            raise Ec2ServerException(
                'Image "{id}" cannot be found', id=image_id)
        else:
            raise Ec2ServerException(
                'No matches for "{name}" can be found', name=image_re)

    def make_tag_specs(self, res_type, *args):
        it = iter(args)
        tag_spec = dict(
            ResourceType=res_type,
            Tags=[dict(Key=k, Value=next(it)) for k in it])
        return tag_spec

    def instance_tags(self):
        # instance name is implemented as a tag: deal with it.
        tag_spec = self.make_tag_specs(
            'instance', 'Name', self.conf.get('vm.name'),
            *self.conf.get('ec2.instance.tags'))
        return [tag_spec]

    def image_tags(self):
        image_tag_spec = self.make_tag_specs(
            'image', 'Name', self.conf.get('vm.name'),
            *self.conf.get('ec2.image.tags'))
        # Also tag the snapshots
        snapshot_tag_spec = self.make_tag_specs(
            'snapshot', 'Name', self.conf.get('vm.name'),
            *self.conf.get('ec2.image.tags'))
        return [image_tag_spec, snapshot_tag_spec]

    # FIXME: This should save the console whether or not the setup fails
    # -- vila 2021-11-30
    def setup(self):
        logger.info('Setting up {} ec2 server...'.format(
            self.conf.get('vm.name')))
        itype = self.find_instance_type()
        image_id = self.find_ec2_image()['ImageId']
        self.create_user_data()
        with open(self._user_data_path) as f:
            user_data = f.read()
        logger.debug('Creating {} ec2 server...'.format(
            self.conf.get('vm.name')))
        instance_id = self.ec2.create_server(
            name=self.conf.get('vm.name'), itype=itype, image_id=image_id,
            user_data=user_data,
            sec_groups=self.conf.get('ec2.security.groups'),
            subnet=self.conf.get('ec2.subnet'),
            tags=self.instance_tags())
        self.econf.set('ec2.instance.id', instance_id)
        self.econf.store.save_changes()  # Recovery checkpoint
        self.wait_for_running_instance()
        self.wait_for_ip()
        self.wait_for_ssh()
        self.wait_for_cloud_init()
        self.setup_over_ssh()

    def hash_setup(self):
        hasher = hashlib.md5()
        # Seed with the digest from the base class to capture common options
        hasher.update(super(Ec2Server, self).hash_setup().encode('utf8'))
        options = self.conf.get('ec2.setup.digest.options')
        if options:
            for opt in options:
                value = self.conf.get(opt, convert=False)
                self.hash_value(hasher, value)
        return hasher.hexdigest()

    def wait_for_state(self, target_states, timeouts_name):
        me = self.wait_for_state.__name__
        vm_name = self.conf.get('vm.name')
        tmouts = self.conf.get(timeouts_name)
        logger.debug('{} {} to reach {} until {}...'.format(
            me, vm_name, target_states, tmouts))
        state = 'UNKNOWN'
        for attempt, sleep in enumerate(tmouts, start=1):
            if attempt > 1:
                logger.debug('Re-trying {} {}/{}'.format(
                    me, attempt, tmouts.retries))
            state = self.state()
            logger.debug('{} is in {} state...'.format(vm_name, state))
            if state in target_states:
                break
            logger.debug('Sleeping {:.2f} seconds for {} {}/{}'.format(
                sleep, me, attempt, tmouts.retries))
            time.sleep(sleep)
        if state not in target_states:
            instance_id = self.conf.get('ec2.instance.id')
            raise Ec2ServerException(
                '{} never reached {} (was: {} last)'.format(
                    instance_id, target_states, state))

    def wait_for_running_instance(self):
        self.wait_for_state(['RUNNING'], 'ec2.boot.timeouts')

    def discover_ip(self):
        instance = self.ec2.instance(self.conf.get('ec2.instance.id'))
        # Just use the public IP for now
        return instance['PublicIpAddress']

    def wait_for_cloud_init(self):
        self._wait_for_cloud_init('ec2.cloud_init.timeouts')

    def wait_for_image_state(self, image_id, target_states, timeouts_name):
        me = self.wait_for_state.__name__
        tmouts = self.conf.get(timeouts_name)
        logger.debug('{} {} to reach {} until {}...'.format(
            me, image_id, target_states, tmouts))
        state = 'unknown'
        for attempt, sleep in enumerate(tmouts, start=1):
            if attempt > 1:
                logger.debug('Re-trying {} {}/{}'.format(
                    me, attempt, tmouts.retries))
                try:
                    image = self.find_ec2_image(image_id)
                    state = image['State']
                    logger.debug('{} is in {} state...'.format(
                        image_id, state))
                    if state in target_states:
                        break
                except Ec2ServerException:
                    logger.error('{} does not exist yet'.format(image_id),
                                 exc_info=True)
            logger.debug('Sleeping {:.2f} seconds for {} {}/{}'.format(
                sleep, me, attempt, tmouts.retries))
            time.sleep(sleep)
        if state not in target_states:
            raise Ec2ServerException(
                '{} never reached {} (was: {} last)'.format(
                    image_id, target_states, state))

    def start(self):
        super(Ec2Server, self).start()
        logger.info('Starting {} ec2 server...'.format(
            self.conf.get('vm.name')))
        self.ec2.start_server(self.conf.get('ec2.instance.id'))
        self.wait_for_running_instance()
        self.wait_for_ip()
        self.wait_for_ssh()
        self.save_existing_config()

    def stop(self):
        logger.info('Stopping {} ec2 server...'.format(
            self.conf.get('vm.name')))
        self.ec2.stop_server(self.conf.get('ec2.instance.id'))
        self.wait_for_state(['STOPPED'], 'ec2.stop.timeouts')

    def teardown(self, force=False):
        logger.info('Tearing down {} ec2 server...'.format(
            self.conf.get('vm.name')))
        if force and self.state() == 'RUNNING':
            self.stop()
        instance_id = self.conf.get('ec2.instance.id')
        if instance_id is not None:
            logger.info('Deleting instance {}'.format(instance_id))
            self.ec2.terminate_server(instance_id)
            self.wait_for_state(['TERMINATED', 'UNKNOWN'],
                                'ec2.terminate.timeouts')
        super(Ec2Server, self).teardown()

    def publish(self):
        image_name = self.conf.get('vm.published_as')
        logger.info('Publishing ec2 image {} from {}...'.format(
            image_name, self.conf.get('vm.name')))
        image_id = self.ec2.create_image(self.conf.get('ec2.instance.id'),
                                         image_name,
                                         tags=self.image_tags())
        self.wait_for_image_state(image_id, ['available'],
                                  'ec2.create_image.timeouts')
        self.econf.set('ec2.published.id', image_id)
        self.econf.store.save_changes()

    def unpublish(self):
        image_name = self.conf.get('vm.published_as')
        image_id = self.conf.get('ec2.published.id')
        if image_id is None:
            return
        logger.info('Un-publishing ec2 image {} {} from {}...'.format(
            image_name, image_id, self.conf.get('vm.name')))
        image = self.find_ec2_image(image_id)
        snapshot_ids = []
        for mappings in image['BlockDeviceMappings']:
            snapshot_id = mappings.get('Ebs', {}).get('SnapshotId', None)
            if snapshot_id is not None:
                snapshot_ids.append(snapshot_id)
        self.ec2.deregister_image(image_id)
        # snaphots used by the image must be deleted after the image is
        # deregistered.
        for snapshot_id in snapshot_ids:
            logger.debug('Deleting snapshot {}'.format(snapshot_id))
            self.ec2.delete_snapshot(snapshot_id)
