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
import io
import sys
import yaml

import unittest

from byoc import errors as conf_errors

from byov import (
    config,
    errors,
    user_data,
)
from byov.tests import fixtures


class TestYaml(unittest.TestCase):

    def yaml_load(self, *args, **kwargs):
        return yaml.safe_load(*args, **kwargs)

    def yaml_dump(self, *args, **kwargs):
        return yaml.safe_dump(*args, **kwargs)

    def test_load_scalar(self):
        self.assertEqual(
            {'foo': 'bar'}, self.yaml_load(io.StringIO('{foo: bar}')))
        # Surprisingly the enclosing braces are not needed, probably a special
        # case for the highest level
        self.assertEqual({'foo': 'bar'}, self.yaml_load(
            io.StringIO('foo: bar')))

    def test_dump_scalar(self):
        if yaml.__version__ >= '5.1':
            expected = 'foo: bar\n'
        else:
            expected = '{foo: bar}\n'
        self.assertEqual(expected, self.yaml_dump(dict(foo='bar')))

    def test_load_list(self):
        self.assertEqual({'foo': ['a', 'b', 'c']},
                         # Single space indentation is enough
                         self.yaml_load(io.StringIO('''\
foo:
 - a
 - b
 - c
''')))

    def test_dump_list(self):
        # No more enclosing braces... yeah for consistency :-/
        if yaml.__version__ >= '5.1':
            expected = 'foo:\n- a\n- b\n- c\n'
        else:
            expected = 'foo: [a, b, c]\n'
        self.assertEqual(
            expected, self.yaml_dump(dict(foo=['a', 'b', 'c'])))

    def test_load_dict(self):
        self.assertEqual({'foo': {'bar': 'baz'}},
                         self.yaml_load(io.StringIO('{foo: {bar: baz}}')))
        multiple_lines = '''\
foo: {bar: multiple
  lines}
'''
        self.assertEqual(
            {'foo': {'bar': 'multiple lines'}},
            self.yaml_load(io.StringIO(multiple_lines)))


