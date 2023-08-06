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
import subprocess
import sys

try:
    if sys.version_info < (3,):
        # novaclient doesn't support python3 (yet)
        from byov.vms import nova
        with_nova = True
    else:
        with_nova = False
except ImportError:
    with_nova = False

try:
    from byov.vms import ec2
    with_ec2 = True
except ImportError:
    with_ec2 = False

from byoc import errors
from byot import features
from byov import (
    config,
    subprocesses,
)
from byov.vms import (
    docker,
    scaleway,
)


class SshFeature(features.ExecutableFeature):

    def __init__(self):
        super().__init__('ssh')
        self.version = None

    def _probe(self):
        exists = super(SshFeature, self)._probe()
        if exists:
            try:
                proc = subprocess.Popen(['ssh', '-V'],
                                        stderr=subprocess.PIPE,
                                        stdout=subprocess.PIPE)
                out, err = proc.communicate()
            except OSError as e:
                if e.errno == errno.ENOENT:
                    # broken install
                    return False
                else:
                    raise
            self.version = err.decode()
        return exists


def requires_existing_vm(test, vm_name):
    """Skip a test if a known reference vm is not provided locally.

    :note: This may be revisited later when it becomes easier to create vms for
       test purposes.

    :note: This should be called after fixtures.setup_tests_config() has been
    called so the user-provided test config is installed.

    :param test: The TestCase requiring the vm.

    :param vm_name: The vm name in the config.

    """
    user_conf = config.VmStack(vm_name)
    # FIXME: This is suspicious and seem to explain why vm.name is set in test
    # config files -- vila 2018-07-29
    if user_conf.get('vm.name') != vm_name:
        test.skipTest('{} is not defined'.format(vm_name))
    kls = user_conf.get('vm.class')
    vm = kls(user_conf)
    if vm.state() == 'UNKNOWN':
        test.skipTest('{} has not been setup'.format(vm_name))


def requires_remote_lxd(test):
    """Skip a test if no configuration is found for lxd remote access."""
    remote_name = 'byov-tests-remote-lxd'
    conf = config.VmStack(remote_name)
    remote_lxd = conf.get('remote.name')
    if not remote_lxd:
        test.skipTest('{} is not defined'.format(remote_name))
    return remote_lxd


def requires_existing_bridge(test, br_name):
    """Skip a test if a bridge does not exists."""
    br_path = '/sys/class/net/{}/bridge'.format(br_name)
    # This doesn't verify the bridge is functional (how can this be achieved ?)
    # but can be used by any user (i.e. not root).
    if not os.path.exists(br_path):
        test.skipTest('{} is not defined'.format(br_path))


class NovaCompute(features.Feature):

    def _probe(self):
        if not with_nova:
            # novaclient doesn't support python3 (yet)
            return False
        client = self.get_client()
        if client is None:
            return False
        try:
            # can transiently fail with requests.exceptions.ConnectionError
            # (converted from MaxRetryError).
            client.authenticate()
        except nova.exceptions.ClientException:
            return False
        return True

    def get_client(self):
        # The byov-tests-nova vm is not required to exist, we'll get
        # credentials from the environment if they are defined there.
        test_vm_conf = config.VmStack('byov-tests-nova')
        try:
            return nova.get_os_nova_client(test_vm_conf)
        except errors.OptionMandatoryValueError:
            return None


class NovaCredentials(features.Feature):

    def _probe(self):
        if not with_nova:
            # novaclient doesn't support python3 (yet)
            return False
        try:
            config.VmStack('byov-tests-nova').get_nova_creds()
        except errors.OptionMandatoryValueError:
            return False
        return True

    def feature_name(self):
        return 'A valid set of nova credentials'


class Ec2Boto3(features.Feature):

    def __init__(self):
        super().__init__()
        self.version = None

    def _probe(self):
        if not with_ec2:
            return False
        client = self.get_client()
        if client is None:
            return False
        self.version = tuple([int(v)
                              for v in ec2.boto3.__version__.split('.')])
        if self.version < (1, 21, 0):
            return False
        try:
            # t3.micro is available where t2.micro is not depending on regions
            client.instance_types(['t2.micro', 't3.micro'], True)
        except (ec2.Ec2ServerException, ec2.botocore.exceptions.ClientError):
            # When the credentials are invalid the botocore exception is
            # translated into an Ec2ServerException.
            return False
        return True

    def get_client(self):
        # FIXME: the byov-tests-ec2 does not exist -- vila 2021-12-03
        # The byov-tests-ec2 vm is not required to exist, we'll get
        # credentials from the environment if they are defined there.
        test_vm_conf = config.VmStack('byov-tests-ec2')
        try:
            return ec2.Ec2Client(test_vm_conf)
        except errors.OptionMandatoryValueError:
            return None

    def feature_name(self):
        return 'boto3 client version >= 1.21.0'


