# This file is part of Build Your Own Virtual machine.
#
# Copyright 2018 Vincent Ladeuil.
# Copyright 2014-2017 Canonical Ltd.
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
import os
import unittest


from byov import (
    config,
    errors,
    vms,
    ssh,
)
from byov.tests import (
    features,
    fixtures,
)


class TestMetaData(unittest.TestCase):

    def setUp(self):
        super(TestMetaData, self).setUp()
        fixtures.isolate_from_disk(self)
        self.conf = config.VmStack('foo')
        self.vm = vms.VM(self.conf)
        images_dir = os.path.join(self.uniq_dir, 'images')
        self.conf.store._load_from_string('''
vm.name=foo
vm.images_dir={images_dir}
'''.format(images_dir=images_dir))

    def test_create_meta_data(self):
        self.vm.create_meta_data()
        self.assertTrue(os.path.exists(self.vm.config_dir_path()))
        self.assertTrue(os.path.exists(self.vm._meta_data_path))
        with open(self.vm._meta_data_path) as f:
            meta_data = f.readlines()
        self.assertEqual(2, len(meta_data))
        self.assertEqual('instance-id: foo\n', meta_data[0])
        self.assertEqual('local-hostname: foo\n', meta_data[1])


class TestCreateUserData(unittest.TestCase):

    def setUp(self):
        super(TestCreateUserData, self).setUp()
        fixtures.setup_tests_config(self)
        self.conf = config.VmStack('foo')
        self.vm = vms.VM(self.conf)

    def test_empty_config(self):
        self.conf.set('vm.name', 'foo')
        self.conf.set('vm.class', 'lxd')
        self.vm.create_user_data()
        self.assertTrue(os.path.exists(self.vm.config_dir_path()))
        self.assertTrue(os.path.exists(self.vm._user_data_path))
        with open(self.vm._user_data_path) as f:
            user_data = f.readlines()
        # We care about the two first lines only here, checking the format (or
        # cloud-init is confused)
        self.assertEqual('#cloud-config-archive\n', user_data[0])
        # yaml seems to flap between different formats changing ' to " and \n
        # to \\n depending on the content length...
        self.assertTrue(user_data[1].startswith('- {content: '))
        self.assertTrue('#cloud-config' in user_data[1])


class TestSeedData(unittest.TestCase):

    def setUp(self):
        super(TestSeedData, self).setUp()
        fixtures.setup_tests_config(self)
        self.conf = config.VmStack('foo')
        self.vm = vms.VM(self.conf)
        self.conf.set('vm.name', 'foo')
        self.conf.set('vm.class', 'lxd')
        self.conf.set('vm.release', 'focal')
        fixtures.override_logging(self)

    def test_create_meta_data(self):
        self.vm.create_meta_data()
        self.assertTrue(os.path.exists(self.vm._meta_data_path))

    def test_create_user_data(self):
        self.vm.create_user_data()
        self.assertTrue(os.path.exists(self.vm._user_data_path))


