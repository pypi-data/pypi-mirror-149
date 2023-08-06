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

from contextlib import contextmanager
from os.path import isfile
from typing import TYPE_CHECKING, Generator
from unittest.mock import call, patch

from gitlabracadabra.containers.blob import Blob
from gitlabracadabra.containers.const import DOCKER_HOSTNAME, DOCKER_MANIFEST_SCHEMA2, DOCKER_MANIFEST_SCHEMA2_LIST
from gitlabracadabra.containers.manifest import Manifest
from gitlabracadabra.containers.registry import Registry
from gitlabracadabra.containers.with_digest import WithDigest
from gitlabracadabra.tests import my_vcr
from gitlabracadabra.tests.case import TestCase


if TYPE_CHECKING:
    from logging import Logger


VERIFY_DIGEST_METHOD = '_verify_digest'
REGISTRY_IMPORTER_LOGGER = 'gitlabracadabra.containers.registry_importer.logger'
REGISTRY_IMPORTER_MESSAGE = '%s%s %simported as %s:%s (%s, %s, %s)'
BLOBS2_0_0_MESSAGE = '2+0+0=2 uploaded+mounted+existing blobs'

DEBIAN_IMAGE = 'library/debian'
BUSYBOX_IMAGE = 'library/busybox'
BUSYBOX_IMAGE_FULL = 'docker.io/library/busybox:latest@{0}'
LATEST = 'latest'


