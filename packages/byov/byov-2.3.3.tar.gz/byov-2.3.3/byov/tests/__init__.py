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
import functools
import io
import logging
import unittest


from byot import (
    assertions,
    results,
)

# Since config.vm_class_registry is populated when commands is imported and
# since some tests are parametrized based on its content, it should be imported
# early.
from byov import commands
# Make sure pep8 is happy
__fake = commands.logger
del __fake


class TestLogger(logging.Logger):
    """A logger dedicated to a given test.

    Log messages are captured in a string buffer.
    """

    def __init__(self, test, level=logging.DEBUG,
                 fmt='%(asctime)-15s %(message)s'):
        super(TestLogger, self).__init__(test.id(), level)
        self.stream = io.StringIO()
        handler = logging.StreamHandler(self.stream)
        handler.setFormatter(logging.Formatter(fmt))
        self.addHandler(handler)

    def getvalue(self):
        return self.stream.getvalue()


class log_on_failure(object):
    """Decorates a test to display log on failure.

    This adds a 'logger' attribute to the parameters of the decorated
    test. Using this logger the test can display its content when it fails or
    errors but stay silent otherwise.
    """

    def __init__(self, level=logging.INFO, fmt='%(message)s'):
        self.level = level
        self.fmt = fmt

    def __call__(self, func):

        @functools.wraps(func)
        def decorator(*args):
            test = args[0]
            logger = TestLogger(test, level=self.level, fmt=self.fmt)
            display_log = True

            # We need to delay the log acquisition until we attempt to display
            # it (or we get no content).
            def delayed_display_log():
                msg = 'Failed test log: >>>\n{}\n<<<'.format(logger.getvalue())
                if display_log:
                    raise Exception(msg)

            test.addCleanup(delayed_display_log)

            # Run the test without the decoration
            func(*args + (logger,))
            # If it terminates properly, disable log display
            display_log = False

        return decorator


class TestLogOnFailure(unittest.TestCase):

    def setUp(self):
        super(TestLogOnFailure, self).setUp()
        self.result = results.TextResult(io.StringIO(), verbosity=2)

        # We don't care about timing here so we always return 0 which
        # simplifies matching the expected result
        def zero(atime):
            return 0.0

        self.result.convert_delta_to_float = zero
        # Inner tests will set this from the logger they receive so outter
        # tests can assert the content.
        self.logger = None

    def test_log_not_displayed(self):

        class Test(unittest.TestCase):

            @log_on_failure()
            def test_pass(inner, logger):
                self.logger = logger
                logger.info('pass')

        t = Test('test_pass')
        t.run(self.result)
        self.assertEqual('pass\n', self.logger.getvalue())
        self.assertEqual('{} ... OK (0.000 secs)\n'.format(t.id()),
                         self.result.stream.getvalue())
        self.assertEqual([], self.result.errors)

    def test_log_displayed(self):

        class Test(unittest.TestCase):

            @log_on_failure()
            def test_fail(inner, logger):
                self.logger = logger
                logger.info("I'm broken")
                inner.fail()

        t = Test('test_fail')
        t.run(self.result)
        self.assertEqual("I'm broken\n", self.logger.getvalue())
        # FAILERROR: The test FAIL, the cleanup ERRORs out.
        self.assertEqual(
            '{} ... FAILERROR (0.000 secs)\n'.format(t.id()),
            self.result.stream.getvalue())
        assertions.assertLength(self, 1, self.result.errors)
        failing_test, traceback = self.result.errors[0]
        self.assertIs(t, failing_test)
        expected = traceback.endswith("Failed test log:"
                                      " >>>\nI'm broken\n\n<<<\n")
        self.assertTrue(expected, 'Actual traceback: {}'.format(traceback))

    def test_log_debug_not_displayed(self):

        class Test(unittest.TestCase):

            @log_on_failure()
            def test_debug_silent(inner, logger):
                self.logger = logger
                logger.debug('more info')
                self.fail()

        t = Test('test_debug_silent')
        t.run(self.result)
        self.assertEqual('', self.logger.getvalue())

    def test_log_debug_displayed(self):

        class Test(unittest.TestCase):

            @log_on_failure(level=logging.DEBUG)
            def test_debug_verbose(inner, logger):
                self.logger = logger
                logger.debug('more info')
                self.fail()

        t = Test('test_debug_verbose')
        t.run(self.result)
        self.assertEqual('more info\n', self.logger.getvalue())
