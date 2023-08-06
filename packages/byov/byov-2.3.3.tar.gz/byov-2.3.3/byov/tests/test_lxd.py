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
import io
import os
import unittest

from byov import (
    commands,
    config,
    errors,
    subprocesses,
)
from byov.tests import (
    features,
    fixtures,
)
from byov.vms import lxd


def lxd_config_get(vm_name, option):
    config_command = ['lxc', 'config', 'get', vm_name, option]
    return subprocesses.run(config_command)


class TestInfo(unittest.TestCase):

    def test_unknown(self):
        info = lxd.lxd_info('idontexist', '')
        self.assertEqual('UNKNOWN', info['state'])

    def test_running(self):
        info = lxd.lxd_info('foo', '''
Name: foo
Architecture: x86_64
Created: 2016/03/23 09:35 UTC
Status: Running
Type: persistent
Profiles: default
Pid: 7821
Processes: 20
Ips:
  eth0:	inet	192.168.0.177	vethMBG5X5
  eth0:	inet6	fe80::216:3eff:fe1e:be0f	vethMBG5X5
  lo:	inet	127.0.0.1
  lo:	inet6	::1
  lxcbr0:	inet	10.0.3.1
  lxcbr0:	inet6	fe80::1833:eff:fe84:a812
Resources:
  Processes: 18
  Disk usage:
    root: 11.24MB
  Memory usage:
    Memory (current): 77.34MB
    Memory (peak): 200.96MB
  Network usage:
    eth0:
      Bytes received: 130.75kB
      Bytes sent: 1.30kB
      Packets received: 885
      Packets sent: 885
    lo:
      Bytes received: 1.22kB
      Bytes sent: 1.22kB
      Packets received: 16
      Packets sent: 16
    lxcbr0:
      Bytes received: 0 bytes
      Bytes sent: 570 bytes
      Packets received: 0
      Packets sent: 0
''')
        self.assertEqual('RUNNING', info['state'])
        self.assertEqual('7821', info['pid'])
        self.assertEqual('192.168.0.177', info['ip'])

    def test_stopped(self):
        info = lxd.lxd_info('foo', '''
Name: foo
Status: Stopped
''')
        self.assertEqual({'state': 'STOPPED'}, info)

    def test_no_ips(self):
        # Before ips are set
        info = lxd.lxd_info('foo', '''
Name: foo
Status: Running
Ips:
(none)
''')
        self.assertEqual({'state': 'RUNNING'}, info)
        self.assertFalse('ip' in info)


@features.requires(features.lxd_client_feature)
class TestConfig(unittest.TestCase):

    def setUp(self):
        super(TestConfig, self).setUp()
        fixtures.setup_tests_config(self)
        fixtures.set_uniq_vm_name(self)
        # Create a shared config
        conf = config.VmStack(None)
        conf.store._load_from_string('''
[{vm_name}]
vm.name = {vm_name}
vm.class = lxd
'''.format(vm_name=self.vm_name))
        conf.store.save()
        conf.store.unload()

    def test_autostart(self):
        vm = lxd.Lxd(config.VmStack(self.vm_name))
        # A real test requires rebooting the host, we just check the default
        # value is the same as lxd itself.
        self.assertEqual(False, vm.conf.get('lxd.config.boot.autostart'))


