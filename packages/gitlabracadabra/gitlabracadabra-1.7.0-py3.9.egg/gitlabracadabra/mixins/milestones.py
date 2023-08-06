#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Mathieu Parent <math.parent@gmail.com>
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


logger = logging.getLogger(__name__)


class MilestonesMixin(object):
    """Object with milestones."""

    """_process_milestones()

    Process the milestones param.
    """
    def _process_milestones(self, param_name, param_value, dry_run=False, skip_save=False):
        assert param_name == 'milestones'  # noqa: S101
        assert not skip_save  # noqa: S101
        unknown_milestones = self._content.get('unknown_milestones', 'warn')
        try:
            current_milestones = dict([[current_milestone.title, current_milestone]
                                      for current_milestone in self._obj.milestones.list(all=True)])
        except AttributeError:
            # https://github.com/python-gitlab/python-gitlab/pull/847
            logger.error('[%s] Unable to manage milestones: %s',
                         self._name, 'group milestones requires python-gitlab >= 1.1.0')
            return
        target_milestones = dict([[target_milestone['title'], deepcopy(target_milestone)]
                                 for target_milestone in param_value])
        # We first check for already existing milestones
        for current_milestone_title, current_milestone in sorted(current_milestones.items()):
            if current_milestone_title in target_milestones:
                for target_milestone_param_name, target_milestone_param_value in (
                    sorted(target_milestones[current_milestone_title].items())
                ):
                    try:
                        current_milestone_param_value = getattr(current_milestone, target_milestone_param_name)
                    except AttributeError:
                        logger.info('[%s] NOT Changing milestone %s %s: %s -> %s (current value is not available)',
                                    self._name, current_milestone_title, target_milestone_param_name,
                                    None, target_milestone_param_value)
                        continue
                    if current_milestone_param_value is None:
                        current_milestone_param_value = ''
                    if current_milestone_param_value != target_milestone_param_value:
                        if target_milestone_param_name == 'state':
                            target_milestone_param_name = 'state_event'
                            if target_milestone_param_value == 'closed':
                                target_milestone_param_value = 'close'
                            else:
                                target_milestone_param_value = 'activate'
                        if dry_run:
                            logger.info('[%s] NOT Changing milestone %s %s: %s -> %s (dry-run)',
                                        self._name, current_milestone_title, target_milestone_param_name,
                                        current_milestone_param_value, target_milestone_param_value)
                        else:
                            logger.info('[%s] Changing milestone %s %s: %s -> %s',
                                        self._name, current_milestone_title, target_milestone_param_name,
                                        current_milestone_param_value, target_milestone_param_value)
                            setattr(current_milestone, target_milestone_param_name, target_milestone_param_value)
                            current_milestone.save()
                target_milestones.pop(current_milestone_title)
            else:
                if unknown_milestones in ['delete', 'remove']:
                    if dry_run:
                        logger.info('[%s] NOT Removing milestone %s (dry-run)',
                                    self._name, current_milestone_title)
                    else:
                        logger.info('[%s] Removing milestone %s',
                                    self._name, current_milestone_title)
                        current_milestone.delete()
                elif unknown_milestones not in ['ignore', 'skip']:
                    logger.warning('[%s] NOT Removing milestone: %s',
                                   self._name, current_milestone_title)
        # Remaining milestones
        for target_milestone_title, target_milestone in sorted(target_milestones.items()):
            if dry_run:
                logger.info('[%s] NOT Adding milestone %s: %s -> %s (dry-run)',
                            self._name, target_milestone_title, None, target_milestone)
            else:
                logger.info('[%s] Adding milestone %s: %s -> %s',
                            self._name, target_milestone_title, None, target_milestone)
                self._obj.milestones.create(target_milestone)
