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
import errno
import io
import os
import unittest

import byov

from byoc import (
    errors as config_errors,
    options,
    registries,
)
from byot import assertions
from byov import (
    commands,
    config,
    errors,
    vms,
)
from byov.tests import fixtures


class TestHelpOptions(unittest.TestCase):

    def setUp(self):
        super(TestHelpOptions, self).setUp()
        self.out = io.StringIO()
        self.err = io.StringIO()

    def parse_args(self, args):
        help_cmd = commands.Help(out=self.out, err=self.err)
        return help_cmd.parse_args(args)

    def test_defaults(self):
        ns = self.parse_args([])
        self.assertEqual([], ns.options)

    def test_single_option(self):
        ns = self.parse_args(['ssh.key'])
        self.assertEqual(['ssh.key'], ns.options)

    def test_several_options(self):
        ns = self.parse_args(['vm.name', 'ssh.key', 'not-an-option'])
        self.assertEqual(['vm.name', 'ssh.key', 'not-an-option'], ns.options)


class TestHelp(unittest.TestCase):

    def setUp(self):
        super(TestHelp, self).setUp()
        self.out = io.StringIO()
        self.err = io.StringIO()
        self.help_cmd = commands.Help(out=self.out, err=self.err)

    def assertHelp(self, expected, args=None):
        if args is None:
            args = []
        self.help_cmd.parse_args(args)
        self.help_cmd.run()
        assertions.assertMultiLineAlmostEqual(self, expected,
                                              self.out.getvalue())

    def test_help_commands(self):
        # Separate first line and its trailing whitespace (go away pep8)
        self.assertHelp('byov.commands: \n' + '''\
\tconfig: Manage a virtual machine configuration.
\tdigest: Display the digest of a virtual machine.
\thelp: Describe byov configuration options.
\tpublish: Publish a virtual machine image.
\tpull: Pull a remote file from an existing virtual machine.
\tpush: Push local file to an existing virtual machine.
\tsetup: Setup a virtual machine.
\tshell: Start a shell, run a command or a script inside a virtual machine.
\tssh-authorize: Authorize a key in the vm for ssh access.
\tssh-register: Register a host in the vm for ssh access.
\tstart: Start an existing virtual machine.
\tstatus: Display the status of a virtual machine.
\tstop: Stop an existing virtual machine.
\tteardown: Teardown a virtual machine.
\tversion: Output the byov version.

''',
                        ['byov.commands'])

    def test_help_help(self):
        with self.assertRaises(SystemExit):
            self.help_cmd.parse_args(['-h'])
        assertions.assertMultiLineAlmostEqual(self, '''\
usage: byov... help [-h] [OPTION [OPTION ...]]

Describe byov configuration options.

positional arguments:
  OPTION      Display help for each option (Topics if none is given).

optional arguments:
  -h, --help  show this help message and exit
''',
                                              self.out.getvalue())

    def test_help_regexp(self):
        self.assertHelp('''\
debian.lxd.image: The debian lxd image to boot from.
debian.package.manager: The package manager for debian.
debian.user: The default user for debian.
debian.user.shell: The default shell on debian.
''',
                        ['debian.*'])

    def test_help_not_matching_regexps(self):
        regexps = ['^IDontExist.*', 'IDoNotExistEither$']
        self.assertHelp('', regexps)
        self.assertEqual(
            'No options matched {}\n'.format(regexps),
            self.err.getvalue())


class FakeVM(vms.VM):
    """A fake VM for tests that doesn't trigger dangerous or costly calls."""

    # Must be set by test (and reset at tearDown)
    states = None

    def __init__(self, conf):
        super(FakeVM, self).__init__(conf)
        self.setup_called = False
        self.start_called = False
        self.shell_called = False
        self.shell_command = None
        self.shell_cmd_args = None
        self.publish_called = False
        self.pull_called = False
        self.pull_remote = None
        self.pull_local = None
        self.push_called = False
        self.push_local = None
        self.push_remote = None
        self.stop_called = False
        self.teardown_called = False

    def state(self):
        return self.states.get(self.conf.get('vm.name'), None)

    def setup(self):
        self.setup_called = True

    def start(self):
        self.start_called = True

    def shell(self, command, *cmd_args):
        self.shell_called = True
        self.shell_command = command
        self.shell_cmd_args = cmd_args
        # Respect signature
        return 0, None, None

    def stop(self):
        self.stop_called = True
        self.states[self.conf.get('vm.name')] = 'shut off'

    def publish(self):
        self.publish_called = True

    def pull(self, remote, local):
        self.pull_called = True
        self.pull_remote = remote
        self.pull_local = local

    def push(self, local, remote):
        self.push_called = True
        self.push_local = local
        self.push_remote = remote

    def teardown(self, force=False):
        self.teardown_called = True


