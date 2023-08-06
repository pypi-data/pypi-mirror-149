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
import argparse
import errno
import logging
import re
import sys

import byov

from byoc import (
    errors as config_errors,
    registries,
)
from byov import (
    config,
    errors,
    options,
)
from byov.vms import (
    docker,
    scaleway,
    qemu,
    lxd,
)


logger = logging.getLogger(__name__)


# The available vm backends are registered here to ensure the config registry
# is loaded before we try to use it.
options.vm_class_registry.register('docker', docker.Docker,
                                   'docker container')
# FIXME: qemu really requires qemu-system-x86_64, qemu-img and genisoimage
# (respectively in packages qemu-system-x86, qemu-utils and genisoimage). This
# should be handled as a soft-dependency -- vila 2019-10-17
options.vm_class_registry.register('qemu', qemu.Qemu,
                                   'QEMU-based virtual machine')
options.vm_class_registry.register('lxd', lxd.Lxd,
                                   'Lxd virtual machine')
options.vm_class_registry.register('ephemeral-lxd', lxd.EphemeralLxd,
                                   'Linux container ephemeral virtual machine')
options.vm_class_registry.register('scaleway', scaleway.Scaleway,
                                   'Scaleway server')
if sys.version_info < (3,):
    try:
        from byov.vms import nova
    except ImportError:
        # No novaclient, no nova vms.
        pass
    else:
        # Only register nova if novaclient is available
        options.vm_class_registry.register(
            'nova', nova.NovaServer, 'Openstack Nova instance')

try:
    from byov.vms import ec2
except ImportError:
        # No boto3, no ec2 vms.
        pass
else:
    # Only register ec2 if boto3 is available
    options.vm_class_registry.register(
        'ec2', ec2.Ec2Server, 'Aws Ec2 instance')

# Import byov.conf.d/byov.py files so additional options (or other tweaks to
# byov.config) can be loaded.

# FIXME: This seems to be involved in failures at test import time, making it
# hard to debug. Conceptually, this may be delayed until a VmStack is needed
# -- vila 2022-04-06
config.import_user_byovs()


class ArgParser(argparse.ArgumentParser):
    """A parser for the byovm script."""

    def __init__(self, name, description):
        script_name = 'byov'
        super(ArgParser, self).__init__(
            prog='{} {}'.format(script_name, name),
            description=description)

    def parse_args(self, args=None, out=None, err=None):
        """Parse arguments, overridding stdout/stderr if provided.

        python argparse uses stdout and stderr for user convenience. For tests
        though, they need to be overriden so test can make assertion on their
        content.

        :params args: Defaults to sys.argv[1:].

        :param out: Defaults to sys.stdout.

        :param err: Defaults to sys.stderr.

        """
        out_orig = sys.stdout
        err_orig = sys.stderr
        try:
            if out is not None:
                sys.stdout = out
            if err is not None:
                sys.stderr = err
            return super(ArgParser, self).parse_args(args)
        finally:
            sys.stdout = out_orig
            sys.stderr = err_orig

    def parse_known_args(self, args=None, out=None, err=None):
        """Parse known arguments, overridding stdout/stderr if provided.

        :params args: Defaults to sys.argv[1:].

        :param out: Defaults to sys.stdout.

        :param err: Defaults to sys.stderr.
        """
        out_orig = sys.stdout
        err_orig = sys.stderr
        try:
            if out is not None:
                sys.stdout = out
            if err is not None:
                sys.stderr = err
            return super(ArgParser, self).parse_known_args(args)
        finally:
            sys.stdout = out_orig
            sys.stderr = err_orig


class CommandRegistry(registries.Registry):
    """A registry specialized for commands."""

    def register(self, cmd):
        super(CommandRegistry, self).register(
            cmd.name, cmd, help_string=cmd.description)


# All commands are registered here, defining what run() supports
command_registry = CommandRegistry()


