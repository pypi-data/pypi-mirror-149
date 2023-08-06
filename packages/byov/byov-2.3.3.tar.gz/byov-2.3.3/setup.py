#!/usr/bin/env python3

# This file is part of Build Your Own Virtual machine.
#
# Copyright 2018 Vincent Ladeuil.
# Copyright 2014, 2015, 2016 Canonical Ltd.
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

import os
import setuptools


import byov


class CleanCommand(setuptools.Command):
    """Custom clean command to tidy up the project root."""
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system('rm -vrf ./byov.egg-info')


setuptools.setup(
    name='byov',
    version='.'.join(str(c) for c in byov.__version__[0:3]),
    description=('Build Your Own Virtual machine.'),
    author='Vincent Ladeuil',
    author_email='v.ladeuil+lp@free.fr',
    url='https://launchpad.net/byov',
    license='GPLv3',
    install_requires=['python3-byoc'],
    packages=['byov', 'byov.tests', 'byov.vms'],
    # FIXME: byovm is kept for backwards compatibility, remove it for 3.0
    # -- vila 2022-03-09
    entry_points=dict(console_scripts=['byov=byov.commands:run',
                                       'byovm=byov.commands:run']),
    cmdclass=dict(clean=CleanCommand),
)
