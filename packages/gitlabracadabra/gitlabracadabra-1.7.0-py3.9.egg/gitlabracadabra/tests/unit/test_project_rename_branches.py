#!/usr/bin/env python
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

from unittest.mock import call, patch

from gitlabracadabra.objects.project import GitLabracadabraProject
from gitlabracadabra.tests import my_vcr
from gitlabracadabra.tests.case import TestCaseWithManager


class TestProjectRenameBranches(TestCaseWithManager):
    @my_vcr.use_cassette
    def test_rename_branches(self, cass):
        obj = GitLabracadabraProject('memory', 'test/test_rename_branches', {
            'rename_branches': [
                {'old_name': 'new_name'},
                {'branch2': 'branch3'},
                {'branch1': 'branch2'},
                {'does_not_exists': 'already_exists'},
                {'does_not_exists': 'should_print_error'},
            ],
        })
        self.assertEqual(obj.errors(), [])
        with patch('gitlabracadabra.mixins.rename_branches.logger', autospec=True) as logger:
            obj.process()
        logger.assert_has_calls([
            call.info('[%s] Renaming branch from %s to %s', 'test/test_rename_branches', 'old_name', 'new_name'),
            call.info('[%s] Renaming branch from %s to %s', 'test/test_rename_branches', 'branch2', 'branch3'),
            call.info('[%s] Renaming branch from %s to %s', 'test/test_rename_branches', 'branch1', 'branch2'),
            call.info('[%s] NOT Renaming branch from %s to %s (old branch not found)',
                      'test/test_rename_branches', 'does_not_exists', 'should_print_error'),
        ])
        self.assertTrue(cass.all_played)
