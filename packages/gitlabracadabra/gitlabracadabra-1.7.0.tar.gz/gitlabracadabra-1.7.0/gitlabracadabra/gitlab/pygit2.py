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

from pygit2 import UserPass

from gitlabracadabra.gitlab.pygitlab import PyGitlab


class PyGit2(PyGitlab):
    """PyGit2 wrapper."""

    @property
    def pygit2_credentials(self) -> UserPass:
        """Get PyGit2 credentials.

        Returns:
            A pygit2.UserPass.

        Raises:
            ValueError: No PyGit2 credentials.
        """
        if self._gl.private_token:
            return UserPass('oauth2', self.pygitlab.private_token)
        if self.pygitlab.oauth_token:
            return UserPass('oauth2', self.pygitlab.oauth_token)
        if self.pygitlab.job_token:
            return UserPass('gitlab-ci-token', self.pygitlab.job_token)
        if self.pygitlab.http_username:
            return UserPass(self.pygitlab.http_username, self.pygitlab.http_password)
        raise ValueError('No PyGit2 credentials')
