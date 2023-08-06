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

from github import Github as PyGithub
from github.GithubException import UnknownObjectException
from github.GitRelease import GitRelease

from gitlabracadabra.matchers import Matcher
from gitlabracadabra.packages.package_file import PackageFile
from gitlabracadabra.packages.source import Source


logger = getLogger(__name__)


class Github(Source):
    """Github source."""

    def __init__(
        self,
        *,
        log_prefix: str = '',
        full_name: str,
        package_name: Optional[str] = None,
        tags: Optional[list[str]] = None,
        semver: Optional[str] = None,
        latest_release: Optional[bool] = None,
        tarball: Optional[bool] = None,
        zipball: Optional[bool] = None,
        assets: Optional[list[str]] = None,
    ) -> None:
        """Initialize a Github source.

        Args:
            log_prefix: Log prefix.
            full_name: Repository full name. Mandatory.
            package_name: Destination package name (defaults to repository name).
            tags: List of tags.
            semver: Semantic version applied on tags.
            latest_release: Get latest release.
            tarball: Get repository tarball (defaults to False).
            zipball: Get repository zip (defaults to False).
            assets: List of assets (None by default).
        """
        self._log_prefix = log_prefix
        self._full_name = full_name
        self._package_name = package_name or full_name.split('/').pop()
        self._tags = tags or []
        self._semver = semver
        self._latest_release = latest_release or False
        self._tarball = tarball or False
        self._zipball = zipball or False
        self._assets = assets or []

        self._repo = PyGithub().get_repo(self._full_name, lazy=True)
        self._all_releases: Optional[dict[str, GitRelease]] = None
        self._matching_releases: Optional[dict[str, GitRelease]] = None

    def __str__(self) -> str:
        """Return string representation.

        Returns:
            A string.
        """
        return 'Github repository (full_name={0})'.format(self._full_name)

    @property
    def package_files(self) -> list[PackageFile]:
        """Return list of package files.

        Returns:
            List of package files.
        """
        package_files: list[PackageFile] = []
        for release in self._get_matching_releases().values():
            self._append_package_file_from_release(package_files, release)
        return package_files

    def _get_matching_releases(self) -> dict[str, GitRelease]:
        if self._matching_releases is None:
            matches = Matcher(
                self._tags,
                self._semver,
                log_prefix=self._log_prefix,
            ).match(
                self._get_all_tag_names,
            )
            self._matching_releases = {}
            for match in matches:
                self._append_matching_release(match[0])
            if self._latest_release:
                try:
                    latest_release = self._repo.get_latest_release()
                    self._matching_releases[latest_release.tag_name] = latest_release
                except UnknownObjectException as err2:
                    logger.warning(
                        '%sError getting package files from repository %s, latest release: %s %s',
                        self._log_prefix,
                        self._full_name,
                        err2.status,
                        err2.data.get('message'),
                    )
        return self._matching_releases

    def _get_all_tag_names(self) -> list[str]:
        return list(self._get_all_releases().keys())

    def _get_all_releases(self) -> dict[str, GitRelease]:
        if self._all_releases is None:
            self._all_releases = {}
            for release in self._repo.get_releases():
                self._all_releases[release.tag_name] = release
        return self._all_releases

    def _append_matching_release(self, tag_name: str) -> None:
        if self._all_releases is None:
            try:
                self._matching_releases[tag_name] = self._repo.get_release(tag_name)  # type: ignore
            except UnknownObjectException as err:
                logger.warning(
                    '%sError getting package files from repository %s, release with tag %s: %s %s',
                    self._log_prefix,
                    self._full_name,
                    tag_name,
                    err.status,
                    err.data.get('message'),
                )
        else:
            self._matching_releases[tag_name] = self._all_releases[tag_name]  # type: ignore

    def _append_package_file_from_release(self, package_files: list[PackageFile], release: GitRelease) -> None:

        if self._tarball:
            package_files.append(PackageFile(
                release.tarball_url,
                'raw',
                self._package_name,
                release.tag_name,
                '{0}-{1}.tar.gz'.format(self._full_name.split('/').pop(), release.tag_name),
            ))
        if self._zipball:
            package_files.append(PackageFile(
                release.zipball_url,
                'raw',
                self._package_name,
                release.tag_name,
                '{0}-{1}.zip'.format(self._full_name.split('/').pop(), release.tag_name),
            ))
        if self._assets:
            try:
                # https://github.com/PyGithub/PyGithub/pull/1899
                assets = release.assets  # type: ignore
            except AttributeError:
                assets = release.get_assets()
            assets = {asset.name: asset.browser_download_url for asset in assets}
            for asset_name in self._assets:
                try:
                    package_files.append(PackageFile(
                        assets[asset_name],
                        'raw',
                        self._package_name,
                        release.tag_name,
                        asset_name,
                    ))
                except KeyError:
                    logger.warning(
                        '%sAsset "%s" not found from repository %s in release with tag %s',
                        self._log_prefix,
                        asset_name,
                        self._full_name,
                        release.tag_name,
                    )
