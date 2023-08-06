"""SampleTest class"""

import unittest

from metadata_client.metadata_client import MetadataClient
from .module_base import ModuleBase
from ..common.config_test import *
from ..common.generators import Generators
from ..common.secrets import *
from ...modules.sample import Sample

MODULE_NAME = SAMPLE


class SampleTest(ModuleBase, unittest.TestCase):
    def setUp(self):
        self.mdc_client = MetadataClient(
            client_id=CLIENT_OAUTH2_INFO['CLIENT_ID'],
            client_secret=CLIENT_OAUTH2_INFO['CLIENT_SECRET'],
            token_url=CLIENT_OAUTH2_INFO['TOKEN_URL'],
            refresh_url=CLIENT_OAUTH2_INFO['REFRESH_URL'],
            auth_url=CLIENT_OAUTH2_INFO['AUTH_URL'],
            scope=CLIENT_OAUTH2_INFO['SCOPE'],
            user_email=CLIENT_OAUTH2_INFO['EMAIL'],
            base_api_url=BASE_API_URL
        )

        __unique_name1 = Generators.generate_unique_name('Sample01')
        self.sample_01 = {
            'name': __unique_name1,
            'url': 'https://in.xfel.eu/upex/sample/101',
            'sample_type_id': '1',
            'proposal_id': '-1',
            'flg_proposal_system': 'U',
            'proposal_system_id': '-123',
            'flg_available': 'true',
            'description': 'desc 01'
        }

        __unique_name_upd = Generators.generate_unique_name('SampleUpd1')
        self.sample_01_upd = {
            'name': __unique_name_upd,
            'url': 'https://in.xfel.eu/upex/sample/202',
            'sample_type_id': '1',
            'proposal_id': '-1',
            'flg_proposal_system': 'U',
            'proposal_system_id': '-321',
            'flg_available': 'false',
            'description': 'desc 01 updated!!!'
        }

    def test_create_sample(self):
        sample_01 = Sample(
            metadata_client=self.mdc_client,
            name=self.sample_01['name'],
            url=self.sample_01['url'],
            sample_type_id=self.sample_01['sample_type_id'],
            proposal_id=self.sample_01['proposal_id'],
            flg_proposal_system=self.sample_01['flg_proposal_system'],
            proposal_system_id=self.sample_01['proposal_system_id'],
            flg_available=self.sample_01['flg_available'],
            description=self.sample_01['description'])

        #
        # Create new entry (should succeed)
        #
        result1 = sample_01.create()
        self.assert_create_success(MODULE_NAME, result1, self.sample_01)

        sample = result1['data']
        sample_id = result1['data']['id']
        sample_name = result1['data']['name']
        sample_proposal_id = result1['data']['proposal_id']

        #
        # Create duplicated entry (should throw an error)
        #
        sample_01_dup = sample_01
        result2 = sample_01_dup.create()
        expect_app_info = {'name': ['has already been taken']}
        self.assert_create_error(MODULE_NAME, result2, expect_app_info)

        #
        # Get entry by name and proposal_id
        #
        result3 = Sample.get_by_name_and_proposal_id(self.mdc_client,
                                                     sample_name,
                                                     sample_proposal_id)
        self.assert_find_success(MODULE_NAME, result3, self.sample_01)

        #
        # Get entry by ID
        #
        result4 = Sample.get_by_id(self.mdc_client, sample_id)
        self.assert_find_success(MODULE_NAME, result4, self.sample_01)

        #
        # Get entry with non-existent ID (should throw an error)
        #
        result5 = Sample.get_by_id(self.mdc_client, -666)
        self.assert_find_error(MODULE_NAME, result5, RESOURCE_NOT_FOUND)

        #
        # Put entry information (update some fields should succeed)
        #
        sample_01.name = self.sample_01_upd['name']
        sample_01.url = self.sample_01_upd['url']
        sample_01.sample_type_id = self.sample_01_upd['sample_type_id']
        sample_01.proposal_id = self.sample_01_upd['proposal_id']
        sample_01.flg_proposal_system = self.sample_01_upd[
            'flg_proposal_system']
        sample_01.proposal_system_id = self.sample_01_upd['proposal_system_id']
        sample_01.flg_available = self.sample_01_upd['flg_available']
        sample_01.description = self.sample_01_upd['description']
        result6 = sample_01.update()
        self.assert_update_success(MODULE_NAME, result6, self.sample_01_upd)

        #
        # Put entry information (update some fields should throw an error)
        #
        sample_01.name = 'X' * 128  # noqa
        sample_01.flg_available = self.sample_01_upd['flg_available']
        sample_01.description = self.sample_01_upd['description']
        result7 = sample_01.update()
        expect_app_info = {'name': ['is too long (maximum is 127 characters)']}
        self.assert_update_error(MODULE_NAME, result7, expect_app_info)

        #
        # Delete entry (should succeed)
        # (test purposes only to keep the DB clean)
        #
        result8 = sample_01.delete()
        self.assert_delete_success(MODULE_NAME, result8)

        #
        # Delete entry (should throw an error)
        # (test purposes only to keep the DB clean)
        #
        result9 = sample_01.delete()
        self.assert_delete_error(MODULE_NAME, result9, RESOURCE_NOT_FOUND)

        #
        # Get entry by proposal_id
        #
        result10 = Sample.get_all_by_proposal_id(self.mdc_client,
                                                 sample_proposal_id,
                                                 page=DEF_PAGE, page_size=2)

        expected_result = [
            {'id': -1,
             'name': 'TestSample DO NOT DELETE!',
             'flg_proposal_system': '',
             'proposal_system_id': '',
             'flg_available': True,
             'proposal_id': -1,
             'url': 'https://www.google.com',
             'sample_type_id': 1,
             'description': ''}]

        self.assert_find_success(MODULE_NAME, result10, expected_result)

    def test_set_sample_by_name_and_proposal_id(self):
        __unique_name = Generators.generate_unique_name('SampleSet01')
        sample_set_01 = {
            'name': __unique_name,
            'url': 'https://in.xfel.eu/upex/sample/101',
            'sample_type_id': '1',
            'proposal_id': '-1',
            'flg_proposal_system': 'U',
            'proposal_system_id': '456321',
            'flg_available': 'true',
            'description': 'desc 01'
        }

        #
        # Create new entry using set_by_name_and_proposal_id (should succeed)
        #
        result1 = Sample.set_by_name_and_proposal_id(self.mdc_client,
                                                     sample_set_01)
        self.assert_create_success(MODULE_NAME, result1, sample_set_01)

        # sample = result1['data']
        sample_id = result1['data']['id']
        sample_name = result1['data']['name']
        sample_proposal_id = result1['data']['proposal_id']

        #
        # Create new entry using set_by_name_and_proposal_id (should succeed)
        #
        result2 = Sample.set_by_name_and_proposal_id(self.mdc_client,
                                                     sample_set_01)
        self.assert_find_success(MODULE_NAME, result2, sample_set_01)

        #
        # Get entry by name
        #
        result3 = Sample.get_by_name_and_proposal_id(self.mdc_client,
                                                     sample_name,
                                                     sample_proposal_id)
        self.assert_find_success(MODULE_NAME, result3, sample_set_01)

        #
        # Delete entry (should succeed)
        # (test purposes only to keep the DB clean)
        #
        result8 = Sample.delete_by_id(self.mdc_client, sample_id)
        self.assert_delete_success(MODULE_NAME, result8)

        #
        # Delete entry (should throw an error)
        # (test purposes only to keep the DB clean)
        #
        result9 = Sample.delete_by_id(self.mdc_client, sample_id)
        self.assert_delete_error(MODULE_NAME, result9, RESOURCE_NOT_FOUND)

    #
    # fields_validation
    #
    def fields_validation(self, receive, expect):
        self.assert_eq_hfield(receive, expect, 'name', STRING)
        self.assert_eq_hfield(receive, expect, 'url', STRING)
        self.assert_eq_hfield(receive, expect, 'sample_type_id', STRING)
        self.assert_eq_hfield(receive, expect, 'proposal_id', STRING)
        self.assert_eq_hfield(receive, expect, 'flg_proposal_system', STRING)
        self.assert_eq_hfield(receive, expect, 'proposal_system_id', STRING)
        self.assert_eq_hfield(receive, expect, 'flg_available', BOOLEAN)
        self.assert_eq_hfield(receive, expect, 'description', STRING)


if __name__ == '__main__':
    unittest.main()
