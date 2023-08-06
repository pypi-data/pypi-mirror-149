"""DataFileTest class"""

import unittest

from metadata_client.metadata_client import MetadataClient
from .module_base import ModuleBase
from ..common.config_test import *
from ..common.generators import Generators
from ..common.secrets import *
from ...modules.data_file import DataFile

MODULE_NAME = DATA_FILE


class DataFileTest(ModuleBase, unittest.TestCase):
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

        self.data_file_01 = {
            'data_group_id': '-2',
            'files': "[{'filename': 'obj_01.h5', 'relative_path': ''}]"
        }

        __unique_name_upd = Generators.generate_unique_name('DataGrpTypeUpd1')
        __unique_identifier_upd = Generators.generate_unique_identifier(1)
        self.data_file_01_upd = {
            'data_group_id': '-2',
            'files': "[{'filename': 'obj_01_UPDATED.h5', 'relative_path': ''}]"
        }

    def test_create_data_file(self):
        data_file_01 = DataFile(
            metadata_client=self.mdc_client,
            data_group_id=self.data_file_01['data_group_id'],
            files=self.data_file_01['files'])

        #
        # Create new entry (should succeed)
        #
        result1 = data_file_01.create()
        self.assert_create_success(MODULE_NAME, result1, self.data_file_01)

        data_file = result1['data']
        data_file_id = result1['data']['id']
        data_file_data_group_id = result1['data']['data_group_id']

        #
        # Get entry by data_group_id
        #
        result3 = DataFile.get_all_by_data_group_id(self.mdc_client,
                                                    data_file_data_group_id,
                                                    page=DEF_PAGE,
                                                    page_size=DEF_PAGE_SIZE)

        expected_result = [self.data_file_01]
        self.assert_find_success(MODULE_NAME, result3, expected_result)

        #
        # Get entry by ID
        #
        result4 = DataFile.get_by_id(self.mdc_client, data_file_id)
        self.assert_find_success(MODULE_NAME, result4, self.data_file_01)

        #
        # Get entry with non-existent ID (should throw an error)
        #
        result5 = DataFile.get_by_id(self.mdc_client, -666)
        self.assert_find_error(MODULE_NAME, result5, RESOURCE_NOT_FOUND)

        #
        # Put entry information (update some fields should succeed)
        #
        data_file_01.data_group_id = self.data_file_01_upd['data_group_id']
        data_file_01.files = self.data_file_01_upd['files']
        result6 = data_file_01.update()
        self.assert_update_success(MODULE_NAME, result6, self.data_file_01_upd)

        #
        # Put entry information (update some fields should throw an error)
        #
        data_file_01.data_group_id = self.data_file_01_upd['data_group_id']
        data_file_01.files = ''
        result7 = data_file_01.update()
        expect_app_info = {
            'files': ["can't be blank",
                      'is too short (minimum is 40 characters)']}
        self.assert_update_error(MODULE_NAME, result7, expect_app_info)

        #
        # Delete entry (should succeed)
        # (test purposes only to keep the DB clean)
        #
        result8 = data_file_01.delete()
        self.assert_delete_success(MODULE_NAME, result8)

        #
        # Delete entry (should throw an error)
        # (test purposes only to keep the DB clean)
        #
        result9 = data_file_01.delete()
        self.assert_delete_error(MODULE_NAME, result9, RESOURCE_NOT_FOUND)

    def test_create_data_file_from_dict(self):
        #
        # Create new entry (should succeed)
        #
        result1 = DataFile.create_from_dict(self.mdc_client, self.data_file_01)
        self.assert_create_success(MODULE_NAME, result1, self.data_file_01)

        data_file = result1['data']
        data_file_id = data_file['id']

        #
        # Update entry (should succeed)
        #
        result3 = DataFile.update_from_dict(self.mdc_client,
                                            data_file_id,
                                            self.data_file_01_upd)
        self.assert_update_success(MODULE_NAME, result3, self.data_file_01_upd)

        #
        # Incomplete (non mandatory) update entry (should succeed)
        #
        data_file_02_upd = {
            'files': "[{'filename': 'obj_02_UPDATED.h5', 'relative_path': ''}]"
        }

        result4 = DataFile.update_from_dict(self.mdc_client,
                                            data_file_id,
                                            data_file_02_upd)

        exp_data_file_02_upd = {
            'data_group_id': self.data_file_01_upd['data_group_id'],
            'files': "[{'filename': 'obj_02_UPDATED.h5', 'relative_path': ''}]"
        }

        self.assert_update_success(MODULE_NAME, result4, exp_data_file_02_upd)

        #
        # Delete entry (should succeed)
        # (test purposes only to keep the DB clean)
        #
        result8 = DataFile.delete_by_id(self.mdc_client, data_file_id)
        self.assert_delete_success(MODULE_NAME, result8)

        #
        # Delete entry (should throw an error)
        # (test purposes only to keep the DB clean)
        #
        result9 = DataFile.delete_by_id(self.mdc_client, data_file_id)
        self.assert_delete_error(MODULE_NAME, result9, RESOURCE_NOT_FOUND)

    #
    # fields_validation
    #
    def fields_validation(self, receive, expect):
        self.assert_eq_hfield(receive, expect, 'data_group_id', NUMBER)
        self.assert_eq_hfield(receive, expect, 'files', STRING)


if __name__ == '__main__':
    unittest.main()
