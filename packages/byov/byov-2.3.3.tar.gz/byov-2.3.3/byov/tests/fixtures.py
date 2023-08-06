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
from __future__ import unicode_literals

import io
import logging
import os
import sys


import byov
from byoc import stacks
from byot import fixtures
from byov import (
    config,
)
from byov.vms import (
    lxd,
)
from byov.tests import features

try:
    if sys.version_info < (3,):
        # novaclient doesn't support python3 (yet)
        from byov.vms import nova
except ImportError:
    pass
try:
    from byov.vms import ec2
    with_boto3 = bool(ec2)  # silly trick to pacify pyflakes
except ImportError:
    # No boto3, no ec2 vms.
    with_boto3 = False


HERE = os.path.abspath(os.path.dirname(__file__))
BRANCH_ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))


# Useful shortcuts
patch = fixtures.patch
override_env = fixtures.override_env


def isolate_from_disk(test):
    """Provide an isolated disk-based environment.

    A $HOME directory is setup as well as an /etc/ one so tests can setup
    config files.
    """
    fixtures.set_uniq_cwd(test)
    fixtures.isolate_from_env(test)
    # Isolate tests from the user environment
    test.home_dir = os.path.join(test.uniq_dir, 'home')
    os.mkdir(test.home_dir)
    fixtures.override_env(test, 'HOME', test.home_dir)
    # Also isolate from the system environment
    test.etc_dir = os.path.join(test.uniq_dir, config.system_config_dir()[1:])
    os.makedirs(test.etc_dir)
    fixtures.patch(test, config, 'system_config_dir', lambda: test.etc_dir)


def set_uniq_vm_name(test, short=False):
    """To isolate tests from each other, created vms need a unique name.

    To keep those names legal and still user-readable we use the class name and
    the test method name. The process id is added so that the same test suite
    can be run on the same host in several processes.

    :param short: Defaults to False. Use only the test method and the pid. This
        helps with qemu unix socket names being limited in length.
    """
    if short:
        vm_name = '{}-{}'.format(test._testMethodName, os.getpid())
    else:
        vm_name = '{}-{}-{}'.format(test.__class__.__name__,
                                    test._testMethodName,
                                    os.getpid())
    # '_' are not valid in hostnames
    test.vm_name = vm_name.replace('_', '-')


# FIXME: Cruft is starting to accumulate here. 1) There is a tension around the
# isolation that happens below and contradicting needs to access user
# configuration (before isolation) /and/ setting up the test configuration
# (after isolation). 2) At least ec2, lxd, qemu backends co-exist rather than
# being selective -- vila 2019-11-16