def register_fake_vm(test):
    # Register our fake vm class inside the registry option as that's where it
    # matters.
    vm_reg = options.option_registry.get('vm.class')
    fixtures.patch(test, vm_reg, 'registry', registries.Registry())
    # Only one kind of vm exists in the temporary registry
    vm_reg.registry.register('fake', FakeVM, 'Fake vm')
    FakeVM.states = {}

    def reset_fake_states():
        FakeVM.states = None
    test.addCleanup(reset_fake_states)


def setup_fake_vm_conf(test, name):
    # Define a user config file for the vm
    dir_path = os.path.join(config.user_config_dir(), 'conf.d')
    c_path = os.path.join(dir_path, '{}.conf'.format(name))
    with open(c_path, 'w') as f:
        f.write('''
[{name}]
vm.name={name}
vm.class=fake
vm.release=bionic
vm.architecture=amd64
        '''.format(name=name))
    return config.VmStack(name)


class TestWithVmFoo(unittest.TestCase):

    def setUp(self):
        super(TestWithVmFoo, self).setUp()
        fixtures.isolate_from_disk(self)
        register_fake_vm(self)
        FakeVM.states = {}
        dir_path = os.path.join(config.user_config_dir(), 'conf.d')
        os.makedirs(dir_path)
        self.conf = setup_fake_vm_conf(self, 'foo')
        self.out = io.StringIO()
        self.err = io.StringIO()


class TestVmCommandOptions(TestWithVmFoo):

    def setUp(self):
        super(TestVmCommandOptions, self).setUp()
        self.vm_cmd = commands.VmCommand(out=self.out, err=self.err)

    def parse_args(self, args):
        return self.vm_cmd.parse_args(args)

    def test_nothing(self):
        with self.assertRaises(SystemExit):
            self.parse_args([])

    def test_defaults(self):
        ns = self.parse_args(['foo'])
        self.assertEqual('foo', ns.vm_name)

    def test_overrides(self):
        ns = self.parse_args(['foo', '--option', 'vm.name=bug',
                              '-O', 'foo=bar', '-Obaz=quux'])
        self.assertEqual('foo', ns.vm_name)
        self.assertEqual(['vm.name=bug', 'foo=bar', 'baz=quux', 'vm.name=foo'],
                         ns.overrides)
        # vm.name override has been ignored
        self.assertEqual('foo', self.vm_cmd.vm.conf.get('vm.name'))
        # The other options are available for the vm
        self.assertEqual('bar', self.vm_cmd.vm.conf.get('foo'))
        self.assertEqual('quux', self.vm_cmd.vm.conf.get('baz'))

    def test_error_in_overrides(self):
        with self.assertRaises(SystemExit):
            self.parse_args(['foo', '-O'])
        with self.assertRaises(config_errors.InvalidOverrideError):
            self.parse_args(['foo', '-O', 'toto'])


class TestVmCommand(TestWithVmFoo):

    def run_cmd(self, args):
        vm_cmd = commands.VmCommand()
        vm_cmd.parse_args(args)
        vm_cmd.run()

    def test_unknown(self):
        self.conf.set('vm.name', 'I-dont-exist')
        with self.assertRaises(errors.ByovError):
            self.run_cmd(['I-dont-exist'])

    def test_unknown_vm_class(self):
        self.conf.set('vm.class', 'I-dont-exist')
        with self.assertRaises(errors.InvalidVmClass):
            self.run_cmd(['foo'])


