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
import logging
import os
import unittest

import byov
from byoc import errors
from byot import (
    assertions,
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
from byov.vms import (
    lxd,
    subprocesses,
)

load_tests = scenarii.load_tests_with_scenarios


class TestVmMatcher(unittest.TestCase):

    def setUp(self):
        super(TestVmMatcher, self).setUp()
        fixtures.isolate_from_disk(self)
        self.store = config.VmStore('foo.conf')
        self.matcher = config.VmMatcher(self.store, 'quux')

    def test_empty_section_always_matches(self):
        self.store._load_from_string('foo=bar')
        matching = list(self.matcher.get_sections())
        self.assertEqual(1, len(matching))

    def test_specific_before_generic(self):
        self.store._load_from_string('foo=bar\n[quux]\nfoo=baz')
        matching = list(self.matcher.get_sections())
        self.assertEqual(2, len(matching))
        # First matching section is for quux
        self.assertEqual(self.store, matching[0][0])
        base_section = matching[0][1]
        self.assertEqual('quux', base_section.id)
        # Second matching section is the no-name one
        self.assertEqual(self.store, matching[0][0])
        no_name_section = matching[1][1]
        self.assertIs(None, no_name_section.id)


class TestVmStackOrdering(unittest.TestCase):

    def setUp(self):
        super(TestVmStackOrdering, self).setUp()
        fixtures.isolate_from_disk(self)
        self.conf = config.VmStack('foo')

    def assertValue(self, value, name):
        conf = config.VmStack('foo')
        self.assertEqual(value, conf.get(name))

    def test_default_in_empty_stack(self):
        self.assertValue('2048', 'vm.ram_size')

    def test_system_overrides_internal(self):
        with open(os.path.join(self.etc_dir,
                               config.config_file_basename()), 'w') as f:
            f.write('vm.ram_size = 42')
        self.assertValue('42', 'vm.ram_size')

    def test_user_overrides_system(self):
        with open(os.path.join(self.etc_dir,
                               config.config_file_basename()), 'w') as f:
            f.write('vm.ram_size = 42')
        os.makedirs(config.user_config_dir())
        with open(os.path.join(config.user_config_dir(),
                               config.config_file_basename()), 'w') as f:
            f.write('vm.ram_size = 84')
        self.assertValue('84', 'vm.ram_size')

    def test_local_overrides_user(self):
        fixtures.patch(self, byov, 'path', byov.path + [self.uniq_dir])
        os.makedirs(config.user_config_dir())
        with open(os.path.join(config.user_config_dir(),
                               config.config_file_basename()), 'w') as f:
            f.write('vm.ram_size = 84')
        with open('byov.conf', 'w') as f:
            f.write('vm.ram_size = 168')
        self.assertValue('168', 'vm.ram_size')

    def test_local_overrides_local_dir(self):
        fixtures.patch(self, byov, 'path', byov.path + [self.uniq_dir])
        os.makedirs('byov.conf.d')
        with open(os.path.join('byov.conf.d',
                               'foo.conf'), 'w') as f:
            f.write('vm.ram_size = 136')
        with open('byov.conf', 'w') as f:
            f.write('vm.ram_size = 168')
        self.assertValue('168', 'vm.ram_size')
        self.assertValue('168', 'vm.ram_size')

    def test_user_overrides_user_dir(self):
        os.makedirs(os.path.join(config.user_config_dir(), 'conf.d'))
        with open(os.path.join(config.user_config_dir(), 'conf.d',
                               'foo.conf'), 'w') as f:
            f.write('vm.ram_size = 136')
        with open(os.path.join(config.user_config_dir(),
                               config.config_file_basename()), 'w') as f:
            f.write('vm.ram_size = 84')
        self.assertValue('84', 'vm.ram_size')

    def test_system_overrides_system_dir(self):
        os.makedirs(os.path.join(config.system_config_dir(), 'conf.d'))
        with open(os.path.join(config.system_config_dir(), 'conf.d',
                               'foo.conf'), 'w') as f:
            f.write('vm.ram_size = 136')
        with open(os.path.join(config.system_config_dir(),
                               config.config_file_basename()), 'w') as f:
            f.write('vm.ram_size = 84')
        self.assertValue('84', 'vm.ram_size')

    def test_only_dotconf_are_seen(self):
        conf_d = os.path.join(config.user_config_dir(), 'conf.d')
        os.makedirs(conf_d)
        with open(os.path.join(conf_d, 'foo.conf'), 'w') as f:
            f.write('vm.ram_size = 42')
        with open(os.path.join(conf_d, 'foo'), 'w') as f:
            f.write('vm.ram_size = 84')
        self.assertValue('42', 'vm.ram_size')

    def test_dotconf_are_sorted(self):
        conf_d = os.path.join(config.user_config_dir(), 'conf.d')
        os.makedirs(conf_d)
        with open(os.path.join(conf_d, '1.conf'), 'w') as f:
            f.write('vm.ram_size = 1')
        with open(os.path.join(conf_d, '2.conf'), 'w') as f:
            f.write('vm.ram_size = 2')
        self.assertValue('1', 'vm.ram_size')


class TestVmStack(unittest.TestCase):
    """Test config option values."""

    def setUp(self):
        super(TestVmStack, self).setUp()
        fixtures.isolate_from_disk(self)
        self.conf = config.VmStack('foo')
        self.conf.store._load_from_string('''
vm.release=focal
vm.architecture=amd64
''')

    def assertValue(self, expected_value, option):
        self.assertEqual(expected_value, self.conf.get(option))

    def test_cloud_image_url(self):
        self.assertValue('http://cloud-images.ubuntu.com/focal/current/'
                         'focal-server-cloudimg-amd64.img',
                         'qemu.download.url')

    def test_apt_proxy_set(self):
        proxy = 'apt_proxy: http://example.org:4321'
        self.conf.set('apt.proxy', proxy)
        self.conf.store.save_changes()
        self.assertEqual(proxy, self.conf.expand_options('{apt.proxy}'))

    def test_vms_dir_with_user_expansion(self):
        vms_dir = '~/vms'
        self.conf.set('vm.vms_dir', vms_dir)
        self.conf.store.save_changes()
        self.assertValue(os.path.join(self.home_dir, 'vms'), 'vm.vms_dir')

    def test_vm_config_dir_with_user_expansion(self):
        config_dir = '~/config'
        self.conf.set('vm.config_dir', config_dir)
        self.conf.store.save_changes()
        self.assertValue(os.path.join(self.home_dir, 'config'),
                         'vm.config_dir')

    def test_lxd_invalid_nesting(self):
        self.conf.set('lxd.nesting', 'true')
        with self.assertRaises(errors.OptionValueError) as cm:
            self.conf.get('lxd.nesting')
        self.assertEqual('lxd.nesting: Value "true" is not valid:'
                         ' invalid literal for int() with base 10:'
                         " 'true'.",
                         str(cm.exception))


class TestPathOptionIsolated(unittest.TestCase):

    def setUp(self):
        super(TestPathOptionIsolated, self).setUp()
        fixtures.isolate_from_disk(self)

    def assertConverted(self, expected, value):
        option = options.PathOption('foo', help_string='A path.')
        self.assertEqual(expected, option.convert_from_unicode(None, value))

    def test_absolute_path(self):
        self.assertConverted('/test/path', '/test/path')

    def test_home_path_with_expansion(self):
        self.assertConverted(self.home_dir, '~')

    def test_path_in_home_with_expansion(self):
        self.assertConverted(os.path.join(self.home_dir, 'test/path'),
                             '~/test/path')


class TestLxdUserMountsOption(unittest.TestCase):

    def setUp(self):
        super(TestLxdUserMountsOption, self).setUp()
        fixtures.isolate_from_disk(self)

    def assertConverted(self, expected, value):
        option = options.LxdUserMountsOption('foo', help_string='A path.')
        self.assertEqual(expected, option.convert_from_unicode(None, value))

    def test_empty(self):
        self.assertConverted([], '')

    def test_odd(self):
        with self.assertRaises(errors.OptionValueError) as cm:
            self.assertConverted(None, 'tagada')
        self.assertEqual('foo', cm.exception.name)

    def test_vm_path_not_absolute(self):
        with self.assertRaises(errors.OptionValueError) as cm:
            self.assertConverted(None, 'here, there')
        self.assertEqual('foo', cm.exception.name)

    def test_absolute_paths(self):
        self.assertConverted([('/host/foo', '/vm/bar')], '/host/foo:/vm/bar')

    def test_tilde_paths(self):
        self.assertConverted([('{}/foo'.format(self.home_dir), '/bar')],
                             '~/foo:/bar')

    def test_relative_paths(self):
        self.assertConverted([('{}/foo'.format(self.uniq_dir), '/bar'),
                              (self.uniq_dir, '/quux')],
                             'foo:/bar, .:/quux')


class TestLoggingLevelOption(unittest.TestCase):

    def test_lower(self):
        self.assertEqual(logging.CRITICAL,
                         options.level_from_store('critical'))
        self.assertEqual(logging.ERROR, options.level_from_store('error'))
        self.assertEqual(logging.DEBUG, options.level_from_store('debug'))
        self.assertEqual(logging.NOTSET, options.level_from_store('notset'))

    def test_upper(self):
        self.assertEqual(logging.CRITICAL,
                         options.level_from_store('CRITICAL'))
        self.assertEqual(logging.ERROR, options.level_from_store('ERROR'))
        self.assertEqual(logging.DEBUG, options.level_from_store('DEBUG'))
        self.assertEqual(logging.NOTSET, options.level_from_store('NOTSET'))


@features.requires(features.bzr_feature)
class TestLaunchpadOptions(unittest.TestCase):

    def setUp(self):
        fixtures.isolate_from_disk(self)
        fixtures.override_env(self, 'BZR_HOME', self.uniq_dir)

    def test_defaults_to_logname(self):
        fixtures.override_env(self, 'LOGNAME', 'foo')
        self.assertEqual('foo', options.default_lp_login())

    # FIXME: testing bzr lp-login requires either a launchpad test server or a
    # real user with a registered ssh key, punting for now after manual tests
    # -- vila 2016-08-30
    def xtest_lp_login_set(self):
        subprocesses.run(['bzr', 'lp-login', 'foo'])
        self.assertEqual('foo', options.default_lp_login())


class TestPackageListOption(unittest.TestCase):

    def setUp(self):
        super(TestPackageListOption, self).setUp()
        fixtures.isolate_from_disk(self)

    def assertConverted(self, expected, value):
        option = options.PackageListOption('foo',
                                           help_string='A package list.')
        self.assertEqual(expected, option.convert_from_unicode(None, value))

    def test_empty(self):
        self.assertConverted(None, None)

    def test_regular_packages(self):
        self.assertConverted(['a', 'b'], 'a,b')

    def test_existing_file(self):
        with open('packages', 'w') as f:
            f.write('a\nb\n')
        self.assertConverted(['a', 'b'], '@packages')

    def test_comments(self):
        with open('packages', 'w') as f:
            f.write('#a\nb # EOL\nc\n')
        self.assertConverted(['b', 'c'], '@packages')

    def test_non_existing_file(self):
        with self.assertRaises(errors.OptionValueError) as cm:
            self.assertConverted(None, '@I-dont-exist')
        self.assertEqual('foo', cm.exception.name)


class TestVmUserOptions(unittest.TestCase):

    def setUp(self):
        super(TestVmUserOptions, self).setUp()
        fixtures.isolate_from_disk(self)

    def test_defaults(self):
        conf = config.VmStack('whatever')
        self.assertEqual('ubuntu', conf.get('vm.user'))
        self.assertEqual('/home/ubuntu', conf.get('vm.user.home'))
        self.assertEqual('/bin/bash', conf.get('vm.user.shell'))


class TestVmClass(unittest.TestCase):

    def setUp(self):
        super(TestVmClass, self).setUp()
        fixtures.isolate_from_disk(self)

    def test_class_mandatory(self):
        conf = config.VmStack('I-dont-exist')
        with self.assertRaises(errors.OptionMandatoryValueError):
            conf.get('vm.class')

    def test_bogus(self):
        conf = config.VmStack('I-dont-exist')
        conf.store._load_from_string('''vm.class=bogus''')
        with self.assertRaises(errors.OptionMandatoryValueError):
            conf.get('vm.class')


class TestAllVmClasses(unittest.TestCase):

    scenarios = [(k, dict(kls=k)) for k in options.vm_class_registry.keys()]

    def setUp(self):
        super(TestAllVmClasses, self).setUp()
        fixtures.isolate_from_disk(self)

    def test_backend(self):
        conf = config.VmStack('I-dont-exist')
        conf.store._load_from_string('vm.class={}'.format(self.kls))
        self.assertIs(options.vm_class_registry.get(self.kls),
                      conf.get('vm.class'))


class TestStartingNameMatcher(unittest.TestCase):

    def setUp(self):
        super(TestStartingNameMatcher, self).setUp()
        fixtures.isolate_from_disk(self)
        # Any simple store is good enough
        self.store = config.VmStore('foo.conf')

    def assertSectionIDs(self, expected, name, content):
        self.store._load_from_string(content)
        matcher = config.StartingNameMatcher(self.store, name)
        sections = list(matcher.get_sections())
        assertions.assertLength(self, len(expected), sections)
        self.assertEqual(expected, [section.id for _, section in sections])
        return sections

    def test_none_with_sections(self):
        self.assertSectionIDs([], None, '''\
[foo]
[bar]
''')

    def test_empty(self):
        self.assertSectionIDs([], 'whatever', '')

    def test_matching_paths(self):
        self.assertSectionIDs(['foo-bar', 'foo'],
                              'foo-bar-baz', '''\
[foo]
[foo-bar]
''')

    def test_no_name_section_included_when_present(self):
        # Note that other tests will cover the case where the no-name section
        # is empty and as such, not included.
        self.assertSectionIDs(['foo-bar', 'foo', None],
                              'foo-bar-baz', '''\
option = defined so the no-name section exists
[foo]
[foo-bar]
''')

    def test_order_reversed(self):
        self.assertSectionIDs(['foo-bar', 'foo'], 'foo-bar-baz', '''\
[foo]
[foo-bar]
''')

    def test_unrelated_section_excluded(self):
        self.assertSectionIDs(['foo-bar', 'foo'], 'foo-bar-baz', '''\
[foo]
[foo-qux]
[foo-bar]
''')


class TestVmHostOrdering(unittest.TestCase):

    def setUp(self):
        super(TestVmHostOrdering, self).setUp()
        fixtures.isolate_from_disk(self)

    def assertSectionIDs(self, expected, conf):
        actual = [section.id for (store, section) in conf.iter_sections()]
        self.assertEqual(expected, actual)

    def test_respect_host_order_in_single_file(self):
        fixtures.patch(self, byov, 'path', byov.path + [self.uniq_dir])
        with open('byov.conf', 'w') as f:
            f.write('''\
[foo-bar-baz]
[foo-qux]
[foo-b]
[foo]
''')
        conf = config.VmStack('foo-bar-baz')
        self.assertSectionIDs([None, 'foo-bar-baz', 'foo-b', 'foo'], conf)

    def test_respect_host_order_across_files(self):
        fixtures.patch(self, byov, 'path', byov.path + [self.uniq_dir])
        with open('byov.conf', 'w') as f:
            f.write('''\
[foo]
''')
        os.mkdir('byov.conf.d')
        with open('byov.conf.d/foo.conf', 'w') as f:
            f.write('''\
[foo-b]
''')
        conf = config.VmStack('foo-bar-baz')
        self.assertSectionIDs([None, 'foo-b', 'foo'], conf)


class TestVmName(unittest.TestCase):

    def setUp(self):
        super(TestVmName, self).setUp()
        fixtures.isolate_from_disk(self)

    def save_config(self, content):
        os.makedirs(config.user_config_dir())
        user_config_path = os.path.join(config.user_config_dir(),
                                        config.config_file_basename())
        with open(user_config_path, 'w')as f:
            f.write(content)

    def test_name_starts_with_section_name(self):
        self.save_config('''\
[foo]
vm.class = lxd
''')
        conf = config.VmStack('foo1')
        conf.cmdline_store.from_cmdline(['vm.name=foo1'])
        self.assertEqual('foo1', conf.get('vm.name'))
        self.assertIs(lxd.Lxd, conf.get('vm.class'))


class TestExistingVmStack(unittest.TestCase):

    def setUp(self):
        super().setUp()
        fixtures.isolate_from_disk(self)

    def test_empty(self):
        conf = config.ExistingVmStack('foo')
        self.assertEqual([], list(conf.iter_sections()))

    def test_existing_vm(self):
        econf = config.ExistingVmStack('foo')
        econf.set('vm.name', 'foo')
        econf.set('vm.class', 'lxd')  # We need a valid class
        econf.set('vm.ip', 'localhost')
        econf.store.save_changes()
        conf = config.VmStack('foo')
        self.assertEqual('foo', conf.get('vm.name'))
        self.assertEqual(lxd.Lxd, conf.get('vm.class'))
        self.assertEqual('localhost', conf.get('vm.ip'))

    def test_sibling_vms_dont_leak(self):
        foo_econf = config.ExistingVmStack('foo')
        foo_econf.set('vm.name', 'foo')
        foo_econf.set('vm.class', 'lxd')  # We need a valid class
        foo_econf.set('blah', 'blah')
        foo_econf.store.save_changes()
        foo2_econf = config.ExistingVmStack('foo-2')
        foo2_econf.set('vm.name', 'foo-2')
        foo2_econf.set('vm.class', 'lxd')
        foo2_econf.store.save_changes()

        conf = config.VmStack('foo-2')
        self.assertEqual('foo-2', conf.get('vm.name'))
        self.assertEqual(lxd.Lxd, conf.get('vm.class'))
        self.assertIsNone(conf.get('blah'))


class TestUserByov(unittest.TestCase):

    # The byov imported file change the value
    changed_by = None

    def setUp(self):
        super().setUp()
        fixtures.setup_tests_config(self)

    def create_import(self, directory, value):
        """Create a byov.py file in `directory` setting changed to True."""
        os.makedirs(directory, exist_ok=True)
        with open(os.path.join(directory, 'byov.py'), 'w') as f:
            f.write('import {}\n'. format(self.__class__.__module__))
            f.write('{}.{}.changed = "{}"\n'.format(
                self.__class__.__module__, self.__class__.__name__, value))

    def test_local(self):
        d = 'byov.conf.d'
        self.create_import(d, 'local')
        config.import_user_byov_from(d)
        self.assertEqual('local', self.changed)

    def test_user(self):
        d = os.path.join(config.user_config_dir(), 'conf.d')
        self.create_import(d, 'user')
        config.import_user_byov_from(d)
        self.assertEqual('user', self.changed)

    def test_system(self):
        d = os.path.join(config.system_config_dir(), 'conf.d')
        self.create_import(d, 'system')
        config.import_user_byov_from(d)
        self.assertEqual('system', self.changed)


@features.requires(features.py3_feature)
class TestLocked(unittest.TestCase):

    def setUp(self):
        super().setUp()
        fixtures.isolate_from_disk(self)

    def test_cant_lock_twice(self):
        with config.Locked('test') as outer:
            with self.assertRaises(config.LockedTimeout):
                with config.Locked('test', 1):
                    self.assertFalse("Wrongly got the lock")
        self.assertFalse(outer.locked, "Locked outside context")
        self.assertTrue(outer.available())

    def test_can_lock_sequentially(self):
        with config.Locked('test') as first:
            self.assertTrue(first.locked, "Unlocked inside with :-/")

        with config.Locked('test') as second:
            self.assertTrue(second.locked, "Unlocked inside with :-/")

        self.assertTrue(first.available())
        self.assertTrue(second.available())

    def test_cant_lock_from_another_process(self):
        with open('script', 'w') as f:
                f.write('''\
#! /usr/bin/env python3
import os
import sys

from byov import config

path = os.path.join(os.getcwd(), 'test')

with config.Locked(path, 1):
    # We got the lock that's wrong exit with a specific code
    sys.exit(2)

# This is dead code, use another specific code just in case
sys.ext(3)
''')
        os.chmod('script', 0o755)
        with config.Locked('test'):
            ret, out, err = subprocesses.run(['./script'],
                                             raise_on_error=False)
        # script failed raising a timeout exception
        self.assertEqual(1, ret, 'ret is {}'.format(ret))
        self.assertEqual('', out)
        self.assertTrue(err.startswith('Traceback'), err)
        self.assertTrue('Timeout occurred.' in err, err)


class TestLockedStack(unittest.TestCase):

    def setUp(self):
        super().setUp()
        fixtures.isolate_from_disk(self)
        self.conf = config.VmStack('localhost')

    def test_get_free_port(self):
        self.conf.set('host.free.ports', '32768, 32769')
        self.conf.store.save_changes()
        with self.conf.lock() as locked:
            self.assertFalse(locked.available())
            free_ports = self.conf.get('host.free.ports')
            taken = free_ports[0]
            self.conf.set('host.free.ports', ','.join(free_ports[1:]))
        self.assertEqual(taken, '32768')
        self.assertEqual(['32769'], self.conf.get('host.free.ports'))
