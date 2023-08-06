"""DarkRunTest class"""

import unittest

from metadata_client.metadata_client import MetadataClient
from .module_base import ModuleBase
from ..common.config_test import *
from ..common.secrets import *
from ...modules.dark_run import DarkRun

MODULE_NAME = DARK_RUN


class DarkRunTest(ModuleBase, unittest.TestCase):
    def setUp(self):
        self.mdc_client = MetadataClient(
            client_id=CLIENT_OAUTH2_INFO['CLIENT_ID'],
            client_secret=CLIENT_OAUTH2_INFO['CLIENT_SECRET'],
            token_url=CLIENT_OAUTH2_INFO['TOKEN_URL'],
            refresh_url=CLIENT_OAUTH2_INFO['REFRESH_URL'],
            auth_url=CLIENT_OAUTH2_INFO['AUTH_URL'],
            scope=CLIENT_OAUTH2_INFO['SCOPE'],
            user_email=CLIENT_OAUTH2_INFO['EMAIL'],
            base_api_url=BASE_API_URL
        )

        self.dark_1 = {
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
            'pdu_karabo_das': ['t1', 't2'],
            'size': '',
            'report_url': '',
            'input_path': '',
            'output_path': '',
            'calcat_feedback': '',
            'description': 'desc default1'
        }

        self.dark_01_orig = {
            # Fix values
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
            'pdu_karabo_das': ['t1', 't2'],

            # UPDATED FIELDS!
            'flg_status': 'R',
            'size': '',
            'report_url': '',
            'input_path': '',
            'output_path': '',
            'calcat_feedback': '',
            'description': 'desc default1'
        }

        self.dark_01_upd = {
            # Fix values
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
            'pdu_karabo_das': ['t1', 't2'],

            # UPDATED FIELDS!
            'flg_status': 'F',
            'size': '1,5Gb',
            'report_url': 'https://www.new_example.com:123#report_UPDATED',
            'input_path': '/this/is/input/path/UPDATED',
            'output_path': '/this/is/output/path/UPDATED',
            'calcat_feedback': 'This dark run performed with success UPD!',
            'description': 'desc 01 UPDATED!!!'
        }

    def test_create_dark_run(self):
        dark_run_01 = DarkRun(
            metadata_client=self.mdc_client,
            proposal_id=self.dark_1['proposal_id'],
            detector_id=self.dark_1['detector_id'],
            detector_identifier=self.dark_1['detector_identifier'],
            detector_type_id=self.dark_1['detector_type_id'],
            pdu_physical_names=self.dark_1['pdu_physical_names'],
            runs_info=self.dark_1['runs_info'],
            operation_mode_id=self.dark_1['operation_mode_id'],
            operation_mode_identifier=self.dark_1['operation_mode_identifier'],
            operation_mode_name=self.dark_1['operation_mode_name'],
            flg_status=self.dark_1['flg_status'],
            pdu_karabo_das=self.dark_1['pdu_karabo_das'],
            size=self.dark_1['size'],
            report_url=self.dark_1['report_url'],
            input_path=self.dark_1['input_path'],
            output_path=self.dark_1['output_path'],
            calcat_feedback=self.dark_1['calcat_feedback'],
            description=self.dark_1['description'])

        #
        dark_run_id = -11
        dark_run_proposal_id = -1

        #
        # Get entry by proposal_id
        #
        res3 = DarkRun.get_all_dark_runs_by_proposal_id(
            self.mdc_client, dark_run_proposal_id,
            page=DEF_PAGE, page_size=DEF_PAGE_SIZE)

        self.assertEqual(res3['success'], True)
        self.assertEqual(res3['info'], 'Got dark_run successfully')
        self.assertIn('\'proposal_id\': -1', str(res3['data']))
        self.assertIn('\'operation_mode_id\': -1', str(res3['data']))
        self.assertIn('\'detector_id\': -2', str(res3['data']))

        #
        # Get entry by ID
        #
        result4 = DarkRun.get_by_id(self.mdc_client, dark_run_id)
        self.assert_find_success(MODULE_NAME, result4, self.dark_1)

        dark_run_01.id = result4['data']['id']

        #
        # Get entry with non-existent ID (should throw an error)
        #
        result5 = DarkRun.get_by_id(self.mdc_client, -666)
        self.assert_find_error(MODULE_NAME, result5, RESOURCE_NOT_FOUND)

        #
        # Put entry information (update some fields should succeed)
        #
        dark_run_01.flg_status = self.dark_01_upd['flg_status']
        dark_run_01.size = self.dark_01_upd['size']
        dark_run_01.report_url = self.dark_01_upd['report_url']
        dark_run_01.input_path = self.dark_01_upd['input_path']
        dark_run_01.output_path = self.dark_01_upd['output_path']
        dark_run_01.calcat_feedback = self.dark_01_upd['calcat_feedback']
        dark_run_01.description = self.dark_01_upd['description']
        result6 = dark_run_01.update()
        self.assert_update_success(MODULE_NAME, result6, self.dark_01_upd)

        #
        # Put entry information (update some fields should succeed)
        #
        dark_run_01.flg_status = self.dark_01_orig['flg_status']
        dark_run_01.size = self.dark_01_orig['size']
        dark_run_01.report_url = self.dark_01_orig['report_url']
        dark_run_01.input_path = self.dark_01_orig['input_path']
        dark_run_01.output_path = self.dark_01_orig['output_path']
        dark_run_01.calcat_feedback = self.dark_01_orig['calcat_feedback']
        dark_run_01.description = self.dark_01_orig['description']
        result6b = dark_run_01.update()
        self.assert_update_success(MODULE_NAME, result6b, self.dark_01_orig)

        #
        # Put entry information (update some fields should throw an error)
        #
        dark_run_01.report_url = '#' * 251  # String with length of 251
        dark_run_01.description = self.dark_01_upd['description']
        result7 = dark_run_01.update()
        expect_app_info = {
            'report_url': ['URL length allows only 250 characters']}
        self.assert_update_error(MODULE_NAME, result7, expect_app_info)

    #
    # fields_validation
    #
    def fields_validation(self, receive, expect):
        self.assert_eq_hfield(receive, expect, 'proposal_id', STRING)
        self.assert_eq_hfield(receive, expect, 'detector_id', STRING)
        self.assert_eq_hfield(receive, expect, 'detector_identifier', STRING)
        self.assert_eq_hfield(receive, expect, 'detector_type_id', STRING)
        self.assert_eq_hfield(receive, expect, 'pdu_physical_names', STRING)
        self.assert_eq_hfield(receive, expect, 'runs_info', STRING)
        self.assert_eq_hfield(receive, expect, 'operation_mode_id', STRING)
        self.assert_eq_hfield(receive, expect, 'operation_mode_identifier',
                              STRING)
        self.assert_eq_hfield(receive, expect, 'operation_mode_name', STRING)
        self.assert_eq_hfield(receive, expect, 'flg_status', STRING)
        # self.assert_eq_hfield(receive, expect, 'pdu_karabo_das', STRING)
        self.assert_eq_hfield(receive, expect, 'size', STRING)
        self.assert_eq_hfield(receive, expect, 'report_url', STRING)
        self.assert_eq_hfield(receive, expect, 'input_path', STRING)
        self.assert_eq_hfield(receive, expect, 'output_path', STRING)
        self.assert_eq_hfield(receive, expect, 'calcat_feedback', STRING)
        self.assert_eq_hfield(receive, expect, 'description', STRING)


if __name__ == '__main__':
    unittest.main()