class Ec2Credentials(features.Feature):

    def _probe(self):
        if not with_ec2:
            return False
        try:
            # FIXME: the byov-tests-ec2 does not exist -- vila 2021-12-03
            config.VmStack('byov-tests-ec2').get_aws_creds()
        except errors.OptionMandatoryValueError:
            return False
        return True

    def feature_name(self):
        return 'A valid set of aws credentials'


class ScalewayCredentials(features.Feature):

    def _probe(self):
        try:
            config.VmStack('byov-tests-scaleway').get_scaleway_creds()
        except errors.OptionMandatoryValueError:
            return False
        return True

    def feature_name(self):
        return 'A valid set of scaleway credentials'


# FIXME: Strictly speaking, ScalewayImage should require
# ScalewayCredentials. In practice, it's easier to require a config object here
# which already knows the credentials but also provide the image name and
# architecture. -- vila 2018-10-14
class ScalewayImage(features.Feature):

    def __init__(self, conf):
        super(ScalewayImage, self).__init__()
        self.conf = conf
        self.image = self.conf.get('scaleway.image')
        self.architecture = scaleway.scaleway_architectures[
            self.conf.get('vm.architecture')]

    def _probe(self):
        vm = scaleway.Scaleway(self.conf)
        try:
            vm.find_scaleway_image(self.image, self.architecture)
        except scaleway.ScalewayComputeException:
            return False
        return True

    def feature_name(self):
        return 'Image {} at scaleway'.format(self.image)


class TestsConfig(features.Feature):
    """User provided tests configuration.

    Some tests require existing vms that the user needs to
    provide. 'byov.conf-tests' define the vms and should be under
    ~/.config/byov'.

    """

    def __init__(self):
        super(TestsConfig, self).__init__()
        self.user_path = os.path.join(config.user_config_dir(),
                                      'byov.conf-tests')
        self.more_paths = list(config.config_files_in(config.user_config_dir(),
                                                      suffix='.conf-tests'))

    def _probe(self):
        # We only test that the config files exists here, tests can make more
        # checks about the content (like ssh.key and the
        # byov-tests-lxd-debian vm)
        return os.path.exists(self.user_path)

    def feature_name(self):
        return 'User-provided configuration to setup test vms'


class LxdNesting(features.Feature):

    def __init__(self, level):
        super(LxdNesting, self).__init__()
        self.level = level

    def _probe(self):
        from byov.vms import lxd
        return lxd.check_nesting(self.level)

    def feature_name(self):
        return ('lxd configured to nest containers'
                ' up to {} level{}'.format(self.level,
                                           's' if self.level > 1 else ''))


# FIXME: This is broken by design. It should be a vm declared in the config
# files so tests that requires it can setup/teardown rather than leaving the
# container running -- vila 2022-01-19
class DockerRegistry(features.Feature):
    """On-demand docker image registry."""

    def _probe(self):
        conf = config.VmStack(None)
        info = docker.container_info(conf.get('docker.registry.name'))
        if info['state'] != 'RUNNING':
            docker_registry_command = conf.get('docker.registry.command')
            ret, out, err = subprocesses.run(docker_registry_command)
        return True

    def feature_name(self):
        return 'docker test image registry'


# There is always a single instance of a given feature (so it's probed only
# once) shared by all tests, they are all declared below to be easier to find.

# FIXME: Is it worth it to have wget as a soft dependency when downloads are
# easy enough to be handled at the http level ? Error handling and timeouts are
# not yet implemented around wget either and would also be simpler at the http
# level. -- vila 2019-11-08
bzr_feature = features.ExecutableFeature('bzr')
docker_client_feature = features.ExecutableFeature('docker')
ec2_boto3 = Ec2Boto3()
ec2_creds = Ec2Credentials()
git_feature = features.ExecutableFeature('git')
lxd_client_feature = features.ExecutableFeature('lxc')
lxd_nesting_1 = LxdNesting(1)
nova_compute = NovaCompute()
nova_creds = NovaCredentials()
py3_feature = features.ExecutableFeature('python3')
qemu_img_feature = features.ExecutableFeature('qemu-img')
scaleway_creds = ScalewayCredentials()
ssh_feature = SshFeature()
tests_config = TestsConfig()
wget_feature = features.ExecutableFeature('wget')

# Useful shortcuts to export
requires = features.requires
test_requires = features.test_requires