@features.requires(features.lxd_client_feature)
class TestInit(unittest.TestCase):

    def setUp(self):
        super(TestInit, self).setUp()
        fixtures.setup_tests_config(self)
        fixtures.set_uniq_vm_name(self)
        # Create a shared config
        conf = config.VmStack(None)
        conf.store._load_from_string('''
[{vm_name}]
vm.name = {vm_name}
vm.class = lxd
'''.format(vm_name=self.vm_name))
        conf.store.save()
        conf.store.unload()

    def get_image_id(self, series, arch):
        return lxd.byov_image_name('cloudimg', series, arch)

    def test_unknown_image(self):
        vm = lxd.Lxd(config.VmStack(self.vm_name))
        vm.conf.set('vm.release', 'Idontexist')
        vm.conf.set('vm.architecture', 'amd64')
        with self.assertRaises(errors.CommandError) as cm:
            vm.init()
        # The error message has changed:
        # 2.0: The requested image couldn't be found.
        # 2.5: Couldn't find the requested image
        self.assertIn('he requested image', cm.exception.err)

    def test_known_image(self):
        vm = lxd.Lxd(config.VmStack(self.vm_name))
        vm.conf.set('vm.release', 'bionic')
        vm.conf.set('vm.architecture', 'amd64')
        self.addCleanup(vm.teardown)
        ret, out, err = vm.init()
        self.assertEqual(0, ret)
        self.assertTrue(out.startswith(('Creating {}\n'.format(
            vm.conf.get('vm.name')))))
        self.assertEqual('', err)

    def test_bad_nesting_config(self):
        vm = lxd.Lxd(config.VmStack(self.vm_name))
        # Short of installing testing /etc/sub[ug]id files, using an insane
        # level of nesting.
        vm.conf.set('lxd.nesting', '1024')
        vm.conf.set('vm.release', 'bionic')
        vm.conf.set('vm.architecture', 'amd64')
        with self.assertRaises(errors.ByovError) as cm:
            vm.init()
        self.assertEqual('Lxd needs more ids for 1024 levels of nesting',
                         str(cm.exception))