class TestConfigOptions(TestWithVmFoo):

    def parse_args(self, args):
        conf_cmd = commands.Config(out=self.out, err=self.err)
        return conf_cmd.parse_args(args)

    def test_nothing(self):
        with self.assertRaises(SystemExit):
            self.parse_args([])

    def test_defaults(self):
        ns = self.parse_args(['foo'])
        self.assertEqual('foo', ns.vm_name)
        self.assertIs(None, ns.name)
        self.assertFalse(ns.all)
        self.assertFalse(ns.remove)

    def test_name(self):
        ns = self.parse_args(['foo', 'bar'])
        self.assertEqual('bar', ns.name)

    def assertError(self, expected):
        assertions.assertMultiLineAlmostEqual(self, expected,
                                              self.err.getvalue())

    def test_too_much_args(self):
        with self.assertRaises(SystemExit) as cm:
            self.parse_args(['foo', 'bar', 'baz'])
        self.assertEqual(2, cm.exception.code)
        self.assertTrue(self.err.getvalue().endswith(
            'config: error: unrecognized arguments: baz\n'))

    def test_remove_requires_name(self):
        with self.assertRaises(errors.ByovError) as cm:
            self.parse_args(['foo', '--remove'])
        self.assertEqual('--remove expects an option to remove.',
                         str(cm.exception))

    def test_remove_all_fails(self):
        with self.assertRaises(errors.ByovError) as cm:
            self.parse_args(['foo', '--remove', '--all'])
        self.assertEqual('--remove and --all are mutually exclusive.',
                         str(cm.exception))

    def test_set_only_one_option(self):
        with self.assertRaises(errors.ByovError) as cm:
            self.parse_args(['foo', 'bar=baz', '--all'])
        self.assertEqual('Only one option can be set.',
                         str(cm.exception))


class TestConfig(TestWithVmFoo):

    def run_config(self, args):
        cmd_config = commands.Config(out=self.out, err=self.err)
        cmd_config.parse_args(args)
        cmd_config.run()

    def test_set_new_option(self):
        self.assertEqual(None, self.conf.get('foo'))
        self.run_config(['foo', 'foo=bar'])
        self.assertEqual('bar', self.conf.get('foo'))

    def test_set_existing_option(self):
        self.conf.set('foo', 'bar')
        self.assertEqual('bar', self.conf.get('foo'))
        self.run_config(['foo', 'foo=qux'])
        self.assertEqual('qux', self.conf.get('foo'))

    def test_remove_unknown_option(self):
        with self.assertRaises(errors.ConfigOptionNotFound):
            self.run_config(['foo', '-r', 'foo'])

    def test_remove_existing_option(self):
        self.conf.set('bar', 'baz')
        self.run_config(['foo', '-r', 'bar'])
        self.assertEqual(None, self.conf.get('bar'))

    def assertOutput(self, expected):
        assertions.assertMultiLineAlmostEqual(self, expected,
                                              self.out.getvalue())

    def test_list_option(self):
        self.conf.set('foo', 'bar')
        self.run_config(['foo', 'foo'])
        self.assertOutput('bar')

    def test_unknown_option(self):
        with self.assertRaises(errors.ConfigOptionNotFound):
            self.run_config(['foo', 'foo'])
        self.assertOutput('')

    def test_list_that_conf(self):
        self.run_config(['foo'])
        self.assertOutput('''\
.../home/.config/byov/conf.d/foo.conf:
  [foo]
  vm.name = foo
  vm.class = fake
  vm.release = bionic
  vm.architecture = amd64
''')

    def test_more_options(self):
        self.conf.set('one', '1')
        self.conf.set('two', '2')
        self.run_config(['foo'])
        self.assertOutput('''\
.../home/.config/byov/byov.conf:
  [foo]
  one = 1
  two = 2
.../home/.config/byov/conf.d/foo.conf:
  [foo]
  vm.name = foo
  vm.class = fake
  vm.release = bionic
  vm.architecture = amd64
''')

    def test_options_several_sections(self):
        self.conf.store.unload()
        self.conf.store._load_from_string('''\
one = 1
two = 2
[foo]
one = 1
two = foo
[bar]
one = bar
two = foo
''')
        self.run_config(['foo'])
        self.assertOutput('''\
.../home/.config/byov/byov.conf:
  [foo]
  one = 1
  two = foo
.../home/.config/byov/conf.d/foo.conf:
  [foo]
  vm.name = foo
  vm.class = fake
  vm.release = bionic
  vm.architecture = amd64
.../home/.config/byov/byov.conf:
  []
  one = 1
  two = 2
''')

    def test_home_config_not_shown_twice(self):
        self.conf.store.unload()
        self.conf.store._load_from_string('''\
one = 1
[foo]
one = foo
[bar]
one = bar
''')
        self.conf.store.save()
        # Reload the stack from the current dir
        os.chdir('home/.config/byov')
        self.conf = config.VmStack('foo')
        self.run_config(['foo'])
        self.assertOutput('''\
.../home/.config/byov/byov.conf:
  [foo]
  one = foo
.../home/.config/byov/conf.d/foo.conf:
  [foo]
  vm.name = foo
  vm.class = fake
  vm.release = bionic
  vm.architecture = amd64
.../home/.config/byov/byov.conf:
  []
  one = 1
''')

    def test_file_not_found(self):
        with self.assertRaises(errors.ConfigPathNotFound):
            self.run_config(['foo', '@I-dont-exist'])

    def test_file_found(self):
        fname = 'bar'
        with open(fname, 'w') as f:
            f.write('{vm.name}\n')
        self.run_config(['foo', '@bar'])
        self.assertOutput('foo\n')


