# This file is part of Build Your Own Virtual machine.
#
# Copyright 2019 Vincent Ladeuil.
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

import contextlib
import errno
import io
import logging
import os
import socket
import subprocess
import time
import sys
import select


import pexpect


from pexpect import fdpexpect


from byoc import (
    registries,
)
from byov import (
    config,
    errors,
    subprocesses,
    vms,
)


logger = logging.getLogger(__name__)


class ImageCommand(object):

    def __init__(self, vm):
        self.vm = vm
        self.conf = vm.conf
        # Some defaults shared by most implementations
        self.target = self.conf.get('qemu.image')
        self.teardown_cmd = ['rm', '-f', '{target}']

    def run_cmd(self, cmd):
        expanded = [self.conf.expand_options(c, dict(source=self.source,
                                                     target=self.target))
                    for c in cmd]
        logger.info('Running {}'.format(' '.join(expanded)))
        return subprocesses.run(expanded)

    def setup(self):
        self.vm.ensure_dir(os.path.dirname(self.target))
        return self.run_cmd(self.setup_cmd)

    def teardown(self):
        return self.run_cmd(self.teardown_cmd)


class ImageClone(ImageCommand):
    '''Clone an existing image.'''

    def __init__(self, conf):
        super().__init__(conf)
        self.setup_cmd = self.conf.get('qemu.clone', expand=False)
        self.source = self.vm.backing_image_path()


class ImageConvert(ImageCommand):
    '''Convert an existing image.'''

    def __init__(self, conf):
        super().__init__(conf)
        self.setup_cmd = self.conf.get('qemu.convert', expand=False)
        self.source = self.conf.get('qemu.download.path')
        self.setup_cmd = ['qemu-img', 'convert', '-O', 'qcow2',
                          '{source}', '{target}']


class ImageCopy(ImageCommand):
    '''Copy an existing image.'''

    def __init__(self, conf):
        super().__init__(conf)
        self.source = self.conf.get('qemu.copy.input', expand=False)
        self.setup_cmd = ['cp', '{source}', '{target}']


class ImageCreate(ImageCommand):
    '''Create an image.'''

    def __init__(self, conf):
        super().__init__(conf)
        self.target = self.conf.get('qemu.image', expand=False)
        self.setup_cmd = ['qemu-img', 'create', '-f', 'qcow2',
                          '{target}']


class ImageDownload(ImageCommand):
    '''Download an image.'''

    def __init__(self, conf):
        super().__init__(conf)
        self.setup_cmd = self.conf.get('qemu.download', expand=False)
        self.source = self.conf.get('qemu.download.url')
        self.target = self.conf.get('qemu.download.path')

    def setup(self):
        logger.info('Downloading {}'.format(self.source))
        if not os.path.exists(self.target):
            super().setup()
        else:
            logger.info('Already at {}'.format(self.target))


class ImageResize(ImageCommand):
    '''Resize an image.'''

    def __init__(self, conf):
        super().__init__(conf)
        self.setup_cmd = self.conf.get('qemu.resize', expand=False)
        disk_size = self.conf.get('vm.disk_size')
        self.source = disk_size
        self.target = self.conf.get('qemu.image')
        if not disk_size:
            self.setup_cmd = ['/bin/true']
        self.teardown_cmd = ['/bin/true']

    def setup(self):
        if self.source:
            return self.run_cmd(self.setup_cmd)


# The image related commands
image_cmd_registry = registries.Registry()


def imgcmd_register(name, kls):
    image_cmd_registry.register(name, kls, kls.__doc__)

imgcmd_register('clone', ImageClone)
imgcmd_register('convert', ImageConvert)
imgcmd_register('copy', ImageCopy)
imgcmd_register('create', ImageCreate)
imgcmd_register('download', ImageDownload)
imgcmd_register('resize', ImageResize)