# FIXME: parametrized by distribution ? -- vila 2017-12-06
@features.requires(features.lxd_client_feature)
class TestSetup(unittest.TestCase):

    def setUp(self):
        super(TestSetup, self).setUp()
        fixtures.setup_tests_config(self)
        fixtures.set_uniq_vm_name(self)
        # Create a shared config
        conf = config.VmStack(self.vm_name)
        conf.set('vm.name', self.vm_name)
        conf.set('vm.class', 'lxd')
        conf.set('vm.release', 'focal')
        conf.set('vm.architecture', 'amd64')
        conf.store.save()
        conf.store.unload()
        fixtures.override_logging(self)

    def get_image_id(self, series, arch):
        return lxd.byov_image_name('cloudimg', series, arch)

    def test_usable(self):
        vm = lxd.Lxd(config.VmStack(self.vm_name))
        self.addCleanup(vm.teardown)
        self.addCleanup(vm.stop)
        vm.setup()
        # We should be able to ssh with the right user
        ret, out, err = vm.shell_captured('whoami')
        self.assertEqual(0, ret)
        self.assertEqual(vm.conf.get('vm.user') + '\n', out)
        # By default, nesting is not set
        ret, out, err = lxd_config_get(self.vm_name, 'security.nesting')
        self.assertEqual(0, ret)
        self.assertEqual('\n', out)
        self.assertEqual('', err)
        # Nor is lxd.remote
        self.assertIs(None, vm.econf.get('lxd.remote'))

    def test_normal_user(self):
        vm = lxd.Lxd(config.VmStack(self.vm_name))
        vm.conf.set('vm.user', 'tester')
        self.addCleanup(vm.teardown)
        self.addCleanup(vm.stop)
        vm.setup()
        # We should be able to ssh with the right user
        ret, out, err = vm.shell_captured('whoami')
        self.assertEqual(0, ret)
        self.assertEqual(vm.conf.get('vm.user') + '\n', out)
        # And sudo
        ret, out, err = vm.shell_captured('sudo whoami')
        self.assertEqual(0, ret)
        self.assertEqual('root\n', out)

    def test_system_user(self):
        vm = lxd.Lxd(config.VmStack(self.vm_name))
        vm.conf.set('vm.user', 'systester')
        vm.conf.set('vm.user.home', '/systester')
        self.addCleanup(vm.teardown)
        self.addCleanup(vm.stop)
        vm.setup()
        # We should be able to ssh with the right user
        ret, out, err = vm.shell_captured('whoami')
        self.assertEqual(0, ret)
        self.assertEqual(vm.conf.get('vm.user') + '\n', out)
        # In the right place
        ret, out, err = vm.shell_captured('pwd')
        self.assertEqual(0, ret)
        self.assertEqual('/systester\n', out)

    @features.requires(features.lxd_nesting_1)
    def test_nesting(self):
        vm = lxd.Lxd(config.VmStack(self.vm_name))
        vm.conf.set('lxd.nesting', '1')
        self.addCleanup(vm.teardown)
        self.addCleanup(vm.stop)
        vm.setup()
        ret, out, err = lxd_config_get(self.vm_name, 'security.nesting')
        self.assertEqual(0, ret)
        self.assertEqual('True\n', out)
        self.assertEqual('', err)

    def test_absolute_user_mounts(self):
        vm = lxd.Lxd(config.VmStack(self.vm_name))
        os.mkdir('testing')
        vm.conf.set('lxd.user_mounts',
                    self.uniq_dir + '/testing:/home/{vm.user}/testing')
        self.addCleanup(vm.teardown)
        self.addCleanup(vm.stop)
        vm.setup()
        ret, out, err = vm.shell_captured('touch testing/inside')
        self.assertEqual(0, ret)
        self.assertEqual('', out)
        self.assertEqual('', err)
        # The file is seen from the host
        self.assertTrue(os.path.exists('testing/inside'))

    def test_relative_user_mounts(self):
        vm = lxd.Lxd(config.VmStack(self.vm_name))
        os.mkdir('testing')
        vm.conf.set('lxd.user_mounts', 'testing:/home/{vm.user}/testing')
        self.addCleanup(vm.teardown)
        self.addCleanup(vm.stop)
        vm.setup()
        ret, out, err = vm.shell_captured('touch testing/inside')
        self.assertEqual(0, ret)
        self.assertEqual('', out)
        self.assertEqual('', err)
        # The file is seen from the host
        self.assertTrue(os.path.exists('testing/inside'))

    def test_homedir_user_mounts(self):
        vm = lxd.Lxd(config.VmStack(self.vm_name))
        os.mkdir('home/testing')
        vm.conf.set('lxd.user_mounts', '~/testing:/home/{vm.user}/testing')
        self.addCleanup(vm.teardown)
        self.addCleanup(vm.stop)
        vm.setup()
        ret, out, err = vm.shell_captured('touch testing/inside')
        self.assertEqual(0, ret)
        self.assertEqual('', out)
        self.assertEqual('', err)
        # The file is seen from the host
        self.assertTrue(os.path.exists('home/testing/inside'))

    # MISSINGTEST: What happens if two vms use the same hwaddr at the same time
    # (or not) ? -- vila 2018-04-23
    def test_hwaddr(self):
        vm = lxd.Lxd(config.VmStack(self.vm_name))
        vm.setup()
        # FIXME: Can we do better than eth0 ? -- vila 2018-04-24
        ret, out, err = lxd_config_get(self.vm_name, 'volatile.eth0.hwaddr')
        self.assertEqual(0, ret)
        self.assertEqual('', err)
        hwaddr = out.strip()
        ip = vm.conf.get('vm.ip')
        vm.teardown(True)
        # Arguably this can fail if the mac address is assigned by lxd to a
        # different container.
        vm.conf.set('lxd.mac.address', hwaddr)
        self.addCleanup(vm.teardown, True)
        vm.setup()
        # FIXME: The test has failed with: AssertionError: '10.242.247.98' !=
        # '10.242.247.99'. I.e. at least thrice, lxd failed to delivered the
        # same IP twice (root cause not understood yet) -- vila 2019-11-15
        self.assertEqual(ip, vm.conf.get('vm.ip'))


