# This file is part of Build Your Own Virtual machine.
#
# Copyright 2017-2018 Vincent Ladeuil.
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

import errno
import io
import os
import unittest

import byov
from byov import (
    config,
    errors,
)
from byov.tests import (
    features,
    fixtures,
)
from byov.vms import lxd


class TestSetupHook(unittest.TestCase):

    def setUp(self):
        super(TestSetupHook, self).setUp()
        fixtures.setup_tests_config(self)
        features.requires_existing_vm(self, 'byov-tests-lxd-ubuntu')
        fixtures.set_uniq_vm_name(self)
        self.out = io.StringIO()
        self.err = io.StringIO()
        fixtures.override_logging(self)
        # Create a shared config
        conf = config.VmStack(self.vm_name)
        conf.set('vm.name', self.vm_name)
        conf.set('vm.class', 'ephemeral-lxd')
        conf.set('vm.backing', 'byov-tests-lxd-ubuntu')
        conf.store.save()
        conf.store.unload()

    def test_empty_hook(self):
        conf = config.VmStack(self.vm_name)
        conf.set('vm.setup.hook', '')
        self.vm = lxd.EphemeralLxd(conf)
        self.addCleanup(self.vm.stop)
        # Just a smoke test
        self.vm.start()

    def test_non_existing_hook(self):
        conf = config.VmStack(self.vm_name)
        conf.set('vm.setup.hook', 'i-dont-exist')
        self.vm = lxd.EphemeralLxd(conf)
        self.addCleanup(self.vm.stop)
        with self.assertRaises(errors.CommandError) as cm:
            self.vm.start()
        self.assertEqual(127, cm.exception.retcode)
        self.assertEqual('/bin/sh: 1: i-dont-exist: not found\n',
                         cm.exception.err)

    def test_hook_success(self):
        conf = config.VmStack(self.vm_name)
        conf.set('vm.setup.hook', 'ls -d .')
        self.vm = lxd.EphemeralLxd(conf)
        self.addCleanup(self.vm.stop)
        # Just a smoke test
        self.vm.start()

    def test_hook_script_success(self):
        fixtures.patch(self, byov, 'path', byov.path + [self.uniq_dir])
        conf = config.VmStack(self.vm_name)
        conf.set('content', 'true')
        with open('script', 'w') as f:
            f.write('''#!/bin/sh\n{content}\n''')
        os.chmod('script', 0o755)
        conf.set('vm.setup.hook', '@script')
        self.vm = lxd.EphemeralLxd(conf)
        self.addCleanup(self.vm.stop)
        # Just a smoke test
        self.vm.start()

    def test_hook_script_fails(self):
        fixtures.patch(self, byov, 'path', byov.path + [self.uniq_dir])
        conf = config.VmStack(self.vm_name)
        conf.set('content', 'false')
        with open('script', 'w') as f:
            f.write('''#!/bin/sh -e\n{content}\ntrue\n''')
        os.chmod('script', 0o755)
        conf.set('vm.setup.hook', '@script')
        self.vm = lxd.EphemeralLxd(conf)
        self.addCleanup(self.vm.stop)
        with self.assertRaises(errors.CommandError) as cm:
            self.vm.start()
        self.assertEqual(1, cm.exception.retcode)

    def test_hook_non_executable_script_fails(self):
        fixtures.patch(self, byov, 'path', byov.path + [self.uniq_dir])
        conf = config.VmStack(self.vm_name)
        conf.set('content', 'false')
        with open('script', 'w') as f:
            f.write('''#!/bin/sh -e\n{content}\ntrue\n''')
        conf.set('vm.setup.hook', '@script')
        self.vm = lxd.EphemeralLxd(conf)
        self.addCleanup(self.vm.stop)
        with self.assertRaises(PermissionError) as cm:
            self.vm.start()
        self.assertEqual(errno.EACCES, cm.exception.errno)
