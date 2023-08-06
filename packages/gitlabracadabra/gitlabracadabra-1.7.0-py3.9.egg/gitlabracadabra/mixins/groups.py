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

import logging
from copy import deepcopy

from gitlabracadabra.gitlab.access_levels import access_level


logger = logging.getLogger(__name__)


class GroupsMixin(object):
    """Object with groups."""

    """_process_groups()

    Process the groups param.
    """
    def _process_groups(self, param_name, param_value, dry_run=False, skip_save=False):
        assert param_name == 'groups'  # noqa: S101
        assert not skip_save  # noqa: S101
        if not hasattr(self._obj, 'shared_with_groups'):
            logger.error('[%s] Unable to share with groups: %s',
                         self._name, 'share group with groups requires GitLab >= 13.1.0')
            return
        if not hasattr(self._obj, 'share'):
            # https://github.com/python-gitlab/python-gitlab/pull/1139
            logger.error('[%s] Unable to share with groups: %s',
                         self._name, 'share group with groups requires python-gitlab >= 2.5.0')
            return
        param_value = deepcopy(param_value)
        unknown_groups = self._content.get('unknown_groups', 'warn')
        # We first check for already shared groups
        for group in self._obj.shared_with_groups:
            if 'group_full_path' not in group:
                # Gitlab < 11.8
                # https://gitlab.com/gitlab-org/gitlab-ce/merge_requests/24052
                group['group_full_path'] = self.connection.group_cache.full_path_from_id(group['group_id'])
            self.connection.group_cache.map_group(group['group_id'], group['group_full_path'])
            if group['group_full_path'] in param_value.keys():
                target_access_level = access_level(param_value[group['group_full_path']])
                if group['group_access_level'] != target_access_level:
                    if dry_run:
                        logger.info('[%s] NOT Changing group %s access level: %s -> %s (dry-run)',
                                    self._name, group['group_full_path'],
                                    group['group_access_level'], target_access_level)
                    else:
                        logger.info('[%s] Changing group %s access level: %s -> %s',
                                    self._name, group['group_full_path'],
                                    group['group_access_level'], target_access_level)
                        self._obj.unshare(group['group_id'])
                        self._obj.share(group['group_id'], target_access_level)
                param_value.pop(group['group_full_path'])
            else:
                if unknown_groups in ['delete', 'remove']:
                    if dry_run:
                        logger.info('[%s] NOT Unsharing from unknown group: %s (dry-run)',
                                    self._name, group['group_full_path'])
                    else:
                        logger.info('[%s] Unsharing from unknown group: %s',
                                    self._name, group['group_full_path'])
                        self._obj.unshare(group['group_id'])
                elif unknown_groups not in ['ignore', 'skip']:
                    logger.warning('[%s] NOT Unsharing from unknown group: %s (unknown_groups=%s)',
                                   self._name, group['group_full_path'], unknown_groups)
        # Remaining groups
        for group_full_path, target_group_access in sorted(param_value.items()):
            group_id = self.connection.group_cache.id_from_full_path(group_full_path)
            if group_id is None:
                logger.warning('[%s] Group not found %s',
                               self._name, group_full_path)
                continue
            target_access_level = access_level(target_group_access)
            if dry_run:
                logger.info('[%s] NOT Sharing group %s: %s -> %s (dry-run)',
                            self._name, group_full_path,
                            0, target_access_level)
            else:
                logger.info('[%s] Sharing group %s: %s -> %s',
                            self._name, group_full_path,
                            0, target_access_level)
                self._obj.share(group_id, target_access_level)
