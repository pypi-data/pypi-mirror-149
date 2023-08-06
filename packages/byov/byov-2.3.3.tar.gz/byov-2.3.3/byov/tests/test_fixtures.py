# This file is part of Build Your Own Virtual machine.
#
# Copyright 2018 Vincent Ladeuil.
# Copyright 2014, 2016 Canonical Ltd.
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

import os
import logging
import unittest

from byot import assertions

from byov.tests import fixtures


class TestIsolateFromDisk(unittest.TestCase):

    def test_disk_preserved(self):
        real_home = os.path.expandvars('$HOME')

        class Inner(unittest.TestCase):

            def test_overridden(self):
                fixtures.isolate_from_disk(self)
                # We know expanduser will use $HOME which is set by
                # isolate_from_disk
                self.assertNotEqual(real_home, os.path.expandvars('$HOME'))
                path = os.path.expanduser('~/testing')
                with open(path, 'w') as f:
                    f.write('whatever')
                # Make sure the file is created in the right place
                self.assertTrue(os.path.exists(path))

        assertions.assertSuccessfullTest(self, Inner('test_overridden'))
        # Make sure the file wasn't created in the wrong place
        self.assertFalse(os.path.exists('~/testing'))


class TestOverrideLogging(unittest.TestCase):

    def test_handlers_preserved(self):
        # Keep a copy of the existing handlers
        installed_handlers = [h for h in logging.getLogger().handlers]

        class Inner(unittest.TestCase):

            def test_overridden(self):
                fixtures.override_logging(self, debug=True)
                root_logger = logging.getLogger()
                assertions.assertLength(self, 1, root_logger.handlers)
                # Careful here, debug=True means any log goes to stdout (aka
                # leaks). Alternatively, aka the day it fails, this should be
                # rewritten by redirecting stdout
                self.assertEqual(self.log_stream,
                                 root_logger.handlers[0].stream)
                self.assertEqual(logging.DEBUG, root_logger.level)

        assertions.assertSuccessfullTest(self, Inner('test_overridden'))
        self.assertEqual(installed_handlers, logging.getLogger().handlers)
