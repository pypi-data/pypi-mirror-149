# This file is part of Build Your Own Virtual machine.
#
# Copyright 2018 Vincent Ladeuil.
# Copyright 2015, 2016, 2017 Canonical Ltd.

# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License version 3, as
# published by the Free Software Foundation.

# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranties of
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import unittest

from byot import assertions

from byov import timeouts


class TestExponentialBackoff(unittest.TestCase):

    def test_no_timeouts(self):
        timo = timeouts.ExponentialBackoff(1, 2, 0)
        assertions.assertLength(self, 0, list(timo))

    def test_single_retry(self):
        eb = timeouts.ExponentialBackoff(0, 2, 1)
        timo = list(eb)
        assertions.assertLength(self, 2, timo)

    def test_two_retries(self):
        eb = timeouts.ExponentialBackoff(0, 2, 2)
        timo = list(eb)
        assertions.assertLength(self, 3, timo)

    def test_up_to_5mins(self):
        timo = timeouts.ExponentialBackoff(12, 300, 10)
        values = list(timo)
        # There is one more timeout than retries
        assertions.assertLength(self, 11, values)
        # The first duration is explicit
        self.assertEqual(12, values[0])
        # The sum of wait times is equal to up_to
        self.assertEqual(300, sum(values))
