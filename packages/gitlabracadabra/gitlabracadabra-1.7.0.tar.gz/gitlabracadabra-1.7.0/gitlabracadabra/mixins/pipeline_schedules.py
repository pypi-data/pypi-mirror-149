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


class PipelineSchedulesMixin(object):
    """Object with pipeline schedules."""

    """_process_pipeline_schedules()

    Process the pipeline_schedules param.
    """
    def _process_pipeline_schedules(self, param_name, param_value, dry_run=False, skip_save=False):
        assert param_name == 'pipeline_schedules'  # noqa: S101
        assert not skip_save  # noqa: S101
        unknown_pipeline_schedules = self._content.get('unknown_pipeline_schedules', 'warn')
        current_pipeline_schedules = dict([[current_pipeline_schedule.description, current_pipeline_schedule]
                                          for current_pipeline_schedule in self._obj.pipelineschedules.list(all=True)])
        target_pipeline_schedules = dict([[target_pipeline_schedule['description'], deepcopy(target_pipeline_schedule)]
                                         for target_pipeline_schedule in param_value])
        unknown_pipeline_schedule_variables = self._content.get('unknown_pipeline_schedule_variables', 'warn')
        # We first check for already existing pipeline schedules
        for current_pipeline_schedule_description, current_pipeline_schedule in (
            sorted(current_pipeline_schedules.items())
        ):
            if current_pipeline_schedule_description in target_pipeline_schedules:
                target_pipeline_schedule = target_pipeline_schedules[current_pipeline_schedule_description]
                for target_pipeline_schedule_param_name, target_pipeline_schedule_param_value in (
                    target_pipeline_schedule.items()
                ):
                    if target_pipeline_schedule_param_name == 'variables':
                        unknown_variables = target_pipeline_schedule.get('unknown_variables',
                                                                         unknown_pipeline_schedule_variables)
                        self._handle_pipeline_schedule_variables(current_pipeline_schedule,
                                                                 target_pipeline_schedule_param_value,
                                                                 unknown_variables,
                                                                 dry_run)
                        continue
                    if target_pipeline_schedule_param_name == 'unknown_variables':
                        continue
                    try:
                        current_pipeline_schedule_param_value = getattr(current_pipeline_schedule,
                                                                        target_pipeline_schedule_param_name)
                    except AttributeError:
                        logger.info('[%s] NOT Changing pipeline schedules %s %s: %s -> %s '
                                    '(current value is not available)',
                                    self._name, current_pipeline_schedule_description,
                                    target_pipeline_schedule_param_name, None, target_pipeline_schedule_param_value)
                        continue
                    if current_pipeline_schedule_param_value != target_pipeline_schedule_param_value:
                        if dry_run:
                            logger.info('[%s] NOT Changing pipeline schedule %s %s: %s -> %s (dry-run)',
                                        self._name, current_pipeline_schedule_description,
                                        target_pipeline_schedule_param_name, current_pipeline_schedule_param_value,
                                        target_pipeline_schedule_param_value)
                        else:
                            logger.info('[%s] Changing pipeline schedule %s %s: %s -> %s',
                                        self._name, current_pipeline_schedule_description,
                                        target_pipeline_schedule_param_name, current_pipeline_schedule_param_value,
                                        target_pipeline_schedule_param_value)
                            setattr(current_pipeline_schedule, target_pipeline_schedule_param_name,
                                    target_pipeline_schedule_param_value)
                            current_pipeline_schedule.save()
                target_pipeline_schedules.pop(current_pipeline_schedule_description)
            else:
                if unknown_pipeline_schedules in ['delete', 'remove']:
                    if dry_run:
                        logger.info('[%s] NOT Removing pipeline schedule %s (dry-run)',
                                    self._name, current_pipeline_schedule_description)
                    else:
                        logger.info('[%s] Removing pipeline schedule %s',
                                    self._name, current_pipeline_schedule_description)
                        current_pipeline_schedule.delete()
                elif unknown_pipeline_schedules not in ['ignore', 'skip']:
                    logger.warning('[%s] NOT Removing pipeline schedule: %s',
                                   self._name, current_pipeline_schedule_description)
        # Remaining pipeline_schedules
        for target_pipeline_schedule_name, target_pipeline_schedule in sorted(target_pipeline_schedules.items()):
            target_pipeline_schedule_variables = target_pipeline_schedule.pop('variables', [])
            unknown_variables = target_pipeline_schedule.pop('unknown_variables', unknown_pipeline_schedule_variables)
            if dry_run:
                logger.info('[%s] NOT Adding pipeline schedule %s: %s -> %s (dry-run)',
                            self._name, target_pipeline_schedule_name, None, target_pipeline_schedule)
            else:
                logger.info('[%s] Adding pipeline schedule %s: %s -> %s',
                            self._name, target_pipeline_schedule_name, None, target_pipeline_schedule)
                pipeline_schedule = self._obj.pipelineschedules.create(target_pipeline_schedule)
                self._handle_pipeline_schedule_variables(pipeline_schedule, target_pipeline_schedule_variables,
                                                         unknown_variables, dry_run)

    """_handle_pipeline_schedule_variables()

    Handle pipeline schedule variables.
    """
    def _handle_pipeline_schedule_variables(self, pipeline_schedule, variables, unknown_variables, dry_run=False):
        if len(variables) == 0 and unknown_variables in ['ignore', 'skip']:
            return
        pipeline_schedule = self._obj.pipelineschedules.get(pipeline_schedule.id)
        current_variables = dict([[current_variable['key'], current_variable]
                                  for current_variable in pipeline_schedule.attributes['variables']])
        target_variables = dict([[target_variable['key'], deepcopy(target_variable)]
                                 for target_variable in variables])
        # We first check for already existing variables
        for current_variable_key, current_variable in sorted(current_variables.items()):
            if current_variable_key in target_variables:
                for target_variable_param_name, target_variable_param_value in (
                    target_variables[current_variable_key].items()
                ):
                    try:
                        current_variable_param_value = current_variable[target_variable_param_name]
                    except KeyError:
                        logger.info('[%s] NOT Changing pipeline schedule variable %s %s: %s -> %s '
                                    '(current value is not available)',
                                    self._name, current_variable_key, target_variable_param_name,
                                    None, target_variable_param_value)
                        continue
                    if current_variable_param_value != target_variable_param_value:
                        if dry_run:
                            logger.info('[%s] NOT Changing pipeline schedule variable %s %s: %s -> %s (dry-run)',
                                        self._name, current_variable_key, target_variable_param_name,
                                        current_variable_param_value, target_variable_param_value)
                        else:
                            logger.info('[%s] Changing pipeline schedule variable %s %s: %s -> %s',
                                        self._name, current_variable_key, target_variable_param_name,
                                        current_variable_param_value, target_variable_param_value)
                            new_data = {'key': current_variable_key,
                                        'value': target_variables[current_variable_key]['value']}
                            new_data[target_variable_param_name] = target_variable_param_value
                            pipeline_schedule.variables.update(current_variable_key, new_data)
                target_variables.pop(current_variable_key)
            else:
                if unknown_variables in ['delete', 'remove']:
                    if dry_run:
                        logger.info('[%s] NOT Removing pipeline schedule variable %s (dry-run)',
                                    self._name, current_variable_key)
                    else:
                        logger.info('[%s] Removing pipeline schedule variable %s',
                                    self._name, current_variable_key)
                        pipeline_schedule.variables.delete(current_variable_key)
                elif unknown_variables not in ['ignore', 'skip']:
                    logger.warning('[%s] NOT Removing variable: %s',
                                   self._name, current_variable_key)
        # Remaining variables
        for target_variable_name, target_variable in sorted(target_variables.items()):
            if dry_run:
                logger.info('[%s] NOT Adding pipeline schedule variable %s: %s -> %s (dry-run)',
                            self._name, target_variable_name, None, target_variable)
            else:
                logger.info('[%s] Adding pipeline schedule variable %s: %s -> %s',
                            self._name, target_variable_name, None, target_variable)
                pipeline_schedule.variables.create(target_variable)
