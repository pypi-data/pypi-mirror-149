"""Run module class"""

import inspect

from ..common.base import Base
from ..common.config import *

MODULE_NAME = RUN


class Run:
    def __init__(self, metadata_client,
                 run_number, run_alias, experiment_id, sample_id,
                 begin_at, end_at, first_train, last_train,
                 flg_available, flg_status,
                 original_format, system_msg,
                 description=''):
        self.metadata_client = metadata_client
        self.id = None
        self.run_number = run_number
        self.run_alias = run_alias
        self.experiment_id = experiment_id
        self.sample_id = sample_id
        self.begin_at = begin_at
        self.end_at = end_at
        self.first_train = first_train
        self.last_train = last_train
        self.flg_available = flg_available
        self.flg_status = flg_status
        self.original_format = original_format
        self.system_msg = system_msg
        self.description = description

    def create(self):
        mdc_client = self.metadata_client
        response = mdc_client.create_run_api(self.__get_resource())

        Base.cal_debug(MODULE_NAME, CREATE, response)
        res = Base.format_response(response, CREATE, CREATED, MODULE_NAME)

        if res['success']:
            self.id = res['data']['id']

        return res

    def delete(self):
        mdc_client = self.metadata_client
        response = mdc_client.delete_run_api(self.id)

        Base.cal_debug(MODULE_NAME, DELETE, response)
        return Base.format_response(response, DELETE, NO_CONTENT, MODULE_NAME)

    def update(self):
        mdc_client = self.metadata_client
        response = mdc_client.update_run_api(self.id,
                                             self.__get_resource())

        Base.cal_debug(MODULE_NAME, UPDATE, response)
        return Base.format_response(response, UPDATE, OK, MODULE_NAME)

    @staticmethod
    def create_from_dict(mdc_client, run):
        new_run = Run(
            metadata_client=mdc_client,
            run_number=run['run_number'],
            run_alias=run['run_alias'],
            experiment_id=run['experiment_id'],
            sample_id=run['sample_id'],
            begin_at=run['begin_at'],
            end_at=run['end_at'],
            first_train=run['first_train'],
            last_train=run['last_train'],
            flg_available=run['flg_available'],
            flg_status=run['flg_status'],
            original_format=run['original_format'],
            system_msg=run['system_msg'],
            description=run['description'])

        resp = new_run.create()
        return resp

    @staticmethod
    def update_from_dict(mdc_client, run_id, run):
        response = mdc_client.update_run_api(run_id, run)

        Base.cal_debug(MODULE_NAME, UPDATE, response)
        return Base.format_response(response, UPDATE, OK, MODULE_NAME)

    @staticmethod
    def delete_by_id(mdc_client, run_id):
        resp = mdc_client.delete_run_api(run_id)
        Base.cal_debug(MODULE_NAME, DELETE, resp)

        return Base.format_response(resp, DELETE, NO_CONTENT, MODULE_NAME)

    @staticmethod
    def get_by_id(mdc_client, run_id):
        response = mdc_client.get_run_by_id_api(run_id)

        curr_method_name = inspect.currentframe().f_code.co_name
        Base.cal_debug(MODULE_NAME, curr_method_name, response)
        return Base.format_response(response, GET, OK, MODULE_NAME)

    @staticmethod
    def get_all_by_run_number_and_experiment_id(mdc_client,
                                                run_number, experiment_id):
        response = mdc_client.get_run_by_run_number_and_experiment_id_api(
            run_number, experiment_id
        )

        curr_method_name = inspect.currentframe().f_code.co_name
        Base.cal_debug(MODULE_NAME, curr_method_name, response)
        return Base.format_response(response, GET, OK, MODULE_NAME)

    @staticmethod
    def get_by_run_number_and_experiment_id(mdc_client,
                                            run_number, experiment_id):
        res = Run.get_all_by_run_number_and_experiment_id(
            mdc_client, run_number, experiment_id)

        if res['success']:
            res = Base.unique_key_format_result(res=res,
                                                module_name=MODULE_NAME)

        return res

    @staticmethod
    def get_all_by_run_number_and_proposal_number(mdc_client,
                                                  run_number, proposal_number):
        response = mdc_client.get_run_all_raw_data_groups_ids_api(
            run_number, proposal_number
        )

        curr_method_name = inspect.currentframe().f_code.co_name
        Base.cal_debug(MODULE_NAME, curr_method_name, response)
        return Base.format_response(response, GET, OK, MODULE_NAME)

    @staticmethod
    def get_by_run_number_and_proposal_number(mdc_client,
                                              run_number, proposal_number):
        res = Run.get_all_by_run_number_and_proposal_number(
            mdc_client, run_number, proposal_number)

        if res['success']:
            res = Base.unique_key_format_result(res=res,
                                                module_name=MODULE_NAME)

        return res

    @staticmethod
    def get_all_raw_data_groups(mdc_client, run_number, proposal_number):
        response = mdc_client.get_run_all_raw_data_groups_ids_api(
            run_number, proposal_number)

        curr_method_name = inspect.currentframe().f_code.co_name
        Base.cal_debug(MODULE_NAME, curr_method_name, response)
        return Base.format_response(response, GET, OK, MODULE_NAME)

    def __get_resource(self):
        run = {
            MODULE_NAME: {
                'run_number': self.run_number,
                'run_alias': self.run_alias,
                'experiment_id': self.experiment_id,
                'sample_id': self.sample_id,
                'begin_at': self.begin_at,
                'end_at': self.end_at,
                'first_train': self.first_train,
                'last_train': self.last_train,
                'flg_available': self.flg_available,
                'flg_status': self.flg_status,
                'original_format': self.original_format,
                'system_msg': self.system_msg,
                'description': self.description
            }
        }

        return run
