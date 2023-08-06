"""DataFile module class"""

import inspect

from ..common.base import Base
from ..common.config import *

MODULE_NAME = DATA_FILE


class DataFile:
    def __init__(self, metadata_client, data_group_id, files):
        self.metadata_client = metadata_client
        self.id = None
        self.data_group_id = data_group_id
        self.files = files

    def create(self):
        mdc_client = self.metadata_client
        response = mdc_client.create_data_file_api(self.__get_resource())

        Base.cal_debug(MODULE_NAME, CREATE, response)
        res = Base.format_response(response, CREATE, CREATED, MODULE_NAME)

        if res['success']:
            self.id = res['data']['id']

        return res

    def delete(self):
        mdc_client = self.metadata_client
        response = mdc_client.delete_data_file_api(self.id)
        Base.cal_debug(MODULE_NAME, DELETE, response)

        return Base.format_response(response, DELETE, NO_CONTENT, MODULE_NAME)

    def update(self):
        mdc_client = self.metadata_client
        response = mdc_client.update_data_file_api(self.id,
                                                   self.__get_resource())

        Base.cal_debug(MODULE_NAME, UPDATE, response)
        return Base.format_response(response, UPDATE, OK, MODULE_NAME)

    @staticmethod
    def create_from_dict(mdc_client, data_file):
        new_data_file = DataFile(metadata_client=mdc_client,
                                 data_group_id=data_file['data_group_id'],
                                 files=data_file['files'])

        resp = new_data_file.create()
        return resp

    @staticmethod
    def delete_by_id(mdc_client, data_file_id):
        resp = mdc_client.delete_data_file_api(data_file_id)
        Base.cal_debug(MODULE_NAME, DELETE, resp)

        return Base.format_response(resp, DELETE, NO_CONTENT, MODULE_NAME)

    @staticmethod
    def update_from_dict(mdc_client, data_file_id, data_file):
        response = mdc_client.update_data_file_api(data_file_id, data_file)

        Base.cal_debug(MODULE_NAME, UPDATE, response)
        return Base.format_response(response, UPDATE, OK, MODULE_NAME)

    @staticmethod
    def get_by_id(mdc_client, data_file_id):
        response = mdc_client.get_data_file_by_id_api(data_file_id)

        curr_method_name = inspect.currentframe().f_code.co_name
        Base.cal_debug(MODULE_NAME, curr_method_name, response)
        return Base.format_response(response, GET, OK, MODULE_NAME)

    @staticmethod
    def get_all_by_data_group_id(mdc_client, data_grp_id,
                                 page=DEF_PAGE, page_size=DEF_PAGE_SIZE):
        resp = mdc_client.get_all_data_files_by_data_group_id_api(
            data_grp_id, page, page_size)

        curr_method_name = inspect.currentframe().f_code.co_name
        Base.cal_debug(MODULE_NAME, curr_method_name, resp)
        return Base.format_response(resp, GET, OK, MODULE_NAME)

    @staticmethod
    def search_data_files(mdc_client, run_number, proposal_number):
        resp = mdc_client.search_data_files_api(run_number, proposal_number)

        curr_method_name = inspect.currentframe().f_code.co_name
        Base.cal_debug(MODULE_NAME, curr_method_name, resp)
        return Base.format_response(resp, GET, OK, MODULE_NAME)

    def __get_resource(self):
        data_file = {
            MODULE_NAME: {
                'data_group_id': self.data_group_id,
                'files': self.files
            }
        }

        return data_file
