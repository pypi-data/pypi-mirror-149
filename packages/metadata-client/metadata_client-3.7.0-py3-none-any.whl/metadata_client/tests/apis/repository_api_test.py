"""RepositoryApiTest class"""

import unittest

from metadata_client import MetadataClient
from .api_base import ApiBase
from ..common.config_test import *
from ..common.generators import Generators
from ..common.secrets import *


class RepositoryApiTest(ApiBase, unittest.TestCase):
    client_api = MetadataClient(
        client_id=CLIENT_OAUTH2_INFO['CLIENT_ID'],
        client_secret=CLIENT_OAUTH2_INFO['CLIENT_SECRET'],
        token_url=CLIENT_OAUTH2_INFO['TOKEN_URL'],
        refresh_url=CLIENT_OAUTH2_INFO['REFRESH_URL'],
        auth_url=CLIENT_OAUTH2_INFO['AUTH_URL'],
        scope=CLIENT_OAUTH2_INFO['SCOPE'],
        user_email=CLIENT_OAUTH2_INFO['EMAIL'],
        base_api_url=BASE_API_URL)

    def test_create_repository_api(self):
        __unique_name = Generators.generate_unique_name('RepositoryApi')
        __unique_identifier = Generators.generate_unique_identifier()
        repository = {
            'repository': {
                'name': __unique_name,
                'identifier': __unique_identifier,
                'img_url': 'https://www.new_example.com/img.png',
                'mount_point': __unique_identifier,
                'transfer_agent_identifier': 'new_special_repo_identifier',
                'transfer_agent_server_url': 'https://www.new_example.com:123',
                'flg_context': 'L',
                'flg_available': 'true',
                'description': 'desc 01'
            }
        }

        expect = repository['repository']

        #
        # Create new entry (should succeed)
        #
        received = self.__create_entry_api(repository, expect)

        repository_id = received['id']
        repository_name = received['name']

        #
        # Create duplicated entry (should throw an error)
        #
        self.__create_error_entry_uk_api(repository)

        #
        # Get entry by name
        #
        self.__get_all_entries_by_name_api(repository_name, expect)

        #
        # Get entry by ID
        #
        self.__get_entry_by_id_api(repository_id, expect)

        #
        # Put entry information (update some fields should succeed)
        #
        self.__update_entry_api(repository_id, expect)

        #
        # Delete entry (should succeed)
        # (test purposes only to keep the DB clean)
        #
        self.__delete_entry_by_id_api(repository_id)

    #
    # fields_validation
    #
    def fields_validation(self, receive, expect):
        self.assert_eq_hfield(receive, expect, 'name', STRING)
        self.assert_eq_hfield(receive, expect, 'identifier', STRING)
        self.assert_eq_hfield(receive, expect, 'mount_point', STRING)
        self.assert_eq_hfield(receive, expect, 'img_url', STRING)
        self.assert_eq_hfield(receive, expect, 'flg_context', STRING)
        self.assert_eq_hfield(receive, expect,
                              'transfer_agent_identifier', STRING),
        self.assert_eq_hfield(receive, expect,
                              'transfer_agent_server_url', STRING),
        self.assert_eq_hfield(receive, expect, 'flg_available', BOOLEAN)
        self.assert_eq_hfield(receive, expect, 'description', STRING)

    #
    # Internal private APIs methods
    #
    def __create_entry_api(self, entry_info, expect):
        response = self.client_api.create_repository_api(entry_info)
        receive = self.get_and_validate_create_entry(response)
        self.fields_validation(receive, expect)
        return receive

    def __create_error_entry_uk_api(self, entry_info):
        response = self.client_api.create_repository_api(entry_info)
        resp_content = self.load_response_content(response)

        receive = resp_content
        expect = {
            'info': {'identifier': ['has already been taken'],
                     'name': ['has already been taken'],
                     'transfer_agent_identifier': ['has already been taken'],
                     'transfer_agent_server_url': ['has already been taken']}}

        self.assertEqual(receive, expect, "Expected result not received")
        self.assert_eq_status_code(response.status_code, UNPROCESSABLE_ENTITY)

        # 'has already been taken'
        receive_msg = receive['info']['name'][0]
        expect_msg = expect['info']['name'][0]
        self.assert_eq_str(receive_msg, expect_msg)

    def __update_entry_api(self, entry_id, expect):
        unique_name_upd = Generators.generate_unique_name('ExpTypeApiUpd')
        unique_id_upd = Generators.generate_unique_identifier(1)
        repository_upd = {
            'repository': {
                'name': unique_name_upd,
                'identifier': unique_id_upd,
                'img_url': 'https://www.upd_example.com/img.png',
                'mount_point': unique_id_upd,
                'transfer_agent_identifier': 'updated_special_repo_identifier',
                'transfer_agent_server_url': 'https://www.upd_example.com:123',
                'flg_context': 'R',
                'flg_available': 'false',
                'description': 'desc 01 updated!!!'
            }
        }

        response = self.client_api.update_repository_api(
            entry_id,
            repository_upd
        )

        resp_content = self.load_response_content(response)

        receive = resp_content
        expect_upd = repository_upd['repository']

        self.fields_validation(receive, expect_upd)
        self.assert_eq_status_code(response.status_code, OK)

        field = 'name'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'identifier'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'img_url'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'mount_point'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'flg_context'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'flg_available'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'description'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)

    def __get_all_entries_by_name_api(self, name, expect):
        response = self.client_api.get_all_repositories_by_name_api(name)
        receive = self.get_and_validate_all_entries_by_name(response)
        self.fields_validation(receive, expect)

    def __get_entry_by_id_api(self, entry_id, expect):
        response = self.client_api.get_repository_by_id_api(entry_id)
        receive = self.get_and_validate_entry_by_id(response)
        self.fields_validation(receive, expect)

    def __delete_entry_by_id_api(self, entry_id):
        response = self.client_api.delete_repository_api(entry_id)
        self.get_and_validate_delete_entry_by_id(response)


if __name__ == '__main__':
    unittest.main()
