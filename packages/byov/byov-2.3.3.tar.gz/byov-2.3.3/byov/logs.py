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
"""Utilities to define, access and process the various log files Vms produce.

Various log files are produced on the host but contains information about vms
internals.

Various tricks are currently involved as while the user want full control on
this file, they are often created or populated with root access rights for the
file themselves or the directories where they leave.

Some information in those files may be acquired in better ways than scrapping
log files. Yet, this is a useful fallback until this information is available
from other sources.
"""

import re

# Note: There may be a simpler way than defining classes to decorate python
# regexps but it's not obvious to get that right. For now, this will do.


class Regexp(object):

    def __init__(self, string, flags=0):
        """Regexp constructor.

        :param string: The regular expression textual representation.

        :params flags: The 're.compile' applicable flags.
        """
        self.string = string
        self.flags = flags
        self.re = None

    def ensure_re(self):
        if self.re is None:
            self.re = re.compile(self.string, self.flags)

    def match(self, string):
        self.ensure_re()
        return self.re.match(string)

# FIXME: The following regexp is searched for in cloud-init output. This design
# fails when cloud-init is disabled (see http://pad.lv/1669675)
# -- vila 2019-10-16

# The following lines have been observed for Ubuntu releases from precise to
# trusty (IP replaced with x.x.x.x to please pep8, /me sighs):

# precise:
# ci-info: eth0  : 1  x.x.x.x   255.255.255.0   00:16:3e:9d:7d:2a
# quantal:
# ci-info: |  eth0  | True | x.x.x.x | 255.255.255.0 | 00:16:3e:5d:83:2d |
# raring
# ci-info: |  eth0  | True | x.x.x.x | 255.255.255.0 | 00:16:3e:87:7b:38 |
# saucy:
# ci-info: |  eth0  | True | x.x.x.x | 255.255.255.0 | 00:16:3e:5f:5d:48 |
# trusty:
# ci-info: |  eth0  | True | x.x.x.x | 255.255.255.0 | 00:16:3e:38:8d:7e |
# wily/systemd appeared briefly bug get reverted:
# ci-info: |  ens3  | True | x.x.x.x | 255.255.255.0 |   .   | <MAC addr> |
# and ens3 is back with xenial
# ci-info: |  ens3  | True | x.x.x.x | 255.255.255.0 |   .   | <MAC addr> |


# Which can be captured with the following regexps:

ip_address_re = Regexp(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
mac_address_re = Regexp(r'[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:'
                        r'[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}')


# We use a template so the interface name can be injected at run time

class InterfaceRegexp(Regexp):

    def __init__(self, iface, flags=0):
        super(InterfaceRegexp, self).__init__(None, flags=flags)
        self.iface = iface

    def ensure_re(self):
        if self.re is None:
            # We could generalize to a TemplatedRegexp accepting a template and
            # some format parameters (and flags ?) but until we need it, it's
            # overkill.

            # FIXME: vivid seems to say it's not overkill anymore...  the
            # output describing the interface definition has changed. Tests
            # missing. -- vila 2015-05-10
            template = r'.*ci-info: .*{0}.*?({1}).*?({1}).*?({2})'
            self.string = template.format(self.iface,
                                          ip_address_re.string,
                                          mac_address_re.string)
            self.re = re.compile(self.string, self.flags)