class Command(object):

    name = 'Must be set by daughter classes'
    description = 'Must be set by daughter classes'

    def __init__(self, out=None, err=None):
        """Command constructor.

        :param out: A stream for command output.

        :param err: A stream for command errors.
        """
        if out is None:
            out = sys.stdout
        if err is None:
            err = sys.stderr
        self.out = out
        self.err = err
        self.parser = ArgParser(self.name, self.description)

    def parse_args(self, args):
        self.options = self.parser.parse_args(args, self.out, self.err)
        return self.options


class Help(Command):

    name = 'help'
    description = 'Describe byov configuration options.'

    def __init__(self, **kwargs):
        super(Help, self).__init__(**kwargs)
        # FIXME: Support regexps -- vila 2017-02-02
        self.parser.add_argument(
            'options', metavar='OPTION', nargs='*',
            help='Display help for each option'
            ' (Topics if none is given).')

    def run(self):
        if not self.options.options:
            self.out.write('Available Topics:\n')
            # Topics are only the ones known to byov.

            # FIXME: There should be a way to declare a topic for the user
            # -- vila 2018-11-04
            for topic in ['logging',
                          'vm', 'ec2', 'qemu', 'scaleway', 'nova', 'lxd',
                          'apt', 'ssh',
                          'launchpad', 'gitlab',
                          'debian', 'ubuntu']:
                names = [name for name, help
                         in options.option_registry.help.items()
                         if name.startswith(topic + '.')]
                self.out.write('\n{}\n'.format(topic))
                self.out.write('{}\n'.format('=' * len(topic)))
                for name in names:
                    option = options.option_registry.get(name)
                    self.out.write('{}: {}\n'.format(name, option.help))
            return
        # But all options are valid here, including the user-defined ones
        matched = set()
        for regexp in self.options.options:
            matcher = re.compile(regexp)
            for name in options.option_registry.keys():
                if name not in matched and matcher.search(name):
                    matched.add(name)
        if matched:
            for name in sorted(matched):
                option = options.option_registry.get(name)
                self.out.write('{}: {}\n'.format(name, option.help))
        else:
            msg = 'No options matched {}\n'.format(self.options.options)
            self.err.write(msg)
            return 1
        return 0


command_registry.register(Help)


class Version(Command):

    name = 'version'
    description = 'Output the byov version.'

    def run(self):
        self.out.write(byov.version() + '\n')
        return 0


command_registry.register(Version)


class VmCommand(Command):
    """A command applying to a given vm.

    This is not a command by itself but a base class for concrete commands.
    """

    def __init__(self, **kwargs):
        super(VmCommand, self).__init__(**kwargs)
        self.parser.add_argument(
            'vm_name',
            help='Virtual machine section in the configuration file.')
        self.parser.add_argument(
            '--option', '-O', metavar='OPTION=VALUE',
            action='append', dest='overrides', default=[],
            help='Override OPTION with provided VALUE. Can be repeated.')
        # override vm.name ?
        # Support @ containing lines of name=value and comments (aka a config
        # file including sections) or just -C <path>.conf ?

    def parse_args(self, args):
        super(VmCommand, self).parse_args(args)
        self.vm = None
        self.parse_vm_arg()
        return self.options

    def parse_vm_arg(self):
        self.vm_name = self.options.vm_name

        conf = config.VmStack(self.vm_name)
        # Append vm.name to overrides (which means it can't be overridden with
        # -O)
        self.options.overrides.append('vm.name={}'.format(self.vm_name))
        conf.cmdline_store.from_cmdline(self.options.overrides)
        try:
            kls_name = conf.get('vm.class', convert=False)
        except config_errors.OptionMandatoryValueError:
            # FIXME: In practice, this happens when the user makes a typo or
            # when running from the wrong place (where the vm is not defined in
            # any visible file) -- vila 2016-08-30
            raise errors.ByovError('"{name}" must define vm.class.',
                                   name=self.vm_name)
        # Even if defined, the value may be wrong
        try:
            kls = conf.get('vm.class')
        except config_errors.OptionMandatoryValueError:
            raise errors.InvalidVmClass(self.vm_name, kls_name)
        self.vm = kls(conf)
        # Now that we know the vm, we may configure logging 'logging' is not
        # configured until we reach this point, this means errors occuring
        # before this point can be logged without the user specified options.
        log_level = self.vm.conf.get('logging.level')
        log_format = self.vm.conf.get('logging.format')
        logging.basicConfig(level=log_level, format=log_format)
        return