class TestSetupOptions(TestWithVmFoo):

    def parse_args(self, args):
        setup = commands.Setup(out=self.out, err=self.err)
        return setup.parse_args(args)

    def test_nothing(self):
        with self.assertRaises(SystemExit):
            self.parse_args([])

    def test_defaults(self):
        ns = self.parse_args(['foo'])
        self.assertEqual('foo', ns.vm_name)
        self.assertFalse(ns.download)
        self.assertFalse(ns.ssh_keygen)

    def test_download(self):
        ns = self.parse_args(['foo', '--download'])
        self.assertEqual('foo', ns.vm_name)
        self.assertTrue(ns.download)
        self.assertFalse(ns.ssh_keygen)

    def test_ssh_keygen(self):
        ns = self.parse_args(['foo', '--ssh-keygen'])
        self.assertEqual('foo', ns.vm_name)
        self.assertFalse(ns.download)
        self.assertTrue(ns.ssh_keygen)


class TestSetup(TestWithVmFoo):

    def run_setup(self, args):
        self.setup = commands.Setup(out=self.out, err=self.err)
        self.setup.parse_args(args)
        self.setup.run()

    def test_not_running(self):
        FakeVM.states = {'foo': 'shut off'}
        self.run_setup(['foo'])
        self.assertTrue(self.setup.vm.setup_called)
        self.assertTrue(self.setup.vm.teardown_called)

    def test_while_running(self):
        FakeVM.states = {'foo': 'running'}
        with self.assertRaises(errors.VmRunning):
            self.run_setup(['foo'])
        self.assertFalse(self.setup.vm.setup_called)
        self.assertFalse(self.setup.vm.teardown_called)

    def test_force_while_running(self):
        FakeVM.states = {'foo': 'running'}
        self.run_setup(['--force', 'foo'])
        self.assertFalse(self.setup.vm.stop_called)
        self.assertTrue(self.setup.vm.teardown_called)
        self.assertTrue(self.setup.vm.setup_called)


class TestDigest(TestWithVmFoo):

    def assertOutput(self, expected):
        assertions.assertMultiLineAlmostEqual(self, expected,
                                              self.out.getvalue())

    def test_unknown(self):
        cmd_digest = commands.Digest(out=self.out, err=self.err)
        cmd_digest.parse_args(['I-dont-exist'])
        cmd_digest.run()
        self.assertOutput('UNKNOWN')


class TestStatus(TestWithVmFoo):

    def run_status(self, args):
        status = commands.Status(out=self.out, err=self.err)
        status.parse_args(args)
        status.run()

    def test_not_setup(self):
        FakeVM.states = {'foo': 'UNKNOWN'}
        self.run_status(['foo'])
        self.assertEqual('UNKNOWN\n', self.out.getvalue())

    def test_not_running(self):
        FakeVM.states = {'foo': 'shut off'}
        self.run_status(['foo'])
        self.assertEqual('STOPPED\n', self.out.getvalue())

    def test_running(self):
        FakeVM.states = {'foo': 'running'}
        self.run_status(['foo'])
        self.assertEqual('RUNNING\n', self.out.getvalue())


