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
import io
import unittest


from byot import fixtures
from byov import (
    errors,
    monitors,
)
from byov.tests import (
    fixtures as vms_fixtures,
)


class TestConsoleParsing(unittest.TestCase):

    def _scan_console_monitor(self, content):
        mon = monitors.ConsoleMonitor(io.BytesIO(content))
        lines = []
        for line in mon.scan():
            lines.append(line)
        return lines

    def test_fails_on_empty(self):
        with self.assertRaises(errors.ConsoleEOFError):
            self._scan_console_monitor(b'')

    def test_fail_on_knwon_cloud_init_errors(self):
        with self.assertRaises(errors.CloudInitError):
            self._scan_console_monitor(b'Failed loading yaml blob\n')
        with self.assertRaises(errors.CloudInitError):
            self._scan_console_monitor(
                b'Unhandled non-multipart userdata starting\n')
        with self.assertRaises(errors.CloudInitError):
            self._scan_console_monitor(
                b"failed to render string to stdout: cannot find 'uptime'\n")
        with self.assertRaises(errors.CloudInitError):
            self._scan_console_monitor(
                b"Failed loading of cloud config "
                b"'/var/lib/cloud/instance/cloud-config.txt'. "
                b"Continuing with empty config\n")

    def test_succeds_on_final_message(self):
        lines = self._scan_console_monitor(b'''
Lalala
I'm doing my work
It goes nicely
byovm finished installing in 1 seconds.
That was fast isn't it ?
 * Will now halt
[   33.204755] Power down.
''')
        # We stop as soon as we get the final message and ignore the rest
        self.assertEqual(' * Will now halt\n', lines[-1])


class TestConsoleParsingWithFile(unittest.TestCase):

    def setUp(self):
        super(TestConsoleParsingWithFile, self).setUp()
        vms_fixtures.isolate_from_disk(self)

    def _scan_file_monitor(self, content):
        with open('console', 'w') as f:
            f.write(content)
        mon = monitors.TailMonitor('console')
        for line in mon.scan():
            pass
        return mon.lines

    def test_succeeds_with_file(self):
        content = '''\
Yet another install
Going well
byovm finished installing in 0.5 seconds.
Wow, even faster !
 * Will now halt
Whatever, won't read that
'''
        lines = self._scan_file_monitor(content)
        expected_lines = content.splitlines(True)
        # Remove the last line that should not be seen
        expected_lines = expected_lines[:-1]
        self.assertEqual(expected_lines, lines)

    def xtest_fails_on_empty_file(self):
        # FIXME: We need some sort of timeout there... -- vila 2013-ish
        with self.assertRaises(errors.CommandError):
            self._scan_file_monitor('')

    def test_fail_on_knwon_cloud_init_errors_with_file(self):
        with self.assertRaises(errors.CloudInitError):
            self._scan_file_monitor('Failed loading yaml blob\n')
        with self.assertRaises(errors.CloudInitError):
            self._scan_file_monitor(
                'Unhandled non-multipart userdata starting\n')
        with self.assertRaises(errors.CloudInitError):
            self._scan_file_monitor(
                "failed to render string to stdout: cannot find 'uptime'\n")


class TestActualFileSize(unittest.TestCase):

    def setUp(self):
        super(TestActualFileSize, self).setUp()
        fixtures.set_uniq_cwd(self)

    def assertSize(self, expected, path):
        self.assertEqual(expected, monitors.actual_file_size(path))

    def test_empty_file(self):
        open('foo', 'w').close()
        self.assertSize(0, 'foo')

    def test_file_with_content(self):
        with open('foo', 'w') as f:
            f.write('bar')
        self.assertSize(3, 'foo')

    def test_unknown_file(self):
        self.assertSize(None, 'I-dont-exist')