@features.requires(features.lxd_client_feature)
class TestCheckSubidsForMountsErrors(unittest.TestCase):
    """Test errors related to sub ids.

    Strictly speaking this should happen in a nested vm so we can change
    /etc/subuid and /ets/subgid. Doing it in the temp directory is easier.
    """
    def setUp(self):
        super(TestCheckSubidsForMountsErrors, self).setUp()
        fixtures.setup_tests_config(self)
        fixtures.set_uniq_vm_name(self)
        # Create a shared config
        conf = config.VmStack(None)
        conf.store._load_from_string('''
[{vm_name}]
vm.name = {vm_name}
vm.class = lxd
vm.release = bionic
vm.architecture = amd64
lxd.user_mounts = .:/work
'''.format(vm_name=self.vm_name))
        conf.store.save()
        conf.store.unload()

    def create_ids(self, uids, gids):
        with open(os.path.join(self.etc_dir, 'subuid'), 'w') as f:
            f.write(uids)
        with open(os.path.join(self.etc_dir, 'subgid'), 'w') as f:
            f.write(gids)

    def test_root_cant_map_uid(self):
        vm = lxd.Lxd(config.VmStack(self.vm_name))
        self.create_ids('', 'root:42:1')
        with self.assertRaises(errors.SubIdError) as cm:
            vm.check_subids_for_mounts(888, 0, self.etc_dir)
        self.assertEqual('uid', cm.exception.typ)
        self.assertEqual(888, cm.exception.subid)

    def test_root_cant_map_gid(self):
        vm = lxd.Lxd(config.VmStack(self.vm_name))
        self.create_ids('root:888:1', 'root:42:1')
        with self.assertRaises(errors.SubIdError) as cm:
            vm.check_subids_for_mounts(888, 888, self.etc_dir)
        self.assertEqual('gid', cm.exception.typ)
        self.assertEqual(888, cm.exception.subid)

    def test_root_can_map(self):
        vm = lxd.Lxd(config.VmStack(self.vm_name))
        self.create_ids('root:888:1', 'root:999:1')
        vm.check_subids_for_mounts(888, 999, self.etc_dir)


# FIXME: parametrized by distribution -- vila 2017-12-06
class TestEphemeralLXD(unittest.TestCase):

    def setUp(self):
        super(TestEphemeralLXD, self).setUp()
        fixtures.setup_tests_config(self)
        features.requires_existing_vm(self, 'byov-tests-lxd-debian')
        fixtures.set_uniq_vm_name(self)
        # Create a shared config
        conf = config.VmStack(None)
        conf.store._load_from_string('''
[{vm_name}]
vm.name = {vm_name}
vm.class = ephemeral-lxd
vm.backing = byov-tests-lxd-debian
'''.format(vm_name=self.vm_name))
        conf.store.save()
        conf.store.unload()

    def test_start(self):
        vm = lxd.EphemeralLxd(config.VmStack(self.vm_name))
        self.addCleanup(vm.stop)
        vm.start()
        self.assertEqual('RUNNING', vm.state())

    def test_stop(self):
        vm = lxd.EphemeralLxd(config.VmStack(self.vm_name))

        def cleanup():
            # vm.start() may fail if no IP can't be acquired (for example). In
            # that case, the container runs and needs to be stopped. If the
            # test succeeds, the vm has already been stopped. This awkward
            # cleanup avoid leaks.
            if vm.state() == 'RUNNING':
                vm.stop()

        self.addCleanup(cleanup)
        vm.start()
        vm.stop()
        # There is a tiny window during which the container can be seen STOPPED
        # before being deleted
        self.assertIn(vm.state(), ('UNKNOWN', 'STOPPED'))

    def test_forbid_lxd_user_mounts_in_both(self):
        conf = config.VmStack('byov-tests-lxd-debian')
        conf.set('lxd.user_mounts', 'home:/work')
        conf.store.save()
        vm = lxd.EphemeralLxd(config.VmStack(self.vm_name))
        vm.conf.set('lxd.user_mounts', '.:/ephemeral')
        # If the backing container has specified lxd.user_mounts, the ephemeral
        # cannot.
        with self.assertRaises(errors.ByovError) as cm:
            vm.start()
        self.assertEqual(
            'Backing vm byov-tests-lxd-debian already has mounts',
            str(cm.exception))

    def test_ephemeral_mounts(self):
        vm = lxd.EphemeralLxd(config.VmStack(self.vm_name))
        os.mkdir('testing')
        vm.conf.set('lxd.user_mounts',
                    self.uniq_dir + '/testing:/home/{vm.user}/testing')
        self.addCleanup(vm.stop)
        vm.start()
        ret, out, err = vm.shell_captured('touch testing/inside')
        self.assertEqual(0, ret)
        self.assertEqual('', out)
        self.assertEqual('', err)
        # The file is seen from the host
        self.assertTrue(os.path.exists('testing/inside'))


