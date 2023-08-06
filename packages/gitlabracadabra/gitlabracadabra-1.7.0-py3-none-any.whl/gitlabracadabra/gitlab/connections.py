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

from typing import Dict, List, Optional

from gitlabracadabra.gitlab.connection import GitlabConnection
from gitlabracadabra.singleton import SingletonMeta


class GitlabConnections(object, metaclass=SingletonMeta):
    """All GitLab connections by id."""

    def __init__(self) -> None:
        """All connected GitLabs.

        Intented to be used as a singleton.
        """
        self._default_id: Optional[str] = None
        self._config_files: Optional[List[str]] = None
        self._debug: bool = False
        self._connections: Dict[Optional[str], GitlabConnection] = {}

    def load(self, default_id: Optional[str], config_files: Optional[List[str]], debug: bool) -> None:
        """Load configuration.

        Args:
            default_id: Default gitlab id.
            config_files: None or list of configuration files.
            debug: True to enable debugging.
        """
        self._default_id = default_id
        self._config_files = config_files
        self._debug = debug
        self._connections = {}

    def get_connection(self, gitlab_id: Optional[str] = None, auth: bool = True) -> GitlabConnection:
        """Get a GitLab connection.

        Args:
            gitlab_id: Section in python-gitlab config files.
            auth: True to authenticate on creation.

        Returns:
            A GitLab connection.
        """
        if gitlab_id is None:
            gitlab_id = self._default_id
        if self._connections.get(gitlab_id) is None:
            self._connections[gitlab_id] = GitlabConnection(gitlab_id, self._config_files, self._debug, auth)
        return self._connections[gitlab_id]
