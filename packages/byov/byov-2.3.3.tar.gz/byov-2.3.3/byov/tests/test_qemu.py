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

import os
import unittest


from byov import (
    config,
    errors,
)
from byov.tests import (
    features,
    fixtures,
)
from byov.vms import qemu


# FIXME: Not used ? -- vila 2019-11-15
def requires_known_reference_image(test):
    """Skip test if a known reference image is not provided locally.

    :note: This should be called early during setUp so the user configuration
        is still available (i.e. the test has not yet been isolated from disk).

    :param test: The TestCase requiring the image.
    """
    # We need a pre-seeded download cache from the user running the tests
    # as downloading the cloud image is too long.
    user_conf = config.VmStack(None)
    download_cache = user_conf.get('qemu.download.dir')
    # FIXME: Testing directory existence will offer an opt-in path for limiting
    # tests -- vila 2019-11-12
    if download_cache is None:
        test.skipTest('qemu.download.dir is not set')
    # We use some known reference
    # FIXME: This is not used by callers, something is wrong -- vila 2019-11-14
    reference_cloud_image_name = 'ubuntu/bionic-amd64'
    cloud_image_path = os.path.join(
        download_cache, reference_cloud_image_name)
    if not os.path.exists(cloud_image_path):
        test.skipTest('{} is not available'.format(cloud_image_path,))
    # /!\ Tests should be careful when using this images_dir shared
    # resource. No existing image should be deleted.
    # I.e. use unique names, cleanup.
    # FIXME: It's probably better to create hard links to existing images ?
    # -- vila 2019-09-11
    images_dir = user_conf.get('qemu.images.dir')
    return download_cache, reference_cloud_image_name, images_dir


@features.requires(features.wget_feature)
class TestDownloadImage(unittest.TestCase):

    def setUp(self):
        # Downloading real isos or images is too long for tests, instead, we
        # fake it by downloading a small but known to exist file: MD5SUMS
        super(TestDownloadImage, self).setUp()
        fixtures.isolate_from_disk(self)
        download_dir = os.path.join(self.uniq_dir, 'downloads')
        os.mkdir(download_dir)
        fixtures.override_logging(self)
        # 'focal' should stay valid for a while...
        # FIXME: 'focal' should be replaced by some option defining the current
        # LTS -- vila-2019-11-08
        # FIXME: Especially given that the "current" LTS is bionic in almost
        # all other tests -- vila 2019-11-16
        self.download_url = (
            'https://cloud-images.ubuntu.com/focal/current/MD5SUMS')
        self.conf = config.VmStack('foo')
        self.conf.store._load_from_string('''
vm.name = foo
vm.release = focal
vm.architecture = amd64
qemu.download.dir = {download_dir}
qemu.download.url = {download_url}
'''.format(download_dir=download_dir, download_url=self.download_url))
        self.conf.set('qemu.image.setup', 'download')
        self.conf.set('qemu.image.teardown', 'download')
        self.conf.set('qemu.image', '{qemu.download.path}')

    def test_download(self):
        vm = qemu.Qemu(self.conf)
        vm.setup_image()
        self.assertTrue(os.path.exists(vm.disk_image_path()))
        # Trying to download again will find the file in the cache
        self.assertFalse('Already at' in self.log_stream.getvalue())
        vm.setup_image()
        self.assertTrue('Already at' in self.log_stream.getvalue())

    def test_download_creates_cache(self):
        download_dir = os.path.join(self.uniq_dir, 'I-dont-exist')
        self.conf.set('qemu.download.dir', download_dir)
        vm = qemu.Qemu(self.conf)
        self.assertFalse(os.path.exists(os.path.dirname(vm.disk_image_path())))
        vm.setup_image()
        self.assertTrue(os.path.exists(vm.disk_image_path()))

    def test_download_unknown_fails(self):
        # Sabotage the valid url
        url = self.conf.get('qemu.download.url')
        self.conf.set('qemu.download.url', url + 'I-dont-exist')
        vm = qemu.Qemu(self.conf)
        self.assertRaises(errors.CommandError, vm.setup_image)


