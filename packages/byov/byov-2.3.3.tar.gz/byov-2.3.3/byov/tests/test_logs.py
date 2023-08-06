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

import unittest


from byov import logs


class TestIpAddrRegexp(unittest.TestCase):

    def setUp(self):
        super(TestIpAddrRegexp, self).setUp()
        self.re = logs.ip_address_re

    def assertMatches(self, ip_addr):
        match = self.re.match(ip_addr)
        self.assertIsNotNone(match)

    def assertDontMatch(self, ip_addr):
        match = self.re.match(ip_addr)
        self.assertIsNone(match)

    def test_matches(self):
        self.assertMatches('192.168.0.12')
        self.assertMatches('19.16.0.0')
        self.assertMatches('1.1.1.1')

    def test_dont_match(self):
        self.assertDontMatch('')
        self.assertDontMatch('1924.168.0.0')
        self.assertDontMatch('192.1682.0.0')
        self.assertDontMatch('192.168..0')


class TestMacAddrRegexp(unittest.TestCase):

    def setUp(self):
        super(TestMacAddrRegexp, self).setUp()
        self.re = logs.mac_address_re

    def assertMatches(self, mac_addr):
        match = self.re.match(mac_addr)
        self.assertIsNotNone(match)

    def assertDontMatch(self, mac_addr):
        match = self.re.match(mac_addr)
        self.assertIsNone(match)

    def test_matches(self):
        self.assertMatches('00:16:3e:38:8d:7e')
        self.assertMatches('00:16:3e:87:7b:38')
        self.assertMatches('00:50:e4:70:b3:23')
        self.assertMatches('00:24:b2:38:f6:d6')
        self.assertMatches('00:16:CB:9E:F0:A1')
        self.assertMatches('08:00:27:9B:A0:2C')
        self.assertMatches('10:9A:DD:A7:08:DA')
        self.assertMatches('00:1D:0F:B0:EB:3A')
        self.assertMatches('52:54:00:04:7B:45')

    def test_dont_match(self):
        self.assertDontMatch('')
        self.assertDontMatch('08:00:27:2d:64:')
        self.assertDontMatch(':00:27:52:27:b8')
        self.assertDontMatch('c4:3d:c7:55:5c:8')
        self.assertDontMatch('0:16:3e:c5:62:08')


class TestIfaceRegexp(unittest.TestCase):

    def setUp(self):
        super(TestIfaceRegexp, self).setUp()
        self.re = logs.InterfaceRegexp('(eth0|ens3)')

    def assertMatches(self, expected, line):
        match = self.re.match(line)
        self.assertIsNotNone(match)
        iface, ip, mask, mac = match.groups()
        self.assertEqual(expected, (iface, ip, mask, mac))

    def test_matches_quantal(self):
        line = 'ci-info: |  {}  | True | {} | {} | {} |'
        addrs = ('eth0', '192.168.0.119', '255.255.255.0', '00:16:3e:38:8d:7e')
        self.assertMatches(addrs, line.format(*addrs))

    def test_matches_xenial(self):
        line = 'ci-info: |  {}  | True | {} | {} | {} |'
        addrs = ('ens3', '192.168.0.119', '255.255.255.0', '00:16:3e:38:8d:7e')
        self.assertMatches(addrs, line.format(*addrs))

    def test_matches_precise(self):
        line = 'ci-info: {}  : 1  {}   {}   {}'
        addrs = ('eth0', '192.168.0.119', '255.255.255.0', '00:16:3e:38:8d:7e')
        self.assertMatches(addrs, line.format(*addrs))
