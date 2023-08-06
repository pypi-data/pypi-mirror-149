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

from gitlabracadabra.mixins.boards import BoardsMixin
from gitlabracadabra.mixins.groups import GroupsMixin
from gitlabracadabra.mixins.labels import LabelsMixin
from gitlabracadabra.mixins.members import MembersMixin
from gitlabracadabra.mixins.milestones import MilestonesMixin
from gitlabracadabra.mixins.variables import VariablesMixin
from gitlabracadabra.objects.object import GitLabracadabraObject


class GitLabracadabraGroup(GitLabracadabraObject, BoardsMixin, GroupsMixin, LabelsMixin, MembersMixin, MilestonesMixin,
                           VariablesMixin):
    EXAMPLE_YAML_HEADER = 'mygroup/:\n'
    DOC = [
        '# Group lifecycle',
        'gitlab_id',
        'create_object',
        'delete_object',

        '# General Settings',
        '## Naming, visibility',
        'name',
        'description',
        # 'avatar',  # FIXME
        'visibility',
        '## Permissions, LFS, 2FA',
        'request_access_enabled',
        'share_with_group_lock',
        'emails_disabled',
        'lfs_enabled',
        'project_creation_level',
        'subgroup_creation_level',
        'require_two_factor_authentication',
        'two_factor_grace_period',
        'membership_lock',
        # '## Badges',  # FIXME ...

        '# CI / CD Settings',
        '## Variables',
        'variables',
        'unknown_variables',
        '## Auto DevOps',
        'auto_devops_enabled',

        '# Members',
        'members',
        'unknown_members',
        'groups',
        'unknown_groups',

        '# Issues',
        '## Boards',
        'boards',
        'unknown_boards',
        'unknown_board_lists',
        '## Labels',
        'labels',
        'unknown_labels',
        '## Milestones',
        'milestones',
        'unknown_milestones',
    ]
    SCHEMA = {
        '$schema': 'http://json-schema.org/draft-04/schema#',
        'title': 'Group',
        'type': 'object',
        'properties': {
            # Standard properties
            'gitlab_id': {
                'type': 'string',
                'description': 'GitLab id',
                '_example': 'gitlab',
                '_doc_link': 'action_file.md#gitlab_id',
            },
            'create_object': {
                'type': 'boolean',
                'description': 'Create object if it does not exists',
            },
            'delete_object': {
                'type': 'boolean',
                'description': 'Delete object if it exists',
            },
            # From https://docs.gitlab.com/ee/api/groups.html#new-group
            'name': {
                'type': 'string',
                'description': 'The name of the group',
            },
            # 'path': {
            #     'type': 'string',
            #     'description': 'The path of the group',
            # },
            'description': {
                'type': 'string',
                'description': 'The group’s description',
            },
            'visibility': {
                'type': 'string',
                'description': 'The group’s visibility. Can be private, internal, or public.',
                'enum': ['private', 'internal', 'public'],
            },
            'request_access_enabled': {
                'type': 'boolean',
                'description': 'Allow users to request member access.',
            },
            'share_with_group_lock': {
                'type': 'boolean',
                'description': 'Prevent sharing a project with another group within this group',
            },
            'emails_disabled': {
                'type': 'boolean',
                'description': 'Disable email notifications',
            },
            'lfs_enabled': {
                'type': 'boolean',
                'description': 'Enable/disable Large File Storage (LFS) for the projects in this group',
            },
            'project_creation_level': {
                'type': 'string',
                'description': 'Determine if developers can create projects in the group',
                'enum': ['noone', 'maintainer', 'developer'],
            },
            'subgroup_creation_level': {
                'type': 'string',
                'description': 'Allowed to create subgroups',
                'enum': ['owner', 'maintainer'],
            },
            'require_two_factor_authentication': {
                'type': 'boolean',
                'description': 'Require all users in this group to setup Two-factor authentication',
            },
            'two_factor_grace_period': {
                'type': 'integer',
                'description': 'Time before Two-factor authentication is enforced (in hours)',
            },
            'membership_lock': {
                'type': 'boolean',
                'description': 'Prevent adding new members to project membership within this group',
            },
            # From https://docs.gitlab.com/ee/api/group_level_variables.html#create-variable
            'variables': {
                'type': 'array',
                'description': "The list of group's variables",
                'items': {
                    'type': 'object',
                    'properties': {
                        'key': {
                            'type': 'string',
                            'description': 'The key of a variable.',
                            'pattern': '[a-zA-Z0-9_]+',
                        },
                        'value': {
                            'type': 'string',
                            'description': 'The value of a variable.',
                        },
                        'variable_type': {
                            'type': 'string',
                            'description': 'The type of a variable. Available types are: env_var (default) and file.',
                            'enum': ['env_var', 'file'],
                        },
                        'protected': {
                            'type': 'boolean',
                            'description': 'Whether the variable is protected.',
                        },
                        'masked': {
                            'type': 'boolean',
                            'description': 'Whether the variable is masked.',
                        },
                    },
                    'required': ['key', 'value'],
                    'additionalProperties': False,
                },
                'uniqueItems': True,
                '_example': ('\n'
                             '    - key: DAST_DISABLED\n'
                             "      value: '1'\n"
                             '      masked: false\n'
                             '      protected: false\n'
                             '      variable_type: env_var\n'),
            },
            'unknown_variables': {  # GitLabracadabra
                'type': 'string',
                'description': 'What to do with unknown variables (`warn` by default).',
                'enum': ['warn', 'delete', 'remove', 'ignore', 'skip'],
            },
            # From https://docs.gitlab.com/ee/api/groups.html#new-group
            'auto_devops_enabled': {
                'type': 'boolean',
                'description': 'Default to Auto DevOps pipeline for all projects within this group',
            },
            # From https://docs.gitlab.com/ee/api/members.html#add-a-member-to-a-group-or-project
            # FIXME expires_at not supported
            'members': {
                'type': 'object',
                'description': 'Members',
                'additionalProperties': {
                    'type': 'string',
                    'description': 'The permissions level to grant the member.',
                    'enum': ['guest', 'reporter', 'developer', 'maintainer', 'owner'],
                },
                '_example': ('\n'
                             '    foo: developer\n'
                             '    bar: maintainer # one of guest, reporter, developer, maintainer, owner\n'),
            },
            'unknown_members': {  # GitLabracadabra
                'type': 'string',
                'description': 'What to do with unknown members (`warn` by default).',
                'enum': ['warn', 'delete', 'remove', 'ignore', 'skip'],
            },
            # From https://docs.gitlab.com/ee/api/groups.html#create-a-link-to-share-a-group-with-another-group
            # and https://docs.gitlab.com/ee/api/groups.html#delete-link-sharing-group-with-another-group
            # FIXME expires_at not supported
            'groups': {
                'type': 'object',
                'description': 'Groups',
                'additionalProperties': {
                    'type': 'string',
                    'description': 'The permissions level to grant the group.',
                    'enum': ['guest', 'reporter', 'developer', 'maintainer'],
                },
                '_example': ('\n'
                             '    group/foo: guest\n'
                             '    group/bar: reporter # one of guest, reporter, developer, maintainer\n'),
            },
            'unknown_groups': {  # GitLabracadabra
                'type': 'string',
                'description': 'What to do with unknown groups (`warn` by default).',
                'enum': ['warn', 'delete', 'remove', 'ignore', 'skip'],
            },
            # From https://docs.gitlab.com/ee/api/group_boards.html
            'boards': {
                'type': 'array',
                'description': "The list of group's boards",
                'items': {
                    'type': 'object',
                    'properties': {
                        'name': {
                            'type': 'string',
                            'description': 'The name of the board.',
                        },
                        'old_name': {
                            'type': 'string',
                            'description': 'The previous name of the board.',
                        },
                        'hide_backlog_list': {
                            'type': 'boolean',
                            'description': 'Hide the Open list',
                        },
                        'hide_closed_list': {
                            'type': 'boolean',
                            'description': 'Hide the Closed list',
                        },
                        'lists': {
                            'type': 'array',
                            'description': 'Ordered list of labels',
                            'items': {
                                'type': 'object',
                                'properties': {
                                    'label': {
                                        'type': 'string',
                                        'description': 'The name of a label',
                                    },
                                },
                            },
                        },
                        'unknown_lists': {  # GitLabracadabra
                            'type': 'string',
                            'description': ('What to do with unknown board lists '
                                            '(Value of `unknown_board_lists` by default).'),
                            'enum': ['warn', 'delete', 'remove', 'ignore', 'skip'],
                        },
                    },
                    'required': ['name'],
                    'additionalProperties': False,
                },
                'uniqueItems': True,
                '_example': ('\n'
                             '    - name: My group board\n'
                             '      # old_name: Development # Use this to rename a board\n'
                             '      hide_backlog_list: false\n'
                             '      hide_closed_list: false\n'
                             '      lists:\n'
                             '        - label: TODO\n'
                             '        - label: WIP\n'),
            },
            'unknown_boards': {  # GitLabracadabra
                'type': 'string',
                'description': 'What to do with unknown boards (`warn` by default).',
                'enum': ['warn', 'delete', 'remove', 'ignore', 'skip'],
            },
            'unknown_board_lists': {  # GitLabracadabra
                'type': 'string',
                'description': 'What to do with unknown board lists (`delete` by default).',
                'enum': ['warn', 'delete', 'remove', 'ignore', 'skip'],
            },
            # From https://docs.gitlab.com/ee/api/group_labels.html#create-a-new-group-label
            'labels': {
                'type': 'array',
                'description': "The list of group's labels",
                'items': {
                    'type': 'object',
                    'properties': {
                        'name': {
                            'type': 'string',
                            'description': 'The name of the label.',
                        },
                        'color': {
                            'type': 'string',
                            'description': 'The color of the label.',
                        },
                        'description': {
                            'type': 'string',
                            'description': 'The description of the label.',
                        },
                    },
                    'required': ['name', 'color'],
                    'additionalProperties': False,
                },
                'uniqueItems': True,
                '_example': ('\n'
                             '    - name: bug\n'
                             "      color: '#d9534f'\n"
                             "      description: ''\n"
                             '    - name: confirmed\n'
                             "      color: '#d9534f'\n"
                             "      description: ''\n"
                             '    - name: critical\n'
                             "      color: '#d9534f'\n"
                             "      description: ''\n"
                             '    - name: discussion\n'
                             "      color: '#428bca'\n"
                             "      description: ''\n"
                             '    - name: documentation\n'
                             "      color: '#f0ad4e'\n"
                             "      description: ''\n"
                             '    - name: enhancement\n'
                             "      color: '#5cb85c'\n"
                             "      description: ''\n"
                             '    - name: suggestion\n'
                             "      color: '#428bca'\n"
                             "      description: ''\n"
                             '    - name: support\n'
                             "      color: '#f0ad4e'\n"
                             "      description: ''\n"),
            },
            'unknown_labels': {  # GitLabracadabra
                'type': 'string',
                'description': 'What to do with unknown labels (`warn` by default).',
                'enum': ['warn', 'delete', 'remove', 'ignore', 'skip'],
            },
            # From https://docs.gitlab.com/ee/api/group_milestones.html#edit-milestone
            'milestones': {
                'type': 'array',
                'description': "The list of group's milestones",
                'items': {
                    'type': 'object',
                    'properties': {
                        'title': {
                            'type': 'string',
                            'description': 'The title of a milestone',
                        },
                        'description': {
                            'type': 'string',
                            'description': 'The description of a milestone',
                        },
                        'due_date': {
                            'type': 'string',
                            'description': 'The due date of the milestone',
                            'pattern': '^(\\d{4}-\\d{2}-\\d{2})?$',
                        },
                        'start_date': {
                            'type': 'string',
                            'description': 'The start date of the milestone',
                            'pattern': '^(\\d{4}-\\d{2}-\\d{2})?$',
                        },
                        'state': {
                            'type': 'string',
                            'description': 'The state event of the milestone',
                            'enum': ['closed', 'active'],
                        },
                    },
                    'required': ['title'],
                    'additionalProperties': False,
                },
                'uniqueItems': True,
                '_example': ('\n'
                             "    - title: '1.0'\n"
                             '      description: Version 1.0\n'
                             "      due_date: '2021-01-23' # Quotes are mandatory\n"
                             "      start_date: '2020-01-23' # Quotes are mandatory\n"
                             '      state: active # or closed\n'),
            },
            'unknown_milestones': {  # GitLabracadabra
                'type': 'string',
                'description': 'What to do with unknown milestones (`warn` by default).',
                'enum': ['warn', 'delete', 'remove', 'ignore', 'skip'],
            },
            # From https://docs.gitlab.com/ee/api/groups.html#new-group
            # Below are undocumented settings
            'file_template_project_id': {
                'type': 'integer',
                'description': '(Premium) The ID of a project to load custom file templates from',
                'multipleOf': 1,
                'minimum': 0,
            },
            'shared_runners_minutes_limit': {
                'type': 'integer',
                'description': '(admin-only) Pipeline minutes quota for this group.',
                'multipleOf': 1,
                'minimum': 0,
            },
            'extra_shared_runners_minutes_limit': {
                'type': 'integer',
                'description': '(admin-only) Extra pipeline minutes quota for this group.',
                'multipleOf': 1,
                'minimum': 0,
            },
        },
        'additionalProperties': False,
    }

    IGNORED_PARAMS = ['unknown_boards',
                      'unknown_board_lists',
                      'unknown_groups',
                      'unknown_labels',
                      'unknown_members',
                      'unknown_milestones',
                      'unknown_variables']

    CREATE_KEY = 'name'
