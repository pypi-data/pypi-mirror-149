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

from gitlabracadabra.packages.github import Github
from gitlabracadabra.packages.package_file import PackageFile
from gitlabracadabra.tests import my_vcr
from gitlabracadabra.tests.case import TestCaseWithManager


class TestGithub(TestCaseWithManager):
    """Test Github class."""

    def test_str(self):
        """Test __str__ method."""
        self.assertEqual(
            str(Github(log_prefix='foo ', full_name='foo/bar')),
            'Github repository (full_name=foo/bar)',
        )

    @my_vcr.use_cassette
    def test_package_files_latest_balls(self, cass):
        """Test package_files method, with latest_release, tarball and zipball.

        Args:
            cass: VCR cassette.
        """
        source = Github(
            full_name='kubernetes-sigs/kubespray',
            latest_release=True,
            tarball=True,
            zipball=True,
        )
        self.assertEqual(
            source.package_files, [
                PackageFile(
                    'https://api.github.com/repos/kubernetes-sigs/kubespray/tarball/v2.15.1',
                    'raw',
                    'kubespray',
                    'v2.15.1',
                    'kubespray-v2.15.1.tar.gz',
                ),
                PackageFile(
                    'https://api.github.com/repos/kubernetes-sigs/kubespray/zipball/v2.15.1',
                    'raw',
                    'kubespray',
                    'v2.15.1',
                    'kubespray-v2.15.1.zip',
                ),
            ],
        )

    @my_vcr.use_cassette
    def test_package_files_assets(self, cass):
        """Test package_files method, with tags, semver and assets.

        Args:
            cass: VCR cassette.
        """
        source = Github(
            log_prefix='[log_prefix] ',
            full_name='operator-framework/operator-lifecycle-manager',
            tags=['/v.*/'],
            semver='>=0.18.0',
            latest_release=True,
            assets=['install.sh', 'crds.yaml', 'olm.yaml', 'unexisting-asset'],
        )
        with patch('gitlabracadabra.packages.github.logger', autospec=True) as logger:
            self.assertEqual(
                source.package_files, [
                    PackageFile(
                        'https://github.com/operator-framework/operator-lifecycle-manager/releases/download/v0.18.1/install.sh',
                        'raw',
                        'operator-lifecycle-manager',
                        'v0.18.1',
                        'install.sh',
                    ),
                    PackageFile(
                        'https://github.com/operator-framework/operator-lifecycle-manager/releases/download/v0.18.1/crds.yaml',
                        'raw',
                        'operator-lifecycle-manager',
                        'v0.18.1',
                        'crds.yaml',
                    ),
                    PackageFile(
                        'https://github.com/operator-framework/operator-lifecycle-manager/releases/download/v0.18.1/olm.yaml',
                        'raw',
                        'operator-lifecycle-manager',
                        'v0.18.1',
                        'olm.yaml',
                    ),
                    PackageFile(
                        'https://github.com/operator-framework/operator-lifecycle-manager/releases/download/v0.18.0/install.sh',
                        'raw',
                        'operator-lifecycle-manager',
                        'v0.18.0',
                        'install.sh',
                    ),
                    PackageFile(
                        'https://github.com/operator-framework/operator-lifecycle-manager/releases/download/v0.18.0/crds.yaml',
                        'raw',
                        'operator-lifecycle-manager',
                        'v0.18.0',
                        'crds.yaml',
                    ),
                    PackageFile(
                        'https://github.com/operator-framework/operator-lifecycle-manager/releases/download/v0.18.0/olm.yaml',
                        'raw',
                        'operator-lifecycle-manager',
                        'v0.18.0',
                        'olm.yaml',
                    ),
                ],
            )
            self.assertEqual(logger.mock_calls, [
                call.warning(
                    '%sAsset "%s" not found from repository %s in release with tag %s',
                    '[log_prefix] ',
                    'unexisting-asset',
                    'operator-framework/operator-lifecycle-manager',
                    'v0.18.1',
                ),
                call.warning(
                    '%sAsset "%s" not found from repository %s in release with tag %s',
                    '[log_prefix] ',
                    'unexisting-asset',
                    'operator-framework/operator-lifecycle-manager',
                    'v0.18.0',
                ),
            ])
