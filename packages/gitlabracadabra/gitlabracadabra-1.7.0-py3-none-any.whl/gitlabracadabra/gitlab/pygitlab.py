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


from __future__ import annotations

from typing import TYPE_CHECKING

from gitlab import Gitlab

from requests.auth import HTTPBasicAuth

from gitlabracadabra.auth_info import AuthInfo
from gitlabracadabra.gitlab.group_cache import GroupCache
from gitlabracadabra.gitlab.user_cache import UserCache


if TYPE_CHECKING:
    from typing import List, Optional


class PyGitlab(object):
    """Python-Gitlab wrapper."""

    def __init__(
        self,
        gitlab_id: Optional[str],
        config_files: Optional[List[str]],
        debug: bool,
        auth: bool = True,
    ) -> None:
        """Initialize a Python-Gitlab wrapper.

        Args:
            gitlab_id: Section in python-gitlab config files.
            config_files: None or list of configuration files.
            debug: True to enable debugging.
            auth: True to authenticate on creation.
        """
        self._gitlab_id = gitlab_id
        self._config_files = config_files
        self._debug = debug
        self._gl = Gitlab.from_config(self.gitlab_id, self._config_files)
        if auth:
            if self.pygitlab.private_token or self.pygitlab.oauth_token:
                self.pygitlab.auth()
        if self._debug:
            self.pygitlab.enable_debug()

        self.group_cache = GroupCache(self)
        self.user_cache = UserCache(self)

    @property
    def gitlab_id(self) -> Optional[str]:
        """Get Gitlab id (section in python-gitlab config files).

        Returns:
            A string.
        """
        return self._gitlab_id

    @property
    def pygitlab(self) -> Gitlab:
        """Get python-gitlab object.

        Returns:
            A gitlab.Gitlab object.
        """
        return self._gl

    @property
    def registry_auth_info(self) -> AuthInfo:
        """Get Registry Authentication information.

        Returns:
            A dict, with 'headers' and 'auth' to pass to requests.

        Raises:
            ValueError: No auth info.
        """
        if self.pygitlab.private_token:
            return AuthInfo(auth=HTTPBasicAuth('personal-access-token', self.pygitlab.private_token))
        if self.pygitlab.oauth_token:
            return AuthInfo(auth=HTTPBasicAuth('oauth2', self.pygitlab.oauth_token))
        if self.pygitlab.job_token:
            return AuthInfo(auth=HTTPBasicAuth('gitlab-ci-token', self.pygitlab.job_token))
        if self.pygitlab.http_username:
            return AuthInfo(auth=HTTPBasicAuth(self.pygitlab.http_username, self.pygitlab.http_password))
        raise ValueError('No auth info')

    @property
    def api_url(self) -> str:
        """Get API URL.

        Returns:
            API URL.
        """
        return self.pygitlab.api_url