class TestNextSubuids(unittest.TestCase):

    def setUp(self):
        super(TestNextSubuids, self).setUp()
        fixtures.isolate_from_disk(self)

    def assertIdRanges(self, expected, content):
        with open(os.path.join(self.etc_dir, 'subuid'), 'w') as f:
            f.write(content)
        self.assertEqual(expected, list(lxd.next_subids('uid', self.etc_dir)))

    def test_unknown(self):
        with self.assertRaises(IOError) as cm:
            list(lxd.next_subids('uid', self.etc_dir))
        # aka FileNotFound (python2 specific)
        self.assertEqual(2, cm.exception.args[0])
        self.assertEqual(errno.ENOENT, cm.exception.errno)

    def test_empty(self):
        self.assertIdRanges([], '')
        self.assertIdRanges([], '\n\n')

    def test_garbage(self):
        self.assertIdRanges([], 'root:foo:2')
        self.assertIdRanges([], 'root:2:foo')

    def test_no_newline(self):
        self.assertIdRanges([('root', 1000, 1)], 'root:1000:1')

    def test_ignore_comments(self):
        self.assertIdRanges([('root', 1000, 1), ('foo', 12, 42)],
                            'root:1000:1\n# foo\nfoo:12:42')


class TestCheckIdFor(unittest.TestCase):

    def setUp(self):
        super(TestCheckIdFor, self).setUp()
        fixtures.isolate_from_disk(self)

    def create_ids(self, typ, ids):
        with open(os.path.join(self.etc_dir, 'sub{}'.format(typ)), 'w') as f:
            f.write(ids)

    def test_present(self):
        self.create_ids('uid', 'root:1000:1')
        self.assertTrue(lxd.check_id_for('root', 1000, 'uid', self.etc_dir))

    def test_absent_from_subgid(self):
        self.create_ids('gid', '')
        self.assertFalse(lxd.check_id_for('root', 1000, 'gid', self.etc_dir))

    def test_absent_from_subuid(self):
        self.create_ids('uid', '')
        self.assertFalse(lxd.check_id_for('root', 1000, 'uid', self.etc_dir))


class TestCheckNesting(unittest.TestCase):

    def setUp(self):
        super(TestCheckNesting, self).setUp()
        fixtures.isolate_from_disk(self)

    def create_ids(self, uids, gids):
        with open(os.path.join(self.etc_dir, 'subuid'), 'w') as f:
            f.write(uids)
        with open(os.path.join(self.etc_dir, 'subgid'), 'w') as f:
            f.write(gids)

    def test_no_nesting(self):
        self.create_ids('root:100000:65536\nlxd:100000:65536\n',
                        'root:100000:65536\nlxd:100000:65536\n')
        self.assertTrue(lxd.check_nesting(0, self.etc_dir))

    def test_nesting_one(self):
        self.create_ids('root:100000:131072\nlxd:100000:131072\n',
                        'root:100000:131072\nlxd:100000:131072\n')
        self.assertTrue(lxd.check_nesting(1, self.etc_dir))

    def test_nesting_two(self):
        self.create_ids('root:100000:196608\nlxd:100000:196608\n',
                        'root:100000:196608\nlxd:100000:196608\n')
        self.assertTrue(lxd.check_nesting(2, self.etc_dir))

    def test_not_enough(self):
        self.create_ids('root:100000:131072\nlxd:100000:131072\n',
                        'root:100000:131072\nlxd:100000:131072\n')
        self.assertFalse(lxd.check_nesting(2, self.etc_dir))


