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

from typing import TYPE_CHECKING, Dict

from gitlab.exceptions import GitlabGetError

from requests import codes


if TYPE_CHECKING:
    from typing import Optional

    from gitlabracadabra.gitlab.pygitlab import PyGitlab


class GroupCache(object):
    """Groups mapping cache.

    indexed by id and full path.
    """

    def __init__(self, connection: PyGitlab) -> None:
        """Initialize a Python-Gitlab wrapper.

        Args:
            connection: A GitlabConnection/PyGitlab.
        """
        self._connection = connection
        self._path2id: Dict[str, Optional[int]] = {}
        self._id2path: Dict[int, Optional[str]] = {}

    def map_group(self, group_id: int, group_full_path: str) -> None:
        """Map group id and full path.

        Args:
            group_id: Group id.
            group_full_path: Group full path.
        """
        self._id2path[group_id] = group_full_path
        self._path2id[group_full_path] = group_id

    def full_path_from_id(self, group_id: int) -> Optional[str]:
        """Get group full path from id.

        Args:
            group_id: Group id.

        Returns:
            Group full path.

        Raises:
            GitlabGetError: Any HTTP error other than 404.
        """
        if group_id not in self._id2path:
            obj_manager = self._connection.pygitlab.groups
            try:
                group = obj_manager.get(group_id)
                self.map_group(group.id, group.full_path)
            except GitlabGetError as err:
                if err.response_code != codes['not_found']:
                    raise
                self._id2path[group_id] = None
        return self._id2path[group_id]

    def id_from_full_path(self, group_full_path: str) -> Optional[int]:
        """Get group id from full path.

        Args:
            group_full_path: Group full path.

        Returns:
            Group id.

        Raises:
            GitlabGetError: Any HTTP error other than 404.
        """
        if group_full_path not in self._path2id:
            obj_manager = self._connection.pygitlab.groups
            try:
                group = obj_manager.get(group_full_path)
                self.map_group(group.id, group.full_path)
            except GitlabGetError as err:
                if err.response_code != codes['not_found']:
                    raise
                self._path2id[group_full_path] = None
        return self._path2id[group_full_path]
