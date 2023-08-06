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

from gitlabracadabra.packages.source import Source
from gitlabracadabra.tests.case import TestCase


class TestSource(TestCase):
    """Test Source class."""

    def test_package_files(self):
        """Test package_files method."""
        source = Source()
        with self.assertRaises(NotImplementedError):
            source.package_files  # noqa: WPS428
