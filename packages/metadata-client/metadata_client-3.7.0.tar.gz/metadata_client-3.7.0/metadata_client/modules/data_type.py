"""DataType module class"""

import inspect

from ..common.base import Base
from ..common.config import *

MODULE_NAME = DATA_TYPE


class DataType:
    def __init__(self, metadata_client,
                 name, identifier,
                 flg_available, description=''):
        self.metadata_client = metadata_client
        self.id = None
        self.name = name
        self.identifier = identifier
        self.flg_available = flg_available
        self.description = description

    def create(self):
        mdc_client = self.metadata_client
        response = mdc_client.create_data_type_api(self.__get_resource())

        Base.cal_debug(MODULE_NAME, CREATE, response)
        res = Base.format_response(response, CREATE, CREATED, MODULE_NAME)

        if res['success']:
            self.id = res['data']['id']

        return res

    def delete(self):
        mdc_client = self.metadata_client
        response = mdc_client.delete_data_type_api(self.id)
        Base.cal_debug(MODULE_NAME, DELETE, response)

        return Base.format_response(response, DELETE, NO_CONTENT, MODULE_NAME)

    def update(self):
        mdc_client = self.metadata_client
        response = mdc_client.update_data_type_api(self.id,
                                                   self.__get_resource())

        Base.cal_debug(MODULE_NAME, UPDATE, response)
        return Base.format_response(response, UPDATE, OK, MODULE_NAME)

    @staticmethod
    def get_by_id(mdc_client, data_type_id):
        response = mdc_client.get_data_type_by_id_api(data_type_id)

        curr_method_name = inspect.currentframe().f_code.co_name
        Base.cal_debug(MODULE_NAME, curr_method_name, response)
        return Base.format_response(response, GET, OK, MODULE_NAME)

    @staticmethod
    def get_all_by_name(mdc_client, name, page=DEF_PAGE,
                        page_size=DEF_PAGE_SIZE):
        response = mdc_client.get_all_data_types_by_name_api(
            name, page, page_size)

        curr_method_name = inspect.currentframe().f_code.co_name
        Base.cal_debug(MODULE_NAME, curr_method_name, response)
        return Base.format_response(response, GET, OK, MODULE_NAME)

    @staticmethod
    def get_by_name(mdc_client, name):
        res = DataType.get_all_by_name(mdc_client, name)

        if res['success']:
            res = Base.unique_key_format_result(res=res,
                                                module_name=MODULE_NAME,
                                                unique_id=name)

        return res

    def __get_resource(self):
        data_type = {
            MODULE_NAME: {
                'name': self.name,
                'identifier': self.identifier,
                'flg_available': self.flg_available,
                'description': self.description
            }
        }

        return data_type
