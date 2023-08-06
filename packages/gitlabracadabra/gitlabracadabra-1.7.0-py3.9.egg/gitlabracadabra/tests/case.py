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

from pathlib import Path
from shutil import rmtree
from tempfile import mkdtemp
from typing import Optional
from unittest import TestCase as BaseTestCase
from unittest.mock import MagicMock, patch

from gitlab import __version__ as gitlab_version

from packaging import version

from gitlabracadabra.containers.registries import Registries
from gitlabracadabra.gitlab.connections import GitlabConnections


class TestCase(BaseTestCase):
    """TestCase."""

    def setUp(self) -> None:
        """Test setup.

        Create temporary directory, and mock user_cache_dir_path().
        """
        super().setUp()

        Registries().reset()

        self._temp_dir = Path(mkdtemp())
        self._user_cache_dir_path_mock = MagicMock()
        self._user_cache_dir_path_mock.return_value = self._temp_dir / 'cache'
        self._user_cache_dir_path_patch = patch(
            'gitlabracadabra.disk_cache.user_cache_dir_path',
            self._user_cache_dir_path_mock,
        )
        self._user_cache_dir_path_patch.start()

    def tearDown(self) -> None:
        """Test teardown.

        Delete temporary directory, and mock user_cache_dir_path().
        """
        self._user_cache_dir_path_patch.stop()
        rmtree(self._temp_dir)
        super().tearDown()

    @classmethod
    def gitlab_version(cls, ge: Optional[str] = None, lt: Optional[str] = None) -> bool:
        """Compare python-gitlab version.

        Args:
            ge: Returns true when python-gitlab version is greater or equal to this version.
            lt: Returns true when python-gitlab version is lower than this version.

        Returns:
            A boolean.
        """
        gitlab_version_parsed = version.parse(gitlab_version)
        ret = True
        if ge:
            ge_parsed = version.parse(ge)
            ret = ret and gitlab_version_parsed >= ge_parsed
        if lt:
            lt_parsed = version.parse(lt)
            ret = ret and gitlab_version_parsed < lt_parsed
        return ret


class TestCaseWithManager(TestCase):
    """TestCase with GitLab connection."""

    def setUp(self) -> None:
        """Test setup.

        Inject a GitLab connection.
        """
        super().setUp()
        pygitlab_config = str((Path(__file__).parent / 'python-gitlab.cfg').absolute())
        GitlabConnections().load(default_id='localhost', config_files=[pygitlab_config], debug=False)
        GitlabConnections().get_connection(None, auth=False)

    def tearDown(self) -> None:
        """Test teardown.

        Prune the GitLab connections.
        """
        GitlabConnections().load(default_id=None, config_files=None, debug=False)
        super().tearDown()
