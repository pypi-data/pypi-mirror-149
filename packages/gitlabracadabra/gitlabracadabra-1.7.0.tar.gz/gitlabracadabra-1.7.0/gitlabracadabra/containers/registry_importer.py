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

from logging import getLogger
from typing import Dict, Optional

from requests import HTTPError, codes

from gitlabracadabra.containers.blob import Blob
from gitlabracadabra.containers.const import (
    DOCKER_MANIFEST_SCHEMA1,
    DOCKER_MANIFEST_SCHEMA1_SIGNED,
    DOCKER_MANIFEST_SCHEMA2,
    DOCKER_MANIFEST_SCHEMA2_LIST,
    OCI_IMAGE_INDEX,
    OCI_IMAGE_MANIFEST,
)
from gitlabracadabra.containers.manifest import Manifest
from gitlabracadabra.containers.registry_session import RegistrySession
from gitlabracadabra.containers.scope import PULL, PUSH_PULL
from gitlabracadabra.containers.with_blobs import WithBlobs


logger = getLogger(__name__)


class ImportStats(object):  # noqa: WPS230
    """Import statistics."""

    __slots__ = (
        'uploaded_count',
        'mounted_count',
        'existing_count',
        'uploaded_size',
        'mounted_size',
        'existing_size',

        'uploaded_manifests_count',
        'existing_manifests_count',
    )

    def __init__(self) -> None:
        """Initialize."""
        self.uploaded_count = 0
        self.mounted_count = 0
        self.existing_count = 0
        self.uploaded_size = 0
        self.mounted_size = 0
        self.existing_size = 0

        self.uploaded_manifests_count = 0
        self.existing_manifests_count = 0

    @property
    def blobs_count(self) -> int:
        """Get total blob count.

        Returns:
            The number of blobs uploaded + mounted + existing.
        """
        return self.uploaded_count + self.mounted_count + self.existing_count

    @property
    def blobs_size(self) -> int:
        """Get total blob size.

        Returns:
            The size of blobs uploaded + mounted + existing.
        """
        return self.uploaded_size + self.mounted_size + self.existing_size

    @property
    def manifests_count(self) -> int:
        """Get total manifest count.

        Returns:
            The number of manifest uploaded + existing + skipped.
        """
        return self.uploaded_manifests_count + self.existing_manifests_count

    def any_stat(self) -> bool:
        """Test if any stat is above zero.

        Returns:
            True if any statistic is non-zero.
        """
        return any((
            self.uploaded_count,
            self.mounted_count,
            # self.existing_count,
            self.uploaded_size,
            self.mounted_size,
            # self.existing_size,
            self.uploaded_manifests_count,
            # self.existing_manifests_count
        ))


