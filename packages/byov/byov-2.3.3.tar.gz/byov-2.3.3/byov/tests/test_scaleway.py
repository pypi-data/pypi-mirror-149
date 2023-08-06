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

import unittest


from byov import config
from byov.vms import scaleway
from byov.tests import (
    features,
    fixtures,
)


@features.requires(features.scaleway_creds)
class TestIps(unittest.TestCase):

    def setUp(self):
        super(TestIps, self).setUp()
        self.conf = config.VmStack(None)
        self.client = scaleway.ComputeClient(
            self.conf, self.conf.get('scaleway.compute.url'),
            self.conf.get('scaleway.compute.timeouts'))

    def test_list_ips(self):
        # Short of having a dedicated account for tests, little can be assumed
        # about the list content. So this is mostly a smoke test.
        ips = self.client.ips_list()
        if ips:
            # When IPs exist, they all belong to the same organization
            foreigns = []
            organization = self.conf.get('scaleway.access_key')
            for ip in ips:
                if not ip['organization'] == organization:
                    foreigns.append(ip)
            self.assertEqual([], foreigns)

    def test_create_ip(self):
        old_ips = self.client.ips_list()
        nb_ips_before = len(old_ips)
        new_ip = self.client.create_ip()
        self.addCleanup(self.client.delete_ip, new_ip['id'])
        self.assertEqual(self.conf.get('scaleway.access_key'),
                         new_ip['organization'])
        new_ips = self.client.ips_list()
        nb_ips_after = len(new_ips)
        self.assertTrue(nb_ips_after > nb_ips_before,
                        'No IP was created: {} vs {}'.format(
                            old_ips, new_ips))

    def test_delete_ip(self):
        old_ips = self.client.ips_list()
        nb_ips_before = len(old_ips)
        new_ip = self.client.create_ip()
        self.assertEqual(self.conf.get('scaleway.access_key'),
                         new_ip['organization'])
        resp = self.client.delete_ip(new_ip['id'])
        self.assertTrue(resp.ok)
        self.assertEqual(204, resp.status_code)
        new_ips = self.client.ips_list()
        nb_ips_after = len(new_ips)
        self.assertTrue(nb_ips_after == nb_ips_before,
                        'No IP was deleted: {} vs {}'.format(
                            old_ips, new_ips))


@features.requires(features.scaleway_creds)
class TestVmWithIp(unittest.TestCase):

    def setUp(self):
        super(TestVmWithIp, self).setUp()
        fixtures.setup_tests_config(self)
        fixtures.set_uniq_vm_name(self)
        fixtures.override_logging(self)
        # Create a shared config
        self.conf = config.VmStack(self.vm_name)
        self.conf.store._load_from_string('''
[{vm_name}]
vm.name = {vm_name}
vm.class = scaleway
vm.distribution = ubuntu
vm.release = bionic
vm.architecture = amd64
'''.format(vm_name=self.vm_name))
        self.conf.set('scaleway.flavor', 'START1-XS')
        self.conf.set('scaleway.image',
                      '{vm.distribution}/{vm.release}/{vm.architecture}-xs')
        features.test_requires(self, features.ScalewayImage(self.conf))
        self.client = scaleway.ComputeClient(
            self.conf, self.conf.get('scaleway.compute.url'),
            self.conf.get('scaleway.compute.timeouts'))
        self.conf.store.save()
        self.conf.store.unload()

    def test_vm_with_ip(self):
        new_ip = self.client.create_ip()
        self.addCleanup(self.client.delete_ip, new_ip['id'])
        conf = config.VmStack(self.vm_name)
        conf.set('scaleway.public_ip', new_ip['address'])
        conf.set('vm.update', 'false')
        vm = scaleway.Scaleway(conf)
        self.addCleanup(vm.teardown, True)
        vm.setup()
        self.assertEqual(new_ip['address'], vm.conf.get('vm.ip'))
