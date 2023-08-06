# This file is part of Build Your Own Virtual machine.
#
# Copyright 2021 Vincent Ladeuil.
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

import unittest

from byot import (
    scenarii,
)


from byov import (
    config,
    options,
)
from byov.tests import (
    features,
    fixtures,
)

try:
    from byov.vms import ec2
except ImportError:
    pass


load_tests = scenarii.load_tests_with_scenarios


@features.requires(features.ec2_creds)
@features.requires(features.ec2_boto3)
class TestTags(unittest.TestCase):
    """Test all tags used on ec2 resources to monitor usage and leaks."""
    maxDiff = None

    def setUp(self):
        super().setUp()
        fixtures.setup_tests_config(self)
        fixtures.set_uniq_vm_name(self)
        conf = config.VmStack(self.vm_name)
        conf.set('vm.class', 'ec2')
        conf.set('vm.name', self.vm_name)
        conf.set('vm.distribution', 'ubuntu')
        conf.set('vm.release', 'focal')
        self.conf = conf
        fixtures.override_logging(self)
        self.vm = ec2.Ec2Server(self.conf)

    def test_instance_tags(self):
        tags = self.vm.instance_tags()
        self.assertEqual([{'ResourceType': 'instance',
                           'Tags':
                           [{'Key': 'Name', 'Value': self.vm_name},
                            {'Key': 'test.id', 'Value': self.id()}]}],
                         tags)

    def test_image_tags(self):
        tags = self.vm.image_tags()
        self.assertEqual([{'ResourceType': 'image',
                           'Tags':
                           [{'Key': 'Name', 'Value': self.vm_name},
                            {'Key': 'test.id', 'Value': self.id()}]},
                          {'ResourceType': 'snapshot',
                           'Tags':
                           [{'Key': 'Name', 'Value': self.vm_name},
                            {'Key': 'test.id', 'Value': self.id()}]}],
                         tags)


@features.requires(features.ec2_creds)
@features.requires(features.ec2_boto3)
class TestDescribeInstanceTypes(unittest.TestCase):

    def setUp(self):
        super().setUp()
        fixtures.setup_tests_config(self)
        conf = config.VmStack('testing-testbed')
        conf.set('vm.class', 'ec2')
        conf.set('vm.name', 'testing-testbed')
        conf.set('vm.distribution', 'ubuntu')
        conf.set('vm.release', 'focal')
        self.conf = conf
        fixtures.override_logging(self)
        self.ec2_client = ec2.Ec2Client(self.conf)

    def test_unknown_type(self):
        with self.assertRaises(ec2.Ec2ServerException) as cm:
            self.ec2_client.instance_types(['unknown'], free_tier=True)
        boto_exc = cm.exception.boto_exc
        self.assertTrue(boto_exc.args[0].endswith('do not exist: [unknown]'))
        self.assertEqual('DescribeInstanceTypes', boto_exc.operation_name)
        resp = boto_exc.response
        self.assertEqual(400, resp['ResponseMetadata']['HTTPStatusCode'])

    def test_free(self):
        # Careful with an empty list below we get all existing types (and then
        # filter the free ones).
        types = self.ec2_client.instance_types([], free_tier=True)
        self.assertEqual(['t1.micro', 't2.micro'], types)

    def test_all(self):
        # Careful with an empty list below we get all existing types (and then
        # filter out the free ones).
        types = self.ec2_client.instance_types([], free_tier=False)
        assert 400 < len(types)
        assert 't1.micro' not in types
        assert 't2.micro' not in types