class Config(VmCommand):

    name = 'config'
    description = 'Manage a virtual machine configuration.'

# FIXME: The full help should be the following but that doesn't fit well with
# the Help command for now -- vila 2014-03-26

# FIXME: Maybe a better way would be to delegate help handling to each command
# (instead of a single help command). From there, 'help config' could accept an
# option name or regexp and display the help for the matching options.
# -- vila 2013-08-30

# Display the active value for option NAME.
#
# If NAME is not given, --all .* is implied (all options are displayed).
#
# If --all is specified, NAME is interpreted as a regular expression and all
# matching options are displayed (without resolving option references in the
# value). The active value is the first one displayed for each option.
#
# NAME=value without spaces sets the value.
#
# --remove NAME remove the option definition.

    def __init__(self, **kwargs):
        super(Config, self).__init__(**kwargs)
        self.parser.add_argument(
            'name', nargs='?', help='''The option name.''')
        self.parser.add_argument(
            '--remove', '-r', action="store_true", help='Remove the option.'),
        self.parser.add_argument(
            '--all', '-a', action="store_true",
            help='Display all the defined values for the matching options.'),

    def parse_args(self, args):
        # Work around argparse not providing a proper way to mix positional
        # arguments and options. If an option arg is used, the 'name'
        # positional arg is not set and ends up in 'rest'.
        self.options, rest = self.parser.parse_known_args(
            args, self.out, self.err)
        self.parse_vm_arg()
        o = self.options
        if o.all or o.remove:
            # Get 'name' back from 'rest' if available
            if rest:
                o.name = rest.pop(0)
        # If we still have args left, it's an error
        if rest:
            err_orig = sys.stderr
            try:
                sys.stderr = self.err
                msg = 'unrecognized arguments: {}'
                self.parser.error(msg.format(' '.join(rest)))
            finally:
                sys.stderr = err_orig
        # Raise errors on option incompatibilities.
        if o.remove:
            if o.all:
                raise errors.ByovError(
                    '--remove and --all are mutually exclusive.')
            if o.name is None:
                raise errors.ByovError(
                    '--remove expects an option to remove.')
        if o.name is not None and '=' in o.name:
            if o.all:
                raise errors.ByovError('Only one option can be set.')
        return o

    def list(self, name):
        # Display the value as a string
        value = self.vm.conf.get(name, expand=True, convert=False)
        if value is not None:
            # No quoting needed (for now)
            self.out.write(value)
        else:
            raise errors.ConfigOptionNotFound(name)

    def list_matching(self, re_str):
        not_a_section_id = object()
        cur_store_id = None
        cur_section_id = not_a_section_id
        names = re.compile(re_str)
        for (store, section, name, value) in self.vm.conf.iter_options():
            if names.search(name) is None:
                # not matching option, ignore
                continue
            if cur_store_id != store.id:
                # Explain where the options are defined
                self.out.write('{}:\n'.format(store.id,))
                cur_store_id = store.id
                cur_section_id = not_a_section_id
            if (cur_section_id != section.id):
                if section.id is None:
                    section_displayed = ''
                else:
                    section_displayed = section.id
                # Display the section id as it appears in the store
                self.out.write('  [{}]\n'.format(section_displayed))
            cur_section_id = section.id
            # No quoting needed (for now)
            self.out.write('  {} = {}\n'.format(name, value))

    def run(self):
        o = self.options
        if o.remove:
            try:
                self.vm.conf.remove(o.name)
            except config_errors.NoSuchConfigOption as e:
                raise errors.ConfigOptionNotFound(e.name)
            self.vm.conf.store.save_changes()
        elif o.name is not None and '=' in o.name:
            # Set the option value
            name, value = o.name.split('=', 1)
            self.vm.conf.set(name, value)
            self.vm.conf.store.save_changes()
        else:
            # List the options
            if o.name is None:
                # Defaults to all options
                o.name = '.*'
                o.all = True
            if o.all:
                self.list_matching(o.name)
            elif o.name.startswith('@'):
                try:
                    self.out.write(self.vm.expand_file(o.name[1:]))
                except IOError as e:
                    # python2 does not provide FileNotFoundError
                    if e.errno == errno.ENOENT:
                        raise errors.ConfigPathNotFound(o.name[1:], o.name)
                    else:
                        raise
            else:
                self.list(o.name)
        return 0