class TestKeyGen(unittest.TestCase):

    @features.requires(features.ssh_feature)
    def setUp(self):
        super(TestKeyGen, self).setUp()
        fixtures.isolate_from_disk(self)
        self.conf = config.VmStack(None)
        self.vm = vms.VM(self.conf)
        self.config_dir = os.path.join(self.uniq_dir, 'config')

    def load_config(self, more):
        content = '''\
vm.config_dir={config_dir}
vm.name=foo
'''.format(config_dir=self.config_dir)
        self.conf.store._load_from_string(content + more)

    def wrap_ssh_keygen(self):
        self.keygen_called = False

        orig_keygen = ssh.keygen

        def wrapped_key_gen(*args, **kwargs):
            self.keygen_called = True
            return orig_keygen(*args, **kwargs)

        fixtures.patch(self, ssh, 'keygen', wrapped_key_gen)

    def test_do_nothing_if_key_exists(self):
        self.load_config('ssh.server_keys=rsa')
        path = self.conf.get('ssh.server_keys')[0]
        self.wrap_ssh_keygen()
        with open(path, 'w') as f:
            f.write('something')
        self.vm.ssh_keygen()
        self.assertFalse(self.keygen_called)

    def test_recreate_key_if_force(self):
        self.load_config('ssh.server_keys=rsa')
        self.wrap_ssh_keygen()
        path = self.conf.get('ssh.server_keys')[0]
        with open(path, 'w') as f:
            f.write('something')
        self.vm.ssh_keygen(force=True)
        self.assertTrue(self.keygen_called)

    def test_create_key_if_it_doesnt_exist(self):
        self.load_config('ssh.server_keys=rsa')
        self.wrap_ssh_keygen()
        self.vm.ssh_keygen()
        self.assertTrue(self.keygen_called)
        self.assertTrue(os.path.exists('rsa'))
        self.assertTrue(os.path.exists('rsa.pub'))

    def assertKeygen(self, ssh_type, upper_type=None):
        if upper_type is None:
            upper_type = ssh_type.upper()
        self.load_config('ssh.server_keys={vm.config_dir}/' + ssh_type)
        self.vm.ssh_keygen()
        private_path = 'config/{}'.format(ssh_type)
        self.assertTrue(os.path.exists(private_path))
        public_path = 'config/{}.pub'.format(ssh_type)
        self.assertTrue(os.path.exists(public_path))

    def test_dsa(self):
        self.assertKeygen('dsa')

    def test_rsa(self):
        self.assertKeygen('rsa')

    def test_ecdsa(self):
        self.assertKeygen('ecdsa', 'EC')


class TestSSH(unittest.TestCase):

    def setUp(self):
        super(TestSSH, self).setUp()
        fixtures.isolate_from_disk(self)
        self.conf = config.VmStack(None)
        self.vm = vms.VM(self.conf)
        self.config_dir = os.path.join(self.uniq_dir, 'config')

    def load_config(self, more):
        content = '''\
vm.name=foo
ssh.options= # Disable the default value to make tests simpler
'''
        self.conf.store._load_from_string(content + more)

    def test_defaults(self):
        self.load_config('vm.ip = localhost')
        ssh_cmd = self.vm.get_ssh_command('whoami')
        self.assertEqual(
            ['ssh', self.vm.conf.get('vm.user') + '@localhost', 'whoami'],
            ssh_cmd)

    def test_ssh_user(self):
        self.load_config('vm.user = foo\nvm.ip = localhost')
        ssh_cmd = self.vm.get_ssh_command('whoami')
        self.assertEqual(['ssh', 'foo@localhost', 'whoami'], ssh_cmd)


class TestAptUpdate(unittest.TestCase):

    def setUp(self):
        super(TestAptUpdate, self).setUp()
        fixtures.isolate_from_disk(self)
        self.conf = config.VmStack(None)
        self.config_dir = os.path.join(self.uniq_dir, 'config')

        self.conf.store._load_from_string('''vm.update = true''')
        self.vm = vms.VM(self.conf)

    def test_apt_get_update_retries(self):
        self.vm.conf.set('apt.update.timeouts', '0.1, 0.1')
        self.nb_calls = 0

        def failing_update(command):
            self.nb_calls += 1
            if self.nb_calls > 1:
                return 0, 'stdout success', 'stderr success'
            else:
                # Fake a failed apt-get update
                raise errors.CommandError(['boo!'], 1, '', 'I failed')

        self.vm.do_apt_get = failing_update
        self.vm.apt_get_update()
        self.assertEqual(2, self.nb_calls)

    def test_apt_get_update_fails(self):
        self.vm.conf.set('apt.update.timeouts', '0.1, 0.1')
        self.nb_calls = 0

        def failing_update(command):
            self.nb_calls += 1
            raise errors.CommandError(['boo!'], 1, '', 'I failed')

        self.vm.do_apt_get = failing_update
        with self.assertRaises(errors.ByovError) as cm:
            self.vm.apt_get_update()
        self.assertEqual('apt-get update never succeeded',
                         str(cm.exception))
        self.assertEqual(2, self.nb_calls)


