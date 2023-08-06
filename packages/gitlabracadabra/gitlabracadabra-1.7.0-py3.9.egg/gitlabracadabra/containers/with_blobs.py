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

from typing import TYPE_CHECKING, Dict, List

from gitlabracadabra.containers.const import DOCKER_MANIFEST_SCHEMA2_LIST, OCI_IMAGE_INDEX


if TYPE_CHECKING:
    from gitlabracadabra.containers.blob import Blob
    from gitlabracadabra.containers.manifest import Manifest


class WithBlobs(object):
    """Keep in which manifest blobs are.

    Method blob_from_digest is in RegistryImporter
    """

    def __init__(self) -> None:
        """Initialize which keeps trace in which manifests blobs are."""
        # Cache where blobs are present
        # Dict key is digest, value is a list of manifest names
        self._blobs: Dict[str, List[str]] = {}
        self._sizes: Dict[str, int] = {}

    def register_manifest_blobs(self, manifest: Manifest) -> None:
        """Add all manifest blobs in the blob mapping.

        Args:
            manifest: Manifest.
        """
        if manifest.mime_type in {DOCKER_MANIFEST_SCHEMA2_LIST, OCI_IMAGE_INDEX}:
            # Note: Should we register all blobs from referenced manifests?
            # or only from requested platform?
            return
        for blob in manifest.blobs():
            self.register_blob(blob)

    def register_blob(self, blob: Blob) -> None:
        """Add a blob in the blob mapping.

        Args:
            blob: Blob to register.
        """
        self._register_digest(blob.digest, blob.manifest_name, blob.size)

    def _register_digest(self, digest: str, manifest_name: str, size: int) -> None:
        """Add a blob in the blob mapping by digest and manifest name.

        Args:
            digest: Digest of Blob to register.
            manifest_name: Manifest name of Blob to register.
            size: Blob size.
        """
        if digest not in self._blobs:
            self._blobs[digest] = []
        if manifest_name not in self._blobs[digest]:
            self._blobs[digest].append(manifest_name)
        if digest not in self._sizes:
            self._sizes[digest] = size
