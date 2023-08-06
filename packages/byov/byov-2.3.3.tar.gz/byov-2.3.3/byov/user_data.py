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
"""Map configuration data into a cloud-init user-data."""

from __future__ import unicode_literals
import errno
import os
import io
import yaml

from byov import (
    errors,
    ssh,
)


class CIUserData(object):
    """Maps configuration data into cloud-init user-data.

    This is a container for the data that will ultimately be encoded into a
    cloud-config-archive user-data file.
    """

    def __init__(self, conf):
        super(CIUserData, self).__init__()
        self.conf = conf
        # The objects we will populate before creating a yaml encoding as a
        # cloud-config-archive file
        self.cloud_config = {}
        self.root_hook = None
        self.user_hook = None
        self.launchpad_hook = None
        self.uploaded_scripts_hook = None

    def set(self, ud_name, conf_name=None, value=None):
        """Set a user-data option from its corresponding configuration one.

        :param ud_name: user-data key.

        :param conf_name: configuration key, If set to None, `value` should be
            provided.

        :param value: value to use if `conf_name` is None.
        """
        if value is None and conf_name is not None:
            value = self.conf.get(conf_name)
        if value:
            self.cloud_config[ud_name] = value

    def _file_content(self, path, option_name):
        full_path = os.path.expanduser(path)
        try:
            with open(full_path) as f:
                content = f.read()
        except IOError as e:
            if e.args[0] == errno.ENOENT:
                raise errors.ConfigPathNotFound(path, option_name)
            else:
                raise
        return content

    def _key_from_path(self, path, option_name):
        """Infer user-data key from file name."""
        ssh_type, kind = ssh.infos_from_path(path)
        if ssh_type is None:
            raise errors.ConfigValueError(option_name, path)
        return '%s_%s' % (ssh_type, kind)

    def set_ssh_keys(self):
        """Set the server ssh keys from a list of paths.

        Provided paths should respect some coding:

        - the base name should start with the ssh type of their key (rsa, dsa,
          ecdsa),

        - base names ending with '.pub' are for public keys, the others are for
          private keys.
        """
        key_paths = self.conf.get('ssh.server_keys')
        if key_paths:
            ssh_keys = {}
            for p in key_paths:
                key = self._key_from_path(p, 'ssh.server_keys')
                ssh_keys[key] = self._file_content(p, 'ssh.server_keys')
            self.set('ssh_keys', None, ssh_keys)

    def set_apt_sources(self):
        sources = self.conf.get('apt.sources')
        if sources:
            apt_sources = []
            for src in sources:
                # '|' should not appear in urls nor keys so it should be safe
                # to use it as a separator.
                parts = src.split('|')
                if len(parts) == 1:
                    apt_sources.append({'source': parts[0]})
                else:
                    # For PPAs, an additional GPG key should be imported in the
                    # guest.
                    apt_sources.append({'source': parts[0], 'keyid': parts[1]})
            self.cloud_config['apt_sources'] = apt_sources

    def append_bootcmd(self, cmd):
        cmds = self.cloud_config.get('bootcmd', [])
        cmds.append(cmd)
        self.cloud_config['bootcmd'] = cmds

    def append_runcmd(self, cmd):
        cmds = self.cloud_config.get('runcmd', [])
        cmds.append(cmd)
        self.cloud_config['runcmd'] = cmds

    def _hook_script_path(self, user, when):
        return '/tmp/{}-byov_{}'.format(user, when)

    def _hook_content(self, option_name, user, hook_path, mode='0700'):
        # FIXME: Add more tests towards properly creating a tree on the guest
        # from a tree on the host. There seems to be three kind of items worth
        # caring about here: file content (output path, owner, chmod), file
        # (input and output paths, owner, chmod) and directory (path, owner,
        # chmod). There are also some subtle traps involved about when files
        # are created across various vm generations (one vm creates a dir, a mv
        # on top of that one doesn't, but still creates a file in this dir,
        # without realizing it can fail in a fresh vm). -- vila 2013-03-10
        host_path = self.conf.get(option_name)
        if host_path is None:
            return None
        fcontent = self._file_content(host_path, option_name)
        # Expand options in the provided content so we report better errors
        expanded_content = self.conf.expand_options(fcontent)
        # The following will generate an additional newline at the end of the
        # script. I can't think of a case where it matters and it makes this
        # code more robust (and/or simpler) if the script/file *doesn't* end up
        # with a proper newline.
        # FIXME: This may be worth fixing if we provide a more generic way to
        # create a remote tree. -- vila 2013-03-10
        hook_content = '''#!/bin/sh -e
cat >{__guest_path} <<'EOSETUPVMUNIQUECONTENTDONTBREAKFORFUN'
{__fcontent}
EOSETUPVMUNIQUECONTENTDONTBREAKFORFUN
chown {__user}:{__user} {__guest_path}
chmod {__mode} {__guest_path}
'''
        return hook_content.format(__user=user, __fcontent=expanded_content,
                                   __mode=mode,
                                   __guest_path=hook_path)

    def set_boot_hook(self):
        # FIXME: Needs a test ensuring we execute as root -- vila 2013-03-07
        hook_path = self._hook_script_path('root', 'pre_install')
        content = self._hook_content('vm.root_script', 'root', hook_path)
        if content is not None:
            self.root_hook = content
            # FIXME: This will run on all boots and the script should also be
            # deleted once executed -- vila 2016-05-11
            self.append_bootcmd(hook_path)

    def set_user_hook(self):
        # FIXME: Needs a test ensuring we execute as default user
        # -- vila 2013-03-07
        hook_path = self._hook_script_path('root', 'post_install')
        host_path = self.conf.get('vm.user_script')
        if host_path is None:
            return
        fcontent = self._file_content(host_path, 'vm.user_script')
        if fcontent is not None:
            # Expand options in the provided content so we report better errors
            self.user_hook = self.conf.expand_options(fcontent)
            self.append_runcmd(hook_path)

    def set_uploaded_scripts(self):
        script_paths = self.conf.get('vm.uploaded_scripts')
        if not script_paths:
            return
        hook_path = self.conf.expand_options('~{vm.user}/byov_uploads')
        bindir = self.conf.get('vm.uploaded_scripts.guest_dir')
        out = io.StringIO()
        out.write('''#!/bin/sh -e
cat >{hook_path} <<'EOSETUPVMUNIQUECONTENTDONTBREAKFORFUN'
mkdir -p {bindir}
cd {bindir}
'''.format(**locals()))
        for path in script_paths:
            fcontent = self._file_content(path, 'vm.uploaded_scripts')
            expanded = self.conf.expand_options(fcontent)
            base = os.path.basename(path)
            # FIXME: ~Duplicated from _hook_content. -- vila 2012-03-15
            out.write('''cat >{base} <<'EOF{base}'
{expanded}
EOF{base}
chmod 0755 {base}
'''.format(**locals()))

        out.write('''EOSETUPVMUNIQUECONTENTDONTBREAKFORFUN
chown {user}:{user} {hook_path}
chmod 0700 {hook_path}
'''.format(user=self.conf.get('vm.user'), **locals()))
        self.uploaded_scripts_hook = out.getvalue()
        self.append_runcmd(['su', '-l', '-c',
                            hook_path, self.conf.get('vm.user')])

    def set_users_groups(self):
        # FIXME: There is a risk that we need to play catch-up with cloud-init
        # changing default values (or running into a bug because we don't
        # properly cover the same defaults). Ideally, there should be a way to
        # revert to cloud-init 'default' user. -- vila 2018-03-06
        user = {
            'name': self.conf.get('vm.user'),
            'system': self.conf.get('vm.user.system'),
        }
        shell = self.conf.get('vm.user.shell')
        if shell:
            user['shell'] = shell
        home = self.conf.get('vm.user.home')
        if home:
            user['homedir'] = home
        ssh_keys = self.conf.get('ssh.authorized_keys')
        if ssh_keys:
            paths = [self._file_content(path, 'ssh.authorized_keys')
                     for path in ssh_keys]
            user['ssh-authorized-keys'] = paths
        sudos = self.conf.get('vm.user.sudo')
        if sudos:
            user['sudo'] = sudos
        self.set('users', None, [user])

    def populate(self):
        # The commands executed during init stage
        self.set_boot_hook()
        # Common and non-configurable options
        # login from the console can help diagnose network issues. This can be
        # authorized by using dict(expire=False, list=['ubuntu:ubuntu']) below
        # FIXME: That was needed again to debug a network related issue so
        # deserve an option -- vila 2019-10-15
        # The rationale is:
        # When something goes wrong in the stack leading to a working ssh
        # connection, debug can be achieved by connecting via the console. But
        # for that to work, the default user needs a valid password rather than
        # the default policy being to allow only ssh access with an authorized
        # key.
        chpasswd = self.conf.get('vm.chpasswd')
        if chpasswd:
            self.set('chpasswd', None, dict(expire=False, list=chpasswd))
        else:
            self.set('chpasswd', None, dict(expire=True))
        # Configurable options
        self.set('manage_etc_hosts', 'vm.manage_etc_hosts')
        self.set('fqdn', 'vm.fqdn')
        msg = self.conf.get('vm.final_message')
        if msg is None:
            if self.conf.get('vm.release') == 'precise':
                # Curse cloud-init lack of compatibility
                msg = 'byov finished installing in $UPTIME seconds.'
            else:
                msg = 'byov finished installing in ${uptime} seconds.'
        self.set('final_message', None, msg)
        self.set_users_groups()
        self.set_ssh_keys()
        self.set('apt_proxy', 'apt.proxy')
        self.set('locale', 'vm.locale')
        self.set_apt_sources()
        # upload the scripts
        self.set_uploaded_scripts()
        # The commands executed before powering off
        self.set_user_hook()

    def add_boot_hook(self, parts, hook):
        """Add a cloud-boothook.

        Note that this hook is excuted immediately, run at every boot at an
        early stage where parts of the system may not be available (including
        the default user).

        :params parts: The existing parts of the cloud-config-archive.

        :params hook: The hook to add in textual form.
        """
        if hook is not None:
            parts.append({'content': '#cloud-boothook\n' + hook})

    def add_user_data_script(self, parts, hook):
        """Add a User-Data script.

        The received script is executed very late in the boot sequence
        (rc.local-like).

        :params parts: The existing parts of the cloud-config-archive.

        :params hook: The hook to add in textual form. It MUST start with a
            shebang line '#!'.
        """
        if hook is not None:
            parts.append({'content': hook})

    def dump(self):
        def yaml_dumps(obj):
            return yaml.safe_dump(obj)

        parts = [{'content':
                  '#cloud-config\n' + yaml_dumps(self.cloud_config)}]
        self.add_boot_hook(parts, self.root_hook)
        self.add_user_data_script(parts, self.launchpad_hook)
        self.add_user_data_script(parts, self.uploaded_scripts_hook)
        self.add_user_data_script(parts, self.user_hook)
        # Wrap the lot into a cloud config archive
        return '#cloud-config-archive\n' + yaml_dumps(parts)