class TestStart(TestWithVmFoo):

    def run_start(self, args):
        self.start = commands.Start(out=self.out, err=self.err)
        self.start.parse_args(args)
        self.start.run()

    def test_not_running(self):
        FakeVM.states = {'foo': 'shut off'}
        self.run_start(['foo'])
        self.assertTrue(self.start.vm.start_called)

    def test_while_running(self):
        FakeVM.states = {'foo': 'running'}
        with self.assertRaises(errors.VmRunning):
            self.run_start(['foo'])
        self.assertFalse(self.start.vm.start_called)

    def test_unknown(self):
        self.conf.set('vm.name', 'I-dont-exist')
        with self.assertRaises(errors.ByovError):
            self.run_start(['I-dont-exist'])


class TestShellOptions(TestWithVmFoo):

    def parse_args(self, args):
        setup = commands.Shell(out=self.out, err=self.err)
        return setup.parse_args(args)

    def test_defaults(self):
        ns = self.parse_args(['foo'])
        self.assertEqual('foo', ns.vm_name)
        self.assertIsNone(ns.command)
        self.assertEqual([], ns.args)

    def test_command_without_arguments(self):
        ns = self.parse_args(['foo', 'doit'])
        self.assertEqual('foo', ns.vm_name)
        self.assertEqual('doit', ns.command)
        self.assertEqual([], ns.args)

    def test_command_with_arguments(self):
        ns = self.parse_args(['foo', 'doit', '-a', 'b', 'c'])
        self.assertEqual('foo', ns.vm_name)
        self.assertEqual('doit', ns.command)
        self.assertEqual(['-a', 'b', 'c'], ns.args)


class TestShell(TestWithVmFoo):

    def run_shell(self, args):
        self.shell = commands.Shell(out=self.out, err=self.err)
        self.shell.parse_args(args)
        self.shell.run()

    def test_not_running(self):
        FakeVM.states = {'foo': 'shut off'}
        with self.assertRaises(errors.VmNotRunning):
            self.run_shell(['foo'])
        self.assertFalse(self.shell.vm.shell_called)
        self.assertIsNone(self.shell.vm.shell_command)
        self.assertIsNone(self.shell.vm.shell_cmd_args)

    def test_while_running_no_command(self):
        FakeVM.states = {'foo': 'running'}
        self.run_shell(['foo'])
        self.assertTrue(self.shell.vm.shell_called)
        self.assertIsNone(self.shell.vm.shell_command)
        self.assertEqual((), self.shell.vm.shell_cmd_args)

    def test_while_running_with_command(self):
        FakeVM.states = {'foo': 'running'}
        self.run_shell(['foo', 'doit', 'a', 'b', 'c'])
        self.assertTrue(self.shell.vm.shell_called)
        self.assertEqual('doit', self.shell.vm.shell_command)
        self.assertEqual(('a', 'b', 'c'), self.shell.vm.shell_cmd_args)

    def test_unknown(self):
        self.conf.set('vm.name', 'I-dont-exist')
        with self.assertRaises(errors.ByovError):
            self.run_shell(['I-dont-exist'])


class TestPullOptions(TestWithVmFoo):

    def parse_args(self, args):
        setup = commands.Pull(out=self.out, err=self.err)
        return setup.parse_args(args)

    def test_nothing(self):
        with self.assertRaises(SystemExit):
            self.parse_args([])

    def test_defaults(self):
        ns = self.parse_args(['foo', 'remote', 'local'])
        self.assertEqual('foo', ns.vm_name)
        self.assertEqual('remote', ns.remote)
        self.assertEqual('local', ns.local)


class TestPull(TestWithVmFoo):

    def run_pull(self, args):
        self.pull = commands.Pull(out=self.out, err=self.err)
        self.pull.parse_args(args)
        self.pull.run()

    def test_not_running(self):
        FakeVM.states = {'foo': 'shut off'}
        with self.assertRaises(errors.VmNotRunning):
            self.run_pull(['foo', 'remote', 'local'])
        self.assertFalse(self.pull.vm.pull_called)
        self.assertEqual(None, self.pull.vm.pull_remote)
        self.assertEqual(None, self.pull.vm.pull_local)

    def test_while_running(self):
        FakeVM.states = {'foo': 'running'}
        self.run_pull(['foo', 'remote', 'local'])
        self.assertTrue(self.pull.vm.pull_called)
        self.assertEqual('remote', self.pull.vm.pull_remote)
        self.assertEqual('local', self.pull.vm.pull_local)

    def test_unknown(self):
        self.conf.set('vm.name', 'I-dont-exist')
        with self.assertRaises(errors.ByovError):
            self.run_pull(['I-dont-exist', 'local', 'remote'])


