"""SampleApiTest class"""

import unittest

from metadata_client import MetadataClient
from .api_base import ApiBase
from ..common.config_test import *
from ..common.generators import Generators
from ..common.secrets import *


class SampleApiTest(ApiBase, unittest.TestCase):
    client_api = MetadataClient(
        client_id=CLIENT_OAUTH2_INFO['CLIENT_ID'],
        client_secret=CLIENT_OAUTH2_INFO['CLIENT_SECRET'],
        token_url=CLIENT_OAUTH2_INFO['TOKEN_URL'],
        refresh_url=CLIENT_OAUTH2_INFO['REFRESH_URL'],
        auth_url=CLIENT_OAUTH2_INFO['AUTH_URL'],
        scope=CLIENT_OAUTH2_INFO['SCOPE'],
        user_email=CLIENT_OAUTH2_INFO['EMAIL'],
        base_api_url=BASE_API_URL)

    def test_create_sample_api(self):
        __unique_name = Generators.generate_unique_name('SampleApi')
        sample = {
            'sample': {
                'name': __unique_name,
                'url': 'https://in.xfel.eu/upex/sample/101',
                'sample_type_id': '1',
                'proposal_id': '-1',
                'flg_proposal_system': 'U',
                'proposal_system_id': '1234567890987654321',
                'flg_available': 'true',
                'description': 'desc 01'
            }
        }

        expect = sample['sample']

        #
        # Create new entry (should succeed)
        #
        received = self.__create_entry_api(sample, expect)

        sample_id = received['id']
        sample_name = received['name']
        sample_proposal_id = received['proposal_id']

        #
        # Create duplicated entry (should throw an error)
        #
        self.__create_error_entry_uk_api(sample)

        #
        # Get entry by name
        #
        self.__get_all_entries_by_name_and_proposal_id_api(sample_name,
                                                           sample_proposal_id,
                                                           expect)

        #
        # Get entry by ID
        #
        self.__get_entry_by_id_api(sample_id, expect)

        #
        # Put entry information (update some fields should succeed)
        #
        self.__update_entry_api(sample_id, expect)

        #
        # Delete entry (should succeed)
        # (test purposes only to keep the DB clean)
        #
        self.__delete_entry_by_id_api(sample_id)

    #
    # fields_validation
    #
    def fields_validation(self, receive, expect):
        self.assert_eq_hfield(receive, expect, 'name', STRING)
        self.assert_eq_hfield(receive, expect, 'url', STRING)
        self.assert_eq_hfield(receive, expect, 'sample_type_id', NUMBER)
        self.assert_eq_hfield(receive, expect, 'proposal_id', NUMBER)
        self.assert_eq_hfield(receive, expect, 'flg_proposal_system', STRING)
        self.assert_eq_hfield(receive, expect, 'proposal_system_id', STRING)
        self.assert_eq_hfield(receive, expect, 'flg_available', BOOLEAN)
        self.assert_eq_hfield(receive, expect, 'description', STRING)

    #
    # Internal private APIs methods
    #
    def __create_entry_api(self, entry_info, expect):
        response = self.client_api.create_sample_api(entry_info)
        receive = self.get_and_validate_create_entry(response)
        self.fields_validation(receive, expect)
        return receive

    def __create_error_entry_uk_api(self, entry_info):
        response = self.client_api.create_sample_api(entry_info)
        resp_content = self.load_response_content(response)

        receive = resp_content
        expect = {'info': {'name': ['has already been taken'],
                           'flg_proposal_system': ['has already been taken'],
                           'proposal_id': ['has already been taken'],
                           'proposal_system_id': ['has already been taken']}}

        self.assertEqual(receive, expect, "Expected result not received")
        self.assert_eq_status_code(response.status_code, UNPROCESSABLE_ENTITY)

        # 'has already been taken'
        receive_msg = receive['info']['name'][0]
        expect_msg = expect['info']['name'][0]
        self.assert_eq_str(receive_msg, expect_msg)

    def __update_entry_api(self, entry_id, expect):
        __unique_name_upd = Generators.generate_unique_name('SampleApiUpd')
        unique_id_upd = Generators.generate_unique_identifier(1)
        sample_upd = {
            'sample': {
                'name': __unique_name_upd,
                'url': 'https://in.xfel.eu/upex/sample/202',
                'sample_type_id': '3',
                'proposal_id': '-1',
                'flg_proposal_system': 'U',
                'proposal_system_id': '12345',
                'flg_available': 'false',
                'description': 'desc 01 updated!!!'
            }
        }

        response = self.client_api.update_sample_api(entry_id, sample_upd)

        resp_content = self.load_response_content(response)

        receive = resp_content
        expect_upd = sample_upd['sample']

        self.fields_validation(receive, expect_upd)
        self.assert_eq_status_code(response.status_code, OK)

        field = 'name'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'url'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'sample_type_id'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'proposal_id'
        self.assert_eq_str(expect[field], expect_upd[field])
        field = 'flg_proposal_system'
        self.assert_eq_str(expect[field], expect_upd[field])
        field = 'proposal_system_id'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'flg_available'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'description'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)

    def __get_all_entries_by_name_and_proposal_id_api(self,
                                                      name, proposal_id,
                                                      expect,
                                                      page=DEF_PAGE,
                                                      page_size=DEF_PAGE_SIZE):
        response = self.client_api.get_all_samples_by_name_and_proposal_id_api(
            name, proposal_id, page, page_size)
        receive = self.get_and_validate_all_entries_by_name(response)
        self.fields_validation(receive, expect)

    def __get_entry_by_id_api(self, entry_id, expect):
        response = self.client_api.get_sample_by_id_api(entry_id)
        receive = self.get_and_validate_entry_by_id(response)
        self.fields_validation(receive, expect)

    def __delete_entry_by_id_api(self, entry_id):
        response = self.client_api.delete_sample_api(entry_id)
        self.get_and_validate_delete_entry_by_id(response)


if __name__ == '__main__':
    unittest.main()
