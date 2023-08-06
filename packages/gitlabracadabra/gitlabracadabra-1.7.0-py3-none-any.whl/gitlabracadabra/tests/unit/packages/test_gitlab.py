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

from unittest.mock import MagicMock, call, patch

from gitlabracadabra.gitlab.connections import GitlabConnections
from gitlabracadabra.packages.gitlab import Gitlab
from gitlabracadabra.packages.package_file import PackageFile
from gitlabracadabra.packages.raw import RawSource
from gitlabracadabra.tests import my_vcr
from gitlabracadabra.tests.case import TestCaseWithManager


class TestGitlab(TestCaseWithManager):
    """Test Gitlab class."""

    def test_head_url_raw(self):
        """Test head_url method, with raw package file."""
        gitlab_connection = MagicMock()
        gitlab_connection.api_url = 'https://gitlab.example.org/api/v4'
        project_id = 42
        gitlab = Gitlab(connection=gitlab_connection, full_path='group/project', project_id=project_id)

        self.assertEqual(
            gitlab.head_url(PackageFile('https://source.example.org/foobar.gz', 'raw', 'pkg', 'v1')),
            'https://gitlab.example.org/api/v4/projects/group%2Fproject/packages/generic/pkg/v1/foobar.gz',
        )

        self.assertEqual(
            gitlab.head_url(PackageFile('https://source.example.org/foobar.gz', 'raw', 'with/slash', 'with/slash', 'foo/barré')),  # noqa: E501
            'https://gitlab.example.org/api/v4/projects/group%2Fproject/packages/generic/with%2Fslash/with%2Fslash/foo%2Fbarr%C3%A9',  # noqa: E501
        )

    @my_vcr.use_cassette
    def test_import_source(self, cass):
        """Test import_source method.

        Args:
            cass: VCR cassette.
        """
        with patch('gitlabracadabra.packages.destination.logger', autospec=True) as logger:
            connection = GitlabConnections().get_connection(None)
            project_id = 42
            gitlab = Gitlab(connection=connection, full_path='test/test_from_raw', project_id=project_id)
            source = RawSource(
                default_url='https://download.docker.com/linux/debian/gpg',
                default_package_name='docker',
            )
            gitlab.import_source(source, dry_run=False)
            self.assertEqual(logger.mock_calls, [
                call.info(
                    '%sUploading %s package file "%s" from "%s" version %s (%s)',
                    '[test/test_from_raw] ',
                    'raw',
                    'gpg',
                    'docker',
                    '0',
                    'https://download.docker.com/linux/debian/gpg',
                ),
            ])
        self.assertTrue(cass.all_played)
