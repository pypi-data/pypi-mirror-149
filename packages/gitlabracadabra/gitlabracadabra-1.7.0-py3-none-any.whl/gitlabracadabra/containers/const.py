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


# =============================================================================
# Media Types (i.e. MIME types)
# =============================================================================

OCI_IMAGE_MANIFEST = 'application/vnd.oci.image.manifest.v1+json'
OCI_IMAGE_INDEX = 'application/vnd.oci.image.index.v1+json'

DOCKER_MANIFEST_SCHEMA2 = 'application/vnd.docker.distribution.manifest.v2+json'
DOCKER_MANIFEST_SCHEMA1_SIGNED = 'application/vnd.docker.distribution.manifest.v1+prettyjws'
DOCKER_MANIFEST_SCHEMA1 = 'application/vnd.docker.distribution.manifest.v1+json'
DOCKER_MANIFEST_SCHEMA2_LIST = 'application/vnd.docker.distribution.manifest.list.v2+json'

MANIFEST = (
    OCI_IMAGE_MANIFEST,
    DOCKER_MANIFEST_SCHEMA2,
    DOCKER_MANIFEST_SCHEMA1_SIGNED,
    DOCKER_MANIFEST_SCHEMA1,
    DOCKER_MANIFEST_SCHEMA2_LIST,
    OCI_IMAGE_INDEX,
)

MANIFEST_LIST = (
    DOCKER_MANIFEST_SCHEMA2_LIST,
    # OCI_IMAGE_INDEX,
)

# =============================================================================
# Domains
# =============================================================================

DOCKER_HOSTNAME = 'docker.io'
DOCKER_REGISTRY = 'registry-1.docker.io'

# =============================================================================
# Headers
# =============================================================================

DIGEST_HEADER = 'Docker-Content-Digest'
