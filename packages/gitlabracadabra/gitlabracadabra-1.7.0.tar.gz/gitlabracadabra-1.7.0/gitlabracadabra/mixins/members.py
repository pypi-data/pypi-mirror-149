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

from gitlab.exceptions import GitlabDeleteError

from gitlabracadabra.gitlab.access_levels import access_level


logger = logging.getLogger(__name__)


class MembersMixin(object):
    """Object with members."""

    """_process_members()

    Process the members param.
    """
    def _process_members(self, param_name, param_value, dry_run=False, skip_save=False):
        assert param_name == 'members'  # noqa: S101
        assert not skip_save  # noqa: S101
        param_value = deepcopy(param_value)
        unknown_members = self._content.get('unknown_members', 'warn')
        current_members = dict([[member.username, member] for member in self._obj.members.list(all=True)])
        # We first check for already existing members
        for _member_username, member in sorted(current_members.items()):
            self.connection.user_cache.map_user(member.id, member.username)
            if member.username in param_value.keys():
                target_access_level = access_level(param_value[member.username])
                if member.access_level != target_access_level:
                    if dry_run:
                        logger.info('[%s] NOT Changing user %s (%s) access level: %s -> %s (dry-run)',
                                    self._name, member.username, member.name,
                                    member.access_level, target_access_level)
                    else:
                        logger.info('[%s] Changing user %s (%s) access level: %s -> %s',
                                    self._name, member.username, member.name,
                                    member.access_level, target_access_level)
                        member.access_level = target_access_level
                        member.save()
                param_value.pop(member.username)
            else:
                if unknown_members in ['delete', 'remove']:
                    if dry_run:
                        logger.info('[%s] NOT Removing member %s (%s) (dry-run)',
                                    self._name, member.username, member.name)
                    else:
                        logger.info('[%s] Removing member %s (%s)',
                                    self._name, member.username, member.name)
                        try:
                            member.delete()
                        except GitlabDeleteError as e:
                            logger.warning('[%s] Unable to remove member %s (%s): %s',
                                           self._name, member.username, member.name, e.error_message)
                elif unknown_members not in ['ignore', 'skip']:
                    logger.warning('[%s] NOT Removing member: %s (%s)',
                                   self._name, member.username, member.name)
        # Remaining members
        for target_username, target_user_access in sorted(param_value.items()):
            user_id = self.connection.user_cache.id_from_username(target_username)
            if user_id is None:
                logger.warning('[%s] User not found %s',
                               self._name, target_username)
                continue
            target_access_level = access_level(target_user_access)
            if dry_run:
                logger.info('[%s] NOT Adding user %s: %s -> %s (dry-run)',
                            self._name, target_username, 0, target_access_level)
            else:
                logger.info('[%s] Adding user %s: %s -> %s',
                            self._name, target_username, 0, target_access_level)
                self._obj.members.create({
                    'user_id': user_id,
                    'access_level': target_access_level,
                })
