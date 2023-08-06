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

# A tuple containing the five components of the version number: major, minor,
# micro, releaselevel, and serial. All values except releaselevel are integers;
# the release level is 'dev' or 'final'. The
# version_info value corresponding to the byov version 2.0 is (2, 0, 0,
# 'final', 0).
import os

# Using realpath below as __file__ may include a symlink
HERE = os.path.realpath(os.path.dirname(__file__))
BRANCH_ROOT = os.path.abspath(os.path.join(HERE, '..'))

__version__ = (2, 3, 3, 'final', 0)


# FIXME: This is not exposed to user like config options. doc ?
# -- vila 2022-03-31

# A list of directories where scripts and hooks (as relative paths) are
# searched for. '~' is expanded if present. An exception is raised if the
# relative path cannot be found in any of the directories or if it's not an
# executable.

# This can be extended by other libraries/projects to layout a new set of
# configuration files on top of the regular ones.
path = os.getenv('BYOV_PATH', BRANCH_ROOT).split(':')


def version(ver=None):
    if ver is None:
        ver = __version__
    major, minor, patch, ver_type, increment = ver
    if ver_type == 'final':
        return '{}.{}.{}'.format(major, minor, patch)
    else:
        return '{}.{}.{}{}{}'.format(*ver)
