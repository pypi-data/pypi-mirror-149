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

from unittest.mock import call, patch

from gitlabracadabra.packages.helm import Helm
from gitlabracadabra.packages.package_file import PackageFile
from gitlabracadabra.tests import my_vcr
from gitlabracadabra.tests.case import TestCaseWithManager


class TestHelm(TestCaseWithManager):
    """Test Helm class."""

    def test_str(self):
        """Test __str__ method."""
        self.assertEqual(
            str(Helm(log_prefix='foo ', repo_url='https://charts.example.org/', package_name='foobar')),
            'Helm charts repository (url=https://charts.example.org/)',
        )

    @my_vcr.use_cassette
    def test_package_files(self, cass):
        """Test package_files method.

        Args:
            cass: VCR cassette.
        """
        with patch('gitlabracadabra.packages.helm.logger', autospec=True) as logger:
            source = Helm(
                repo_url='https://charts.rook.io/release',
                package_name='rook-ceph',
            )
            self.assertEqual(
                source.package_files, [
                    PackageFile(
                        'https://charts.rook.io/release/rook-ceph-v1.6.3.tgz',
                        'helm',
                        'rook-ceph',
                        'v1.6.3',
                        'rook-ceph-v1.6.3.tgz',
                        metadata={'channel': 'stable'},
                    ),
                ],
            )
            self.assertEqual(logger.mock_calls, [])
        self.assertTrue(cass.all_played)

    @my_vcr.use_cassette
    def test_package_files_index_not_found(self, cass):
        """Test package_files method, with index not found.

        Args:
            cass: VCR cassette.
        """
        with patch('gitlabracadabra.packages.helm.logger', autospec=True) as logger:
            source = Helm(
                repo_url='https://charts.rook.io/not_found',
                package_name='rook-ceph',
            )
            self.assertEqual(source.package_files, [])
            self.assertEqual(logger.mock_calls, [
                call.warning('%sUnexpected HTTP status for Helm index %s: received %i %s', '', 'https://charts.rook.io/not_found/index.yaml', 404, 'Not Found'),
                call.info('%sPackage not found %s for Helm index %s', '', 'rook-ceph', 'https://charts.rook.io/not_found/index.yaml'),
            ])
        self.assertTrue(cass.all_played)

    @my_vcr.use_cassette
    def test_package_files_relative(self, cass):
        """Test package_files method, with relative urls.

        Args:
            cass: VCR cassette.
        """
        with patch('gitlabracadabra.packages.helm.logger', autospec=True) as logger:
            source = Helm(
                repo_url='https://argoproj.github.io/argo-helm',
                package_name='/ar[g]o/',
            )
            self.assertEqual(
                source.package_files, [
                    PackageFile(
                        'https://argoproj.github.io/argo-helm/argo-1.0.0.tgz',
                        'helm',
                        'argo',
                        '1.0.0',
                        'argo-1.0.0.tgz',
                        metadata={'channel': 'stable'},
                    ),
                ],
            )
            self.assertEqual(logger.mock_calls, [])
        self.assertTrue(cass.all_played)
