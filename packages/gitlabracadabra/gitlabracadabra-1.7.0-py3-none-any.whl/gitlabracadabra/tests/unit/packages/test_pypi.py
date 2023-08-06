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

from unittest import skipIf
from unittest.mock import patch

from packaging import __version__ as packaging_version

from gitlabracadabra.packages.package_file import PackageFile
from gitlabracadabra.packages.pypi import PyPI
from gitlabracadabra.tests import my_vcr
from gitlabracadabra.tests.case import TestCaseWithManager


class TestPyPI(TestCaseWithManager):
    """Test PyPI class."""

    def test_str(self):
        """Test __str__ method."""
        self.assertEqual(
            str(PyPI(log_prefix='foo ', requirements='')),
            'PyPI repository',
        )

    @skipIf(packaging_version == '19.0', 'PyPI package mirror requires packaging >= 20.9')
    @my_vcr.use_cassette
    def test_package_files(self, cass):
        """Test package_files method.

        Args:
            cass: VCR cassette.
        """
        with patch('gitlabracadabra.packages.pypi.logger', autospec=True) as logger:
            source = PyPI(
                requirements=[
                    'gitlabracadabra==1.2.0',
                    'ansible==2.9.20',
                ],
            )
            self.assertEqual(
                source.package_files, [
                    PackageFile(
                        'https://files.pythonhosted.org/packages/ef/54/77ef237185b9e01b48d2f6748fe2d3a8da2d32acd1dbf92677d8c43de8e2/gitlabracadabra-1.2.0-py2.py3-none-any.whl',
                        'pypi',
                        'gitlabracadabra',
                        '1.2.0',
                        'gitlabracadabra-1.2.0-py2.py3-none-any.whl',
                        metadata={
                            'sha256': 'e3b0c06ddc076c7ca8dbfc5664c96b93f093cc8c3070c0f192df4ae7ba820547',
                        },
                    ),
                    PackageFile(
                        'https://files.pythonhosted.org/packages/63/9c/3aa2f1ba06fcdbc6b1c723fae953c608def8bb3d69d1724aed332c33404c/gitlabracadabra-1.2.0.tar.gz',
                        'pypi',
                        'gitlabracadabra',
                        '1.2.0',
                        'gitlabracadabra-1.2.0.tar.gz',
                        metadata={
                            'sha256': 'f082a4fef09394b0406b8f1e20e1db595c43cf63f0a916fbca37424a050a4812',
                        },
                    ),
                    PackageFile(
                        'https://files.pythonhosted.org/packages/ed/53/01fe1f54d8d408306b72c961e573223a0d95eca26d6c3b59d57a9c64e4ef/ansible-2.9.20.tar.gz',
                        'pypi',
                        'ansible',
                        '2.9.20',
                        'ansible-2.9.20.tar.gz',
                        metadata={
                            'requires-python': '>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*',
                            'sha256': '73a271b9b2081a254deaa7347583d8bd97142b67c891e463ff2302006c5c8c38',
                        },
                    ),
                ],
            )
            self.assertEqual(logger.mock_calls, [])
        self.assertTrue(cass.all_played)

    @skipIf(packaging_version == '19.0', 'PyPI package mirror requires packaging >= 20.9')
    @my_vcr.use_cassette
    def test_package_files_yanked_equal(self, cass):
        """Test package_files method, with yanked package with equal requirement.

        Args:
            cass: VCR cassette.
        """
        with patch('gitlabracadabra.packages.pypi.logger', autospec=True) as logger:
            source = PyPI(
                requirements=[
                    'ruamel.yaml.clib==0.2.4',
                ],
            )
            self.assertEqual(
                source.package_files[0],
                PackageFile(
                    'https://files.pythonhosted.org/packages/44/bc/8139e502475f986fb108c465596b82d278c10dc94c2f69366c2358cb3923/ruamel.yaml.clib-0.2.4-cp35-cp35m-macosx_10_6_intel.whl',
                    'pypi',
                    'ruamel-yaml-clib',
                    '0.2.4',
                    'ruamel.yaml.clib-0.2.4-cp35-cp35m-macosx_10_6_intel.whl',
                    metadata={
                        'sha256': '329ac9064c1cfff9fc77fbecd90d07d698176fcd0720bfef9c2d27faa09dcc0e',
                    },
                ),
            )
            self.assertEqual(len(source.package_files), 21)
            self.assertEqual(logger.mock_calls, [])
        self.assertTrue(cass.all_played)

    @skipIf(packaging_version == '19.0', 'PyPI package mirror requires packaging >= 20.9')
    @my_vcr.use_cassette
    def test_package_files_yanked_le(self, cass):
        """Test package_files method, with yanked package with <= requirement.

        Args:
            cass: VCR cassette.
        """
        with patch('gitlabracadabra.packages.pypi.logger', autospec=True) as logger:
            source = PyPI(
                requirements=[
                    'ruamel.yaml.clib<=0.2.4',
                ],
            )
            self.assertEqual(
                source.package_files[0],
                PackageFile(
                    'https://files.pythonhosted.org/packages/31/bd/40071f2200d5e3eeaad85687064c3867cd5565b147c5ea7e9611bc0d4c0a/ruamel.yaml.clib-0.2.2-cp27-cp27m-macosx_10_9_x86_64.whl',
                    'pypi',
                    'ruamel-yaml-clib',
                    '0.2.2',
                    'ruamel.yaml.clib-0.2.2-cp27-cp27m-macosx_10_9_x86_64.whl',
                    metadata={
                        'sha256': '28116f204103cb3a108dfd37668f20abe6e3cafd0d3fd40dba126c732457b3cc',
                    },
                ),
            )
            self.assertEqual(len(source.package_files), 31)
            self.assertEqual(logger.mock_calls, [])
        self.assertTrue(cass.all_played)
