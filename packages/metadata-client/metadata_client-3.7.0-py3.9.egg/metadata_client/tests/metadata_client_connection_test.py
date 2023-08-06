"""MetadataClientConnectionTest class"""

import logging
import unittest

from metadata_client.metadata_client import MetadataClient
from .common.config_test import *
from .common.secrets import *
from .modules.module_base import ModuleBase


class MetadataClientConnectionTest(ModuleBase, unittest.TestCase):
    def setUp(self):
        self.wrong_mdc_client = MetadataClient(
            client_id=CLIENT_OAUTH2_INFO['CLIENT_ID'],
            client_secret=CLIENT_OAUTH2_INFO['CLIENT_SECRET'],
            token_url=CLIENT_OAUTH2_INFO['TOKEN_URL'],
            refresh_url=CLIENT_OAUTH2_INFO['REFRESH_URL'],
            auth_url=CLIENT_OAUTH2_INFO['AUTH_URL'],
            scope=CLIENT_OAUTH2_INFO['SCOPE'],
            user_email='xxxxxxxxxxxxxx',
            base_api_url=BASE_API_URL
        )

    def test_get_data_group_types_with_errors(self):
        resp = self.wrong_mdc_client.get_all_data_group_types()

        # Logging information
        logging.error('resp: {0}'.format(resp))

        #
        # RESPONSE example
        #
        # resp = {'app_info': "Incorrect request header: 'X-User-Email'!",
        #         'success': False,
        #         'info': 'data_group_type not found!',
        #         'data': {}}

        self.assert_eq_val(resp['app_info'],
                           "Incorrect request header: 'X-User-Email'!")
        self.assert_eq_val(resp['success'], False)
        self.assert_eq_val(resp['info'], 'Error getting data_group_type')
        self.assert_eq_val(resp['data'], {})


if __name__ == '__main__':
    unittest.main()
