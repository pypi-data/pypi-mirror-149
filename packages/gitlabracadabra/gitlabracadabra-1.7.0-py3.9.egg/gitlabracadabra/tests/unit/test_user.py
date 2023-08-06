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

from gitlabracadabra.objects.user import GitLabracadabraUser
from gitlabracadabra.tests import my_vcr
from gitlabracadabra.tests.case import TestCaseWithManager


class TestUser(TestCaseWithManager):
    @my_vcr.use_cassette
    def test_no_create(self, cass):
        obj = GitLabracadabraUser('memory', 'no_create_user', {})
        obj.process()
        self.assertTrue(cass.all_played)

    @my_vcr.use_cassette
    def test_create(self, cass):
        obj = GitLabracadabraUser('memory', 'create_user', {
            'create_object': True,
            'email': 'create_user@example.org',
            'name': 'Create User',
            'password': 'P@ssw0rdNot24get',
        })
        obj.process()
        self.assertTrue(cass.all_played)

    @my_vcr.use_cassette
    def test_delete(self, cass):
        obj = GitLabracadabraUser('memory', 'delete_this_user', {'delete_object': True})
        obj.process()
        self.assertTrue(cass.all_played)

    @my_vcr.use_cassette
    def test_exists(self, cass):
        obj = GitLabracadabraUser('memory', 'user_exists', {})
        obj.process()
        self.assertTrue(cass.all_played)

    @my_vcr.use_cassette
    def test_simple_parameters(self, cass):
        obj = GitLabracadabraUser('memory', 'user_simple_parameters', {
            'name': 'user-with-simple-parameters',
            'email': 'user-with-simple-parameters@example.org',
            'skip_confirmation': True,
            'skip_reconfirmation': True,
            'public_email': 'contact@example.org',
            'password': 'P@ss12345678',
            # 'reset_password'
            'projects_limit': 42,
            'can_create_group': False,
            'admin': True,
            'external': True,
            'shared_runners_minutes_limit': 42,
            'extra_shared_runners_minutes_limit': 42,
            # 'avatar'
            'skype': '12345',
            'linkedin': 'linked_in',
            'twitter': 't_w_i_t_t_e_r',
            'website_url': 'https://example.org',
            'location': 'Nowhere',
            'organization': 'My Corp',
            'bio': 'Not much',
            'private_profile': True,
            'note': 'Fake account?',
            'extern_uid': '12345678',
            'provider': 'github',
            # 'color_scheme_id'
            # 'theme_id'
            # 'force_random_password'
            # 'group_id_for_saml'
            # 'view_diffs_file_by_file'
        })
        self.assertEqual(obj.errors(), [])
        obj.process()
        self.assertTrue(cass.all_played)

    @my_vcr.use_cassette
    def test_block(self, cass):
        # from active
        obj = GitLabracadabraUser('memory', 'userfoo', {'state': 'blocked'})
        obj.process()
        self.assertTrue(cass.all_played)

    @my_vcr.use_cassette
    def test_unblock(self, cass):
        # from blocked
        obj = GitLabracadabraUser('memory', 'userfoo', {'state': 'active'})
        obj.process()
        self.assertTrue(cass.all_played)

    @my_vcr.use_cassette
    def test_deactivate(self, cass):
        # from active
        obj = GitLabracadabraUser('memory', 'userfoo', {'state': 'deactivated'})
        obj.process()
        self.assertTrue(cass.all_played)

    @my_vcr.use_cassette
    def test_activate(self, cass):
        # from deactivated
        obj = GitLabracadabraUser('memory', 'userfoo', {'state': 'active'})
        obj.process()
        self.assertTrue(cass.all_played)
