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


class VariablesMixin(object):
    """Object with variables."""

    """_process_variables()

    Process the variables param.
    """
    def _process_variables(self, param_name, param_value, dry_run=False, skip_save=False):
        assert param_name == 'variables'  # noqa: S101
        assert not skip_save  # noqa: S101
        unknown_variables = self._content.get('unknown_variables', 'warn')
        current_variables = dict([[current_variable.key, current_variable]
                                  for current_variable in self._obj.variables.list(all=True)])
        target_variables = dict([[target_variable['key'], deepcopy(target_variable)]
                                 for target_variable in param_value])
        # We first check for already existing variables
        for current_variable_key, current_variable in sorted(current_variables.items()):
            if current_variable_key in target_variables:
                for target_variable_param_name, target_variable_param_value in (
                    target_variables[current_variable_key].items()
                ):
                    try:
                        current_variable_param_value = getattr(current_variable, target_variable_param_name)
                    except AttributeError:
                        logger.info('[%s] NOT Changing variable %s %s: %s -> %s (current value is not available)',
                                    self._name, current_variable_key, target_variable_param_name,
                                    None, target_variable_param_value)
                        continue
                    if current_variable_param_value != target_variable_param_value:
                        if dry_run:
                            logger.info('[%s] NOT Changing variable %s %s: %s -> %s (dry-run)',
                                        self._name, current_variable_key, target_variable_param_name,
                                        current_variable_param_value, target_variable_param_value)
                        else:
                            logger.info('[%s] Changing variable %s %s: %s -> %s',
                                        self._name, current_variable_key, target_variable_param_name,
                                        current_variable_param_value, target_variable_param_value)
                            setattr(current_variable, target_variable_param_name, target_variable_param_value)
                            current_variable.save()
                target_variables.pop(current_variable_key)
            else:
                if unknown_variables in ['delete', 'remove']:
                    if dry_run:
                        logger.info('[%s] NOT Removing variable %s (dry-run)',
                                    self._name, current_variable_key)
                    else:
                        logger.info('[%s] Removing variable %s',
                                    self._name, current_variable_key)
                        current_variable.delete()
                elif unknown_variables not in ['ignore', 'skip']:
                    logger.warning('[%s] NOT Removing variable: %s',
                                   self._name, current_variable_key)
        # Remaining variables
        for target_variable_name, target_variable in sorted(target_variables.items()):
            if dry_run:
                logger.info('[%s] NOT Adding variable %s: %s -> %s (dry-run)',
                            self._name, target_variable_name, None, target_variable)
            else:
                logger.info('[%s] Adding variable %s: %s -> %s',
                            self._name, target_variable_name, None, target_variable)
                self._obj.variables.create(target_variable)
