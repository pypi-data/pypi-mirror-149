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

import random

# A very nice and concise summary about timeouts and retries and why using any
# network related resource requires them:
# https://docs.aws.amazon.com/general/latest/gr/api-retries.html


class ExponentialBackoff(object):
    """Provides wait times summing up to a limit.

    When an operation can fail transiently, it can be retried several times
    until it succeeds up to a specified limit. The returned values are the
    successive wait times and their total equals ``up_to``.

    :note: The total of the returned times will be ``up_to``. This mimics
        manual retries by a user re-trying randomly but giving up after a
        limit.

    :note: To simplify use by callers doing a loop around attempt/sleep, the
        last value is always zero so no time is wasted waiting after the last
        failed attempt.
    """

    random = random.random

    def __init__(self, first, up_to, retries):
        self.first = first
        self.up_to = up_to
        self.retries = retries

    def __repr__(self):
        return 'waiting {first} up to {up_to} in {retries} attempts'.format(
            **self.__dict__)

    def __iter__(self):
        attempts = 1
        cumulated = backoff = self.first
        if self.retries:
            # First wait is specified by the user
            yield self.first
        # Yield the time to wait between retries
        while attempts + 1 < self.retries:
            if cumulated + backoff > self.up_to:
                backoff = 0
            else:
                cumulated += backoff
            yield backoff
            backoff = self.first + (2 ** attempts) * self.random()
            attempts += 1
        if self.retries > 1:
            # We need at least two retries to reach ``up_to`` since ``first``
            # is specified by the user
            yield (self.up_to - cumulated)
        if self.retries:
            # Waiting after the last failure is useless
            yield 0.0
