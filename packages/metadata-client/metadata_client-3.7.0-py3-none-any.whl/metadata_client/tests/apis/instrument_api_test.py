"""InstrumentApiTest class"""

import unittest

from metadata_client import MetadataClient
from .api_base import ApiBase
from ..common.config_test import *
from ..common.secrets import *


class InstrumentApiTest(ApiBase, unittest.TestCase):
    client_api = MetadataClient(
        client_id=CLIENT_OAUTH2_INFO['CLIENT_ID'],
        client_secret=CLIENT_OAUTH2_INFO['CLIENT_SECRET'],
        token_url=CLIENT_OAUTH2_INFO['TOKEN_URL'],
        refresh_url=CLIENT_OAUTH2_INFO['REFRESH_URL'],
        auth_url=CLIENT_OAUTH2_INFO['AUTH_URL'],
        scope=CLIENT_OAUTH2_INFO['SCOPE'],
        user_email=CLIENT_OAUTH2_INFO['EMAIL'],
        base_api_url=BASE_API_URL)

    def test_create_instrument_api(self):
        instrument_func = {
            'instrument': {
                'name': 'Functional Tests Instrument (DO NOT CHANGE)',
                'identifier': 'INST_T',
                'url': 'https://in.xfel.eu/upex',
                'facility_id': '3',
                'topic_id': '-1',
                'instrument_type_id': '1',
                'repository_id': '-1',
                'flg_available': 'false',
                'description': 'instrument used by upex and metadata client '
                               'library for functional tests.'
            }
        }

        expect = instrument_func['instrument']

        #
        # Get entry by name
        #
        self.__get_all_entries_by_identifier_api('INST_T', expect)

        #
        # Get entry by ID
        #
        instrument_id = -1
        self.__get_entry_by_id_api(instrument_id, expect)

        #
        # Get entry by TOPIC ID
        #
        topic_id = -1
        self.__get_entry_by_topic_id_api(topic_id, expect)

        #
        # Get entry by FACILITY ID
        #
        facility_id = 3
        self.__get_entry_by_facility_id_api(facility_id, expect)

    #
    # fields_validation
    #
    def fields_validation(self, receive, expect):
        self.assert_eq_hfield(receive, expect, 'name', STRING)
        self.assert_eq_hfield(receive, expect, 'identifier', STRING)
        self.assert_eq_hfield(receive, expect, 'url', STRING)
        self.assert_eq_hfield(receive, expect, 'facility_id', NUMBER)
        self.assert_eq_hfield(receive, expect, 'topic_id', NUMBER)
        self.assert_eq_hfield(receive, expect, 'instrument_type_id', NUMBER)
        self.assert_eq_hfield(receive, expect, 'repository_id', NUMBER)
        self.assert_eq_hfield(receive, expect, 'flg_available', BOOLEAN)
        self.assert_eq_hfield(receive, expect, 'description', STRING)

    #
    # Internal private APIs methods
    #
    def __get_all_entries_by_identifier_api(self, identifier, expect):
        response = self.client_api.get_all_instruments_by_identifier_api(
            identifier)
        receive = self.get_and_validate_all_entries_by_name(response)
        self.fields_validation(receive, expect)

    def __get_entry_by_id_api(self, entry_id, expect):
        response = self.client_api.get_instrument_by_id_api(entry_id)
        receive = self.get_and_validate_entry_by_id(response)
        self.fields_validation(receive, expect)

    def __get_entry_by_facility_id_api(self, facility_id, expect):
        response = self.client_api.get_all_instruments_by_facility_id_api(
            facility_id)
        receive = self.get_and_validate_all_entries_by_name(response)
        self.fields_validation(receive, expect)

    def __get_entry_by_topic_id_api(self, topic_id, expect):
        resp = self.client_api.get_all_instruments_by_topic_id_api(topic_id)
        receive = self.get_and_validate_all_entries_by_name(resp)
        self.fields_validation(receive, expect)


if __name__ == '__main__':
    unittest.main()