class TestWaitForIp(unittest.TestCase):

    def setUp(self):
        super(TestWaitForIp, self).setUp()
        fixtures.isolate_from_disk(self)
        self.conf = config.VmStack(None)
        self.vm = vms.VM(self.conf)

    def set_timeouts(self, value):
        # Use lxd.setup_ip.timeouts to get a TimeoutsOption
        self.conf.set('lxd.setup_ip.timeouts', value)
        self.vm.setup_ip_timeouts = 'lxd.setup_ip.timeouts'

    def test_wait_for_ip_fails(self):
        # Force a 0 timeout so the instance never get an IP
        self.set_timeouts('0, 0, 0')
        with self.assertRaises(errors.ByovError) as cm:
            self.vm.wait_for_ip()
        msg = '{} never received an IP'.format(self.conf.get('vm.name'))
        self.assertEqual(msg, str(cm.exception))

    def test_wait_for_ip_succeed(self):
        self.set_timeouts('0, 0, 1')

        def an_ip():
            return '127.0.0.1'
        self.vm.discover_ip = an_ip
        self.vm.wait_for_ip()
        self.assertEqual('127.0.0.1', self.vm.conf.get('vm.ip'))


# FIXME: parametrized by distribution -- vila 2017-12-06
# FIXME: Because launchpad.login is an ugly duck... -- vila 2016-11-07
# FIXME: Because gitlab.login is an ugly duck... -- vila 2018-07-25
@features.requires(features.bzr_feature)
class TestHashSetup(unittest.TestCase):

    def setUp(self):
        super(TestHashSetup, self).setUp()
        fixtures.isolate_from_disk(self)

    def prepare_vm(self, name='foo'):
        conf = config.VmStack(name)
        conf.set('vm.name', name)
        conf.set('vm.class', 'lxd')
        vm = vms.VM(conf)
        return vm

    def test_defaults(self):
        vm = self.prepare_vm()
        # This should not fail nor produce any output
        vm.hash_setup()

    def test_empty_options(self):
        vm = self.prepare_vm()
        vm.conf.set('vm.setup.digest.options', '')
        self.assertIsNot(None, vm.hash_setup())

    def test_change_name(self):
        foo = self.prepare_vm()
        foo_digest = foo.hash_setup()
        bar = self.prepare_vm('bar')
        bar_digest = bar.hash_setup()
        self.assertNotEqual(foo_digest, bar_digest)

    def test_unknown_file(self):
        vm = self.prepare_vm()
        vm.conf.set('vm.root_script', 'I-dont-exist')
        # This should not fail nor produce any output
        vm.hash_setup()

    def test_file_content_change(self):
        vm = self.prepare_vm()
        vm.conf.set('vm.root_script', 'script')
        with open('script', 'w') as f:
            f.write('do something')
        something = vm.hash_setup()
        with open('script', 'w') as f:
            f.write('do something else')
        something_else = vm.hash_setup()
        self.assertNotEqual(something, something_else)

    def test_file_name_change(self):
        vm = self.prepare_vm()
        vm.conf.set('vm.root_script', 'script')
        with open('script', 'w') as f:
            f.write('do something')
        something = vm.hash_setup()
        os.rename('script', 'tagada')
        vm.conf.set('vm.root_script', 'tagada')
        something_else = vm.hash_setup()
        self.assertEqual(something, something_else)

    def _test_package_file_content_change(self, oname):
        vm = self.prepare_vm()
        vm.conf.set(oname, '@packages')
        with open('packages', 'w') as f:
            f.write('a-package\nanother_package\n')
        something = vm.hash_setup()
        with open('packages', 'w') as f:
            f.write('another-package\n')
        something_else = vm.hash_setup()
        self.assertNotEqual(something, something_else)

    def test_apt_package_file_content_change(self):
        self._test_package_file_content_change('vm.packages')

    def test_pip_package_file_content_change(self):
        self._test_package_file_content_change('pip.packages')
