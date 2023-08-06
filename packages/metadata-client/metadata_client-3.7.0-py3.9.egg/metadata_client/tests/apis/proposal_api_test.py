"""ProposalApiTest class"""

import unittest
from datetime import datetime, timedelta, timezone

from metadata_client import MetadataClient
from .api_base import ApiBase
from ..common.config_test import *
from ..common.generators import Generators
from ..common.secrets import *
from ..common.util_datetime import UtilDatetime as util_dt


class ProposalApiTest(ApiBase, unittest.TestCase):
    client_api = MetadataClient(
        client_id=CLIENT_OAUTH2_INFO['CLIENT_ID'],
        client_secret=CLIENT_OAUTH2_INFO['CLIENT_SECRET'],
        token_url=CLIENT_OAUTH2_INFO['TOKEN_URL'],
        refresh_url=CLIENT_OAUTH2_INFO['REFRESH_URL'],
        auth_url=CLIENT_OAUTH2_INFO['AUTH_URL'],
        scope=CLIENT_OAUTH2_INFO['SCOPE'],
        user_email=CLIENT_OAUTH2_INFO['EMAIL'],
        base_api_url=BASE_API_URL)

    __utc = timezone(timedelta())

    __now = datetime.now()
    end_at = datetime(__now.year, __now.month, __now.day,
                      __now.hour, __now.minute, __now.second,
                      __now.microsecond, tzinfo=__utc)
    __yesterday = __now - timedelta(1)
    begin_at = datetime(__yesterday.year, __yesterday.month, __yesterday.day,
                        __yesterday.hour, __yesterday.minute,
                        __yesterday.second, __yesterday.microsecond,
                        tzinfo=__utc)
    __tomorrow = __now + timedelta(365 * 3 + 1)
    release_at = datetime(__tomorrow.year, __tomorrow.month, __tomorrow.day,
                          __tomorrow.hour, __tomorrow.minute,
                          __tomorrow.second, __tomorrow.microsecond,
                          tzinfo=__utc)

    def test_create_proposal_api(self):
        __unique_id = Generators.generate_unique_id(min_value=2017,
                                                    max_value=799999)
        proposal = {
            PROPOSAL: {
                'number': __unique_id,
                'title': 'this is the title',
                'abstract': 'this is the abstract',
                'url': 'https://in.xfel.eu/upex/proposal/{0}'.format(
                    __unique_id),
                'instrument_id': '1',
                'instrument_identifier': 'SPB',
                'instrument_cycle_id': '-1',
                'principal_investigator_id': '-1',
                'main_proposer_id': '-1',
                'begin_at': util_dt.datetime_to_local_tz_str(self.begin_at),
                'end_at': util_dt.datetime_to_local_tz_str(self.end_at),
                'release_at': util_dt.datetime_to_local_tz_str(
                    self.release_at),
                'flg_beamtime_status': 'N',
                'beamtime_start_at': util_dt.datetime_to_local_tz_str(
                    self.begin_at + timedelta(1)),
                'beamtime_end_at': util_dt.datetime_to_local_tz_str(
                    self.end_at + timedelta(2)),
                'flg_proposal_system': 'U',
                'flg_available': 'true',
                'description': 'desc 01'
            }
        }

        expect = proposal[PROPOSAL]

        #
        # Create new entry (should succeed)
        #
        received = self.__create_entry_api(proposal, expect)

        proposal_id = received['id']
        prop_number = received['number']

        #
        # Create duplicated entry (should throw an error)
        #
        self.__create_error_entry_uk_api(proposal)

        #
        # Get entry by number
        #
        self.__get_all_entries_by_number_api(prop_number, expect)

        #
        # Get entry by ID
        #
        self.__get_entry_by_id_api(proposal_id, expect)

        #
        # Put entry information (update some fields should succeed)
        #
        self.__update_entry_api(proposal_id, prop_number, expect)

        #
        # Delete entry (should succeed)
        # (test purposes only to keep the DB clean)
        #
        self.__delete_entry_by_id_api(proposal_id)

    def test_existing_proposal_api(self):
        proposal_2 = {
            PROPOSAL: {
                'id': -2,
                'number': 900061,
                'title': 'DO NOT DELETE - CONTROLS TEST PROPOSAL 900061',
                'abstract': '',
                'url': 'https://www.xfel.eu/cas_robot_framework_test',
                'instrument_id': '1',
                'instrument_identifier': 'SPB',
                'instrument_cycle_id': '-1',
                'principal_investigator_id': '-7',
                'main_proposer_id': '-7',
                'orig_repository_id': -1,
                # 'begin_at': util_dt.datetime_to_local_tz_str(self.begin_at),
                # 'end_at': util_dt.datetime_to_local_tz_str(self.end_at),
                # 'release_at': util_dt.datetime_to_local_tz_str(
                #     self.release_at),
                'flg_beamtime_status': 'R',
                # 'beamtime_start_at': util_dt.datetime_to_local_tz_str(
                #     self.begin_at + timedelta(1)),
                # 'beamtime_end_at': util_dt.datetime_to_local_tz_str(
                #     self.end_at + timedelta(2)),
                'flg_proposal_system': 'L',
                'flg_available': 'true',
                'description': '...'
            }
        }

        expect = proposal_2[PROPOSAL]
        prop_number = expect['number']

        #
        # Get entry by number
        #
        self.__get_proposal_by_number_api(prop_number, expect)

        #
        # Get entry by number DAQ Info
        #
        self.__get_proposal_by_number_daq_info_api(prop_number, expect)

    #
    # fields_validation
    #
    def fields_validation(self, receive, expect):
        self.assert_eq_hfield(receive, expect, 'number', NUMBER)
        self.assert_eq_hfield(receive, expect, 'title', STRING)
        self.assert_eq_hfield(receive, expect, 'abstract', STRING)
        self.assert_eq_hfield(receive, expect, 'url', STRING)
        self.assert_eq_hfield(receive, expect, 'instrument_id', NUMBER)
        self.assert_eq_hfield(receive, expect, 'instrument_identifier', STRING)
        self.assert_eq_hfield(receive, expect, 'instrument_cycle_id', NUMBER)
        self.assert_eq_hfield(receive, expect,
                              'principal_investigator_id', NUMBER)
        self.assert_eq_hfield(receive, expect, 'main_proposer_id', NUMBER)
        self.assert_eq_hfield(receive, expect, 'begin_at', DATETIME)
        self.assert_eq_hfield(receive, expect, 'end_at', DATETIME)
        # self.assert_eq_hfield(receive, expect, 'release_at', DATETIME)

        self.assert_eq_hfield(receive, expect, 'flg_beamtime_status', STRING)
        # self.assert_eq_hfield(receive, expect, 'beamtime_start_at', DATETIME)
        # self.assert_eq_hfield(receive, expect, 'beamtime_end_at', DATETIME)

        self.assert_eq_hfield(receive, expect, 'flg_proposal_system', STRING)

        self.assert_eq_hfield(receive, expect, 'flg_available', BOOLEAN)
        self.assert_eq_hfield(receive, expect, 'description', STRING)

        #
        # Validate "generated" fields
        expect['proposal_folder'] = 'p{0:06d}'.format(expect['number'])
        self.assert_eq_hfield(receive, expect, 'proposal_folder', STRING)

    #
    # Internal private APIs methods
    #
    def __create_entry_api(self, entry_info, expect):
        response = self.client_api.create_proposal_api(entry_info)
        receive = self.get_and_validate_create_entry(response)
        self.fields_validation(receive, expect)

        return receive

    def __create_error_entry_uk_api(self, entry_info):
        response = self.client_api.create_proposal_api(entry_info)
        resp_content = self.load_response_content(response)

        receive = resp_content
        expect = {'info': {'def_proposal_path': ['has already been taken'],
                           'number': ['has already been taken'],
                           'proposal_folder': ['has already been taken'],
                           'url': ['has already been taken']}}

        self.assertEqual(receive, expect, "Expected result not received")
        self.assert_eq_status_code(response.status_code, UNPROCESSABLE_ENTITY)

        # 'has already been taken'
        receive_msg = receive['info']['number'][0]
        expect_msg = expect['info']['number'][0]
        self.assert_eq_str(receive_msg, expect_msg)

    def __update_entry_api(self, entry_id, prop_number, expect):
        __end_at_upd = self.end_at + timedelta(1)
        __release_at_upd = self.release_at + timedelta(1)

        proposal_upd = {
            PROPOSAL: {
                'number': prop_number,  # Cannot be updated
                'title': 'this is the title',  # Cannot be updated
                'abstract': 'this is the updated abstract!',
                'url': 'https://in.xfel.eu/upex/proposal/102xxxxxxxx',
                'instrument_id': '2',
                'instrument_identifier': 'FXE',
                'instrument_cycle_id': '-1',
                'principal_investigator_id': '-1',
                'main_proposer_id': '-1',
                # 'begin_at' can't be updated
                'begin_at': util_dt.datetime_to_local_tz_str(self.begin_at),
                'end_at': util_dt.datetime_to_local_tz_str(__end_at_upd),
                'release_at': util_dt.datetime_to_local_tz_str(
                    self.release_at),
                'flg_beamtime_status': 'T',
                'beamtime_start_at': util_dt.datetime_to_local_tz_str(
                    self.begin_at + timedelta(1)),
                'beamtime_end_at': util_dt.datetime_to_local_tz_str(
                    self.end_at + timedelta(2)),
                'flg_proposal_system': 'U',  # Cannot be updated
                'flg_available': 'false',
                'description': 'desc 01 updated!!!'
            }
        }

        # Deleting keys not allowed on the update!
        # {'info': {'beamtime_end_at': ['cannot be updated'],
        #           'beamtime_start_at': ['cannot be updated'],
        #           'release_at': ['cannot be updated']}}
        prop_upd_request = proposal_upd.copy()
        del prop_upd_request['proposal']['release_at']
        del prop_upd_request['proposal']['beamtime_start_at']
        del prop_upd_request['proposal']['beamtime_end_at']

        res = self.client_api.update_proposal_api(entry_id, prop_upd_request)
        receive = self.load_response_content(res)

        #
        expect_upd = proposal_upd[PROPOSAL]

        self.fields_validation(receive, expect_upd)
        self.assert_eq_status_code(res.status_code, OK)

        # This field cannot be updated
        field = 'number'
        self.assert_eq_str(expect[field], expect_upd[field])
        field = 'title'
        self.assert_eq_str(expect[field], expect_upd[field])
        field = 'begin_at'
        self.assert_eq_str(expect[field], expect_upd[field])
        field = 'flg_proposal_system'
        self.assert_eq_str(expect[field], expect_upd[field])

        # This fields were successfully updated
        field = 'url'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'abstract'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'instrument_id'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'instrument_cycle_id'
        self.assert_eq_str(expect[field], expect_upd[field])
        field = 'principal_investigator_id'
        self.assert_eq_str(expect[field], expect_upd[field])
        field = 'main_proposer_id'
        self.assert_eq_str(expect[field], expect_upd[field])
        field = 'end_at'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        # field = 'release_at'
        # self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'flg_beamtime_status'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        # field = 'beamtime_start_at'
        # self.assert_not_eq_str(expect[field], expect_upd[field], field)
        # field = 'beamtime_end_at'
        # self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'flg_available'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'description'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)

    def __get_all_entries_by_number_api(self, number, expect,
                                        page=DEF_PAGE,
                                        page_size=DEF_PAGE_SIZE):
        resp = self.client_api.get_all_proposals_by_number_api(number,
                                                               page, page_size)
        receive = self.get_and_validate_all_entries_by_name(resp)
        self.fields_validation(receive, expect)

    def __get_proposal_by_number_api(self, number, expect):
        response = self.client_api.get_proposal_by_number_api(number)
        receive = self.get_and_validate_entry_by_id(response)

        # Fix this values because they depend on the moment the tests are run!
        expect['begin_at'] = receive['begin_at']
        expect['end_at'] = receive['end_at']
        expect['description'] = receive['description']

        self.fields_validation(receive, expect)

    def __get_proposal_by_number_daq_info_api(self, number, expect):
        resp = self.client_api.get_proposal_by_number_daq_info_api(number)
        receive = self.get_and_validate_entry_by_id(resp)

        # Fix this values because they depend on the moment the tests are run!
        expect['begin_at'] = receive['begin_at']
        expect['end_at'] = receive['end_at']
        expect['description'] = receive['description']

        self.fields_validation(receive, expect)

    def __get_entry_by_id_api(self, entry_id, expect):
        response = self.client_api.get_proposal_by_id_api(entry_id)
        receive = self.get_and_validate_entry_by_id(response)
        self.fields_validation(receive, expect)

    def __delete_entry_by_id_api(self, entry_id):
        response = self.client_api.delete_proposal_api(entry_id)
        self.get_and_validate_delete_entry_by_id(response)


if __name__ == '__main__':
    unittest.main()
