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

from byot import (
    features,
    scenarii,
)

from byov import (
    config,
    ssh,
)
from byov.tests import (
    features as vms_features,
    fixtures as vms_fixtures,
)
from byov.vms import lxd


load_tests = scenarii.load_tests_with_scenarios


class TestInfoFromPath(unittest.TestCase):

    scenarios = scenarii.multiply_scenarios(
        # key
        ([('rsa', dict(algo='rsa', key_name='rsa')),
          ('dsa', dict(algo='dsa', key_name='dsa')),
          ('ecdsa', dict(algo='ecdsa', key_name='ecdsa')),
          ('unknown', dict(algo=None, key_name='foo'))]),
        # visibility
        ([('private', dict(visible='private', suffix='')),
          ('public', dict(visible='public', suffix='.pub'))]))

    def assertInfoFromPath(self, expected, key_path):
        self.assertEqual(expected, ssh.infos_from_path(key_path))

    def test_key(self):
        self.assertInfoFromPath((self.algo, self.visible),
                                './{}{}'.format(self.key_name, self.suffix))


@features.requires(vms_features.ssh_feature)
class TestKeyGen(unittest.TestCase):

    scenarios = [('rsa', dict(algo='rsa', prefix='ssh-rsa ',
                              upper_type='RSA')),
                 ('dsa', dict(algo='dsa', prefix='ssh-dss ',
                              upper_type='DSA')),
                 ('ecdsa', dict(algo='ecdsa', prefix='ecdsa-sha2-nistp256 ',
                                upper_type='EC'))]

    def setUp(self):
        super(TestKeyGen, self).setUp()
        vms_fixtures.isolate_from_disk(self)

    def keygen(self, ssh_type, upper_type):
        private_path = os.path.join(self.uniq_dir, ssh_type)
        ssh.keygen(private_path, 'byov@test')
        self.assertTrue(os.path.exists(private_path))
        public_path = private_path + '.pub'
        self.assertTrue(os.path.exists(public_path))
        with open(public_path) as f:
            public = f.read()
        with open(private_path) as f:
            private = f.read()
        if vms_features.ssh_feature.version >= 'OpenSSH_7.9':
            comment_decoration = 'OPENSSH'
        else:
            comment_decoration = upper_type
        self.assertTrue(
            private.startswith('-----BEGIN {} PRIVATE KEY-----\n'.format(
                comment_decoration,)))
        self.assertTrue(
            private.endswith('-----END {} PRIVATE KEY-----\n'.format(
                             comment_decoration,)))
        self.assertTrue(public.endswith(' byov@test\n'))
        return private, public

    def test_key(self):
        private, public = self.keygen(self.algo, self.upper_type)
        self.assertTrue(public.startswith(self.prefix))


class TestSsh(unittest.TestCase):

    def setUp(self):
        super(TestSsh, self).setUp()
        vms_fixtures.setup_tests_config(self)
        vms_features.requires_existing_vm(self, 'byov-tests-lxd-debian')
        vms_fixtures.set_uniq_vm_name(self)
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

    def test_simple_command(self):
        vm = lxd.EphemeralLxd(config.VmStack(self.vm_name))
        self.addCleanup(vm.stop)
        vm.start()
        ret, out, err = vm.shell_captured('whoami')
        self.assertEqual(0, ret)
        self.assertEqual(vm.conf.get('vm.user') + '\n', out)

# test_ssh_no_args (hard, interactive session)
# test_ssh_cant_connect (wrong host, unknown host, missing key, wrong user)
