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


class BaseError(Exception):
    """Base class for all byov exceptions.

    :cvar fmt: A format string that daughter classes override.
    """

    fmt = 'Daughter classes should redefine this'

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __unicode__(self):
        return self.fmt.format([], **self.__dict__)

    __repr__ = __unicode__
    __str__ = __unicode__


class ByovError(BaseError):

    def __init__(self, fmt, **kwargs):
        super(ByovError, self).__init__(**kwargs)
        self.fmt = fmt


class VmUnknown(BaseError):

    fmt = '"{name}" is unknown.'

    def __init__(self, name):
        super(VmUnknown, self).__init__(name=name)


class InvalidVmClass(BaseError):

    fmt = 'vm.class "{value}" is not valid for "{name}".'

    def __init__(self, name, value):
        super(InvalidVmClass, self).__init__(name=name, value=value)


class VmRunning(BaseError):

    fmt = '"{name}" is running.'

    def __init__(self, name):
        super(VmRunning, self).__init__(name=name)


class VmNotRunning(BaseError):

    fmt = '"{name}" is not running.'

    def __init__(self, name):
        super(VmNotRunning, self).__init__(name=name)


class CommandError(BaseError):

    fmt = '''
  command: {joined_cmd}
  retcode: {retcode}
  stdout: {out}
  stderr: {err}
'''

    def __init__(self, cmd, retcode, out, err):
        super(CommandError, self).__init__(joined_cmd=' '.join(cmd),
                                           retcode=retcode, err=err, out=out)


class ConfigOptionNotFound(BaseError):

    fmt = 'Option "{name}" does not exist.'

    def __init__(self, name):
        super(ConfigOptionNotFound, self).__init__(name=name)


class ConfigValueError(BaseError):

    fmt = 'Bad value "{value}" for option "{name}".'

    def __init__(self, name, value):
        super(ConfigValueError, self).__init__(name=name, value=value)


class ConfigPathNotFound(BaseError):

    fmt = 'No such file: {path} from {name}'

    def __init__(self, path, name):
        super(ConfigPathNotFound, self).__init__(path=path, name=name)


class ConsoleEOFError(BaseError):

    fmt = 'Encountered EOF on console, something went wrong'


class CloudInitError(BaseError):

    fmt = 'cloud-init reported: {line} check your config'

    def __init__(self, line):
        super(CloudInitError, self).__init__(line=line)


class SubIdError(BaseError):

    fmt = 'The /etc/sub{typ} file has no "root:{subid}:1" line'

    def __init__(self, typ, subid):
        super(SubIdError, self).__init__(typ=typ, subid=subid)
