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

from copy import deepcopy
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from typing import Dict


# Deeply update target with defaults where appropriate
def update_dict_with_defaults(target: Dict, defaults: Dict, aggregate: bool = False) -> None:
    """Merge dictionnaries.

    Args:
        target: Target dictionnary.
        defaults: Defaults dictionnary.
        aggregate: If true, lists are aggregated.
    """
    for key, value in defaults.items():
        if key in target:
            if isinstance(target[key], dict):
                update_dict_with_defaults(target[key], value, aggregate)
            elif isinstance(target[key], list) and aggregate:
                target[key] = deepcopy(value) + deepcopy(target[key])
        else:
            target[key] = deepcopy(value)
