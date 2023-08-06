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
import errno
import os
import unittest

from byot import fixtures
from byov import (
    errors,
    subprocesses,
)


class TestRun(unittest.TestCase):

    def setUp(self):
        super(TestRun, self).setUp()
        fixtures.set_uniq_cwd(self)

    def test_success(self):
        ret, out, err = subprocesses.run(['echo', '-n', 'Hello'])
        self.assertEqual(0, ret)
        self.assertEqual('Hello', out)
        self.assertEqual('', err)

    def test_with_input(self):
        ret, out, err = subprocesses.run(['cat', '-'], 'bar\n')
        self.assertEqual(0, ret)
        self.assertEqual('bar\n', out)
        self.assertEqual('', err)

    def test_failure(self):
        with self.assertRaises(errors.CommandError) as cm:
            subprocesses.run(['ls', 'I-dont-exist'])
        self.assertEqual(2, cm.exception.retcode)
        self.assertEqual('', cm.exception.out)
        self.assertTrue('I-dont-exist' in cm.exception.err)

    def test_raise_on_error(self):
        retcode, out, err = subprocesses.run(
            ['ls', 'I-dont-exist'], raise_on_error=False)
        self.assertEqual(2, retcode)
        self.assertEqual('', out)
        self.assertTrue('I-dont-exist' in err)

    def test_error(self):
        with self.assertRaises(FileNotFoundError) as cm:
            subprocesses.run(['I-dont-exist'])
        self.assertEqual(errno.ENOENT, cm.exception.errno)
        self.assertEqual("No such file or directory",
                         cm.exception.strerror)
        self.assertEqual('I-dont-exist', cm.exception.filename)


class TestPipe(unittest.TestCase):

    def setUp(self):
        super(TestPipe, self).setUp()
        fixtures.set_uniq_cwd(self)

    def test_success(self):
        proc = subprocesses.pipe(['echo', '-n', 'Hello'])
        self.assertEqual('Hello', proc.stdout.read().decode('utf8'))

    def test_failure(self):
        proc = subprocesses.pipe(['ls', 'I-dont-exist'])
        self.assertTrue('I-dont-exist' in proc.stdout.read().decode('utf8'))
        # We get the above in stdout because stderr is redirected there
        self.assertIs(None, proc.stderr)

    def test_error(self):
        with self.assertRaises(FileNotFoundError) as cm:
            subprocesses.pipe(['I-dont-exist'])
        self.assertEqual(errno.ENOENT, cm.exception.errno)
        self.assertEqual("No such file or directory",
                         cm.exception.strerror)
        self.assertEqual('I-dont-exist', cm.exception.filename)


class TestWhich(unittest.TestCase):

    def setUp(self):
        super().setUp()
        fixtures.set_uniq_cwd(self)

    def test_empty_path(self):
        self.assertEqual(None, subprocesses.which('/bin/true', []))

    def test_current_dir(self):
        with open('script', 'w') as f:
            f.write('''#!/bin/sh\ntrue\n''')
        os.chmod('script', 0o755)
        self.assertEqual('./script', subprocesses.which('script', ['.']))

    def test_subdir(self):
        os.mkdir('sub')
        path = os.path.join('sub', 'script')
        with open(path, 'w') as f:
            f.write('''#!/bin/sh\ntrue\n''')
        os.chmod(path, 0o755)
        self.assertEqual('sub/script', subprocesses.which(
            'script', ['.', 'sub']))

# MISSINGTESTS:
# test_ssh_no_args (hard, interactive session)
# test_ssh_simple_command
# test_ssh_cant_connect (wrong host, unknown host, missing key, wrong user)
