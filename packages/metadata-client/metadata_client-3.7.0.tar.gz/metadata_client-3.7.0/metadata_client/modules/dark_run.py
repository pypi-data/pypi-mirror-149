"""DarkRun module class"""

import inspect

from ..common.base import Base
from ..common.config import *

MODULE_NAME = DARK_RUN


class DarkRun:
    def __init__(self, metadata_client,
                 proposal_id, detector_id, detector_identifier,
                 detector_type_id, pdu_physical_names, runs_info,
                 operation_mode_id, operation_mode_name, flg_status,
                 pdu_karabo_das, operation_mode_identifier, size,
                 report_url, input_path, output_path,
                 calcat_feedback, description=''):
        self.metadata_client = metadata_client
        self.id = None
        self.proposal_id = proposal_id
        self.detector_id = detector_id
        self.detector_identifier = detector_identifier
        self.detector_type_id = detector_type_id
        self.pdu_physical_names = pdu_physical_names
        self.runs_info = runs_info
        self.operation_mode_id = operation_mode_id
        self.operation_mode_name = operation_mode_name
        self.flg_status = flg_status
        self.pdu_karabo_das = pdu_karabo_das
        self.operation_mode_identifier = operation_mode_identifier
        self.size = size
        self.full_calcat_report_url = None
        self.report_url = report_url
        self.input_path = input_path
        self.output_path = output_path
        self.calcat_feedback = calcat_feedback
        self.description = description

    def create(self):
        mdc_client = self.metadata_client
        response = mdc_client.create_dark_run_api(self.__get_resource())

        Base.cal_debug(MODULE_NAME, CREATE, response)
        res = Base.format_response(response, CREATE, CREATED, MODULE_NAME)

        if res['success']:
            self.id = res['data']['id']

        return res

    def delete(self):
        mdc_client = self.metadata_client
        response = mdc_client.delete_dark_run_api(self.id)
        Base.cal_debug(MODULE_NAME, DELETE, response)

        return Base.format_response(response, DELETE, NO_CONTENT, MODULE_NAME)

    def update(self):
        mdc_client = self.metadata_client
        response = mdc_client.update_dark_run_api(self.id,
                                                  self.__get_resource())

        Base.cal_debug(MODULE_NAME, UPDATE, response)
        return Base.format_response(response, UPDATE, OK, MODULE_NAME)

    @staticmethod
    def get_by_id(mdc_client, dark_run_id):
        response = mdc_client.get_dark_run_by_id_api(dark_run_id)

        curr_method_name = inspect.currentframe().f_code.co_name
        Base.cal_debug(MODULE_NAME, curr_method_name, response)
        return Base.format_response(response, GET, OK, MODULE_NAME)

    @staticmethod
    def get_all_dark_runs_by_proposal_id(mdc_client, proposal_id,
                                         page=DEF_PAGE,
                                         page_size=DEF_PAGE_SIZE):
        response = mdc_client.get_all_dark_runs_by_proposal_id_api(
            proposal_id, page, page_size)

        curr_method_name = inspect.currentframe().f_code.co_name
        Base.cal_debug(MODULE_NAME, curr_method_name, response)
        return Base.format_response(response, GET, OK, MODULE_NAME)

    @staticmethod
    def get_all_dark_runs_by_detector_id(mdc_client, detector_id,
                                         page=DEF_PAGE,
                                         page_size=DEF_PAGE_SIZE):
        response = mdc_client.get_all_dark_runs_by_detector_id_api(
            detector_id, page, page_size)

        curr_method_name = inspect.currentframe().f_code.co_name
        Base.cal_debug(MODULE_NAME, curr_method_name, response)
        return Base.format_response(response, GET, OK, MODULE_NAME)

    def __get_resource(self):
        dark_run = {
            MODULE_NAME: {
                'proposal_id': self.proposal_id,
                'detector_id': self.detector_id,
                'detector_identifier': self.detector_identifier,
                'detector_type_id': self.detector_type_id,
                'pdu_physical_names': self.pdu_physical_names,
                'runs_info': self.runs_info,
                'operation_mode_id': self.operation_mode_id,
                'operation_mode_name': self.operation_mode_name,
                'flg_status': self.flg_status,
                'pdu_karabo_das': self.pdu_karabo_das,
                'operation_mode_identifier': self.operation_mode_identifier,
                'size': self.size,
                'full_calcat_report_url': self.full_calcat_report_url,
                'report_url': self.report_url,
                'input_path': self.input_path,
                'output_path': self.output_path,
                'calcat_feedback': self.calcat_feedback,
                'description': self.description
            }
        }

        return dark_run
