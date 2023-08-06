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
import contextlib
import importlib.util
import os
import sys
import time


import byov
from byoc import (
    stacks,
    stores,
)


HERE = os.path.abspath(os.path.dirname(__file__))
BRANCH_ROOT = os.path.abspath(os.path.join(HERE, '..'))


class StartingNameMatcher(stacks.SectionMatcher):
    """A sub name section matcher.

    This selects sections starting with a given name with sections sorted
    alphanumerically.
    """

    def __init__(self, store, name):
        super(StartingNameMatcher, self).__init__(store)
        self.name = name

    def get_sections(self):
        """Get all sections starting with ``name`` in the store.

        The most generic sections are described first in the store, then more
        specific ones can be provided for reduced scopes.

        The returned sections are therefore returned in the reversed order so
        the most specific ones can be found first.
        """
        store = self.store
        # Longer sections are more specific, they should be returned first
        for _, section in sorted(
                store.get_sections(), reverse=True,
                # s[1].id or '' is to cope with None as a section id
                key=lambda s: s[1].id or ''):
            if section.id is None:
                # The no-name section is always included if present
                yield store, section
                continue
            if self.name is None:
                # If no name has been defined, no section can match
                continue
            section_name = section.id
            if self.name.startswith(section_name):
                yield store, section


VmMatcher = StartingNameMatcher
VmStore = stores.FileStore
VmCmdLineStore = stores.CommandLineStore


def system_config_dir():
    return '/etc/byov'


def user_config_dir():
    return os.path.expanduser('~/.config/byov')


def config_file_basename():
    return 'byov.conf'


def existing_config_file_basename():
    return 'existing-vms.conf'


def config_files_in(directory, conf_dir='conf.d', suffix='.conf'):
    """Iterate valid config file names in a directory."""
    fulldir = os.path.join(directory, conf_dir)
    if os.path.exists(fulldir):
        for p in sorted(os.listdir(fulldir)):
            # Filter out if not ending with suffix (so README files, for
            # example could be added or renaming can be used to disable config
            # files)
            if p.endswith(suffix):
                yield os.path.join(fulldir, p)


class LockedTimeout(Exception):
    pass


class Locked(object):

    def __init__(self, protected, timeout=10, delay=.05, info=None):
        self.path = protected + '.lock'
        self.timeout = timeout
        self.delay = delay
        self.locked = False
        self.info = info
        if self.info is None:
            self.info = "Created by:\n" + '\n'.join(sys.argv)

    def available(self):
        """
        Returns True iff the file is currently available to be locked.
        """
        return not os.path.exists(self.path)

    def acquire(self, blocking=True):
        '''Acquire the lock, if possible.

        If the lock is in use, and `blocking` is False, return
        False. Otherwise, check again every `self.delay` seconds until it
        either gets the lock or exceeds `timeout` number of seconds, in which
        case it raises an exception.
        '''
        start_time = time.time()
        while True:
            try:
                # Attempt to create the lockfile.

                # These flags cause os.open to raise an FileExistsError if the
                # file already exists.
                fd = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_RDWR)
                with os.fdopen(fd, "a") as f:
                    # Print some info about the current process as debug info
                    # for anyone who bothers to look.
                    f.write(self.info)
                break
            except FileExistsError:
                # The lock is held, wait before retrying
                if (time.time() - start_time) >= self.timeout:
                    raise LockedTimeout("Timeout occurred.")
                if not blocking:
                    return False
                time.sleep(self.delay)
        self.locked = True
        return True

    def release(self):
        self.locked = False
        os.unlink(self.path)

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.release()
        # Handle exceptions that may have come up during execution, by
        # default any exceptions are raised to the user.
        return bool(exc_type is None)

    def __del__(self):
        '''Make sure to cleanup.'''
        if self.locked:
            self.release()


