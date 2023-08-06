"""ParameterApiTest class"""

import unittest

from metadata_client import MetadataClient
from .api_base import ApiBase
from ..common.config_test import *
from ..common.secrets import *


class ParameterApiTest(ApiBase, unittest.TestCase):
    client_api = MetadataClient(
        client_id=CLIENT_OAUTH2_INFO['CLIENT_ID'],
        client_secret=CLIENT_OAUTH2_INFO['CLIENT_SECRET'],
        token_url=CLIENT_OAUTH2_INFO['TOKEN_URL'],
        refresh_url=CLIENT_OAUTH2_INFO['REFRESH_URL'],
        auth_url=CLIENT_OAUTH2_INFO['AUTH_URL'],
        scope=CLIENT_OAUTH2_INFO['SCOPE'],
        user_email=CLIENT_OAUTH2_INFO['EMAIL'],
        base_api_url=BASE_API_URL)

    def test_create_parameter_api(self):
        parameter = {
            'parameter': {
                'data_source': 'MID/XTD6/ATT/MOTOR/BLADE_TOP',
                'name': 'VelocityLeft',
                'value': '15.6',
                'minimum': '15.0',
                'maximum': '16.0',
                'mean': '15.5',
                'standard_deviation': '0.5',
                'data_type_id': '30',
                'parameter_type_id': '1',
                'unit_id': '1',
                'unit_prefix': '',
                'flg_available': 'true',
                'description': 'desc 01'
            }
        }

        expect = parameter['parameter']

        #
        # Create new entry (should succeed)
        #
        received = self.__create_entry_api(parameter, expect)

        parameter_id = received['id']
        data_source = received['data_source']
        param_name = received['name']

        #
        # Get entry by name
        #
        self.__get_all_entries_by_data_source_and_name_api(data_source,
                                                           param_name, expect)

        #
        # Get entry by ID
        #
        self.__get_entry_by_id_api(parameter_id, expect)

        #
        # Put entry information (update some fields should succeed)
        #
        self.__update_entry_api(parameter_id, expect)

        #
        # Delete entry (should succeed)
        # (test purposes only to keep the DB clean)
        #
        self.__delete_entry_by_id_api(parameter_id)

    #
    # fields_validation
    #
    def fields_validation(self, receive, expect):
        self.assert_eq_hfield(receive, expect, 'data_source', STRING)
        self.assert_eq_hfield(receive, expect, 'name', STRING)
        self.assert_eq_hfield(receive, expect, 'value', STRING)
        self.assert_eq_hfield(receive, expect, 'minimum', STRING)
        self.assert_eq_hfield(receive, expect, 'maximum', STRING)
        self.assert_eq_hfield(receive, expect, 'mean', STRING)
        self.assert_eq_hfield(receive, expect, 'standard_deviation', STRING)
        self.assert_eq_hfield(receive, expect, 'data_type_id', NUMBER)
        self.assert_eq_hfield(receive, expect, 'parameter_type_id', NUMBER)
        self.assert_eq_hfield(receive, expect, 'unit_id', NUMBER)
        self.assert_eq_hfield(receive, expect, 'unit_prefix', STRING)
        self.assert_eq_hfield(receive, expect, 'flg_available', BOOLEAN)
        self.assert_eq_hfield(receive, expect, 'description', STRING)

    #
    # Internal private APIs methods
    #
    def __create_entry_api(self, entry_info, expect):
        response = self.client_api.create_parameter_api(entry_info)
        receive = self.get_and_validate_create_entry(response)
        self.fields_validation(receive, expect)
        return receive

    def __update_entry_api(self, entry_id, expect):
        parameter_upd = {
            'parameter': {
                'data_source': 'MID/XTD6/ATT/MOTOR/BLADE_DOWN',
                'name': 'VelocityRight',
                'value': '13.6',
                'minimum': '13.0',
                'maximum': '14.0',
                'mean': '13.5',
                'standard_deviation': '0.51',
                'data_type_id': '31',
                'parameter_type_id': '1',
                'unit_id': '1',
                'unit_prefix': 'Kilo',
                'flg_available': 'false',
                'description': 'desc 01 updated!!!'
            }
        }

        response = self.client_api.update_parameter_api(entry_id,
                                                        parameter_upd)

        resp_content = self.load_response_content(response)

        receive = resp_content
        expect_upd = parameter_upd['parameter']

        self.fields_validation(receive, expect_upd)
        self.assert_eq_status_code(response.status_code, OK)

        field = 'data_source'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'name'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'value'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'minimum'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'maximum'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'mean'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'standard_deviation'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'data_type_id'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'parameter_type_id'
        self.assert_eq_str(expect[field], expect_upd[field])
        field = 'unit_id'
        self.assert_eq_str(expect[field], expect_upd[field])
        field = 'unit_prefix'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'flg_available'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'description'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)

    def __get_all_entries_by_data_source_and_name_api(self,
                                                      data_source,
                                                      name,
                                                      expect):
        resp = self.client_api.get_all_parameters_by_data_source_and_name_api(
            data_source, name)
        receive = self.get_and_validate_all_entries_by_name(resp)
        self.fields_validation(receive, expect)

    def __get_entry_by_id_api(self, entry_id, expect):
        response = self.client_api.get_parameter_by_id_api(entry_id)
        receive = self.get_and_validate_entry_by_id(response)
        self.fields_validation(receive, expect)

    def __delete_entry_by_id_api(self, entry_id):
        response = self.client_api.delete_parameter_api(entry_id)
        self.get_and_validate_delete_entry_by_id(response)


if __name__ == '__main__':
    unittest.main()
