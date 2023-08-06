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

import hashlib
import logging
import os

from byov import (
    config,
    errors,
    subprocesses,
    vms,
)


logger = logging.getLogger(__name__)


def next_subids(typ, etc_dir=None):
    if etc_dir is None:
        etc_dir = '/etc'
    fname = 'sub{}'.format(typ)
    with open(os.path.join(etc_dir, fname)) as f:
        for line in f.readlines():
            if line.startswith('#'):
                continue
            try:
                user, first, nb = line.strip().split(':')
                first = int(first)
                nb = int(nb)
            except ValueError:
                continue
            yield user, first, nb


def check_id_for(name, the_id, typ, etc_dir=None):
    for user, first, nb in next_subids(typ, etc_dir):
        if user == name and first <= the_id < (first + nb):
            return True
    return False


def available_ids(name, typ, etc_dir=None):
    total = 0
    for user, _, nb in next_subids(typ, etc_dir):
        if user == name:
            # FIXME: Recovering range definitions ? -- vila 2017-01-19
            total += nb
    return total


def user_can_nest(user, level, etc_dir=None):
    # For each level of nesting, a full additional range is needed
    # No nesting still requires a full range
    needed_ids = (level + 1) * 65536
    uids = available_ids(user, 'uid', etc_dir)
    gids = available_ids(user, 'gid', etc_dir)
    return (uids >= needed_ids and gids >= needed_ids)


def check_nesting(level, etc_dir=None):
    root = user_can_nest('root', level, etc_dir)
    lxd = user_can_nest('lxd', level, etc_dir)
    return root and lxd


def lxd_info(vm_name, source=None):
    info = dict(state='UNKNOWN')
    if source is None:
        info_command = ['lxc', 'info', vm_name]
        try:
            _, source, err = subprocesses.run(info_command)
        except errors.CommandError as e:
            if e.err.lower() == 'error: not found\n':
                return info
            else:
                raise
    scanning_ips = False
    for l in source.splitlines():
        if l.startswith('Resources:'):
            # Nothing for us from there
            break
        elif scanning_ips:
            if l == '(none)':
                # interfaces are not setup yet
                continue
            details = l.split('\t')
            try:
                ifce, proto, ip = details[0:3]
                ifce = ifce[0:-1].strip()
            except ValueError:
                raise ValueError('Unexpected IP line: {}'.format(l))
            # FIXME: Assume eth0 until we can do better -- vila 2015-12-22
            if 'eth0' in ifce and proto == 'inet':
                info['ip'] = ip
        elif l.startswith('Status:'):
            _, s = l.split()
            info['state'] = s.upper()
        elif l.startswith('Pid:'):
            _, pid = l.split()
            info['pid'] = pid
        elif l.startswith('Ips:'):
            scanning_ips = True
    return info


