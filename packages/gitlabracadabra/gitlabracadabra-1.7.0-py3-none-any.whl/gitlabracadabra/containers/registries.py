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

from collections import namedtuple
from re import search as re_search, sub as re_sub
from typing import Dict, Optional, Tuple, Union

from gitlabracadabra.auth_info import AuthInfo
from gitlabracadabra.containers.const import DOCKER_HOSTNAME, DOCKER_REGISTRY
from gitlabracadabra.containers.manifest import Manifest
from gitlabracadabra.containers.registry import Registry
from gitlabracadabra.singleton import SingletonMeta


ReferenceParts = namedtuple('ReferenceParts', ['hostname', 'manifest_name', 'tag', 'digest'])


class Registries(object, metaclass=SingletonMeta):
    """All registies by name."""

    def __init__(self) -> None:
        """All connected registries.

        Intented to be used as a singleton.
        """
        self._registries: Dict[str, Registry] = {}

    def reset(self) -> None:
        """Reset registry cache."""
        self._registries = {}

    def get_registry(self, hostname: str, auth_info: Optional[AuthInfo] = None) -> Registry:
        """Get a registry connection.

        Args:
            hostname: fqdn of a registry.
            auth_info: Authentication information.

        Returns:
            The registry with the given hostname
        """
        if hostname == DOCKER_REGISTRY:
            hostname = DOCKER_HOSTNAME
        if hostname not in self._registries:
            self._registries[hostname] = Registry(hostname, auth_info)
        return self._registries[hostname]

    def get_manifest(self, name: Union[str, ReferenceParts]) -> Manifest:
        """Get a manifest.

        Args:
            name: Reference name, or reference parts.

        Returns:
            The Manifest with the given full reference name.
        """
        if isinstance(name, str):
            full_reference_parts = self.full_reference_parts(name)
        else:
            full_reference_parts = name
        registry = self.get_registry(full_reference_parts.hostname)
        return Manifest(
            registry,
            full_reference_parts.manifest_name,
            full_reference_parts.digest,
            tag=full_reference_parts.tag,
        )

    @classmethod
    def short_reference(cls, name: str) -> str:
        """Get short reference (i.e. familiar name).

        Args:
            name: Reference name.

        Returns:
            The corresponding short reference name.
        """
        short_reference = cls.full_reference(name)
        if short_reference.startswith('{0}/library/'.format(DOCKER_HOSTNAME)):
            prefix_len = len(DOCKER_HOSTNAME) + 1 + len('library') + 1
            short_reference = short_reference[prefix_len:]
        if short_reference.startswith('{0}/'.format(DOCKER_HOSTNAME)):
            prefix_len = len(DOCKER_HOSTNAME) + 1
            short_reference = short_reference[prefix_len:]
        return re_sub(':latest(@sha256:[0-9A-Fa-f]{64})?$', r'\1', short_reference)

    @classmethod
    def full_reference(cls, name: str) -> str:
        """Get full reference.

        Args:
            name: Reference name.

        Returns:
            The corresponding full reference name.
        """
        full_reference_parts = cls.full_reference_parts(name)
        full_reference = '{0}/{1}'.format(full_reference_parts.hostname, full_reference_parts.manifest_name)
        if full_reference_parts.tag:
            full_reference = '{0}:{1}'.format(full_reference, full_reference_parts.tag)
        if full_reference_parts.digest:
            full_reference = '{0}@{1}'.format(full_reference, full_reference_parts.digest)
        return full_reference

    @classmethod
    def full_reference_parts(cls, name: str) -> ReferenceParts:
        """Get full reference parts (hostname, manifest_name, tag, digest).

        Args:
            name: Reference name.

        Returns:
            The corresponding full reference parts.
        """
        hostname, remaining = cls._split_docker_domain(name)
        digest: Optional[str]
        tag: Optional[str]
        try:
            remaining, digest = remaining.split('@', 1)
        except ValueError:
            digest = None
        try:
            remaining, tag = remaining.split(':', 1)
        except ValueError:
            tag = None
        if hostname == DOCKER_HOSTNAME and '/' not in remaining:
            remaining = 'library/{0}'.format(remaining)
        return ReferenceParts(hostname, remaining, tag, digest)

    @classmethod
    def _split_docker_domain(cls, name: str) -> Tuple[str, str]:
        parts = name.split('/', 1)
        if len(parts) == 2 and re_search(r'^localhost$|:\d|\.', parts[0]):
            return parts[0], parts[1]
        return DOCKER_HOSTNAME, name