class TestCIUserData(unittest.TestCase):

    maxDiff = None

    def setUp(self):
        super(TestCIUserData, self).setUp()
        fixtures.setup_tests_config(self)
        self.conf = config.VmStack('foo')
        # Set some options to arbitrary but valid values
        self.conf.set('vm.name', 'foo')
        self.conf.set('vm.class', 'lxd')
        self.conf.set('vm.distribution', 'ubuntu')
        self.ci_data = user_data.CIUserData(self.conf)

    def test_empty_config(self):
        self.ci_data.populate()
        # Check default values
        self.assertIs(None, self.ci_data.root_hook)
        self.assertIs(None, self.ci_data.user_hook)
        cc = self.ci_data.cloud_config
        self.assertFalse('apt_update' in cc)
        self.assertFalse('apt_upgrade' in cc)
        self.assertEqual({'expire': True}, cc['chpasswd'])
        self.assertEqual('byov finished installing in ${uptime} seconds.',
                         cc['final_message'])
        self.assertEqual('True', cc['manage_etc_hosts'])
        self.assertFalse('fqdn' in cc)
        self.assertEqual('en_US.UTF-8', cc['locale'])

    def test_etc_manage_hosts_locahost(self):
        self.conf.set('vm.manage_etc_hosts', 'localhost')
        self.ci_data.populate()
        self.assertEqual('localhost',
                         self.ci_data.cloud_config['manage_etc_hosts'])

    def test_fqdn(self):
        fqdn = 'foo.example.com'
        self.conf.set('vm.fqdn', fqdn)
        self.ci_data.populate()
        self.assertEqual(fqdn, self.ci_data.cloud_config['fqdn'])

    def test_vm_user_default(self):
        self.conf.set('ssh.authorized_keys', '')
        self.ci_data.populate()
        self.assertEqual([{'name': 'ubuntu', 'homedir': '/home/ubuntu',
                           'shell': '/bin/bash',
                           'system': False,
                           'sudo': ['ALL=(ALL) NOPASSWD:ALL']}],
                         self.ci_data.cloud_config['users'])

    def test_specified_vm_user(self):
        self.conf.set('vm.user', 'tester')
        self.conf.set('vm.user.home', '/lamaison')
        self.conf.set('vm.user.shell', '/bin/bash')
        with open('test-key', 'w') as f:
            f.write('unused')
        self.conf.set('ssh.authorized_keys', 'test-key')
        self.conf.set('vm.user.sudo', 'ALL=(ALL) NOPASSWD:/bin/true')
        self.ci_data.populate()
        self.assertEqual([{'name': 'tester',
                           'shell': '/bin/bash',
                           'system': False,
                           'homedir': '/lamaison',
                           'ssh-authorized-keys': ['unused'],
                           'sudo': ['ALL=(ALL) NOPASSWD:/bin/true']}],
                         self.ci_data.cloud_config['users'])

    def test_vm_chpasswd_default(self):
        self.ci_data.populate()
        self.assertEqual({'expire': True},
                         self.ci_data.cloud_config['chpasswd'])

    def test_vm_chpasswd(self):
        self.conf.set('vm.chpasswd', 'root:s3cr3t, ubuntu:tagada')
        self.ci_data.populate()
        self.assertEqual(
            {'expire': False, 'list': ['root:s3cr3t', 'ubuntu:tagada']},
            self.ci_data.cloud_config['chpasswd'])

    def test_apt_proxy(self):
        self.conf.set('apt.proxy', 'tagada')
        self.ci_data.populate()
        self.assertEqual('tagada', self.ci_data.cloud_config['apt_proxy'])

    def test_locale(self):
        self.conf.set('vm.locale', 'C.UTF-8')
        self.ci_data.populate()
        self.assertEqual('C.UTF-8', self.ci_data.cloud_config['locale'])

    def test_final_message_precise(self):
        self.conf.set('vm.release', 'precise')
        self.ci_data.populate()
        self.assertEqual('byov finished installing in $UPTIME seconds.',
                         self.ci_data.cloud_config['final_message'])

    def test_final_message_explicit(self):
        self.conf.set('vm.final_message', 'hello there')
        self.ci_data.populate()
        self.assertEqual('hello there',
                         self.ci_data.cloud_config['final_message'])

    def test_update_true(self):
        self.conf.set('vm.update', 'True')
        self.ci_data.populate()
        cc = self.ci_data.cloud_config
        # We don't use cloud-init for that anymore, ensure we don't regress
        self.assertFalse('apt_update' in cc)
        self.assertFalse('apt_upgrade' in cc)
        self.assertFalse('package_update' in cc)
        self.assertFalse('package_upgrade' in cc)

    def test_apt_sources(self):
        self.conf.set('vm.release', 'RELEASE')
        self.conf.set('_archive_url', 'http://archive.ubuntu.com/ubuntu')
        self.conf.set('_ppa_url', 'https://u:p@ppa.lp.net/user/ppa/ubuntu')
        self.conf.set('apt.sources',
                      'deb {_archive_url} {vm.release} partner,'
                      ' deb {_archive_url} {vm.release} main,'
                      ' deb {_ppa_url} {vm.release} main|ABCDEF')
        self.ci_data.populate()
        self.assertEqual(
            [{'source':
              'deb http://archive.ubuntu.com/ubuntu RELEASE partner'},
             {'source': 'deb http://archive.ubuntu.com/ubuntu RELEASE main'},
             {'source':
              'deb https://u:p@ppa.lp.net/user/ppa/ubuntu RELEASE main',
              'keyid': 'ABCDEF'}],
            self.ci_data.cloud_config['apt_sources'])

    def create_file(self, path, content=None):
        if content is None:
            content = '{}\ncontent\n'.format(path)
        with open(path, 'wb') as f:
            if sys.version_info[0] < 3:
                f.write(content)
            else:
                f.write(bytes(content, 'utf8'))

    def test_good_ssh_keys(self):
        paths = ('rsa', 'rsa.pub', 'dsa', 'dsa.pub', 'ecdsa', 'ecdsa.pub')
        for path in paths:
            self.create_file(path)
        self.conf.set('ssh.server_keys', ','.join(paths))
        self.ci_data.populate()
        self.assertEqual({'dsa_private': 'dsa\ncontent\n',
                          'dsa_public': 'dsa.pub\ncontent\n',
                          'ecdsa_private': 'ecdsa\ncontent\n',
                          'ecdsa_public': 'ecdsa.pub\ncontent\n',
                          'rsa_private': 'rsa\ncontent\n',
                          'rsa_public': 'rsa.pub\ncontent\n'},
                         self.ci_data.cloud_config['ssh_keys'])

    def test_bad_type_ssh_keys(self):
        self.conf.set('ssh.server_keys', 'I-dont-exist')
        self.assertRaises(errors.ConfigValueError, self.ci_data.populate)

    def test_unknown_ssh_keys(self):
        self.conf.set('ssh.server_keys', 'rsa.pub')
        self.assertRaises(errors.ConfigPathNotFound, self.ci_data.populate)

    def test_unknown_ssh_authorized_keys(self):
        self.conf.set('ssh.authorized_keys', 'rsa.pub')
        self.assertRaises(errors.ConfigPathNotFound, self.ci_data.populate)

    def test_unknown_root_script(self):
        self.conf.set('vm.root_script', 'I-dont-exist')
        self.assertRaises(errors.ConfigPathNotFound, self.ci_data.populate)

    def test_unknown_user_script(self):
        self.conf.set('vm.user_script', 'I-dont-exist')
        self.assertRaises(errors.ConfigPathNotFound, self.ci_data.populate)

    def test_expansion_error_in_script(self):
        root_script_content = '''#!/bin/sh
echo Hello {I_dont_exist}
'''
        with open('root_script.sh', 'w') as f:
            f.write(root_script_content)
        self.conf.set('vm.root_script', 'root_script.sh')
        with self.assertRaises(conf_errors.ExpandingUnknownOption) as cm:
            self.ci_data.populate()
        self.assertEqual(root_script_content, cm.exception.string)

    def test_unknown_uploaded_scripts(self):
        self.conf.set('vm.uploaded_scripts', 'I-dont-exist')
        self.assertRaises(errors.ConfigPathNotFound, self.ci_data.populate)

    def test_root_script(self):
        with open('root_script.sh', 'w') as f:
            f.write('''#!/bin/sh
echo Hello {user}
''')
        self.conf.set('vm.root_script', 'root_script.sh')
        self.conf.set('user', 'root')
        self.ci_data.populate()
        # The additional newline after the script is expected
        self.assertEqual('''\
#!/bin/sh -e
cat >/tmp/root-byov_pre_install <<'EOSETUPVMUNIQUECONTENTDONTBREAKFORFUN'
#!/bin/sh
echo Hello root

EOSETUPVMUNIQUECONTENTDONTBREAKFORFUN
chown root:root /tmp/root-byov_pre_install
chmod 0700 /tmp/root-byov_pre_install
''', self.ci_data.root_hook)
        self.assertEqual(['/tmp/root-byov_pre_install'],
                         self.ci_data.cloud_config['bootcmd'])

    def test_user_script(self):
        with open('user_script.sh', 'w') as f:
            f.write('''#!/bin/sh
echo Hello {user}
''')
        self.conf.set('vm.user_script', 'user_script.sh')
        self.conf.set('user', 'testuser')
        self.ci_data.populate()
        # The additional newline after the script is expected
        self.assertEqual('''\
#!/bin/sh
echo Hello testuser
''', self.ci_data.user_hook)
        self.assertEqual(['/tmp/root-byov_post_install'],
                         self.ci_data.cloud_config['runcmd'])

    def test_uploaded_scripts(self):
        paths = ('foo', 'bar')
        for path in paths:
            self.create_file(path)
        self.conf.set('vm.uploaded_scripts', ','.join(paths))
        self.ci_data.populate()
        self.assertEqual('''\
#!/bin/sh -e
cat >~ubuntu/byov_uploads <<'EOSETUPVMUNIQUECONTENTDONTBREAKFORFUN'
mkdir -p ~ubuntu/bin
cd ~ubuntu/bin
cat >foo <<'EOFfoo'
foo
content

EOFfoo
chmod 0755 foo
cat >bar <<'EOFbar'
bar
content

EOFbar
chmod 0755 bar
EOSETUPVMUNIQUECONTENTDONTBREAKFORFUN
chown ubuntu:ubuntu ~ubuntu/byov_uploads
chmod 0700 ~ubuntu/byov_uploads
''',
                         self.ci_data.uploaded_scripts_hook)
        self.assertEqual([['su', '-l', '-c', '~ubuntu/byov_uploads',
                           'ubuntu']],
                         self.ci_data.cloud_config['runcmd'])
