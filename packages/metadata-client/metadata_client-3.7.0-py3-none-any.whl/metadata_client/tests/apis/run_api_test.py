"""RunApiTest class"""

import unittest

from metadata_client import MetadataClient
from .api_base import ApiBase
from ..common.config_test import *
from ..common.generators import Generators
from ..common.secrets import *


class RunApiTest(ApiBase, unittest.TestCase):
    client_api = MetadataClient(
        client_id=CLIENT_OAUTH2_INFO['CLIENT_ID'],
        client_secret=CLIENT_OAUTH2_INFO['CLIENT_SECRET'],
        token_url=CLIENT_OAUTH2_INFO['TOKEN_URL'],
        refresh_url=CLIENT_OAUTH2_INFO['REFRESH_URL'],
        auth_url=CLIENT_OAUTH2_INFO['AUTH_URL'],
        scope=CLIENT_OAUTH2_INFO['SCOPE'],
        user_email=CLIENT_OAUTH2_INFO['EMAIL'],
        base_api_url=BASE_API_URL)

    def test_create_run_api(self):
        __unique_name = Generators.generate_unique_id()
        run = {
            RUN: {
                'run_number': __unique_name,
                'run_alias': 'Run_Alias',
                'experiment_id': '-1',
                'sample_id': '-1',
                'begin_at': '2014-05-25T08:30:00.000+02:00',
                'end_at': '2015-05-25T08:30:00.000+02:00',
                'first_train': '1',
                'last_train': '999',
                'flg_available': 'true',
                'flg_status': '1',
                'original_format': '',
                'system_msg': '',
                'description': 'desc 01'
            }
        }

        expect = run[RUN]

        #
        # Create new entry (should succeed)
        #
        received = self.__create_entry_api(run, expect)

        run_id = received['id']
        run_number = received['run_number']
        experiment_id = received['experiment_id']

        #
        # Create duplicated entry (should throw an error)
        #
        self.__create_error_entry_uk_api(run)

        #
        # Get entry by name
        #
        self.__get_all_entries_by_run_number_api(run_number, expect)

        #
        # Get all runs from proposal
        #
        self.__get_all_entries_by_proposal_number_api('000000', expect)

        #
        # Get entry by ID
        #
        self.__get_entry_by_id_api(run_id, expect)

        #
        # Get entry by run_number and experiment_id
        #
        self.__get_entry_by_run_number_and_experiment_id_api(run_number,
                                                             experiment_id,
                                                             expect)

        #
        # Put entry information (update some fields should succeed)
        #
        self.__update_entry_api(run_id, run_number, expect)

        #
        # Delete entry (should succeed)
        # (test purposes only to keep the DB clean)
        #
        self.__delete_entry_by_id_api(run_id)

    #
    # fields_validation
    #
    def fields_validation(self, receive, expect):
        self.assert_eq_hfield(receive, expect, 'run_number', NUMBER)
        # Commented, because this field should be set async.
        # self.assert_eq_hfield(receive, expect, 'run_alias', STRING)
        self.assert_eq_hfield(receive, expect, 'experiment_id', NUMBER)
        self.assert_eq_hfield(receive, expect, 'sample_id', NUMBER)
        self.assert_eq_hfield(receive, expect, 'begin_at', DATETIME)
        self.assert_eq_hfield(receive, expect, 'end_at', DATETIME)
        self.assert_eq_hfield(receive, expect, 'first_train', NUMBER)
        self.assert_eq_hfield(receive, expect, 'last_train', NUMBER)
        self.assert_eq_hfield(receive, expect, 'flg_available', BOOLEAN)
        self.assert_eq_hfield(receive, expect, 'flg_status', NUMBER)
        self.assert_eq_hfield(receive, expect, 'original_format', STRING)
        self.assert_eq_hfield(receive, expect, 'system_msg', STRING)
        self.assert_eq_hfield(receive, expect, 'description', STRING)

        #
        # Validate "generated" fields
        expect['run_folder'] = 'r{0:04d}'.format(expect['run_number'])
        self.assert_eq_hfield(receive, expect, 'run_folder', STRING)

    #
    # Internal private APIs methods
    #
    def __create_entry_api(self, entry_info, expect):
        response = self.client_api.create_run_api(entry_info)
        receive = self.get_and_validate_create_entry(response)
        self.fields_validation(receive, expect)

        return receive

    def __create_error_entry_uk_api(self, entry_info):
        response = self.client_api.create_run_api(entry_info)
        resp_content = self.load_response_content(response)

        receive = resp_content
        expect = {'info': {'experiment_id': ['has already been taken'],
                           'run_number': ['must be unique per proposal',
                                          'has already been taken']}}

        self.assertEqual(receive, expect, "Expected result not received")
        self.assert_eq_status_code(response.status_code, UNPROCESSABLE_ENTITY)

        # 'has already been taken'
        receive_msg = receive['info']['run_number'][0]
        expect_msg = expect['info']['run_number'][0]
        self.assert_eq_str(receive_msg, expect_msg)

    def __update_entry_api(self, entry_id, run_number, expect):
        run_upd = {
            RUN: {
                'run_number': run_number,  # This field cannot be updated
                'run_alias': 'Run_Alias_Updated...',
                'experiment_id': '-1',
                'sample_id': '-1',
                'begin_at': '2014-06-25T08:30:00.000+02:00',
                'end_at': '2015-06-25T08:30:00.000+02:00',
                'first_train': 9223372036854775802,
                'last_train': 9223372036854775807,
                'flg_available': 'false',
                'flg_status': '-1',
                'original_format': 'format updated',
                'system_msg': 'system msg update',
                'description': 'desc 01 updated!!!'
            }
        }

        res = self.client_api.update_run_api(entry_id, run_upd)
        resp_content = self.load_response_content(res)

        receive = resp_content

        # Add runs not send to the update API
        run_upd[RUN]['unit_id'] = '-1'
        expect_upd = run_upd[RUN]

        self.fields_validation(receive, expect_upd)
        self.assert_eq_status_code(res.status_code, OK)

        # This field cannot be updated
        field = 'run_number'
        self.assert_eq_str(expect[field], expect_upd[field])

        field = 'run_alias'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'begin_at'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'end_at'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'first_train'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'last_train'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'flg_available'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'flg_status'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'original_format'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'system_msg'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'description'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)

    def __get_all_entries_by_run_number_api(self, run_number, expect):
        response = self.client_api.get_all_runs_by_run_number_api(
            run_number, page=DEF_PAGE, page_size=10)
        receive = self.get_and_validate_all_entries_by_name(response)
        self.fields_validation(receive, expect)

    def __get_all_entries_by_proposal_number_api(self, prop_number, expect):
        resp = self.client_api.get_all_runs_by_proposal_number_api(
            prop_number, page=DEF_PAGE, page_size=10)
        receive = self.get_and_validate_all_entries_by_name(resp)
        self.fields_validation(receive, expect)

    def __get_entry_by_run_number_and_experiment_id_api(self,
                                                        run_number,
                                                        experiment_id,
                                                        expect):
        response = self.client_api.get_run_by_run_number_and_experiment_id_api(
            run_number,
            experiment_id)
        receive = self.get_and_validate_all_entries_by_name(response)
        self.fields_validation(receive, expect)

    def __get_entry_by_id_api(self, entry_id, expect):
        response = self.client_api.get_run_by_id_api(entry_id)
        receive = self.get_and_validate_entry_by_id(response)
        self.fields_validation(receive, expect)

    def __delete_entry_by_id_api(self, entry_id):
        response = self.client_api.delete_run_api(entry_id)
        self.get_and_validate_delete_entry_by_id(response)


if __name__ == '__main__':
    unittest.main()
