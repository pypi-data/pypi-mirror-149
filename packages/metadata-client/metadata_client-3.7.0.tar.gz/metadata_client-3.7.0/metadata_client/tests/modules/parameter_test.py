"""ParameterTest class"""

import copy
import unittest

from metadata_client.metadata_client import MetadataClient
from .module_base import ModuleBase
from ..common.config_test import *
from ..common.secrets import *
from ...modules.parameter import Parameter

MODULE_NAME = PARAMETER


class ParameterTest(ModuleBase, unittest.TestCase):
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

        self.param_01 = {
            'data_source': 'MID/XTD6/ATT/MOTOR/BLADE_TOP',
            'name': 'VelocityLeft',
            'value': '15.6',
            'minimum': '15.0',
            'maximum': '16.0',
            'mean': '15.5',
            'standard_deviation': '0.5',
            'data_type_id': '70',
            'parameter_type_id': '1',
            'unit_id': '1',
            'unit_prefix': '',
            'flg_available': 'false',
            'description': 'desc 01',
            'data_groups_parameters_attributes': None
        }

        self.param_01_upd = {
            'data_source': 'MID/XTD6/ATT/MOTOR/BLADE_TOP',
            'name': 'VelocityLeft',
            'value': '13.6',
            'minimum': '13.0',
            'maximum': '14.0',
            'mean': '13.5',
            'standard_deviation': '0.51',
            'data_type_id': '70',
            'parameter_type_id': '1',
            'unit_id': '1',
            'unit_prefix': 'Kilo',
            'flg_available': 'false',
            'description': 'desc 01 updated!!!',
            'data_groups_parameters_attributes': None  # Optional field
        }

    def test_create_parameter(self):
        param_01 = Parameter(
            metadata_client=self.mdc_client,
            data_source=self.param_01['data_source'],
            name=self.param_01['name'],
            value=self.param_01['value'],
            minimum=self.param_01['minimum'],
            maximum=self.param_01['maximum'],
            mean=self.param_01['mean'],
            standard_deviation=self.param_01['standard_deviation'],
            data_type_id=self.param_01['data_type_id'],
            parameter_type_id=self.param_01['parameter_type_id'],
            unit_id=self.param_01['unit_id'],
            unit_prefix=self.param_01['unit_prefix'],
            flg_available=self.param_01['flg_available'],
            description=self.param_01['description'],
            data_groups_parameters_attributes=None  # Optional field
        )

        #
        # Create new entry (should succeed)
        #
        result1 = param_01.create()
        self.assert_create_success(MODULE_NAME, result1, self.param_01)

        parameter_id = result1['data']['id']
        data_source = result1['data']['data_source']
        param_name = result1['data']['name']

        #
        # Create duplicated entry (should NOT throw an error)
        #
        param_01_dup = copy.copy(param_01)
        result2 = param_01_dup.create()
        self.assert_create_success(MODULE_NAME, result2, self.param_01)

        #
        # Get all by name
        #
        result3 = Parameter.get_all_by_data_source_and_name(
            self.mdc_client, data_source, param_name,
            page=DEF_PAGE, page_size=DEF_PAGE_SIZE)

        # The result should be double because the same Parameter was
        # successfully created twice
        exp_data = [self.param_01, self.param_01]
        self.assert_find_success(MODULE_NAME, result3, exp_data)

        #
        # Get all by experiment_id
        #
        # result31 = Parameter.get_all_by_experiment_id(self.mdc_client,
        #                                               param_exp_id)
        #
        # Note that position 0 of the List is already present in the
        # Application seeds file as an example
        # self.fields_validation(result31['data'][1], self.param_01)
        # self.fields_validation(result31['data'][2], self.param_01)

        #
        # Get entry by ID
        #
        result4 = Parameter.get_by_id(self.mdc_client, parameter_id)
        self.assert_find_success(MODULE_NAME, result4, self.param_01)

        #
        # Get entry with non-existent ID (should throw an error)
        #
        result5 = Parameter.get_by_id(self.mdc_client, -666)
        self.assert_find_error(MODULE_NAME, result5, RESOURCE_NOT_FOUND)

        #
        # Put entry information (update some fields should succeed)
        #
        param_01.data_source = self.param_01_upd['data_source']
        param_01.name = self.param_01_upd['name']
        param_01.value = self.param_01_upd['value']
        param_01.minimum = self.param_01_upd['minimum']
        param_01.maximum = self.param_01_upd['maximum']
        param_01.mean = self.param_01_upd['mean']
        param_01.standard_deviation = self.param_01_upd['standard_deviation']
        param_01.data_type_id = self.param_01_upd['data_type_id']
        param_01.parameter_type_id = self.param_01_upd['parameter_type_id']
        param_01.unit_id = self.param_01_upd['unit_id']
        param_01.unit_prefix = self.param_01_upd['unit_prefix']
        param_01.flg_available = self.param_01_upd['flg_available']
        param_01.description = self.param_01_upd['description']
        result6 = param_01.update()
        self.assert_update_success(MODULE_NAME, result6, self.param_01_upd)

        #
        # Put entry information (update some fields should throw an error)
        #
        tmp_name = '______THIS__NAME__IS__50__CHARACTERS__LONGER______'
        tmp_name_incorrect = tmp_name * 6
        param_01.name = tmp_name_incorrect
        param_01.flg_available = self.param_01_upd['flg_available']
        param_01.description = self.param_01_upd['description']
        result7 = param_01.update()
        expect_app_info = {'name': ['is too long (maximum is 255 characters)']}

        self.assert_update_error(MODULE_NAME, result7, expect_app_info)

        #
        # Delete entry (should succeed)
        # (test purposes only to keep the DB clean)
        #
        result8 = param_01.delete()
        self.assert_delete_success(MODULE_NAME, result8)

        result8_2 = param_01_dup.delete()
        self.assert_delete_success(MODULE_NAME, result8_2)

        #
        # Delete entry (should throw an error)
        # (test purposes only to keep the DB clean)
        #
        result9 = param_01.delete()
        self.assert_delete_error(MODULE_NAME, result9, RESOURCE_NOT_FOUND)

    def test_create_multiple_parameter_from_dict(self):
        param_data_group_id = -1

        parameter_01 = self.param_01
        parameter_01['name'] = 'multiple_velocityDown'

        parameter_02 = self.param_01_upd
        parameter_02['name'] = 'multiple_velocityUp'

        parameters_list = {'parameters': [parameter_01,
                                          parameter_02]}
        #
        # Create new entry (should succeed)
        #
        result1 = Parameter.create_multiple_from_dict(self.mdc_client,
                                                      parameters_list)

        self.assert_create_success(MODULE_NAME, result1,
                                   parameters_list['parameters'])

        parameters = result1['data']

        for index, parameter_dict in enumerate(parameters):
            parameter_id = parameter_dict['id']

            #
            # Delete entry (should succeed)
            # (test purposes only to keep the DB clean)
            #
            result8 = Parameter.delete_by_id(self.mdc_client, parameter_id)
            self.assert_delete_success(MODULE_NAME, result8)

            #
            # Delete entry (should throw an error)
            # (test purposes only to keep the DB clean)
            #
            result9 = Parameter.delete_by_id(self.mdc_client, parameter_id)
            self.assert_delete_error(MODULE_NAME, result9, RESOURCE_NOT_FOUND)

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


if __name__ == '__main__':
    unittest.main()