# FIXME: (2) should be addressed by creating setup_tests_config_ec2,
# setup_tests_config_qemu and setup_tests_config_lxd, all calling
# setup_tests_config internally -- vila 2022-04-05
def setup_tests_config(test):
    """Setup user provided configuration for tests.

    A self.uniq_dir/etc/byov.conf is created from
    ~/.config/byov/byov.conf-tests with a pre-defined set of config
    options.

    If files ending with '.conf-tests' exist under '~/.config/byov/conf.d',
    they are installed under 'test.etc_dir/conf.d' without the '-tests' suffix.

    """
    # Get a user configuration before isolation
    user_conf = config.VmStack(None)
    # qemu relies on images being provided (hence downloaded) by the user,
    # tests just reuse them.
    test.user_download_dir = user_conf.get('qemu.download.dir')
    # Make sure config stores don't leak via
    # byoc.stacks._shared_stores. vm.run_hook has to save all known config
    # stores before running to make sure any hook modification is properly
    # seen.
    fixtures.patch(test, stacks, '_shared_stores', {})
    # Stop here if there is no user provided test configs
    features.test_requires(test, features.tests_config)
    # Share the lxd certificate. We could generate one on the fly but assume
    # instead that one is already available since we require the lxc client
    # already.
    lxd_conf_dir = os.path.expanduser('~/.config/lxc')
    # the following calls isolate_from_env and create unique dirs
    isolate_from_disk(test)
    fixtures.override_env(test, 'LXD_CONF', lxd_conf_dir)

    # By default, qemu tests start with a private images dir
    test.images_dir = os.path.join(test.uniq_dir, 'images')

    # Make user provided test config files visible to tests by installing them
    # under self.uniq_dir/etc/byov/conf.d
    def install(src, dst):
        with open(src) as s, open(dst, 'w') as d:
            d.write(s.read())
    install(features.tests_config.user_path,
            os.path.join(test.etc_dir, config.config_file_basename()))
    if features.tests_config.more_paths:
        confd_dir = os.path.join(test.etc_dir, 'conf.d')
        os.mkdir(confd_dir)
        for p in features.tests_config.more_paths:
            _, bname = os.path.split(p)
            # Drop the -tests suffix from the basename
            # FIXME: This trick should probably be refactored by installing
            # (where ?) a hook to read directly from those files and stop
            # creating copies and squatting the file namespace
            # -- vila 2022-04-04
            install(p, os.path.join(confd_dir, bname[:-len('-tests')]))
    # Create a config file for tests (all set() go to the section chosen at
    # Stack creation time)
    # FIXME: Ideally we'd want self.vm_name rather than None. Refactor tests to
    # allow that -- vila 2022-02-16
    conf = config.VmStack(None)
    # Some tests assumes -oLogLevel=ERROR is part of ssh.options to avoid the
    # 'Warning: Permanently added xxx to the list of known hosts.'
    test.assertTrue('-oLogLevel=ERROR' in conf.get('ssh.options'))
    # If there is no ssh key or it's pub counterpart is not in authorized_keys,
    # we won't be able to connect to vms
    key_path = conf.get('ssh.key')
    test.assertTrue(os.path.exists(key_path),
                    '{} does not exist'.format(key_path))
    authorized_keys = conf.get('ssh.authorized_keys')
    test.assertTrue(key_path + '.pub' in authorized_keys)
    # Some tests assumes byov-tests-<class>-debian exists (in the user env)
    # and that its digest matches the vm . The safest way to isolate this
    # properly is to just re-calculate the digest (in the test env).
    for kls_name, kls in (('lxd', lxd.Lxd),):
        vm_name = 'byov-tests-{}-debian'.format(kls_name)
        vm = kls(config.VmStack(vm_name))
        vm.econf.set('vm.name', vm_name)
        vm.econf.set('vm.class', kls_name)
        vm.econf.set('vm.setup.digest', vm.hash_setup())
        vm.econf.store.save_changes()
        vm.econf.store.unload()

    # ec2 test resources get some specific tags
    conf.set('ec2.instance.tags', 'test.id ' + test.id())
    conf.set('ec2.image.tags', 'test.id ' + test.id())
    conf.store.save_changes()
    conf.store.unload()

    # setup byov.path to include the files created above
    byov.path.insert(0, test.uniq_dir)
    fixtures.override_env(test, 'BYOV_PATH', ':'.join(byov.path))
    config.import_user_byovs()


class _MyStreamHandler(logging.StreamHandler):
    """Work around an issue in python2 urllib3 library not using unicode.

    Can be deleted once we migrate to python3 novaclient.
    """

    def emit(self, record):
        msg = record.msg
        if sys.version_info < (3,) and isinstance(msg, str):
            record.msg = msg.decode('utf8')
        super(_MyStreamHandler, self).emit(record)


def override_logging(test, debug=None):
    """Setup a logging handler, restoring the actual handlers after the test.

    This assumes a logging setup where handlers are added to the root logger
    only.

    :param debug: When set to True, log output with level debug is sent to
        stdout.
    """
    # FIXME: Should we ask for '{logging.level}' instead ? -- vila 2022-01-07
    env_debug = bool(os.environ.get('DEBUG', False))
    if debug is None and env_debug:
        debug = env_debug
    if debug:
        stream = sys.stdout
        level = logging.DEBUG
        if with_boto3:
            # Silence boto a bit. without the following, roughly every http
            # request and response is traced. Because types and AMIs can't be
            # queried finely enough, it's mostly noise.
            for mod_name in ('boto3', 'botocore', 'urllib3.connectionpool'):
                logging.getLogger(mod_name).setLevel(logging.ERROR)
    else:
        stream = io.StringIO()
        level = logging.INFO
    root_logger = logging.getLogger(None)
    # Using reversed() below ensures we can modify root_logger.handlers as well
    # as providing the handlers in the right order for cleanups.
    for handler in reversed(root_logger.handlers):
        root_logger.removeHandler(handler)
        test.addCleanup(root_logger.addHandler, handler)
    # Install the new handler
    test.log_stream = stream
    new_handler = _MyStreamHandler(stream)
    test.addCleanup(root_logger.removeHandler, new_handler)
    root_logger.addHandler(new_handler)
    # Install the new level, restoring the actual one after the test
    test.addCleanup(root_logger.setLevel, root_logger.level)
    root_logger.setLevel(level)


