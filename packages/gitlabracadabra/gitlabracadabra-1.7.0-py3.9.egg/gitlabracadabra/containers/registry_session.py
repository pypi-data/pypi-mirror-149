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

from time import time
from typing import TYPE_CHECKING
from urllib.request import parse_http_list, parse_keqv_list

from requests import Response, Session, codes
from requests.adapters import HTTPAdapter
from requests.structures import CaseInsensitiveDict

from gitlabracadabra.auth_info import AuthInfo
from gitlabracadabra.containers.const import DOCKER_HOSTNAME, DOCKER_REGISTRY
from gitlabracadabra.containers.scope import Scope


if TYPE_CHECKING:
    from typing import Any, Dict, List, MutableMapping, Optional, Set, Tuple, Union

    from requests.auth import AuthBase

    Params = Optional[  # noqa: WPS110
        MutableMapping[
            str,
            Union[str, List[str]],
        ]
    ]
    SimpleParams = Dict[str, Union[str, List[str]]]


class Token(object):
    """JWT Token."""

    def __init__(
        self,
        token: str,
        expires_in: int,
    ) -> None:
        """Instanciate a token.

        Args:
            token: Token.
            expires_in: Expires in x seconds.
        """
        minimum_token_lifetime_seconds = 60

        self._token = token
        self._expires_in = expires_in
        if self._expires_in < minimum_token_lifetime_seconds:
            self._expires_in = minimum_token_lifetime_seconds

        # We ignore issued_at property, and use local time instead
        self._issued_at = time()

    @property
    def token(self) -> str:
        """Get token.

        Returns:
            The token.
        """
        return self._token

    @property
    def expiration_time(self) -> float:
        """Get expiration time.

        Returns:
            Expiration time.
        """
        return self._issued_at + self._expires_in

    def is_expired(self) -> bool:
        """Check if token is expired.

        Returns:
            True if token is expired.
        """
        return time() >= self.expiration_time


class RegistrySession(object):
    """Container registry HTTP methods."""

    def __init__(self, hostname: str, auth_info: Optional[AuthInfo] = None) -> None:
        """Instanciate a registry connection.

        Args:
            hostname: fqdn of a registry.
            auth_info: Authentication information.
        """
        if hostname == DOCKER_HOSTNAME:
            self._hostname = DOCKER_REGISTRY
        else:
            self._hostname = hostname
        self._auth_info = auth_info or AuthInfo()
        self._scheme = 'https'
        self._session = Session()
        self._session.mount('http://', HTTPAdapter(max_retries=3))
        self._session.mount('https://', HTTPAdapter(max_retries=3))
        self._session.headers = CaseInsensitiveDict({'Docker-Distribution-Api-Version': 'registry/2.0'})
        # Tokens, by set of scopes (as query string or None for all scope)
        self._tokens: Dict[Optional[str], Token] = {}
        # Cache where blobs are present
        # Dict key is digest, value is a list of manifest names
        # Used in WithBlobs
        self._blobs: Dict[str, List[str]] = {}
        self._sizes: Dict[str, int] = {}

    def __del__(self) -> None:  # noqa:WPS603
        """Destroy a registry connection."""
        self._session.close()

    @property
    def hostname(self) -> str:
        """Get hostname.

        Returns:
            The registry hostname.
        """
        if self._hostname == DOCKER_REGISTRY:
            return DOCKER_HOSTNAME
        return self._hostname

    def request(
        self,
        method: str,
        url: str,
        *,
        scopes: Optional[Set[Scope]] = None,
        params: Params = None,  # noqa: WPS110
        data: Any = None,  # noqa: WPS110
        headers: Optional[Dict[str, str]] = None,
        content_type: Optional[str] = None,
        accept: Optional[Tuple[str, ...]] = None,
        auth: Optional[AuthBase] = None,
        stream: Optional[bool] = None,
        raise_for_status: bool = True,
    ) -> Response:
        """Send an HTTP request.

        Args:
            method: HTTP method.
            url: Either a path or a full url.
            scopes: An optional set of scopes.
            params: query string params.
            data: Request body stream.
            headers: Request headers.
            content_type: Uploaded MIME type.
            accept: An optional list of accepted mime-types.
            auth: HTTPBasicAuth.
            stream: Stream the response.
            raise_for_status: Raises `requests.HTTPError`, if one occurred.

        Returns:
            A Response.
        """
        if url.startswith('/'):
            url = '{0}://{1}{2}'.format(self._scheme, self._hostname, url)
        if headers:
            headers = headers.copy()
        else:
            headers = {}
        if accept:
            headers['Accept'] = ', '.join(accept)
        if content_type:
            headers['Content-Type'] = content_type

        self._connect(scopes)
        response = self._session.request(
            method,
            url,
            params=params,
            data=data,
            headers=headers,
            auth=auth,
            stream=stream,
        )
        if raise_for_status:
            response.raise_for_status()
        return response

    def _connect(self, scopes: Optional[Set[Scope]]) -> None:
        """Connect.

        Args:
            scopes: An optional set of scopes.
        """
        if scopes is None or None in self._tokens:
            self._set_session_auth()
            return
        token = self._get_token(scopes)
        if token:
            self._set_session_auth(token=token)
            return
        response = self.request('get', '/v2/', raise_for_status=False)
        if response.status_code == codes['ok']:
            one_hour = 3600
            self._tokens[None] = Token('no_auth', one_hour)
            return
        if response.status_code == codes['unauthorized']:
            if response.headers['Www-Authenticate'].startswith('Bearer '):
                self._get_bearer_token(response, scopes)
                self._set_session_auth(token=self._get_token(scopes))
                return
        response.raise_for_status()

    def _set_session_auth(self, token: Optional[Token] = None) -> None:
        if token is None:
            if 'Authorization' in self._session.headers:
                self._session.headers.pop('Authorization')
        else:
            self._session.headers['Authorization'] = 'Bearer {0}'.format(token.token)

    def _get_bearer_token(self, response: Response, scopes: Set[Scope]) -> None:
        challenge_parameters = self._get_challenge_parameters(response)
        get_params: SimpleParams = {}
        if 'service' in challenge_parameters:
            get_params['service'] = challenge_parameters.get('service', 'unknown')
        get_params['scope'] = []
        for scope in sorted(scopes):
            get_params['scope'].append(  # type: ignore
                'repository:{0}:{1}'.format(scope.remote_name, scope.actions),
            )
        response = self.request(
            'get',
            challenge_parameters['realm'],
            params=get_params,
            headers=self._auth_info.headers,
            auth=self._auth_info.auth,
        )
        json = response.json()
        self._set_token(
            scopes,
            Token(
                str(json.get('token', json.get('access_token', ''))),
                int(json.get('expires_in', 0)),
            ),
        )

    def _get_challenge_parameters(self, response: Response) -> Dict[str, str]:
        _, _, challenge = response.headers['Www-Authenticate'].partition('Bearer ')
        return parse_keqv_list(parse_http_list(challenge))

    def _get_token(self, scopes: Set[Scope]) -> Optional[Token]:
        key = self._scopes_hash(scopes)
        token = self._tokens.get(key)
        if token and token.is_expired():
            self._tokens.pop(key)
            return None
        return token

    def _set_token(self, scopes: Set[Scope], token: Token) -> None:
        self._tokens[self._scopes_hash(scopes)] = token

    def _scopes_hash(self, scopes: Set[Scope]) -> Optional[str]:
        return ','.join(map(str, sorted(scopes)))