class TestPushOptions(TestWithVmFoo):

    def parse_args(self, args):
        setup = commands.Push(out=self.out, err=self.err)
        return setup.parse_args(args)

    def test_nothing(self):
        with self.assertRaises(SystemExit):
            self.parse_args([])

    def test_defaults(self):
        ns = self.parse_args(['foo', 'local', 'remote'])
        self.assertEqual('foo', ns.vm_name)
        self.assertEqual('local', ns.local)
        self.assertEqual('remote', ns.remote)


class TestPush(TestWithVmFoo):

    def run_push(self, args):
        self.push = commands.Push(out=self.out, err=self.err)
        self.push.parse_args(args)
        self.push.run()

    def test_not_running(self):
        FakeVM.states = {'foo': 'shut off'}
        with self.assertRaises(errors.VmNotRunning):
            self.run_push(['foo', 'local', 'remote'])
        self.assertFalse(self.push.vm.push_called)
        self.assertEqual(None, self.push.vm.push_local)
        self.assertEqual(None, self.push.vm.push_remote)

    def test_while_running(self):
        FakeVM.states = {'foo': 'running'}
        self.run_push(['foo', 'local', 'remote'])
        self.assertTrue(self.push.vm.push_called)
        self.assertEqual('local', self.push.vm.push_local)
        self.assertEqual('remote', self.push.vm.push_remote)

    def test_unknown(self):
        self.conf.set('vm.name', 'I-dont-exist')
        with self.assertRaises(errors.ByovError):
            self.run_push(['I-dont-exist', 'local', 'remote'])


class TestStop(TestWithVmFoo):

    def run_stop(self):
        self.stop = commands.Stop(out=self.out, err=self.err)
        self.stop.parse_args(['foo'])
        self.stop.run()

    def test_not_running(self):
        FakeVM.states = {'foo': 'shut off'}
        with self.assertRaises(errors.VmNotRunning):
            self.run_stop()
        self.assertFalse(self.stop.vm.stop_called)

    def test_while_running(self):
        FakeVM.states = {'foo': 'running'}
        self.run_stop()
        self.assertTrue(self.stop.vm.stop_called)

    def test_unknown(self):
        self.conf.set('vm.name', 'I-dont-exist')
        FakeVM.states = {}
        with self.assertRaises(errors.VmUnknown):
            self.run_stop()


class TestPublish(TestWithVmFoo):

    def run_publish(self, args):
        self.publish = commands.Publish(out=self.out, err=self.err)
        self.publish.parse_args(args)
        self.publish.run()

    def test_not_running(self):
        FakeVM.states = {'foo': 'shut off'}
        self.run_publish(['foo'])
        self.assertTrue(self.publish.vm.publish_called)

    def test_while_running(self):
        FakeVM.states = {'foo': 'running'}
        with self.assertRaises(errors.VmRunning):
            self.run_publish(['foo'])
        self.assertFalse(self.publish.vm.publish_called)

    def test_unknown(self):
        self.conf.set('vm.name', 'I-dont-exist')
        FakeVM.states = {}
        with self.assertRaises(errors.ByovError):
            self.run_publish(['I-dont-exist'])


class TestTeardown(TestWithVmFoo):

    def run_teardown(self, args):
        self.teardown = commands.Teardown(out=self.out, err=self.err)
        self.teardown.parse_args(args)
        self.teardown.run()

    def test_not_running(self):
        FakeVM.states = {'foo': 'shut off'}
        self.run_teardown(['foo'])
        self.assertTrue(self.teardown.vm.teardown_called)

    def test_while_running(self):
        FakeVM.states = {'foo': 'running'}
        with self.assertRaises(errors.VmRunning):
            self.run_teardown(['foo'])
        self.assertFalse(self.teardown.vm.teardown_called)

    def test_force_while_running(self):
        FakeVM.states = {'foo': 'running'}
        self.run_teardown(['foo', '--force'])
        self.assertTrue(self.teardown.vm.teardown_called)

    def test_unknown(self):
        self.conf.set('vm.name', 'I-dont-exist')
        FakeVM.states = {}
        with self.assertRaises(errors.ByovError):
            self.run_teardown(['I-dont-exist'])


