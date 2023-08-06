# Copyright (C) 2008-2021 The pip developers (see AUTHORS.txt file)
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
# .
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
# .
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from typing import Optional

from packaging.utils import canonicalize_name


# The functions below are copied from pip:
# _internal/index/package_finder.py


def _find_name_version_sep(fragment, canonical_name):
    # type: (str, str) -> int
    """Find the separator's index based on the package's canonical name.

    :param fragment: A <package>+<version> filename "fragment" (stem) or
        egg fragment.
    :param canonical_name: The package's canonical name.

    This function is needed since the canonicalized name does not necessarily
    have the same length as the egg info's name part. An example::

    >>> fragment = 'foo__bar-1.0'
    >>> canonical_name = 'foo-bar'
    >>> _find_name_version_sep(fragment, canonical_name)
    8
    """
    # Project name and version must be separated by one single dash. Find all
    # occurrences of dashes; if the string in front of it matches the canonical
    # name, this is the one separating the name and version parts.
    for i, c in enumerate(fragment):
        if c != "-":
            continue
        if canonicalize_name(fragment[:i]) == canonical_name:
            return i
    raise ValueError("{} does not match {}".format(fragment, canonical_name))


def _extract_version_from_fragment(fragment, canonical_name):
    # type: (str, str) -> Optional[str]
    """Parse the version string from a <package>+<version> filename
    "fragment" (stem) or egg fragment.

    :param fragment: The string to parse. E.g. foo-2.1
    :param canonical_name: The canonicalized name of the package this
        belongs to.
    """
    try:
        version_start = _find_name_version_sep(fragment, canonical_name) + 1
    except ValueError:
        return None
    version = fragment[version_start:]
    if not version:
        return None
    return version


extract_version_from_fragment = _extract_version_from_fragment