command_registry.register(Config)


class Setup(VmCommand):

    name = 'setup'
    description = 'Setup a virtual machine.'

    def __init__(self, **kwargs):
        super(Setup, self).__init__(**kwargs)
        self.parser.add_argument(
            '--download', '-d', action="store_true",
            help='Force download of the required image.')
        self.parser.add_argument(
            '--ssh-keygen', '-k', action="store_true",
            help="Generate the ssh keys defined in 'ssh.server_keys'.")
        self.parser.add_argument(
            '--force', '-f', action="store_true",
            help='Force setup even if the vm is running.')

    def run(self):
        state = self.vm.state()
        # FIXME: states need to be defined uniquely across the various vms
        # implementations -- vila 2014-01-17
        if state in ('running', 'RUNNING'):
            if self.options.force:
                self.vm.teardown(force=self.options.force)
                state = self.vm.state()
            else:
                raise errors.VmRunning(self.vm_name)
        elif state in('shut off', 'STOPPED'):
            self.vm.teardown()
        self.vm.ssh_keygen(force=self.options.ssh_keygen)

        self.vm.setup()
        if self.vm.conf.get('vm.poweroff'):
            self.vm.stop()
        return 0


command_registry.register(Setup)


class Digest(VmCommand):

    name = 'digest'
    description = 'Display the digest of a virtual machine.'

    def parse_args(self, args):
        # FIXME: Another case where 'must define vm.class' sucks
        # -- vila 2016-11-14
        try:
            self.options = super(Digest, self).parse_args(args)
        except errors.ByovError as e:
            if 'must define vm.class' in e.fmt:
                self.options = None
        return self.options

    def run(self):
        if self.options is None:
            digest = 'UNKNOWN'
        else:
            digest = self.vm.hash_setup()
        if sys.version_info < (3,):
            digest = digest.decode('utf8')
        self.out.write(digest)
        return 0


command_registry.register(Digest)


class Status(VmCommand):

    name = 'status'
    description = 'Display the status of a virtual machine.'

    def run(self):
        state = self.vm.state()
        # FIXME: states need to be defined uniquely across the various vms
        # implementations -- vila 2014-01-17
        if state in ('shut off', 'STOPPED'):
            state = 'STOPPED'
        elif state in ('running', 'RUNNING'):
            state = 'RUNNING'
        self.out.write(state + '\n')
        return 0


command_registry.register(Status)


class Start(VmCommand):

    name = 'start'
    description = 'Start an existing virtual machine.'

    def run(self):
        state = self.vm.state()
        if state is None:
            raise errors.VmUnknown(self.vm_name)
        # FIXME: states need to be defined uniquely across the various vms
        # implementations -- vila 2014-01-17
        if state in ('running', 'RUNNING'):
            raise errors.VmRunning(self.vm_name)
        self.vm.start()
        return 0


command_registry.register(Start)


class Shell(VmCommand):

    name = 'shell'
    description = (
        'Start a shell, run a command or a script inside a virtual machine.')

    def __init__(self, **kwargs):
        super(Shell, self).__init__(**kwargs)
        self.parser.add_argument(
            'command', help='The command to run inside the vm.'
            ' Use a @ prefix to use a local script instead', nargs='?')
        self.parser.add_argument(
            'args', help='The arguments for the command to run on the vm.',
            nargs=argparse.REMAINDER)

    def run(self):
        state = self.vm.state()
        if state is None:
            raise errors.VmUnknown(self.vm_name)
        # FIXME: states need to be defined uniquely across the various vms
        # implementations -- vila 2014-01-17
        if state not in ('running', 'RUNNING'):
            raise errors.VmNotRunning(self.vm_name)
        ret, out, err = self.vm.shell(self.options.command, *self.options.args)
        # out and err are displayed separately rather than interspred as in
        # real life... but hey, is it that bad to lose the hard-to-figure-out
        # chaos ?
        print(out, file=self.out, end='')
        print(err, file=self.err, end='')
        return ret