# FIXME: Require newer version for pexpect (>~=4.6)? -- vila 2019-12-09
def select_ignore_interrupts(iwtd, owtd, ewtd, timeout=None):

    '''This is a wrapper around select.select() that ignores signals. If
    select.select raises a select.error exception and errno is an EINTR
    error then it is ignored. Mainly this is used to ignore sigwinch
    (terminal resize). '''

    # if select() is interrupted by a signal (errno==EINTR) then
    # we loop back and enter the select() again.
    if timeout is not None:
        end_time = time.time() + timeout
    while True:
        try:
            return select.select(iwtd, owtd, ewtd, timeout)
        except InterruptedError:
            err = sys.exc_info()[1]
            if err.args[0] == errno.EINTR:
                # if we loop back we have to subtract the
                # amount of time we already waited.
                if timeout is not None:
                    timeout = end_time - time.time()
                    if timeout < 0:
                        return([], [], [])
            else:
                # something else caused the select.error, so
                # this actually is an exception.
                raise


# FIXME: upstream wants 'fd' to support os.fstat(fd) which our socket doesn't
# support. So we get rid of the restriction as the code works fine with a
# socket.
# -- vila 2019-12-09
class fdspawn(fdpexpect.fdspawn):

    def __init__(self, fd, args=None, timeout=30, maxread=2000,
                 searchwindowsize=None, logfile=None, encoding=None,
                 codec_errors='strict', use_poll=False):

        if hasattr(fd, 'fileno'):
            fd = fd.fileno()

        self.args = None
        self.command = None
        fdpexpect.SpawnBase.__init__(self, timeout, maxread, searchwindowsize,
                                     logfile, encoding=encoding,
                                     codec_errors=codec_errors)
        self.child_fd = fd
        self.own_fd = False
        self.closed = False
        self.name = '<file descriptor %d>' % fd
        self.use_poll = use_poll

    def read_nonblocking(self, size=1, timeout=-1):
        """
        Read from the file descriptor and return the result as a string.

        The read_nonblocking method of :class:`SpawnBase` assumes that a call
        to os.read will not block (timeout parameter is ignored). This is not
        the case for POSIX file-like objects such as sockets and serial ports.

        Use :func:`select.select`, timeout is implemented conditionally for
        POSIX systems.

        :param int size: Read at most *size* bytes.
        :param int timeout: Wait timeout seconds for file descriptor to be
            ready to read. When -1 (default), use self.timeout. When 0, poll.
        :return: String containing the bytes read
        """
        if os.name == 'posix':
            if timeout == -1:
                timeout = self.timeout
            rlist = [self.child_fd]
            wlist = []
            xlist = []
            rlist, wlist, xlist = select_ignore_interrupts(
                rlist, wlist, xlist, timeout)
            if self.child_fd not in rlist:
                raise pexpect.TIMEOUT('Timeout exceeded.')
        return super(fdspawn, self).read_nonblocking(size)


@contextlib.contextmanager
def MonitorSocket(qemu):
    try:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        monitor_path = qemu.monitor_path()
        logger.debug('Connecting to {}...'.format(monitor_path))
        sock.connect(monitor_path)
        yield sock
    finally:
        try:
            sock.close()
        except OSError as e:
            if e.args[0] == 9:
                # bad file descriptor, qemu closed the socket
                pass
            else:
                raise


@contextlib.contextmanager
def Monitor(qemu):
    with MonitorSocket(qemu) as sock:
        monitor = None
        try:
            monitor = fdspawn(sock, timeout=10)
            yield monitor
        finally:
            if monitor is not None:
                try:
                    monitor.close()
                except OSError as e:
                    if e.args[0] == 9:  # Bad file descriptor, already closed
                        pass
                    raise


