"""Repository module class"""
import inspect

from ..common.base import Base
from ..common.config import *

MODULE_NAME = REPOSITORY


class Repository:
    def __init__(self, metadata_client,
                 name, identifier, img_url, mount_point,
                 transfer_agent_identifier, transfer_agent_server_url,
                 flg_context, flg_available, description=''):
        self.metadata_client = metadata_client
        self.id = None
        self.name = name
        self.identifier = identifier
        self.img_url = img_url
        self.mount_point = mount_point
        self.transfer_agent_identifier = transfer_agent_identifier
        self.transfer_agent_server_url = transfer_agent_server_url
        self.flg_context = flg_context
        self.flg_available = flg_available
        self.description = description

    def create(self):
        mdc_client = self.metadata_client
        response = mdc_client.create_repository_api(self.__get_resource())

        Base.cal_debug(MODULE_NAME, CREATE, response)
        res = Base.format_response(response, CREATE, CREATED, MODULE_NAME)

        if res['success']:
            self.id = res['data']['id']

        return res

    def delete(self):
        mdc_client = self.metadata_client
        response = mdc_client.delete_repository_api(self.id)
        Base.cal_debug(MODULE_NAME, DELETE, response)

        return Base.format_response(response, DELETE, NO_CONTENT, MODULE_NAME)

    def update(self):
        mdc_client = self.metadata_client
        response = mdc_client.update_repository_api(self.id,
                                                    self.__get_resource())

        Base.cal_debug(MODULE_NAME, UPDATE, response)
        return Base.format_response(response, UPDATE, OK, MODULE_NAME)

    @staticmethod
    def get_by_id(mdc_client, repository_id):
        response = mdc_client.get_repository_by_id_api(repository_id)

        curr_method_name = inspect.currentframe().f_code.co_name
        Base.cal_debug(MODULE_NAME, curr_method_name, response)
        return Base.format_response(response, GET, OK, MODULE_NAME)

    @staticmethod
    def get_all_by_name(mdc_client, name, page=DEF_PAGE,
                        page_size=DEF_PAGE_SIZE):
        response = mdc_client.get_all_repositories_by_name_api(
            name, page, page_size)

        curr_method_name = inspect.currentframe().f_code.co_name
        Base.cal_debug(MODULE_NAME, curr_method_name, response)
        return Base.format_response(response, GET, OK, MODULE_NAME)

    @staticmethod
    def get_all_by_identifier(mdc_client, identifier):
        response = mdc_client.get_all_repositories_by_identifier_api(
            identifier)

        curr_method_name = inspect.currentframe().f_code.co_name
        Base.cal_debug(MODULE_NAME, curr_method_name, response)
        return Base.format_response(response, GET, OK, MODULE_NAME)

    @staticmethod
    def get_by_name(mdc_client, name):
        res = Repository.get_all_by_name(mdc_client, name)

        if res['success']:
            res = Base.unique_key_format_result(res=res,
                                                module_name=MODULE_NAME,
                                                unique_id=name)

        return res

    def __get_resource(self):
        repository = {
            MODULE_NAME: {
                'name': self.name,
                'identifier': self.identifier,
                'img_url': self.img_url,
                'mount_point': self.mount_point,
                'transfer_agent_identifier': self.transfer_agent_identifier,
                'transfer_agent_server_url': self.transfer_agent_server_url,
                'flg_context': self.flg_context,
                'flg_available': self.flg_available,
                'description': self.description
            }
        }

        return repository
