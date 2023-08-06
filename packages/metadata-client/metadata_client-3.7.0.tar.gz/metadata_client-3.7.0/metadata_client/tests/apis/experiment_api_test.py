"""ExperimentApiTest class"""

import unittest

from metadata_client import MetadataClient
from .api_base import ApiBase
from ..common.config_test import *
from ..common.generators import Generators
from ..common.secrets import *


class ExperimentApiTest(ApiBase, unittest.TestCase):
    client_api = MetadataClient(
        client_id=CLIENT_OAUTH2_INFO['CLIENT_ID'],
        client_secret=CLIENT_OAUTH2_INFO['CLIENT_SECRET'],
        token_url=CLIENT_OAUTH2_INFO['TOKEN_URL'],
        refresh_url=CLIENT_OAUTH2_INFO['REFRESH_URL'],
        auth_url=CLIENT_OAUTH2_INFO['AUTH_URL'],
        scope=CLIENT_OAUTH2_INFO['SCOPE'],
        user_email=CLIENT_OAUTH2_INFO['EMAIL'],
        base_api_url=BASE_API_URL)

    def test_create_experiment_api(self):
        __unique_name = Generators.generate_unique_name('ExperimentApi')
        experiment = {
            'experiment': {
                'name': __unique_name,
                'experiment_type_id': '1',
                'proposal_id': '-1',
                'flg_available': 'true',
                'publisher': 'this is the publisher',
                'contributor': 'this is the contributor',
                'description': 'desc 01'
            }
        }

        expect = experiment['experiment']

        #
        # Create new entry (should succeed)
        #
        received = self.__create_entry_api(experiment, expect)

        experiment_id = received['id']
        experiment_name = received['name']
        experiment_proposal_id = received['proposal_id']
        expect['doi'] = received['doi']

        #
        # Create duplicated entry (should throw an error)
        #
        self.__create_error_entry_uk_api(experiment)

        #
        # Get entry by name
        #
        self.__get_all_entries_by_name_api(experiment_name,
                                           experiment_proposal_id, expect)

        #
        # Get entry by ID
        #
        self.__get_entry_by_id_api(experiment_id, expect)

        #
        # Put entry information (update some fields should succeed)
        #
        self.__update_entry_api(experiment_id, expect)

        #
        # Delete entry (should succeed)
        # (test purposes only to keep the DB clean)
        #
        self.__delete_entry_by_id_api(experiment_id)

    #
    # fields_validation
    #
    def fields_validation(self, receive, expect):
        self.assert_eq_hfield(receive, expect, 'name', STRING)
        self.assert_eq_hfield(receive, expect, 'experiment_type_id', NUMBER)
        self.assert_eq_hfield(receive, expect, 'proposal_id', NUMBER)
        self.assert_eq_hfield(receive, expect, 'flg_available', BOOLEAN)
        self.assert_eq_hfield(receive, expect, 'publisher', STRING)
        self.assert_eq_hfield(receive, expect, 'contributor', STRING)
        self.assert_eq_hfield(receive, expect, 'description', STRING)

        #
        # Validate "generated" fields
        expected_doi = {'doi': 'xfel.mdc.exp.{0}'.format(receive['id'])}
        self.assert_eq_hfield(receive, expected_doi, 'doi', STRING)

        expected_folder = 'e{0:04d}'.format(receive['experiment_number'])
        expect['experiment_folder'] = expected_folder
        self.assert_eq_hfield(receive, expect, 'experiment_folder', STRING)

    #
    # Internal private APIs methods
    #
    def __create_entry_api(self, entry_info, expect):
        response = self.client_api.create_experiment_api(entry_info)
        receive = self.get_and_validate_create_entry(response)
        self.fields_validation(receive, expect)
        return receive

    def __create_error_entry_uk_api(self, entry_info):
        response = self.client_api.create_experiment_api(entry_info)
        resp_content = self.load_response_content(response)

        receive = resp_content
        expect = {'info': {'name': ['has already been taken']}}

        self.assertEqual(receive, expect, "Expected result not received")
        self.assert_eq_status_code(response.status_code, UNPROCESSABLE_ENTITY)

        # 'has already been taken'
        receive_msg = receive['info']['name'][0]
        expect_msg = expect['info']['name'][0]
        self.assert_eq_str(receive_msg, expect_msg)

    def __update_entry_api(self, entry_id, expect):
        unique_name_upd = Generators.generate_unique_name('ExperimentApiUpd')
        experiment_upd = {
            'experiment': {
                'name': unique_name_upd,
                'doi': 'It is not possible to updated doi!',
                'experiment_type_id': '1',
                'proposal_id': '-1',
                'flg_available': 'false',
                'publisher': 'this is the updated publisher!',
                'contributor': 'this is the updated contributor!',
                'description': 'desc 01 updated!!!'
            }
        }

        response = self.client_api.update_experiment_api(
            entry_id,
            experiment_upd
        )

        resp_content = self.load_response_content(response)

        receive = resp_content
        expect_upd = experiment_upd['experiment']

        self.fields_validation(receive, expect_upd)
        self.assert_eq_status_code(response.status_code, OK)

        field = 'name'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'doi'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        self.assert_eq_str(expect[field], receive[field])
        field = 'experiment_type_id'
        self.assert_eq_str(expect[field], expect_upd[field])
        field = 'proposal_id'
        self.assert_eq_str(expect[field], expect_upd[field])
        field = 'flg_available'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'publisher'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'contributor'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)
        field = 'description'
        self.assert_not_eq_str(expect[field], expect_upd[field], field)

    def __get_all_entries_by_name_api(self, name, proposal_id, expect):
        resp = self.client_api. \
            get_all_experiments_by_name_and_proposal_id_api(name, proposal_id)
        receive = self.get_and_validate_all_entries_by_name(resp)
        self.fields_validation(receive, expect)

    def __get_entry_by_id_api(self, entry_id, expect):
        response = self.client_api.get_experiment_by_id_api(entry_id)
        receive = self.get_and_validate_entry_by_id(response)
        self.fields_validation(receive, expect)

    def __delete_entry_by_id_api(self, entry_id):
        response = self.client_api.delete_experiment_api(entry_id)
        self.get_and_validate_delete_entry_by_id(response)


if __name__ == '__main__':
    unittest.main()
