# This file is part of Build Your Own Virtual machine.
#
# Copyright 2018 Vincent Ladeuil.
# Copyright 2014, 2015, 2016 Canonical Ltd.
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
import os

from byov import (
    errors,
    subprocesses,
)


class ConsoleMonitor(object):
    """Monitor a console to identify known events."""

    def __init__(self, stream):
        super(ConsoleMonitor, self).__init__()
        self.stream = stream

    def scan(self):
        # FIXME: An overall timeout is needed there (in case things get really
        # wrong with cloud-init) -- vila 2015-04-15
        while True:
            line = self.stream.readline().decode(errors='replace')
            yield line
            if not line:
                raise errors.ConsoleEOFError()
            # MISSINGTEST: ' reboot: Power down\r\n' keeping an eye on finding
            # a more transparent way to test beginning and end of lines
            # (possibly using python universal newlines.  -- vila 2015-05-10
            elif (line.startswith(' * Will now halt') or
                  line.endswith(' reboot: Power down\r\n') or
                  # end of cloud-init with systemd
                  'Stopping Initial cloud-init' in line or
                  # end of wily cloud init with systemd
                  'Stopping Execute cloud user/final scripts' in line or
                  # end of xenial cloud init with systemd
                  'Stopped Execute cloud user/final scripts' in line or
                  "running 'modules:final'" in line):
                # That's our final_message, we're done
                return
            elif ('Failed loading yaml blob' in line or
                  'Unhandled non-multipart userdata starting' in line or
                  'failed to render string to stdout:' in line or
                  'Failed loading of cloud config' in line or
                  # MISSINGTESST: This is cloud-init being more explicit when
                  # it fails because of bugs in user-data -- vila 2015-05-10
                  'Failed running /var/lib/cloud/instance/scripts' in line):
                raise errors.CloudInitError(line)


def actual_file_size(path):
    """Return file size or None if the file doesn't exist.

    :param path: The file of interest.

    :return: 'path' size or None if the file doesn't exist.
    """
    try:
        stat = os.stat(path)
        return stat.st_size
    except OSError as e:
        if e.errno == errno.ENOENT:
            return None
        else:
            raise


class TailMonitor(ConsoleMonitor):

    def __init__(self, path, offset=None):
        cmd = ['tail', '-F', path]
        # MISSINGTEST
        if offset is not None:
            cmd += ['--bytes', '+{}'.format(offset)]
        proc = subprocesses.pipe(cmd)
        super(TailMonitor, self).__init__(proc.stdout)
        self.path = path
        self.cmd = cmd
        self.proc = proc
        self.lines = []

    def scan(self):
        try:
            for line in super(TailMonitor, self).scan():
                # FIXME: Arguably we should decode line from an utf8 encoding
                # as subprocesses.pipe() merges stderr into stdout and utf8
                # error messages have been observed in real life: 'tail: cannot
                # open \xe2\x80\x98/home/vila/vms/lxc1/console\xe2\x80\x99 for
                # reading: Permission denied\n' -- vila 2014-01-19
                self.lines.append(line)
                yield line
        finally:
            self.proc.terminate()
