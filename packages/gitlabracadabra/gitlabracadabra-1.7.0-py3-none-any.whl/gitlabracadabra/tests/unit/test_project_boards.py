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

from unittest import skipIf

from gitlab import __version__ as gitlab_version

from gitlabracadabra.objects.project import GitLabracadabraProject
from gitlabracadabra.tests import my_vcr
from gitlabracadabra.tests.case import TestCaseWithManager


class TestProjectBoards(TestCaseWithManager):
    @skipIf(gitlab_version in ['1.6.0'], 'python-gitlab without board update support')
    @my_vcr.use_cassette
    def test_boards(self, cass):
        obj = GitLabracadabraProject('memory', 'test/test_boards', {
            'boards': [
                {
                    'name': 'create_me',
                    'hide_backlog_list': True,
                    'hide_closed_list': True,
                    'lists': [
                        {
                            'label': 'move_me_first',
                        },
                        {
                            'label': 'keep_me',
                        },
                        {
                            'label': 'add_me',
                        },
                        {
                            'label': 'i_dont_exists',
                        },
                    ],
                },
                {
                    'name': 'modify_me',
                    'hide_backlog_list': True,
                    'hide_closed_list': True,
                    'lists': [
                        {
                            'label': 'move_me_first',
                        },
                        {
                            'label': 'keep_me',
                        },
                        {
                            'label': 'add_me',
                        },
                        {
                            'label': 'i_dont_exists',
                        },
                    ],
                },
                {
                    'name': 'do_no_modify_my_lists',
                },
            ],
            'unknown_boards': 'delete',
            'unknown_board_lists': 'delete',
        })
        self.assertEqual(obj.errors(), [])
        obj.process()
        self.assertTrue(cass.all_played)
