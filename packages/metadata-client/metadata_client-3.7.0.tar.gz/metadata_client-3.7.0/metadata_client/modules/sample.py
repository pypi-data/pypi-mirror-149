"""Sample module class"""

import inspect

from ..common.base import Base
from ..common.config import *

MODULE_NAME = SAMPLE


class Sample:
    def __init__(self, metadata_client,
                 name, url,
                 sample_type_id, proposal_id,
                 flg_proposal_system, proposal_system_id,
                 flg_available, description=''):
        self.metadata_client = metadata_client
        self.id = None
        self.name = name
        self.proposal_id = proposal_id
        self.sample_type_id = sample_type_id
        self.url = url
        self.flg_proposal_system = flg_proposal_system
        self.proposal_system_id = proposal_system_id
        self.flg_available = flg_available
        self.description = description

    def create(self):
        mdc_client = self.metadata_client
        response = mdc_client.create_sample_api(self.__get_resource())

        Base.cal_debug(MODULE_NAME, CREATE, response)
        res = Base.format_response(response, CREATE, CREATED, MODULE_NAME)

        if res['success']:
            self.id = res['data']['id']

        return res

    def delete(self):
        mdc_client = self.metadata_client
        response = mdc_client.delete_sample_api(self.id)
        Base.cal_debug(MODULE_NAME, DELETE, response)

        return Base.format_response(response, DELETE, NO_CONTENT, MODULE_NAME)

    def update(self):
        mdc_client = self.metadata_client
        response = mdc_client.update_sample_api(self.id,
                                                self.__get_resource())

        Base.cal_debug(MODULE_NAME, UPDATE, response)
        return Base.format_response(response, UPDATE, OK, MODULE_NAME)

    @staticmethod
    def set_by_name_and_proposal_id(mdc_client, sample_h):
        resp = Sample.get_by_name_and_proposal_id(mdc_client,
                                                  sample_h['name'],
                                                  sample_h['proposal_id'])

        if resp['success'] and resp['data'] != {}:
            return resp

        new_sample = Sample(
            metadata_client=mdc_client,
            name=sample_h['name'],
            url=sample_h['url'],
            sample_type_id=sample_h['sample_type_id'],
            proposal_id=sample_h['proposal_id'],
            flg_proposal_system=sample_h['flg_proposal_system'],
            proposal_system_id=sample_h['proposal_system_id'],
            flg_available=sample_h['flg_available'],
            description=sample_h['description'])

        resp = new_sample.create()

        return resp

    @staticmethod
    def delete_by_id(mdc_client, sample_id):
        resp = mdc_client.delete_sample_api(sample_id)
        Base.cal_debug(MODULE_NAME, DELETE, resp)

        return Base.format_response(resp, DELETE, NO_CONTENT, MODULE_NAME)

    @staticmethod
    def get_by_id(mdc_client, sample_id):
        response = mdc_client.get_sample_by_id_api(sample_id)

        curr_method_name = inspect.currentframe().f_code.co_name
        Base.cal_debug(MODULE_NAME, curr_method_name, response)
        return Base.format_response(response, GET, OK, MODULE_NAME)

    @staticmethod
    def get_all_by_name_and_proposal_id(mdc_client, name, proposal_id,
                                        page=DEF_PAGE,
                                        page_size=DEF_PAGE_SIZE):
        response = mdc_client.get_all_samples_by_name_and_proposal_id_api(
            name, proposal_id, page, page_size)

        curr_method_name = inspect.currentframe().f_code.co_name
        Base.cal_debug(MODULE_NAME, curr_method_name, response)
        return Base.format_response(response, GET, OK, MODULE_NAME)

    @staticmethod
    def get_all_by_proposal_id(mdc_client, proposal_id, page=DEF_PAGE,
                               page_size=DEF_PAGE_SIZE):
        resp = mdc_client.get_all_samples_by_proposal_id_api(
            proposal_id, page, page_size)

        curr_method_name = inspect.currentframe().f_code.co_name
        Base.cal_debug(MODULE_NAME, curr_method_name, resp)
        return Base.format_response(resp, GET, OK, MODULE_NAME)

    @staticmethod
    def get_by_name_and_proposal_id(mdc_client, name, proposal_id,
                                    page=DEF_PAGE, page_size=DEF_PAGE_SIZE):
        res = Sample.get_all_by_name_and_proposal_id(
            mdc_client, name, proposal_id, page, page_size)

        if res['success']:
            res = Base.unique_key_format_result(res=res,
                                                module_name=MODULE_NAME)

        return res

    def __get_resource(self):
        sample = {
            MODULE_NAME: {
                'name': self.name,
                'url': self.url,
                'sample_type_id': self.sample_type_id,
                'proposal_id': self.proposal_id,
                'flg_proposal_system': self.flg_proposal_system,
                'proposal_system_id': self.proposal_system_id,
                'flg_available': self.flg_available,
                'description': self.description
            }
        }

        return sample
