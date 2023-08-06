#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2013-2017 Gauvain Pocentek <gauvain@pocentek.net>
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

from __future__ import print_function

import argparse
import logging
import sys

import gitlabracadabra
import gitlabracadabra.parser
from gitlabracadabra.gitlab.connections import GitlabConnections


logger = logging.getLogger(__name__)


def _get_parser():
    parser = argparse.ArgumentParser(
        description='GitLabracadabra')
    parser.add_argument('--version', help='Display the version.',
                        action='store_true')
    parser.add_argument('-v', '--verbose', '--fancy',
                        help='Verbose mode',
                        action='store_true')
    parser.add_argument('-d', '--debug',
                        help='Debug mode (display HTTP requests)',
                        action='store_true')
    parser.add_argument('--logging-format',
                        help='Logging format',
                        choices=['short', 'long'],
                        default='short')
    parser.add_argument('-c', '--config-file', action='append',
                        help=('Configuration file to use. Can be used '
                              'multiple times.'))
    parser.add_argument('-g', '--gitlab',
                        help=('Which configuration section should '
                              'be used. If not defined, the default selection '
                              'will be used.'),
                        required=False)
    parser.add_argument('--dry-run',
                        help='Dry run',
                        action='store_true')
    parser.add_argument('--doc-markdown',
                        help=('Output the help for the given type (project, '
                              'group, user, application_settings) as '
                              'Markdown.'))
    parser.add_argument('action_files',
                        help='Action file. Can be used multiple times.',
                        metavar='ACTIONFILE.yml',
                        nargs='*',
                        default=['gitlabracadabra.yml'])

    return parser


def main():
    parser = _get_parser()

    args = parser.parse_args(sys.argv[1:])

    if args.version:
        print(gitlabracadabra.__version__)
        sys.exit(0)

    config_files = args.config_file
    gitlab_id = args.gitlab
    verbose = args.verbose
    debug = args.debug

    log_level = logging.WARNING
    if verbose:
        log_level = logging.INFO
    if debug:
        log_level = logging.DEBUG
    if args.logging_format == 'long':
        logging_format = '%(asctime)s [%(process)d] %(levelname)-8.8s %(name)s: %(message)s'
    else:
        logging_format = '%(levelname)-8.8s %(message)s'
    logging.basicConfig(format=logging_format, level=log_level)

    if args.doc_markdown:
        cls = gitlabracadabra.parser.GitlabracadabraParser.get_class_for(args.doc_markdown)
        print(cls.doc_markdown())
        sys.exit(0)

    try:
        GitlabConnections().load(gitlab_id, config_files, debug)
    except Exception as e:  # noqa: B902
        logger.error(str(e))  # noqa: G200
        sys.exit(1)

    # First pass: Load data and preflight checks
    objects = {}
    has_errors = False
    for action_file in args.action_files:
        if action_file.endswith('.yml') or action_file.endswith('.yaml'):
            parser = gitlabracadabra.parser.GitlabracadabraParser.from_yaml_file(action_file)
        else:
            logger.error('Unhandled file: %s', action_file)
            has_errors = True
            continue
        logger.debug('Parsing file: %s', action_file)
        objects[action_file] = parser.objects()
        for k, v in sorted(objects[action_file].items()):
            if len(v.errors()) > 0:
                for error in v.errors():
                    logger.error('Error in %s (%s %s): %s', action_file, v._type_name(), k, str(error))
                has_errors = True

    if has_errors:
        logger.error('Preflight checks errors. Exiting')
        sys.exit(1)

    # Second pass:
    for action_file in args.action_files:
        for _name, obj in sorted(objects[action_file].items()):
            obj.process(args.dry_run)


if __name__ == '__main__':
    main()  # type: ignore
