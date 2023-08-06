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

import sys
import unittest

from byoc import options
from byot import (
    assertions,
    scenarii,
)


from byov import config
from byov.tests import (
    features,
    fixtures,
)

try:
    if sys.version_info < (3,):
        # novaclient doesn't support python3 (yet)
        from byov.vms import nova
except ImportError:
    pass


load_tests = scenarii.load_tests_with_scenarios


@features.requires(features.nova_creds)
class TestByovImageName(unittest.TestCase):

    def test_valid_britney_image(self):
        self.assertEqual(
            'byov/britney/precise-amd64.img',
            nova.byov_image_name('britney', 'precise', 'amd64'))

    def test_valid_cloud_image(self):
        self.assertEqual(
            'byov/cloudimg/precise-amd64.img',
            nova.byov_image_name('cloudimg', 'precise', 'amd64'))

    def test_invalid_image(self):
        with self.assertRaises(ValueError) as cm:
            nova.byov_image_name('I-dont-exist', 'precise', 'amd64')
        self.assertEqual('Invalid image domain', str(cm.exception))


@features.requires(features.nova_creds)
@features.requires(features.nova_compute)
class TestNovaClient(unittest.TestCase):
    """Check the nova client behavior when it encounters exceptions.

    This is achieved by overriding specific methods from NovaClient and
    exercising it through the TestBed methods.
    """

    def setUp(self):
        super(TestNovaClient, self).setUp()
        fixtures.setup_tests_config(self)
        conf = config.VmStack('testing-nova-client')
        conf.set('vm.class', 'nova')
        # Default to precise
        conf.set('vm.release', 'precise')
        self.conf = conf
        fixtures.override_logging(self)

    def get_image_id(self, series, arch):
        return nova.byov_image_name('cloudimg', series, arch)

    def test_retry_is_called(self):
        self.retry_calls = []

        class RetryingNovaClient(nova.NovaClient):

            def __init__(inner, conf, **kwargs):
                # We don't want to wait, it's enough to retry
                super(RetryingNovaClient, inner).__init__(
                    conf, first_wait=0, wait_up_to=0, **kwargs)

            def retry(inner, func, *args, **kwargs):
                self.retry_calls.append((func, args, kwargs))
                return super(RetryingNovaClient, inner).retry(
                    func, *args, **kwargs)

        image_id = self.get_image_id('trusty', 'amd64')
        self.conf.set('nova.image', image_id)
        fixtures.patch(self, nova.NovaServer,
                       'nova_client_class', RetryingNovaClient)
        tb = nova.NovaServer(self.conf)
        self.assertEqual(image_id, tb.find_nova_image().name)
        assertions.assertLength(self, 1, self.retry_calls)

    def test_known_failure_is_retried(self):
        self.nb_calls = 0

        class FailingOnceNovaClient(nova.NovaClient):

            def __init__(inner, conf, **kwargs):
                # We don't want to wait, it's enough to retry
                super(FailingOnceNovaClient, inner).__init__(
                    conf, first_wait=0, wait_up_to=0, retries=1,
                    **kwargs)

            def fail_once(inner):
                self.nb_calls += 1
                if self.nb_calls == 1:
                    raise nova.client.requests.ConnectionError()
                else:
                    return inner.nova.flavors.list()

            def flavors_list(inner):
                return inner.retry(inner.fail_once)

        fixtures.patch(self, nova.NovaServer,
                       'nova_client_class', FailingOnceNovaClient)
        tb = nova.NovaServer(self.conf)
        tb.find_flavor()
        self.assertEqual(2, self.nb_calls)

    def test_unknown_failure_is_raised(self):

        class FailingNovaClient(nova.NovaClient):

            def __init__(inner, conf, **kwargs):
                # We don't want to wait, it's enough to retry
                super(FailingNovaClient, inner).__init__(
                    conf, first_wait=0, wait_up_to=0,
                    **kwargs)

            def fail(inner):
                raise AssertionError('Boom!')

            def flavors_list(inner):
                return inner.retry(inner.fail)

        fixtures.patch(self, nova.NovaServer,
                       'nova_client_class', FailingNovaClient)
        tb = nova.NovaServer(self.conf)
        # This mimics what will happen when we encounter unknown transient
        # failures we want to catch: an exception will bubble up and we'll have
        # to add it to NovaClient.retry().
        with self.assertRaises(nova.NovaServerException) as cm:
            tb.find_flavor()
        self.assertEqual('fail failed', str(cm.exception))