@features.requires(features.qemu_img_feature)
class TestConvertImage(unittest.TestCase):

    def setUp(self):
        super(TestConvertImage, self).setUp()
        fixtures.setup_tests_config(self)
        convert_dir = os.path.join(self.uniq_dir, 'convert')
        self.conf = config.VmStack('foo')
        self.vm = qemu.Qemu(self.conf)
        self.conf.set('vm.name', 'foo')
        self.conf.set('vm.release', 'bionic')
        self.conf.set('vm.architecture', 'amd64')
        self.conf.set('vm.disk_size', '2.5G')  # Limit the size for tests
        self.conf.set('qemu.download.dir', self.user_download_dir)
        self.conf.set('qemu.images.dir', convert_dir)
        self.conf.set('qemu.image.setup', 'convert,resize')
        self.conf.set('qemu.image.teardown', 'convert')

    def test_convert_image(self):
        self.assertFalse(os.path.exists(self.vm.disk_image_path()))
        self.vm.setup_image()
        self.assertTrue(os.path.exists(self.vm.disk_image_path()))

    def test_convert_no_source(self):
        self.conf.set('qemu.download.path', 'I-dont-exist')
        with self.assertRaises(errors.CommandError) as cm:
            self.vm.setup_image()
        self.assertEqual(1, cm.exception.retcode)
        self.assertTrue('I-dont-exist' in cm.exception.err)

    def test_convert_too_small(self):
        # This is a lower bound to the reference image which is unlikely to
        # shrink below that.
        self.conf.set('vm.disk_size', '1G')
        self.assertFalse(os.path.exists(self.vm.disk_image_path()))
        with self.assertRaises(errors.CommandError) as cm:
            self.vm.setup_image()
        self.assertEqual(1, cm.exception.retcode)
        self.assertTrue('does not support resize' in cm.exception.err)
        # The resize failed but the image exists (if only to help set the
        # proper size)
        self.assertTrue(os.path.exists(self.vm.disk_image_path()))


@features.requires(features.qemu_img_feature)
class TestClone(unittest.TestCase):

    def setUp(self):
        super(TestClone, self).setUp()
        fixtures.setup_tests_config(self)
        clone_dir = os.path.join(self.uniq_dir, 'clone')
        # Create a shared config
        conf = config.VmStack(None)
        conf.store._load_from_string('''
vm.release=bionic
vm.architecture = amd64
vm.disk_size = 2.5G # Limit the size for tests
qemu.download.dir = {download_dir}
qemu.images.dir = {images_dir}
[base]
vm.name=base
[foo]
vm.name=foo
vm.backing=base
'''.format(download_dir=self.user_download_dir, images_dir=clone_dir))
        conf.store.save()
        conf.store.unload()
        # Points to the reference image
        bconf = config.VmStack('base')
        bconf.set('vm.published_as', '{qemu.download.path}')
        bconf.store.save()
        bconf.store.unload()
        self.conf = config.VmStack('foo')
        self.vm = qemu.Qemu(self.conf)
        self.conf.set('qemu.image.setup', 'clone,resize')
        self.conf.set('qemu.image.teardown', 'clone')

    def test_clone_image(self):
        self.assertFalse(os.path.exists(self.vm.disk_image_path()))
        self.vm.setup_image()
        self.assertTrue(os.path.exists(self.vm.disk_image_path()))

    def test_clone_no_source(self):
        bconf = config.VmStack('base')
        bconf.set('vm.published_as', 'I-dont-exist')
        with self.assertRaises(errors.CommandError) as cm:
            self.vm.setup_image()
        self.assertEqual(1, cm.exception.retcode)
        self.assertTrue('I-dont-exist' in cm.exception.err)

    def test_clone_too_small(self):
        # This is a lower bound to the reference image which is unlikely to
        # shrink below that.
        self.conf.set('vm.disk_size', '1G')
        self.assertFalse(os.path.exists(self.vm.disk_image_path()))
        with self.assertRaises(errors.CommandError) as cm:
            self.vm.setup_image()
        self.assertEqual(1, cm.exception.retcode)
        self.assertTrue('does not support resize' in cm.exception.err)
        # The resize failed but the image exists (if only to help set the
        # proper size)
        self.assertTrue(os.path.exists(self.vm.disk_image_path()))


@features.requires(features.qemu_img_feature)
class TestSeedImage(unittest.TestCase):

    def setUp(self):
        super(TestSeedImage, self).setUp()
        fixtures.setup_tests_config(self)
        images_dir = os.path.join(self.uniq_dir, 'images')
        self.conf = config.VmStack('foo')
        self.vm = qemu.Qemu(self.conf)
        self.conf.set('vm.class', 'qemu')
        self.conf.set('vm.name', 'foo')
        self.conf.set('vm.release', 'bionic')
        self.conf.set('vm.architecture', 'amd64')
        self.conf.set('qemu.images.dir', images_dir)

    def test_create_seed_image(self):
        self.assertTrue(self.vm._seed_path is None)
        self.vm.create_seed_image()
        self.assertFalse(self.vm._seed_path is None)
        self.assertTrue(os.path.exists(self.vm._seed_path))


