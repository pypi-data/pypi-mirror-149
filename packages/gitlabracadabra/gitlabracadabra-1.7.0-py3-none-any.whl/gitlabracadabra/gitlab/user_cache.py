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


class UserCache(object):
    """Users mapping cache.

    indexed by id and username.
    """

    def __init__(self, connection: PyGitlab) -> None:
        """Initialize a Python-Gitlab wrapper.

        Args:
            connection: A GitlabConnection/PyGitlab.
        """
        self._connection = connection
        self._username2id: Dict[str, Optional[int]] = {}
        self._id2username: Dict[int, Optional[str]] = {}

    def map_user(self, user_id: int, user_username: str) -> None:
        """Map user id and username.

        Args:
            user_id: User id.
            user_username: User username.
        """
        self._id2username[user_id] = user_username
        self._username2id[user_username] = user_id

    def username_from_id(self, user_id: int) -> Optional[str]:
        """Get user username from id.

        Args:
            user_id: User id.

        Returns:
            User username.

        Raises:
            GitlabGetError: Any HTTP error other than 404.
        """
        if user_id not in self._id2username:
            obj_manager = self._connection.pygitlab.users
            try:
                user = obj_manager.get(user_id)
                self.map_user(user.id, user.username)
            except GitlabGetError as err:
                if err.response_code != codes['not_found']:
                    raise
                self._id2username[user_id] = None
        return self._id2username[user_id]

    def id_from_username(self, user_username: str) -> Optional[int]:
        """Get user id from username.

        Args:
            user_username: User username.

        Returns:
            User id.
        """
        if user_username not in self._username2id:
            obj_manager = self._connection.pygitlab.users
            try:
                user = list(obj_manager.list(username=user_username))[0]
                self.map_user(user.id, user.username)
            except IndexError:
                self._username2id[user_username] = None
        return self._username2id[user_username]
