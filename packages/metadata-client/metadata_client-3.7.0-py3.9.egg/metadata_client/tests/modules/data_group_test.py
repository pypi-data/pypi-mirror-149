"""DataGroupTest class"""

import copy
import unittest

from metadata_client.metadata_client import MetadataClient
from .module_base import ModuleBase
from ..common.config_test import *
from ..common.generators import Generators
from ..common.secrets import *
from ...modules.data_group import DataGroup

MODULE_NAME = DATA_GROUP


class DataGroupTest(ModuleBase, unittest.TestCase):
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

        __unique_name = Generators.generate_unique_name('DataGroup01')
        __prefix_path = '/webstorage/XFEL/raw/SPB/2016_01/p0008/e0001/'
        self.data_grp_01 = {
            'name': __unique_name,
            'language': 'en',
            'data_group_type_id': '1',
            'experiment_id': '-1',
            'user_id': '-1',
            'prefix_path': __prefix_path,
            'flg_available': 'true',
            'flg_writing': 'false',
            'flg_public': 'false',
            'format': 'this is a format!',
            'data_passport': 'this is a data passport!',
            'removed_at': '2099-05-25T08:30:00.000+02:00',
            'description': 'desc 01',
            'runs_data_groups_attributes': None
        }

        __unique_name_upd = Generators.generate_unique_name('DataGroupUpd1')
        self.data_grp_01_upd = {
            'name': __unique_name,  # This field cannot be updated
            'language': 'pt',
            'doi': 'It is not possible to updated doi!',
            'data_group_type_id': '1',  # This field cannot be updated
            'experiment_id': '-1',
            'user_id': '-1',
            'prefix_path': __prefix_path,  # This field cannot be updated
            'flg_available': 'false',
            'flg_writing': 'true',
            'flg_public': 'true',
            'format': 'this is an updated format!',
            'data_passport': 'this is an updated data passport!',
            'removed_at': '2100-05-25T08:30:00.000+02:00',
            'description': 'desc 01 updated!!!'
            # , 'runs_data_groups_attributes': None  # Optional field
        }

    def test_create_data_group(self):
        data_grp_01 = DataGroup(
            metadata_client=self.mdc_client,
            name=self.data_grp_01['name'],
            language=self.data_grp_01['language'],
            data_group_type_id=self.data_grp_01['data_group_type_id'],
            experiment_id=self.data_grp_01['experiment_id'],
            user_id=self.data_grp_01['user_id'],
            prefix_path=self.data_grp_01['prefix_path'],
            flg_available=self.data_grp_01['flg_available'],
            flg_writing=self.data_grp_01['flg_writing'],
            flg_public=self.data_grp_01['flg_public'],
            format=self.data_grp_01['format'],
            data_passport=self.data_grp_01['data_passport'],
            removed_at=self.data_grp_01['removed_at'],
            description=self.data_grp_01['description']
            # , runs_data_groups_attributes=None  # Optional field
        )

        #
        # Create new entry (should succeed)
        #
        result1 = data_grp_01.create()
        self.assert_create_success(MODULE_NAME, result1, self.data_grp_01)

        data_group_id = result1['data']['id']
        data_group_name = result1['data']['name']
        data_group_exp_id = result1['data']['experiment_id']
        data_grp_01.doi = result1['data']['doi']

        #
        # Create duplicated entry (should NOT throw an error)
        #
        data_grp_01_dup = copy.copy(data_grp_01)
        result2 = data_grp_01_dup.create()
        self.assert_create_success(MODULE_NAME, result2, data_grp_01_dup)

        #
        # Get all by name
        #
        result3 = DataGroup.get_all_by_name(self.mdc_client,
                                            data_group_name,
                                            page=DEF_PAGE,
                                            page_size=DEF_PAGE_SIZE)

        # The result should be double because the same DataGroup was
        # successfully created twice
        exp_data = [self.data_grp_01, self.data_grp_01]
        self.assert_find_success(MODULE_NAME, result3, exp_data)

        #
        # Get all by experiment_id
        #
        result31 = DataGroup.get_all_by_experiment_id(self.mdc_client,
                                                      data_group_exp_id,
                                                      page=DEF_PAGE,
                                                      page_size=DEF_PAGE_SIZE)

        # Note that position 0 of the List is already present in the
        # Application seeds file as an example
        self.fields_validation(result31['data'][1], self.data_grp_01)
        self.fields_validation(result31['data'][2], self.data_grp_01)

        #
        # Get entry by ID
        #
        result4 = DataGroup.get_by_id(self.mdc_client, data_group_id)
        self.assert_find_success(MODULE_NAME, result4, self.data_grp_01)

        #
        # Get entry with non-existent ID (should throw an error)
        #
        result5 = DataGroup.get_by_id(self.mdc_client, -666)
        self.assert_find_error(MODULE_NAME, result5, RESOURCE_NOT_FOUND)

        #
        # Put entry information (update some fields should succeed)
        #
        data_grp_01.name = self.data_grp_01_upd['name']
        data_grp_01.language = self.data_grp_01_upd['language']
        data_grp_01.doi = self.data_grp_01_upd['doi']
        data_grp_01.data_group_type_id = \
            self.data_grp_01_upd['data_group_type_id']
        data_grp_01.experiment_id = self.data_grp_01_upd['experiment_id']
        data_grp_01.user_id = self.data_grp_01_upd['user_id']
        data_grp_01.prefix_path = self.data_grp_01_upd['prefix_path']
        data_grp_01.flg_available = self.data_grp_01_upd['flg_available']
        data_grp_01.flg_writing = self.data_grp_01_upd['flg_writing']
        data_grp_01.flg_public = self.data_grp_01_upd['flg_public']
        data_grp_01.format = self.data_grp_01_upd['format']
        data_grp_01.data_passport = self.data_grp_01_upd['data_passport']
        data_grp_01.removed_at = self.data_grp_01_upd['removed_at']
        data_grp_01.description = self.data_grp_01_upd['description']
        result6 = data_grp_01.update()
        self.assert_update_success(MODULE_NAME, result6, self.data_grp_01_upd)

        #
        # Put entry information (update some fields should throw an error)
        #
        data_grp_01.name = '__THIS_NAME_IS_1_CHARACTERS_LONGER_THAN_THE_ALLOWED_MAX_NUM__'  # noqa
        data_grp_01.flg_available = self.data_grp_01_upd['flg_available']
        data_grp_01.description = self.data_grp_01_upd['description']
        result7 = data_grp_01.update()
        expect_app_info = {'name': ['cannot be updated',
                                    'is too long (maximum is 60 characters)']}
        self.assert_update_error(MODULE_NAME, result7, expect_app_info)

        #
        # Delete entry (should succeed)
        # (test purposes only to keep the DB clean)
        #
        result8 = data_grp_01.delete()
        self.assert_delete_success(MODULE_NAME, result8)

        result8_2 = data_grp_01_dup.delete()
        self.assert_delete_success(MODULE_NAME, result8_2)

        #
        # Delete entry (should throw an error)
        # (test purposes only to keep the DB clean)
        #
        result9 = data_grp_01.delete()
        self.assert_delete_error(MODULE_NAME, result9, RESOURCE_NOT_FOUND)

    def test_create_data_group_from_dict(self):
        #
        # Create new entry (should succeed)
        #
        result1 = DataGroup.create_from_dict(self.mdc_client, self.data_grp_01)
        self.assert_create_success(MODULE_NAME, result1, self.data_grp_01)

        data_group = result1['data']
        data_group_id = data_group['id']

        #
        # Update entry (should succeed)
        #
        result3 = DataGroup.update_from_dict(self.mdc_client,
                                             data_group_id,
                                             self.data_grp_01_upd)
        self.assert_update_success(MODULE_NAME, result3, self.data_grp_01_upd)

        #
        # Incomplete (non mandatory) update entry (should succeed)
        #
        data_grp_02_upd = {
            'language': 'es',
            'format': 'update test to format...',
            'flg_available': 'true'
        }

        result4 = DataGroup.update_from_dict(self.mdc_client,
                                             data_group_id,
                                             data_grp_02_upd)

        exp_data_grp_02_upd = {
            'name': self.data_grp_01_upd['name'],
            'language': 'es',
            'doi': self.data_grp_01_upd['doi'],
            'data_group_type_id': self.data_grp_01_upd['data_group_type_id'],
            'experiment_id': self.data_grp_01_upd['experiment_id'],
            'user_id': self.data_grp_01_upd['user_id'],
            'prefix_path': self.data_grp_01_upd['prefix_path'],
            'flg_available': 'true',
            'flg_writing': self.data_grp_01_upd['flg_writing'],
            'flg_public': self.data_grp_01_upd['flg_public'],
            'format': 'update test to format...',
            'data_passport': self.data_grp_01_upd['data_passport'],
            'removed_at': self.data_grp_01_upd['removed_at'],
            'description': self.data_grp_01_upd['description']
        }

        self.assert_update_success(MODULE_NAME, result4, exp_data_grp_02_upd)

        #
        # Delete entry (should succeed)
        # (test purposes only to keep the DB clean)
        #
        result8 = DataGroup.delete_by_id(self.mdc_client, data_group_id)
        self.assert_delete_success(MODULE_NAME, result8)

        #
        # Delete entry (should throw an error)
        # (test purposes only to keep the DB clean)
        #
        result9 = DataGroup.delete_by_id(self.mdc_client, data_group_id)
        self.assert_delete_error(MODULE_NAME, result9, RESOURCE_NOT_FOUND)

    #
    # fields_validation
    #
    def fields_validation(self, receive, expect):
        self.assert_eq_hfield(receive, expect, 'name', STRING)
        self.assert_eq_hfield(receive, expect, 'language', STRING)
        self.assert_eq_hfield(receive, expect, 'data_group_type_id', NUMBER)
        self.assert_eq_hfield(receive, expect, 'experiment_id', NUMBER)
        self.assert_eq_hfield(receive, expect, 'user_id', NUMBER)
        self.assert_eq_hfield(receive, expect, 'prefix_path', STRING)
        self.assert_eq_hfield(receive, expect, 'flg_available', BOOLEAN)
        self.assert_eq_hfield(receive, expect, 'flg_writing', BOOLEAN)
        self.assert_eq_hfield(receive, expect, 'flg_public', BOOLEAN)
        self.assert_eq_hfield(receive, expect, 'format', STRING)
        self.assert_eq_hfield(receive, expect, 'data_passport', STRING)
        self.assert_eq_hfield(receive, expect, 'removed_at', DATETIME)
        self.assert_eq_hfield(receive, expect, 'description', STRING)

        #
        # Validate "generated" fields
        expected_doi = {'doi': 'xfel.mdc.dg.{0}'.format(receive['id'])}
        self.assert_eq_hfield(receive, expected_doi, 'doi', STRING)


if __name__ == '__main__':
    unittest.main()
