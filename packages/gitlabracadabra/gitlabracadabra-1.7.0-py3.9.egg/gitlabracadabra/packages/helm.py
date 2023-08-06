# -*- coding: utf-8 -*-
#
# Copyright (C) 2019-2021 Mathieu Parent <math.parent@gmail.com>
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

from logging import getLogger
from typing import Optional
from urllib.parse import urljoin

from requests import Session, codes
from requests.adapters import HTTPAdapter
from yaml import safe_load as yaml_safe_load

from gitlabracadabra.matchers import Matcher
from gitlabracadabra.packages.package_file import PackageFile
from gitlabracadabra.packages.source import Source


logger = getLogger(__name__)


class Helm(Source):
    """Helm repository."""

    def __init__(  # noqa: WPS211
        self,
        *,
        log_prefix: str = '',
        repo_url: str,
        package_name: str,
        versions: Optional[list[str]] = None,
        semver: Optional[str] = None,
        limit: Optional[int] = 1,
        channel: Optional[str] = None,
    ) -> None:
        """Initialize a Helm repository object.

        Args:
            log_prefix: Log prefix.
            repo_url: Helm repository URL.
            package_name: Package name.
            versions: List of versions.
            semver: Semantic version.
            limit: Keep at most n latest versions.
            channel: Destination channel.
        """
        self._log_prefix = log_prefix
        self._repo_url = repo_url
        self._package_name = package_name
        self._versions = versions or ['/.*/']
        self._semver = semver or '*'
        self._limit = limit
        self._channel = channel or 'stable'

        self._session = Session()
        self._session.mount('http://', HTTPAdapter(max_retries=3))
        self._session.mount('https://', HTTPAdapter(max_retries=3))

    def __str__(self) -> str:
        """Return string representation.

        Returns:
            A string.
        """
        return 'Helm charts repository (url={0})'.format(self._repo_url)

    @property  # noqa: WPS210
    def package_files(self) -> list[PackageFile]:  # noqa: WPS210
        """Return list of package files.

        Returns:
            List of package files.
        """
        package_entries = self._get_helm_index().get('entries', {})
        package_matches = Matcher(
            self._package_name,
            None,
            log_prefix=self._log_prefix,
        ).match(
            list(package_entries.keys()),
        )
        package_files: list[PackageFile] = []
        for package_match in package_matches:
            package_entry = package_entries[package_match.group(0)]
            package_versions = {package_dict.get('version', '0'): package_dict for package_dict in package_entry}
            matches = Matcher(
                self._versions,
                self._semver,
                self._limit,
                log_prefix=self._log_prefix,
            ).match(
                list(package_versions.keys()),
            )
            for match in matches:
                package_files.append(self._package_file(package_versions[match[0]]))
        if not package_files:
            logger.info(
                '%sPackage not found %s for Helm index %s',
                self._log_prefix,
                self._package_name,
                self._repo_index_url,
            )
        return package_files

    def _get_helm_index(self) -> dict:
        index_response = self._session.request('get', self._repo_index_url)
        if index_response.status_code != codes['ok']:
            logger.warning(
                '%sUnexpected HTTP status for Helm index %s: received %i %s',
                self._log_prefix,
                self._repo_index_url,
                index_response.status_code,
                index_response.reason,
            )
            return {}
        return yaml_safe_load(index_response.content)  # type: ignore

    @property
    def _repo_index_url(self) -> str:
        return '{0}/index.yaml'.format(self._repo_url)

    def _package_file(self, package_dict: dict) -> PackageFile:
        url = urljoin(self._repo_index_url, package_dict.get('urls', []).pop())
        return PackageFile(
            url,
            'helm',
            package_dict.get('name', self._package_name),
            package_dict.get('version', '0'),
            metadata={'channel': self._channel},
        )
