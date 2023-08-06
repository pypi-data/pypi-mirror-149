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


class BoardsMixin(object):
    """Object with boards."""

    """_process_boards()

    Process the boards param.
    """
    def _process_boards(self, param_name, param_value, dry_run=False, skip_save=False):
        assert param_name == 'boards'  # noqa: S101
        assert not skip_save  # noqa: S101

        unknown_boards = self._content.get('unknown_boards', 'warn')
        unknown_board_lists = self._content.get('unknown_board_lists', 'delete')

        current_boards = dict([[current_board.name, current_board]
                              for current_board in self._obj.boards.list(all=True)])
        target_boards = dict([[target_board['name'], deepcopy(target_board)]
                             for target_board in param_value])
        target_boards_by_old_name = dict([[target_board['old_name'], deepcopy(target_board)]
                                         for target_board in param_value if 'old_name' in target_board])

        # We do not reuse labels from LabelsMixin, to have fresh data
        try:
            self._current_labels = dict([[current_label.name, current_label]
                                        for current_label in self._obj.labels.list(all=True)])
        except AttributeError:
            # https://github.com/python-gitlab/python-gitlab/pull/847
            logger.error('[%s] Unable to manage labels: %s',
                         self._name, 'group labels requires python-gitlab >= 1.11.0')
            return

        # We first check for already existing boards
        for current_board_name, current_board in sorted(current_boards.items()):
            if current_board_name in target_boards:
                target_board = target_boards.pop(current_board_name)
            elif current_board_name in target_boards_by_old_name:
                target_board = target_boards_by_old_name[current_board_name]
                target_boards.pop(target_board['name'])
                if dry_run:
                    logger.info('[%s] NOT Changing board %s %s: %s -> %s (dry-run)',
                                self._name, current_board_name,
                                'name', current_board_name,
                                target_board['name'])
                else:
                    logger.info('[%s] Changing board %s %s: %s -> %s',
                                self._name, current_board_name,
                                'name', current_board_name,
                                target_board['name'])
                    current_board.name = target_board['name']
                    try:
                        current_board.save()
                    except KeyError:
                        # v1.10.0 - feat: add support for board update
                        # https://github.com/python-gitlab/python-gitlab/pull/804
                        logger.error('[%s] Unable to update board: %s',
                                     self._name, 'board update requires python-gitlab >= 1.10.0')
                        return
            else:
                target_board = None
            if target_board:
                for target_board_param_name, target_board_param_value in target_board.items():
                    if target_board_param_name == 'lists':
                        unknown_lists = target_board.get('unknown_lists', unknown_board_lists)
                        self._handle_board_lists(current_board, target_board_param_value, unknown_lists, dry_run)
                        continue
                    if target_board_param_name in ['old_name', 'unknown_lists']:
                        continue
                    try:
                        current_board_param_value = getattr(current_board, target_board_param_name)
                    except AttributeError:
                        logger.info('[%s] NOT Changing boards %s %s: %s -> %s '
                                    '(current value is not available)',
                                    self._name, current_board_name,
                                    target_board_param_name, None, target_board_param_value)
                        continue
                    if current_board_param_value != target_board_param_value:
                        if dry_run:
                            logger.info('[%s] NOT Changing board %s %s: %s -> %s (dry-run)',
                                        self._name, current_board_name,
                                        target_board_param_name, current_board_param_value,
                                        target_board_param_value)
                        else:
                            logger.info('[%s] Changing board %s %s: %s -> %s',
                                        self._name, current_board_name,
                                        target_board_param_name, current_board_param_value,
                                        target_board_param_value)
                            setattr(current_board, target_board_param_name,
                                    target_board_param_value)
                            try:
                                current_board.save()
                            except KeyError:
                                # v1.10.0 - feat: add support for board update
                                # https://github.com/python-gitlab/python-gitlab/pull/804
                                logger.error('[%s] Unable to update board: %s',
                                             self._name, 'board update requires python-gitlab >= 1.10.0')
                                return
            else:
                if unknown_boards in ['delete', 'remove']:
                    if dry_run:
                        logger.info('[%s] NOT Removing board %s (dry-run)',
                                    self._name, current_board_name)
                    else:
                        logger.info('[%s] Removing board %s',
                                    self._name, current_board_name)
                        current_board.delete()
                elif unknown_boards not in ['ignore', 'skip']:
                    logger.warning('[%s] NOT Removing board: %s',
                                   self._name, current_board_name)
        # Remaining boards
        for target_board_name, target_board in sorted(target_boards.items()):
            target_board_lists = target_board.pop('lists', [])
            unknown_lists = target_board.pop('unknown_lists', unknown_board_lists)
            if dry_run:
                logger.info('[%s] NOT Adding board %s: %s -> %s (dry-run)',
                            self._name, target_board_name, None, target_board)
            else:
                logger.info('[%s] Adding board %s: %s -> %s',
                            self._name, target_board_name, None, target_board)
                board = self._obj.boards.create(target_board)
                self._handle_board_lists(board, target_board_lists, unknown_lists, dry_run)

    """_handle_board_lists()

    Handle board lists.
    """
    def _handle_board_lists(self, board, target_lists, unknown_lists, dry_run=False):
        if len(target_lists) == 0 and unknown_lists in ['ignore', 'skip']:
            return
        board = self._obj.boards.get(board.id)
        current_lists = dict([[current_list.label['name'], current_list]
                              for current_list in board.lists.list()])
        # We first add any missing list
        for target_list_position, target_list in enumerate(target_lists):
            if target_list['label'] in current_lists:
                current_list = current_lists[target_list['label']]
                if target_list_position != current_list.position:
                    old_list_position = current_list.position
                    # Boards::Lists::MoveService
                    # https://gitlab.com/gitlab-org/gitlab/-/blob/master/app/services/boards/lists/move_service.rb#L29
                    if old_list_position < target_list_position:
                        self._decrement_intermediate_lists(current_lists, old_list_position, target_list_position)
                    else:
                        self._increment_intermediate_lists(current_lists, old_list_position, target_list_position)
                    current_list.position = target_list_position
                    if dry_run:
                        logger.info('[%s] NOT Changing board list position %s: %s -> %s (dry-run)',
                                    self._name, target_list,
                                    current_list.position, target_list_position)
                    else:
                        logger.info('[%s] Changing board list position %s: %s -> %s (dry-run)',
                                    self._name, target_list,
                                    current_list.position, target_list_position)
                        current_list.save()
            else:
                if target_list['label'] not in self._current_labels:
                    logger.warning('[%s] Label not found for board %s: %s',
                                   self._name, board.name, target_list['label'])
                    continue
                label_id = self._current_labels[target_list['label']].id
                if dry_run:
                    logger.info('[%s] NOT Adding board list %s (dry-run)',
                                self._name, target_list)
                else:
                    logger.info('[%s] Adding board list %s',
                                self._name, target_list)
                    board.lists.create({'label_id': label_id})

        if unknown_lists in ['ignore', 'skip']:
            return
        # Delete any remaining lists
        for current_list_label, current_list in sorted(current_lists.items()):
            current_list_dict = {'label': current_list_label}
            if current_list_dict in target_lists:
                continue

            if unknown_lists in ['delete', 'remove']:
                if dry_run:
                    logger.info('[%s] NOT Removing board list %s (dry-run)',
                                self._name, current_list_dict)
                else:
                    logger.info('[%s] Removing board list %s',
                                self._name, current_list_dict)
                    current_list.delete()
            elif unknown_lists not in ['ignore', 'skip']:
                logger.warning('[%s] NOT Removing board list: %s',
                               self._name, current_list_dict)

    """_decrement_intermediate_lists()

    Decrement intermediate lists.
    """
    def _decrement_intermediate_lists(self, lists, old_position, new_position):
        for _list_name, list_object in lists.items():
            if list_object.position > old_position and list_object.position <= new_position:
                list_object.position = list_object.position - 1

    """_increment_intermediate_lists()

    Increment intermediate lists.
    """
    def _increment_intermediate_lists(self, lists, old_position, new_position):
        for _list_name, list_object in lists.items():
            if list_object.position >= new_position and list_object.position < old_position:
                list_object.position = list_object.position + 1
