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
from gitlabracadabra.packages.raw import RawSource
from gitlabracadabra.tests.case import TestCase


class TestRawSource(TestCase):
    """Test RawSource class."""

    def test_str(self):
        """Test __str__ method."""
        self.assertEqual(
            str(RawSource(log_prefix='foo ', default_url='https://foobar.example.org')),
            'Raw repository (default_url=https://foobar.example.org)',
        )

    def test_package_files_mono(self):
        """Test package_files method, with only mandatory arguments."""
        source = RawSource(
            default_url='https://example.org/foobar.tgz',
        )
        self.assertEqual(
            source.package_files,
            [PackageFile('https://example.org/foobar.tgz', 'raw', 'unknown', '0', 'foobar.tgz')],
        )

    def test_package_files_format(self):
        """Test package_files method, with format in url."""
        source = RawSource(
            default_url='https://example.org/{package_name}/{package_version}/pkg.tgz',
            package_files=[
                {'package_name': 'pkg1', 'package_version': '2.0', 'file_name': 'file_name.tgz'},
                {'package_name': 'pkg2', 'package_version': '3.0'},
                {'file_name': 'file_name2.tgz'},
                {},
            ],
        )
        self.assertEqual(
            source.package_files,
            [
                PackageFile('https://example.org/pkg1/2.0/pkg.tgz', 'raw', 'pkg1', '2.0', 'file_name.tgz'),
                PackageFile('https://example.org/pkg2/3.0/pkg.tgz', 'raw', 'pkg2', '3.0', 'pkg.tgz'),
                PackageFile('https://example.org/unknown/0/pkg.tgz', 'raw', 'unknown', '0', 'file_name2.tgz'),
                PackageFile('https://example.org/unknown/0/pkg.tgz', 'raw', 'unknown', '0', 'pkg.tgz'),
            ],
        )

    def test_package_files_format_file_name(self):
        """Test package_files method, with default_* and file_name."""
        source = RawSource(
            default_url='https://storage.googleapis.com/{package_name}-release/release/{package_version}/bin/linux/amd64/{file_name}',  # noqa: E501
            default_package_name='kubernetes',
            default_package_version='v1.20.5',
            package_files=[
                {'file_name': 'kubectl'},
                {'file_name': 'kubelet'},
                {'file_name': 'kubeadm'},
            ],
        )
        self.assertEqual(
            source.package_files,
            [
                PackageFile('https://storage.googleapis.com/kubernetes-release/release/v1.20.5/bin/linux/amd64/kubectl', 'raw', 'kubernetes', 'v1.20.5', 'kubectl'),  # noqa: E501
                PackageFile('https://storage.googleapis.com/kubernetes-release/release/v1.20.5/bin/linux/amd64/kubelet', 'raw', 'kubernetes', 'v1.20.5', 'kubelet'),  # noqa: E501
                PackageFile('https://storage.googleapis.com/kubernetes-release/release/v1.20.5/bin/linux/amd64/kubeadm', 'raw', 'kubernetes', 'v1.20.5', 'kubeadm'),  # noqa: E501
            ],
        )

    def test_package_files_format_url(self):
        """Test package_files method, with default_* and url."""
        source = RawSource(
            default_url='https://storage.googleapis.com/{package_name}-release/release/{package_version}/bin/linux/amd64',  # noqa: E501
            default_package_name='kubernetes',
            default_package_version='v1.20.5',
            package_files=[
                {'url': '{default_url}/kubectl'},
                {'url': '{default_url}/kubelet'},
                {'url': '{default_url}/kubeadm'},
            ],
        )
        self.assertEqual(
            source.package_files,
            [
                PackageFile('https://storage.googleapis.com/kubernetes-release/release/v1.20.5/bin/linux/amd64/kubectl', 'raw', 'kubernetes', 'v1.20.5', 'kubectl'),  # noqa: E501
                PackageFile('https://storage.googleapis.com/kubernetes-release/release/v1.20.5/bin/linux/amd64/kubelet', 'raw', 'kubernetes', 'v1.20.5', 'kubelet'),  # noqa: E501
                PackageFile('https://storage.googleapis.com/kubernetes-release/release/v1.20.5/bin/linux/amd64/kubeadm', 'raw', 'kubernetes', 'v1.20.5', 'kubeadm'),  # noqa: E501
            ],
        )

    def test_package_files_format_edge_cases(self):
        """Test package_files method, with {file_name} in url."""
        source = RawSource(
            default_url='http://example.org/{default_package_name}/{package_name}/{default_package_version}/{package_version}/{file_name}',  # noqa: E501
            package_files=[
                {'url': '{default_url}/foo', 'package_name': 'pkg2', 'package_version': '3.0'},
                {},
            ],
        )
        self.assertEqual(
            source.package_files,
            [
                PackageFile('http://example.org/unknown/pkg2/0/3.0/{file_name}/foo', 'raw', 'pkg2', '3.0', 'foo'),
                PackageFile('http://example.org/unknown/unknown/0/0/{file_name}', 'raw', 'unknown', '0', '{file_name}'),
            ],
        )
