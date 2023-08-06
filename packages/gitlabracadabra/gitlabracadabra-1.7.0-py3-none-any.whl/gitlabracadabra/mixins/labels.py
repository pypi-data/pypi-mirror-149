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
from copy import deepcopy


logger = logging.getLogger(__name__)


class LabelsMixin(object):
    """Object with labels."""

    """_process_labels()

    Process the labels param.
    """
    def _process_labels(self, param_name, param_value, dry_run=False, skip_save=False):
        assert param_name == 'labels'  # noqa: S101
        assert not skip_save  # noqa: S101
        unknown_labels = self._content.get('unknown_labels', 'warn')
        try:
            current_labels = dict([[current_label.name, current_label]
                                   for current_label in self._obj.labels.list(all=True)])
        except AttributeError:
            # https://github.com/python-gitlab/python-gitlab/pull/847
            logger.error('[%s] Unable to manage labels: %s',
                         self._name, 'group labels requires python-gitlab >= 1.11.0')
            return
        target_labels = dict([[target_label['name'], deepcopy(target_label)]
                              for target_label in param_value])
        # We first check for already existing labels
        for current_label_name, current_label in sorted(current_labels.items()):
            if current_label_name in target_labels:
                for target_label_param_name, target_label_param_value in (
                    sorted(target_labels[current_label_name].items())
                ):
                    try:
                        current_label_param_value = getattr(current_label, target_label_param_name)
                    except AttributeError:
                        logger.info('[%s] NOT Changing label %s %s: %s -> %s (current value is not available)',
                                    self._name, current_label_name, target_label_param_name,
                                    None, target_label_param_value)
                        continue
                    if target_label_param_name == 'description' and current_label_param_value is None:
                        current_label_param_value = ''
                    if current_label_param_value != target_label_param_value:
                        if dry_run:
                            logger.info('[%s] NOT Changing label %s %s: %s -> %s (dry-run)',
                                        self._name, current_label_name, target_label_param_name,
                                        current_label_param_value, target_label_param_value)
                        else:
                            logger.info('[%s] Changing label %s %s: %s -> %s',
                                        self._name, current_label_name, target_label_param_name,
                                        current_label_param_value, target_label_param_value)
                            setattr(current_label, target_label_param_name, target_label_param_value)
                            current_label.save()
                target_labels.pop(current_label_name)
            else:
                if (
                    self.__class__.__name__ == 'GitLabracadabraProject' and
                    not getattr(current_label, 'is_project_label', False)
                ):
                    # Ignore group-level labels on projects
                    continue
                if unknown_labels in ['delete', 'remove']:
                    if dry_run:
                        logger.info('[%s] NOT Removing label %s (dry-run)',
                                    self._name, current_label_name)
                    else:
                        logger.info('[%s] Removing label %s',
                                    self._name, current_label_name)
                        current_label.delete()
                elif unknown_labels not in ['ignore', 'skip']:
                    logger.warning('[%s] NOT Removing label: %s',
                                   self._name, current_label_name)
        # Remaining labels
        for target_label_name, target_label in sorted(target_labels.items()):
            if dry_run:
                logger.info('[%s] NOT Adding label %s: %s -> %s (dry-run)',
                            self._name, target_label_name, None, target_label)
            else:
                logger.info('[%s] Adding label %s: %s -> %s',
                            self._name, target_label_name, None, target_label)
                self._obj.labels.create(target_label)
