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

from os import getenv
from pathlib import Path
from platform import system


def user_cache_dir_path() -> Path:
    """Get user cache directory.

    Returns:
        A Path object.
    """
    if system().lower() == 'windows':
        path = Path(getenv('APPDATA') or '~')
    elif system().lower() == 'darwin':
        path = Path('~') / 'Library' / 'Caches'
    else:
        path = Path(getenv('XDG_CACHE_HOME') or '~/.cache')
    return path.expanduser()


def cache_dir(subdir: str) -> Path:
    """Create a cached dir and returns its full path.

    Args:
        subdir: Subdirectory.

    Returns:
        Cache dir full path.
    """
    path = user_cache_dir_path() / 'gitlabracadabra'
    if subdir:
        path /= subdir
    path.mkdir(parents=True, exist_ok=True)
    return path