class TestRemoteAdd(unittest.TestCase):

    def setUp(self):
        super(TestRemoteAdd, self).setUp()
        fixtures.setup_tests_config(self)
        features.requires_existing_vm(self, 'byov-lxd-client')
        features.requires_existing_vm(self, 'byov-lxd-server')
        fixtures.set_uniq_vm_name(self)
        self.client_name = 'client-' + self.vm_name
        self.server_name = 'server-' + self.vm_name
        # Create a shared config
        conf = config.VmStack(None)
        conf.store._load_from_string('''
[{client}]
vm.name = {client}
vm.class = ephemeral-lxd
vm.backing = byov-lxd-server
[{server}]
vm.name = {server}
vm.class = ephemeral-lxd
vm.backing = byov-lxd-server
'''.format(client=self.client_name, server=self.server_name))
        conf.store.save()
        conf.store.unload()
        self.client = self.start_ephemeral(self.client_name)
        self.server = self.start_ephemeral(self.server_name)
        self.out = io.StringIO()
        self.err = io.StringIO()
        fixtures.override_logging(self)

    def start_ephemeral(self, vm_name):
        vm = lxd.EphemeralLxd(config.VmStack(vm_name))
        self.addCleanup(vm.stop)
        vm.start()
        return vm

    def shell_on_vm(self, vm_name, args, out=None, err=None):
        if out is None:
            out = self.out
        if err is None:
            err = self.err
        full_cmd = ['shell', vm_name] + args
        ret = commands.run(full_cmd, out=out, err=err)
        msg = 'Cmd {} failed with {}:\n\tstdout: {}\n\tstderr: {}'
        self.assertEqual(0, ret, msg.format(
            full_cmd, ret, out.getvalue(),
            err.getvalue()))
        return ret, out.getvalue(), err.getvalue()

    def shell_on_server(self, args, out=None, err=None):
        return self.shell_on_vm(self.server_name, args, out=out, err=err)

    def test_add_remote(self):
        self.shell_on_server(['lxc config set core.https_address :8443'])
        self.shell_on_server(['lxc config set core.trust_password s3cr3t'])
        server_ip = self.server.conf.get('vm.ip')
        cmd_args = ['remote', 'add', self.server_name,
                    '{}:8443'.format(server_ip),
                    '--password', 's3cr3t', '--accept-certificate']
        ret, out, err = self.client.shell_captured('lxc', *cmd_args)
        msg = 'remote add {} failed with {}:\n\tstdout: {}\n\tstderr: {}'
        self.assertEqual(0, ret, msg.format(cmd_args, ret, out, err))
        _, out, _ = self.client.shell_captured('lxc', 'remote', 'list')
        stem = self.server_name
        self.assertTrue(stem in out, 'Cannot find {} in {}'.format(stem, out))
        stem = 'https://' + server_ip + ':8443'
        self.assertTrue(stem in out, 'Cannot find {} in {}'.format(stem, out))


class TestRemote(unittest.TestCase):

    def setUp(self):
        super(TestRemote, self).setUp()
        fixtures.setup_tests_config(self)
        fixtures.set_uniq_vm_name(self)
        self.lxd_remote = features.requires_remote_lxd(self)
        # Create a shared config
        conf = config.VmStack(self.vm_name)
        conf.set('vm.name', self.vm_name)
        conf.set('vm.class', 'lxd')
        conf.set('vm.distribution', 'ubuntu')
        conf.set('vm.release', 'bionic')
        conf.set('vm.architecture', 'amd64')
        conf.set('lxd.remote', self.lxd_remote)
        conf.store.save()
        conf.store.unload()
        fixtures.override_logging(self)

    def test_setup(self):
        vm = lxd.Lxd(config.VmStack(self.vm_name))
        self.addCleanup(vm.teardown)
        self.addCleanup(vm.stop)
        vm.setup()
        # We should be able to ssh with the right user
        ret, out, err = vm.shell_captured('whoami')
        self.assertEqual(0, ret)
        self.assertEqual(vm.conf.get('vm.user') + '\n', out)
        # The lxd.remote option should be saved.
        self.assertEqual(self.lxd_remote, vm.econf.get('lxd.remote'))

    def test_mount_map_defaults(self):
        # lxd.user_mounts are a bit tricky: the host uid/gid is the remote one
        # so it needs to be overridable.
        vm = lxd.Lxd(config.VmStack(self.vm_name))
        mount_map = vm.get_mount_id_map()
        # The defaults are a bit ubuntu/debian specific (but they may also be
        # valid for other distros (we're not there yet)).
        self.assertEqual(
            ('uid 1000-1000 1000-1000', 'gid 1000-1000 1000-1000'),
            mount_map)
