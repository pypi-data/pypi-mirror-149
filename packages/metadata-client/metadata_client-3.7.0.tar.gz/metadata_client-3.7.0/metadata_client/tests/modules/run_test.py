"""RunTest class"""

import unittest

from metadata_client.metadata_client import MetadataClient
from .module_base import ModuleBase
from ..common.config_test import *
from ..common.generators import Generators
from ..common.secrets import *
from ...modules.run import Run

MODULE_NAME = RUN


class RunTest(ModuleBase, unittest.TestCase):
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

        __unique_run_id_1 = Generators.generate_unique_id()
        self.run_01 = {
            'run_number': __unique_run_id_1,
            'run_alias': None,
            'experiment_id': '-1',
            'sample_id': '-1',
            'begin_at': '2014-06-25T08:30:00.000+02:00',
            'end_at': '2015-06-25T08:30:00.000+02:00',
            'first_train': 100,
            'last_train': 100,
            'flg_available': 'true',
            'flg_status': '1',
            'original_format': 'format',
            'system_msg': 'system msg',
            'description': 'desc 01'
        }

        self.run_01_upd = {
            'run_number': __unique_run_id_1,  # This field cannot be updated
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

    def test_create_run(self):
        run_01 = Run(
            metadata_client=self.mdc_client,
            run_number=self.run_01['run_number'],
            run_alias=self.run_01['run_alias'],
            experiment_id=self.run_01['experiment_id'],
            sample_id=self.run_01['sample_id'],
            begin_at=self.run_01['begin_at'],
            end_at=self.run_01['end_at'],
            first_train=self.run_01['first_train'],
            last_train=self.run_01['last_train'],
            flg_available=self.run_01['flg_available'],
            flg_status=self.run_01['flg_status'],
            original_format=self.run_01['original_format'],
            system_msg=self.run_01['system_msg'],
            description=self.run_01['description'])

        #
        # Create new entry (should succeed)
        #
        result1 = run_01.create()

        run_folder = '{0:04d}'.format(self.run_01['run_number'])
        self.run_01['run_alias'] = 'p000000.r{0}.e0001'.format(run_folder)
        self.assert_create_success(MODULE_NAME, result1, self.run_01)

        run = result1['data']
        run_id = result1['data']['id']
        run_number = result1['data']['run_number']
        experiment_id = result1['data']['experiment_id']

        #
        # Validate "generated" fields
        self.assertEqual(int(result1['data']['run_folder'][1:]), run_number)

        #
        # Create duplicated entry (should throw an error)
        #
        run_01_dup = run_01
        result2 = run_01_dup.create()
        expect_app_info = {'run_number': ['must be unique per proposal',
                                          'has already been taken']}
        self.assert_create_error(MODULE_NAME, result2, expect_app_info)

        #
        # Get entry by run_number
        #
        result3 = Run.get_by_run_number_and_experiment_id(self.mdc_client,
                                                          run_number,
                                                          experiment_id)
        self.assert_find_success(MODULE_NAME, result3, self.run_01)

        #
        # Get entry by ID
        #
        result4 = Run.get_by_id(self.mdc_client, run_id)
        self.assert_find_success(MODULE_NAME, result4, self.run_01)

        #
        # Get entry with non-existent ID (should throw an error)
        #
        result5 = Run.get_by_id(self.mdc_client, -666)
        self.assert_find_error(MODULE_NAME, result5, RESOURCE_NOT_FOUND)

        #
        # Put entry information (update some fields should succeed)
        #
        run_01.run_number = self.run_01_upd['run_number']
        run_01.run_alias = self.run_01_upd['run_alias']
        run_01.experiment_id = self.run_01_upd['experiment_id']
        run_01.sample_id = self.run_01_upd['sample_id']
        run_01.begin_at = self.run_01_upd['begin_at']
        run_01.end_at = self.run_01_upd['end_at']
        run_01.first_train = self.run_01_upd['first_train']
        run_01.last_train = self.run_01_upd['last_train']
        run_01.flg_available = self.run_01_upd['flg_available']
        run_01.flg_status = self.run_01_upd['flg_status']
        run_01.original_format = self.run_01_upd['original_format']
        run_01.system_msg = self.run_01_upd['system_msg']
        run_01.description = self.run_01_upd['description']
        result6 = run_01.update()
        self.assert_update_success(MODULE_NAME, result6, self.run_01_upd)

        #
        # Put entry information (update some fields should throw an error)
        #
        run_01.run_number = '__THIS_NAME_IS_1_CHARACTERS_LONGER_THAN_THE_ALLOWED_MAX_NUM__'  # noqa
        run_01.flg_available = self.run_01_upd['flg_available']
        run_01.description = self.run_01_upd['description']
        result7 = run_01.update()
        expect_app_info = {'run_number': ['cannot be updated',
                                          'is not a number']}
        self.assert_update_error(MODULE_NAME, result7, expect_app_info)

        #
        # Delete entry (should succeed)
        # (test purposes only to keep the DB clean)
        #
        result8 = run_01.delete()
        self.assert_delete_success(MODULE_NAME, result8)

        #
        # Delete entry (should throw an error)
        # (test purposes only to keep the DB clean)
        #
        result9 = run_01.delete()
        self.assert_delete_error(MODULE_NAME, result9, RESOURCE_NOT_FOUND)

    def test_create_run_from_dict(self):
        #
        # Create new entry (should succeed)
        #
        result1 = Run.create_from_dict(self.mdc_client, self.run_01)

        run_folder = '{0:04d}'.format(self.run_01['run_number'])
        self.run_01['run_alias'] = 'p000000.r{0}.e0001'.format(run_folder)
        self.assert_create_success(MODULE_NAME, result1, self.run_01)

        run = result1['data']
        run_id = run['id']

        #
        # Create duplicated entry (should throw an error)
        #
        result2 = Run.create_from_dict(self.mdc_client, self.run_01)
        expect_app_info = {'run_number': ['must be unique per proposal',
                                          'has already been taken']}
        self.assert_create_error(MODULE_NAME, result2, expect_app_info)

        #
        # Update entry (should succeed)
        #
        result3 = Run.update_from_dict(self.mdc_client,
                                       run_id,
                                       self.run_01_upd)
        self.assert_update_success(MODULE_NAME, result3, self.run_01_upd)

        #
        # Incomplete (non mandatory) update entry (should succeed)
        #
        run_02_upd = {
            'first_train': '100',
            'last_train': '101',
            'flg_available': 'true'
        }

        result4 = Run.update_from_dict(self.mdc_client,
                                       run_id,
                                       run_02_upd)

        exp_run_02_upd = {
            'run_number': self.run_01_upd['run_number'],
            'run_alias': self.run_01_upd['run_alias'],
            'experiment_id': self.run_01_upd['experiment_id'],
            'sample_id': self.run_01_upd['sample_id'],
            'begin_at': self.run_01_upd['begin_at'],
            'end_at': self.run_01_upd['end_at'],
            'first_train': '100',
            'last_train': '101',
            'flg_available': 'true',
            'flg_status': self.run_01_upd['flg_status'],
            'original_format': self.run_01_upd['original_format'],
            'system_msg': self.run_01_upd['system_msg'],
            'description': self.run_01_upd['description'],
        }

        self.assert_update_success(MODULE_NAME, result4, exp_run_02_upd)

        #
        # Delete entry (should succeed)
        # (test purposes only to keep the DB clean)
        #
        result8 = Run.delete_by_id(self.mdc_client, run_id)
        self.assert_delete_success(MODULE_NAME, result8)

        #
        # Delete entry (should throw an error)
        # (test purposes only to keep the DB clean)
        #
        result9 = Run.delete_by_id(self.mdc_client, run_id)
        self.assert_delete_error(MODULE_NAME, result9, RESOURCE_NOT_FOUND)

    #
    # fields_validation
    #
    def fields_validation(self, receive, expect):
        self.assert_eq_hfield(receive, expect, 'run_number', NUMBER)
        self.assert_eq_hfield(receive, expect, 'run_alias', STRING)
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


if __name__ == '__main__':
    unittest.main()
