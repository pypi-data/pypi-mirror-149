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

from __future__ import annotations

from unittest import skipIf
from unittest.mock import call, patch

from packaging import __version__ as packaging_version

from gitlabracadabra.objects.project import GitLabracadabraProject
from gitlabracadabra.tests import my_vcr
from gitlabracadabra.tests.case import TestCaseWithManager


class TestProjectPackageMirrors(TestCaseWithManager):
    """Test package_mirrors param."""

    def assert_has_errors(self, project: GitLabracadabraProject, expected_errors: list[str]) -> None:
        """Asset JSONschema errors.

        Args:
            project: Project.
            expected_errors: List of expected errors (as strings).
        """
        actual_errors = []
        for error in project.errors():
            actual_errors.append(error.message)
        self.assertListEqual(actual_errors, expected_errors)

    def test_package_mirrors_validation(self):
        """Test package_mirrors syntax."""
        project = GitLabracadabraProject('memory', 'group/project', {
            'package_mirrors': [{
                'raw': {
                    'default_url': 'https://example.org/foobar.tgz',
                },
            }],
        })
        self.assert_has_errors(project, [])

        project = GitLabracadabraProject('memory', 'group/project', {
            'package_mirrors': [{
                'raw': {
                    'default_url': 'https://storage.googleapis.com/{package_name}-release/release/{package_version}/bin/linux/amd64/{file_name}',  # noqa: E501
                    'default_package_name': 'kubernetes',
                    'default_package_version': 'v1.20.5',
                    'package_files': [
                        {'url': 'foo'},
                        {'package_name': 'foo'},
                        {'package_version': 'foo'},
                        {'file_name': 'kubectl'},
                        {'url': 'foo', 'package_name': 'foo', 'package_version': 'foo', 'file_name': 'kubectl'},
                    ],
                },
            }],
        })
        self.assert_has_errors(project, [])

        project = GitLabracadabraProject('memory', 'group/project', {
            'package_mirrors': [{
                'raw': {},
            }],
        })
        self.assert_has_errors(project, ["{'raw': {}} is not valid under any of the given schemas"])

        project = GitLabracadabraProject('memory', 'group/project', {
            'package_mirrors': [{
                'github': {
                    'full_name': 'operator-framework/operator-lifecycle-manager',
                    'package_name': 'olm',
                    'tags': ['/v.*/'],
                    'semver': '>=0.18.0',
                    'latest_release': True,
                    'tarball': True,
                    'zipball': True,
                    'assets': ['install.sh', 'crds.yaml', 'olm.yaml'],
                },
            }],
        })
        self.assert_has_errors(project, [])

    @my_vcr.use_cassette
    def test_package_mirrors_raw(self, cass):
        """Test package_mirrors, from raw.

        Args:
            cass: VCR cassette.
        """
        project = GitLabracadabraProject('memory', 'test/test_from_raw', {
            'package_mirrors': [{
                'raw': {
                    'default_url': 'https://download.docker.com/linux/debian/gpg',
                },
            }],
        })
        self.assertEqual(project.errors(), [])
        with patch('gitlabracadabra.packages.destination.logger', autospec=True) as logger:
            project.process()
            self.assertEqual(logger.mock_calls, [
                call.info(
                    '%sUploading %s package file "%s" from "%s" version %s (%s)',
                    '[test/test_from_raw] ',
                    'raw',
                    'gpg',
                    'unknown',
                    '0',
                    'https://download.docker.com/linux/debian/gpg',
                ),
            ])
        self.assertTrue(cass.all_played)

    @my_vcr.use_cassette
    def test_package_mirrors_github(self, cass):
        """Test package_mirrors, from github.

        Args:
            cass: VCR cassette.
        """
        project = GitLabracadabraProject('memory', 'test/test_from_github', {
            'package_mirrors': [{
                'github': {
                    'full_name': 'operator-framework/operator-lifecycle-manager',
                    'package_name': 'olm',
                    'latest_release': True,
                    'assets': ['install.sh', 'Boom'],
                },
            }],
        })
        self.assertEqual(project.errors(), [])
        with patch('gitlabracadabra.packages.destination.logger', autospec=True) as destination_logger:
            with patch('gitlabracadabra.packages.github.logger', autospec=True) as github_logger:
                project.process()
                self.assertEqual(destination_logger.mock_calls, [
                    call.info(
                        '%sUploading %s package file "%s" from "%s" version %s (%s)',
                        '[test/test_from_github] ',
                        'raw',
                        'install.sh',
                        'olm',
                        'v0.18.1',
                        'https://github.com/operator-framework/operator-lifecycle-manager/releases/download/v0.18.1/install.sh',
                    ),
                ])
                self.assertEqual(github_logger.mock_calls, [
                    call.warning(
                        '%sAsset "%s" not found from repository %s in release with tag %s',
                        '[test/test_from_github] ',
                        'Boom',
                        'operator-framework/operator-lifecycle-manager',
                        'v0.18.1',
                    ),
                ])
        self.assertTrue(cass.all_played)

    @my_vcr.use_cassette
    def test_package_mirrors_github_tarball(self, cass):
        """Test package_mirrors, from github tarball: Without Content-Length header.

        Args:
            cass: VCR cassette.
        """
        project = GitLabracadabraProject('memory', 'test/test_from_github', {
            'package_mirrors': [{
                'github': {
                    'full_name': 'projectcalico/calicoctl',
                    'latest_release': True,
                    'tarball': True,
                },
            }],
        })
        self.assertEqual(project.errors(), [])
        with patch('gitlabracadabra.packages.destination.logger', autospec=True) as destination_logger:
            with patch('gitlabracadabra.packages.github.logger', autospec=True) as github_logger:
                project.process()
                self.assertEqual(destination_logger.mock_calls, [
                    call.info(
                        '%sUploading %s package file "%s" from "%s" version %s (%s)',
                        '[test/test_from_github] ',
                        'raw',
                        'calicoctl-v3.18.3.tar.gz',
                        'calicoctl',
                        'v3.18.3',
                        'https://api.github.com/repos/projectcalico/calicoctl/tarball/v3.18.3',
                    ),
                ])
                self.assertEqual(github_logger.mock_calls, [])
        self.assertTrue(cass.all_played)

    @my_vcr.use_cassette(match_on=['method', 'gitlabracadabra_uri', 'gitlabracadabra_body'])
    def test_package_mirrors_helm(self, cass):
        """Test package_mirrors, from helm.

        Args:
            cass: VCR cassette.
        """
        project = GitLabracadabraProject('memory', 'test/test_from_helm', {
            'package_mirrors': [{
                'helm': {
                    'repo_url': 'https://charts.rook.io/release',
                    'package_name': 'rook-ceph',
                },
            }],
        })
        self.assertEqual(project.errors(), [])
        with patch('gitlabracadabra.packages.destination.logger', autospec=True) as destination_logger:
            with patch('gitlabracadabra.packages.helm.logger', autospec=True) as helm_logger:
                project.process()
                self.assertEqual(destination_logger.mock_calls, [
                    call.info(
                        '%sUploading %s package file "%s" from "%s" version %s (%s)',
                        '[test/test_from_helm] ',
                        'helm',
                        'rook-ceph-v1.6.3.tgz',
                        'rook-ceph',
                        'v1.6.3',
                        'https://charts.rook.io/release/rook-ceph-v1.6.3.tgz',
                    ),
                ])
                self.assertEqual(helm_logger.mock_calls, [])
        self.assertTrue(cass.all_played)

    @my_vcr.use_cassette
    def test_package_mirrors_helm_exists(self, cass):
        """Test package_mirrors, from existing helm.

        Args:
            cass: VCR cassette.
        """
        project = GitLabracadabraProject('memory', 'test/test_from_helm', {
            'package_mirrors': [{
                'helm': {
                    'repo_url': 'https://charts.rook.io/release',
                    'package_name': 'rook-ceph',
                },
            }],
        })
        self.assertEqual(project.errors(), [])
        with patch('gitlabracadabra.packages.destination.logger', autospec=True) as destination_logger:
            with patch('gitlabracadabra.packages.helm.logger', autospec=True) as helm_logger:
                project.process()
                self.assertEqual(destination_logger.mock_calls, [])
                self.assertEqual(helm_logger.mock_calls, [])
        self.assertTrue(cass.all_played)

    @skipIf(packaging_version == '19.0', 'PyPI package mirror requires packaging >= 20.9')
    @my_vcr.use_cassette(match_on=['method', 'gitlabracadabra_uri', 'gitlabracadabra_body'])
    def test_package_mirrors_pypi(self, cass):
        """Test package_mirrors, from pypi.

        Args:
            cass: VCR cassette.
        """
        project = GitLabracadabraProject('memory', 'test/test_from_pypi', {
            'package_mirrors': [{
                'pypi': {
                    'requirements': [
                        'types-html5lib',
                        'types-PyYAML',
                    ],
                },
            }],
        })
        self.assertEqual(project.errors(), [])
        with patch('gitlabracadabra.packages.destination.logger', autospec=True) as destination_logger:
            with patch('gitlabracadabra.packages.pypi.logger', autospec=True) as pypi_logger:
                project.process()
                self.assertEqual(destination_logger.mock_calls, [
                    call.info(
                        '%sUploading %s package file "%s" from "%s" version %s (%s)',
                        '[test/test_from_pypi] ',
                        'pypi',
                        'types-html5lib-1.1.0.tar.gz',
                        'types-html5lib',
                        '1.1.0',
                        'https://files.pythonhosted.org/packages/0c/45/2308f303dd263cd1b186ef129cfb20e5938930b96f6ee44293387612ec99/types-html5lib-1.1.0.tar.gz',
                    ),
                    call.info(
                        '%sUploading %s package file "%s" from "%s" version %s (%s)',
                        '[test/test_from_pypi] ',
                        'pypi',
                        'types_html5lib-1.1.0-py3-none-any.whl',
                        'types-html5lib',
                        '1.1.0',
                        'https://files.pythonhosted.org/packages/a9/61/1c6a5536f7ede682e26b9d5a0fe7ba082d3e776bda673cca2db95d7364e0/types_html5lib-1.1.0-py3-none-any.whl',
                    ),
                    call.info(
                        '%sUploading %s package file "%s" from "%s" version %s (%s)',
                        '[test/test_from_pypi] ',
                        'pypi',
                        'types-PyYAML-5.4.3.tar.gz',
                        'types-pyyaml',
                        '5.4.3',
                        'https://files.pythonhosted.org/packages/c1/6a/76f047f9289ed40b8a6460ae9900deec9aa85b9e1276da24112ce8fc9a7b/types-PyYAML-5.4.3.tar.gz',
                    ),
                    call.info(
                        '%sUploading %s package file "%s" from "%s" version %s (%s)',
                        '[test/test_from_pypi] ',
                        'pypi',
                        'types_PyYAML-5.4.3-py2.py3-none-any.whl',
                        'types-pyyaml',
                        '5.4.3',
                        'https://files.pythonhosted.org/packages/b8/86/b957c28571005b1f13b92703400453c6a3a7fddd3f75c4c83bd2e7dc4d47/types_PyYAML-5.4.3-py2.py3-none-any.whl',
                    ),
                ])
                self.assertEqual(pypi_logger.mock_calls, [])
        self.assertTrue(cass.all_played)

    @skipIf(packaging_version == '19.0', 'PyPI package mirror requires packaging >= 20.9')
    @my_vcr.use_cassette(match_on=['method', 'gitlabracadabra_uri', 'gitlabracadabra_body'])
    def test_package_mirrors_pypi_exists(self, cass):
        """Test package_mirrors, from pypi.

        Args:
            cass: VCR cassette.
        """
        project = GitLabracadabraProject('memory', 'test/test_from_pypi', {
            'package_mirrors': [{
                'pypi': {
                    'requirements': [
                        'types-html5lib',
                        'types-PyYAML',
                    ],
                },
            }],
        })
        self.assertEqual(project.errors(), [])
        with patch('gitlabracadabra.packages.destination.logger', autospec=True) as destination_logger:
            with patch('gitlabracadabra.packages.pypi.logger', autospec=True) as pypi_logger:
                project.process()
                self.assertEqual(destination_logger.mock_calls, [])
                self.assertEqual(pypi_logger.mock_calls, [])
        self.assertTrue(cass.all_played)