@features.requires(features.ec2_creds)
@features.requires(features.ec2_boto3)
class TestDescribeImages(unittest.TestCase):

    def setUp(self):
        super().setUp()
        fixtures.setup_tests_config(self)
        conf = config.VmStack('testing-testbed')
        conf.set('vm.class', 'ec2')
        conf.set('vm.name', 'testing-testbed')
        conf.set('vm.distribution', 'ubuntu')
        conf.set('vm.release', 'focal')
        conf.set('vm.architecture', 'amd64')
        self.conf = conf
        fixtures.override_logging(self)
        self.ec2_client = ec2.Ec2Client(self.conf)

    def images(self, image_id=None):
        arch = ec2.ec2_architectures[self.conf.get('vm.architecture')]
        owners = ec2.ec2_image_owners.get(self.conf.get('vm.distribution'),
                                          ['self'])
        return self.ec2_client.images(arch, owners, image_id)

    def test_malformed_image(self):
        with self.assertRaises(ec2.Ec2ServerException) as cm:
            self.images(image_id='not-an-ami')
        boto_exc = cm.exception.boto_exc
        self.assertTrue('InvalidAMIID.Malformed' in boto_exc.args[0])
        self.assertTrue('Invalid id: "not-an-ami"' in boto_exc.args[0])
        self.assertEqual('DescribeImages', boto_exc.operation_name)
        resp = boto_exc.response
        self.assertEqual(400, resp['ResponseMetadata']['HTTPStatusCode'])

    def test_unknown_image(self):
        with self.assertRaises(ec2.Ec2ServerException) as cm:
            # Empirically found a well formed but not existing image for this
            # test
            self.images(image_id='ami-01fffffffffffffff')
        boto_exc = cm.exception.boto_exc
        self.assertTrue('InvalidAMIID.NotFound' in boto_exc.args[0])
        self.assertTrue(boto_exc.args[0].endswith(
            "'[ami-01fffffffffffffff]' does not exist"))
        self.assertEqual('DescribeImages', boto_exc.operation_name)
        resp = boto_exc.response
        # 404 sounds more appropriate but ec2 says 400
        self.assertEqual(400, resp['ResponseMetadata']['HTTPStatusCode'])

    def test_some_images(self):
        # At the time of writing this test, there are 156.100 available images
        # 116.000 still for virt. type hvm and x86_64 arch
        # 116.00 still for type machine
        # 18.000 when filtering on owner (self, amazon, canonical, debian and
        #        redhat)
        #  6.800 when filtering on owner (self, canonical)
        images = self.images()
        self.assertTrue(6800 < len(images))

    def test_known_image_id(self):
        # was ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-20211129
        # on 2021-11-30
        # FIXME: We need either a stable id or be prepared to update the test
        # when the used one become unavailable -- vila 2021-11-30
        images = self.images(image_id='ami-04505e74c0741db8d')
        self.assertEqual(1, len(images))


@features.requires(features.ec2_creds)
@features.requires(features.ec2_boto3)
class TestFindEc2Image(unittest.TestCase):

    def setUp(self):
        super().setUp()
        fixtures.setup_tests_config(self)
        conf = config.VmStack('testing-testbed')
        conf.set('vm.class', 'ec2')
        conf.set('vm.name', 'testing-testbed')
        conf.set('vm.distribution', 'ubuntu')
        conf.set('vm.architecture', 'amd64')
        conf.set('vm.release', 'focal')
        self.conf = conf
        fixtures.override_logging(self)
        self.tb = ec2.Ec2Server(self.conf)

    def test_no_image(self):
        with self.assertRaises(options.OptionMandatoryValueError) as cm:
            self.tb.find_ec2_image()
        self.assertEqual('ec2.image must be set.', str(cm.exception))

    def test_known_image(self):
        # FIXME: Use a better value for ec2.image -- vila 2021-12-08
        self.conf.set('ec2.image', '^ubuntu')
        expected = 'ami-04505e74c0741db8d'
        self.conf.set('ec2.image.id', expected)
        image_id = self.tb.find_ec2_image()['ImageId']
        self.assertEqual(expected, image_id)


@features.requires(features.ec2_creds)
@features.requires(features.ec2_boto3)
class TestFindEc2ImageByDistribution(unittest.TestCase):

    scenarios = scenarii.multiply_scenarios(
        # distro/series
        ([('ubuntu,focal', dict(distro='ubuntu', release='focal')),
          ('ubuntu,impish', dict(distro='ubuntu', release='impish')),
          ('debian,10', dict(distro='debian', release='10')),
          ('debian,11', dict(distro='debian', release='11')),
          ('al2', dict(distro='amazon', release='2'))]),
        # architectures
        ([('amd64', dict(arch='amd64'))]))

    def setUp(self):
        super().setUp()
        fixtures.setup_tests_config(self)
        conf = config.VmStack('testing-testbed')
        conf.set('vm.class', 'ec2')
        conf.set('vm.name', 'testing-testbed')
        conf.set('vm.distribution', self.distro)
        conf.set('vm.architecture', self.arch)
        conf.set('vm.release', self.release)
        conf.set('ec2.image', options.ec2_image_re_registry.get(self.distro))
        conf.set('aws.region', 'us-east-1')
        self.conf = conf
        fixtures.override_logging(self)
        self.tb = ec2.Ec2Server(self.conf)

    def test_default_image(self):
        image = self.tb.find_ec2_image()
        self.assertTrue(image['ImageId'] is not None)
        # FIXME: stricter checks around distribution/series/arch ?
        # -- vila 2022-02-11


