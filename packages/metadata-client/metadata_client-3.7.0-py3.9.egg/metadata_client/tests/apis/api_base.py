"""BaseApiTest Class with helper methods common to all modules tests"""

import unittest

from ..common.config_test import *
from ..common.util import Util


class ApiBase(Util, unittest.TestCase):
    def get_and_validate_create_entry(self, response):
        resp_content = self.load_response_content(response)
        print('CREATE RESPONSE: {0}'.format(resp_content))

        self.assert_eq_status_code(response.status_code, CREATED)

        return resp_content

    def get_and_validate_all_entries_by_name(self, response):
        resp_content = self.load_response_content(response)
        print('GET BY NAME RESPONSE: {0}'.format(resp_content))

        self.assert_eq_status_code(response.status_code, OK)

        return resp_content[-1]

    def get_and_validate_entry_by_id(self, response):
        resp_content = self.load_response_content(response)
        print('GET BY ID RESPONSE: {0}'.format(resp_content))

        self.assert_eq_status_code(response.status_code, OK)

        return resp_content

    def get_and_validate_delete_entry_by_id(self, response):
        self.assert_eq_status_code(response.status_code, NO_CONTENT)

        resp_content = self.load_response_content(response)
        receive = resp_content
        expect = {}

        self.assert_eq_val(receive, expect)

    def get_and_validate_resource_not_found(self, response):
        resp_content = self.load_response_content(response)

        receive = resp_content
        receive_msg = receive['info']
        expect_msg = RESOURCE_NOT_FOUND
        expect = {'info': expect_msg}

        self.assert_eq_status_code(response.status_code, NOT_FOUND)
        self.assertEqual(receive, expect, "Data must not be found")
        self.assert_eq_str(receive_msg, expect_msg)

    @staticmethod
    def escape_and_load_json_from_str(hash_str):
        return Util.escape_and_load_json_from_str(hash_str)
