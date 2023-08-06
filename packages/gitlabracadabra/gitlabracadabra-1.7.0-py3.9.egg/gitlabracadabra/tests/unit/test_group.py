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

from gitlabracadabra.objects.group import GitLabracadabraGroup
from gitlabracadabra.objects.user import GitLabracadabraUser
from gitlabracadabra.tests import my_vcr, patch
from gitlabracadabra.tests.case import TestCaseWithManager


class TestGroup(TestCaseWithManager):
    @my_vcr.use_cassette
    def test_no_create(self, cass):
        obj = GitLabracadabraGroup('memory', 'test/no_create_group', {})
        obj.process()
        self.assertTrue(cass.all_played)

    @my_vcr.use_cassette
    def test_delete(self, cass):
        obj = GitLabracadabraGroup('memory', 'delete_this_group', {'delete_object': True})
        obj.process()
        self.assertTrue(cass.all_played)

    @my_vcr.use_cassette
    def test_create(self, cass):
        obj = GitLabracadabraGroup('memory', 'test/create_group', {'create_object': True})
        obj.process()
        self.assertTrue(cass.all_played)

    @my_vcr.use_cassette
    def test_missing_parent(self, cass):
        obj = GitLabracadabraGroup('memory', 'test/missing_parent/subgroup', {'create_object': True})
        with patch('gitlabracadabra.objects.object.logger', autospec=True) as logger:
            obj.process()
            self.assertTrue(cass.all_played)
            logger.error.assert_called_once_with('[%s] NOT Creating %s (%s)',
                                                 'test/missing_parent/subgroup',
                                                 'group',
                                                 'parent namespace not found')

    @my_vcr.use_cassette
    def test_exists(self, cass):
        obj = GitLabracadabraGroup('memory', 'test/group_exists', {})
        obj.process()
        self.assertTrue(cass.all_played)

    @my_vcr.use_cassette
    def test_simple_parameters(self, cass):
        obj = GitLabracadabraGroup('memory', 'test/group_simple_parameters', {
            'name': 'group-with-simple-parameters',
            'description': 'Group with simple parameters',
            # 'membership_lock': true,  # EE-only
            # 'share_with_group_lock': true,  # EE-only
            'visibility': 'public',
            # 'file_template_project_id': 12,  # EE-only
            'lfs_enabled': False,
            'request_access_enabled': True,
            # 'shared_runners_minutes_limit': 42,  # EE, admin-only
            # 'extra_shared_runners_minutes_limit': 42,  # EE, admin-only
        })
        obj.process()
        self.assertTrue(cass.all_played)

    @my_vcr.use_cassette
    def test_members(self, cass):
        obj = GitLabracadabraGroup('memory', 'test/group_members', {
            'members': {'some_member': 'developer'},
        })
        obj.process()
        self.assertTrue(cass.all_played)

    @my_vcr.use_cassette
    def test_members_change_access_level(self, cass):
        obj = GitLabracadabraGroup('memory', 'test/group_members', {
            'members': {'some_member': 'maintainer'},
        })
        obj.process()
        self.assertTrue(cass.all_played)

    @my_vcr.use_cassette
    def test_members_not_found(self, cass):
        # Clean up
        GitLabracadabraUser._USERS_USERNAME2ID = {}
        GitLabracadabraUser._USERS_ID2USERNAME = {}
        obj = GitLabracadabraGroup('memory', 'test/group_members', {
            'members': {'member_not_found': 'maintainer'},
            'unknown_members': 'ignore',
        })
        with patch('gitlabracadabra.mixins.members.logger', autospec=True) as logger:
            obj.process()
            self.assertTrue(cass.all_played)
            logger.warning.assert_called_once_with('[%s] User not found %s',
                                                   'test/group_members', 'member_not_found')

    @my_vcr.use_cassette
    def test_members_delete_unknown(self, cass):
        obj = GitLabracadabraGroup('memory', 'test/group_members', {
            'members': {},
            'unknown_members': 'delete',
        })
        obj.process()
        self.assertTrue(cass.all_played)

    # https://github.com/python-gitlab/python-gitlab/pull/1139
    @skipIf(gitlab_version in ['1.6.0', '2.4.0'], 'python-gitlab without share group with groups')
    @my_vcr.use_cassette
    def test_groups(self, cass):
        obj = GitLabracadabraGroup('memory', 'test/group_of_groups1', {
            'groups': {'test/group1': 'developer'},
        })
        obj.process()
        self.assertTrue(cass.all_played)

    # https://github.com/python-gitlab/python-gitlab/pull/1139
    @skipIf(gitlab_version in ['1.6.0', '2.4.0'], 'python-gitlab without share group with groups')
    @my_vcr.use_cassette
    def test_groups_change_access_level(self, cass):
        obj = GitLabracadabraGroup('memory', 'test/group_of_groups2', {
            'groups': {'test/group1': 'maintainer'},
        })
        obj.process()
        self.assertTrue(cass.all_played)

    # https://github.com/python-gitlab/python-gitlab/pull/1139
    @skipIf(gitlab_version in ['1.6.0', '2.4.0'], 'python-gitlab without share group with groups')
    @my_vcr.use_cassette
    def test_groups_not_found(self, cass):
        obj = GitLabracadabraGroup('memory', 'test/group_of_groups3', {
            'groups': {'test/group_not_found': 'maintainer'},
            'unknown_groups': 'ignore',
        })
        with patch('gitlabracadabra.mixins.groups.logger', autospec=True) as logger:
            obj.process()
            self.assertTrue(cass.all_played)
            logger.warning.assert_called_once_with('[%s] Group not found %s',
                                                   'test/group_of_groups3',
                                                   'test/group_not_found')

    # https://github.com/python-gitlab/python-gitlab/pull/1139
    @skipIf(gitlab_version in ['1.6.0', '2.4.0'], 'python-gitlab without share group with groups')
    @my_vcr.use_cassette
    def test_groups_delete_unknown(self, cass):
        obj = GitLabracadabraGroup('memory', 'test/group_of_groups4', {
            'groups': {},
            'unknown_groups': 'delete',
        })
        obj.process()
        self.assertTrue(cass.all_played)

    @my_vcr.use_cassette
    def test_variables(self, cass):
        obj = GitLabracadabraGroup('memory', 'test/group_variables', {
            'variables': [
                {
                    'key': 'simple_var',
                    'value': 'simple_value',
                },
                {
                    'key': 'file_variable',
                    'value': 'BEGIN CERTIFICATE',
                    'variable_type': 'file',
                },
                {
                    'key': 'change_me',
                    'value': 'new_value',
                    'masked': False,
                    'protected': False,
                    'variable_type': 'file',
                },
            ],
            'unknown_variables': 'ignore',
        })
        obj.process()
        self.assertTrue(cass.all_played)

    # https://github.com/python-gitlab/python-gitlab/pull/847
    @skipIf(gitlab_version in ['1.6.0', '1.10.0', '1.11.0', '1.13.0'], 'python-gitlab without group labels support')
    @my_vcr.use_cassette
    def test_labels(self, cass):
        if self.gitlab_version(lt='3.2'):
            cass.requests[4].uri = 'http://localhost/api/v4/groups/24/labels?name=delete_this_group_label'
        obj = GitLabracadabraGroup('memory', 'test/group_labels', {
            'labels': [
                {
                    'name': 'new_group_label',
                    'color': 'red',
                },
                {
                    'name': 'change_this_group_label',
                    'color': 'green',
                    'description': 'New description',
                },
            ],
            'unknown_labels': 'delete',
        })
        obj.process()
        self.assertTrue(cass.all_played)

    @my_vcr.use_cassette
    def test_milestones(self, cass):
        obj = GitLabracadabraGroup('memory', 'test/group_milestones', {
            'milestones': [
                {
                    'title': 'new_milestone',
                    'description': 'New milestone',
                    'due_date': '2023-01-23',
                    'start_date': '2022-01-23',
                    # 'state': 'active',  # FIXME
                },
                {
                    'title': 'existing_milestone',
                    'description': 'New description',
                    'due_date': '',
                    'start_date': '',
                    'state': 'closed',
                },
            ],
            'unknown_milestones': 'delete',
        })
        obj.process()
        self.assertTrue(cass.all_played)