command_registry.register(Shell)


class SshRegister(VmCommand):

    name = 'ssh-register'
    description = 'Register a host in the vm for ssh access.'

    def __init__(self, **kwargs):
        super(SshRegister, self).__init__(**kwargs)
        # FIXME: Support using an existing key ? -- vila 2018-10-21
        self.parser.add_argument(
            '--type', '-t', default='rsa',
            help='The ssh key type.')
        self.parser.add_argument(
            'host', help='The host to register.')

    def run(self):
        state = self.vm.state()
        if state is None:
            raise errors.VmUnknown(self.vm_name)
        # FIXME: states need to be defined uniquely across the various vms
        # implementations -- vila 2014-01-17
        if state not in ('running', 'RUNNING'):
            raise errors.VmNotRunning(self.vm_name)
        # FIXME: Duplicated from VmCommand.parse_vm_arg -- vila 2018-10-22
        host_conf = config.VmStack(self.options.host)
        try:
            kls = host_conf.get('vm.class')
        except config_errors.OptionMandatoryValueError:
            raise errors.VmUnknown(self.options.host)
        self.host = kls(host_conf)
        host_state = self.host.state()
        if host_state is None:
            raise errors.VmUnknown(self.options.host)
        # FIXME: states need to be defined uniquely across the various vms
        # implementations -- vila 2014-01-17
        if host_state not in ('running', 'RUNNING'):
            raise errors.VmNotRunning(self.options.host)
        # Get the host key from the host itself (hard to MITM ;-)
        keyscan_cmd = ['ssh-keyscan', '-t', self.options.type, 'localhost']
        ret, out, err = self.host.shell_captured(*keyscan_cmd)
        if ret:
            raise errors.CommandError(keyscan_cmd, ret, out, err)
        # Put the key in the vm known_hosts
        host_name = host_conf.get('vm.name')
        host_ip = host_conf.get('vm.ip')
        host_def = ('"' + out.replace('localhost ',
                                      '{},{} '.format(host_name, host_ip)) +
                    '"')
        knownhosts_cmd = 'echo -n' + host_def + '>> ~/.ssh/known_hosts'
        ret, out, err = self.vm.shell_captured(
            self.vm.conf.get('vm.user.shell'),
            cmd_input=knownhosts_cmd)
        if ret:
            raise errors.CommandError(knownhosts_cmd, ret, out, err)
        return ret


command_registry.register(SshRegister)


class SshAuthorize(VmCommand):

    name = 'ssh-authorize'
    description = 'Authorize a key in the vm for ssh access.'

    def __init__(self, **kwargs):
        super(SshAuthorize, self).__init__(**kwargs)
        self.parser.add_argument(
            'key', help='The path to the public key to add.')

    def run(self):
        state = self.vm.state()
        if state is None:
            raise errors.VmUnknown(self.vm_name)
        # FIXME: states need to be defined uniquely across the various vms
        # implementations -- vila 2014-01-17
        if state not in ('running', 'RUNNING'):
            raise errors.VmNotRunning(self.vm_name)
        with open(self.options.key) as f:
            key = f.read()
        authorize_cmd = ['cat', '-', '>>', '~/.ssh/authorized_keys']
        ret, out, err = self.vm.shell_captured(*authorize_cmd, cmd_input=key)
        if ret:
            raise errors.CommandError(authorize_cmd, ret, out, err)
        return ret


command_registry.register(SshAuthorize)


