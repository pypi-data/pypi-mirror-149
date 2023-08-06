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

from __future__ import annotations

from typing import AnyStr, Iterator, Optional

from requests.models import Response


class Stream(object):
    """Stream."""

    def __init__(self, response: Response, chunksize: int = 65536) -> None:
        """Initialize Stream.

        Args:
            response: Streamed response.
            chunksize: Chunk size (used when there is no Content-Length header).
        """
        self._response = response
        self._chunksize = chunksize

    def __bool__(self) -> bool:
        """Stream as boolean.

        Needed for Session.request() which uses: data=data or dict().
        (otherwise, would be considered False when length is 0).

        Returns:
            Always True.
        """
        return True

    def __len__(self) -> int:
        """Get stream length.

        Returns:
            The stream length. Zero if there is no Content-Length header.
        """
        return int(self._response.headers.get('Content-Length', '0'))

    def __iter__(self) -> Iterator[bytes]:
        """Get an iterator of chunks of body.

        Returns:
            A bytes iterator.
        """
        return self._response.raw.stream(self._chunksize)  # type: ignore

    @property
    def name(self) -> str:
        """Return URL.

        This is needed to have proper file name in multipart upload.

        Called from requests.utils.guess_filename(),
        called from requests.models.RequestEncodingMixin._encode_files(),
        called from requests.models.PreparedRequest.prepare_body().

        Returns:
            The response URL.
        """
        if self._response.history:
            # Keep original request URL, to avoid too long filename
            return self._response.history[0].url
        return self._response.url

    def read(self, size: Optional[int] = None) -> AnyStr:
        """Read stream.

        Args:
            size: Length to read. Defaulting to None like http.client.HTTPResponse.read().

        Returns:
            The read bytes/str.
        """
        return self._response.raw.read(size)  # type: ignore
