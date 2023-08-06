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

from __future__ import annotations

import logging
import re
from copy import deepcopy
from typing import TYPE_CHECKING, List, Optional

from gitlab.exceptions import GitlabCreateError, GitlabDeleteError, GitlabGetError, GitlabListError, GitlabUpdateError

from jsonschema.exceptions import ValidationError
from jsonschema.validators import validator_for

from gitlabracadabra.gitlab.connections import GitlabConnections


if TYPE_CHECKING:
    from gitlab import Gitlab

    from pygit2 import UserPass

    from gitlabracadabra.auth_info import AuthInfo
    from gitlabracadabra.gitlab.connection import GitlabConnection

logger = logging.getLogger(__name__)


class GitLabracadabraObject(object):
    SCHEMA = {
        '$schema': 'http://json-schema.org/draft-04/schema#',
        'title': 'Object',
        'type': 'object',
        'properties': {
        },
        'additionalProperties': False,
        # 'required': [],
    }

    # If not None, use find(FIND_PARAM=...) instead of get(...)
    FIND_PARAM: Optional[str] = None

    # If not None, set to id of the object on create
    CREATE_KEY: Optional[str] = None

    CREATE_PARAMS: List[str] = []

    IGNORED_PARAMS: List[str] = []

    def __init__(self, action_file, name, content):
        self._action_file = action_file
        self._name = name
        self._content = content
        validator_class = validator_for(self.SCHEMA)
        validator_class.check_schema(self.SCHEMA)
        validator = validator_class(self.SCHEMA)
        self._errors: list[ValidationError] = sorted(validator.iter_errors(content), key=lambda e: e.path)
        self._gitlab_id = self._content.pop('gitlab_id', None)
        self._create_object = self._content.pop('create_object', None)
        self._delete_object = self._content.pop('delete_object', None)

    @property
    def connection(self) -> GitlabConnection:
        return GitlabConnections().get_connection(self._gitlab_id)

    @property
    def pygitlab(self) -> Gitlab:
        return self.connection.pygitlab

    @property
    def pygit2_credentials(self) -> UserPass:
        return self.connection.pygit2_credentials

    @property
    def registry_auth_info(self) -> AuthInfo:
        return self.connection.registry_auth_info

    def errors(self) -> list[ValidationError]:
        return self._errors

    """"type_name()

    GitLabracadabraProject -> project.
    """
    @classmethod
    def _type_name(cls):
        return cls.__name__[15:].lower()

    """"type_name_plural()

    GitLabracadabraProject -> projects.
    """
    @classmethod
    def _type_name_plural(cls):
        return cls._type_name() + 's'

    """"_object_manager()

    Return the python-gitlab Gilab object.
    """
    def _object_manager(self):
        return getattr(self.pygitlab, self._type_name_plural())

    """"_create()

    Create the object.
    """
    def _create(self, dry_run=False):
        obj_manager = self._object_manager()
        namespace_manager = self.pygitlab.namespaces
        namespaces = self._name.split('/')
        object_path = namespaces.pop()
        create_params = {
            'path': object_path,
        }
        if self.CREATE_KEY:
            create_params[self.CREATE_KEY] = object_path
        for param_name in self.CREATE_PARAMS:
            if param_name in self._content:
                create_params[param_name] = self._content[param_name]
        if len(namespaces):
            try:
                parent_namespace = namespace_manager.get('/'.join(namespaces))
            except GitlabGetError as e:
                error_message = e.error_message
                if e.response_code == 404:
                    error_message = 'parent namespace not found'
                logger.error('[%s] NOT Creating %s (%s)', self._name, self._type_name(), error_message)
                return None
            if self._type_name() == 'group':
                create_params['parent_id'] = parent_namespace.id
            else:
                create_params['namespace_id'] = parent_namespace.id
        if dry_run:
            logger.info('[%s] NOT Creating %s (dry-run)', self._name, self._type_name())
            return None
        else:
            logger.info('[%s] Creating %s', self._name, self._type_name())
            try:
                return obj_manager.create(create_params)
            except GitlabCreateError as e:
                logger.error('[%s] NOT Creating %s (%s)', self._name, self._type_name(), e.error_message)
                return None

    """"_delete()

    Delete the object.
    """
    def _delete(self, dry_run=False):
        if self._obj is None:
            logger.debug('[%s] NOT Deleting %s (not found)', self._name, self._type_name())
        elif dry_run:
            logger.info('[%s] NOT Deleting %s (dry-run)', self._name, self._type_name())
        else:
            logger.info('[%s] Deleting %s', self._name, self._type_name())
            try:
                self._obj.delete()
            except GitlabCreateError as e:
                logger.error('[%s] Unable to delete %s (%s)', self._name, self._type_name(), e.error_message)

    """"_mangle_param()

    Convert a param value from GitLabracadabra form to API form.
    """
    def _mangle_param(self, param_name, param_value):
        if isinstance(param_value, str):
            # GitLab normalize to CRLF
            # YAML normalize to LF
            return param_value.replace('\n', '\r\n')
        return param_value

    """"_unmangle_param()

    Convert a param value from API form to GitLabracadabra form.
    """
    def _unmangle_param(self, param_name, param_value):
        return param_value

    """"_canonalize_param()

    Canonalize a param value.
    """
    def _canonalize_param(self, param_name, param_value):
        if isinstance(param_value, list):
            return sorted(param_value)
        return param_value

    """"_get_param()

    Get a param value.
    """
    def _get_param(self, param_name):
        return getattr(self._obj, param_name)

    """"_process_param()

    Process one param.
    """
    def _process_param(self, param_name, param_value, dry_run=False, skip_save=False):
        if param_name in self.IGNORED_PARAMS and not skip_save:
            return
        target_value = self._canonalize_param(param_name, param_value)
        try:
            current_value = self._canonalize_param(param_name,
                                                   self._unmangle_param(param_name, self._get_param(param_name)))
        except AttributeError:
            if not skip_save:
                # FIXME Hidden attributes cannot be idempotent (i.e password)
                logger.info('[%s] NOT Changing param %s: %s -> %s (current value is not available)',
                            self._name, param_name, None, target_value)
                return
            current_value = None
        if current_value != target_value or skip_save:
            if 'dependencies' in self.SCHEMA and param_name in self.SCHEMA['dependencies']:
                for dependency in self.SCHEMA['dependencies'][param_name]:
                    process_method = getattr(self, '_process_' + dependency, self._process_param)
                    process_method(dependency, self._content[dependency], dry_run, skip_save=True)
            if dry_run:
                logger.info('[%s] NOT Changing param %s: %s -> %s (dry-run)',
                            self._name, param_name, current_value, target_value)
                setattr(self._obj, param_name, self._mangle_param(param_name, target_value))
            else:
                logger.info('[%s] Changing param %s: %s -> %s',
                            self._name, param_name, current_value, target_value)
                setattr(self._obj, param_name, self._mangle_param(param_name, target_value))
                if not skip_save:
                    try:
                        self._obj.save()
                    except GitlabUpdateError as e:
                        logger.error('[%s] Unable to change param %s (%s -> %s): %s',
                                     self._name, param_name, current_value, target_value, e.error_message)

    """"_get()

    Set the _object attribute
    """
    def _get(self):
        obj_manager = self._object_manager()
        if self.FIND_PARAM:
            params = {self.FIND_PARAM: self._name}
            try:
                self._obj = obj_manager.list(**params)[0]
            except IndexError:
                self._obj = None
        else:
            try:
                self._obj = obj_manager.get(self._name)
            except GitlabGetError as err:
                if err.response_code != 404:
                    pass
                self._obj = None

    """"process()

    Process the object.
    """
    def process(self, dry_run=False):
        content_copy = deepcopy(self._content)
        self._get()
        if self._delete_object:
            self._delete(dry_run)
            return
        if self._obj is None:
            if self._create_object:
                self._obj = self._create(dry_run)
                if self._obj is None:
                    return
            else:
                logger.info('[%s] NOT Creating %s (create_object is false)', self._name, self._type_name())
                return
        for param_name, param_value in sorted(self._content.items()):
            process_method = getattr(self, '_process_' + param_name, self._process_param)
            try:
                process_method(param_name, param_value, dry_run)
            except (GitlabCreateError, GitlabDeleteError, GitlabGetError, GitlabListError, GitlabUpdateError) as e:
                logger.error('[%s] Error while processing param %s: %s',
                             self._name, param_name, e.error_message)
        if content_copy != self._content:
            raise RuntimeError('[%s] Changed values during processing' % self._name)

    """"_markdown_link()

    Generate a Markdown link.
    """
    @classmethod
    def _markdown_link(cls, header):
        # Remove heading #
        out = re.sub(r'^#+', '', header)
        # Trim and lower
        out = out.strip().lower()
        # Remove non-word characters
        out = re.sub(r'[^\w\- ]+', ' ', out)
        # Replace multiple spaces with dash
        out = re.sub(r'\s+', '-', out)
        # Remove trailing dashed
        out = re.sub(r'-+$', '', out)
        return '#' + out

    """"doc_markdown()

    Generate Markdown documentation.
    """
    @classmethod
    def doc_markdown(cls):
        output = ''
        properties = cls.SCHEMA.get('properties', {})
        first_undocumented = True
        for p in sorted(properties):
            if p not in cls.DOC:
                if first_undocumented:
                    cls.DOC.append('# Undocumented')
                    first_undocumented = False
                cls.DOC.append(p)
        # Generate TOC
        output += '# Table of Contents <!-- omit in toc -->' + '\n\n'
        for doc in cls.DOC:
            if doc[0] == '#':
                matches = re.match(r'^(#+) ?(.*)$', doc)
                indent = '  ' * (len(matches.group(1)) - 1)
                output += indent + '- [' + doc.replace('#', '').strip() + '](' + cls._markdown_link(doc) + ')\n'
        output += '\n'
        # Detail
        for doc in cls.DOC:
            if doc[0] == '#':
                output += doc + '\n\n'
            elif doc in properties:
                example = cls.EXAMPLE_YAML_HEADER
                if '_example' in properties[doc]:
                    if properties[doc]['_example'].startswith('\n'):
                        example += '  ' + doc + ':' + properties[doc]['_example'] + '\n'
                    else:
                        example += '  ' + doc + ': ' + properties[doc]['_example'] + '\n'
                elif 'enum' in properties[doc]:
                    enum = properties[doc]['enum']
                    example += ('  ' + doc + ': ' + str(enum[0]) +
                                ' # one of ' + ', '.join([str(item) for item in enum]) + '\n')
                elif properties[doc]['type'] == 'boolean':
                    example += '  ' + doc + ': true # or false\n'
                elif properties[doc]['type'] == 'integer':
                    example += '  ' + doc + ': 42\n'
                elif properties[doc]['type'] == 'array':
                    example += '  ' + doc + ': [My ' + doc.replace('_', ' ') + ']\n'
                else:
                    example += '  ' + doc + ': My ' + doc.replace('_', ' ') + '\n'
                output += '`' + doc + '` ' + properties[doc].get('description', 'Undocumented') + ':\n'
                output += '```yaml\n' + example + '```\n\n'
                if '_doc_link' in properties[doc]:
                    output += 'More information can be found [here]({0})\n\n'.format(properties[doc]['_doc_link'])
            else:
                output += '`' + doc + '` *Undocumented*.\n\n'
        return output
