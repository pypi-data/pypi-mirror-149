"""ProposalTest class"""

import copy
import unittest
from datetime import datetime, timedelta, timezone

from metadata_client.metadata_client import MetadataClient
from .module_base import ModuleBase
from ..common.config_test import *
from ..common.generators import Generators
from ..common.secrets import *
from ..common.util_datetime import UtilDatetime as util_dt
from ...modules.proposal import Proposal

MODULE_NAME = PROPOSAL


class ProposalTest(ModuleBase, unittest.TestCase):
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

        __utc = timezone(timedelta())

        __now = datetime.now()
        __end_at = datetime(__now.year, __now.month, __now.day, __now.hour,
                            __now.minute, __now.second, __now.microsecond,
                            tzinfo=__utc)
        __yesterday = __now - timedelta(1)
        __begin_at = datetime(__yesterday.year, __yesterday.month,
                              __yesterday.day, __yesterday.hour,
                              __yesterday.minute, __yesterday.second,
                              __yesterday.microsecond, tzinfo=__utc)
        __tomorrow = __now + timedelta(1)
        __release_at = datetime(__tomorrow.year, __tomorrow.month,
                                __tomorrow.day, __tomorrow.hour,
                                __tomorrow.minute, __tomorrow.second,
                                __tomorrow.microsecond, tzinfo=__utc)

        __unique_proposal_id1 = Generators.generate_unique_id(min_value=2017,
                                                              max_value=799999)
        self.prop_1 = {
            'number': __unique_proposal_id1,
            'title': __unique_proposal_id1,
            'abstract': '',
            'url': 'https://in.xfel.eu/upex/proposal/{0}'.format(
                __unique_proposal_id1),
            'instrument_id': '1',
            'instrument_cycle_id': '-1',
            'principal_investigator_id': '1',
            'main_proposer_id': '1',
            'begin_at': util_dt.datetime_to_local_tz_str(__begin_at),
            'end_at': util_dt.datetime_to_local_tz_str(__end_at),
            'release_at': util_dt.datetime_to_local_tz_str(__release_at),
            'flg_beamtime_status': 'T',
            'beamtime_start_at': util_dt.datetime_to_local_tz_str(
                __begin_at + timedelta(1)),
            'beamtime_end_at': util_dt.datetime_to_local_tz_str(
                __end_at + timedelta(2)),
            'flg_proposal_system': 'U',
            'flg_available': 'true',
            'description': 'desc 01'
        }

        __end_at_upd = __end_at + timedelta(1)
        __release_at_upd = __release_at + timedelta(1)

        self.prop1_upd = {
            'number': __unique_proposal_id1,  # This field cannot be updated
            'title': __unique_proposal_id1,  # This field cannot be updated
            'abstract': '',
            'url': 'https://in.xfel.eu/upex/proposal/{0}_2'.format(
                __unique_proposal_id1),
            'instrument_id': '2',
            'instrument_cycle_id': '-1',
            'principal_investigator_id': '1',
            'main_proposer_id': '1',
            # 'begin_at' can't be updated
            'begin_at': util_dt.datetime_to_local_tz_str(__begin_at),
            'end_at': util_dt.datetime_to_local_tz_str(__end_at_upd),
            'release_at': util_dt.datetime_to_local_tz_str(__release_at_upd),
            'flg_beamtime_status': 'T',
            'beamtime_start_at': util_dt.datetime_to_local_tz_str(
                __begin_at + timedelta(1)),
            'beamtime_end_at': util_dt.datetime_to_local_tz_str(
                __end_at + timedelta(2)),
            'flg_proposal_system': 'U',  # This field cannot be updated
            'flg_available': 'false',
            'description': 'desc 01 updated!!!'
        }

    def test_create_proposal(self):
        proposal_01 = Proposal(
            metadata_client=self.mdc_client,
            number=self.prop_1['number'],
            title=self.prop_1['title'],
            abstract=self.prop_1['abstract'],
            url=self.prop_1['url'],
            instrument_id=self.prop_1['instrument_id'],
            instrument_cycle_id=self.prop_1['instrument_cycle_id'],
            principal_investigator_id=self.prop_1['principal_investigator_id'],
            main_proposer_id=self.prop_1['main_proposer_id'],
            begin_at=self.prop_1['begin_at'],
            end_at=self.prop_1['end_at'],
            release_at=self.prop_1['release_at'],
            flg_beamtime_status=self.prop_1['flg_beamtime_status'],
            beamtime_start_at=self.prop_1['beamtime_start_at'],
            beamtime_end_at=self.prop_1['beamtime_end_at'],
            flg_proposal_system=self.prop_1['flg_proposal_system'],
            flg_available=self.prop_1['flg_available'],
            description=self.prop_1['description'])

        #
        # Create new entry (should succeed)
        #
        result1 = proposal_01.create()
        self.assert_create_success(MODULE_NAME, result1, self.prop_1)

        proposal = result1['data']
        proposal_id = result1['data']['id']
        number = result1['data']['number']

        #
        # Validate "generated" fields
        self.assertEqual(int(result1['data']['proposal_folder'][1:]), number)

        #
        # Create duplicated entry (should throw an error)
        #
        proposal_01_dup = copy.copy(proposal_01)
        result2 = proposal_01_dup.create()
        expect_app_info = {'number': ['has already been taken'],
                           'url': ['has already been taken']}
        self.assert_create_error(MODULE_NAME, result2, expect_app_info)

        #
        # Get entry by number
        #
        result3 = Proposal.get_by_number(self.mdc_client, number)
        self.assert_find_success(MODULE_NAME, result3, self.prop_1)

        # Necessary to guarantee the release_at matches the calculated datetime
        proposal_01.release_at = result3['data']['release_at']

        #
        # Get entry with non-existent number (should throw an error)
        #
        non_existing_number = 12345
        expected_return = 'Proposal number 12345 not found'

        result31 = Proposal.get_by_number(self.mdc_client, non_existing_number)
        self.assert_find_error(MODULE_NAME, result31, expected_return)

        #
        # Get entry by ID
        #
        result4 = Proposal.get_by_id(self.mdc_client, proposal_id)
        self.assert_find_success(MODULE_NAME, result4, self.prop_1)

        #
        # Get entry with non-existent ID (should throw an error)
        #
        result5 = Proposal.get_by_id(self.mdc_client, -666)
        self.assert_find_error(MODULE_NAME, result5, RESOURCE_NOT_FOUND)

        #
        # Put entry information (update some fields should succeed)
        #
        proposal_01.number = self.prop1_upd['number']
        proposal_01.title = self.prop1_upd['title']
        proposal_01.abstract = self.prop1_upd['abstract']
        proposal_01.url = self.prop1_upd['url']
        proposal_01.instrument_id = self.prop1_upd['instrument_id']
        proposal_01.instrument_cycle_id = self.prop1_upd['instrument_cycle_id']
        proposal_01.principal_investigator_id = self.prop1_upd[
            'principal_investigator_id']
        proposal_01.main_proposer_id = self.prop1_upd['main_proposer_id']
        proposal_01.begin_at = self.prop1_upd['begin_at']
        proposal_01.end_at = self.prop1_upd['end_at']

        proposal_01.flg_beamtime_status = self.prop1_upd['flg_beamtime_status']

        # Fields not updatable
        proposal_01.release_at = proposal_01.release_at
        proposal_01.beamtime_start_at = self.prop_1['beamtime_start_at']
        proposal_01.beamtime_end_at = self.prop_1['beamtime_end_at']

        proposal_01.flg_proposal_system = self.prop1_upd['flg_proposal_system']
        proposal_01.flg_available = self.prop1_upd['flg_available']
        proposal_01.description = self.prop1_upd['description']
        # result6 = proposal_01.update()
        # self.assert_update_success(MODULE_NAME, result6, self.prop1_upd)

        #
        # Put entry information (update some fields should throw an error)
        #
        proposal_01.number = 1234567  # noqa
        proposal_01.flg_available = self.prop1_upd['flg_available']
        proposal_01.description = self.prop1_upd['description']
        result7 = proposal_01.update()
        expect_app_info = {'number': ['cannot be updated']}
        self.assert_update_error(MODULE_NAME, result7, expect_app_info)

        #
        # Delete entry (should succeed)
        # (test purposes only to keep the DB clean)
        #
        result8 = proposal_01.delete()
        self.assert_delete_success(MODULE_NAME, result8)

        #
        # Delete entry (should throw an error)
        # (test purposes only to keep the DB clean)
        #
        result9 = proposal_01.delete()
        self.assert_delete_error(MODULE_NAME, result9, RESOURCE_NOT_FOUND)

    def test_create_proposal_from_dict(self):
        #
        # Create new entry (should succeed)
        #
        result1 = Proposal.create_from_dict(self.mdc_client, self.prop_1)
        self.assert_create_success(MODULE_NAME, result1, self.prop_1)

        proposal = result1['data']
        proposal_id = proposal['id']

        #
        # Create duplicated entry (should throw an error)
        #
        result2 = Proposal.create_from_dict(self.mdc_client, self.prop_1)
        expect_app_info = {'number': ['has already been taken'],
                           'url': ['has already been taken']}
        self.assert_create_error(MODULE_NAME, result2, expect_app_info)

        #
        # Delete entry (should succeed)
        # (test purposes only to keep the DB clean)
        #
        result8 = Proposal.delete_by_id(self.mdc_client, proposal_id)
        self.assert_delete_success(MODULE_NAME, result8)

        #
        # Delete entry (should throw an error)
        # (test purposes only to keep the DB clean)
        #
        result9 = Proposal.delete_by_id(self.mdc_client, proposal_id)
        self.assert_delete_error(MODULE_NAME, result9, RESOURCE_NOT_FOUND)

    def test_existing_proposal_api(self):
        proposal_2 = {
            PROPOSAL: {
                'id': -2,
                'number': 900061,
                'title': 'DO NOT DELETE - CONTROLS TEST PROPOSAL 900061',
                # 'abstract': '',
                # 'url': 'https://www.xfel.eu/cas_robot_framework_test',
                # 'instrument_id': '1',
                'instrument_identifier': 'SPB',
                # 'instrument_cycle_id': '-1',
                # 'principal_investigator_id': '-7',
                # 'main_proposer_id': '-7',
                # 'orig_repository_id': -1,
                'flg_beamtime_status': 'R'
            }
        }

        expect = proposal_2[PROPOSAL]
        prop_number = expect['number']

        #
        # Get entry by number
        #
        result1 = Proposal.get_by_number(self.mdc_client, prop_number)
        received = result1['data']

        # Test matching fields
        self.assertEqual(expect['id'], received['id'], 'proposal id')
        self.assertEqual(expect['number'], received['number'],
                         'proposal number')
        self.assertEqual(expect['title'], received['title'], 'proposal title')
        self.assertEqual(expect['instrument_identifier'],
                         received['instrument_identifier'],
                         'proposal instrument_identifier')
        self.assertEqual(expect['flg_beamtime_status'],
                         received['flg_beamtime_status'],
                         'proposal flg_beamtime_status')

        #
        # Get entry by number DAQ Info
        #
        result2 = Proposal.get_by_number_daq_info(self.mdc_client, prop_number)
        received = result2['data']

        # Test matching fields
        self.assertEqual(expect['id'], received['id'], 'proposal id')
        self.assertEqual(expect['number'], received['number'],
                         'proposal number')
        self.assertEqual(expect['title'], received['title'], 'proposal title')
        self.assertEqual(expect['instrument_identifier'],
                         received['instrument_identifier'],
                         'proposal instrument_identifier')
        self.assertEqual(expect['flg_beamtime_status'],
                         received['flg_beamtime_status'],
                         'proposal flg_beamtime_status')

    #
    # fields_validation
    #
    def fields_validation(self, receive, expect):
        self.assert_eq_hfield(receive, expect, 'number', NUMBER)
        self.assert_eq_hfield(receive, expect, 'title', STRING)
        self.assert_eq_hfield(receive, expect, 'abstract', STRING)
        self.assert_eq_hfield(receive, expect, 'url', STRING)
        self.assert_eq_hfield(receive, expect, 'instrument_id', NUMBER)
        self.assert_eq_hfield(receive, expect, 'instrument_cycle_id', NUMBER)
        self.assert_eq_hfield(receive, expect,
                              'principal_investigator_id', NUMBER)
        self.assert_eq_hfield(receive, expect, 'main_proposer_id', NUMBER)
        self.assert_eq_hfield(receive, expect, 'begin_at', DATETIME)
        self.assert_eq_hfield(receive, expect, 'end_at', DATETIME)
        # self.assert_eq_hfield(receive, expect, 'release_at', DATETIME)
        self.assert_eq_hfield(receive, expect, 'flg_beamtime_status', STRING)
        self.assert_eq_hfield(receive, expect, 'beamtime_start_at', DATETIME)
        self.assert_eq_hfield(receive, expect, 'beamtime_end_at', DATETIME)
        self.assert_eq_hfield(receive, expect, 'flg_proposal_system', BOOLEAN)
        self.assert_eq_hfield(receive, expect, 'flg_available', BOOLEAN)
        self.assert_eq_hfield(receive, expect, 'description', STRING)

        #
        # Validate "generated" fields
        expect['proposal_folder'] = 'p{0:06d}'.format(expect['number'])
        self.assert_eq_hfield(receive, expect, 'proposal_folder', STRING)


if __name__ == '__main__':
    unittest.main()
