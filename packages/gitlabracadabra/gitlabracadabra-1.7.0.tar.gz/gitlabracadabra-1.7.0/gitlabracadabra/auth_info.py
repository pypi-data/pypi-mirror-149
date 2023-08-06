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

from typing import Dict, Optional

from requests.auth import AuthBase


class AuthInfo(object):
    """Authentication information."""

    headers: Optional[Dict[str, str]]
    auth: Optional[AuthBase]

    def __init__(
        self,
        headers: Optional[Dict[str, str]] = None,
        auth: Optional[AuthBase] = None,
    ) -> None:
        """Instanciate an Authentication information.

        Args:
            headers: Dict of headers.
            auth: AuthBase object.
        """
        self.headers = headers
        self.auth = auth
