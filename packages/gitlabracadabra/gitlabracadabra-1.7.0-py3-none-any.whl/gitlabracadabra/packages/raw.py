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

from typing import TYPE_CHECKING, Optional

from gitlabracadabra.packages.package_file import PackageFile
from gitlabracadabra.packages.source import Source


if TYPE_CHECKING:
    from typing import TypedDict  # noqa: WPS433
    PackageFileArgs = TypedDict(
        'PackageFileArgs',
        {'url': str, 'package_name': str, 'package_version': str, 'file_name': str},
        total=False,
    )


class RawSource(Source):
    """Raw urls repository."""

    def __init__(
        self,
        *,
        log_prefix: str = '',
        default_url: str,
        default_package_name: Optional[str] = None,
        default_package_version: Optional[str] = None,
        package_files: Optional[list[PackageFileArgs]] = None,
    ) -> None:
        """Initialize a Raw Source object.

        Args:
            log_prefix: Log prefix.
            default_url: Default package file URL.
            default_package_name: Default package name.
            default_package_version: Default package version.
            package_files: Package files.
        """
        self._log_prefix = log_prefix
        self._default_url = default_url
        self._default_package_name = default_package_name or 'unknown'
        self._default_package_version = default_package_version or '0'
        self._package_files: list[PackageFileArgs] = package_files or [{}]

    def __str__(self) -> str:
        """Return string representation.

        Returns:
            A string.
        """
        return 'Raw repository (default_url={0})'.format(self._default_url)

    @property
    def package_files(self) -> list[PackageFile]:
        """Return list of package files.

        Returns:
            List of package files.
        """
        package_files: list[PackageFile] = []
        for package_file_args in self._package_files:
            package_file = self._package_file(package_file_args)
            if package_file:
                package_files.append(package_file)
        return package_files

    def _package_file(self, package_file_args: PackageFileArgs) -> Optional[PackageFile]:
        url = package_file_args.get('url') or self._default_url
        if not url:
            return None
        package_name = package_file_args.get('package_name') or self._default_package_name
        package_version = package_file_args.get('package_version') or self._default_package_version
        file_name = package_file_args.get('file_name')
        default_url = self._default_url.format(
            default_package_name=self._default_package_name,
            default_package_version=self._default_package_version,
            package_name=package_name,
            package_version=package_version,
            file_name=file_name or '{file_name}',
        )
        url = url.format(
            default_url=default_url,
            default_package_name=self._default_package_name,
            default_package_version=self._default_package_version,
            package_name=package_name,
            package_version=package_version,
            file_name=file_name or '{file_name}',
        )
        if not file_name:
            file_name = url.split('/').pop()
        return PackageFile(
            url,
            'raw',
            package_name,
            package_version,
            file_name,
        )
