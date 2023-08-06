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

import logging
from pathlib import PurePosixPath
from typing import TYPE_CHECKING, Match, Optional, Tuple

from gitlabracadabra.containers.registries import ReferenceParts, Registries
from gitlabracadabra.matchers import Matcher


if TYPE_CHECKING:
    from typing import Any, Dict, List

    from gitlabracadabra.containers.registry import Registry


logger = logging.getLogger(__name__)

Source = Tuple[PurePosixPath, str, Match, Optional[str]]


class ImageMirrorsMixin(object):
    """Object (Project) with image mirrors."""

    def _process_image_mirrors(
        self,
        param_name: str,
        param_value: Any,
        dry_run: bool = False,
        skip_save: bool = False,
    ) -> None:
        """Process the image_mirrors param.

        Args:
            param_name: "image_mirrors".
            param_value: List of image mirror dicts.
            dry_run: Dry run.
            skip_save: False.
        """
        assert param_name == 'image_mirrors'  # noqa: S101
        assert not skip_save  # noqa: S101

        dest_registry, prefix = self._get_destination()

        for image_mirror in param_value:
            self._mirror(image_mirror, dest_registry, prefix, dry_run=dry_run)

    def _get_destination(self) -> Tuple[Registry, PurePosixPath]:
        # https://gitlab.com/gitlab-org/gitlab/-/merge_requests/54090
        try:
            container_registry_image_prefix = self._obj.container_registry_image_prefix  # type: ignore
        except AttributeError:
            container_registry_image_prefix = None
        if not isinstance(container_registry_image_prefix, str):
            raise ValueError('Unexpected type for container_registry_image_prefix: {0}'.format(
                type(container_registry_image_prefix),
            ))

        netloc, path = container_registry_image_prefix.split('/', 1)
        registry = Registries().get_registry(netloc, self.registry_auth_info)  # type: ignore
        return (registry, PurePosixPath(path))

    def _mirror(  # noqa: WPS210
        self,
        image_mirror: Dict,
        dest_registry: Registry,
        prefix: PurePosixPath,
        *,
        dry_run: bool,
    ) -> None:
        sources = self._get_sources(image_mirror.get('from'), image_mirror.get('semver'))
        for source in sources:
            dest = self._get_dest(
                source[0],
                source[1],
                source[2],
                source[3],
                image_mirror.get('to'),
            )
            digest_suffix = ''
            if source[3]:
                digest_suffix = '@{0}'.format(source[3])
            source_manifest = Registries().get_manifest('{0}:{1}{2}'.format(
                str(source[0] / source[1]),
                source[2][0],
                digest_suffix,
            ))
            source_manifest.forced_digest = source[3] is not None
            dest_manifest = Registries().get_manifest(ReferenceParts(
                dest_registry.hostname,
                str(prefix / dest[0]),
                dest[1],
                None,
            ))
            dest_manifest.registry.import_manifest(
                source_manifest,
                dest_manifest.manifest_name,
                tag=dest_manifest.tag,
                platform=None,
                log_prefix='[{0}] '.format(self._name),  # type: ignore
                dry_run=dry_run,
            )

    def _get_sources(self, from_param: Any, semver: Optional[str]) -> List[Source]:
        """Get sources.

        Args:
            from_param: The "from" param.
            semver: Optional "semver" param.

        Returns:
            A list of tuples (base, repository, tag, digest)

        Raises:
            ValueError: Unexpected from param type.
        """
        default_tag = 'latest'
        if semver:
            default_tag = '/.*/'
        if isinstance(from_param, str):
            parts = Registries().full_reference_parts(from_param)
            return self._get_sources_from_parts(
                PurePosixPath(parts.hostname),
                [parts.manifest_name],
                [parts.tag or default_tag],
                parts.digest,
                semver,
            )
        elif isinstance(from_param, dict):
            base = PurePosixPath(from_param.get('base', ''))
            repositories = from_param.get('repositories', None)
            tags = from_param.get('tags', [default_tag])
            return self._get_sources_from_parts(base, repositories, tags, None, semver)
        raise ValueError('Unexpected from param type: {0}'.format(type(from_param)))

    def _get_sources_from_parts(
        self,
        base: PurePosixPath,
        repositories: List[str],
        tags: List[str],
        digest: Optional[str],
        semver: Optional[str],
    ) -> List[Source]:
        if not isinstance(repositories, list):
            raise ValueError('Unexpected from.repositories param type: {0}'.format(type(repositories)))
        if not isinstance(tags, list):
            raise ValueError('Unexpected from.tags param type: {0}'.format(type(tags)))
        sources: List[Source] = []
        for repository in repositories:
            matcher = Matcher(
                tags,
                semver,
                log_prefix='[{0}] '.format(self._name),  # type: ignore
            )
            manifest = Registries().get_manifest(str(base / repository))
            for match in matcher.match(manifest.tag_list):
                sources.append((base, repository, match, digest))
        return sources

    def _get_dest(
        self,
        source_base: PurePosixPath,
        source_repository: str,
        source_tag: Match,
        source_digest: Optional[str],
        to_param: Any,
    ) -> Tuple[str, str]:
        """Get Destination.

        Args:
            source_base: base as PurePosixPath.
            source_repository: source repository, relative to base.
            source_tag: source tag.
            source_digest: source digest.
            to_param: "to" parameter.

        Returns:
            A tuple (repository, tag)

        Raises:
            ValueError: Unexpected to param type.
        """
        if to_param is None:
            repository = str(source_base / source_repository).split('/', 1).pop()
            return repository, source_tag[0]
        elif isinstance(to_param, str):
            tag: Optional[str]
            try:
                to_param, tag = to_param.rsplit(':', 1)
            except ValueError:
                tag = None
            return to_param, tag or source_tag[0]
        elif isinstance(to_param, dict):
            return self._get_dest_from_dict(source_base, source_repository, source_tag, source_digest, to_param)
        raise ValueError('Unexpected to param type: {0}'.format(type(to_param)))

    def _get_dest_from_dict(
        self,
        source_base: PurePosixPath,
        source_repository: str,
        source_tag: Match,
        source_digest: Optional[str],
        to_param: Dict,
    ) -> Tuple[str, str]:
        base = PurePosixPath(to_param.get('base', source_base) or '')
        repository = to_param.get('repository', source_repository) or ''
        tag = source_tag.expand(to_param.get('tag') or source_tag[0])
        return str(base / repository), tag