class RegistryImporter(RegistrySession, WithBlobs):
    """Container registry importer methods."""

    def blob_from_digest(self, digest: str, *, preferred_manifest_name: str) -> Optional[Blob]:
        """Return a Blob with the given digest, within the preferred manifest if possible.

        Args:
            digest: Digest of Blob to look for.
            preferred_manifest_name: Preferred manifest name.

        Returns:
            A Blob with the expected digest, or None.
        """
        manifest_names = self._blobs.get(digest, [])
        if not len(manifest_names):
            return None
        if preferred_manifest_name in manifest_names:
            return Blob(self, preferred_manifest_name, digest, size=self._sizes[digest])
        return Blob(self, manifest_names[0], digest, size=self._sizes[digest])

    def import_manifest(  # noqa: WPS231
        self,
        source: Manifest,
        manifest_name: Optional[str] = None,
        tag: Optional[str] = None,
        *,
        platform: Optional[Dict] = None,
        log_prefix: str = '',
        dry_run: bool = False,
    ) -> None:
        """Import a manifest.

        Args:
            source: Source manifest.
            manifest_name: Target manifest name (defaults to source's).
            tag: Target manifest tag (defaults to source's).
            platform: 'all' or a specific platform, defaults to linux/amd64.
            log_prefix: Log prefix.
            dry_run: Dry run.

        Raises:
            ValueError: Unsupported media type.
        """
        stats = ImportStats()
        if manifest_name is None:
            manifest_name = source.manifest_name
        if tag is None:
            tag = source.tag
        if platform is None:
            platform = {'architecture': 'amd64', 'os': 'linux'}
        try:
            source_mime_type = source.mime_type
        except HTTPError as err:
            logger.warning(  # noqa: G200
                '%s%s NOT imported as %s:%s: %s',
                log_prefix,
                str(source),
                manifest_name,
                tag,
                str(err),
            )
            return
        try:
            if source_mime_type in {DOCKER_MANIFEST_SCHEMA2_LIST, OCI_IMAGE_INDEX}:
                self._import_manifest_list(source, manifest_name, tag, platform=platform, stats=stats, dry_run=dry_run)
            elif source_mime_type in {DOCKER_MANIFEST_SCHEMA2, OCI_IMAGE_MANIFEST}:
                self._import_manifest(source, manifest_name, tag, stats=stats, dry_run=dry_run)
            elif source_mime_type in {DOCKER_MANIFEST_SCHEMA1, DOCKER_MANIFEST_SCHEMA1_SIGNED}:
                self._import_manifest_v1(source, manifest_name, tag, stats=stats, dry_run=dry_run)
            else:
                raise ValueError('Unsupported media type: {0}'.format(source_mime_type))
        except HTTPError as err2:
            logger.warning(  # noqa: G200
                '%s%s NOT imported as %s:%s: %s',
                log_prefix,
                str(source),
                manifest_name,
                tag,
                str(err2),
            )
            return

        if stats.any_stat():
            logger.info(
                '%s%s %simported as %s:%s (%s, %s, %s)',
                log_prefix,
                str(source),
                'NOT ' if dry_run else '',
                manifest_name,
                tag,
                '{0}+{1}={2} uploaded+existing manifests'.format(
                    stats.uploaded_manifests_count,
                    stats.existing_manifests_count,
                    stats.manifests_count,
                ),
                '{0}+{1}+{2}={3} uploaded+mounted+existing blobs'.format(
                    stats.uploaded_count,
                    stats.mounted_count,
                    stats.existing_count,
                    stats.blobs_count,
                ),
                '{0}+{1}+{2}={3} uploaded+mounted+existing blobs size'.format(
                    stats.uploaded_size,
                    stats.mounted_size,
                    stats.existing_size,
                    stats.blobs_size,
                ),
            )

    def _import_manifest_list(
        self,
        source: Manifest,
        manifest_name: str,
        tag: str,
        *,
        platform: dict,
        stats: ImportStats,
        dry_run: bool,
    ) -> None:
        if platform == 'all' or source.forced_digest:
            self._import_manifest_list_all(source, manifest_name, stats=stats, dry_run=dry_run)
        else:
            for manifest in source.manifests():  # noqa:WPS440
                if manifest.platform == platform:
                    self._import_manifest(manifest, manifest_name, tag, stats=stats, dry_run=dry_run)
                    return
            raise ValueError('Platform {0} not found in manifest {1}'.format(platform, source))

    def _import_manifest_list_all(
        self,
        source: Manifest,
        manifest_name: str,
        *,
        stats: ImportStats,
        dry_run: bool,
    ) -> None:
        dest = Manifest(
            self,
            manifest_name,
            size=source.size,
            mime_type=source.mime_type,
            tag=source.tag,
        )
        if dest.exists() and dest.digest == source.digest:
            # Short path if manifest already exists
            stats.existing_manifests_count += 1
            self.register_manifest_blobs(dest)
            return
        for manifest in source.manifests():
            self._import_manifest(manifest, manifest_name, manifest.digest, stats=stats, dry_run=dry_run)
        if not dry_run:
            self._upload_manifest(source, dest, stats=stats)
        stats.uploaded_manifests_count += 1

    def _import_manifest(
        self,
        source: Manifest,
        manifest_name: str,
        tag: str,
        *,
        stats: ImportStats,
        dry_run: bool,
    ) -> None:
        # https://docs.docker.com/registry/spec/api/#pushing-an-image
        manifest = Manifest(
            self,
            manifest_name,
            size=source.size,
            mime_type=source.mime_type,
            tag=tag,
        )
        if manifest.exists() and manifest.digest == source.digest:
            # Short path if manifest already exists
            stats.existing_manifests_count += 1
            self.register_manifest_blobs(manifest)
            return

        self._upload_blob_if_needed(
            source,
            manifest_name,
            source.json.get('config'),
            stats=stats,
            dry_run=dry_run,
        )
        for layer_json in source.json.get('layers'):
            self._upload_blob_if_needed(source, manifest_name, layer_json, stats=stats, dry_run=dry_run)
        if not dry_run:
            self._upload_manifest(source, manifest, stats=stats)
        stats.uploaded_manifests_count += 1

    def _import_manifest_v1(
        self,
        source: Manifest,
        manifest_name: str,
        tag: str,
        *,
        stats: ImportStats,
        dry_run: bool,
    ) -> None:
        # https://docs.docker.com/registry/spec/api/#pushing-an-image
        manifest = Manifest(
            self,
            manifest_name,
            size=source.size,
            mime_type=source.mime_type,
            tag=tag,
        )
        if manifest.exists() and manifest.digest == source.digest:
            # Short path if manifest already exists
            stats.existing_manifests_count += 1
            self.register_manifest_blobs(manifest)
            return

        for fs_layer_json in source.json.get('fsLayers'):
            layer_json = {
                'digest': fs_layer_json['blobSum'],
                'size': -1,
                'mediaType': None,
            }
            self._upload_blob_if_needed(source, manifest_name, layer_json, stats=stats, dry_run=dry_run)
        if not dry_run:
            self._upload_manifest(source, manifest, stats=stats)
        stats.uploaded_manifests_count += 1

    def _upload_blob_if_needed(
        self,
        source: Manifest,
        manifest_name: str,
        json: Dict,
        *,
        stats: ImportStats,
        dry_run: bool,
    ) -> None:
        """Upload or mount a blob as needed.

        Args:
            source: Source manifest.
            manifest_name: Destination manifest name.
            json: Blob json (as dict).
            stats: Import statistics.
            dry_run: Dry run.
        """
        blob = self._blob_from_json(manifest_name, json)
        existing_blob = self.blob_from_digest(blob.digest, preferred_manifest_name=manifest_name)
        if (existing_blob is not None and existing_blob.manifest_name == manifest_name) or blob.exists():
            stats.existing_count += 1
            stats.existing_size += blob.size
        elif existing_blob is not None:
            if not dry_run:
                self._mount_blob(existing_blob, blob, stats=stats)
            stats.mounted_size += existing_blob.size
            stats.mounted_count += 1
        else:
            if not dry_run:
                self._upload_blob(source, blob, stats=stats)
            stats.uploaded_size += blob.size
            stats.uploaded_count += 1
        self.register_blob(blob)

    def _blob_from_json(self, manifest_name: str, json: Dict) -> Blob:
        return Blob(
            self,
            manifest_name,
            json['digest'],
            size=json['size'],
            mime_type=json['mediaType'],
        )

    def _upload_blob(self, source: Manifest, blob: Blob, *, stats: ImportStats) -> None:
        """Upload a blob.

        Args:
            source: Source manifest.
            blob: Destination blob to upload to.
            stats: Import statistics.
        """
        if blob.exists():
            return
        upload_url = self._start_upload(blob)
        if '?' in upload_url:
            blob_upload_url = '{0}&digest={1}'.format(upload_url, blob.digest)
        else:
            blob_upload_url = '{0}?digest={1}'.format(upload_url, blob.digest)
        orig_blob = Blob(
            source.registry,
            source.manifest_name,
            blob.digest,
        )
        with orig_blob:
            chunk_size = 52428800
            self.request(
                'put',
                blob_upload_url,
                data=iter(lambda: orig_blob.read(chunk_size), b''),
                scopes={blob.scope(PUSH_PULL)},
            )

    def _start_upload(self, blob: Blob) -> str:
        response = self.request(
            'post',
            '/v2/{0}/blobs/uploads/'.format(blob.manifest_name),
            scopes={blob.scope(PUSH_PULL)},
        )
        if response.status_code != codes['accepted']:
            raise ValueError('Unexpected status {0}'.format(response.status_code))
        return response.headers['Location']

    def _mount_blob(self, existing_blob: Blob, blob: Blob, *, stats: ImportStats) -> None:
        """Mount a blob.

        Args:
            existing_blob: Existing blob.
            blob: Destination blob to mount to.
            stats: Import statistics.

        Raises:
            ValueError: Unexpected HTTP status.
        """
        response = self.request(
            'post',
            '/v2/{0}/blobs/uploads/?mount={1}&from={2}'.format(
                blob.manifest_name,
                existing_blob.digest,
                existing_blob.manifest_name,
            ),
            scopes={
                blob.scope(PUSH_PULL),
                existing_blob.scope(PULL),
            },
        )
        if response.status_code != codes['created']:
            raise ValueError('Unexpected HTTP status {0}'.format(response.status_code))

    def _upload_manifest(self, source: Manifest, manifest: Manifest, *, stats: ImportStats) -> None:
        with source:
            chunk_size = 52428800
            registry_path = '/v2/{0}/manifests/{1}'.format(manifest.manifest_name, manifest.tag)
            self.request(
                'put',
                registry_path,
                scopes={manifest.scope(PUSH_PULL)},
                data=iter(lambda: source.read(chunk_size), b''),
                content_type=source.mime_type,
            )