class TestQemuMonitor(unittest.TestCase):

    def setUp(self):
        super(TestQemuMonitor, self).setUp()
        fixtures.set_uniq_vm_name(self)
        fixtures.setup_tests_config(self)
        # Create a shared config
        conf = config.VmStack(None)
        conf.store._load_from_string('''
[{name}]
vm.name = {name}
vm.class = qemu
qemu.ssh.localhost.port = 10022 # FIXME: Needs a better way -- vila 2019-09-11
vm.release=bionic
vm.architecture = amd64
'''.format(name=self.vm_name))
        conf.store.save()
        conf.store.unload()

    def test_terminate_qemu(self):
        vm = qemu.Qemu(config.VmStack(self.vm_name))
        vm.spawn_qemu()
        self.addCleanup(vm.terminate_qemu)
        self.assertEqual('RUNNING', vm.state())


class TestSetupWithSeed(unittest.TestCase):

    def setUp(self):
        super(TestSetupWithSeed, self).setUp()
        fixtures.set_uniq_vm_name(self, short=True)
        fixtures.setup_tests_config(self)
        fixtures.override_logging(self)
        self.conf = config.VmStack(self.vm_name)
        features.requires_existing_bridge(self, self.conf.get('qemu.bridge'))
        images_dir = os.path.join(self.uniq_dir, 'images')
        self.conf.set('vm.class', 'qemu')
        self.conf.set('vm.update', 'False')  # Shorten install time
        self.conf.set('vm.cpus', '2')
        self.conf.set('vm.release', 'bionic')
        self.conf.set('vm.architecture', 'amd64')
        self.conf.set('vm.disk_size', '2.5G')  # Limit the size for tests
        self.conf.set('qemu.download.dir', self.user_download_dir)
        self.conf.set('qemu.images.dir', images_dir)
        self.conf.set('qemu.image.setup', 'download,convert,resize')
        self.conf.set('qemu.image.teardown', 'convert,resize')
        self.conf.set('vm.name', self.vm_name)
        self.conf.set('qemu.networks',
                      '-net bridge,br={qemu.bridge}'
                      ' -net nic,macaddr={qemu.mac.address}')
        self.conf.store.save()
        self.conf.store.unload()
        self.vm = qemu.Qemu(self.conf)

    def test_setup_with_seed(self):
        self.addCleanup(self.vm.teardown, force=True)
        self.vm.setup()
        self.assertEqual('RUNNING', self.vm.state())

    def test_start_keeps_mac(self):
        self.addCleanup(self.vm.teardown, force=True)
        self.vm.setup()
        self.assertEqual('RUNNING', self.vm.state())
        mac_address = self.vm.econf.get('qemu.mac.address')
        ip_addresss = self.vm.econf.get('vm.ip')
        self.vm.stop()
        self.vm.start()
        self.assertEquals(mac_address, self.vm.econf.get('qemu.mac.address'))
        # The aim is to get a stable ip so it must be the same on all starts
        self.assertEquals(ip_addresss, self.vm.econf.get('vm.ip'))


class TestSetupWithBacking(unittest.TestCase):

    def setUp(self):
        super(TestSetupWithBacking, self).setUp()
        fixtures.set_uniq_vm_name(self, short=True)
        fixtures.setup_tests_config(self)
        fixtures.override_logging(self)
        # Create a shared config
        conf = config.VmStack(None)
        features.requires_existing_bridge(self, conf.get('qemu.bridge'))
        images_dir = os.path.join(self.uniq_dir, 'images')
        conf.set('vm.class', 'qemu')
        conf.set('vm.update', 'False')  # Shorten install time
        conf.set('vm.release', 'bionic')
        conf.set('vm.architecture', 'amd64')
        conf.set('vm.disk_size', '2.5G')  # Limit the size for tests
        conf.set('qemu.download.dir', self.user_download_dir)
        conf.set('qemu.images.dir', images_dir)

        bconf = config.VmStack('base')
        bconf.set('vm.name', 'base')

        vconf = config.VmStack(self.vm_name)
        vconf.set('vm.name', self.vm_name)
        vconf.set('vm.backing', 'base')

        conf.set('qemu.image.setup', 'clone,resize')
        conf.set('qemu.image.teardown', 'clone')
        conf.set('qemu.networks',
                 '-net bridge,br={qemu.bridge}'
                 ' -net nic,macaddr={qemu.mac.address}')
        # Points to the reference image
        bconf.set('vm.published_as', '{qemu.download.path}')

        # conf, bconf and vconf are all in the same store, a single save is
        # enough
        self.assertTrue(conf.store == vconf.store)
        self.assertTrue(conf.store == bconf.store)
        conf.store.save()
        conf.store.unload()

    def test_setup_with_backing(self):
        vm = qemu.Qemu(config.VmStack(self.vm_name))
        self.addCleanup(vm.teardown, force=True)
        vm.setup()
        self.assertEqual('RUNNING', vm.state())

# FIXME: While vm.update=False makes the test faster, it missed the bug where
# Qemu.setup() wasn't waiting for cloud-init to finish leading to a very
# confusing behavior. Specifically, cloud-init add-apt-repository (for a ppa)
# raced with the first apt-get update issued by byov.
# -- vila 2019-12-03
