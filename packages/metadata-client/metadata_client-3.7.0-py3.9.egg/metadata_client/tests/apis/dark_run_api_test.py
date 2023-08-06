"""DarkRunApiTest class"""

import unittest

from metadata_client import MetadataClient
from .api_base import ApiBase
from ..common.config_test import *
from ..common.generators import Generators
from ..common.secrets import *


class DarkRunApiTest(ApiBase, unittest.TestCase):
    client_api = MetadataClient(
        client_id=CLIENT_OAUTH2_INFO['CLIENT_ID'],
        client_secret=CLIENT_OAUTH2_INFO['CLIENT_SECRET'],
        token_url=CLIENT_OAUTH2_INFO['TOKEN_URL'],
        refresh_url=CLIENT_OAUTH2_INFO['REFRESH_URL'],
        auth_url=CLIENT_OAUTH2_INFO['AUTH_URL'],
        scope=CLIENT_OAUTH2_INFO['SCOPE'],
        user_email=CLIENT_OAUTH2_INFO['EMAIL'],
        base_api_url=BASE_API_URL)

    def test_create_dark_run_api(self):
        __unique_name = Generators.generate_unique_name('DarkRunApi')
        __unique_identifier = Generators.generate_unique_identifier()
        dark_run = {
            'dark_run': {
                'proposal_id': -1,
                'detector_id': -2,
                'detector_identifier': 'TEST_DET_CI-11 - DO NOT DELETE!',
                'detector_type_id': -1,
                'pdu_physical_names':
                    '["PDU-3_DO_NOT_DELETE", "PDU-2_DO_NOT_DELETE"]',
                'runs_info': str([1]),
                'operation_mode_id': -1,
                'operation_mode_identifier': 'Operation_identifier-11',
                'operation_mode_name': 'Operation Mode 1 - DO NOT DELETE!',
                'flg_status': 'R',
                # 'pdu_karabo_das': ['t1', 't2'],
                'size': '',
                'report_url': '',
                'input_path': '',
                'output_path': '',
                'calcat_feedback': '',
                'description': 'desc default1'
            }
        }

        expect = dark_run['dark_run']

        dark_run_id = -11
        dark_run_proposal_id = -1

        #
        # Get entry by proposal_id
        #
        self.__get_all_entries_by_proposal_id_api(dark_run_proposal_id,
                                                  dark_run['dark_run'])

        #
        # Get entry by ID
        #
        self.__get_entry_by_id_api(dark_run_id, dark_run['dark_run'])

    #
    # fields_validation
    #
    def fields_validation(self, receive, expect):
        self.assert_eq_hfield(receive, expect, 'proposal_id', STRING)
        self.assert_eq_hfield(receive, expect, 'detector_id', STRING)
        self.assert_eq_hfield(receive, expect, 'detector_identifier', STRING)
        self.assert_eq_hfield(receive, expect, 'detector_type_id', STRING)
        self.assert_eq_hfield(receive, expect, 'pdu_physical_names', STRING)
        self.assert_eq_hfield(receive, expect, 'runs_info', STRING),
        self.assert_eq_hfield(receive, expect, 'operation_mode_id', STRING),
        self.assert_eq_hfield(receive, expect, 'operation_mode_name', STRING)
        self.assert_eq_hfield(receive, expect, 'flg_status', STRING)
        # self.assert_eq_hfield(receive, expect, 'pdu_karabo_das', STRING)
        self.assert_eq_hfield(receive, expect,
                              'operation_mode_identifier', STRING)
        self.assert_eq_hfield(receive, expect, 'size', STRING)
        self.assert_eq_hfield(receive, expect, 'report_url', STRING)
        self.assert_eq_hfield(receive, expect, 'input_path', STRING)
        self.assert_eq_hfield(receive, expect, 'output_path', STRING)
        self.assert_eq_hfield(receive, expect, 'calcat_feedback', STRING)
        self.assert_eq_hfield(receive, expect, 'description', STRING)
        self.assert_eq_hfield(receive, expect, 'description', STRING)

    #
    # Internal private APIs methods
    #
    def __get_all_entries_by_proposal_id_api(self, proposal_id, expect):
        response = self.client_api.get_all_dark_runs_by_proposal_id_api(
            proposal_id)
        receive = self.get_and_validate_all_entries_by_name(response)
        self.fields_validation(receive, expect)

    def __get_entry_by_id_api(self, entry_id, expect):
        response = self.client_api.get_dark_run_by_id_api(entry_id)
        receive = self.get_and_validate_entry_by_id(response)
        self.fields_validation(receive, expect)


if __name__ == '__main__':
    unittest.main()
