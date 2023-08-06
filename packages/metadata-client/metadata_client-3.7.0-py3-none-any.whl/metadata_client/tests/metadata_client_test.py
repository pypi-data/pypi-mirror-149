"""MetadataClientTest class"""

import logging
import unittest

from metadata_client.metadata_client import MetadataClient
from .common.config_test import *
from .common.secrets import *
from .modules.module_base import ModuleBase


class MetadataClientTest(ModuleBase, unittest.TestCase):
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

    def test_get_data_group_types(self):
        resp = self.mdc_client.get_all_data_group_types(page=DEF_PAGE,
                                                        page_size=1)

        # Logging information
        logging.error('resp: {0}'.format(resp))

        #
        # RESPONSE example
        #
        # resp = {'info': 'Got data_group_type successfully',
        #         'data': [
        #             {'flg_available': True, 'id': 1, 'identifier': 'RAW',
        #              'name': 'Raw', 'description': ''},
        #             {'flg_available': True, 'id': 2, 'identifier': 'CAL',
        #              'name': 'Calibration', 'description': ''},
        #             {'flg_available': True, 'id': 3, 'identifier': 'PROC',
        #              'name': 'Processed', 'description': ''},
        #             {'flg_available': True, 'id': 4, 'identifier': 'REDU',
        #              'name': 'Reduced', 'description': ''},
        #             {'flg_available': True, 'id': 5, 'identifier': 'SIM',
        #              'name': 'Simulation', 'description': ''},
        #             {'flg_available': True, 'id': 6, 'identifier': 'UNK',
        #              'name': 'Unknown', 'description': ''}],
        #         'app_info': {},
        #         'success': True}

        self.assert_eq_val(resp['app_info'], {})
        self.assert_eq_val(resp['success'], True)
        self.assert_eq_val(resp['info'], 'Got data_group_type successfully')

        first_dgt = resp['data'][0]
        self.assert_eq_val(first_dgt['id'], 1)
        self.assert_eq_val(first_dgt['name'], 'Raw')
        self.assert_eq_val(first_dgt['identifier'], 'RAW')
        self.assert_eq_val(first_dgt['flg_available'], True)
        self.assert_eq_val(first_dgt['description'], '')

    def test_get_proposal_experiments(self):
        proposal_number = 0
        resp = self.mdc_client.get_proposal_experiments(proposal_number)

        # Logging information
        logging.error('resp: {0}'.format(resp))

        #
        # RESPONSE example
        #
        # resp = {'info': 'Got experiment successfully',
        #         'success': True,
        #         'data': [{'id': -1,
        #                   'name': 'TestExperiment DO NOT DELETE!',
        #                   'doi': 'xfel.mdc.exp.-1',
        #                   'experiment_number': 1,
        #                   'flg_available': True,
        #                   'proposal_id': -1,
        #                   'experiment_type_id': 1,
        #                   'experiment_folder': 'e0001',
        #                   'publisher': 'XFEL',
        #                   'contributor': 'XFEL',
        #                   'proposal_last_run': 0,
        #                   'experiment_last_run': 0,
        #                   'description': ''}],
        #         'app_info': {}}

        self.assert_eq_val(resp['app_info'], {})
        self.assert_eq_val(resp['success'], True)
        self.assert_eq_val(resp['info'], 'Got experiment successfully')

        first_exp = resp['data'][0]
        self.assert_eq_val(first_exp['id'], -1)
        self.assert_eq_val(first_exp['name'], 'TestExperiment DO NOT DELETE!')
        self.assert_eq_val(first_exp['doi'], 'xfel.mdc.exp.-1')
        self.assert_eq_val(first_exp['experiment_number'], 1)
        self.assert_eq_val(first_exp['flg_available'], True)
        self.assert_eq_val(first_exp['proposal_id'], -1)
        self.assert_eq_val(first_exp['experiment_type_id'], 1)
        self.assert_eq_val(first_exp['experiment_folder'], 'e0001')
        self.assert_eq_val(first_exp['publisher'], 'XFEL')
        self.assert_eq_val(first_exp['contributor'], 'XFEL')

        # Unfortunately these tests are not possible to be executed when
        # using in.xfel.eu/test_metadata application/DB as test system
        # self.assert_eq_val(first_exp['proposal_last_run'], 0)
        # self.assert_eq_val(first_exp['experiment_last_run'], 0)

        self.assert_eq_val(first_exp['description'], '')

    def test_get_active_proposal_by_instrument(self):
        instrument_id = -2
        resp = MetadataClient. \
            get_active_proposal_by_instrument(self.mdc_client, instrument_id)

        #
        # RESPONSE example
        #
        # resp = {'info': 'proposal not found!',
        #         'data': {},
        #         'success': False,
        #         'app_info': 'Resource not found!'}

        self.assert_eq_val(resp['app_info'], 'Resource not found!')
        self.assert_eq_val(resp['success'], False)
        self.assert_eq_val(resp['info'], 'Error getting proposal')
        self.assert_eq_val(resp['data'], {})

    def test_get_proposal_experiments_with_errors(self):
        proposal_number = -99
        resp = self.mdc_client.get_proposal_experiments(proposal_number)

        # Logging information
        logging.error('resp: {0}'.format(resp))

        #
        # RESPONSE example
        #
        # resp = {'info': 'proposal not found!',
        #         'success': False,
        #         'app_info': 'Proposal number -99 not found',
        #         'data': {}}

        self.assert_eq_val(resp['info'], 'Error getting proposal')
        self.assert_eq_val(resp['success'], False)
        self.assert_eq_val(resp['app_info'], 'Proposal number -99 not found')
        self.assert_eq_val(resp['data'], {})

    def test_get_proposal_runs_all_runs(self):
        proposal_number = 0
        resp = self.mdc_client.get_proposal_runs(proposal_number)

        # Logging information
        logging.error('resp: {0}'.format(resp))

        #
        # RESPONSE example
        #
        # resp = {'info': 'Got proposal successfully',
        #         'success': True,
        #         'data': {
        #           'proposal': {
        #               'id': -1,
        #               'number': 0,
        #               'title': 'Proposal Title 001'
        #                  },
        #           'runs': [
        #               {
        #               'id': -1,
        #               'run_number': 1,
        #               'flg_status': 1,
        #               'flg_run_quality': -1,
        #               'size': null,
        #               'num_files': 0,
        #               'repositories': {
        #                   'XFEL_TESTS_REPO': {
        #                       'name": 'XFEL Tests Repository',
        #                       'mount_point': '/webstorage/XFEL',
        #                       'data_groups': 1
        #                       }
        #                   }
        #               }
        #            ]
        #          },
        #         'app_info': {}}

        self.assert_eq_val(resp['app_info'], {})
        self.assert_eq_val(resp['success'], True)
        self.assert_eq_val(resp['info'], 'Got proposal successfully')

        self.assert_eq_val(len(resp['data']['runs']), 2)

        first_run = resp['data']['runs'][0]
        self.assert_eq_val(first_run['id'], -1)
        self.assert_eq_val(first_run['run_number'], 1)
        self.assert_eq_val(first_run['flg_status'], 2)
        self.assert_eq_val(first_run['flg_run_quality'], 1)
        self.assert_eq_val(first_run['num_files'], 0)

        first_repo = first_run['repositories']['XFEL_TESTS_REPO']
        self.assert_eq_val(first_repo['name'],
                           'XFEL Tests Repository')
        self.assert_eq_val(first_repo['mount_point'], '/webstorage/XFEL')
        self.assert_eq_val(first_repo['data_groups'], 1)

        second_run = resp['data']['runs'][1]
        self.assert_eq_val(second_run['id'], -2)
        self.assert_eq_val(second_run['run_number'], 2)
        self.assert_eq_val(second_run['flg_status'], 1)
        self.assert_eq_val(second_run['flg_run_quality'], -1)
        self.assert_eq_val(second_run['num_files'], 0)

    def test_get_proposal_runs_first_page(self):
        proposal_number = 0
        resp = self.mdc_client.get_proposal_runs(proposal_number, page=2,
                                                 page_size=1)

        # Logging information
        logging.error('resp: {0}'.format(resp))

        self.assert_eq_val(resp['app_info'], {})
        self.assert_eq_val(resp['success'], True)
        self.assert_eq_val(resp['info'], 'Got proposal successfully')

        self.assert_eq_val(len(resp['data']['runs']), 1)

        first_run = resp['data']['runs'][0]
        self.assert_eq_val(first_run['id'], -1)
        self.assert_eq_val(first_run['run_number'], 1)
        self.assert_eq_val(first_run['flg_status'], 2)
        self.assert_eq_val(first_run['flg_run_quality'], 1)
        self.assert_eq_val(first_run['num_files'], 0)

        first_repo = first_run['repositories']['XFEL_TESTS_REPO']
        self.assert_eq_val(first_repo['name'],
                           'XFEL Tests Repository')
        self.assert_eq_val(first_repo['mount_point'], '/webstorage/XFEL')
        self.assert_eq_val(first_repo['data_groups'], 1)

    def test_get_proposal_runs_second_page(self):
        proposal_number = 0
        resp = self.mdc_client.get_proposal_runs(proposal_number,
                                                 page=DEF_PAGE,
                                                 page_size=1)

        # Logging information
        logging.error('resp: {0}'.format(resp))

        self.assert_eq_val(resp['app_info'], {})
        self.assert_eq_val(resp['success'], True)
        self.assert_eq_val(resp['info'], 'Got proposal successfully')

        self.assert_eq_val(len(resp['data']['runs']), 1)

        second_run = resp['data']['runs'][0]
        self.assert_eq_val(second_run['id'], -2)
        self.assert_eq_val(second_run['run_number'], 2)
        self.assert_eq_val(second_run['flg_status'], 1)
        self.assert_eq_val(second_run['flg_run_quality'], -1)
        self.assert_eq_val(second_run['num_files'], 0)

    def test_get_proposal_runs_with_errors(self):
        proposal_number = -99
        resp = self.mdc_client.get_proposal_runs(proposal_number)

        # Logging information
        logging.error('resp: {0}'.format(resp))

        #
        # RESPONSE example
        #
        # resp = {'info': 'proposal not found!',
        #         'success': False,
        #         'data': 'Proposal number -99 not found',
        #         'app_info': {}}

        self.assert_eq_val(resp['info'], 'Error getting proposal')
        self.assert_eq_val(resp['success'], False)
        self.assert_eq_val(resp['app_info'], 'Proposal number -99 not found')
        self.assert_eq_val(resp['data'], {})

    def test_get_proposal_samples(self):
        proposal_number = 0
        resp = self.mdc_client.get_proposal_samples(proposal_number)

        # Logging information
        logging.error('resp: {0}'.format(resp))

        #
        # RESPONSE example
        #
        # resp = {'info': 'Got sample successfully',
        #         'success': True,
        #         'data': [{'id': -1,
        #                   'name': 'TestSample DO NOT DELETE!',
        #                   'proposal_id': -1,
        #                   'sample_type_id': 1,
        #                   'flg_available': True,
        #                   'url': '',
        #                   'description': ''}],
        #         'app_info': {}}

        self.assert_eq_val(resp['app_info'], {})
        self.assert_eq_val(resp['success'], True)
        self.assert_eq_val(resp['info'], 'Got sample successfully')

        first_exp = resp['data'][0]
        self.assert_eq_val(first_exp['id'], -1)
        self.assert_eq_val(first_exp['name'], 'TestSample DO NOT DELETE!')
        self.assert_eq_val(first_exp['proposal_id'], -1)
        self.assert_eq_val(first_exp['sample_type_id'], 1)
        self.assert_eq_val(first_exp['flg_available'], True)
        self.assert_eq_val(first_exp['url'], 'https://www.google.com')
        self.assert_eq_val(first_exp['description'], '')

    def test_get_proposal_samples_with_errors(self):
        proposal_number = -99
        resp = self.mdc_client.get_proposal_samples(proposal_number)

        # Logging information
        logging.error('resp: {0}'.format(resp))

        #
        # RESPONSE example
        #
        # resp = {'info': 'proposal not found!',
        #         'success': False,
        #         'data': 'Proposal number -99 not found',
        #         'app_info': {}}

        self.assert_eq_val(resp['info'], 'Error getting proposal')
        self.assert_eq_val(resp['success'], False)
        self.assert_eq_val(resp['app_info'], 'Proposal number -99 not found')
        self.assert_eq_val(resp['data'], {})

    def test_get_proposal_samples_with_page_error_and_empty_data(self):
        proposal_number = 0
        resp = self.mdc_client.get_proposal_samples(proposal_number,
                                                    page=100,
                                                    page_size=3)

        # Logging information
        logging.error('resp: {0}'.format(resp))

        #
        # RESPONSE example
        #
        # resp = {'info': 'proposal not found!',
        #         'success': False,
        #         'data': 'Proposal number -99 not found',
        #         'app_info': {}}

        self.assert_eq_val(resp['info'], 'Error getting sample')
        self.assert_eq_val(resp['success'], False)
        self.assert_eq_val(resp['app_info'], {})
        self.assert_eq_val(resp['data'], {})

    def test_get_proposal_details_success(self):
        resp = self.mdc_client.get_proposal_info(900061, ['SPB', 'SA1'])

        # Logging information
        logging.error('resp: {0}'.format(resp))

        # Expected return:
        #
        self.assert_eq_val(resp['app_info'], {})
        self.assert_eq_val(resp['success'], True)
        self.assert_eq_val(resp['info'], 'Got proposal successfully')

        prop_info = resp['data']

        self.assertEqual(prop_info['id'], -2)
        self.assertEqual(prop_info['number'], 900061)
        self.assertEqual(prop_info['title'],
                         'DO NOT DELETE - CONTROLS TEST PROPOSAL 900061')
        self.assertEqual(prop_info['abstract'], "")
        self.assertEqual(prop_info['proposal_folder'], 'p900061')
        self.assertEqual(prop_info['def_proposal_path'],
                         '/gpfs/exfel/exp/SPB/200030/p900061/raw')
        self.assertEqual(prop_info['doi'], '10.0850/XFEL.EU-DATA-900061-00')
        self.assertEqual(prop_info['url'],
                         'https://www.xfel.eu/cas_robot_framework_test')
        self.assertEqual(prop_info['instrument_id'], 1)
        self.assertEqual(prop_info['instrument_cycle_id'], -1)
        self.assertEqual(prop_info['principal_investigator_id'], -7)
        self.assertEqual(prop_info['main_proposer_id'], -7)
        self.assertEqual(prop_info['local_contact_id'], None)
        # self.assertEqual(prop_info['orig_repository_id'], 103)
        # self.assertEqual(prop_info['last_run'], 422)
        # self.assertEqual(prop_info['begin_at'], '2021-06-02T17:42:...')
        # self.assertEqual(prop_info['end_at'], '2021-06-09T17:42:...')
        # self.assertEqual(prop_info['release_at'], '2024-06-09T17:42:...')
        # self.assertEqual(prop_info['num_delivered_shifts'], None)
        # self.assertEqual(prop_info['num_preparation_shifts'], None)
        # self.assertEqual(prop_info['flg_public'], False)
        self.assertEqual(prop_info['flg_proposal_system'], 'L')
        # self.assertEqual(prop_info['flg_preferred_data_output'], 'R')
        self.assertEqual(prop_info['flg_available'], True)
        # self.assertEqual(prop_info['flg_auto_run_quality'], -1)
        # self.assertEqual(prop_info['flg_cloneable_status'], 'NC')
        self.assertEqual(prop_info['flg_beamtime_status'], 'R')
        # self.assertEqual(prop_info['beamtime_start_at'], None)
        # self.assertEqual(prop_info['beamtime_end_at'], None)
        # self.assertEqual(prop_info['description'], '???')

        self.assertEqual(prop_info['instrument_identifier'], 'SPB')

    def test_get_proposal_details_error_sample(self):
        resp = self.mdc_client.get_proposal_info(900966, ['SA1', 'SA2', 'SA3'])

        # Logging information
        logging.error('resp: {0}'.format(resp))

        # Expected return:
        #
        self.assert_eq_val(resp['info'], 'Error getting proposal')
        self.assert_eq_val(resp['app_info'],
                           'The proposal has no Samples defined yet in myMdC!')  # noqa
        self.assert_eq_val(resp['success'], False)
        self.assert_eq_val(resp['data'], {})

    def test_get_proposal_details_error_instruments(self):
        resp = self.mdc_client.get_proposal_info(900061, ['SA1', 'SA2', 'SA3'])

        # Logging information
        logging.error('resp: {0}'.format(resp))

        # Expected return:
        #
        self.assert_eq_val(resp['info'], 'Error getting proposal')
        self.assert_eq_val(resp['app_info'],
                           "The proposal doesn\'t match this DAQ instance configured list of allowed instruments!")  # noqa
        self.assert_eq_val(resp['success'], True)
        self.assert_eq_val(resp['data'], {})

    def test_register_run_with_invalid_keys(self):
        experiment_id = None
        sample_id = None
        run_dict = {}
        data_grp_dict = {}

        resp = self.mdc_client.register_run(
            experiment_id, sample_id, run_dict, data_grp_dict
        )

        # Logging information
        logging.error('resp: {0}'.format(resp))

        #
        # RESPONSE example
        #
        # resp = {
        #     'info': "The following fields are mandatory: "
        #             "['experiment_id', 'run.run_number', 'run.begin_at', "
        #             "'run.first_train', 'data_group.data_group_type_id', "
        #             "'data_group.creator_id', 'data_group.prefix_path']",
        #     'success': False,
        #     'data': {},
        #     'app_info': {}}

        exp_info = "The following fields are mandatory: " \
                   "['experiment_id', 'run.run_number', 'run.begin_at', " \
                   "'run.first_train', 'data_group.data_group_type_id', " \
                   "'data_group.creator_id', 'data_group.prefix_path']"

        self.assert_eq_val(resp['info'], exp_info)
        self.assert_eq_val(resp['success'], False)
        self.assert_eq_val(resp['app_info'], {})
        self.assert_eq_val(resp['data'], {})

    def test_register_run_with_app_error_in_run(self):
        experiment_id = -1
        sample_id = -1

        run_dict = {'run_number': 125,
                    'begin_at': '2014-06-25T08:30:00.000+02:00',
                    'first_train': None}

        __prefix_path = '/webstorage/XFEL/raw/SPB/2016_01/p0008/e0001/'
        data_grp_dict = {'data_group_type_id': '1',
                         # 'experiment_id': '-1',
                         'creator_id': '-1',  # user_id
                         'prefix_path': __prefix_path}

        resp = self.mdc_client.register_run(
            experiment_id, sample_id, run_dict, data_grp_dict
        )

        # Logging information
        logging.error('resp: {0}'.format(resp))

        #
        # RESPONSE example
        #
        # resp = {'info': 'Error creating run',
        #         'success': False,
        #         'app_info': {
        #             'first_train': ["can't be blank", 'is not a number']},
        #         'data': {}}

        app_info = {'first_train': ["can't be blank", 'is not a number']}

        self.assert_eq_val(resp['info'], 'Error creating run')
        self.assert_eq_val(resp['success'], False)
        self.assert_eq_val(resp['app_info'], app_info)
        self.assert_eq_val(resp['data'], {})

    def test_register_run_with_app_error_in_data_group(self):
        experiment_id = -1
        sample_id = -1

        run_number_val = 126
        run_dict = {'run_number': run_number_val,
                    'begin_at': '2014-06-25T08:30:00.000+02:00',
                    'first_train': 126}

        data_grp_dict = {'data_group_type_id': '1',
                         # 'experiment_id': '-1',
                         'creator_id': '-1',  # user_id
                         'prefix_path': None}

        resp = self.mdc_client.register_run(
            experiment_id, sample_id, run_dict, data_grp_dict
        )

        # Logging information
        logging.error('resp: {0}'.format(resp))

        #
        # RESPONSE example
        #
        # resp = {'info': 'Error creating data_group',
        #         'success': False,
        #         'app_info': {
        #             'prefix_path': [
        #                 "can't be blank",
        #                 'is too short (minimum is 2 characters)']},
        #         'data': {}}

        app_info = {'prefix_path': ["can't be blank",
                                    'is too short (minimum is 2 characters)']}

        self.assert_eq_val(resp['info'], 'Error creating data_group')
        self.assert_eq_val(resp['success'], False)
        self.assert_eq_val(resp['app_info'], app_info)
        self.assert_eq_val(resp['data'], {})

    def test_register_run_with_success(self):
        run_info = self.__test_successful_register_run()
        run_id = run_info['run_id']
        run_number = run_info['run_number']
        data_group_id = run_info['data_group_id']

        # DELETE created Run...
        self.__test_delete_run_by_id(run_id)

        # DELETE created DataGroup...
        self.__test_delete_data_group_by_id(data_group_id)

    def test_register_run_data_with_invalid_keys(self):
        experiment_id = None
        sample_id = None
        run_id = None
        data_group_id = None
        data_group_dict = {}
        data_group_files_ar = []

        resp = self.mdc_client.register_run_data(
            experiment_id,
            sample_id,
            run_id,
            data_group_id,
            data_group_dict,
            data_group_files_ar)

        # Logging information
        logging.error('resp: {0}'.format(resp))

        #
        # RESPONSE example
        #
        # resp = {'info': "The following fields are mandatory: "
        #                 "['experiment_id', 'run_id', 'data_group_id', "
        #                 "'data_group_files']",
        #         'success': False,
        #         'data': {},
        #         'app_info': {}}

        exp_info = "The following fields are mandatory: ['experiment_id', " \
                   "'run_id', 'data_group_id', 'data_group_files']"

        self.assert_eq_val(resp['info'], exp_info)
        self.assert_eq_val(resp['success'], False)
        self.assert_eq_val(resp['app_info'], {})
        self.assert_eq_val(resp['data'], {})

    def test_register_run_data_with_invalid_keys_2(self):
        experiment_id = None
        sample_id = None
        run_id = None
        data_group_id = None
        data_group_dict = {'language': 'pt'}
        data_group_files_ar = [{'filename': 's0000.h5', 'sequence': 11},
                               {'relative_path': 'r0001/', 'sequence': 11},
                               {'sequence': 11}]

        resp = self.mdc_client.register_run_data(
            experiment_id,
            sample_id,
            run_id,
            data_group_id,
            data_group_dict,
            data_group_files_ar)

        # Logging information
        logging.error('resp: {0}'.format(resp))

        #
        # RESPONSE example
        #
        # resp = {
        #     'info': "The following fields are mandatory: ["
        #             "'experiment_id', "
        #             "'run_id', "
        #             "'data_group_id', "
        #             "'data_group.data_group_type_id', "
        #             "'data_group.creator_id', "
        #             "'data_group_files[0].relative_path', "
        #             "'data_group_files[1].filename', "
        #             "'data_group_files[2].filename', "
        #             "'data_group_files[2].relative_path']",
        #     'success': False,
        #     'data': {},
        #     'app_info': {}}

        exp_info = "The following fields are mandatory: [" \
                   "'experiment_id', " \
                   "'run_id', " \
                   "'data_group_id', " \
                   "'data_group.data_group_type_id', " \
                   "'data_group.creator_id', " \
                   "'data_group_files[0].relative_path', " \
                   "'data_group_files[1].filename', " \
                   "'data_group_files[2].filename', " \
                   "'data_group_files[2].relative_path']"

        self.assert_eq_val(resp['info'], exp_info)
        self.assert_eq_val(resp['success'], False)
        self.assert_eq_val(resp['app_info'], {})
        self.assert_eq_val(resp['data'], {})

    def test_register_run_data_with_app_error_in_data_group(self):
        run_info = self.__test_successful_register_run()
        experiment_id = run_info['experiment_id']
        sample_id = run_info['sample_id']
        run_id = run_info['run_id']
        run_number = run_info['run_number']
        data_group_id = run_info['data_group_id']

        data_group_dict = {'data_group_type_id': 2,
                           'creator_id': -999,
                           'name': 'just a new name',
                           'prefix_path': 'bla_bla'}
        data_group_files_ar = [{'filename': 's0000.h5',
                                'sequence': 11,
                                'relative_path': 'r0001/'}]

        resp = self.mdc_client.register_run_data(
            experiment_id,
            sample_id,
            run_id,
            data_group_id,
            data_group_dict,
            data_group_files_ar)

        # Logging information
        logging.error('resp: {0}'.format(resp))

        #
        # RESPONSE example
        #
        # resp = {'info': 'Error updating data_group',
        #         'success': False,
        #         'data': {},
        #         'app_info': {'name': ['cannot be updated'],
        #                      'data_group_type_id': ['cannot be updated'],
        #                      'prefix_path': ['cannot be updated']}
        #         }

        # DELETE created Run...
        self.__test_delete_run_by_id(run_id)
        # DELETE created DataGroup...
        self.__test_delete_data_group_by_id(data_group_id)

        app_info = {'name': ['cannot be updated'],
                    'data_group_type_id': ['cannot be updated'],
                    'prefix_path': ['cannot be updated']}

        self.assert_eq_val(resp['info'], 'Error updating data_group')
        self.assert_eq_val(resp['success'], False)
        self.assert_eq_val(resp['app_info'], app_info)
        self.assert_eq_val(resp['data'], {})

    def test_register_run_data_with_app_error_in_data_group_files(self):
        run_info = self.__test_successful_register_run()
        experiment_id = run_info['experiment_id']
        sample_id = run_info['sample_id']
        run_id = run_info['run_id']
        run_number = run_info['run_number']
        data_group_id = run_info['data_group_id']

        data_group_dict = {'data_group_type_id': 1,
                           'creator_id': -1}
        data_group_files_ar = [{'filename': '1', 'relative_path': '1'}]

        resp = self.mdc_client.register_run_data(
            experiment_id,
            sample_id,
            run_id,
            data_group_id,
            data_group_dict,
            data_group_files_ar)

        # Logging information
        logging.error('resp: {0}'.format(resp))

        #
        # RESPONSE example
        #
        # resp = {'info': 'Error creating data_file',
        #         'success': False,
        #         'app_info': {
        #             'files': ['is too short (minimum is 40 characters)']},
        #         'data': {}}

        # DELETE created Run...
        self.__test_delete_run_by_id(run_id)
        # DELETE created DataGroup...
        self.__test_delete_data_group_by_id(data_group_id)

        app_info = {'files': ['is too short (minimum is 40 characters)']}

        self.assert_eq_val(resp['info'], 'Error creating data_file')
        self.assert_eq_val(resp['success'], False)
        self.assert_eq_val(resp['app_info'], app_info)
        self.assert_eq_val(resp['data'], {})

    def test_register_run_data_with_success(self):
        run_data_info = self.__test_successful_register_data_run()
        data_file_id = run_data_info['data_file_id']
        run_id = run_data_info['run_id']
        run_number = run_data_info['run_number']
        data_group_id = run_data_info['data_group_id']

        # DELETE created DataFile...
        self.__test_delete_data_file_by_id(data_file_id)
        # DELETE created Run...
        self.__test_delete_run_by_id(run_id)
        # DELETE created DataGroup...
        self.__test_delete_data_group_by_id(data_group_id)

    def test_close_run_with_keys_of_wrong_type(self):
        run_info = self.__test_successful_register_data_run()
        experiment_id = run_info['experiment_id']
        sample_id = run_info['sample_id']
        run_id = run_info['run_id']
        run_number = run_info['run_number']
        data_group_id = run_info['data_group_id']
        data_file_id = run_info['data_file_id']
        run_dict = ''  # Should be an Dict, not an String ('str')
        dg_parameters_dict = []  # Should be an Dict, not an Array ('list')

        resp = self.mdc_client.close_run(
            experiment_id,
            sample_id,
            run_id,
            data_group_id,
            run_dict,
            dg_parameters_dict)

        # Logging information
        logging.error('resp: {0}'.format(resp))

        #
        # RESPONSE example
        #
        # resp = {'success': False,
        #         'info': "The following fields are mandatory: "
        #                 "['run must be a hash', "
        #                 "'run.end_at', "
        #                 "'run.last_train', "
        #                 "'parameters must be a hash']",
        #         'data': {},
        #         'app_info': {}}

        self.assert_eq_val(resp['info'],
                           "The following fields are mandatory: "
                           "['run must be a hash', "
                           "'run.end_at', "
                           "'run.last_train', "
                           "'parameters must be a Hash']")
        self.assert_eq_val(resp['success'], False)
        self.assert_eq_val(resp['app_info'], {})
        self.assert_eq_val(resp['data'], {})

        # DELETE created DataFile...
        self.__test_delete_data_file_by_id(data_file_id)
        # DELETE created Run...
        self.__test_delete_run_by_id(run_id)
        # DELETE created DataGroup...
        self.__test_delete_data_group_by_id(data_group_id)

    def test_close_run_with_invalid_keys(self):
        run_info = self.__test_successful_register_data_run()
        experiment_id = run_info['experiment_id']
        sample_id = run_info['sample_id']
        run_id = run_info['run_id']
        run_number = run_info['run_number']
        data_group_id = run_info['data_group_id']
        data_file_id = run_info['data_file_id']
        run_dict = {'first_train': 100}
        dg_parameters_dict = {}

        resp = self.mdc_client.close_run(
            experiment_id,
            sample_id,
            run_id,
            data_group_id,
            run_dict,
            dg_parameters_dict)

        # Logging information
        logging.error('resp: {0}'.format(resp))

        #
        # RESPONSE example
        #
        # resp = {'success': False,
        #         'info': "The following fields are mandatory: "
        #                 "['parameters']",
        #         'data': {},
        #         'app_info': {}}

        self.assert_eq_val(resp['info'],
                           "The following fields are mandatory: "
                           "['run.end_at', 'run.last_train']")
        self.assert_eq_val(resp['success'], False)
        self.assert_eq_val(resp['app_info'], {})
        self.assert_eq_val(resp['data'], {})

        # DELETE created DataFile...
        self.__test_delete_data_file_by_id(data_file_id)
        # DELETE created Run...
        self.__test_delete_run_by_id(run_id)
        # DELETE created DataGroup...
        self.__test_delete_data_group_by_id(data_group_id)

    def test_close_run_with_invalid_keys_2(self):
        run_info = self.__test_successful_register_data_run()
        experiment_id = run_info['experiment_id']
        sample_id = run_info['sample_id']
        run_id = run_info['run_id']
        run_number = run_info['run_number']
        data_group_id = run_info['data_group_id']
        data_file_id = run_info['data_file_id']
        run_dict = {'first_train': 100}
        dg_parameters_dict = {'parameters': [{}]}

        resp = self.mdc_client.close_run(
            experiment_id,
            sample_id,
            run_id,
            data_group_id,
            run_dict,
            dg_parameters_dict)

        # Logging information
        logging.error('resp: {0}'.format(resp))

        #
        # RESPONSE example
        #
        # resp = {'success': False,
        #         'info': "The following fields are mandatory: "
        #                 "['run.end_at', 'run.last_train', "
        #                 "'parameters[0].data_source', "
        #                 "'parameters[0].param_name', "
        #                 "'parameters[0].param_value', "
        #                 "'parameters[0].data_type_id']",
        #         'data': {},
        #         'app_info': {}}

        self.assert_eq_val(resp['info'],
                           "The following fields are mandatory: "
                           "['run.end_at', 'run.last_train', "
                           "'parameters[0].data_source', "
                           "'parameters[0].name', "
                           "'parameters[0].value', "
                           "'parameters[0].minimum', "
                           "'parameters[0].maximum', "
                           "'parameters[0].mean', "
                           "'parameters[0].standard_deviation', "
                           "'parameters[0].data_type_id', "
                           "'parameters[0].parameter_type_id', "
                           "'parameters[0].unit_id']")
        self.assert_eq_val(resp['success'], False)
        self.assert_eq_val(resp['app_info'], {})
        self.assert_eq_val(resp['data'], {})

        # DELETE created DataFile...
        self.__test_delete_data_file_by_id(data_file_id)
        # DELETE created Run...
        self.__test_delete_run_by_id(run_id)
        # DELETE created DataGroup...
        self.__test_delete_data_group_by_id(data_group_id)

    def test_close_run_with_invalid_keys_3(self):
        run_info = self.__test_successful_register_data_run()
        experiment_id = run_info['experiment_id']
        sample_id = run_info['sample_id']
        run_id = run_info['run_id']
        run_number = run_info['run_number']
        data_group_id = run_info['data_group_id']
        data_file_id = run_info['data_file_id']
        run_dict = {'first_train': 100}
        dg_parameters_dict = {'parameters': ''}

        resp = self.mdc_client.close_run(
            experiment_id,
            sample_id,
            run_id,
            data_group_id,
            run_dict,
            dg_parameters_dict)

        # Logging information
        logging.error('resp: {0}'.format(resp))

        #
        # RESPONSE example
        #
        # resp = {'success': False,
        #         'info': "The following fields are mandatory: "
        #                 "['run.end_at', 'run.last_train', "
        #                 "'parameters[0].data_source', "
        #                 "'parameters[0].param_name', "
        #                 "'parameters[0].param_value', "
        #                 "'parameters[0].data_type_id']",
        #         'data': {},
        #         'app_info': {}}

        self.assert_eq_val(resp['info'],
                           "The following fields are mandatory: "
                           "['run.end_at', 'run.last_train', "
                           "'parameters[0].data_source', "
                           "'parameters[0].name', "
                           "'parameters[0].value', "
                           "'parameters[0].minimum', "
                           "'parameters[0].maximum', "
                           "'parameters[0].mean', "
                           "'parameters[0].standard_deviation', "
                           "'parameters[0].data_type_id', "
                           "'parameters[0].parameter_type_id', "
                           "'parameters[0].unit_id']")
        self.assert_eq_val(resp['success'], False)
        self.assert_eq_val(resp['app_info'], {})
        self.assert_eq_val(resp['data'], {})

        # DELETE created DataFile...
        self.__test_delete_data_file_by_id(data_file_id)
        # DELETE created Run...
        self.__test_delete_run_by_id(run_id)
        # DELETE created DataGroup...
        self.__test_delete_data_group_by_id(data_group_id)

    def test_close_run_with_app_error_in_run(self):
        run_info = self.__test_successful_register_data_run()
        experiment_id = run_info['experiment_id']
        sample_id = run_info['sample_id']
        run_id = run_info['run_id']
        run_number = run_info['run_number']
        data_group_id = run_info['data_group_id']
        data_file_id = run_info['data_file_id']
        #
        run_dict = {'run_number': 1234,
                    'end_at': '2015-06-25T08:30:00.000+02:00',
                    'last_train': -1,
                    'flg_available': 1,
                    'flg_status': 1}
        #
        dg_parameters_ar = {
            'parameters': [
                {'data_source': 'MID/XTD6/ATT/MOTOR/BLADE_TOP',
                 'name': 'Velocity Right',
                 'value': 15.6,
                 'minimum': 15.6,
                 'maximum': 15.6,
                 'mean': 15.6,
                 'standard_deviation': 15.6,
                 'data_type_id': 2,
                 'parameter_type_id': 3,
                 'unit_id': 1}
            ]}

        resp = self.mdc_client.close_run(
            experiment_id,
            sample_id,
            run_id,
            data_group_id,
            run_dict,
            dg_parameters_ar)

        # Logging information
        logging.error('resp: {0}'.format(resp))

        #
        # RESPONSE example
        #
        # resp = {'success': False,
        #         'info': 'Error updating run',
        #         'data': {},
        #         'app_info': {
        #             'run_number': ['cannot be updated'],
        #             'run_folder': ['cannot be updated'],
        #             'last_train': ['must be greater than or equal to 126']}}
        cannot_update_ar = ['cannot be updated']
        must_be_greater_ar = ['must be greater than or equal to 126']

        self.assert_eq_val(resp['info'], 'Error updating run')
        self.assert_eq_val(resp['success'], False)
        self.assert_eq_val(resp['data'], {})
        #
        self.assert_eq_val(resp['app_info']['run_number'], cannot_update_ar)
        self.assert_eq_val(resp['app_info']['run_folder'], cannot_update_ar)
        self.assert_eq_val(resp['app_info']['last_train'], must_be_greater_ar)

        # DELETE created DataFile...
        self.__test_delete_data_file_by_id(data_file_id)
        # DELETE created Run...
        self.__test_delete_run_by_id(run_id)
        # DELETE created DataGroup...
        self.__test_delete_data_group_by_id(data_group_id)

    def test_close_run_with_app_error_in_parameters(self):
        run_info = self.__test_successful_register_data_run()
        experiment_id = run_info['experiment_id']
        sample_id = run_info['sample_id']
        run_id = run_info['run_id']
        run_number = run_info['run_number']
        data_group_id = run_info['data_group_id']
        data_file_id = run_info['data_file_id']
        #
        run_dict = {}
        #
        dg_parameters_ar = {
            'parameters': [
                {'data_source': 'MID/XTD6/ATT/MOTOR/BLADE_TOP',
                 # 'name': 'Velocity Right',
                 'name': '',
                 'value': 15.6,
                 'minimum': 15.6,
                 'maximum': 15.6,
                 'mean': 15.6,
                 'standard_deviation': 15.6,
                 'data_type_id': 2,
                 'parameter_type_id': 3,
                 'unit_id': 1}
            ]
        }

        resp = self.mdc_client.close_run(
            experiment_id,
            sample_id,
            run_id,
            data_group_id,
            run_dict,
            dg_parameters_ar)

        # Logging information
        logging.error('resp: {0}'.format(resp))

        #
        # RESPONSE example
        #
        # resp = {'success': False,
        #         'info': 'Error creating parameter',
        #         'data': {},
        #         'app_info': [{'name': ["can't be blank"]}]}
        cannot_be_blank_ar = ["can't be blank"]

        self.assert_eq_val(resp['info'], 'Error creating parameter')
        self.assert_eq_val(resp['success'], False)
        self.assert_eq_val(resp['data'], {})
        #
        # TODO, correct array!!!
        self.assert_eq_val(resp['app_info'][0]['name'], cannot_be_blank_ar)

        # DELETE created DataFile...
        self.__test_delete_data_file_by_id(data_file_id)
        # DELETE created Run...
        self.__test_delete_run_by_id(run_id)
        # DELETE created DataGroup...
        self.__test_delete_data_group_by_id(data_group_id)

    def test_close_run_with_success(self):
        run_info = self.__test_successful_close_run()
        experiment_id = run_info['experiment_id']
        sample_id = run_info['sample_id']
        run_id = run_info['run_id']
        run_number = run_info['run_number']
        data_group_id = run_info['data_group_id']
        data_file_id = run_info['data_file_id']

        # DELETE created DataFile...
        self.__test_delete_data_file_by_id(data_file_id)
        # DELETE created Run...
        self.__test_delete_run_by_id(run_id)
        # DELETE created Parameter...
        self.__test_delete_parameters_by_data_group_id(data_group_id)
        # DELETE created DataGroup...
        self.__test_delete_data_group_by_id(data_group_id)

    def test_register_run_replica_with_success(self):
        run_info = self.__test_successful_close_run()
        experiment_id = run_info['experiment_id']
        sample_id = run_info['sample_id']
        run_id = run_info['run_id']
        run_number = run_info['run_number']
        data_group_id = run_info['data_group_id']
        data_file_id = run_info['data_file_id']

        # Other variables
        proposal_number = '000000'
        repository_identifier = 'XFEL_GPFS_OFFLINE_RAW_CC'
        repository_id = 11

        resp_reg = self.mdc_client.register_run_replica(
            proposal_number,
            run_number,
            repository_identifier)

        # Logging information
        logging.error('resp: {0}'.format(resp_reg))
        #
        # RESPONSE example
        #
        # resp = {'success': True,
        #         'info': 'Run replica registered successfully',
        #         'data': {'experiment_id': '-1',
        #                  'sample_id': '-1',
        #                  'run_id': '1588',
        #                  'data_group_id': '777'},
        #         'app_info': {}}

        self.assert_eq_val(resp_reg['info'],
                           'Run replica registered successfully')
        self.assert_eq_val(resp_reg['success'], True)
        self.assert_eq_val(resp_reg['app_info'], {})
        #
        resp_reg_data = resp_reg['data']
        self.assert_eq_val(resp_reg_data[0]['data_group_id'], data_group_id)
        self.assert_eq_val(resp_reg_data[0]['repository_id'], repository_id)
        self.assert_eq_val(resp_reg_data[0]['flg_available'], True)
        #
        self.assert_eq_val(len(resp_reg_data), 1)

        resp_unreg = MetadataClient.unregister_run_replica(
            self.mdc_client,
            proposal_number, run_number, repository_identifier)

        # Logging information
        logging.error('resp: {0}'.format(resp_unreg))
        #
        # RESPONSE example
        #
        # resp = {'success': True,
        #         'info': 'Run replica unregistered successfully',
        #         'data': {'data_group_id': '-1',
        #                  'repository_id': '1',
        #                  'flg_available': 'false'},
        #         'app_info': {}}

        self.assert_eq_val(resp_unreg['info'],
                           'Run replica unregistered successfully')
        self.assert_eq_val(resp_unreg['success'], True)
        self.assert_eq_val(resp_unreg['app_info'], {})
        #
        resp_unreg_data = resp_unreg['data']
        self.assert_eq_val(resp_unreg_data[0]['data_group_id'], data_group_id)
        self.assert_eq_val(resp_unreg_data[0]['repository_id'], repository_id)
        self.assert_eq_val(resp_unreg_data[0]['flg_available'], False)
        #
        self.assert_eq_val(len(resp_unreg_data), 1)

        # DELETE created DataFile...
        self.__test_delete_data_file_by_id(data_file_id)
        # DELETE created Run...
        self.__test_delete_run_by_id(run_id)
        # DELETE created Parameter...
        self.__test_delete_parameters_by_data_group_id(data_group_id)
        # DELETE created DataGroup...
        self.__test_delete_data_group_by_id(data_group_id)

    def __test_successful_register_run(self):
        experiment_id = -1
        sample_id = -1

        run_number_val = 126
        run_dict = {'run_number': run_number_val,
                    'begin_at': '2014-06-25T08:30:00.000+02:00',
                    'first_train': 126}

        __prefix_path = '/webstorage/XFEL/raw/SPB/2016_01/p0008/e0001/'
        data_grp_dict = {'data_group_type_id': '1',
                         # 'experiment_id': '-1',
                         'creator_id': '-1',  # user_id
                         'prefix_path': __prefix_path}

        resp = self.mdc_client.register_run(
            experiment_id, sample_id,
            run_dict, data_grp_dict)

        # Logging information
        logging.error('resp: {0}'.format(resp))

        #
        # RESPONSE example
        #
        # resp = {'info': 'Run registered successfully',
        #         'success': True,
        #         'app_info': {},
        #         'data': {'experiment_id': '-1',
        #                  'sample_id': '-1',
        #                  'run_id': '343',
        #                  'data_group_id': '574'}
        #         }

        # The new IDs received are:
        run_id = resp['data']['run_id']
        data_group_id = resp['data']['data_group_id']

        # Assert creation message
        self.assert_eq_val(resp['info'], 'Run registered successfully')
        self.assert_eq_val(resp['success'], True)
        self.assert_eq_val(resp['app_info'], {})
        self.assert_eq_val(resp['data']['experiment_id'], experiment_id)
        self.assert_eq_val(resp['data']['sample_id'], sample_id)
        self.assert_not_eq_str(run_id, '', 'run_id')
        self.assert_not_eq_str(data_group_id, '', 'data_group_id')

        return {'experiment_id': experiment_id,
                'sample_id': sample_id,
                'run_id': run_id,
                'run_number': run_number_val,
                'data_group_id': data_group_id}

    def __test_successful_register_data_run(self):
        run_info = self.__test_successful_register_run()
        experiment_id = run_info['experiment_id']
        sample_id = run_info['sample_id']
        run_id = run_info['run_id']
        run_number = run_info['run_number']
        data_group_id = run_info['data_group_id']

        data_group_dict = {'data_group_type_id': 1,
                           'creator_id': -1}
        data_group_files_ar = [{'filename': 's0000.h5',
                                'sequence': 11,
                                'relative_path': 'r0001/'}]

        resp = self.mdc_client.register_run_data(
            experiment_id,
            sample_id,
            run_id,
            data_group_id,
            data_group_dict,
            data_group_files_ar)

        # Logging information
        logging.error('resp: {0}'.format(resp))

        #
        # RESPONSE example
        #
        # resp = {'info': 'Run data registered successfully',
        #         'success': True,
        #         'data': {'run_id': '498',
        #                  'data_group_id': '692',
        #                  'sample_id': '-1',
        #                  'experiment_id': '-1',
        #                  'data_file_id': '240'},
        #         'app_info': {}}

        # The new IDs received are:
        data_file_id = resp['data']['data_file_id']

        # Assert creation message
        self.assert_eq_val(resp['info'], 'Run data registered successfully')
        self.assert_eq_val(resp['success'], True)
        self.assert_eq_val(resp['app_info'], {})
        self.assert_eq_val(resp['data']['experiment_id'], experiment_id)
        self.assert_eq_val(resp['data']['sample_id'], sample_id)
        self.assert_eq_val(resp['data']['run_id'], run_id)
        self.assert_eq_val(resp['data']['data_group_id'], data_group_id)
        self.assert_not_eq_str(data_file_id, '', 'data_file_id')

        return {'experiment_id': experiment_id,
                'sample_id': sample_id,
                'run_id': run_id,
                'run_number': run_number,
                'data_group_id': data_group_id,
                'data_file_id': data_file_id}

    def __test_successful_close_run(self):
        run_info = self.__test_successful_register_data_run()
        experiment_id = run_info['experiment_id']
        sample_id = run_info['sample_id']
        run_id = run_info['run_id']
        run_number = run_info['run_number']
        data_group_id = run_info['data_group_id']
        data_file_id = run_info['data_file_id']
        #
        run_dict = {'end_at': '2015-06-25T08:30:00.000+02:00',
                    'last_train': 127,
                    'flg_available': 1,
                    'flg_status': 1}
        #
        dg_parameters_ar = {
            'parameters': [
                {'data_source': 'MID/XTD6/ATT/MOTOR/BLADE_TOP',
                 'name': 'VelocityLeft',
                 'value': 15.6,
                 'minimum': 15.6,
                 'maximum': 15.6,
                 'mean': 15.6,
                 'standard_deviation': 15.6,
                 'data_type_id': 2,
                 'parameter_type_id': 3,
                 'unit_id': 1}
            ]
        }

        resp = self.mdc_client.close_run(
            experiment_id,
            sample_id,
            run_id,
            data_group_id,
            run_dict,
            dg_parameters_ar)

        # Logging information
        logging.error('resp: {0}'.format(resp))

        #
        # RESPONSE example
        #
        # resp = {'success': True,
        #         'info': 'Run closed successfully',
        #         'data': {'sample_id': '-1',
        #                  'run_id': '1382',
        #                  'experiment_id': '-1'},
        #         'app_info': {}}

        self.assert_eq_val(resp['info'], 'Run closed successfully')
        self.assert_eq_val(resp['success'], True)
        self.assert_eq_val(resp['app_info'], {})
        #
        self.assert_eq_val(resp['data']['sample_id'], sample_id)
        self.assert_eq_val(resp['data']['run_id'], run_id)
        self.assert_eq_val(resp['data']['experiment_id'], experiment_id)

        return {'experiment_id': experiment_id,
                'sample_id': sample_id,
                'run_id': run_id,
                'run_number': run_number,
                'data_group_id': data_group_id,
                'data_file_id': data_file_id}

    def __test_delete_run_by_id(self, run_id):
        # RESPONSE example
        #
        # resp = {'info': 'run deleted successfully',
        #         'success': True,
        #         'data': {},
        #         'app_info': {}}
        # TODO, Hierarchy vs. Composites
        resp_api = self.mdc_client.delete_run_api(run_id)
        resp = self.mdc_client.format_response(resp_api, DELETE, NO_CONTENT,
                                               RUN)

        self.assert_eq_val(resp['info'], 'run deleted successfully')
        self.assert_eq_val(resp['success'], True)
        self.assert_eq_val(resp['app_info'], {})
        self.assert_eq_val(resp['data'], {})

    def __test_delete_parameters_by_data_group_id(self, data_group_id):
        resp_api = self.mdc_client.delete_bulk_parameter_api_by_data_group_id(
            data_group_id)

        # RESPONSE example
        #
        # resp = {'info': 'parameter deleted successfully',
        #         'success': True,
        #         'data': {},
        #         'app_info': {}}
        # TODO, Hierarchy vs. Composites
        resp = self.mdc_client.format_response(resp_api, DELETE,
                                               NO_CONTENT, PARAMETER)

        self.assert_eq_val(resp['info'], 'parameter deleted successfully')
        self.assert_eq_val(resp['success'], True)
        self.assert_eq_val(resp['app_info'], {})
        self.assert_eq_val(resp['data'], {})

    def __test_delete_data_group_by_id(self, data_group_id):
        # RESPONSE example
        #
        # resp = {'info': 'data_group deleted successfully',
        #         'success': True,
        #         'data': {},
        #         'app_info': {}}
        # TODO, Hierarchy vs. Composites
        resp_api = self.mdc_client.delete_data_group_api(data_group_id)
        resp = self.mdc_client.format_response(resp_api, DELETE, NO_CONTENT,
                                               DATA_GROUP)

        self.assert_eq_val(resp['info'], 'data_group deleted successfully')
        self.assert_eq_val(resp['success'], True)
        self.assert_eq_val(resp['app_info'], {})
        self.assert_eq_val(resp['data'], {})

    def __test_delete_data_file_by_id(self, data_file_id):
        # RESPONSE example
        #
        # resp = {'info': 'data_group_file deleted successfully',
        #         'success': True,
        #         'data': {},
        #         'app_info': {}}
        # TODO, Hierarchy vs. Composites
        resp_api = self.mdc_client.delete_data_file_api(data_file_id)
        resp = self.mdc_client.format_response(resp_api, DELETE, NO_CONTENT,
                                               DATA_FILE)

        self.assert_eq_val(resp['info'], 'data_file deleted successfully')
        self.assert_eq_val(resp['success'], True)
        self.assert_eq_val(resp['app_info'], {})
        self.assert_eq_val(resp['data'], {})


if __name__ == '__main__':
    unittest.main()
