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

from types import MappingProxyType
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from typing import Optional


LEVELS = MappingProxyType({
    'noone': 0,
    'guest': 10,
    'reporter': 20,
    'developer': 30,
    'maintainer': 40,
    'owner': 50,
})


def access_level(level: str) -> Optional[int]:
    """Convert access level to int.

    Args:
        level: Access level as str.

    Returns:
        Access level as int, or None.
    """
    return LEVELS.get(level, None)
