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

from os.path import isfile

from gitlabracadabra.containers.blob import Blob
from gitlabracadabra.containers.registry import Registry
from gitlabracadabra.tests import my_vcr
from gitlabracadabra.tests.case import TestCase


MANIFEST_NAME = 'debian'
DIGEST = 'sha256:12345'
SIZE = 42


class TestBlob(TestCase):
    def test_equal(self):  # noqa: WPS210
        registry1 = Registry('localhost:5000')
        registry2 = Registry('localhost:5000')
        blob1 = Blob(registry1, MANIFEST_NAME, DIGEST)
        blob2 = Blob(registry1, MANIFEST_NAME, DIGEST)
        blob3 = Blob(registry2, MANIFEST_NAME, DIGEST)
        blob4 = Blob(registry1, MANIFEST_NAME, DIGEST, size=SIZE)
        self.assertEqual(blob1, blob2)
        self.assertNotEqual(blob1, blob3)
        self.assertNotEqual(blob1, blob4)

    @my_vcr.use_cassette
    def test_open(self, cass):
        registry = Registry('docker.io')
        blob = Blob(
            registry,
            'library/debian',
            'sha256:5890f8ba95f680c87fcf89e51190098641b4f646102ce7ca906e7f83c84874dc',
        )
        self.assertIsInstance(blob, Blob)
        self.assertFalse(isfile(blob.cache_path))
        with blob as opened_blob:
            blob_content = opened_blob.read().decode('utf-8')
            self.assertTrue(
                blob_content.startswith('{"architecture":"amd64","config":{'),
                msg=blob_content,
            )
        self.assertTrue(isfile(blob.cache_path))
        self.assertTrue(cass.all_played)
