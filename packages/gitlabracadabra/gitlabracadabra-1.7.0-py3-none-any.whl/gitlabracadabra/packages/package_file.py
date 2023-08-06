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

from typing import Any, Optional


class PackageFile(object):
    """Package file."""

    def __init__(
        self,
        url: str,
        package_type: str,
        package_name: str,
        package_version: Optional[str] = None,
        file_name: Optional[str] = None,
        *,
        metadata: Optional[dict[str, str]] = None,
    ) -> None:
        """Initialize an package file object.

        Args:
            url: Package URL.
            package_type: Package type.
            package_name: Package name.
            package_version: Package version.
            file_name: Package file name.
            metadata: Package file metadata.
        """
        self._url = url
        self._package_type = package_type
        self._package_name = package_name
        self._package_version = package_version or '0'
        self._file_name = file_name or url.split('/').pop()
        self._metadata = metadata or {}

    @property
    def url(self) -> str:
        """Get URL.

        Returns:
            Package file's source URL.
        """
        return self._url

    @property
    def package_type(self) -> str:
        """Get package type.

        Returns:
            Package type.
        """
        return self._package_type

    @property
    def package_name(self) -> str:
        """Get package name.

        Returns:
            Package name.
        """
        return self._package_name

    @property
    def package_version(self) -> str:
        """Get package version.

        Returns:
            Package version.
        """
        return self._package_version

    @property
    def file_name(self) -> str:
        """Get package file name.

        Returns:
            Package file name.
        """
        return self._file_name

    @property
    def metadata(self) -> dict[str, str]:
        """Get package file metadata.

        Returns:
            Package file metadata.
        """
        return self._metadata

    def __eq__(self, other: Any) -> bool:
        """Test equality.

        Args:
            other: Item to compare with.

        Returns:
            True if all attributes match.
        """
        return self.__dict__ == other.__dict__  # type: ignore # noqa: WPS609

    def __repr__(self) -> str:
        """Representation.

        Returns:
            String representation of the package file.
        """
        return str(self.__dict__)
