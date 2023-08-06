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

from gitlabracadabra.dictutils import update_dict_with_defaults
from gitlabracadabra.tests.case import TestCase


class TestDictUtils(TestCase):
    """Test gitlabracadabra.dictutils."""

    def test_update_dict_with_defaults(self):
        """Test update_dict_with_defaults."""
        defaults = {
            '.foo': {
                'not_overridden_string': 'foo',
                'not_overridden_dict': {'foo': {'bar': 'buz'}},
                'not_overridden_list': ['ab', 'cd'],
                'overridden_string': 'D_foo',
                'overridden_dict': {'D_foo': {'D_bar': 'D_buz'}},
                'overridden_list': ['D_ab', 'D_cd'],
            },
        }
        target = {
            '.foo': {
                'overridden_string': 'O_foo',
                'overridden_dict': {'D_foo': {'O_bar': 'O_buz'}},
                'overridden_list': ['O_ab', 'O_cd'],
            },
        }
        update_dict_with_defaults(target, defaults)
        expected = {
            '.foo': {
                'not_overridden_string': 'foo',
                'not_overridden_dict': {'foo': {'bar': 'buz'}},
                'not_overridden_list': ['ab', 'cd'],
                'overridden_string': 'O_foo',
                'overridden_dict': {'D_foo': {'D_bar': 'D_buz', 'O_bar': 'O_buz'}},
                'overridden_list': ['O_ab', 'O_cd'],
            },
        }
        self.assertEqual(target, expected)

    def test_update_dict_with_defaults_aggregate(self):
        """Test update_dict_with_defaults with aggregate=True."""
        defaults = {
            '.foo': {
                'not_overridden_string': 'foo',
                'not_overridden_dict': {'foo': {'bar': 'buz'}},
                'not_overridden_list': ['ab', 'cd'],
                'overridden_string': 'D_foo',
                'overridden_dict': {'D_foo': {'D_bar': 'D_buz'}},
                'overridden_list': ['D_ab', 'D_cd'],
            },
        }
        target = {
            '.foo': {
                'overridden_string': 'O_foo',
                'overridden_dict': {'D_foo': {'O_bar': 'O_buz'}},
                'overridden_list': ['O_ab', 'O_cd'],
            },
        }
        update_dict_with_defaults(target, defaults, aggregate=True)
        expected = {
            '.foo': {
                'not_overridden_string': 'foo',
                'not_overridden_dict': {'foo': {'bar': 'buz'}},
                'not_overridden_list': ['ab', 'cd'],
                'overridden_string': 'O_foo',
                'overridden_dict': {'D_foo': {'D_bar': 'D_buz', 'O_bar': 'O_buz'}},
                'overridden_list': ['D_ab', 'D_cd', 'O_ab', 'O_cd'],
            },
        }
        self.assertEqual(target, expected)
