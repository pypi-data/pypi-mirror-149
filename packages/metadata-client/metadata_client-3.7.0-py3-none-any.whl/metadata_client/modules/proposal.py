"""Proposal module class"""

import inspect

from ..common.base import Base
from ..common.config import *

MODULE_NAME = PROPOSAL


class Proposal:
    def __init__(self, metadata_client,
                 number, title, abstract, url,
                 instrument_id, instrument_cycle_id,
                 principal_investigator_id, main_proposer_id,
                 begin_at, end_at, release_at,
                 flg_beamtime_status, beamtime_start_at, beamtime_end_at,
                 flg_proposal_system, flg_available, description=''):
        self.metadata_client = metadata_client
        self.id = None
        self.number = number
        self.title = title
        self.abstract = abstract
        self.url = url
        self.instrument_id = instrument_id
        self.instrument_cycle_id = instrument_cycle_id
        self.principal_investigator_id = principal_investigator_id
        self.main_proposer_id = main_proposer_id
        self.begin_at = begin_at
        self.end_at = end_at
        self.release_at = release_at
        self.flg_beamtime_status = flg_beamtime_status
        self.beamtime_start_at = beamtime_start_at
        self.beamtime_end_at = beamtime_end_at
        self.flg_proposal_system = flg_proposal_system
        self.flg_available = flg_available
        self.description = description

    def create(self):
        mdc_client = self.metadata_client
        response = mdc_client.create_proposal_api(self.__get_resource())

        Base.cal_debug(MODULE_NAME, CREATE, response)
        res = Base.format_response(response, CREATE, CREATED, MODULE_NAME)

        if res['success']:
            self.id = res['data']['id']

        return res

    def delete(self):
        mdc_client = self.metadata_client
        response = mdc_client.delete_proposal_api(self.id)
        Base.cal_debug(MODULE_NAME, DELETE, response)

        return Base.format_response(response, DELETE, NO_CONTENT, MODULE_NAME)

    def update(self):
        mdc_client = self.metadata_client
        response = mdc_client.update_proposal_api(self.id,
                                                  self.__get_resource())

        Base.cal_debug(MODULE_NAME, UPDATE, response)
        return Base.format_response(response, UPDATE, OK, MODULE_NAME)

    @staticmethod
    def create_from_dict(mdc_client, proposal):
        new_proposal = Proposal(
            metadata_client=mdc_client,
            number=proposal['number'],
            title=proposal['title'],
            abstract=proposal['abstract'],
            url=proposal['url'],
            instrument_id=proposal['instrument_id'],
            instrument_cycle_id=proposal['instrument_cycle_id'],
            principal_investigator_id=proposal['principal_investigator_id'],
            main_proposer_id=proposal['main_proposer_id'],
            begin_at=proposal['begin_at'],
            end_at=proposal['end_at'],
            release_at=proposal['release_at'],
            flg_beamtime_status=proposal['flg_beamtime_status'],
            beamtime_start_at=proposal['beamtime_start_at'],
            beamtime_end_at=proposal['beamtime_end_at'],
            flg_proposal_system=proposal['flg_proposal_system'],
            flg_available=proposal['flg_available'],
            description=proposal['description'])

        resp = new_proposal.create()
        return resp

    @staticmethod
    def delete_by_id(mdc_client, proposal_id):
        resp = mdc_client.delete_proposal_api(proposal_id)
        Base.cal_debug(MODULE_NAME, DELETE, resp)

        return Base.format_response(resp, DELETE, NO_CONTENT, MODULE_NAME)

    @staticmethod
    def get_by_id(mdc_client, proposal_id):
        response = mdc_client.get_proposal_by_id_api(proposal_id)

        curr_method_name = inspect.currentframe().f_code.co_name
        Base.cal_debug(MODULE_NAME, curr_method_name, response)
        return Base.format_response(response, GET, OK, MODULE_NAME)

    @staticmethod
    def get_all_by_number(mdc_client, number, page=DEF_PAGE,
                          page_size=DEF_PAGE_SIZE):
        response = mdc_client.get_all_proposals_by_number_api(
            number, page, page_size)

        curr_method_name = inspect.currentframe().f_code.co_name
        Base.cal_debug(MODULE_NAME, curr_method_name, response)
        return Base.format_response(response, GET, OK, MODULE_NAME)

    @staticmethod
    def get_by_number(mdc_client, number):
        response = mdc_client.get_proposal_by_number_api(number)

        curr_method_name = inspect.currentframe().f_code.co_name
        Base.cal_debug(MODULE_NAME, curr_method_name, response)
        return Base.format_response(response, GET, OK, MODULE_NAME)

    @staticmethod
    def get_by_number_daq_info(mdc_client, number):
        response = mdc_client.get_proposal_by_number_daq_info_api(number)

        curr_method_name = inspect.currentframe().f_code.co_name
        Base.cal_debug(MODULE_NAME, curr_method_name, response)
        return Base.format_response(response, GET, OK, MODULE_NAME)

    @staticmethod
    def get_runs_by_proposal_number(mdc_client, proposal_number,
                                    run_number=None, page=DEF_PAGE,
                                    page_size=DEF_PAGE_SIZE):
        response = mdc_client.get_runs_by_proposal_number_api(
            proposal_number, run_number, page, page_size)
        return Base.format_response(response, GET, OK, MODULE_NAME)

    @staticmethod
    def get_active_proposal_by_instrument(mdc_client, instrument_id):
        resp = mdc_client.get_instrument_active_proposal_api(instrument_id)

        curr_method_name = inspect.currentframe().f_code.co_name
        Base.cal_debug(MODULE_NAME, curr_method_name, resp)
        return Base.format_response(resp, GET, OK, MODULE_NAME)

    def __get_resource(self):
        proposal = {
            MODULE_NAME: {
                'number': self.number,
                'title': self.title,
                'abstract': self.abstract,
                'url': self.url,
                'instrument_id': self.instrument_id,
                'instrument_cycle_id': self.instrument_cycle_id,
                'principal_investigator_id': self.principal_investigator_id,
                'main_proposer_id': self.main_proposer_id,
                'begin_at': self.begin_at,
                'end_at': self.end_at,
                'release_at': self.release_at,
                'flg_beamtime_status': self.flg_beamtime_status,
                'beamtime_start_at': self.beamtime_start_at,
                'beamtime_end_at': self.beamtime_end_at,
                'flg_proposal_system': self.flg_proposal_system,
                'flg_available': self.flg_available,
                'description': self.description
            }
        }

        return proposal