class Lxd(vms.VM):

    setup_ip_timeouts = 'lxd.setup_ip.timeouts'
    setup_ssh_timeouts = 'lxd.setup_ssh.timeouts'
    existing_vm_options = vms.VM.existing_vm_options + ['lxd.remote']

    def get_lxd_name(self):
        name = self.conf.get('vm.name')
        remote = self.conf.get('lxd.remote')
        if remote:
            name = '{}:{}'.format(remote, name)
        return name

    def state(self):
        # man lxc(7) defines the possible states as: STOPPED, STARTING,
        # RUNNING, ABORTING, STOPPING. We add UNKNOWN.
        info = lxd_info(self.get_lxd_name())
        return info['state']

    def init(self):
        init_command = ['lxc', 'init', self.conf.get('lxd.image'),
                        self.get_lxd_name()]
        profiles = self.conf.get('lxd.profiles')
        if profiles:
            for p in profiles:
                init_command.extend(['-p', p])
        nesting = self.conf.get('lxd.nesting')
        if not check_nesting(nesting):
            raise errors.ByovError(
                'Lxd needs more ids for {nesting} levels of nesting',
                nesting=nesting)
        if nesting:
            init_command.extend(
                ['--config', 'security.nesting=True'])
        if self.conf.get('lxd.user_mounts'):
            self.check_subids_for_mounts(os.getuid(), os.getgid())
        mac_address = self.conf.get('lxd.mac.address')
        if mac_address:
            # FIXME: Can we do better than eth0 ? -- vila 2018-03-09
            init_command.extend(
                ['--config', 'volatile.eth0.hwaddr={}'.format(mac_address)])
        if self.conf.get('lxd.config.boot.autostart'):
            init_command.extend(['--config', 'boot.autostart=true'])

        logger.debug('Initializing {} lxd container with {}'.format(
            self.conf.get('vm.name'), ' '.join(init_command)))
        # FIXME: Log out & err ? -- vila 2016-01-05
        # FIXME: This can hang IRL (apparently when a new image needs to be
        # downloaded requiring an lxd restart, but this cannot be reliably
        # reproduced so far) and should be guarded by a timeout
        # -- vila 2016-11-16
        return subprocesses.run(init_command)

    def set_cloud_init_config(self):
        self.create_user_data()
        config_command = ['lxc', 'config', 'set', self.get_lxd_name(),
                          'user.user-data', '-']
        logger.debug('Configuring {} lxd container with {}'.format(
            self.conf.get('vm.name'), ' '.join(config_command)))
        subprocesses.run(config_command, cmd_input=self.ci_user_data.dump())

    def check_subids_for_mounts(self, uid, gid, etc_dir=None):
        if not check_id_for('root', uid, 'uid', etc_dir):
            raise errors.SubIdError('uid', uid)
        if not check_id_for('root', gid, 'gid', etc_dir):
            raise errors.SubIdError('gid', gid)

    def get_mount_id_map(self):
        # Declare the needed id mapping.
        huid = self.conf.get('lxd.user_mounts.host.uid')
        hgid = self.conf.get('lxd.user_mounts.host.gid')
        vuid = self.conf.get('lxd.user_mounts.container.uid')
        vgid = self.conf.get('lxd.user_mounts.container.gid')
        # We can't use 'both {host uid/gid} {vm uid/gid}' as uid and gid
        # may differ.
        mapping_template = '{map} {host_id}-{host_id} {vm_id}-{vm_id}'
        uid_map = mapping_template.format(map='uid', host_id=huid, vm_id=vuid)
        gid_map = mapping_template.format(map='gid', host_id=hgid, vm_id=vgid)
        return uid_map, gid_map

    def set_user_mounts(self):
        mounts = self.conf.get('lxd.user_mounts')
        if not mounts:
            return

        config_command = ['lxc', 'config', 'set', self.get_lxd_name(),
                          'raw.idmap', '-']
        mapping = ''.join([m + '\n' for m in self.get_mount_id_map()])
        logger.debug('Configuring {} lxd container with {}'.format(
            self.conf.get('vm.name'),
            ' '.join(config_command) + '\n' + mapping))
        subprocesses.run(config_command, cmd_input=mapping)

        base_command = ['lxc', 'config', 'device', 'add',
                        self.get_lxd_name()]
        for rank, (host_path, vm_path) in enumerate(mounts):
            disk_def = ['byovdisk{}'.format(rank),
                        'disk', 'source={}'.format(host_path),
                        'path={}'.format(vm_path)]
            config_command = base_command + disk_def
            logger.debug('Adding mount for {} with {}'.format(
                self.conf.get('vm.name'), ' '.join(config_command)))
            subprocesses.run(config_command)

    def setup(self):
        logger.info('Setting up {} lxd container...'.format(
            self.conf.get('vm.name')))
        self.init()
        self.set_cloud_init_config()
        self.set_user_mounts()
        self.start()  # calls wait_for_ssh()
        self.wait_for_cloud_init()
        self.setup_over_ssh()

    def hash_setup(self):
        hasher = hashlib.md5()
        # Seed with the digest from the base class to capture common options
        hasher.update(super(Lxd, self).hash_setup().encode('utf8'))
        options = self.conf.get('lxd.setup.digest.options')
        if options:
            for opt in options:
                value = self.conf.get(opt, convert=False)
                self.hash_value(hasher, value)
        return hasher.hexdigest()

    def discover_ip(self):
        info = lxd_info(self.get_lxd_name())
        if info['state'] != 'RUNNING' or 'ip' not in info:
            raise errors.ByovError(
                'Lxd {name} has not provided an IP yet: {info}',
                name=self.get_lxd_name(), info=info)
        return info['ip']

    def wait_for_cloud_init(self):
        self._wait_for_cloud_init('lxd.cloud_init.timeouts')

    def start(self):
        super(Lxd, self).start()
        logger.info('Starting {} lxd container...'.format(
            self.conf.get('vm.name')))
        start_command = ['lxc', 'start', self.get_lxd_name()]
        subprocesses.run(start_command)
        self.wait_for_ip()
        self.wait_for_ssh()
        self.save_existing_config()

    def stop(self):
        logger.info('Stopping {} lxd container...'.format(
            self.conf.get('vm.name')))
        # FIXME: Seen failing with:
        # command: lxc stop --force TestSetupHook-test-hook-success-12702
        # retcode: 1
        # stdout:
        # stderr: Error: websocket: close 1006 (abnormal closure): \
        #                unexpected EOF
        # -- vila 2019-10-16
        stop_command = ['lxc', 'stop', '--force', self.get_lxd_name()]
        subprocesses.run(stop_command)

    def publish(self):
        img_name = self.conf.get('vm.published_as')
        logger.info('Publishing {} lxd image from {}...'.format(
            img_name, self.conf.get('vm.name')))
        publish_command = ['lxc', 'publish', self.get_lxd_name(),
                           '--alias', img_name]
        # FIXME: Seen failing with:
        #   command: lxc publish TestPublish-test-publish-7621 \
        #                --alias TestPublish-test-publish-7621
        # retcode: 1
        # output:
        # error: error: websocket: close 1006 (abnormal closure): \
        #               unexpected EOF
        # -- vila 2018-01-17
        subprocesses.run(publish_command)

    def unpublish(self):
        img_name = self.conf.get('vm.published_as')
        logger.info('Un-publishing {} lxd image from {}...'.format(
            img_name, self.conf.get('vm.name')))
        unpublish_command = ['lxc', 'image', 'delete', img_name]
        subprocesses.run(unpublish_command)

    def teardown(self, force=False):
        logger.info('Tearing down {} lxd container...'.format(
            self.conf.get('vm.name')))
        if force and self.state() == 'RUNNING':
            self.stop()
        teardown_command = ['lxc', 'delete', '--force',
                            self.get_lxd_name()]
        subprocesses.run(teardown_command)
        super(Lxd, self).teardown()


