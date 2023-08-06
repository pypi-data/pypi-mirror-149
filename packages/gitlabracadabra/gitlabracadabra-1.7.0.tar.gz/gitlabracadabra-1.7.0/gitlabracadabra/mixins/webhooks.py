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


class WebhooksMixin(object):
    """Object with webhooks."""

    """_process_webhooks()

    Process the webhooks param.
    """
    def _process_webhooks(self, param_name, param_value, dry_run=False, skip_save=False):
        assert param_name == 'webhooks'  # noqa: S101
        assert not skip_save  # noqa: S101
        unknown_webhooks = self._content.get('unknown_webhooks', 'warn')
        current_webhooks = dict([[current_webhook.url, current_webhook]
                                 for current_webhook in self._obj.hooks.list(all=True)])
        target_webhooks = dict([[target_webhook['url'], deepcopy(target_webhook)]
                                for target_webhook in param_value])
        # We first check for already existing webhooks
        for current_webhook_url, current_webhook in sorted(current_webhooks.items()):
            if current_webhook_url in target_webhooks:
                for target_webhook_param_name, target_webhook_param_value in (
                    target_webhooks[current_webhook_url].items()
                ):
                    current_webhook_param_value = getattr(current_webhook, target_webhook_param_name, None)
                    if current_webhook_param_value != target_webhook_param_value:
                        if dry_run:
                            logger.info('[%s] NOT Changing webhook %s %s: %s -> %s (dry-run)',
                                        self._name, current_webhook_url, target_webhook_param_name,
                                        current_webhook_param_value, target_webhook_param_value)
                        else:
                            logger.info('[%s] Changing webhook %s %s: %s -> %s',
                                        self._name, current_webhook_url, target_webhook_param_name,
                                        current_webhook_param_value, target_webhook_param_value)
                            setattr(current_webhook, target_webhook_param_name, target_webhook_param_value)
                            current_webhook.save()
                target_webhooks.pop(current_webhook_url)
            else:
                if unknown_webhooks in ['delete', 'remove']:
                    if dry_run:
                        logger.info('[%s] NOT Removing webhook %s (dry-run)',
                                    self._name, current_webhook_url)
                    else:
                        logger.info('[%s] Removing webhook %s',
                                    self._name, current_webhook_url)
                        current_webhook.delete()
                elif unknown_webhooks not in ['ignore', 'skip']:
                    logger.warning('[%s] NOT Removing webhook: %s',
                                   self._name, current_webhook_url)
        # Remaining webhooks
        for target_webhook_name, target_webhook in sorted(target_webhooks.items()):
            if dry_run:
                logger.info('[%s] NOT Adding webhook %s: %s -> %s (dry-run)',
                            self._name, target_webhook_name, None, target_webhook)
            else:
                logger.info('[%s] Adding webhook %s: %s -> %s',
                            self._name, target_webhook_name, None, target_webhook)
                self._obj.hooks.create(target_webhook)
