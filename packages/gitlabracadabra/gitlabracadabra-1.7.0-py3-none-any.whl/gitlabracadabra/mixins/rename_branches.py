#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2019-2020 Mathieu Parent <math.parent@gmail.com>
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

import logging


logger = logging.getLogger(__name__)


class RenameBranchesMixin(object):
    """Object with branches that can be renamed."""

    """_process_rename_branches()

    Process the rename_branches param.
    """
    def _process_rename_branches(self, param_name, param_value, dry_run=False, skip_save=False):
        assert param_name == 'rename_branches'  # noqa: S101
        assert not skip_save  # noqa: S101
        for branch_pair in param_value:
            for old_name, new_name in branch_pair.items():
                if new_name not in self._get_current_branches():
                    if old_name not in self._get_current_branches():
                        logger.info('[%s] NOT Renaming branch from %s to %s (old branch not found)',
                                    self._name, old_name, new_name)
                    else:
                        self._current_branches.append(new_name)
                        self._current_branches.remove(old_name)
                        if dry_run:
                            logger.info('[%s] NOT Renaming branch from %s to %s (dry-run)',
                                        self._name, old_name, new_name)
                        else:
                            logger.info('[%s] Renaming branch from %s to %s',
                                        self._name, old_name, new_name)
                            self._obj.branches.create({
                                'branch': new_name,
                                'ref': old_name,
                            })
                            self._obj.branches.delete(old_name)
