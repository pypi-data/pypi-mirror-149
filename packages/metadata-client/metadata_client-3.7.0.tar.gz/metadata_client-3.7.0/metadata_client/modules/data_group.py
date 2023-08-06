"""DataGroup module class"""

import inspect

from ..common.base import Base
from ..common.config import *

MODULE_NAME = DATA_GROUP


class DataGroup:
    def __init__(self, metadata_client,
                 name, language,
                 data_group_type_id, experiment_id, user_id,
                 prefix_path,
                 flg_available, flg_writing, flg_public,
                 format, data_passport,
                 removed_at,
                 description='',
                 runs_data_groups_attributes=None):
        self.metadata_client = metadata_client
        self.id = None
        self.name = name
        self.language = language
        self.doi = None
        self.data_group_type_id = data_group_type_id
        self.experiment_id = experiment_id
        self.user_id = user_id
        self.prefix_path = prefix_path
        self.flg_available = flg_available
        self.flg_writing = flg_writing
        self.flg_public = flg_public
        self.format = format
        self.data_passport = data_passport
        self.removed_at = removed_at
        self.description = description
        self.runs_data_groups_attributes = runs_data_groups_attributes

    def create(self):
        mdc_client = self.metadata_client
        response = mdc_client.create_data_group_api(self.__get_resource())

        Base.cal_debug(MODULE_NAME, CREATE, response)
        res = Base.format_response(response, CREATE, CREATED, MODULE_NAME)

        if res['success']:
            self.id = res['data']['id']

        return res

    def delete(self):
        mdc_client = self.metadata_client
        response = mdc_client.delete_data_group_api(self.id)
        Base.cal_debug(MODULE_NAME, DELETE, response)

        return Base.format_response(response, DELETE, NO_CONTENT, MODULE_NAME)

    def update(self):
        mdc_client = self.metadata_client
        response = mdc_client.update_data_group_api(self.id,
                                                    self.__get_resource())

        Base.cal_debug(MODULE_NAME, UPDATE, response)
        return Base.format_response(response, UPDATE, OK, MODULE_NAME)

    @staticmethod
    def create_from_dict(mdc_client, data_grp):
        new_data_group = DataGroup(
            metadata_client=mdc_client,
            name=data_grp['name'],
            language=data_grp['language'],
            data_group_type_id=data_grp['data_group_type_id'],
            experiment_id=data_grp['experiment_id'],
            user_id=data_grp['user_id'],
            prefix_path=data_grp['prefix_path'],
            flg_available=data_grp['flg_available'],
            flg_writing=data_grp['flg_writing'],
            flg_public=data_grp['flg_public'],
            format=data_grp['format'],
            data_passport=data_grp['data_passport'],
            removed_at=data_grp['removed_at'],
            description=data_grp['description'],
            runs_data_groups_attributes=data_grp[
                'runs_data_groups_attributes'])

        resp = new_data_group.create()
        return resp

    @staticmethod
    def delete_by_id(mdc_client, data_group_id):
        resp = mdc_client.delete_data_group_api(data_group_id)
        Base.cal_debug(MODULE_NAME, DELETE, resp)

        return Base.format_response(resp, DELETE, NO_CONTENT, MODULE_NAME)

    @staticmethod
    def update_from_dict(mdc_client, data_group_id, data_grp):
        response = mdc_client.update_data_group_api(data_group_id, data_grp)

        Base.cal_debug(MODULE_NAME, UPDATE, response)
        return Base.format_response(response, UPDATE, OK, MODULE_NAME)

    @staticmethod
    def get_by_id(mdc_client, data_group_id):
        response = mdc_client.get_data_group_by_id_api(data_group_id)

        curr_method_name = inspect.currentframe().f_code.co_name
        Base.cal_debug(MODULE_NAME, curr_method_name, response)
        return Base.format_response(response, GET, OK, MODULE_NAME)

    @staticmethod
    def get_all_by_name(mdc_client, name, page=DEF_PAGE,
                        page_size=DEF_PAGE_SIZE):
        response = mdc_client.get_all_data_groups_by_name_api(
            name, page, page_size)

        curr_method_name = inspect.currentframe().f_code.co_name
        Base.cal_debug(MODULE_NAME, curr_method_name, response)
        return Base.format_response(response, GET, OK, MODULE_NAME)

    @staticmethod
    def get_all_by_experiment_id(mdc_client, experiment_id,
                                 page=DEF_PAGE, page_size=DEF_PAGE_SIZE):
        response = mdc_client.get_all_data_groups_by_experiment_id_api(
            experiment_id, page, page_size)

        curr_method_name = inspect.currentframe().f_code.co_name
        Base.cal_debug(MODULE_NAME, curr_method_name, response)
        return Base.format_response(response, GET, OK, MODULE_NAME)

    def __get_resource(self):
        data_group = {
            MODULE_NAME: {
                'name': self.name,
                'language': self.language,
                'doi': self.doi,
                'data_group_type_id': self.data_group_type_id,
                'experiment_id': self.experiment_id,
                'user_id': self.user_id,
                'prefix_path': self.prefix_path,
                'flg_available': self.flg_available,
                'flg_writing': self.flg_writing,
                'flg_public': self.flg_public,
                'format': self.format,
                'data_passport': self.data_passport,
                'removed_at': self.removed_at,
                'description': self.description,
                'runs_data_groups_attributes': self.runs_data_groups_attributes
            }
        }

        return data_group