def per_backend_release_arch_setup(test):
    """Prepare setting up vm for parametrization by backend, release and arch.

    This is used by the per_vm tests.
    """
    # Some classes require additional features
    required_features = {
        'docker': [features.docker_client_feature],
        'ec2': [features.ec2_creds, features.ec2_boto3],
        'lxd': [features.lxd_client_feature],
        'nova': [features.nova_creds],
        'qemu': [features.qemu_img_feature],
        'scaleway': [features.scaleway_creds],
    }
    if test.kls in required_features:
        feats = required_features[test.kls]
        for f in feats:
            if not f.available():
                test.skipTest('{} is not available'.format(f.feature_name()))
    # Create a shared config
    conf = config.VmStack(test.vm_name)
    conf.set('vm.name', test.vm_name)
    conf.set('vm.class', test.kls)
    conf.set('vm.distribution', test.dist)
    conf.set('vm.release', test.series)
    conf.set('vm.architecture', test.arch)
    # Some classes require additional and specific setup

    def docker_setup(test, conf):
        conf.set('vm.published_as', '{vm.name}-public')
        image = conf.get('docker.image')
        with io.open('./Dockerfile', 'w', encoding='utf8') as f:
            f.write('''\
FROM {}
# FIXME: This is a mistake, building the image should not require running the
# container as ENTRYPOINT can interfere with it. -- vila 2022-03-01
# Force the container to stay up once started
ENTRYPOINT ["tail", "-f", "/dev/null"]
'''.format(image))

    def ec2_setup(test, conf):
        # Set to the empty string to use 'ec2.distribution.images'
        conf.set('ec2.image', '')
        conf.set('vm.published_as', '{vm.name}-public')
        if test.dist == "amazon":
            # at least on al2, dnf is not installed
            conf.set('dnf.command', 'sudo, yum, {dnf.options}')
            conf.set('dnf.options', '-y, -t')

    def lxd_setup(test, conf):
        conf.set('vm.published_as', '{vm.name}-public')

    def qemu_setup(test, conf):
        features.requires_existing_bridge(test, conf.get('qemu.bridge'))
        conf.set('qemu.networks',
                 '-net bridge,br={qemu.bridge}'
                 ' -net nic,macaddr={qemu.mac.address}')
        # Unless the test overrides it, qemu vms reuse downloads provided by
        # the user but use a private image dir.
        conf.set('qemu.download.dir', test.user_download_dir)
        conf.set('qemu.images.dir', test.images_dir)
        conf.set('vm.published_as', '{qemu.image}-public')
        # FIXME: qemu.image.setup and qemu.image.teardown ?
        # -- vila 2019-12-07

    def nova_setup(test, conf):
        image_id = nova.byov_image_name('cloudimg', test.series, test.arch)
        conf.set('nova.image', image_id)

    def scaleway_setup(test, conf):
        conf.set('scaleway.flavor', 'START1-XS')
        conf.set('scaleway.image',
                 '{vm.distribution}/{vm.release}/{vm.architecture}-xs')
        # conf.set('scaleway.flavor', 'C1')
        # conf.set('vm.architecture', 'armhf')
        features.test_requires(test, features.ScalewayImage(conf))

    specific_setups = {
        'docker': docker_setup,
        'ec2': ec2_setup,
        'lxd': lxd_setup,
        'nova': nova_setup,
        'qemu': qemu_setup,
        'scaleway': scaleway_setup,
    }
    if test.kls in specific_setups:
        setup = specific_setups[test.kls]
        setup(test, conf)
    # save all config changes
    conf.store.save()
    conf.store.unload()
