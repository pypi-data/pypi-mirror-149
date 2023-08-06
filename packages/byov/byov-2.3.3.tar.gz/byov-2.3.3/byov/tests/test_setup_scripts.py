# This file is part of Build Your Own Virtual machine.
#
# Copyright 2018 Vincent Ladeuil.
# Copyright 2016, 2017 Canonical Ltd.
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

import io
import errno
import os
import sys
import unittest

import byov
from byoc import errors as conf_errors
from byov import (
    config,
    errors,
)
from byov.tests import (
    features,
    fixtures,
)
from byov.vms import lxd


@features.requires(features.tests_config)
class TestWithEphemeralLxd(unittest.TestCase):

    def setUp(self):
        super(TestWithEphemeralLxd, self).setUp()
        fixtures.setup_tests_config(self)
        features.requires_existing_vm(self, 'byov-tests-lxd-ubuntu')
        fixtures.set_uniq_vm_name(self)
        fixtures.override_logging(self)
        # Create a shared config
        conf = config.VmStack(self.vm_name)
        conf.set('vm.name', self.vm_name)
        conf.set('vm.class', 'ephemeral-lxd')
        conf.set('vm.backing', 'byov-tests-lxd-ubuntu')
        conf.store.save()
        conf.store.unload()
        self.vm = lxd.EphemeralLxd(config.VmStack(self.vm_name))
        self.addCleanup(self.vm.stop)
        self.vm.start()


# FIXME: parametrized by distribution -- vila 2017-12-06
class TestUpload(TestWithEphemeralLxd):

    def test_binary_file(self):
        self.vm.upload('/usr/bin/yes', '/home/ubuntu/yes')
        self.assertEqual(
            (0, '', ''),
            self.vm.shell_captured('test', '-f', '/home/ubuntu/yes'))

    def test_unknown_file(self):
        # python2 doesn't have FileNotFoundError
        with self.assertRaises(OSError) as cm:
            self.vm.upload('I-dont-exist', 'not-used')
        self.assertEqual(errno.ENOENT, cm.exception.errno)

    def test_unknown_remote_dir(self):
        # This is mainly testing the error handling for the receiving pipe
        with self.assertRaises(errors.CommandError) as cm:
            self.vm.upload('/usr/bin/yes', '/I-dont-exist/yes')
        self.assertEquals(1, cm.exception.retcode)
        self.assertTrue('/I-dont-exist/yes' in cm.exception.err)

    def test_empty_file(self):
        with open('empty', 'w') as f:
            f.write('')
        self.vm.upload('empty',
                       '/home/{}/empty'.format(self.vm.conf.get('vm.user')))
        self.assertEqual(
            (0, '', ''),
            self.vm.shell_captured(
                'test', '-f',
                '/home/{}/empty'.format(self.vm.conf.get('vm.user'))))


class TestRunScript(TestWithEphemeralLxd):

    # FIXME: Popen(stdout=None) can be redirected so we can't capture it which
    # means this test leaks, disabling until blackbox tests are defined (using
    # the byovm script). -- vila 2016-07-04
    def xtest_simple_script(self):
        with open('script', 'w')as f:
            f.write('#!/bin/sh\nwhoami\n')
        os.chmod('script', 0o755)
        fixtures.patch(self, sys, 'stdout', io.StringIO())
        self.vm.run_script('script', captured=False)

    def test_script_fails_with_params(self):
        fixtures.patch(self, byov, 'path', byov.path + [self.uniq_dir])
        with open('script', 'w')as f:
            f.write('#!/bin/sh\necho $*\nfalse\n')
        os.chmod('script', 0o755)
        with self.assertRaises(errors.CommandError) as cm:
            self.vm.run_script('script', ['foo'])
        self.assertEqual(1, cm.exception.retcode)
        self.assertEqual('foo\n', cm.exception.out)
        self.assertEqual('', cm.exception.err)


class TestSetupScripts(TestWithEphemeralLxd):
    """Test vm.setup_scripts on a started vm as that's faster."""

    def test_no_scripts(self):
        # The following shouldn't fail
        self.vm.run_setup_scripts()

    def test_unknown_script(self):
        self.vm.conf.set('vm.setup_scripts', 'I-dont-exist')
        with self.assertRaises(OSError) as cm:
            self.vm.run_setup_scripts()
        self.assertEquals(errno.ENOENT, cm.exception.errno)
        self.assertTrue('I-dont-exist' in str(cm.exception))

    def test_several_scripts(self):
        fixtures.patch(self, byov, 'path', byov.path + [self.uniq_dir])
        with open('script1', 'w')as f:
            f.write('#!/bin/sh\ntouch script1-ran\n')
        os.chmod('script1', 0o755)
        with open('script2', 'w')as f:
            f.write('#!/bin/sh\ntouch script2-ran\n')
        os.chmod('script2', 0o755)
        self.vm.conf.set('vm.setup_scripts', 'script1, script2')
        self.vm.run_setup_scripts()
        ret, out, err = self.vm.shell_captured('ls', 'script*ran')
        self.assertEqual(0, ret)
        self.assertEqual('script1-ran\nscript2-ran\n', out)
        self.assertEqual('', err)

    def test_expand_options_in_script(self):
        fixtures.patch(self, byov, 'path', byov.path + [self.uniq_dir])
        script_name = 'script1'
        self.vm.conf.set('script_name', script_name)
        with open(script_name, 'w')as f:
            f.write('#!/bin/sh\ntouch {script_name}-ran\n')
        os.chmod(script_name, 0o755)
        self.vm.conf.set('vm.setup_scripts', script_name)
        self.vm.run_setup_scripts()
        ret, out, err = self.vm.shell_captured(
            'ls', '{}*ran'.format(script_name))
        self.assertEqual(0, ret)
        self.assertEqual('{}-ran\n'.format(script_name), out)
        self.assertEqual('', err)

    def test_expansion_error(self):
        fixtures.patch(self, byov, 'path', byov.path + [self.uniq_dir])
        with open('script1', 'w')as f:
            f.write('#!/bin/sh\ntouch {I_dont_exist}-ran\n')
        os.chmod('script1', 0o755)
        self.vm.conf.set('vm.setup_scripts', 'script1')
        with self.assertRaises(conf_errors.ExpandingUnknownOption) as cm:
            self.vm.run_setup_scripts()
        self.assertEqual('I_dont_exist', cm.exception.name)

    def test_home_script(self):
        fixtures.patch(self, byov, 'path', byov.path + [self.home_dir])
        script_path = 'script'
        expanded_script_path = os.path.expanduser('~/' + script_path)
        with open(expanded_script_path, 'w')as f:
            f.write('#!/bin/sh\ntouch script-ran\n')
        os.chmod(expanded_script_path, 0o755)
        self.vm.conf.set('vm.setup_scripts', script_path)
        self.vm.run_setup_scripts()
        ret, out, err = self.vm.shell_captured('ls', 'script*ran')
        self.assertEqual(0, ret)
        self.assertEqual('script-ran\n', out)
        self.assertEqual('', err)
