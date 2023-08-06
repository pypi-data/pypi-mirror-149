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
"""Setup a virtual machine from a config file.

Note: Most of the operations requires root access and this script uses ``sudo``
to get them.
"""
import errno
import hashlib
import logging
import os
import subprocess
import tempfile
import time

import byov
from byoc import stacks
from byov import (
    config,
    errors,
    logs,
    monitors,
    options,
    ssh,
    subprocesses,
    user_data,
)


logger = logging.getLogger(__name__)


class VM(object):
    """A virtual machine relying on cloud-init to customize installation."""

    setup_ip_timeouts = None  # Must be set by daughter classes
    setup_ssh_timeouts = None  # Must be set by daughter classes
    existing_vm_options = ['vm.name', 'vm.class', 'vm.distribution',
                           'vm.user', 'vm.user.home', 'vm.user.shell']

    def __init__(self, conf):
        # The conf where most of the options are defined
        self.conf = conf
        # The conf for the existing vm
        self.econf = config.ExistingVmStack(conf.get('vm.name'))
        # Seed files
        self._meta_data_path = None
        self._user_data_path = None
        self.ci_user_data = None

    def setup(self):
        raise NotImplementedError(self.setup)

    def teardown(self, force=False):
        self.cleanup_configs()

    def start(self):
        return self.run_start_hook()

    def stop(self):
        raise NotImplementedError(self.stop)

    def publish(self):
        raise NotImplementedError(self.publish)

    def unpublish(self):
        raise NotImplementedError(self.unpublish)

    # FIXME: logging missing -- vila 2020-02-17
    def pull(self, remote, local):
        """Pull a file from a vm.

        :param remote: A remote path inside the vm.

        :param local: A local path.
        """
        mode_bits = self._remote_mode_bits(remote)
        with open(local, 'w') as f:
            # We can't use 'scp' here as the ssh connection obeys ssh.options
            # and scp doesn't support all ssh options. So we just leverage the
            # ssh shell
            send_command = ['cat', remote]
            ssh_command = self.get_ssh_command(*send_command)
            send = subprocess.Popen(ssh_command,
                                    stdout=f,
                                    stderr=subprocess.PIPE)
            _, err = send.communicate()
            if send.returncode:
                raise errors.CommandError(ssh_command, send.returncode,
                                          '', err.decode('utf8'))
        os.chmod(local, mode_bits)
        return send.returncode

    # FIXME: logging missing -- vila 2020-02-17
    def push(self, local, remote):
        """Push a local file to a vm.

        :param local: A local path. If prefixed with '@' options are expanded
            before pushing.

        :param remote: A remote path inside the vm.
        """
        tmp = None
        if local.startswith('@'):
            src = local[1:]
            mode_bits = oct(self._mode_bits(src))[-3:]
            content = self.expand_file(src)
            tmp = tempfile.NamedTemporaryFile(delete=False, mode='w')
            tmp.write(content)
            tmp.close()
            src = tmp.name
        else:
            src = local
            mode_bits = None
        try:
            ret = self.upload(src, remote, mode_bits)
        finally:
            if tmp is not None:
                os.remove(tmp.name)
        return ret

    # FIXME: logging missing -- vila 2020-02-17
    def save_existing_config(self):
        conf = self.conf
        for opt in self.existing_vm_options:
            # We need the raw values
            value = conf.get(opt, convert=False)
            if value:  # 'None' is never saved
                self.econf.set(opt, value)
        self.econf.store.save_changes()

    def cleanup_configs(self):
        for path in (self.console_path(), self.user_data_path(),
                     self.meta_data_path()):
            if os.path.exists(path):
                os.remove(path)
        config_dir_path = self.config_dir_path()
        # Delete the config directory if we can.
        try:
            os.rmdir(config_dir_path)
        except OSError as e:
            # Some server keys can still be there, keep them. If the dir is
            # already gone, don't complain.
            if e.errno not in (errno.ENOTEMPTY, errno.ENOENT):
                raise
        # Remove the vm from the existing ones
        name = self.conf.get('vm.name')
        try:
            del self.econf.store.sections[name]
        except KeyError:
            # The setup didn't went as far as creating the section
            pass
        # deleting a section is not supported by save_changes() so save() and
        # unload()
        self.econf.store.save()
        self.econf.store.unload()

    def hash_value(self, hasher, value):
        # No point in hashing none values, as soon as a value is set, it
        # introduces a difference.
        if value is not None:
            hasher.update(value.encode('utf8'))

    def hash_setup(self):
        """Returns a digest of the options used to setup the vm.

        This covers all relevant option values as well as the content of files
        referred to.

        This is a best effort that should cover most needs. Known limitations
        include: changes in files that are referred to indirectly, changes done
        inside the the vm after it was setup.
        """
        hasher = hashlib.md5()
        opts = []
        for more in ('vm.setup.digest.options', 'apt.setup.digest.options',
                     'pip.setup.digest.options',
                     'ssh.setup.digest_options'):
            l = self.conf.get(more)
            if l is not None:
                opts.extend(l)
        for opt in opts:
            odef = options.option_registry.get(opt)
            if isinstance(odef, options.PackageListOption):
                # The content of all the @file should be taken into account
                # (which PackageListOption conversion provides).
                value = self.conf.get(opt)
                if value is not None:
                    # We got a list, convert to a string
                    value = ' '.join(value)
            else:
                value = self.conf.get(opt, convert=False)
            self.hash_value(hasher, value)
        # FIXME: It would be nice to list the options below in a
        # 'vm.setup.digest.files' option but there are several blockers: 1) we
        # can't just dereference them as they may be None, 2) there is a mix of
        # scalar and lists (make them all lists ?) -- vila 2016-10-17
        setups = self.conf.get('vm.setup_scripts') or []
        uploads = self.conf.get('vm.uploaded_scripts') or []
        user_keys = self.conf.get('ssh.authorized_keys') or []
        server_keys = self.conf.get('ssh.server_keys') or []
        keys = user_keys + server_keys
        paths = [self.conf.get('vm.root_script'),
                 self.conf.get('vm.user_script')] + uploads + setups + keys
        for path in paths:
            try:
                with open(path) as f:
                    value = f.read()
            except Exception:
                # If an error has to be reported to the user, this is not from
                # here: the setup itself has/will fail and the digest will be
                # different, so just ignore
                continue
            self.hash_value(hasher, value)
        return hasher.hexdigest()

    # FIXME: could be named setup_over_shell -- vila 2022-01-19
    def setup_over_ssh(self):
        """Once shell access is setup, install  packages and run scripts."""
        # Save the defined config. Errors after that point should not break the
        # vm hard enough that one cannot shell into it and debug.
        self.save_existing_config()
        # Finish the setup
        self.update()
        self.install_packages()
        # Either update() or install_apt_packages() can trigger a reboot

        # FIXME: only on backends relying on cloud-init (docker doesn't)
        # -- vila 2022-03-25
        try:
            self.shell_captured(self.conf.get('vm.user.shell'),
                                cmd_input='test -f /var/run/reboot-required')
            logger.info('Rebooting {}...'.format(self.conf.get('vm.name')))
            self.stop()
            self.start()
        except errors.CommandError:
            # No reboot required, we're done
            pass
        self.run_setup_hook()
        self.run_setup_scripts()
        self.install_pip_packages()
        self.econf.set('vm.setup.digest', self.hash_setup())
        self.econf.store.save_changes()

    def shell(self, command, *args):
        if not command:
            ssh_command = self.get_ssh_command(command, *args)
            ret = subprocesses.raw_run(ssh_command)
            out, err = '', ''
        elif command.startswith('@'):
            script_path = command[1:]
            ret, out, err = self.run_script(
                script_path, args=args, captured=False)
        else:
            ssh_command = self.get_ssh_command(command, *args)
            ret, out, err = subprocesses.run(ssh_command)
        return ret, out, err

    def shell_captured(self, command, *args, **kwargs):
        cmd_input = kwargs.pop('cmd_input', None)
        # Compose Running [{cmd_input} under ]{command} on {vm.name}
        under = ''
        if cmd_input:
            under = ' ' + cmd_input + ' under '
        logger.debug('Running {}{} on {}'.format(
            under, command, self.conf.get('vm.name')))
        ssh_command = self.get_ssh_command(command, *args)
        retcode, out, err = subprocesses.run(ssh_command, cmd_input=cmd_input)
        logger.debug('Done with {}{}, it returned {} on {}'.format(
            command, under, retcode, self.conf.get('vm.name')))
        return retcode, out, err

    def update(self):
        if self.conf.get('vm.update'):
            logger.info('Updating {}...'.format(self.conf.get('vm.name')))
            pack_mgr = self.conf.expand_options(
                '{{vm.distribution}.package.manager}')
            if pack_mgr == 'apt':
                self.apt_get_update()
                self.apt_get_upgrade()
            elif pack_mgr == 'dnf':
                self.dnf_upgrade()

    def install_packages(self):
        packages = self.conf.get('vm.packages')
        if not packages:
            return 0
        logger.info('Installing packages {} on {}'.format(
            ' '.join(packages), self.conf.get('vm.name')))
        pack_mgr = self.conf.expand_options(
            '{{vm.distribution}.package.manager}')
        try:
            if pack_mgr == 'apt':
                self.do_apt_get(['install'] + packages)
            elif pack_mgr == 'dnf':
                self.do_dnf(['install'] + packages)
        except errors.CommandError:
            logger.debug('Failed to install packages', exc_info=True)
            raise

    def install_pip_packages(self):
        packages = self.conf.get('pip.packages')
        if not packages:
            return 0
        logger.info('Installing packages {} on {}'.format(
            ' '.join(packages), self.conf.get('vm.name')))
        install_command = self.conf.get('pip.install.command') + packages
        try:
            self.do_pip(install_command)
        except errors.CommandError:
            logger.debug('Failed to install packages', exc_info=True)
            raise

    def run_hook(self, option):
        """Locally run a command defined by the user."""
        hook = self.conf.get(option)
        if not hook:
            return
        logger.info('Running {} ({}) on host for {}'.format(
            option, hook, self.conf.get('vm.name')))

        def save_config_stores():
            # Hook can potentially change config files. Save all changes so
            # stores will be reloaded after each hook run.
            for store in stacks._shared_stores.values():
                store.save_changes()
                store.unload()

        tmp = None
        cmd = None
        logger.debug('Hook: {}'.format(hook))
        if hook.startswith('@'):
            path = subprocesses.which(hook[1:], byov.path)
            if path is None:
                raise FileNotFoundError(errno.ENOENT, 'File not found.',
                                        hook[1:])
            mode_bits = self._mode_bits(path)
            content = self.expand_file(path)
            logger.debug('Expanded script {}: {}'.format(path, content))
            tmp = tempfile.NamedTemporaryFile(delete=False, mode='w')
            tmp.write(content)
            tmp.close()
            os.chmod(tmp.name, mode_bits)
            # FIXME: If hooks were imported and executed, this wouldn't be
            # needed -- vila 2022-04-04
            os.environ['BYOV_PATH'] = ':'.join(byov.path)
            cmd = [tmp.name]
        else:
            # FIXME: needs which() -- vila 2022-03-28
            cmd = ['/bin/sh', '-c', hook]
        try:
            save_config_stores()
            ret, out, err = subprocesses.run(cmd)
        except errors.CommandError:
            logger.error('Failed to run {}'.format(cmd), exc_info=True)
            raise
        finally:
            if tmp is not None:
                os.remove(tmp.name)
        return ret

    def run_setup_hook(self):
        """Locally run a setup command defined by the user."""
        return self.run_hook('vm.setup.hook')

    def run_start_hook(self):
        """Locally run a start command defined by the user."""
        return self.run_hook('vm.start.hook')

    def run_setup_scripts(self):
        scripts = self.conf.get('vm.setup_scripts')
        if scripts is None:
            return
        for path in scripts:
            try:
                self.run_script(path)
            except Exception:
                logger.debug('Failed to run {}'.format(path), exc_info=True)
                raise

    def _mode_bits(self, path):
        """Get mode bits for a path as string."""
        return os.stat(os.path.expanduser(path)).st_mode

    def _remote_mode_bits(self, path):
        """Get mode bits for a remote path as string."""
        _, out, _ = self.shell_captured('stat', '-c%a', path)
        return int(out, 8)

    def expand_file(self, local_path):
        with open(os.path.expanduser(local_path)) as f:
            content = f.read()
        expanded = self.conf.expand_options(content)
        return expanded

    def run_script(self, script_path, args=None, captured=True):
        if args is None:
            args = []
        found_path = subprocesses.which(script_path, byov.path)
        if found_path is None:
                raise FileNotFoundError(errno.ENOENT, 'File not found.',
                                        script_path)
        logger.info('Running {}{} on {}'.format(
            script_path, ' '.join(args), self.conf.get('vm.name')))
        mode_bits = oct(self._mode_bits(found_path))[-3:]
        content = self.expand_file(found_path)
        logger.debug('Expanded script {}: {}'.format(found_path, content))
        tmp = tempfile.NamedTemporaryFile(delete=False, mode='w')
        tmp.write(content)
        tmp.close()
        # Get a temporary path (requires dropping the newline from the output)
        remote_path = self.shell_captured(
            'mktemp', '-t', 'byov.XXXXXX')[1][:-1]
        try:
            self.upload(tmp.name, remote_path, mode_bits=mode_bits)
            if captured:
                retcode, out, err = self.shell_captured(remote_path, *args)
                if retcode:
                    raise errors.CommandError([remote_path] + args,
                                              retcode, out, err)
            else:
                retcode, out, err = self.shell(remote_path, *args)
        finally:
            os.remove(tmp.name)
            # All ended well, remove remote path silently
            self.shell_captured('rm', '-f', remote_path)
        logger.debug('Done with {}, it returned {} on {}'.format(
            found_path, retcode, self.conf.get('vm.name')))
        return retcode, out, err

    def upload(self, local_path, remote_path, mode_bits=None):
        if mode_bits is None:
            # Keep only the last 3 digits as that's what chmod will
            # accept. This will raise if path doesn't exist
            mode_bits = oct(self._mode_bits(local_path))[-3:]
        send_command = ['cat', local_path]
        send = subprocess.Popen(send_command,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        # We can't use 'scp' here as the ssh connection obeys ssh.options and
        # scp doesn't support all ssh options. So we just leverage the ssh
        # shell
        cat_command = ['cat', '-', '>', remote_path,
                       '&&', 'chmod', mode_bits, remote_path]
        ssh_command = self.get_ssh_command(*cat_command)
        recv = subprocess.Popen(ssh_command,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                stdin=send.stdout)
        # send.stdout.close()  # Allow 'recv' to get a SIGPIPE if 'send' exits
        out, err = recv.communicate()
        if recv.returncode:
            raise errors.CommandError(ssh_command, recv.returncode,
                                      out.decode('utf8'), err.decode('utf8'))
        out, err = send.communicate()
        if send.returncode:
            raise errors.CommandError(send_command, send.returncode,
                                      out.decode('utf8'), err.decode('utf8'))
        return send.returncode

    def dnf_upgrade(self):
        for timeout in self.conf.get('dnf.upgrade.timeouts'):
            try:
                self.do_dnf(['upgrade'])
                return  # We're done
            except errors.CommandError:
                msg = ('dnf upgrade failed,'
                       ' will sleep for {:.2f} seconds')
                logger.debug(msg.format(float(timeout)), exc_info=True)
                time.sleep(float(timeout))
        raise errors.ByovError('dnf upgrade never succeeded')

    def do_dnf(self, command):
        dnf_command = self.conf.get('dnf.command')
        # Filter empty values
        dnf_command = [arg for arg in dnf_command if arg]
        dnf_command.extend(command)
        return self.shell_captured(*dnf_command)

    def do_apt_get(self, command):
        apt_command = self.conf.get('apt.command')
        # Filter empty values
        apt_command = [arg for arg in apt_command if arg]
        apt_command.extend(command)
        return self.shell_captured(*apt_command)

    def do_pip(self, command):
        pip_command = self.conf.get('pip.command')
        # Filter empty values
        pip_command = [arg for arg in pip_command if arg]
        pip_command.extend(command)
        ret, out, err = self.shell_captured(
            self.conf.get('vm.user.shell'), cmd_input=' '.join(pip_command))
        return ret, out, err

    def apt_get_update(self):
        for timeout in self.conf.get('apt.update.timeouts'):
            try:
                self.do_apt_get(['update'])
                return  # We're done
            except errors.CommandError:
                msg = 'apt-get update failed, will sleep for {:.2f} seconds'
                logger.debug(msg.format(float(timeout)), exc_info=True)
                time.sleep(float(timeout))
        raise errors.ByovError('apt-get update never succeeded')

    def apt_get_upgrade(self):
        for timeout in self.conf.get('apt.upgrade.timeouts'):
            try:
                self.do_apt_get(['dist-upgrade'])
                return  # We're done
            except errors.CommandError:
                msg = ('apt-get dist-upgrade failed,'
                       ' will sleep for {:.2f} seconds')
                logger.debug(msg.format(float(timeout)), exc_info=True)
                time.sleep(float(timeout))
        raise errors.ByovError('apt-get dist-upgrade never succeeded')

    def ensure_dir(self, path):
        try:
            os.makedirs(path)
        except OSError as e:
            # python2 doesn't provide the exist_ok=True to makedirs
            if e.errno != errno.EEXIST:
                raise

    def remove(self, path):
        """Remove a path but don't complain if it's not there.

        Non-empty dirs still can't be deleted that way.

        Aka: It's Dead Jim.
        """
        if os.path.exists(path):
            os.remove(path)

    # FIXME: 'vm.config_dir' should be removed and fallouts addressed: calls to
    # self.ensure_dir(self.config_dir_path()) need to be removed too and
    # replaced by a better solution -- vila 2016-07-07
    def config_dir_path(self):
        return self.conf.get('vm.config_dir')

    def console_path(self):
        # The console is used to record 'setup' and 'start' outputs
        return os.path.join(self.config_dir_path(), 'console')

    def user_data_path(self):
        return os.path.join(self.config_dir_path(), 'user-data')

    def meta_data_path(self):
        return os.path.join(self.config_dir_path(), 'meta-data')

    def ssh_keygen(self, force=False):
        keys = self.conf.get('ssh.server_keys')
        if keys:
            for key in keys:
                key = os.path.abspath(os.path.expanduser(key))  # Just in case
                if force or not os.path.exists(key):
                    self.ensure_dir(os.path.dirname(key))
                    ssh.keygen(key, self.conf.get('vm.name'))

    def create_meta_data(self):
        self.ensure_dir(self.config_dir_path())
        self._meta_data_path = self.meta_data_path()
        with open(self._meta_data_path, 'w') as f:
            f.write(self.conf.get('vm.meta_data'))

    def create_user_data(self):
        ci_user_data = user_data.CIUserData(self.conf)
        ci_user_data.populate()
        self.ensure_dir(self.config_dir_path())
        self._user_data_path = self.user_data_path()
        with open(self._user_data_path, 'w') as f:
            f.write(ci_user_data.dump())
        self.ci_user_data = ci_user_data

    def capture_interface(self, line, iface_re):
        """Capture the required interface if it appears in 'line'.

        :param line: A line from the vm console.

        :param iface_re: The regexp matching a cloud-init output revealing an
            interface.

        :return: True if the interface was captured, False otherwise.
        """
        match = iface_re.match(line)
        if match is not None:
            iface, ip, mask, mac = match.groups()
            self.econf.set('vm.ip', ip)
            return True
        return False

    def scan_console_during_setup(self, console_size, console_path, cmd):
        """Scan the console output until the end of the setup.

        We add a specific part for cloud-init to ensure we properly detect
        the end of the run.

        :param console_size: The size of the console file before 'install' is
            run.

        :param console_path: The path to the console file.

        :param cmd: The setup command (used for error display).
        """
        console = monitors.TailMonitor(console_path, console_size)
        iface = '(eth0|ens3)'
        iface_re = logs.InterfaceRegexp(iface)
        try:
            for line in console.scan():
                # FIXME: We need some way to activate this dynamically (conf
                # var defaulting to environment variable OR cmdline parameter ?
                # -- vila 2013-02-11
                # print('read: [{}]'.format(line))  # so useful for debug...
                self.capture_interface(line, iface_re)
        except (errors.ConsoleEOFError, errors.CloudInitError):
            # FIXME: No explicit test covers this path -- vila 2013-02-15
            # FIXME: errors.ConsoleEOFError says 'Suspicious line', that's
            # confusing -- vila 2019-10-16
            err_lines = ['Suspicious output line from cloud-init.\n',
                         '\t' + console.lines[-1],
                         'Check the configuration:\n']
            with open(self._meta_data_path) as f:
                err_lines.append('meta-data content:\n')
                err_lines.extend(f.readlines())
            with open(self._user_data_path) as f:
                err_lines.append('user-data content:\n')
                err_lines.extend(f.readlines())
            raise errors.CommandError(cmd, console.proc.returncode,
                                      '\n'.join(console.lines),
                                      ''.join(err_lines))

    def scan_console_during_start(self, console_size, cmd):
        """Scan the console output while the instance starts.

        This is used to capture the network addresses displayed by cloud-init.

        :param console_size: The size of the console file before 'start' is
            run.

        :param cmd: The start command (used for error display).
        """
        console = monitors.TailMonitor(self.console_path(), console_size)
        iface = '(eth0|ens3)'
        iface_re = logs.InterfaceRegexp(iface)
        try:
            for line in console.scan():
                if self.capture_interface(line, iface_re):
                    # We're done, no need to scan anymore (and work around the
                    # fact that 'scan' will otherwise terminate when the vm is
                    # stopped ;)
                    # FIXME: This fails to exit the loop when no IP can be
                    # provided (seen while investigating
                    # https://bugs.launchpad.net/bugs/1465196)
                    # -- vila 2015-11-01
                    return
        except errors.ConsoleEOFError:
            # We're done
            pass

    def get_ssh_user_host_port(self):
        c = self.conf
        return (c.get('ssh.user'), c.get('ssh.host'), c.get('ssh.port'))

    def get_ssh_command(self, command, *args):
        cmd = ['ssh']
        user, host, port = self.get_ssh_user_host_port()
        options = self.conf.get('ssh.options')
        if options:
            cmd += options
        cmd += ['{}@{}'.format(user, host)]
        if port:
            cmd += ['-p', port]
        if command is not None:
            cmd += [command]
            if args:
                cmd += args
        return cmd

    def discover_ip(self):
        raise NotImplementedError(self.discover_ip)

    def wait_for_ip(self):
        logger.info('Waiting for an IP address for {}...'.format(
            self.conf.get('vm.name')))
        ip = None
        stos = self.conf.get(self.setup_ip_timeouts)
        me = self.wait_for_ip.__name__
        for attempt, sleep in enumerate(stos):
            try:
                if attempt > 1:
                    logger.debug('Re-trying {} {}/{}'.format(
                        me, attempt, stos.retries))
                ip = self.discover_ip()
                self.econf.set('vm.ip', ip)
                logger.info('{} IP is {}'.format(self.conf.get('vm.name'),
                                                 self.conf.get('vm.ip')))
                return
            except Exception:
                logger.debug(
                    'IP not yet available for {}'.format(
                        self.conf.get('vm.name')),
                    exc_info=True)
            # FIXME: metric  -- vila 2015-06-25
            logger.debug('Sleeping {:.2f} seconds for {} {}/{}'.format(
                sleep, me, attempt, stos.retries))
            time.sleep(sleep)
        raise errors.ByovError('{name} never received an IP',
                               name=self.conf.get('vm.name'))

    def wait_for_ssh(self):
        logger.info('Waiting for {} ssh...'.format(self.conf.get('vm.name')))
        stos = self.conf.get(self.setup_ssh_timeouts)
        me = self.wait_for_ssh.__name__
        exc = None
        for attempt, sleep in enumerate(stos, start=1):
            try:
                if attempt > 1:
                    logger.debug('Re-trying {} {}/{}'.format(
                        me, attempt, stos.retries))
                ret, out, err = self.shell_captured('whoami')
                # Success, clear the exception
                exc = None
                break
            except errors.CommandError as e:
                logger.debug('ssh is not up yet', exc_info=True)
                exc = e
                # FIXME: metric  -- vila 2015-06-25
                pass
            logger.debug('Sleeping {:.2f} seconds for {} {}/{}'.format(
                sleep, me, attempt, stos.retries))
            time.sleep(sleep)
        if exc is not None:
            # Re-raise the last seen exception
            raise exc

    def _wait_for_cloud_init(self, timeouts_name):
        logger.info('Waiting for cloud-init on {}...'.format(
            self.conf.get('vm.name')))
        # Now let's track cloud-init completion
        # We know ssh is up and running
        citos = self.conf.get(timeouts_name)
        me = self.wait_for_cloud_init.__name__
        exc = None
        # boot-finished is deleted when cloud-init starts (which is before the
        # guest get network access) and created once it finishes. Since we use
        # ssh to check, there is no race around the deletion so it's always
        # safe to wait for the file to appear.
        for attempt, sleep in enumerate(citos, start=1):
            try:
                if attempt > 1:
                    logger.debug('Re-trying {} {}/{}'.format(
                        me, attempt, citos.retries))
                self.shell_captured(
                    self.conf.get('vm.user.shell'),
                    cmd_input='test -f /var/lib/cloud/instance/boot-finished')
                # Success, clear the exception in case it was set
                exc = None
                break
            except errors.CommandError as e:
                logger.debug('cloud-init is not done yet', exc_info=True)
                exc = e
                # FIXME: logging + metric  -- vila 2015-06-25
            logger.debug('Sleeping {:.2f} seconds for {} {}/{}'.format(
                sleep, me, attempt, citos.retries))
            time.sleep(sleep)
        # FIXME: Worth downloading cloud-init[-output].log locally. It's the
        # first place to look when debugging cloud-init issues
        # -- vila 2019-12-10
        if exc is not None:
            # Re-raise the last seen exception
            raise exc
        # FIXME: We need to check if cloud-init failed or not but
        # /var/log/cloud-init[-output].log contain all executions :-/ So
        # checking only for the last execution is not trivial
        # -- vila 2016-05-13