class TestRegistry(TestCase):
    def destination_registry(self):
        registry = Registry('localhost:5000')
        registry._scheme = 'http'  # noqa: WPS437
        return registry

    def assert_with_digest(self, registry, cacheable, digest, size, mime_type):
        self.assertIsInstance(cacheable, WithDigest)
        self.assertEqual(cacheable.registry, registry)
        self.assertEqual(cacheable.digest, digest)
        self.assertEqual(cacheable.size, size)
        self.assertEqual(cacheable.mime_type, mime_type)

    def assert_manifest(self, registry, manifest, digest, size, mime_type):
        self.assert_with_digest(registry, manifest, digest, size, mime_type)
        self.assertIsInstance(manifest, Manifest)
        self.assertIsInstance(manifest.json, dict)
        self.assertTrue(isfile(manifest.cache_path))
        self.assertEqual(manifest.json['mediaType'], mime_type)
        self.assertEqual(manifest.json['schemaVersion'], 2)

    @contextmanager
    def mocked_objects(self) -> Generator[Logger, None, None]:
        with patch.object(WithDigest, VERIFY_DIGEST_METHOD) as verify_digest_mock:
            verify_digest_mock.return_value = None
            with patch(REGISTRY_IMPORTER_LOGGER, autospec=True) as logger:
                yield logger

    @my_vcr.use_cassette
    def test_manifest(self, cass):
        digest = 'sha256:102ab2db1ad671545c0ace25463c4e3c45f9b15e319d3a00a1b2b085293c27fb'
        registry = Registry(DOCKER_HOSTNAME)  # noqa: WPS204
        manifest = registry.manifest(DEBIAN_IMAGE, digest)
        self.assert_manifest(
            registry,
            manifest,
            digest,
            529,
            DOCKER_MANIFEST_SCHEMA2,
        )
        self.assertIsInstance(manifest.json['config'], dict)
        self.assertIsInstance(manifest.json['layers'], list)
        self.assertTrue(cass.all_played)

    @my_vcr.use_cassette
    def test_manifest_list(self, cass):
        registry = Registry(DOCKER_HOSTNAME)
        manifest_list = registry.manifest(DEBIAN_IMAGE)
        self.assert_manifest(
            registry,
            manifest_list,
            'sha256:1092695e843ad975267131f27a2b523128c4e03d2d96574bbdd7cf949ed51475',
            1854,
            DOCKER_MANIFEST_SCHEMA2_LIST,
        )
        self.assertIsInstance(manifest_list.json['manifests'], list)

        manifests = manifest_list.manifests()
        self.assertIsInstance(manifests, list)
        first = manifests[0]
        self.assertFalse(isfile(first.cache_path))
        self.assert_manifest(
            registry,
            first,
            'sha256:102ab2db1ad671545c0ace25463c4e3c45f9b15e319d3a00a1b2b085293c27fb',
            529,
            DOCKER_MANIFEST_SCHEMA2,
        )
        self.assertIsInstance(first, Manifest)
        self.assertEqual(first.platform, {'architecture': 'amd64', 'os': 'linux'})
        self.assertTrue(cass.all_played)

    @my_vcr.use_cassette
    def test_blob(self, cass):
        manifest_name = DEBIAN_IMAGE
        digest = 'sha256:5890f8ba95f680c87fcf89e51190098641b4f646102ce7ca906e7f83c84874dc'
        registry = Registry(DOCKER_HOSTNAME)
        blob = registry.blob(manifest_name, digest)
        self.assertIsInstance(blob, Blob)
        self.assertEqual(blob.registry, registry)
        self.assertEqual(blob.manifest_name, manifest_name)
        self.assertEqual(blob.digest, digest)
        self.assertFalse(isfile(blob.cache_path))
        self.assertEqual(blob.size, 1459)
        self.assertFalse(isfile(blob.cache_path))
        self.assertTrue(cass.all_played)

    @my_vcr.use_cassette
    def test_import_manifest(self, cass):
        digest = 'sha256:74e4a68dfba6f40b01787a3876cc1be0fb1d9025c3567cf8367c659f2187234f'
        registry = Registry(DOCKER_HOSTNAME)
        registry2 = self.destination_registry()
        manifest = Manifest(
            registry,
            BUSYBOX_IMAGE,
            digest,
        )
        with self.mocked_objects() as logger:
            registry2.import_manifest(manifest)
            logger.info.assert_has_calls([call(
                REGISTRY_IMPORTER_MESSAGE,
                '',
                BUSYBOX_IMAGE_FULL.format(digest),
                '',
                BUSYBOX_IMAGE,
                LATEST,
                '1+0=1 uploaded+existing manifests',
                BLOBS2_0_0_MESSAGE,
                '766112+0+0=766112 uploaded+mounted+existing blobs size',
            )])
        self.assertTrue(cass.all_played)

    @my_vcr.use_cassette
    def test_import_manifest_already_exists(self, cass):
        digest = 'sha256:74e4a68dfba6f40b01787a3876cc1be0fb1d9025c3567cf8367c659f2187234f'
        registry = Registry(DOCKER_HOSTNAME)
        registry2 = self.destination_registry()
        manifest = Manifest(
            registry,
            BUSYBOX_IMAGE,
            digest,
        )
        with self.mocked_objects() as logger:
            registry2.import_manifest(manifest)
            logger.info.assert_has_calls([])
        self.assertTrue(cass.all_played)

    @my_vcr.use_cassette
    def test_import_manifest_list(self, cass):
        digest = 'sha256:c6b45a95f932202dbb27c31333c4789f45184a744060f6e569cc9d2bf1b9ad6f'
        registry = Registry(DOCKER_HOSTNAME)
        registry2 = self.destination_registry()
        manifest = Manifest(
            registry,
            BUSYBOX_IMAGE,
            tag=LATEST,
        )
        with self.mocked_objects() as logger:
            registry2.import_manifest(manifest)
            logger.info.assert_has_calls([call(
                REGISTRY_IMPORTER_MESSAGE,
                '',
                BUSYBOX_IMAGE_FULL.format(digest),
                '',
                BUSYBOX_IMAGE,
                LATEST,
                '1+0=1 uploaded+existing manifests',
                BLOBS2_0_0_MESSAGE,
                '766112+0+0=766112 uploaded+mounted+existing blobs size',
            )])
        self.assertTrue(cass.all_played)

    @my_vcr.use_cassette
    def test_import_manifest_list_dry_run(self, cass):
        digest = 'sha256:c6b45a95f932202dbb27c31333c4789f45184a744060f6e569cc9d2bf1b9ad6f'
        registry = Registry(DOCKER_HOSTNAME)
        registry2 = self.destination_registry()
        manifest = Manifest(
            registry,
            BUSYBOX_IMAGE,
            tag=LATEST,
        )
        with self.mocked_objects() as logger:
            registry2.import_manifest(manifest, dry_run=True)
            logger.info.assert_has_calls([call(
                REGISTRY_IMPORTER_MESSAGE,
                '',
                BUSYBOX_IMAGE_FULL.format(digest),
                'NOT ',
                BUSYBOX_IMAGE,
                LATEST,
                '1+0=1 uploaded+existing manifests',
                BLOBS2_0_0_MESSAGE,
                '766112+0+0=766112 uploaded+mounted+existing blobs size',
            )])
        self.assertTrue(cass.all_played)

    @my_vcr.use_cassette
    def test_import_manifest_list_all(self, cass):
        digest = 'sha256:c6b45a95f932202dbb27c31333c4789f45184a744060f6e569cc9d2bf1b9ad6f'
        registry = Registry(DOCKER_HOSTNAME)
        registry2 = self.destination_registry()
        manifest = Manifest(
            registry,
            BUSYBOX_IMAGE,
            tag=LATEST,
        )
        with self.mocked_objects() as logger:
            registry2.import_manifest(manifest, 'newname', 'newtag', platform='all')
            logger.info.assert_has_calls([call(
                REGISTRY_IMPORTER_MESSAGE,
                '',
                BUSYBOX_IMAGE_FULL.format(digest),
                '',
                'newname',
                'newtag',
                '2+8=10 uploaded+existing manifests',
                BLOBS2_0_0_MESSAGE,
                '2140766+0+0=2140766 uploaded+mounted+existing blobs size',
            )])
        self.assertTrue(cass.all_played)

    @my_vcr.use_cassette
    def test_import_manifest_not_found(self, cass):
        registry = Registry(DOCKER_HOSTNAME)
        registry2 = self.destination_registry()
        manifest = Manifest(
            registry,
            BUSYBOX_IMAGE,
            tag='not_found',
        )
        url = 'https://registry-1.docker.io/v2/library/busybox/manifests/not_found'
        with self.mocked_objects() as logger:
            registry2.import_manifest(manifest)
            logger.warning.assert_has_calls([call(
                '%s%s NOT imported as %s:%s: %s',
                '',
                'docker.io/library/busybox:not_found',
                'library/busybox',
                'not_found',
                '404 Client Error: Not Found for url: {0}'.format(url),
            )])
        self.assertTrue(cass.all_played)
