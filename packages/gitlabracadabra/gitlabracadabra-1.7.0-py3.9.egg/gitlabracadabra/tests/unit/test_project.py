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
from gitlabracadabra.objects.user import GitLabracadabraUser
from gitlabracadabra.tests import my_vcr, patch
from gitlabracadabra.tests.case import TestCaseWithManager


class TestProject(TestCaseWithManager):
    @my_vcr.use_cassette
    def test_no_create(self, cass):
        obj = GitLabracadabraProject('memory', 'test/no_create_object', {})
        obj.process()
        self.assertTrue(cass.all_played)

    @my_vcr.use_cassette
    def test_create(self, cass):
        obj = GitLabracadabraProject('memory', 'test/create_object', {'create_object': True})
        obj.process()
        self.assertTrue(cass.all_played)

    @my_vcr.use_cassette
    def test_delete(self, cass):
        obj = GitLabracadabraProject('memory', 'test/delete_me', {'delete_object': True})
        obj.process()
        self.assertTrue(cass.all_played)

    @my_vcr.use_cassette
    def test_exists(self, cass):
        obj = GitLabracadabraProject('memory', 'test/exists', {})
        obj.process()
        self.assertTrue(cass.all_played)

    @my_vcr.use_cassette
    def test_simple_parameters(self, cass):
        obj = GitLabracadabraProject('memory', 'test/project_simple_parameters', {
            'name': 'project-with-simple-parameters',
            'description': 'Project with simple parameters',
            'issues_enabled': False,
            'merge_requests_enabled': False,
            'jobs_enabled': False,
            'wiki_enabled': False,
            'snippets_enabled': False,
            'resolve_outdated_diff_discussions': True,
            'container_registry_enabled': False,
            'shared_runners_enabled': False,
            'visibility': 'public',
            # 'import_url': 'http://example.com/foo.git',  # FIXME
            # 'public_builds': False,  # FIXME
            'only_allow_merge_if_pipeline_succeeds': True,
            'only_allow_merge_if_all_discussions_are_resolved': True,
            'merge_method': 'ff',
            # 'remove_source_branch_after_merge': False, # TODO
            'lfs_enabled': False,
            'request_access_enabled': True,
            'tag_list': ['foo', 'bar'],
            # 'avatar': 'http://example.com/foo.png',  # FIXME
            'printing_merge_request_link_enabled': False,
            'ci_config_path': 'debian/gitlab-ci.yml',
            # 'repository_storage': 'foo',  # EE
            # 'approvals_before_merge': False,  # EE
            # 'external_authorization_classification_label': 'foo',  # EE
            # 'mirror': False,  # EE
            # 'mirror_user_id': 2,  # EE
            # 'mirror_trigger_builds': False,  # EE
            # 'only_mirror_protected_branches': True,  # EE
            # 'mirror_overwrites_diverged_branches': True,  # EE
            # 'packages_enabled': True,  # EE
        })
        obj.process()
        self.assertTrue(cass.all_played)

    @my_vcr.use_cassette
    def test_simple_parameters2(self, cass):
        obj = GitLabracadabraProject('memory', 'test/project_simple_parameters2', {
            'issues_access_level': 'private',
            'repository_access_level': 'private',
            'merge_requests_access_level': 'private',
            'builds_access_level': 'private',
            'wiki_access_level': 'private',
            'snippets_access_level': 'private',
            'build_git_strategy': 'clone',
            'build_timeout': 7200,
            'auto_cancel_pending_pipelines': 'disabled',
            'build_coverage_regex': '^TOTAL\\s+\\d+\\s+\\d+\\s+(\\d+\\%)$',
            'ci_default_git_depth': 100,
            'auto_devops_enabled': False,
            'auto_devops_deploy_strategy': 'timed_incremental',
        })
        obj.process()
        self.assertTrue(cass.all_played)

    @my_vcr.use_cassette
    def test_default_branch_exists(self, cass):
        obj = GitLabracadabraProject('memory', 'test/project_default_branch', {
            'default_branch': 'exists',
        })
        obj.process()
        self.assertTrue(cass.all_played)

    @my_vcr.use_cassette
    def test_default_branch_not_exists(self, cass):
        obj = GitLabracadabraProject('memory', 'test/project_default_branch', {
            'default_branch': 'not_exists',
        })
        with patch('gitlabracadabra.objects.object.logger', autospec=True) as logger:
            obj.process()
            self.assertTrue(cass.all_played)
            logger.error.assert_called_once_with('[%s] Unable to change param %s (%s -> %s): %s',
                                                 'test/project_default_branch',
                                                 'default_branch',
                                                 'exists',
                                                 'not_exists',
                                                 {'base': [
                                                  "Could not change HEAD: branch 'not_exists' does not exist"]})

    @my_vcr.use_cassette
    def test_branches(self, cass):
        obj = GitLabracadabraProject('memory', 'test/project_branches', {
            'branches': ['a', 'b', 'c'],

        })
        obj.process()
        self.assertTrue(cass.all_played)

    @my_vcr.use_cassette
    def test_groups(self, cass):
        obj = GitLabracadabraProject('memory', 'test/project_groups', {
            'groups': {'test2': 'developer'},
        })
        obj.process()
        self.assertTrue(cass.all_played)

    @my_vcr.use_cassette
    def test_groups_change_access_level(self, cass):
        obj = GitLabracadabraProject('memory', 'test/project_groups', {
            'groups': {'test2': 'maintainer'},
        })
        obj.process()
        self.assertTrue(cass.all_played)

    @my_vcr.use_cassette
    def test_groups_not_found(self, cass):
        obj = GitLabracadabraProject('memory', 'test/project_groups', {
            'groups': {'group_not_found': 'maintainer'},
            'unknown_groups': 'ignore',
        })
        with patch('gitlabracadabra.mixins.groups.logger', autospec=True) as logger:
            obj.process()
            self.assertTrue(cass.all_played)
            logger.warning.assert_called_once_with('[%s] Group not found %s',
                                                   'test/project_groups',
                                                   'group_not_found')

    @my_vcr.use_cassette
    def test_groups_delete_unknown(self, cass):
        obj = GitLabracadabraProject('memory', 'test/project_groups', {
            'groups': {},
            'unknown_groups': 'delete',
        })
        obj.process()
        self.assertTrue(cass.all_played)

    @my_vcr.use_cassette
    def test_members(self, cass):
        # Clean up
        GitLabracadabraUser._USERS_USERNAME2ID = {}
        GitLabracadabraUser._USERS_ID2USERNAME = {}
        obj = GitLabracadabraProject('memory', 'test/project_members', {
            'members': {'some_member': 'developer'},
        })
        obj.process()
        self.assertTrue(cass.all_played)

    @my_vcr.use_cassette
    def test_members_change_access_level(self, cass):
        obj = GitLabracadabraProject('memory', 'test/project_members', {
            'members': {'some_member': 'maintainer'},
        })
        obj.process()
        self.assertTrue(cass.all_played)

    @my_vcr.use_cassette
    def test_members_not_found(self, cass):
        # Clean up
        GitLabracadabraUser._USERS_USERNAME2ID = {}
        GitLabracadabraUser._USERS_ID2USERNAME = {}
        obj = GitLabracadabraProject('memory', 'test/project_members', {
            'members': {'member_not_found': 'maintainer'},
            'unknown_members': 'ignore',
        })
        with patch('gitlabracadabra.mixins.members.logger', autospec=True) as logger:
            obj.process()
            self.assertTrue(cass.all_played)
            logger.warning.assert_called_once_with('[%s] User not found %s',
                                                   'test/project_members', 'member_not_found')

    @my_vcr.use_cassette
    def test_members_delete_unknown(self, cass):
        obj = GitLabracadabraProject('memory', 'test/project_members', {
            'members': {},
            'unknown_members': 'delete',
        })
        obj.process()
        self.assertTrue(cass.all_played)

    @my_vcr.use_cassette
    def test_protected_branches_wildcard(self, cass):
        obj = GitLabracadabraProject('memory', 'test/protected_branches', {
            'protected_branches': {'release/*': {'push_access_level': 'noone', 'merge_access_level': 'maintainer'}},
        })
        with patch('gitlabracadabra.objects.project.logger', autospec=True) as logger:
            obj.process()
            self.assertTrue(cass.all_played)
            logger.warning.assert_called_once_with('[%s] NOT Deleting unknown protected branch: %s'
                                                   ' (unknown_protected_branches=%s)',
                                                   'test/protected_branches', 'master', 'warn')

    @my_vcr.use_cassette
    def test_protected_branches_delete(self, cass):
        obj = GitLabracadabraProject('memory', 'test/protected_branches', {
            'protected_branches': {},
            'unknown_protected_branches': 'delete',
        })
        with patch('gitlabracadabra.objects.project.logger', autospec=True) as logger:
            obj.process()
            self.assertTrue(cass.all_played)
            logger.info.assert_called_once_with('[%s] Deleting unknown protected branch: %s',
                                                'test/protected_branches', 'master')

    @skipIf(gitlab_version in ['1.6.0'], 'python-gitlab without protected tags support')
    @my_vcr.use_cassette
    def test_protected_tags_wildcard(self, cass):
        obj = GitLabracadabraProject('memory', 'test/protected_tags', {
            'protected_tags': {'v*': 'maintainer'},
        })
        with patch('gitlabracadabra.objects.project.logger', autospec=True) as logger:
            obj.process()
            self.assertTrue(cass.all_played)
            logger.info.assert_called_once_with('[%s] Changing protected tag %s access level: %s -> %s',
                                                'test/protected_tags', 'v*',
                                                {}, {'name': 'v*', 'create_access_level': 40})

    @skipIf(gitlab_version in ['1.6.0'], 'python-gitlab without protected tags support')
    @my_vcr.use_cassette
    def test_protected_tags_change(self, cass):
        if self.gitlab_version(lt='3.0'):
            cass.requests[2].uri = 'http://localhost/api/v4/projects/19/protected_tags/v1%2E0'
        obj = GitLabracadabraProject('memory', 'test/protected_tags', {
            'protected_tags': {'v1.0': 'maintainer'},
        })
        with patch('gitlabracadabra.objects.project.logger', autospec=True) as logger:
            obj.process()
            self.assertTrue(cass.all_played)
            logger.info.assert_called_once_with('[%s] Changing protected tag %s access level: %s -> %s',
                                                'test/protected_tags', 'v1.0',
                                                {'name': 'v1.0', 'create_access_level': 30},
                                                {'name': 'v1.0', 'create_access_level': 40})

    @skipIf(gitlab_version in ['1.6.0'], 'python-gitlab without protected tags support')
    @my_vcr.use_cassette
    def test_protected_tags_delete(self, cass):
        obj = GitLabracadabraProject('memory', 'test/protected_tags', {
            'protected_tags': {},
            'unknown_protected_tags': 'delete',
        })
        with patch('gitlabracadabra.objects.project.logger', autospec=True) as logger:
            obj.process()
            self.assertTrue(cass.all_played)
            logger.info.assert_called_once_with('[%s] Deleting unknown protected tag: %s',
                                                'test/protected_tags', 'unknown')

    @my_vcr.use_cassette
    def test_archived(self, cass):
        obj = GitLabracadabraProject('memory', 'test/archived', {
            'archived': True,
        })
        with patch('gitlabracadabra.objects.project.logger', autospec=True) as logger:
            obj.process()
            self.assertTrue(cass.all_played)
            logger.info.assert_called_once_with('[%s] Changing param %s: %s -> %s',
                                                'test/archived', 'archived', False, True)

    @my_vcr.use_cassette
    def test_unarchived(self, cass):
        obj = GitLabracadabraProject('memory', 'test/unarchived', {
            'archived': False,
        })
        with patch('gitlabracadabra.objects.project.logger', autospec=True) as logger:
            obj.process()
            self.assertTrue(cass.all_played)
            logger.info.assert_called_once_with('[%s] Changing param %s: %s -> %s',
                                                'test/unarchived', 'archived', True, False)

    @my_vcr.use_cassette
    def test_variables(self, cass):
        obj = GitLabracadabraProject('memory', 'test/project_variables', {
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

    @skipIf(gitlab_version in ['1.11.0', '1.13.0'], 'python-gitlab without proper project labels support')
    @my_vcr.use_cassette
    def test_labels(self, cass):
        if self.gitlab_version(lt='3.2'):
            cass.requests[4].uri = 'http://localhost/api/v4/projects/33/labels?name=delete_me'
        obj = GitLabracadabraProject('memory', 'test/project_labels', {
            'labels': [
                {
                    'name': 'new_label',
                    'color': 'red',
                },
                {
                    'name': 'change_me',
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
        obj = GitLabracadabraProject('memory', 'test/project_milestones', {
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

    @my_vcr.use_cassette
    def test_webhooks(self, cass):
        obj = GitLabracadabraProject('memory', 'test/test_webhooks', {
            'webhooks': [
                {
                    'url': 'http://example.com/create_me',
                    'push_events': False,
                    'push_events_branch_filter': 'master',
                    'issues_events': True,
                    'confidential_issues_events': True,
                    'merge_requests_events': True,
                    'tag_push_events': True,
                    'note_events': True,
                    'confidential_note_events': True,
                    'job_events': True,
                    'pipeline_events': True,
                    'wiki_page_events': True,
                    'enable_ssl_verification': False,
                    # 'repository_update_events': True,
                },
                {
                    'url': 'http://example.com/modify_me',
                    'push_events': False,
                    'push_events_branch_filter': 'master',
                    'issues_events': True,
                    'confidential_issues_events': True,
                    'merge_requests_events': True,
                    'tag_push_events': True,
                    'note_events': True,
                    'confidential_note_events': True,
                    'job_events': True,
                    'pipeline_events': True,
                    'wiki_page_events': True,
                    'enable_ssl_verification': False,
                    # 'repository_update_events': True,
                },
            ],
            'unknown_webhooks': 'delete',
        })
        obj.process()
        self.assertTrue(cass.all_played)

    @my_vcr.use_cassette
    def test_container_expiration_policy(self, cass):
        obj = GitLabracadabraProject('memory', 'test/container_expiration_policy', {
            'container_expiration_policy': {
                'enabled': True,
                'cadence': '14d',
                'keep_n': 25,
                'name_regex_keep': '.*master|.*release|release-.*|master-.*',
                'older_than': '90d',
                'name_regex_delete': '.*',
            },
        })
        obj.process()
        self.assertTrue(cass.all_played)

    @my_vcr.use_cassette
    def test_pipeline_schedules(self, cass):
        obj = GitLabracadabraProject('memory', 'test/test_pipeline_schedules', {
            'pipeline_schedules': [
                {
                    'description': 'create_me',
                    'ref': 'master',
                    'cron': '0 1 * * 5',
                    'cron_timezone': 'UTC',
                    'active': True,
                },
                {
                    'description': 'modify_me',
                    'ref': 'develop',
                    'cron': '0 3 * * 5',
                    'cron_timezone': 'Pacific Time (US & Canada)',
                    'active': False,
                },
            ],
            'unknown_pipeline_schedules': 'delete',
            'unknown_pipeline_schedule_variables': 'ignore',
        })
        obj.process()
        self.assertTrue(cass.all_played)

    @my_vcr.use_cassette
    def test_pipeline_schedule_variables(self, cass):
        obj = GitLabracadabraProject('memory', 'test/test_pipeline_schedule_variables', {
            'pipeline_schedules': [
                {
                    'description': 'some_schedule',
                    'ref': 'master',
                    'cron': '0 16 * * *',
                    'cron_timezone': 'UTC',
                    'active': False,
                    'variables': [
                        {
                            'key': 'create_me',
                            'value': 'some_value',
                            'variable_type': 'file',
                        },
                        {
                            'key': 'modify_me',
                            'value': 'new_value',
                            'variable_type': 'file',
                        },
                    ],
                },
            ],
            'unknown_pipeline_schedules': 'delete',
            'unknown_pipeline_schedule_variables': 'delete',
        })
        obj.process()
        self.assertTrue(cass.all_played)
