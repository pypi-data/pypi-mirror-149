# -*- coding: utf-8 -*-
#
# Copyright (C) 2019-2020 Mathieu Parent <math.parent@gmail.com>
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

from gitlabracadabra.packages.package_file import PackageFile
from gitlabracadabra.tests.case import TestCase


class TestPackageFile(TestCase):
    """Test PackageFile class."""

    def test_attributes(self):
        """Test attributes."""
        package_file = PackageFile(
            'https://example.org/foobar.tgz',
            'raw',
            'my-package-name',
            '1.0',
            'foobar.tar.gz',
            metadata={'hello': 'world'},
        )
        self.assertEqual(package_file.url, 'https://example.org/foobar.tgz')
        self.assertEqual(package_file.package_type, 'raw')
        self.assertEqual(package_file.package_name, 'my-package-name')
        self.assertEqual(package_file.package_version, '1.0')
        self.assertEqual(package_file.file_name, 'foobar.tar.gz')
        self.assertEqual(package_file.metadata, {'hello': 'world'})

    def test_attributes_defaults(self):
        """Test attributes."""
        package_file = PackageFile(
            'https://example.org/foobar.tgz',
            'raw',
            'my-package-name',
        )
        self.assertEqual(package_file.url, 'https://example.org/foobar.tgz')
        self.assertEqual(package_file.package_type, 'raw')
        self.assertEqual(package_file.package_name, 'my-package-name')
        self.assertEqual(package_file.package_version, '0')
        self.assertEqual(package_file.file_name, 'foobar.tgz')
        self.assertEqual(package_file.metadata, {})

    def test_equals(self):
        """Test ==."""
        url = 'https://example.org/foobar.tgz'
        package_file = PackageFile(url, 'raw', 'my-package-name')
        self.assertEqual(
            package_file,
            PackageFile(url, 'raw', 'my-package-name'),
        )
        self.assertEqual(
            package_file,
            PackageFile(url, 'raw', 'my-package-name', '0', 'foobar.tgz', metadata={}),
        )
        self.assertNotEqual(
            package_file,
            PackageFile('!', 'raw', 'my-package-name', '0', 'foobar.tgz', metadata={}),
        )
        self.assertNotEqual(
            package_file,
            PackageFile(url, '!', 'my-package-name', '0', 'foobar.tgz', metadata={}),
        )
        self.assertNotEqual(
            package_file,
            PackageFile(url, 'raw', '!', '0', 'foobar.tgz', metadata={}),
        )
        self.assertNotEqual(
            package_file,
            PackageFile(url, 'raw', 'my-package-name', '!', 'foobar.tgz', metadata={}),
        )
        self.assertNotEqual(
            package_file,
            PackageFile(url, 'raw', 'my-package-name', '0', '!', metadata={}),
        )
        self.assertNotEqual(
            package_file,
            PackageFile(url, 'raw', 'my-package-name', '0', 'foobar.tgz', metadata={'foo': '!'}),
        )
