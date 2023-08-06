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

from typing import List

from gitlabracadabra.containers.blob import Blob
from gitlabracadabra.containers.const import (
    DOCKER_MANIFEST_SCHEMA1,
    DOCKER_MANIFEST_SCHEMA1_SIGNED,
    DOCKER_MANIFEST_SCHEMA2,
    DOCKER_MANIFEST_SCHEMA2_LIST,
    OCI_IMAGE_INDEX,
    OCI_IMAGE_MANIFEST,
)
from gitlabracadabra.containers.manifest_base import ManifestBase


class Manifest(ManifestBase):
    """Retrieve Manifest or Manifest list."""

    def manifests(self) -> List[Manifest]:
        """Get manifests of the manifest list.

        Returns:
            A list of manifests.

        Raises:
            ValueError: Unsupported manifest list type.
        """
        if self.mime_type in {DOCKER_MANIFEST_SCHEMA2_LIST, OCI_IMAGE_INDEX}:
            return self._manifests_v2()
        raise ValueError('Unsupported manifest list type {0}'.format(self.mime_type))

    def tag_list(self) -> List[str]:
        """Get tags of the manifest.

        Returns:
            A list of tags (strings).

        Raises:
            ValueError: Expected list got something else.
        """
        response = self._registry.request(
            'get',
            '/v2/{0}/tags/list'.format(self.manifest_name),
            scopes={self.scope()},
        )
        tags = response.json().get('tags')
        if not isinstance(tags, list):
            raise ValueError('Expected list got {0}'.format(type(tags)))
        return tags

    def blobs(self) -> List[Blob]:
        """Get blobs of the manifest.

        Returns:
            A list of blobs.

        Raises:
            ValueError: Unsupported media type.
        """
        if self.mime_type in {DOCKER_MANIFEST_SCHEMA2, OCI_IMAGE_MANIFEST}:
            blobs = []
            for layer_json in self.json.get('layers'):
                blobs.append(Blob(
                    self.registry,
                    self.manifest_name,
                    layer_json['digest'],
                    size=layer_json['size'],
                    mime_type=layer_json['mediaType'],
                ))
            return blobs
        elif self.mime_type in {DOCKER_MANIFEST_SCHEMA1, DOCKER_MANIFEST_SCHEMA1_SIGNED}:
            blobs = []
            for fs_layer_json in self.json.get('fsLayers'):
                blobs.append(Blob(
                    self.registry,
                    self.manifest_name,
                    fs_layer_json['blobSum'],
                    mime_type='application/octet-stream',
                ))
            return blobs
        raise ValueError('Unsupported media type: {0}'.format(self.mime_type))

    def _manifests_v2(self) -> List[Manifest]:
        json = dict(self.json)
        if json['mediaType'] not in {DOCKER_MANIFEST_SCHEMA2_LIST, OCI_IMAGE_INDEX}:
            raise ValueError('Unexpected manifest list type {0}'.format(json['mediaType']))
        if json['schemaVersion'] != 2:
            raise ValueError('Unexpected manifest schema version {0}'.format(json['schemaVersion']))
        manifests = []
        for manifest_json in json['manifests']:
            manifest = Manifest(
                self.registry,
                self.manifest_name,
                digest=manifest_json['digest'],
                size=manifest_json['size'],
                mime_type=manifest_json['mediaType'],
                tag=self.tag,
            )
            manifest.platform = manifest_json['platform']
            manifests.append(manifest)
        return manifests