@features.requires(features.ec2_creds)
@features.requires(features.ec2_boto3)
class TestTestbed(unittest.TestCase):

    def setUp(self):
        super(TestTestbed, self).setUp()
        fixtures.setup_tests_config(self)
        conf = config.VmStack('testing-testbed')
        conf.set('vm.class', 'ec2')
        conf.set('vm.name', 'testing-testbed')
        conf.set('vm.distribution', 'ubuntu')
        conf.set('vm.release', 'focal')
        conf.set('vm.architecture', 'amd64')
        self.conf = conf
        fixtures.override_logging(self)

    # FIXME: This should fail. It's valid to not set ec2.image and relies on
    # ec2.distribution.images instead -- vila 2022-02-11
    def test_no_ec2_image(self):
        tb = ec2.Ec2Server(self.conf)
        self.addCleanup(tb.teardown)
        with self.assertRaises(options.OptionMandatoryValueError) as cm:
            tb.setup()
        self.assertEqual('ec2.image must be set.', str(cm.exception))

    def test_no_instance_types(self):
        tb = ec2.Ec2Server(self.conf)
        self.addCleanup(tb.teardown)
        tb.conf.set('ec2.instance.types', '')
        with self.assertRaises(ec2.Ec2ServerException) as cm:
            tb.setup()
        self.assertEqual('ec2.instance.types must be set', str(cm.exception))

    def test_unknown_image(self):
        self.conf.set('ec2.image', '')
        image_name = 'ami-01fffffffffffffff'
        self.conf.set('ec2.image.id', image_name)
        tb = ec2.Ec2Server(self.conf)
        self.addCleanup(tb.teardown)
        with self.assertRaises(ec2.Ec2ServerException) as cm:
            tb.setup()
        msg_end = "The image id '[{}]' does not exist".format(image_name)
        self.assertTrue(str(cm.exception).endswith(msg_end), cm.exception)

    def test_unknown_type(self):
        itypes = 'I-dont-exist'
        self.conf.set('ec2.instance.types', itypes)
        tb = ec2.Ec2Server(self.conf)
        self.addCleanup(tb.teardown)
        with self.assertRaises(ec2.Ec2ServerException) as cm:
            tb.setup()
        msg_end = "instance types do not exist: [{}]".format(itypes)
        self.assertTrue(str(cm.exception).endswith(msg_end), cm.exception)

    def test_wait_for_instance_fails(self):
        self.conf.set('ec2.image', '')
        # Force a 0 timeout so the instance can't finish booting
        self.conf.set('ec2.boot.timeouts', '0, 0, 0')
        tb = ec2.Ec2Server(self.conf)
        self.addCleanup(tb.teardown)
        with self.assertRaises(ec2.Ec2ServerException) as cm:
            tb.setup()
        msg = ("{} never reached ['RUNNING']"
               " (was: UNKNOWN last)")
        msg = msg.format(tb.conf.get('ec2.instance.id'))
        self.assertEqual(msg, str(cm.exception))


# FIXME: parametrized by distribution ? -- vila 2017-12-06
@features.requires(features.ec2_creds)
@features.requires(features.ec2_boto3)
class TestUsableTestbed(unittest.TestCase):

    scenarios = scenarii.multiply_scenarios(
        # series
        ([('focal', dict(release='focal'))]),
        # architectures
        ([('amd64', dict(arch='amd64'))]))

    def setUp(self):
        super(TestUsableTestbed, self).setUp()
        fixtures.setup_tests_config(self)
        tb_name = 'testing-testbed-{}-{}'.format(self.release, self.arch)
        conf = config.VmStack(tb_name)
        conf.set('vm.class', 'ec2')
        conf.set('vm.name', tb_name)
        conf.set('vm.release', self.release)
        conf.set('vm.architecture', self.arch)
        conf.set('ec2.image', '')
        self.conf = conf
        fixtures.override_logging(self)

    def test_create_usable_testbed(self):
        tb = ec2.Ec2Server(self.conf)
        self.addCleanup(tb.teardown)
        tb.setup()
        # We should be able to ssh with the right user
        retcode, out, err = tb.shell_captured('whoami')
        self.assertEqual(0, retcode)
        self.assertEqual(self.conf.get('vm.user') + '\n', out)
