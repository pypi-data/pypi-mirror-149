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

from gitlabracadabra.containers.blob import Blob
from gitlabracadabra.containers.manifest import Manifest
from gitlabracadabra.containers.registry_importer import RegistryImporter


class Registry(RegistryImporter):
    """Container registry."""

    def manifest(self, manifest_name: str, tag: str = 'latest') -> Manifest:
        """Connect.

        Args:
            manifest_name: Manifest name. Example: 'library/debian'.
            tag: A tag. Example: 'latest'.

        Returns:
            A Manifest object.
        """
        return Manifest(self, manifest_name, tag=tag)

    def blob(self, manifest_name: str, digest: str) -> Blob:
        """Connect.

        Args:
            manifest_name: Manifest name. Example: 'library/debian'.
            digest: A digest. Example: 'latest'.

        Returns:
            A Manifest object.
        """
        return Blob(self, manifest_name, digest)
