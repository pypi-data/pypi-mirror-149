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

from collections import namedtuple

from gitlabracadabra.containers.const import DOCKER_HOSTNAME, DOCKER_REGISTRY
from gitlabracadabra.containers.registries import Registries
from gitlabracadabra.tests.case import TestCase


TestData = namedtuple(
    'TestData',
    ['input_name', 'hostname', 'manifest_name', 'tag', 'reference_tag', 'digest', 'full_reference', 'short_reference'],
)

LATEST = 'latest'
TEST_DATA = (
    TestData(
        'my/repo',
        DOCKER_HOSTNAME,
        'my/repo',
        LATEST,
        None,
        None,
        'docker.io/my/repo',
        'my/repo',
    ),
    TestData(
        'debian',
        DOCKER_HOSTNAME,
        'library/debian',
        LATEST,
        None,
        None,
        'docker.io/library/debian',
        'debian',
    ),
    TestData(
        'localhost/foo/bar:v1.0',
        'localhost',
        'foo/bar',
        'v1.0',
        'v1.0',
        None,
        'localhost/foo/bar:v1.0',
        'localhost/foo/bar:v1.0',
    ),
    TestData(
        'example.org/foo/baz:v2.3.4',
        'example.org',
        'foo/baz',
        'v2.3.4',
        'v2.3.4',
        None,
        'example.org/foo/baz:v2.3.4',
        'example.org/foo/baz:v2.3.4',
    ),
    TestData(
        'registry:5000/foo/bar:latest',
        'registry:5000',
        'foo/bar',
        LATEST,
        LATEST,
        None,
        'registry:5000/foo/bar:latest',
        'registry:5000/foo/bar',
    ),
    TestData(
        'busybox:latest@sha256:74e4a68dfba6f40b01787a3876cc1be0fb1d9025c3567cf8367c659f2187234f',
        DOCKER_HOSTNAME,
        'library/busybox',
        LATEST,
        LATEST,
        'sha256:74e4a68dfba6f40b01787a3876cc1be0fb1d9025c3567cf8367c659f2187234f',
        'docker.io/library/busybox:latest@sha256:74e4a68dfba6f40b01787a3876cc1be0fb1d9025c3567cf8367c659f2187234f',
        'busybox@sha256:74e4a68dfba6f40b01787a3876cc1be0fb1d9025c3567cf8367c659f2187234f',
    ),
)


class TestRegistries(TestCase):
    def test_singleton(self) -> None:
        registries1 = Registries()
        registries2 = Registries()
        self.assertEqual(id(registries1), id(registries2))

    def test_get_registry(self) -> None:
        registries = Registries()
        docker_registry = registries.get_registry(DOCKER_REGISTRY)
        self.assertEqual(docker_registry.hostname, DOCKER_HOSTNAME)
        docker_registry2 = registries.get_registry(DOCKER_HOSTNAME)
        self.assertEqual(docker_registry2.hostname, DOCKER_HOSTNAME)
        docker_registry3 = registries.get_registry('example.org')
        self.assertEqual(docker_registry3.hostname, 'example.org')

    def test_get_manifest(self) -> None:
        registries = Registries()
        for test_data in TEST_DATA:
            with self.subTest(input_name=test_data.input_name):
                manifest = registries.get_manifest(test_data.input_name)
                self.assertEqual(manifest.registry.hostname, test_data.hostname)
                self.assertEqual(manifest.manifest_name, test_data.manifest_name)
                self.assertEqual(manifest.tag, test_data.tag)
                self.assertEqual(manifest._digest, test_data.digest)  # noqa: WPS437

    def test_short_reference(self) -> None:
        for test_data in TEST_DATA:
            with self.subTest(input_name=test_data.input_name):
                reference = Registries.short_reference(test_data.input_name)
                self.assertEqual(reference, test_data.short_reference)

    def test_full_reference(self) -> None:
        for test_data in TEST_DATA:
            with self.subTest(input_name=test_data.input_name):
                reference = Registries.full_reference(test_data.input_name)
                self.assertEqual(reference, test_data.full_reference)

    def test_full_reference_parts(self) -> None:
        for test_data in TEST_DATA:
            with self.subTest(input_name=test_data.input_name):
                manifest = Registries.full_reference_parts(test_data.input_name)
                self.assertEqual(manifest.hostname, test_data.hostname)
                self.assertEqual(manifest.manifest_name, test_data.manifest_name)
                self.assertEqual(manifest.tag, test_data.reference_tag)
                self.assertEqual(manifest.digest, test_data.digest)