class VmStack(stacks.Stack):
    """Per-vm options."""

    def __init__(self, name):
        """Make a new stack for a given vm.

        :param name: The name of a virtual machine.

        The options are searched in following files for all sections matching
        ``name``. Additionally, defaults can be provided in the no-name
        section, except for ``existing-vms.conf`` which uses only the ``name``
        section.

        * for each path in byov.path:
          * the directory local file: ./byov.conf
          * the directory files in alphanumeric order: byov.conf.d/*.conf.

        * the user file: ~/.config/byov/byov.conf
        * the user files in alphanumeric order: ~/.config/byov/conf.d/*.conf.
        * the system-wide file: /etc/byov.conf
        * the system-wide files in alphanumeric order: /etc/byov/conf.d/*.conf.
        * the existing vms file (for vms already setup):
          ~/.config/byov/existing-vms.conf

        Longer section names are more specific than shorter ones across all
        files.

        """
        self.vm_name = name
        # FIXME: Would life be simpler if the cmdline store was shared ?  Or
        # not ? -- vila 2018-02-12

        # FIXME: Hard-coding a class name is a smell, at the very least make
        # this a class attribute. -- vila 2019-08-13
        self.cmdline_store = VmCmdLineStore()

        section_getters = []

        for root in byov.path:
            lpath = os.path.abspath(os.path.join(root, config_file_basename()))
            store = self.get_shared_store(VmStore(lpath))
            section_getters.append(VmMatcher(store, name).get_sections)

            for cpath in config_files_in(root, 'byov.conf.d'):
                store = self.get_shared_store(VmStore(cpath))
                section_getters.append(VmMatcher(store, name).get_sections)

        upath = os.path.join(user_config_dir(), config_file_basename())
        self.user_store = self.get_shared_store(VmStore(upath))
        section_getters.append(VmMatcher(self.user_store, name).get_sections)

        for cpath in config_files_in(user_config_dir()):
            store = self.get_shared_store(VmStore(cpath))
            section_getters.append(VmMatcher(store, name).get_sections)

        spath = os.path.join(system_config_dir(), config_file_basename())
        self.system_store = self.get_shared_store(VmStore(spath))
        section_getters.append(VmMatcher(self.system_store, name).get_sections)

        for cpath in config_files_in(system_config_dir()):
            store = self.get_shared_store(VmStore(cpath))
            section_getters.append(VmMatcher(store, name).get_sections)

        epath = os.path.join(user_config_dir(),
                             existing_config_file_basename())
        self.existing_store = self.get_shared_store(VmStore(epath))

        super(VmStack, self).__init__(
            section_getters, self.user_store, mutable_section_id=name)

    def iter_sections(self):
        """Iterate all the defined sections.

        We break the lazy loading from byoc here as we want to ensure that
        section referring to a matching host are matched across
        files. Otherwise, a more specific section in a file is masked by a
        shorter section in a previous file.
        """
        # First the cmdline section
        for store, section in self.cmdline_store.get_sections():
            yield store, section

        host_getters = []
        # Now we break the lazy loading: we need to find all matching sections
        # keeping track of the store rank for later sort.
        for rank, section_getter in enumerate(self.sections_def):
            host_getters.extend([(-rank, store, section)
                                 for store, section in section_getter()])
        # We sort on section name then store rank and reverse the whole.
        # Specific section comes first, ties respect store order
        # t[2].id or '' is to cope with None as a section id
        getters = sorted(host_getters, key=lambda t: (t[2].id or '', t[0]),
                         reverse=True)
        for _, store, section in getters:
            yield store, section

        # Finally the existing vm section
        # We want to match only the existing vm, not any other one
        for store, section in stacks.NameMatcher(self.existing_store,
                                                 self.vm_name).get_sections():
            yield store, section

    @contextlib.contextmanager
    def lock(self, store=None):
        if store is None:
            store = self.store
        with Locked(store.path) as locked:
            # Make sure to start with a fresh copy
            store.unload()
            store.load()
            yield locked
            # Save all changes before unlocking
            store.save()
            # Unload for good measure
            store.unload()

    # FIXME: This should be a DictOption or a NameSpaceOption
    # -- vila 2018-01-08
    def get_nova_creds(self):
        """Get nova credentials from a config.

        This defines the set of options needed to authenticate against nova in
        a single place.

        :raises: byoc.errors.OptionMandatoryValueError if one of the
            options is not set.
        """
        creds = {}
        for k in ('username', 'password', 'tenant_name',
                  'auth_url', 'region_name'):
            opt_name = 'nova.{}'.format(k)
            creds[opt_name] = self.get(opt_name)
        return creds

    # FIXME: This should be a DictOption or a NameSpaceOption
    # -- vila 2021-12-03
    def get_aws_creds(self):
        """Get aws credentials from a config.

        This defines the set of options needed to authenticate against aws in
        a single place.

        :raises: byoc.errors.OptionMandatoryValueError if one of the
            options is not set.
        """
        creds = {}
        for k in ('key', 'secret', 'token', 'region'):
            opt_name = 'aws.{}'.format(k)
            creds[opt_name] = self.get(opt_name)
        return creds

    # FIXME: This should be a DictOption or a NameSpaceOption
    # -- vila 2021-12-03
    def get_scaleway_creds(self):
        """Get scaleway credentials from a config.

        This defines the set of options needed to authenticate against scaleway
        in a single place.

        :raises: byoc.errors.OptionMandatoryValueError if one of the
            options is not set.

        """
        # In theory the token is region agnostic, in practice you can't use
        # compute without a region (the api host name includes the region
        # name).
        creds = {}
        for k in ('access_key', 'token', 'region_name'):
            opt_name = 'scaleway.{}'.format(k)
            creds[opt_name] = self.get(opt_name)
        return creds


class ExistingVmStack(stacks.Stack):
    """Internal stack for defined vms."""

    def __init__(self, name):
        """Make a new stack for an already setup virtual machine.

        :param name: The name of a virtual machine.

        The options are searched only in the ~/.config/byov/existing-vms.conf
        which contains one section per virtual machine.
        """
        dpath = os.path.join(user_config_dir(),
                             existing_config_file_basename())
        store = self.get_shared_store(VmStore(dpath))
        section_getters = [stacks.NameMatcher(store,
                                              name).get_sections]
        super(ExistingVmStack, self).__init__(
            section_getters, store, mutable_section_id=name)


# MISSINGTESTS: below, to refine the API, basically, when user provided
# 'byov.py' have to be imported requires precision. It's the complement to
# byov.path/BYOV_PATH handling, it controls when user provided `byov.py` files
# are imported. This even desserve a whole documentation better than a FIXME or
# MISSINGTESTS <8-) -- vila 2022-04-04


def import_user_byov_from(dir_path):
    path = os.path.abspath(os.path.join(dir_path, 'byov.py'))
    if os.path.exists(path):
        spec = importlib.util.spec_from_file_location('byov.config.user',
                                                      path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)


def import_user_byovs():
    # FIXME: This duplicates VmStack definition somehow, will need a better way
    # -- vila 2018-10-18
    if BRANCH_ROOT not in byov.path:
        byov.path.append(BRANCH_ROOT)
    searched_dirs = [os.path.join(root, 'byov.conf.d') for root in byov.path]
    searched_dirs.append(os.path.join(user_config_dir(), 'conf.d'))
    searched_dirs.append(os.path.join(system_config_dir(), 'conf.d'))
    for d in searched_dirs:
        import_user_byov_from(d)