class EphemeralLxd(Lxd):

    def setup(self):
        raise NotImplementedError(self.setup)

    def teardown(self):
        raise NotImplementedError(self.teardown)

    def start(self):
        # /!\ We don't call super(EphemeralLxd,self) ! We just want the Vm one.
        super(Lxd, self).start()
        backing_conf = config.VmStack(self.conf.get('vm.backing'))
        # Inherit basic values from the backing vm. Those /could/ be changed by
        # the user but won't make sense.
        self.conf.set('vm.distribution', backing_conf.get('vm.distribution'))
        self.conf.set('vm.release', backing_conf.get('vm.release'))
        self.conf.set('vm.architecture', backing_conf.get('vm.architecture'))
        # Back to ephemeral specifics:
        mounts = self.conf.get('lxd.user_mounts')
        if mounts and backing_conf.get('lxd.user_mounts'):
            # FIXME: We could have mounts in both backing and the ephemeral but
            # that requires checking which mounts are already set to not add
            # the same volume twice (and also find a better naming scheme to
            # not conflict (byovdiskN needs at least to start above the
            # existing ones) -- vila 2017-01-12

            # FIXME: The solution is one vm.backing.conf.get('lxd.user_mounts')
            # away -- vila 2017-02-04
            raise errors.ByovError(
                'Backing vm {backing} already has mounts',
                backing=self.conf.get('vm.backing'))
        logger.info('Starting {} ephemeral lxd container...'.format(
            self.conf.get('vm.name')))
        # FIXME: This should get vm.published_as from the backing vm
        # -- vila 2019-11-17
        copy_command = ['lxc', 'copy', self.conf.get('vm.backing'),
                        self.get_lxd_name(),
                        '--ephemeral']
        subprocesses.run(copy_command)
        self.set_user_mounts()
        start_command = ['lxc', 'start', self.get_lxd_name()]
        subprocesses.run(start_command)
        self.wait_for_ip()
        self.wait_for_ssh()
        self.setup_over_ssh()

    def stop(self):
        super(EphemeralLxd, self).stop()
        # Stopping an ephemeral deletes it
        self.cleanup_configs()

# MISSINGTEST: Experiment and run tests in qemu where lxd is not installed

# /etc/cloud/cloud.cfg is the defaut config for cloud-init

# /etc/cloud/cloud.cfg.d/90_dpkg.cfg may be worth overriding to avoid searching
# for clouds we don't use