@features.requires(features.nova_creds)
@features.requires(features.nova_compute)
class TestTestbed(unittest.TestCase):

    def setUp(self):
        super(TestTestbed, self).setUp()
        fixtures.setup_tests_config(self)
        conf = config.VmStack('testing-testbed')
        conf.set('vm.class', 'nova')
        conf.set('vm.name', 'testing-testbed')
        # Default to precise
        conf.set('vm.release', 'precise')
        self.conf = conf
        fixtures.override_logging(self)

    def get_image_id(self, series='precise', arch='amd64'):
        return nova.byov_image_name('cloudimg', series, arch)

    def test_create_no_image(self):
        tb = nova.NovaServer(self.conf)
        with self.assertRaises(options.errors.OptionMandatoryValueError) as cm:
            tb.setup()
        self.assertEqual('nova.image must be set.', str(cm.exception))

    def test_create_no_flavor(self):
        tb = nova.NovaServer(self.conf)
        tb.conf.set('nova.flavors', '')
        with self.assertRaises(nova.NovaServerException) as cm:
            tb.setup()
        self.assertEqual('nova.flavors must be set', str(cm.exception))

    def test_create_unknown_image(self):
        image_name = "I don't exist and eat kittens"
        self.conf.set('nova.image', image_name)
        tb = nova.NovaServer(self.conf)
        with self.assertRaises(nova.NovaServerException) as cm:
            tb.setup()
        self.assertEqual('Image "{}" cannot be found'.format(image_name),
                         str(cm.exception))

    def test_create_unknown_flavor(self):
        flavors = "I don't exist and eat kittens"
        self.conf.set('nova.flavors', flavors)
        tb = nova.NovaServer(self.conf)
        with self.assertRaises(nova.NovaServerException) as cm:
            tb.setup()
        self.assertEqual('None of [{}] can be found'.format(flavors),
                         str(cm.exception))

    def test_wait_for_instance_fails(self):
        self.conf.set('nova.image', self.get_image_id())
        # Force a 0 timeout so the instance can't finish booting
        self.conf.set('nova.boot_timeout', '0')
        tb = nova.NovaServer(self.conf)
        self.addCleanup(tb.teardown)
        with self.assertRaises(nova.NovaServerException) as cm:
            tb.setup()
        msg = 'Instance {} never came up (last status: BUILD)'
        msg = msg.format(tb.instance.id)
        self.assertEqual(msg, str(cm.exception))

    def test_wait_for_instance_errors(self):
        self.conf.set('nova.image', self.get_image_id())
        tb = nova.NovaServer(self.conf)
        self.addCleanup(tb.teardown)

        def update_instance_to_error():
            # Fake an instance starting in error state
            tb.instance.status = 'ERROR'
            return True
        tb.update_instance = update_instance_to_error
        with self.assertRaises(nova.NovaServerException) as cm:
            tb.setup()
        msg = 'Instance {} never came up (last status: ERROR)'
        msg = msg.format(tb.instance.id)
        self.assertEqual(msg, str(cm.exception))


# FIXME: parametrized by distribution ? -- vila 2017-12-06
@features.requires(features.nova_creds)
@features.requires(features.nova_compute)
class TestUsableTestbed(unittest.TestCase):

    scenarios = scenarii.multiply_scenarios(
        # series
        ([('precise', dict(series='precise', result='skip')),
          ('trusty', dict(series='trusty', result='pass')),
          ('xenial', dict(series='xenial', result='pass')),
          ('yakkety', dict(series='yakkety', result='pass')),
          ('zesty', dict(series='zesty', result='pass'))]),
        # architectures
        ([('amd64', dict(arch='amd64')), ('i386', dict(arch='i386'))]))

    def setUp(self):
        super(TestUsableTestbed, self).setUp()
        fixtures.setup_tests_config(self)
        tb_name = 'testing-testbed-{}-{}'.format(self.series, self.arch)
        conf = config.VmStack(tb_name)
        conf.set('vm.class', 'nova')
        conf.set('vm.name', tb_name)
        conf.set('vm.release', self.series)
        self.conf = conf
        fixtures.override_logging(self)

    def get_image_id(self):
        return nova.byov_image_name('cloudimg', self.series, self.arch)

    def test_create_usable_testbed(self):
        self.conf.set('nova.image', self.get_image_id())
        tb = nova.NovaServer(self.conf)
        self.addCleanup(tb.teardown)
        tb.setup()
        # We should be able to ssh with the right user
        retcode, out, err = tb.shell_captured('whoami')
        self.assertEqual(0, retcode)
        self.assertEqual(self.conf.get('vm.user') + '\n', out)
