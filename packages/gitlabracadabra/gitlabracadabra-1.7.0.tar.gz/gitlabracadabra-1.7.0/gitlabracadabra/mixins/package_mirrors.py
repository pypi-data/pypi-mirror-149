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

from copy import deepcopy
from logging import getLogger
from typing import Any

from gitlabracadabra.packages.github import Github
from gitlabracadabra.packages.gitlab import Gitlab
from gitlabracadabra.packages.helm import Helm
from gitlabracadabra.packages.pypi import PyPI
from gitlabracadabra.packages.raw import RawSource
from gitlabracadabra.packages.source import Source


logger = getLogger(__name__)


class PackageMirrorsMixin(object):
    """Object (Project) with package mirrors."""

    def _process_package_mirrors(
        self,
        param_name: str,
        param_value: Any,
        dry_run: bool = False,
        skip_save: bool = False,
    ) -> None:
        """Process the package_mirrors param.

        Args:
            param_name: "package_mirrors".
            param_value: List of package mirror dicts.
            dry_run: Dry run.
            skip_save: False.
        """
        assert param_name == 'package_mirrors'  # noqa: S101
        assert not skip_save  # noqa: S101

        destination = Gitlab(
            connection=self.connection,  # type: ignore
            full_path=self._name,  # type: ignore
            project_id=self._obj.id,  # type: ignore
        )

        for package_mirror in param_value:
            for source_type, source_params in package_mirror.items():
                destination.import_source(
                    self._get_source(source_type, deepcopy(source_params)),
                    dry_run=dry_run,
                )

    def _get_source(self, source_type: str, source_params: dict[str, Any]) -> Source:
        source_class = {
            'raw': RawSource,
            'github': Github,
            'helm': Helm,
            'pypi': PyPI,
        }[source_type]
        source_params['log_prefix'] = '[{0}] '.format(self._name)  # type: ignore
        return source_class(**source_params)  # type: ignore
