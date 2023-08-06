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

from contextlib import contextmanager
from io import StringIO
from unittest.mock import patch


# Inspired by https://mapleoin.github.io/perma/mocking-python-file-open
@contextmanager
def patch_open(contents_map):
    def mock_open(*args, **kwargs):
        if args[0] in contents_map:
            f = StringIO(contents_map[args[0]])
            f.name = args[0]
        else:
            mocked_open.stop()
            try:
                f = open(*args)
            finally:
                mocked_open.start()
        return f
    mocked_open = patch('builtins.open', mock_open)
    mocked_open.start()
    yield
    mocked_open.stop()