class TestVersionFunction(unittest.TestCase):

    def test_dev(self):
        self.assertEqual('0.0.1dev8', byov.version((0, 0, 1, 'dev', 8)))

    def test_final(self):
        self.assertEqual('0.0.1', byov.version((0, 0, 1, 'final', 8)))


class TestVersion(unittest.TestCase):

    def setUp(self):
        super(TestVersion, self).setUp()
        self.out = io.StringIO()
        self.err = io.StringIO()
        self.version_cmd = commands.Version(out=self.out, err=self.err)

    def assertVersion(self, expected, args=None):
        if args is None:
            args = []
        self.version_cmd.parse_args(args)
        self.version_cmd.run()
        self.assertEqual(expected, self.out.getvalue())
        self.assertEqual('', self.err.getvalue())

    def test_dev(self):
        fixtures.patch(self, byov, '__version__', (1, 2, 3, 'dev', 4))
        self.assertVersion('1.2.3dev4\n')

    def test_final(self):
        fixtures.patch(self, byov, '__version__', (1, 2, 3, 'final', 4))
        self.assertVersion('1.2.3\n')


class TestSshRegisterOptions(TestWithVmFoo):

    def parse_args(self, args):
        self.register = commands.SshRegister(out=self.out, err=self.err)
        return self.register.parse_args(args)

    def test_nothing(self):
        with self.assertRaises(SystemExit):
            self.parse_args([])

    def test_defaults(self):
        ns = self.parse_args(['foo', 'target'])
        self.assertEqual('foo', ns.vm_name)
        self.assertEqual('rsa', ns.type)
        self.assertEqual('target', ns.host)


class TestSshRegisterErrors(TestWithVmFoo):

    def setUp(self):
        super(TestSshRegisterErrors, self).setUp()
        self.host_conf = setup_fake_vm_conf(self, 'host')

    def run_ssh_register(self, args):
        self.vm = FakeVM(self.conf)
        self.host = FakeVM(self.host_conf)
        self.ssh_register = commands.SshRegister(out=self.out, err=self.err)
        self.ssh_register.parse_args(args)
        self.ssh_register.run()

    def test_unknown(self):
        with self.assertRaises(errors.ByovError):
            self.run_ssh_register(['I-dont-exist', 'host'])

    def test_not_running(self):
        FakeVM.states = {'foo': 'shut off', 'host': 'shut off'}
        with self.assertRaises(errors.VmNotRunning):
            self.run_ssh_register(['foo', 'host'])

    def test_host_unknown(self):
        FakeVM.states = {'foo': 'running'}
        with self.assertRaises(errors.VmUnknown):
            self.run_ssh_register(['foo', 'I-dont-exist'])

    def test_host_not_running(self):
        FakeVM.states = {'foo': 'running', 'host': 'shut off'}
        with self.assertRaises(errors.VmNotRunning):
            self.run_ssh_register(['foo', 'host'])


class TestSshAuthorizeOptions(TestWithVmFoo):

    def parse_args(self, args):
        self.authorize = commands.SshAuthorize(out=self.out, err=self.err)
        return self.authorize.parse_args(args)

    def test_nothing(self):
        with self.assertRaises(SystemExit):
            self.parse_args([])

    def test_defaults(self):
        ns = self.parse_args(['foo', 'key'])
        self.assertEqual('foo', ns.vm_name)
        self.assertEqual('key', ns.key)


class TestSshAuthorizeErrors(TestWithVmFoo):

    def run_ssh_authorize(self, args):
        self.ssh_authorize = commands.SshAuthorize(out=self.out, err=self.err)
        self.ssh_authorize.parse_args(args)
        self.ssh_authorize.run()

    def test_unknown_vm(self):
        with self.assertRaises(errors.ByovError):
            self.run_ssh_authorize(['I-dont-exist', 'not-used'])

    def test_unknown_key(self):
        FakeVM.states = {'foo': 'running'}
        with self.assertRaises(IOError) as cm:
            self.run_ssh_authorize(['foo', 'I-dont-exist'])
        self.assertEqual(errno.ENOENT, cm.exception.errno)
        self.assertEqual('I-dont-exist', cm.exception.filename)
