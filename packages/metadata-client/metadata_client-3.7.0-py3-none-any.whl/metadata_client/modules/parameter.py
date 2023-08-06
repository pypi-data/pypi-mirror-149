"""Parameter module class"""

import inspect

from ..common.base import Base
from ..common.config import *

MODULE_NAME = PARAMETER


class Parameter:
    def __init__(self, metadata_client,
                 data_source, name, value,
                 minimum, maximum, mean, standard_deviation,
                 data_type_id, parameter_type_id, unit_id,
                 unit_prefix, flg_available, description='',
                 data_groups_parameters_attributes=None):
        self.metadata_client = metadata_client
        self.id = None
        self.data_source = data_source
        self.name = name
        self.value = value
        self.minimum = minimum
        self.maximum = maximum
        self.mean = mean
        self.standard_deviation = standard_deviation
        self.data_type_id = data_type_id
        self.parameter_type_id = parameter_type_id
        self.unit_id = unit_id
        self.unit_prefix = unit_prefix
        self.flg_available = flg_available
        self.description = description
        self.data_groups_parameters_attributes = \
            data_groups_parameters_attributes

    def create(self):
        mdc_client = self.metadata_client
        response = mdc_client.create_parameter_api(self.__get_resource())

        Base.cal_debug(MODULE_NAME, CREATE, response)
        res = Base.format_response(response, CREATE, CREATED, MODULE_NAME)

        if res['success']:
            self.id = res['data']['id']

        return res

    def delete(self):
        mdc_client = self.metadata_client
        response = mdc_client.delete_parameter_api(self.id)
        Base.cal_debug(MODULE_NAME, DELETE, response)

        return Base.format_response(response, DELETE, NO_CONTENT, MODULE_NAME)

    def update(self):
        mdc_client = self.metadata_client
        response = mdc_client.update_parameter_api(self.id,
                                                   self.__get_resource())

        Base.cal_debug(MODULE_NAME, UPDATE, response)
        return Base.format_response(response, UPDATE, OK, MODULE_NAME)

    # @staticmethod
    # def create_from_dict(mdc_client, parameter):
    #     new_parameter = Parameter(
    #         metadata_client=mdc_client,
    #         data_source=parameter['data_source'],
    #         name=parameter['name'],
    #         value=parameter['value'],
    #         minimum=parameter['minimum'],
    #         maximum=parameter['maximum'],
    #         mean=parameter['mean'],
    #         standard_deviation=parameter['standard_deviation'],
    #         data_type_id=parameter['data_type_id'],
    #         parameter_type_id=parameter['parameter_type_id'],
    #         unit_id=parameter['unit_id'],
    #         unit_prefix=parameter['unit_prefix'],
    #         flg_available=parameter['flg_available'],
    #         description=parameter['description'],
    #         data_groups_parameters_attributes=parameter[
    #             'data_groups_parameters_attributes'])
    #
    #     resp = new_parameter.create()
    #     return resp

    @staticmethod
    def create_multiple_from_dict(mdc_client, parameter_list):
        response = mdc_client.create_bulk_parameter_api(parameter_list)

        Base.cal_debug(MODULE_NAME, CREATE, response)
        res = Base.format_response(response, CREATE, CREATED, MODULE_NAME)
        return res

    @staticmethod
    def get_by_id(mdc_client, parameter_id):
        response = mdc_client.get_parameter_by_id_api(parameter_id)

        curr_method_name = inspect.currentframe().f_code.co_name
        Base.cal_debug(MODULE_NAME, curr_method_name, response)
        return Base.format_response(response, GET, OK, MODULE_NAME)

    @staticmethod
    def get_all_by_data_source_and_name(mdc_client, data_source, name,
                                        page=DEF_PAGE,
                                        page_size=DEF_PAGE_SIZE):
        response = mdc_client.get_all_parameters_by_data_source_and_name_api(
            data_source, name, page, page_size)

        curr_method_name = inspect.currentframe().f_code.co_name
        Base.cal_debug(MODULE_NAME, curr_method_name, response)
        return Base.format_response(response, GET, OK, MODULE_NAME)

    @staticmethod
    def delete_by_id(mdc_client, parameter_id):
        resp = mdc_client.delete_parameter_api(parameter_id)
        Base.cal_debug(MODULE_NAME, DELETE, resp)

        return Base.format_response(resp, DELETE, NO_CONTENT, MODULE_NAME)

    def __get_resource(self):
        parameter = {
            MODULE_NAME: {
                'data_source': self.data_source,
                'name': self.name,
                'value': self.value,
                'minimum': self.minimum,
                'maximum': self.maximum,
                'mean': self.mean,
                'standard_deviation': self.standard_deviation,
                'data_type_id': self.data_type_id,
                'parameter_type_id': self.parameter_type_id,
                'unit_id': self.unit_id,
                'unit_prefix': self.unit_prefix,
                'flg_available': self.flg_available,
                'description': self.description,
                'data_groups_parameters_attributes':
                    self.data_groups_parameters_attributes
            }
        }

        return parameter
