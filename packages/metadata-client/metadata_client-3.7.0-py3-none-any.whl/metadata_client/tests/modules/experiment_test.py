"""ExperimentTest class"""

import unittest

from metadata_client.metadata_client import MetadataClient
from .module_base import ModuleBase
from ..common.config_test import *
from ..common.generators import Generators
from ..common.secrets import *
from ...modules.experiment import Experiment

MODULE_NAME = EXPERIMENT


class ExperimentTest(ModuleBase, unittest.TestCase):
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

        __unique_name1 = Generators.generate_unique_name('Experiment01')
        self.experiment_01 = {
            'name': __unique_name1,
            'experiment_type_id': '1',
            'proposal_id': '-1',
            'flg_available': 'true',
            'publisher': 'this is the publisher',
            'contributor': 'this is the contributor',
            'description': 'desc 01'
        }

        __unique_name_upd = Generators.generate_unique_name('ExperimentUpd1')
        self.exp_01_upd = {
            'name': __unique_name_upd,
            'doi': 'It is not possible to updated doi!',
            'experiment_type_id': '1',
            'proposal_id': '-1',
            'flg_available': 'false',
            'publisher': 'this is the updated publisher!',
            'contributor': 'this is the updated contributor!',
            'description': 'desc 01 updated!!!'
        }

    def test_create_experiment(self):
        exp_01 = Experiment(
            metadata_client=self.mdc_client,
            name=self.experiment_01['name'],
            experiment_type_id=self.experiment_01['experiment_type_id'],
            proposal_id=self.experiment_01['proposal_id'],
            flg_available=self.experiment_01['flg_available'],
            publisher=self.experiment_01['publisher'],
            contributor=self.experiment_01['contributor'],
            description=self.experiment_01['description'])

        #
        # Create new entry (should succeed)
        #
        result1 = exp_01.create()
        self.assert_create_success(MODULE_NAME, result1, self.experiment_01)

        experiment_id = result1['data']['id']
        experiment_name = result1['data']['name']
        proposal_id = result1['data']['proposal_id']
        exp_01.doi = result1['data']['doi']

        #
        # Create duplicated entry (should throw an error)
        #
        exp_01_dup = exp_01
        result2 = exp_01_dup.create()
        expect_app_info = {'name': ['has already been taken']}
        self.assert_create_error(MODULE_NAME, result2, expect_app_info)

        #
        # Get entry by name
        #
        result3 = Experiment.get_by_name_and_proposal_id(self.mdc_client,
                                                         experiment_name,
                                                         proposal_id)
        self.assert_find_success(MODULE_NAME, result3, self.experiment_01)

        #
        # Get entry by proposal_id
        #
        result32 = Experiment.get_all_by_proposal_id(self.mdc_client,
                                                     proposal_id)
        result32_redu = {'success': result32['success'],
                         'info': result32['info'],
                         'app_info': result32['app_info'],
                         'data': [result32['data'][1]]}
        self.assert_find_success(MODULE_NAME, result32_redu,
                                 [self.experiment_01])

        #
        # Get entry by ID
        #
        result4 = Experiment.get_by_id(self.mdc_client, experiment_id)
        self.assert_find_success(MODULE_NAME, result4, self.experiment_01)

        #
        # Get entry with non-existent ID (should throw an error)
        #
        result5 = Experiment.get_by_id(self.mdc_client, -666)
        self.assert_find_error(MODULE_NAME, result5, RESOURCE_NOT_FOUND)

        #
        # Put entry information (update some fields should succeed)
        #
        exp_01.name = self.exp_01_upd['name']
        exp_01.doi = self.exp_01_upd['doi']
        exp_01.experiment_type_id = self.exp_01_upd['experiment_type_id']
        exp_01.proposal_id = self.exp_01_upd['proposal_id']
        exp_01.flg_available = self.exp_01_upd['flg_available']
        exp_01.publisher = self.exp_01_upd['publisher']
        exp_01.contributor = self.exp_01_upd['contributor']
        exp_01.description = self.exp_01_upd['description']
        result6 = exp_01.update()
        self.assert_update_success(MODULE_NAME, result6, self.exp_01_upd)

        #
        # Put entry information (update some fields should throw an error)
        #
        exp_01.name = '__THIS_NAME_IS_1_CHARACTERS_LONGER_THAN_THE_ALLOWED_MAX_NUM__'  # noqa
        exp_01.doi = self.exp_01_upd['doi']
        exp_01.experiment_type_id = self.exp_01_upd['experiment_type_id']
        exp_01.proposal_id = self.exp_01_upd['proposal_id']
        exp_01.flg_available = self.exp_01_upd['flg_available']
        exp_01.publisher = self.exp_01_upd['publisher']
        exp_01.contributor = self.exp_01_upd['contributor']
        exp_01.description = self.exp_01_upd['description']
        result7 = exp_01.update()
        expect_app_info = {'name': ['is too long (maximum is 60 characters)']}
        self.assert_update_error(MODULE_NAME, result7, expect_app_info)

        #
        # Delete entry (should succeed)
        # (test purposes only to keep the DB clean)
        #
        result8 = exp_01.delete()
        self.assert_delete_success(MODULE_NAME, result8)

        #
        # Delete entry (should throw an error)
        # (test purposes only to keep the DB clean)
        #
        result9 = exp_01.delete()
        self.assert_delete_error(MODULE_NAME, result9, RESOURCE_NOT_FOUND)

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


if __name__ == '__main__':
    unittest.main()
