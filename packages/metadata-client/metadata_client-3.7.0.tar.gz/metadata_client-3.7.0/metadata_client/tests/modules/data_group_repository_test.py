"""DataGroupRepositoryTest class"""

import unittest

from metadata_client.metadata_client import MetadataClient
from .module_base import ModuleBase
from ..common.config_test import *
from ..common.secrets import *
from ...modules.data_group_repository import DataGroupRepository

MODULE_NAME = DATA_GROUP_REPOSITORY


class DataGroupRepositoryTest(ModuleBase, unittest.TestCase):
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

        self.data_grp_repo_00 = {
            'data_group_id': '-1',
            'repository_id': '-1',
            'flg_available': 'true'
        }

        self.data_grp_repo_01 = {
            'data_group_id': '-1',
            'repository_id': '11',
            'flg_available': 'true'
        }

        self.data_grp_repo_01_upd = {
            'data_group_id': '-1',
            'repository_id': '11',
            'flg_available': 'false'
        }

    def test_create_data_group_repository(self):
        dgrp_repo_01 = DataGroupRepository(
            metadata_client=self.mdc_client,
            data_group_id=self.data_grp_repo_01['data_group_id'],
            repository_id=self.data_grp_repo_01['repository_id'],
            flg_available=self.data_grp_repo_01['flg_available'])

        #
        # Create new entry (should succeed)
        #
        result1 = dgrp_repo_01.create()
        self.assert_create_success(MODULE_NAME, result1, self.data_grp_repo_01)

        data_group_repository = result1['data']
        data_group_repository_id = result1['data']['id']
        data_group_id = result1['data']['data_group_id']
        repository_id = result1['data']['repository_id']

        #
        # Create duplicated entry (should throw an error)
        #
        data_group_repo_01_dup = dgrp_repo_01
        result2 = data_group_repo_01_dup.create()
        expect_app_info = {'data_group_id': ['has already been taken'],
                           'repository_id': ['has already been taken']}
        self.assert_create_error(MODULE_NAME, result2, expect_app_info)

        #
        # Get entry by data_group_id
        #
        result3 = DataGroupRepository.get_all_by_data_group_id(
            self.mdc_client, data_group_id,
            page=DEF_PAGE, page_size=DEF_PAGE_SIZE)

        expected = [self.data_grp_repo_00, self.data_grp_repo_01]
        self.assert_find_success(MODULE_NAME, result3, expected)

        #
        # Get entry by data_group_id and repository_id
        #
        result4 = DataGroupRepository. \
            get_all_by_data_group_id_and_repository_id(self.mdc_client,
                                                       data_group_id,
                                                       repository_id,
                                                       page=DEF_PAGE,
                                                       page_size=DEF_PAGE_SIZE)
        self.assert_find_success(MODULE_NAME, result4, [self.data_grp_repo_01])

        #
        # Get entry by ID
        #
        result5 = DataGroupRepository.get_by_id(self.mdc_client,
                                                data_group_repository_id)
        self.assert_find_success(MODULE_NAME, result5, self.data_grp_repo_01)

        #
        # Get entry with non-existent ID (should throw an error)
        #
        result6 = DataGroupRepository.get_by_id(self.mdc_client, -666)
        self.assert_find_error(MODULE_NAME, result6, RESOURCE_NOT_FOUND)

        #
        # Put entry information (update some fields should succeed)
        #
        dgrp_repo_01.data_group_id = self.data_grp_repo_01_upd['data_group_id']
        dgrp_repo_01.repository_id = self.data_grp_repo_01_upd['repository_id']
        dgrp_repo_01.flg_available = self.data_grp_repo_01_upd['flg_available']
        result7 = dgrp_repo_01.update()
        self.assert_update_success(MODULE_NAME, result7,
                                   self.data_grp_repo_01_upd)

        #
        # Delete entry (should succeed)
        # (test purposes only to keep the DB clean)
        #
        result8 = dgrp_repo_01.delete()
        self.assert_delete_success(MODULE_NAME, result8)

        #
        # Delete entry (should throw an error)
        # (test purposes only to keep the DB clean)
        #
        result9 = dgrp_repo_01.delete()
        self.assert_delete_error(MODULE_NAME, result9, RESOURCE_NOT_FOUND)

    #
    # fields_validation
    #
    def fields_validation(self, receive, expect):
        self.assert_eq_hfield(receive, expect, 'data_group_id', NUMBER)
        self.assert_eq_hfield(receive, expect, 'repository_id', NUMBER)
        self.assert_eq_hfield(receive, expect, 'flg_available', BOOLEAN)


if __name__ == '__main__':
    unittest.main()
