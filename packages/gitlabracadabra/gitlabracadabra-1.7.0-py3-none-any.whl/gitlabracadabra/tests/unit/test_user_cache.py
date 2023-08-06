# -*- coding: utf-8 -*-
#
# Copyright (C) 2019-2020 Mathieu Parent <math.parent@gmail.com>
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

from gitlabracadabra.gitlab.connections import GitlabConnections
from gitlabracadabra.tests import my_vcr
from gitlabracadabra.tests.case import TestCaseWithManager


class TestUserCache(TestCaseWithManager):
    """Test UserCache."""

    @my_vcr.use_cassette
    def test_id_from_username(self, cass):
        """Test #id_from_username.

        Args:
            cass: VCR cassette.
        """
        cache = GitlabConnections().get_connection().user_cache
        ret = cache.id_from_username('user_mapping')
        self.assertEqual(ret, 9)
        self.assertTrue(cass.all_played)

    @my_vcr.use_cassette
    def test_username_from_id(self, cass):
        """Test #username_from_id.

        Args:
            cass: VCR cassette.
        """
        cache = GitlabConnections().get_connection().user_cache
        ret = cache.username_from_id(9)
        self.assertEqual(ret, 'user_mapping')
        self.assertTrue(cass.all_played)
