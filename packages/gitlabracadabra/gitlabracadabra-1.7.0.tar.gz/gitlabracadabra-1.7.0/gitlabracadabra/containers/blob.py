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

from gitlabracadabra.containers.with_digest import WithDigest


class Blob(WithDigest):
    """Registry Blob."""

    @property
    def registry_path(self) -> str:
        """Get relative path of the blob in the registry.

        Returns:
            The path.
        """
        return '/v2/{0}/blobs/{1}'.format(self.manifest_name, self.digest)

    def register(self) -> None:
        """Notify the registry that the Digest exists."""
        self.registry.register_blob(self)
