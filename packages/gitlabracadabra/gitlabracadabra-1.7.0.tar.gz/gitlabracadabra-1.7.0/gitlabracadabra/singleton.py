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


if TYPE_CHECKING:
    from typing import Any, Dict


class SingletonMeta(type):
    """MetaClass to implement Singleton pattern.

    Usage:
        class Registries(metaclass=SingletonMeta):
            # ...
    """

    _instances: Dict[type, object] = {}

    def __call__(cls, *args: Any, **kwargs: Dict[Any, Any]) -> object:
        """Get singleton for the calling class.

        Args:
            args: Passed to method.
            kwargs: Passed to method.

        Returns:
            The singleton.
        """
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
