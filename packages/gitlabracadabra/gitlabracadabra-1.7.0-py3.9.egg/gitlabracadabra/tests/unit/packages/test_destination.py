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

from re import escape as re_escape
from typing import Optional
from unittest.mock import MagicMock, call, patch

from requests import Response, Session
from requests.auth import AuthBase
from requests.utils import set_environ

from gitlabracadabra.packages.destination import Destination, Stream
from gitlabracadabra.packages.helm import Helm
from gitlabracadabra.packages.package_file import PackageFile
from gitlabracadabra.tests.case import TestCase


class TestDestination(TestCase):
    """Test Destination class."""

    def test_import_source_not_found(self):
        """Test import_source method, with unexisting source."""
        with patch('gitlabracadabra.packages.destination.logger', autospec=True) as logger:
            destination = Destination(log_prefix='[foobar] ')
            source = MagicMock
            source.package_files = [PackageFile('https://source.example.org/not_exists.tgz', 'raw', 'foobar')]
            with patch.object(Session, 'request') as request_mock:
                request_mock.side_effect = self._mocked_request
                destination.import_source(source, dry_run=False)
                self.assertEqual(request_mock.mock_calls, [
                    call('HEAD', 'https://source.example.org/not_exists.tgz'),
                ])
            self.assertEqual(logger.mock_calls, [
                call.warning(
                    '%sNOT uploading %s package file "%s" from "%s" version %s (%s): source not found',
                    '[foobar] ',
                    'raw',
                    'not_exists.tgz',
                    'foobar',
                    '0',
                    'https://source.example.org/not_exists.tgz',
                ),
            ])

    def test_import_destination_exists(self):
        """Test import_source method, with existing destination."""
        with patch('gitlabracadabra.packages.destination.logger', autospec=True) as logger:
            destination = Destination(log_prefix='[foobar] ')
            destination.head_url = MagicMock()
            destination.head_url.return_value = 'https://destination.example.org/foobar.tgz'
            source = MagicMock
            source.package_files = [PackageFile('https://source.example.org/foobar.tgz', 'raw', 'foobar')]
            with patch.object(Session, 'request') as request_mock:
                request_mock.side_effect = self._mocked_request
                destination.import_source(source, dry_run=False)
                self.assertEqual(request_mock.mock_calls, [
                    call('HEAD', 'https://source.example.org/foobar.tgz'),
                    call('HEAD', 'https://destination.example.org/foobar.tgz', headers=None, auth=None),
                ])
            self.assertEqual(logger.mock_calls, [])

    def test_import_dry_run(self):
        """Test import_source method, with dry_run."""
        with patch('gitlabracadabra.packages.destination.logger', autospec=True) as logger:
            destination = Destination(log_prefix='[foobar] ')
            destination.head_url = MagicMock()
            destination.head_url.return_value = 'https://destination.example.org/not_exists.tgz'
            source = MagicMock
            source.package_files = [PackageFile('https://source.example.org/foobar.tgz', 'raw', 'foobar')]
            with patch.object(Session, 'request') as request_mock:
                request_mock.side_effect = self._mocked_request
                destination.import_source(source, dry_run=True)
                self.assertEqual(request_mock.mock_calls, [
                    call('HEAD', 'https://source.example.org/foobar.tgz'),
                    call('HEAD', 'https://destination.example.org/not_exists.tgz', headers=None, auth=None),
                ])
            self.assertEqual(logger.mock_calls, [
                call.info(
                    '%sNOT uploading %s package file "%s" from "%s" version %s (%s): Dry run',
                    '[foobar] ',
                    'raw',
                    'foobar.tgz',
                    'foobar',
                    '0',
                    'https://source.example.org/foobar.tgz',
                ),
            ])

    def test_import_source_proxy_error(self):
        """Test import_source method, with ProxyError raised."""
        with patch('gitlabracadabra.packages.destination.logger', autospec=True) as logger:
            destination = Destination(log_prefix='[foobar] ')
            source = MagicMock
            source.package_files = [PackageFile('https://source.example.org/anything.tgz', 'raw', 'foobar')]
            with set_environ('HTTPS_PROXY', 'http://localhost:42'):
                destination.import_source(source, dry_run=False)
            _, args, _ = logger.mock_calls[0]
            msg = args[8]
            self.assertRegexpMatches(msg, re_escape(
                'ProxyError(MaxRetryError("HTTPSConnectionPool(host=\'source.example.org\', port=443): Max retries exceeded with url: /anything.tgz (Caused by ProxyError(\'Cannot connect to proxy.\', NewConnectionError(\'<urllib3.connection.HTTPSConnection object at 0x7f9b3ef3c8e0>: Failed to establish a new connection: [Errno 111] Connection refused\')))',
            ).replace(
                '0x7f9b3ef3c8e0',
                '0x[0-9A-Fa-f]+',
            ).replace(
                r'urllib3\.connection\.HTTPSConnection',
                r'urllib3\.connection\.(Verified)?HTTPSConnection',
            ))
            self.assertEqual(logger.mock_calls, [
                call.warning(
                    '%sError uploading %s package file "%s" from "%s" version %s (%s %s): %s',
                    '[foobar] ',
                    'raw',
                    'anything.tgz',
                    'foobar',
                    '0',
                    'HEAD',
                    'https://source.example.org/anything.tgz',
                    msg,
                ),
            ])

    def test_import_source_proxy_error2(self):
        """Test import_source method, with ProxyError raised while retrieving package files."""
        with patch('gitlabracadabra.packages.destination.logger', autospec=True) as logger:
            destination = Destination(log_prefix='[foobar] ')
            source = Helm(log_prefix='[foobar] ', repo_url='https://source.example.org', package_name='foo')
            with set_environ('HTTPS_PROXY', 'http://localhost:42'):
                destination.import_source(source, dry_run=False)
            _, args, _ = logger.mock_calls[0]
            msg = args[5]
            self.assertRegexpMatches(msg, re_escape(
                'ProxyError(MaxRetryError("HTTPSConnectionPool(host=\'source.example.org\', port=443): Max retries exceeded with url: /index.yaml (Caused by ProxyError(\'Cannot connect to proxy.\', NewConnectionError(\'<urllib3.connection.HTTPSConnection object at 0x7f9b3ef3c8e0>: Failed to establish a new connection: [Errno 111] Connection refused\')))',
            ).replace(
                '0x7f9b3ef3c8e0',
                '0x[0-9A-Fa-f]+',
            ).replace(
                r'urllib3\.connection\.HTTPSConnection',
                r'urllib3\.connection\.(Verified)?HTTPSConnection',
            ))
            self.assertEqual(logger.mock_calls, [
                call.warning(
                    '%sError retrieving package files list from %s (%s %s): %s',
                    '[foobar] ',
                    str(source),
                    'GET',
                    'https://source.example.org/index.yaml',
                    msg,
                ),
            ])

    def test_import_upload(self):
        """Test import_source method, without dry_run."""
        with patch('gitlabracadabra.packages.destination.logger', autospec=True) as logger:
            destination = Destination(log_prefix='[foobar] ')
            destination.head_url = MagicMock()
            destination.head_url.return_value = 'https://destination.example.org/not_exists.tgz'
            source = MagicMock
            source.package_files = [PackageFile('https://source.example.org/foobar.tgz', 'raw', 'foobar')]
            with patch.object(Session, 'request') as request_mock:
                request_mock.side_effect = self._mocked_request
                destination.import_source(source, dry_run=False)
                with patch.object(Stream, '__eq__') as stream_eq_mock:
                    stream_eq_mock.return_value = True
                    self.assertEqual(request_mock.mock_calls, [
                        call('HEAD', 'https://source.example.org/foobar.tgz'),
                        call('HEAD', 'https://destination.example.org/not_exists.tgz', headers=None, auth=None),
                        call('GET', 'https://source.example.org/foobar.tgz', stream=True, headers={'Accept-Encoding': '*'}),
                        call('PUT', 'https://destination.example.org/not_exists.tgz', data=Stream('a file-like object'), headers=None, auth=None),  # noqa: E501
                    ])
            self.assertEqual(logger.mock_calls, [
                call.info(
                    '%sUploading %s package file "%s" from "%s" version %s (%s)',
                    '[foobar] ',
                    'raw',
                    'foobar.tgz',
                    'foobar',
                    '0',
                    'https://source.example.org/foobar.tgz',
                ),
            ])

    def _mocked_request(
        self,
        method: str,
        url: str,
        data: Optional[Stream] = None,  # noqa: WPS110
        headers: Optional[dict[str, str]] = None,
        stream: Optional[bool] = None,
        auth: Optional[AuthBase] = None,
    ) -> Response:
        response = Response()
        if method in {'HEAD', 'GET'}:
            if url in {'https://source.example.org/foobar.tgz', 'https://destination.example.org/foobar.tgz'}:
                response.status_code = 200
                if stream is True:
                    response.raw = 'a file-like object'
            else:
                response.status_code = 404
        elif method == 'PUT':
            if url == 'https://destination.example.org/not_exists.tgz':
                response.status_code = 201
        return response
