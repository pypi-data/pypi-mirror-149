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

from json import loads as json_loads
from typing import TYPE_CHECKING, Any, Optional

from gitlabracadabra.containers.const import MANIFEST
from gitlabracadabra.containers.with_digest import WithDigest


if TYPE_CHECKING:
    from gitlabracadabra.containers.registry_importer import RegistryImporter


class ManifestBase(WithDigest):
    """Base methods for manifest or manifest list."""

    supported_mime_types = MANIFEST

    def __init__(
        self,
        registry: RegistryImporter,
        manifest_name: str,
        digest: Optional[str] = None,
        *,
        size: Optional[int] = None,
        mime_type: Optional[str] = None,
        tag: str = 'latest',
    ) -> None:
        """Instanciate a manifest.

        Args:
            registry: Registry.
            manifest_name: Manifest name (Example: library/debian).
            digest: Digest.
            size: Size.
            mime_type: Content-Type / mediaType.
            tag: Manifest tag (Example: latest).
        """
        super().__init__(registry, manifest_name, digest, size=size, mime_type=mime_type)
        self.tag = tag or 'latest'
        self._json = None
        self.platform = None
        self._retrieve_mehod = 'get'

    @property
    def json(self) -> Any:
        """Get JSON.

        Returns:
            JSON.
        """
        if self._json is None:
            self._ensure_cached()
            with self as opened_manifest:
                self._json = json_loads(opened_manifest.read().decode('utf-8'))
        return self._json

    @property
    def registry_path(self) -> str:
        """Get relative path of the manifest in the registry.

        Returns:
            The path.
        """
        if self._digest is not None:
            return '/v2/{0}/manifests/{1}'.format(self.manifest_name, self._digest)
        return '/v2/{0}/manifests/{1}'.format(self.manifest_name, self.tag)

    def __str__(self) -> str:
        """Get string representation.

        Returns:
            The full reference
            (docker.io/library/busybox:latest@sha256:c6b45a95f932202dbb27c31333c4789f45184a744060f6e569cc9d2bf1b9ad6f).
        """
        return '{0}/{1}:{2}{3}'.format(
            self.registry.hostname,
            self.manifest_name,
            self.tag,
            '@{0}'.format(self._digest) if self._digest else '',
        )