class Qemu(vms.VM):
    """QEMU implementation.

    A qemu process is launched in the background with a monitor socket and log
    files for stdout/stderr.

    All interactions happen via the monitor to get the state, start, stop or
    shut down the vm.
    """

    setup_ssh_timeouts = 'qemu.setup_ssh.timeouts'

    existing_vm_options = vms.VM.existing_vm_options + [
        'qemu.bridge',
        'qemu.download.dir',
        'qemu.download.path',
        'qemu.download.url',
        'qemu.graphics',
        'qemu.mac.address',
        'qemu.networks',
        'qemu.pid',  # FIXME: What happens on host reboot ? -- vila 2021-11-30
        'qemu.ssh.localhost.port',
        'qemu.image',
        'qemu.images.dir',
        'qemu.mac.address',
        'qemu.mac.prefix',
    ]

    def __init__(self, conf):
        super(Qemu, self).__init__(conf)
        # FIXME: cleanup _seed_path and friends, they
        # aren't really needed -- vila 2019-12-07
        # Disk paths
        self._seed_path = None

    def state(self):
        logger.debug('Find {} qemu state'.format(self.conf.get('vm.name')))
        state = 'UNKNOWN'
        # FIXME: https://qemu.weilnetz.de/doc/qemu-doc.html#Network-options
        # mentions :
        # -pidfile file
        # Store the QEMU process PID in file. It is useful if you launch QEMU
        # from a script.
        # -- vila 2019-09-10
        pid = self.conf.get('qemu.pid')
        if pid is None:
            return 'UNKNOWN'
        # If there is a pid, check it is still alive
        try:
            # Using signal 0 as kill(2) won't send a signal in that case but
            # still checks the pid exist.
            os.kill(pid, 0)
        except OSError:
            return 'STOPPED'
        # The pid exists, qemu is still running
        try:
            with Monitor(self) as monitor:
                monitor.expect('\(qemu\) ')
                # See there between RUNNING and STOPPED (suspended ?). Until
                # then, assume qemu is running when the monitor expects a
                # command.  Could be 'info status' returning running or paused
                # according to
                # https://qemu.readthedocs.io/en/latest/system/monitor.html
                state = 'RUNNING'
        except (ConnectionRefusedError, ConnectionResetError):
            logger.debug('Monitor cannot be reached')
            state = 'STOPPED'
        return state

    def spawn_qemu(self, with_seed=True):
        logger.info('Spawning {} qemu'.format(self.conf.get('vm.name')))
        try:
            return self._spawn_qemu(with_seed)
        except errors.ByovError:
            with io.open(self.stderr_path(), encoding='utf8') as f:
                stderr = f.read()
            logger.exception(
                'Spawning qemu for {} failed, qemu.stderr: {}'.format(
                    self.conf.get('vm.name'), stderr))
            raise

    def _spawn_qemu(self, with_seed=True):
        self.ensure_dir(self.config_dir_path())
        qemu_cmd = ['qemu-system-x86_64', '-enable-kvm']

        nb_cpus = self.conf.get('vm.cpus')
        if nb_cpus:
            qemu_cmd.extend(['-smp', nb_cpus])
        ram_size = self.conf.get('vm.ram_size')
        if ram_size:
            qemu_cmd.extend(['-m', ram_size])
        graphics = self.conf.get('qemu.graphics')
        if graphics:
            qemu_cmd.extend(graphics)
        networks = self.conf.get('qemu.networks')
        if networks:
            qemu_cmd.extend(networks)
        di_path = self.disk_image_path()
        if os.path.exists(di_path):
            qemu_cmd.extend(['-drive', 'if=virtio,file={}'.format(di_path)])
        more_disks = self.conf.get('qemu.disks')
        if more_disks:
            qemu_cmd.extend(more_disks)
        if with_seed and self._seed_path:
            qemu_cmd.extend(['-cdrom', self._seed_path])

        qemu_cmd.extend(
            ['-monitor', 'unix:' + self.monitor_path() + ',server'])

        def utf8_open(path):
            return io.open(path, 'w', encoding='utf8')

        # The child will inherit the file handles and take care of them. The
        # parent can close them safely.
        stdout_path = self.stdout_path()
        stderr_path = self.stderr_path()
        with utf8_open(stdout_path) as out, utf8_open(stderr_path) as err:
            logger.debug('Running {}'.format(' '.join(qemu_cmd)))
            proc = subprocess.Popen(qemu_cmd,
                                    stdin=subprocess.DEVNULL,
                                    stdout=out, stderr=err,
                                    close_fds=True)
        self.econf.set('qemu.pid', '{}'.format(proc.pid))
        self.save_existing_config()
        # At that point qemu is waiting for a connection to the monitor socket
        # This avoids a race between starting qemu up to the point where it
        # starts booting and monitoring it.
        qtos = self.conf.get('qemu.init.timeouts')
        me = self.spawn_qemu.__name__
        exc = None
        for attempt, sleep in enumerate(qtos, start=1):
            try:
                with MonitorSocket(self):
                    # Opening the socket is enough
                    logger.debug('qemu process {} is up'.format(proc.pid))
                    exc = None
                break  # We're done
            except ConnectionRefusedError as e:
                exc = e
                # FIXME: metric  -- vila 2019-09-11
                logger.debug(
                    'Sleeping {:.2f} seconds for {}/{} {}/{}'.format(
                        sleep, me, 'ConnectionRefusedError',
                        attempt, qtos.retries))
                time.sleep(sleep)
                continue  # Try again maybe ?
            except IOError as e:
                # The socket is not available yet
                # python2 does not provide FileNotFoundError
                if e.errno == errno.ENOENT:
                    # FIXME: metric  -- vila 2019-09-11
                    logger.debug(
                        'Sleeping {:.2f} seconds for {}/{} {}/{}'.format(
                            sleep, me, 'IOError', attempt, qtos.retries))
                    time.sleep(sleep)
                    continue  # Try again maybe ?
                else:
                    exc = e  # Try again maybe ?
        if exc is not None:  # We didn't succeed
            raise exc  # Re-raise the last seen exception

        # FIXME: The current design is quite ugly :-/ May be this means the ssh
        # access configuration is not appropriate (at least using port
        # forwarding looks messy). -- vila 2019-09-13

        # Two different network configurations are ~supported at this point,
        # differing mainly by how ssh access is obtained: port forwarding works
        # even if no other network connectivity is provided, whereas all other
        # configurations are supposed to reveal an IP address controlled by a
        # provided mac address. But depending on specifics, the IP is found
        # from the arp cache (populated by a ping on name) or in the cloud-init
        # console output (assuming cloud-init has not been disabled). Right now
        # only the arp/ping implementation is supported and it requires a
        # user-provided bridge on the host.  -- vila 2019-10-17
        if self.conf.get('qemu.ssh.localhost.port') is None:
            self.capture_ip()
            if self.conf.get('vm.ip') is None:
                raise errors.ByovError('{name} never received an IP',
                                       name=self.conf.get('vm.name'))
        logger.debug('IP address is {}'.format(self.conf.get('vm.ip')))

    def terminate_qemu(self):
        logger.info('Terminating {} qemu'.format(self.conf.get('vm.name')))
        try:
            with Monitor(self) as monitor:
                monitor.sendline('quit')
                monitor.expect(pexpect.EOF)
        # Catch TIMEOUT because it either happens when connecting (so it's
        # already dead) or after connecting successfully (so it was alive and
        # is now dead).
        except (ConnectionRefusedError, pexpect.exceptions.TIMEOUT):
            # It's dead Jim
            logger.debug('Monitor cannot be reached', exc_info=True)

    def monitor_path(self):
        return os.path.join(self.config_dir_path(), 'monitor')

    def stdout_path(self):
        return os.path.join(self.config_dir_path(), 'qemu.stdout')

    def stderr_path(self):
        return os.path.join(self.config_dir_path(), 'qemu.stderr')

    def disk_image_path(self):
        return self.conf.get('qemu.image')

    def seed_path(self):
        return self.conf.get('qemu.image') + '.seed'

    def backing_image_path(self):
        backing_conf = config.VmStack(self.conf.get('vm.backing'))
        image_path = backing_conf.get('vm.published_as')
        return image_path

    def public_image_path(self):
        return self.conf.get('vm.published_as')

    def ips_from_arp(self, known=None):
        """Returns IP addresses for a given MAC address.

        This relies on arp and can be fed with a set of IPs known have been
        used in the past. This makes it possible to detect only (one) new IP
        when it's revealed.

        :param known: A list of known IPs as returned from a previous call.
        """
        if known is None:
            known = []
        mac_addr = self.conf.get('qemu.mac.address')
        bridge = self.conf.get('qemu.bridge')
        arp_cmd = ['arp', '-a', '-n', '-i', bridge]
        logger.debug('Running {}'.format(' '.join(arp_cmd)))
        arp = pexpect.spawn(arp_cmd[0], arp_cmd[1:])
        # Should match:
        # ? (192.168.0.178) at 0e:00:00:01:91:50 [ether] on br0
        ip_re = '\((\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\) at ' + mac_addr
        ips = []
        while True:
            ip_match = arp.expect([pexpect.EOF, ip_re])
            if ip_match:
                ip = arp.match.groups()[0].decode('utf8')
                if ip not in known:
                    ips.append(ip)
            else:
                break
        logger.debug('Found [{}] in arp output'.format(','.join(ips)))
        return ips

    def capture_ip(self):
        """Capture the qemu IP address in vm.ip.

        This avoids relying on cloud-init to get the IP address as long as
        'ping host' is enough to populate the arp cache. The underlying
        assumption is that the localhost should be able to resolve the host to
        IP translation (which is generally true when the dhcp server also
        populate the dns server(s)).
        """
        mac_addr = self.conf.get('qemu.mac.address')
        ping_cmd = 'ping -c1 {}'.format(self.conf.get('vm.name'))
        cpos = self.conf.get('qemu.setup_ip.timeouts')
        me = self.capture_ip.__name__
        # See what IPs are known for that mac address
        previous = self.ips_from_arp()
        for attempt, sleep in enumerate(cpos, start=1):
            logger.debug('Running {}'.format(ping_cmd))
            # If a new mac address is seen, the dhcp server should provide a
            # new IP. ping'ing the vm name should make that IP appear in the
            # arp tables.
            ping_output, ret = pexpect.run(ping_cmd, withexitstatus=True)
            ping_output = ping_output.decode('utf8')
            logger.debug('Ping output: {}'.format(ping_output))
            if not ret:
                # ping succeeded so the host can be found from the localhost it
                # should come with a new IP not seen before
                new_ips = self.ips_from_arp(previous)
                logger.debug('New IPs from arp: [{}]'.format(
                    ','.join(new_ips)))
                the_ip = 'not known yet'
                if len(new_ips) > 1:
                    raise errors.ByovError('{name} {mac} has weird {ips}',
                                           name=self.conf.get('vm.name'),
                                           mac=mac_addr, ips=new_ips)
                elif len(new_ips) == 1:
                    the_ip = new_ips[0]
                    self.econf.set('vm.ip', new_ips[0])
                else:
                    # No new IP appeared, from the ones known before the ping
                    # (somehow the host has already talked to the guest before
                    # the ping or when the guest is restarted), take the one
                    # appearing in the ping output
                    for p in previous:
                        if p in ping_output:
                            the_ip = p
                            break
                self.econf.set('vm.ip', the_ip)
                logger.info('{} IP is {}'.format(self.conf.get('vm.name'),
                                                 self.conf.get('vm.ip')))
                break
            logger.debug('Sleeping {:.2f} seconds for {} {}/{}'.format(
                sleep, me, attempt, cpos.retries))
            time.sleep(sleep)
        else:
            raise errors.ByovError('{name} {mac} never revealed an IP',
                                   name=self.conf.get('vm.name'),
                                   mac=mac_addr)

    def create_seed_image(self):
        if self._meta_data_path is None:
            self.create_meta_data()
        if self._user_data_path is None:
            self.create_user_data()
        seed_path = self.seed_path()
        self.ensure_dir(os.path.dirname(seed_path))
        subprocesses.run(
            ['genisoimage', '-output', seed_path,
             # cloud-init relies on the volid to discover its data
             '-volid', 'cidata',
             '-joliet', '-rock', '-input-charset', 'default',
             '-graft-points',
             'user-data=%s' % (self._user_data_path,),
             'meta-data=%s' % (self._meta_data_path,),
             ])
        self._seed_path = seed_path

    def setup_image(self):
        cmds = self.conf.get('qemu.image.setup')
        if cmds:
            # FIXME: If values need to be passed from command to command,
            # imgcmd.target may be involved... -- vila 2019-12-10
            for c in cmds:
                img = image_cmd_registry.get(c)
                imgcmd = img(self)
                imgcmd.setup()

    def teardown_image(self):
        cmds = self.conf.get('qemu.image.teardown')
        if cmds:
            for c in reversed(cmds):
                img = image_cmd_registry.get(c)
                img(self).teardown()

    def get_ssh_user_host_port(self):
        c = self.conf
        qemu_port = c.get('qemu.ssh.localhost.port')
        if qemu_port:
            return (c.get('ssh.user'), 'localhost', qemu_port)
        else:
            return super().get_ssh_user_host_port()

    def wait_for_cloud_init(self):
        self._wait_for_cloud_init('qemu.cloud_init.timeouts')

    def setup(self):
        logger.info('Setting up {} qemu...'.format(self.conf.get('vm.name')))
        if self._seed_path is None:
            self.create_seed_image()
        self.setup_image()
        self.spawn_qemu()
        self.wait_for_ssh()
        self.wait_for_cloud_init()
        self.setup_over_ssh()

    def start(self):
        super(Qemu, self).start()
        logger.info('Starting {} qemu...'.format(self.conf.get('vm.name')))
        # FIXME: Due to cloud-init disabling itself if the seed is not mounted
        # (see
        # https://bugs.launchpad.net/ubuntu/+source/cloud-init/+bug/1669675 and
        # https://bugs.launchpad.net/cloud-init/+bugs?field.tag=dsid), force
        # the seed below. Otherwise, we fail to find the IP address which is
        # provided by cloud-init -- vila 2019-10-15
        self.spawn_qemu(with_seed=True)
        self.wait_for_ssh()
        self.save_existing_config()

    def stop(self):
        logger.info('Stopping {} qemu...'.format(self.conf.get('vm.name')))
        with Monitor(self) as monitor:
            logger.debug('Sending system_powerdown...')
            monitor.sendline('system_powerdown')
            ret = monitor.expect([pexpect.EOF, pexpect.TIMEOUT])
            if ret:
                # We got a timeout, something bad is going on, escalate
                monitor.sendline('quit')
                try:
                    monitor.expect([pexpect.EOF, pexpect.TIMEOUT])
                except Exception:
                    # This will help understand when and why this can fail
                    logger.debug('monitor.expect failed', exc_info=True)
                    raise
                # FIXME: Report stderr on timeout here ? Start warning above
                # about qemu potentially left in an unbootable env ?
                # -- vila 2019-12-09

        # When the qemu process finish, no monitor connection can succeed
        stmos = self.conf.get('qemu.stop.timeouts')
        me = self.stop.__name__
        for attempt, sleep in enumerate(stmos, start=1):
            try:
                with MonitorSocket(self):
                    logger.debug('Socket is still up.')
            except ConnectionRefusedError:
                logger.debug('Socket is down.')
                break
            logger.debug('Sleeping {:.2f} seconds for {} {}/{}'.format(
                sleep, me, attempt, stmos.retries))
            time.sleep(sleep)
        else:
            raise errors.ByovError('{name} never stopped',
                                   name=self.conf.get('vm.name'))

    def teardown(self, force=False):
        if force and self.state() == 'RUNNING':
            self.stop()
        if self.state() == 'RUNNING':
            self.terminate_qemu()
        self.teardown_image()
        self.remove(self.seed_path())
        self.remove(self.stdout_path())
        self.remove(self.stderr_path())
        self.remove(self.monitor_path())
        super(Qemu, self).teardown()

    def publish(self):
        # FIXME: Probably worth rewriting with ImageCommand -- vila 2019-12-08
        # FIXME: ImageCommand should also provide a way to publish an image
        # from a disk other than the booting one -- vila 2019-12-19
        image_path = self.public_image_path()
        logger.info('Publishing qemu image {} from {}...'.format(
            image_path, self.conf.get('vm.name')))
        publish_command = ['cp', self.disk_image_path(), image_path]
        subprocesses.run(publish_command)

    def unpublish(self):
        # FIXME: Should published_as be registered in econf so that unpublish
        # use that ? That would allow removing an old image when the name is
        # changed. -- vila 2019-11-16
        # FIXME: Probably worth rewriting with ImageCommand -- vila 2019-12-08
        image_path = self.public_image_path()
        logger.info('Un-publishing {} qemu image from {}...'.format(
            image_path, self.conf.get('vm.name')))
        unpublish_command = ['rm', '-f', image_path]
        subprocesses.run(unpublish_command)
