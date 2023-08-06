# -*- coding: utf-8 -*-
#
# Copyright (C) 2019-2021 Mathieu Parent <math.parent@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from unittest.mock import patch

from gitlabracadabra.containers.registry_session import Token
from gitlabracadabra.tests.case import TestCase


class TestToken(TestCase):
    """Test Token class."""

    def test_simple(self) -> None:
        """Test simple token."""
        current_time = 42.42
        one_hour = 3600
        with patch('gitlabracadabra.containers.registry_session.time') as mocked_time:
            mocked_time.return_value = current_time
            token = Token('abc', one_hour)
            self.assertEqual(token.token, 'abc')
            self.assertEqual(token.expiration_time, current_time + one_hour)
            self.assertFalse(token.is_expired())

            mocked_time.return_value = current_time + one_hour - 1
            self.assertFalse(token.is_expired())

            mocked_time.return_value = current_time + one_hour
            self.assertTrue(token.is_expired())

    def test_short_lifetime(self) -> None:
        """Test token with too short expires_in."""
        current_time = 42.42
        one_minute = 60
        with patch('gitlabracadabra.containers.registry_session.time') as mocked_time:
            mocked_time.return_value = current_time
            token = Token('def', 1)
            self.assertEqual(token.token, 'def')
            self.assertEqual(token.expiration_time, current_time + one_minute)
            self.assertFalse(token.is_expired())

            mocked_time.return_value = current_time + one_minute - 1
            self.assertFalse(token.is_expired())

            mocked_time.return_value = current_time + one_minute
            self.assertTrue(token.is_expired())
