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

import os
from unittest.mock import call, patch
from urllib.parse import quote

from pygit2 import init_repository

from gitlabracadabra.objects.project import GitLabracadabraProject
from gitlabracadabra.tests import my_vcr
from gitlabracadabra.tests.case import TestCaseWithManager


class TestProjectMirror(TestCaseWithManager):
    @my_vcr.use_cassette
    def test_mirrors_pull(self, cass):
        testrepo_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures', 'testrepo.git')
        testrepo_url = 'file://{0}'.format(testrepo_dir)
        dest_dir = str(self._temp_dir / 'dest.git')
        dest_url = 'file://{0}'.format(dest_dir)
        dest_repo = init_repository(dest_dir, bare=True)
        repo_cache_dir = str(self._temp_dir / 'cache' / 'gitlabracadabra' / quote(dest_url, safe=''))
        with patch('gitlabracadabra.mixins.mirrors.logger', autospec=True) as logger:
            with patch.object(GitLabracadabraProject, 'web_url') as web_url_mock:
                project = GitLabracadabraProject('memory', 'test/project_pull_mirror', {
                    'create_object': True,
                    'mirrors': [
                        {
                            'url': testrepo_url,
                            'direction': 'pull',
                        },
                    ],
                })

                web_url_mock.return_value = dest_url
                project.process()
                logger.debug.assert_called_once_with(
                    '[%s] Creating cache repository in %s',
                    'test/project_pull_mirror',
                    repo_cache_dir,
                )
                logger.info.assert_has_calls(
                    [
                        call(
                            '[%s] %s Pushing %s %s to %s: %s -> %s',
                            'test/project_pull_mirror',
                            testrepo_url,
                            'branch',
                            'hello',
                            'hello',
                            None,
                            '8d1fd4e584faf465d96e2f9b3cbd5000721469b3',
                        ),
                        call(
                            '[%s] %s Pushing %s %s to %s: %s -> %s',
                            'test/project_pull_mirror',
                            testrepo_url,
                            'branch',
                            'master',
                            'master',
                            None,
                            '5e8dfc288cf87620e22e67b6db671dc8a596e2f9',
                        ),
                        call(
                            '[%s] %s Pushing %s %s to %s: %s -> %s',
                            'test/project_pull_mirror',
                            testrepo_url,
                            'tag',
                            'tag1',
                            'tag1',
                            None,
                            '8d1fd4e584faf465d96e2f9b3cbd5000721469b3',
                        ),
                        call(
                            '[%s] %s Pushing %s %s to %s: %s -> %s',
                            'test/project_pull_mirror',
                            testrepo_url,
                            'tag',
                            'tag2',
                            'tag2',
                            None,
                            '5e8dfc288cf87620e22e67b6db671dc8a596e2f9',
                        ),
                    ],
                    any_order=True,
                )
        self.assertEqual(
            list(dest_repo.references),
            ['refs/heads/hello', 'refs/heads/master', 'refs/tags/tag1', 'refs/tags/tag2'],
        )
        self.assertTrue(cass.all_played)

    @my_vcr.use_cassette
    def test_mirrors_pull_mappings(self, cass):
        testrepo_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures', 'testrepo.git')
        testrepo_url = 'file://{0}'.format(testrepo_dir)
        dest_dir = str(self._temp_dir / 'dest2.git')
        dest_url = 'file://{0}'.format(dest_dir)
        dest_repo = init_repository(dest_dir, bare=True)
        repo_cache_dir = str(self._temp_dir / 'cache' / 'gitlabracadabra' / quote(dest_url, safe=''))
        with patch('gitlabracadabra.mixins.mirrors.logger', autospec=True) as logger:
            with patch.object(GitLabracadabraProject, 'web_url') as web_url_mock:
                project = GitLabracadabraProject('memory', 'test/project_pull_mirror', {
                    'create_object': True,
                    'mirrors': [
                        {
                            'url': testrepo_url,
                            'direction': 'pull',
                            'branches': [
                                {
                                    'from': 'hello',
                                    'to': 'world',
                                },
                                {
                                    'from': '/(.*)/',
                                    'to': r'upstream/\1',
                                },
                            ],
                            'tags': [
                                {
                                    'from': '/(.*1)/',
                                    'to': r'upstream-\1',
                                },
                            ],
                        },
                    ],
                })

                web_url_mock.return_value = dest_url
                project.process()
                logger.debug.assert_called_once_with(
                    '[%s] Creating cache repository in %s',
                    'test/project_pull_mirror',
                    repo_cache_dir,
                )
                logger.info.assert_has_calls(
                    [
                        call(
                            '[%s] %s Pushing %s %s to %s: %s -> %s',
                            'test/project_pull_mirror',
                            testrepo_url,
                            'branch',
                            'hello',
                            'world',
                            None,
                            '8d1fd4e584faf465d96e2f9b3cbd5000721469b3',
                        ),
                        call(
                            '[%s] %s Pushing %s %s to %s: %s -> %s',
                            'test/project_pull_mirror',
                            testrepo_url,
                            'branch',
                            'master',
                            'upstream/master',
                            None,
                            '5e8dfc288cf87620e22e67b6db671dc8a596e2f9',
                        ),
                        call(
                            '[%s] %s Pushing %s %s to %s: %s -> %s',
                            'test/project_pull_mirror',
                            testrepo_url,
                            'tag',
                            'tag1',
                            'upstream-tag1',
                            None,
                            '8d1fd4e584faf465d96e2f9b3cbd5000721469b3',
                        ),
                    ],
                    any_order=True,
                )
        self.assertEqual(
            list(dest_repo.references),
            ['refs/heads/upstream/master', 'refs/heads/world', 'refs/tags/upstream-tag1'],
        )
        self.assertTrue(cass.all_played)
