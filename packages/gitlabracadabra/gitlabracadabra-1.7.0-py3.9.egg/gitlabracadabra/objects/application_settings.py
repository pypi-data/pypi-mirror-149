#!/usr/bin/env python
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

import logging
from typing import List

from gitlabracadabra.objects.object import GitLabracadabraObject


logger = logging.getLogger(__name__)


class GitLabracadabraApplicationSettings(GitLabracadabraObject):
    EXAMPLE_YAML_HEADER = 'application_settings:\n  type: application-settings\n'
    DOC: List[str] = [
        '# Application settings lifecycle',
        'gitlab_id',
    ]
    SCHEMA = {
        '$schema': 'http://json-schema.org/draft-04/schema#',
        'title': 'Application settings',
        'type': 'object',
        'properties': {
            # Standard properties
            'gitlab_id': {
                'type': 'string',
                'description': 'GitLab id',
                '_example': 'gitlab',
                '_doc_link': 'action_file.md#gitlab_id',
            },
            # From https://docs.gitlab.com/ee/api/settings.html#list-of-settings-that-can-be-accessed-via-api-calls
            'admin_notification_email': {
                'type': 'string',
                'description': 'Abuse reports will be sent to this address if it is set. Abuse reports are always '
                               'available in the admin area.',
            },
            'after_sign_out_path': {
                'type': 'string',
                'description': 'Where to redirect users after logout.',
            },
            'after_sign_up_text': {
                'type': 'string',
                'description': 'Text shown to the user after signing up',
            },
            'akismet_api_key': {
                'type': 'string',
                'description': 'API key for akismet spam protection.',
            },
            'akismet_enabled': {
                'type': 'boolean',
                'description': 'Enable or disable akismet spam protection.',
            },
            'allow_group_owners_to_manage_ldap': {  # >= PREMIUM, SILVER
                'type': 'boolean',
                'description': 'Set to true to allow group owners to manage LDAP',
            },
            'allow_local_requests_from_hooks_and_services': {
                'type': 'boolean',
                'description': 'Allow requests to the local network from hooks and services.',
            },
            'archive_builds_in_human_readable': {
                'type': 'string',
                'description': 'Set the duration for which the jobs will be considered as old and expired. Once that '
                               'time passes, the jobs will be archived and no longer able to be retried. Make it empty '
                               'to never expire jobs. It has to be no less than 1 day, for example: `15 days`, `1 '
                               'month`, `2 years`.',
            },
            'authorized_keys_enabled': {
                'type': 'boolean',
                'description': 'By default, we write to the authorized_keys file to support Git over SSH without '
                               'additional configuration. GitLab can be optimized to authenticate SSH keys via the '
                               'database file. Only disable this if you have configured your OpenSSH server to use the '
                               'AuthorizedKeysCommand.',
            },
            'auto_devops_domain': {
                'type': 'string',
                'description': 'Specify a domain to use by default for every project’s Auto Review Apps and Auto '
                               'Deploy stages.',
            },
            'auto_devops_enabled': {
                'type': 'boolean',
                'description': 'Enable Auto DevOps for projects by default. It will automatically build, test, and '
                               'deploy applications based on a predefined CI/CD configuration.',
            },
            'check_namespace_plan': {  # >= PREMIUM, SILVER
                'type': 'boolean',
                'description': 'Enabling this will make only licensed EE features available to projects if the project '
                               'namespace’s plan includes the feature or if the project is public.',
            },
            'commit_email_hostname': {
                'type': 'string',
                'description': ' Custom hostname (for private commit emails).',
            },
            'container_registry_token_expire_delay': {
                'type': 'integer',
                'description': 'Container Registry token duration in minutes.',
            },
            'default_artifacts_expire_in': {
                'type': 'string',
                'description': 'Set the default expiration time for each job’s artifacts.',
            },
            'default_branch_protection': {
                'type': 'integer',
                'description': 'Determine if developers can push to master. Can take: 0 (not protected, both '
                               'developers and maintainers can push new commits, force push, or delete the branch), 1 '
                               '(partially protected, developers and maintainers can push new commits, but cannot '
                               'force push or delete the branch) or 2 (fully protected, developers cannot push new '
                               'commits, but maintainers can; no-one can force push or delete the branch) as a '
                               'parameter. Default is 2.',
                'enum': [0, 1, 2, 3],
            },
            'default_ci_config_path': {
                'type': 'string',
                'description': 'Default CI configuration path for new projects',
            },
            'default_group_visibility': {
                'type': 'string',
                'description': 'What visibility level new groups receive. Can take private, internal and public as a '
                               'parameter. Default is private.',
                'enum': ['private', 'internal', 'public'],
            },
            'default_project_creation': {
                'type': 'integer',
                'description': 'Default project creation protection. Can take: `0` _(No one)_, `1` _(Maintainers)_ or '
                               '`2` _(Developers + Maintainers)_',
                'enum': [0, 1, 2],
            },
            'default_project_visibility': {
                'type': 'string',
                'description': 'What visibility level new projects receive. Can take `private`, `internal` and '
                               '`public` as a parameter.',
                'enum': ['private', 'internal', 'public'],
            },
            'default_projects_limit': {
                'type': 'integer',
                'description': 'Project limit per user.',
            },
            'default_snippet_visibility': {
                'type': 'string',
                'description': 'What visibility level new snippets receive. Can take private, internal and public as a '
                               'parameter. Default is private.',
                'enum': ['private', 'internal', 'public'],
            },
            'diff_max_patch_bytes': {
                'type': 'integer',
                'description': 'Maximum diff patch size (Bytes).',
            },
            'disabled_oauth_sign_in_sources': {
                'type': 'array',
                'description': 'Disabled OAuth sign-in sources.',
                'items': {
                    'type': 'string',
                },
                'uniqueItems': True,
            },
            'dns_rebinding_protection_enabled': {
                'type': 'boolean',
                'description': 'Enforce DNS rebinding attack protection.',
            },
            'domain_blacklist': {
                'type': 'array',
                'description': 'Users with e-mail addresses that match these domain(s) will NOT be able to sign-up. '
                               'Wildcards allowed. Use separate lines for multiple entries. Ex: domain.com, '
                               '*.domain.com.',
                'items': {
                    'type': 'string',
                },
                'uniqueItems': True,
            },
            'domain_blacklist_enabled': {
                'type': 'boolean',
                'description': 'Allows blocking sign-ups from emails from specific domains.',
            },
            'domain_whitelist': {
                'type': 'array',
                'description': 'Force people to use only corporate emails for sign-up. Default is null, meaning there '
                               'is no restriction.',
                'items': {
                    'type': 'string',
                },
                'uniqueItems': True,
            },
            'dsa_key_restriction': {
                'type': 'integer',
                'description': 'The minimum allowed bit length of an uploaded DSA key. Default is 0 (no restriction). '
                               '-1 disables DSA keys.',
            },
            'ecdsa_key_restriction': {
                'type': 'integer',
                'description': 'The minimum allowed curve size (in bits) of an uploaded ECDSA key. Default is 0 (no '
                               'restriction). -1 disables ECDSA keys.',
            },
            'ed25519_key_restriction': {
                'type': 'integer',
                'description': 'The minimum allowed curve size (in bits) of an uploaded ED25519 key. Default is 0 (no '
                               'restriction). -1 disables ED25519 keys.',
            },
            'elasticsearch_aws': {  # >= PREMIUM, SILVER
                'type': 'boolean',
                'description': 'Enable the use of AWS hosted Elasticsearch',
            },
            'elasticsearch_aws_access_key': {  # >= PREMIUM, SILVER
                'type': 'string',
                'description': 'AWS IAM access key',
            },
            'elasticsearch_aws_region': {  # >= PREMIUM, SILVER
                'type': 'string',
                'description': 'The AWS region the elasticsearch domain is configured',
            },
            'elasticsearch_aws_secret_access_key': {  # >= PREMIUM, SILVER
                'type': 'string',
                'description': 'AWS IAM secret access key',
            },
            'elasticsearch_experimental_indexer': {  # >= PREMIUM, SILVER
                'type': 'boolean',
                'description': 'Use the experimental elasticsearch indexer. More info: '
                               'https://gitlab.com/gitlab-org/gitlab-elasticsearch-indexer ',
            },
            'elasticsearch_indexing': {  # >= PREMIUM, SILVER
                'type': 'boolean',
                'description': 'Enable Elasticsearch indexing',
            },
            'elasticsearch_search': {  # >= PREMIUM, SILVER
                'type': 'boolean',
                'description': 'Enable Elasticsearch search',
            },
            'elasticsearch_url': {  # >= PREMIUM, SILVER
                'type': 'string',
                'description': 'The url to use for connecting to Elasticsearch. Use a comma-separated list to support '
                               'cluster (e.g., http://localhost:9200, http://localhost:9201). If your Elasticsearch '
                               'instance is password protected, pass the username:password in the URL (e.g., '
                               'http://<username>:<password>@<elastic_host>:9200/).',
            },
            'elasticsearch_limit_indexing': {  # >= PREMIUM, SILVER
                'type': 'boolean',
                'description': 'Limit Elasticsearch to index certain namespaces and projects',
            },
            'elasticsearch_project_ids': {  # >= PREMIUM, SILVER
                'type': 'array',
                'description': 'The projects to index via Elasticsearch if elasticsearch_limit_indexing is enabled.',
                'items': {
                    'type': 'integer',
                },
                'uniqueItems': True,
            },
            'elasticsearch_namespace_ids': {  # >= PREMIUM, SILVER
                'type': 'array',
                'description': 'The namespaces to index via Elasticsearch if elasticsearch_limit_indexing is enabled.',
                'items': {
                    'type': 'integer',
                },
                'uniqueItems': True,
            },
            'email_additional_text': {  # >= PREMIUM, SILVER
                'type': 'string',
                'description': 'Additional text added to the bottom of every email for legal/auditing/compliance '
                               'reasons',
            },
            'email_author_in_body': {
                'type': 'boolean',
                'description': 'Some email servers do not support overriding the email sender name. Enable this option '
                               'to include the name of the author of the issue, merge request or comment in the email '
                               'body instead.',
            },
            'enabled_git_access_protocol': {
                'type': 'string',
                'description': 'Enabled protocols for Git access. Allowed values are: ssh, http, and nil to allow both '
                               'protocols.',
                'enum': ['ssh', 'http', 'both'],
            },
            'enforce_terms': {
                'type': 'boolean',
                'description': 'Enforce application ToS to all users.',
            },
            'external_auth_client_cert': {
                'type': 'string',
                'description': 'The certificate to use to authenticate with the external authorization service',
            },
            'external_auth_client_key': {
                'type': 'string',
                'description': 'Private key for the certificate when authentication is required for the external '
                               'authorization service, this is encrypted when stored',
            },
            'external_auth_client_key_pass': {
                'type': 'string',
                'description': 'Passphrase to use for the private key when authenticating with the external service '
                               'this is encrypted when stored',
            },
            'external_authorization_service_default_label': {
                'type': 'string',
                'description': 'The default classification label to use when requesting authorization and no '
                               'classification label has been specified on the project',
            },
            'external_authorization_service_enabled': {
                'type': 'boolean',
                'description': 'Enable using an external authorization service for accessing projects',
            },
            'external_authorization_service_timeout': {
                'type': 'number',
                'description': 'The timeout after which an authorization request is aborted, in seconds. When a '
                               'request times out, access is denied to the user. (min: 0.001, max: 10, step: 0.001)',
            },
            'external_authorization_service_url': {
                'type': 'string',
                'description': 'URL to which authorization requests will be directed',
            },
            'file_template_project_id': {  # >= PREMIUM, SILVER
                'type': 'integer',
                'description': 'The ID of a project to load custom file templates from',
            },
            'first_day_of_week': {
                'type': 'string',
                'description': 'Start day of the week for calendar views and date pickers.',
                'enum': ['sunday', 'monday', 'saturday'],
            },
            'geo_node_allowed_ips': {  # PREMIUM, SILVER
                'type': 'string',
                'description': 'Comma-separated list of IPs and CIDRs of allowed secondary nodes. For example, '
                               '1.1.1.1, 2.2.2.0/24.',
            },
            'geo_status_timeout': {  # >= PREMIUM, SILVER
                'type': 'integer',
                'description': 'The amount of seconds after which a request to get a secondary node status will time '
                               'out.',
            },
            'gitaly_timeout_default': {
                'type': 'integer',
                'description': 'Default Gitaly timeout, in seconds. This timeout is not enforced for git fetch/push '
                               'operations or Sidekiq jobs. Set to 0 to disable timeouts.',
            },
            'gitaly_timeout_fast': {
                'type': 'integer',
                'description': 'Gitaly fast operation timeout, in seconds. Some Gitaly operations are expected to be '
                               'fast. If they exceed this threshold, there may be a problem with a storage shard and '
                               '‘failing fast’ can help maintain the stability of the GitLab instance. Set to 0 to '
                               'disable timeouts.',
            },
            'gitaly_timeout_medium': {
                'type': 'integer',
                'description': 'Medium Gitaly timeout, in seconds. This should be a value between the Fast and the '
                               'Default timeout. Set to 0 to disable timeouts.',
            },
            'grafana_enabled': {
                'type': 'boolean',
                'description': 'Enable Grafana.',
            },
            'grafana_url': {
                'type': 'string',
                'description': 'Grafana URL.',
            },
            'gravatar_enabled': {
                'type': 'boolean',
                'description': 'Enable Gravatar.',
            },
            'hashed_storage_enabled': {
                'type': 'boolean',
                'description': 'Create new projects using hashed storage paths: Enable immutable, hash-based paths and '
                               'repository names to store repositories on disk. This prevents repositories from having '
                               'to be moved or renamed when the Project URL changes and may improve disk I/O '
                               'performance. (EXPERIMENTAL)',
            },
            'help_page_hide_commercial_content': {
                'type': 'boolean',
                'description': 'Hide marketing-related entries from help.',
            },
            'help_page_support_url': {
                'type': 'string',
                'description': 'Alternate support URL for help page.',
            },
            'help_page_text': {
                'type': 'string',
                'description': 'Custom text displayed on the help page.',
            },
            'help_text': {  # >= PREMIUM, SILVER
                'type': 'string',
                'description': 'GitLab server administrator information',
            },
            'hide_third_party_offers': {
                'type': 'boolean',
                'description': 'Do not display offers from third parties within GitLab.',
            },
            'home_page_url': {
                'type': 'string',
                'description': 'Redirect to this URL when not logged in.',
            },
            'housekeeping_enabled': {
                'type': 'boolean',
                'description': 'Enable or disable git housekeeping.',
            },
            'housekeeping_full_repack_period': {
                'type': 'integer',
                'description': 'Number of Git pushes after which an incremental git repack is run.',
            },
            'housekeeping_gc_period': {
                'type': 'integer',
                'description': 'Number of Git pushes after which git gc is run.',
            },
            'housekeeping_incremental_repack_period': {
                'type': 'integer',
                'description': 'Number of Git pushes after which an incremental git repack is run.',
            },
            'html_emails_enabled': {
                'type': 'boolean',
                'description': 'Enable HTML emails.',
            },
            'import_sources': {
                'type': 'array',
                'description': 'Sources to allow project import from, possible values.',
                'items': {
                    'type': 'string',
                    'enum': [
                        'github',
                        'bitbucket',
                        'bitbucket_server',
                        'gitlab',
                        'google_code',
                        'fogbugz',
                        'git',
                        'gitlab_project',
                        'gitea',
                        'manifest',
                        'phabricator',
                    ],
                },
                'uniqueItems': True,
            },
            'instance_statistics_visibility_private': {
                'type': 'boolean',
                'description': 'When set to true Instance statistics will only be available to admins.',
            },
            'local_markdown_version': {
                'type': 'integer',
                'description': 'Increase this value when any cached markdown should be invalidated.',
            },
            'max_artifacts_size': {
                'type': 'integer',
                'description': 'Maximum artifacts size in MB',
            },
            'max_attachment_size': {
                'type': 'integer',
                'description': 'Limit attachment size in MB',
            },
            'max_pages_size': {
                'type': 'integer',
                'description': 'Maximum size of pages repositories in MB',
            },
            'metrics_enabled': {
                'type': 'boolean',
                'description': 'Enable influxDB metrics.',
            },
            'metrics_host': {
                'type': 'string',
                'description': 'InfluxDB host.',
            },
            'metrics_method_call_threshold': {
                'type': 'integer',
                'description': 'A method call is only tracked when it takes longer than the given amount of '
                               'milliseconds.',
            },
            'metrics_packet_size': {
                'type': 'integer',
                'description': 'The amount of datapoints to send in a single UDP packet.',
            },
            'metrics_pool_size': {
                'type': 'integer',
                'description': 'The amount of InfluxDB connections to keep open.',
            },
            'metrics_port': {
                'type': 'integer',
                'description': 'The UDP port to use for connecting to InfluxDB.',
            },
            'metrics_sample_interval': {
                'type': 'integer',
                'description': 'The sampling interval in seconds.',
            },
            'metrics_timeout': {
                'type': 'integer',
                'description': 'The amount of seconds after which InfluxDB will time out.',
            },
            'mirror_available': {
                'type': 'boolean',
                'description': 'Allow mirrors to be set up for projects. If disabled, only admins will be able to set '
                               'up mirrors in projects.',
            },
            'mirror_capacity_threshold': {  # >= PREMIUM, SILVER
                'type': 'integer',
                'description': 'Minimum capacity to be available before scheduling more mirrors preemptively',
            },
            'mirror_max_capacity': {  # >= PREMIUM, SILVER
                'type': 'integer',
                'description': 'Maximum number of mirrors that can be synchronizing at the same time.',
            },
            'mirror_max_delay': {  # >= PREMIUM, SILVER
                'type': 'integer',
                'description': 'Maximum time (in minutes) between updates that a mirror can have when scheduled to '
                               'synchronize.',
            },
            'pages_domain_verification_enabled': {
                'type': 'boolean',
                'description': 'Require users to prove ownership of custom domains. Domain verification is an '
                               'essential security measure for public GitLab sites. Users are required to demonstrate '
                               'they control a domain before it is enabled.',
            },
            'password_authentication_enabled_for_git': {
                'type': 'boolean',
                'description': 'Enable authentication for Git over HTTP(S) via a GitLab account password. Default is '
                               'true.',
            },
            'password_authentication_enabled_for_web': {
                'type': 'boolean',
                'description': 'Enable authentication for the web interface via a GitLab account password. Default is '
                               'true.',
            },
            'performance_bar_allowed_group_path': {
                'type': 'string',
                'description': 'Path of the group that is allowed to toggle the performance bar.',
            },
            'plantuml_enabled': {
                'type': 'boolean',
                'description': 'Enable PlantUML integration.',
            },
            'plantuml_url': {
                'type': 'string',
                'description': 'The PlantUML instance URL for integration.',
            },
            'polling_interval_multiplier': {
                'type': 'number',
                'description': 'Interval multiplier used by endpoints that perform polling. Set to 0 to disable '
                               'polling.',
            },
            'project_export_enabled': {
                'type': 'boolean',
                'description': 'Enable project export.',
            },
            'prometheus_metrics_enabled': {
                'type': 'boolean',
                'description': 'Enable prometheus metrics.',
            },
            'protected_ci_variables': {
                'type': 'boolean',
                'description': 'Environment variables are protected by default.',
            },
            'pseudonymizer_enabled': {  # >= PREMIUM, SILVER
                'type': 'boolean',
                'description': 'When enabled, GitLab will run a background job that will produce pseudonymized CSVs of '
                               'the GitLab database that will be uploaded to your configured object storage directory.',
            },
            'recaptcha_enabled': {
                'type': 'boolean',
                'description': 'Enable recaptcha.',
            },
            'recaptcha_private_key': {
                'type': 'string',
                'description': 'Private key for recaptcha.',
            },
            'recaptcha_site_key': {
                'type': 'string',
                'description': 'Site key for recaptcha.',
            },
            'receive_max_input_size': {
                'type': 'integer',
                'description': 'Maximum push size (MB).',
            },
            'repository_checks_enabled': {
                'type': 'boolean',
                'description': 'GitLab will periodically run git fsck in all project and wiki repositories to look for '
                               'silent disk corruption issues.',
            },
            'repository_size_limit': {  # >= PREMIUM, SILVER
                'type': 'integer',
                'description': 'Size limit per repository (MB)',
            },
            'repository_storages': {
                'type': 'array',
                'description': 'A list of names of enabled storage paths, taken from gitlab.yml. New projects will be '
                               'created in one of these stores, chosen at random.',
                'items': {
                    'type': 'string',
                },
                'uniqueItems': True,
            },
            'require_two_factor_authentication': {
                'type': 'boolean',
                'description': 'Require all users to set up Two-factor authentication.',
            },
            'restricted_visibility_levels': {
                'type': 'array',
                'description': 'Selected levels cannot be used by non-admin users for groups, projects or snippets. '
                               'Can take private, internal and public as a parameter. Default is null which means '
                               'there is no restriction.',
                'items': {
                    'type': 'string',
                    'enum': ['private', 'internal', 'public'],
                },
                'uniqueItems': True,
            },
            'rsa_key_restriction': {
                'type': 'integer',
                'description': 'The minimum allowed bit length of an uploaded RSA key. Default is 0 (no restriction). '
                               '-1 disables RSA keys.',
            },
            'send_user_confirmation_email': {
                'type': 'boolean',
                'description': 'Send confirmation email on sign-up.',
            },
            'session_expire_delay': {
                'type': 'integer',
                'description': 'Session duration in minutes. GitLab restart is required to apply changes',
            },
            'shared_runners_enabled': {
                'type': 'boolean',
                'description': 'Enable shared runners for new projects.',
            },
            'shared_runners_minutes': {  # PREMIUM, SILVER
                'type': 'integer',
                'description': 'Set the maximum number of pipeline minutes that a group can use on shared Runners per '
                               'month.',
            },
            'shared_runners_text': {
                'type': 'string',
                'description': 'Shared runners text.',
            },
            'sign_in_text': {
                'type': 'string',
                'description': 'Text on the login page.',
            },
            'signup_enabled': {
                'type': 'boolean',
                'description': 'Enable registration.',
            },
            'slack_app_enabled': {  # PREMIUM, SILVER
                'type': 'boolean',
                'description': ' Enable Slack app.',
            },
            'slack_app_id': {  # PREMIUM, SILVER
                'type': 'string',
                'description': 'The app id of the Slack-app.',
            },
            'slack_app_secret': {  # PREMIUM, SILVER
                'type': 'string',
                'description': 'The app secret of the Slack-app.',
            },
            'slack_app_verification_token': {  # PREMIUM, SILVER
                'type': 'string',
                'description': 'The verification token of the Slack-app.',
            },
            'terminal_max_session_time': {
                'type': 'integer',
                'description': 'Maximum time for web terminal websocket connection (in seconds). Set to 0 for '
                               'unlimited time.',
            },
            'terms': {
                'type': 'string',
                'description': 'Markdown content for the ToS.',
            },
            'throttle_authenticated_api_enabled': {
                'type': 'boolean',
                'description': 'Enable authenticated API request rate limit. Helps reduce request volume (e.g. from '
                               'crawlers or abusive bots).',
            },
            'throttle_authenticated_api_period_in_seconds': {
                'type': 'integer',
                'description': 'Rate limit period in seconds.',
            },
            'throttle_authenticated_api_requests_per_period': {
                'type': 'integer',
                'description': 'Max requests per period per user.',
            },
            'throttle_authenticated_web_enabled': {
                'type': 'boolean',
                'description': 'Enable authenticated web request rate limit. Helps reduce request volume (e.g. from '
                               'crawlers or abusive bots).',
            },
            'throttle_authenticated_web_period_in_seconds': {
                'type': 'integer',
                'description': 'Rate limit period in seconds.',
            },
            'throttle_authenticated_web_requests_per_period': {
                'type': 'integer',
                'description': 'Max requests per period per user.',
            },
            'throttle_unauthenticated_enabled': {
                'type': 'boolean',
                'description': 'Enable unauthenticated request rate limit. Helps reduce request volume (e.g. from '
                               'crawlers or abusive bots).',
            },
            'throttle_unauthenticated_period_in_seconds': {
                'type': 'integer',
                'description': 'Rate limit period in seconds.',
            },
            'throttle_unauthenticated_requests_per_period': {
                'type': 'integer',
                'description': 'Max requests per period per IP.',
            },
            'time_tracking_limit_to_hours': {
                'type': 'boolean',
                'description': 'Limit display of time tracking units to hours. Default is false.',
            },
            'two_factor_grace_period': {
                'type': 'integer',
                'description': 'Amount of time (in hours) that users are allowed to skip forced configuration of '
                               'two-factor authentication.',
            },
            'unique_ips_limit_enabled': {
                'type': 'boolean',
                'description': 'Limit sign in from multiple ips.',
            },
            'unique_ips_limit_per_user': {
                'type': 'integer',
                'description': 'Maximum number of ips per user.',
            },
            'unique_ips_limit_time_window': {
                'type': 'integer',
                'description': 'How many seconds an IP will be counted towards the limit.',
            },
            'usage_ping_enabled': {
                'type': 'boolean',
                'description': 'Every week GitLab will report license usage back to GitLab, Inc.',
            },
            'user_default_external': {
                'type': 'boolean',
                'description': 'Newly registered users will be external by default.',
            },
            'user_default_internal_regex': {
                'type': 'string',
                'description': 'Specify an e-mail address regex pattern to identify default internal users.',
            },
            'user_oauth_applications': {
                'type': 'boolean',
                'description': 'Allow users to register any application to use GitLab as an OAuth provider.',
            },
            'user_show_add_ssh_key_message': {
                'type': 'boolean',
                'description': 'When set to false disable the “You won’t be able to pull or push project code via SSH” '
                               'warning shown to users with no uploaded SSH key.',
            },
            'version_check_enabled': {
                'type': 'boolean',
                'description': 'Let GitLab inform you when an update is available.',
            },
            'web_ide_clientside_preview_enabled': {
                'type': 'boolean',
                'description': 'Client side evaluation (Allow live previews of JavaScript projects in the Web IDE '
                               'using CodeSandbox client side evaluation).',
            },
        },
        'additionalProperties': False,
        'dependencies': {
            'akismet_enabled': ['akismet_api_key'],
            'domain_blacklist_enabled': ['domain_blacklist'],
            'elasticsearch_aws': ['elasticsearch_aws_region'],
            'elasticsearch_indexing': ['elasticsearch_url'],
            'enforce_terms': ['terms'],
            'external_auth_client_cert': ['external_auth_client_key'],
            'external_authorization_service_enabled': ['external_authorization_service_timeout',
                                                       'external_authorization_service_url'],
            'housekeeping_enabled': ['housekeeping_full_repack_period',
                                     'housekeeping_gc_period', 'housekeeping_incremental_repack_period'],
            'metrics_enabled': ['metrics_host', 'metrics_method_call_threshold', 'metrics_packet_size',
                                'metrics_pool_size', 'metrics_port', 'metrics_sample_interval', 'metrics_timeout'],
            'plantuml_enabled': ['plantuml_url'],
            'recaptcha_enabled': ['recaptcha_site_key', 'recaptcha_private_key'],
            'require_two_factor_authentication': ['two_factor_grace_period'],
            'shared_runners_enabled': ['shared_runners_text'],
        },
    }

    """"_object_manager()

    Return the python-gitlab Gilab object.
    """
    def _object_manager(self):
        return self.pygitlab.settings

    """"_get()

    Set the _object attribute
    """
    def _get(self):
        obj_manager = self._object_manager()
        self._obj = obj_manager.get()

    """"_mangle_param()

    Convert a param value from GitLabracadabra form to API form.
    """
    def _mangle_param(self, param_name, param_value):
        if param_name == 'first_day_of_week':
            if param_value == 'sunday':
                return 0
            if param_value == 'monday':
                return 1
            if param_value == 'saturday':
                return 6
        # https://github.com/python-gitlab/python-gitlab/blob/8753add72061ea01c508a42d16a27388b1d92677/gitlab/v4/objects/settings.py#L80-L87
        if param_name in [
            'asset_proxy_allowlist',
            'disabled_oauth_sign_in_sources',
            'domain_allowlist',
            'domain_denylist',
            'import_sources',
            'restricted_visibility_levels',
        ]:
            return ','.join([str(x) for x in param_value])
        return GitLabracadabraObject._mangle_param(self, param_name, param_value)

    """"_unmangle_param()

    Convert a param value from API form to GitLabracadabra form.
    """
    def _unmangle_param(self, param_name, param_value):
        if param_name == 'first_day_of_week':
            if param_value == 0:
                return 'sunday'
            if param_value == 1:
                return 'monday'
            if param_value == 6:
                return 'saturday'
        return GitLabracadabraObject._unmangle_param(self, param_name, param_value)