class Pull(VmCommand):

    name = 'pull'
    description = 'Pull a remote file from an existing virtual machine.'

    def __init__(self, **kwargs):
        super(Pull, self).__init__(**kwargs)
        self.parser.add_argument(
            'remote', metavar='REMOTE',
            help='The remote file in the vm to pull from.')
        self.parser.add_argument(
            'local', metavar='LOCAL',
            help='The local file.')

    def run(self):
        state = self.vm.state()
        if state is None:
            raise errors.VmUnknown(self.vm_name)
        # FIXME: states need to be defined uniquely across the various vms
        # implementations -- vila 2014-01-17
        if state not in ('running', 'RUNNING'):
            raise errors.VmNotRunning(self.vm_name)
        retcode = self.vm.pull(self.options.remote, self.options.local)
        return retcode


command_registry.register(Pull)


class Push(VmCommand):

    name = 'push'
    description = 'Push local file to an existing virtual machine.'

    def __init__(self, **kwargs):
        super(Push, self).__init__(**kwargs)
        self.parser.add_argument(
            'local', metavar='LOCAL',
            help='The local file to push. Option expanded if prefixed with @.')
        self.parser.add_argument(
            'remote', metavar='REMOTE',
            help='The remote file in the vm to push to.')

    def run(self):
        state = self.vm.state()
        if state is None:
            raise errors.VmUnknown(self.vm_name)
        # FIXME: states need to be defined uniquely across the various vms
        # implementations -- vila 2014-01-17
        if state not in ('running', 'RUNNING'):
            raise errors.VmNotRunning(self.vm_name)
        retcode = self.vm.push(self.options.local, self.options.remote)
        return retcode


command_registry.register(Push)


class Stop(VmCommand):

    name = 'stop'
    description = 'Stop an existing virtual machine.'

    def run(self):
        state = self.vm.state()
        if state is None:
            raise errors.VmUnknown(self.vm_name)
        # FIXME: states need to be defined uniquely across the various vms
        # implementations -- vila 2014-01-17
        if state not in ('running', 'RUNNING'):
            raise errors.VmNotRunning(self.vm_name)
        self.vm.stop()
        return 0


command_registry.register(Stop)


class Publish(VmCommand):

    name = 'publish'
    description = 'Publish a virtual machine image.'

    def run(self):
        state = self.vm.state()
        if state is None:
            raise errors.VmUnknown(self.vm_name)
        # FIXME: states need to be defined uniquely across the various vms
        # implementations -- vila 2014-01-17
        if state in ('running', 'RUNNING'):
            raise errors.VmRunning(self.vm_name)
        self.vm.publish()
        return 0


command_registry.register(Publish)


class Teardown(VmCommand):

    name = 'teardown'
    description = 'Teardown a virtual machine.'

    def __init__(self, **kwargs):
        super(Teardown, self).__init__(**kwargs)
        self.parser.add_argument(
            '--force', '-f', action="store_true",
            help='Force teardown even if the vm is running.')

    def run(self):
        state = self.vm.state()
        if state is None:
            raise errors.VmUnknown(self.vm_name)
        if state in ('running', 'RUNNING') and not self.options.force:
            raise errors.VmRunning(self.vm_name)
        self.vm.teardown(force=self.options.force)
        return 0


command_registry.register(Teardown)

# Now that we have all the commands registered, we can create a place holder
# option for help.
commands_help = '\n' + ''.join([
    '\t{}: {}\n'.format(cmd_name,
                        command_registry.get(cmd_name).description)
    for cmd_name in command_registry.keys()])
options.register(options.Option('byov.commands', default=None,
                                help_string=commands_help))


def run(args=None, out=None, err=None):
    if args is None:
        args = sys.argv[1:]
    if not args:
        cmd = Help()
        cmd_name = 'help'
    else:
        cmd_name = args[0]
        args = args[1:]
        try:
            cmd_class = command_registry.get(cmd_name)
            cmd = cmd_class(out=out, err=err)
        except KeyError:
            cmd = Help(out=out, err=err)
            args = [cmd_name]
    try:
        cmd.parse_args(args)
        return cmd.run()
    except Exception as e:
        logger.debug('{} failed'.format(cmd_name), exc_info=True)
        logger.error('{} failed: {!r}'.format(cmd_name, e))
        return -1
