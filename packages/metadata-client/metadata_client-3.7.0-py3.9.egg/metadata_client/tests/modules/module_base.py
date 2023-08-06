"""BaseTest Class with helper methods common to all modules tests"""

import unittest

from ..common.util import Util


class ModuleBase(Util, unittest.TestCase):
    def assert_create_success(self, module_name, receive, exp_data):
        msg = '{0} created successfully'.format(module_name)
        exp = {'success': True, 'info': msg, 'app_info': {}, 'data': exp_data}
        self.__assert_success(receive, exp)

    def assert_find_success(self, module_name, receive, exp_data):
        msg = 'Got {0} successfully'.format(module_name)
        exp = {'success': True, 'info': msg, 'app_info': {}, 'data': exp_data}
        self.__assert_success(receive, exp)

    def assert_not_found_success(self, module_name, receive, exp_data,
                                 unique_id):
        if unique_id:
            msg = '{0} "{1}" could not be found!'.format(module_name,
                                                         unique_id)
        else:
            info_msg = 'No {0} could be found respecting the specified ' \
                       'search criteria'
            msg = info_msg.format(module_name)

        exp = {'success': True, 'info': msg, 'app_info': {}, 'data': exp_data}
        self.__assert_success(receive, exp)

    def assert_update_success(self, module_name, receive, exp_data):
        msg = '{0} updated successfully'.format(module_name)
        exp = {'success': True, 'info': msg, 'app_info': {}, 'data': exp_data}
        self.__assert_success(receive, exp)

    def assert_delete_success(self, module_name, receive):
        msg = '{0} deleted successfully'.format(module_name)
        exp = {'success': True, 'info': msg, 'app_info': {}, 'data': {}}
        self.__assert_success(receive, exp)

    def assert_set_success(self, module_name, receive, exp_data):
        msg = '{0} set successfully'.format(module_name)
        exp = {'success': True, 'info': msg, 'app_info': {}, 'data': exp_data}
        self.__assert_success(receive, exp)

    def assert_create_error(self, module_name, receive, exp_info):
        msg = 'Error creating {0}'.format(module_name)
        exp = {'success': False, 'info': msg, 'app_info': exp_info, 'data': {}}
        self.__assert_error(receive, exp)

    def assert_find_error(self, module_name, receive, exp_info):
        msg = 'Error getting {0}'.format(module_name)
        exp = {'success': False, 'info': msg, 'app_info': exp_info, 'data': {}}
        self.__assert_error(receive, exp)

    def assert_update_error(self, module_name, receive, exp_info):
        msg = 'Error updating {0}'.format(module_name)
        exp = {'success': False, 'info': msg, 'app_info': exp_info, 'data': {}}
        self.__assert_error(receive, exp)

    def assert_delete_error(self, module_name, receive, exp_info):
        msg = 'Error deleting {0}'.format(module_name)
        exp = {'success': False, 'info': msg, 'app_info': exp_info, 'data': {}}
        self.__assert_error(receive, exp)

    def assert_set_error(self, module_name, receive, exp_info):
        msg = 'Error setting {0}'.format(module_name)
        exp = {'success': False, 'info': msg, 'app_info': exp_info, 'data': {}}
        self.__assert_error(receive, exp)

    def __assert_success(self, receive, expect):
        field = 'app_info'
        self.assert_eq_val(receive[field], {})

        # Validate all 'data' fields
        expect_data = expect['data']
        if type(expect_data) is list and len(expect_data) > 0:
            for i in range(0, len(expect_data)):
                self.fields_validation(receive['data'][i], expect['data'][i])
        elif type(expect_data) is dict and len(expect_data) > 0:
            self.fields_validation(receive['data'], expect['data'])
        else:
            self.assert_eq_val(receive[field], expect[field])

        field = 'info'
        self.assert_eq_val(receive[field], expect[field])

        field = 'success'
        self.assert_eq_val(receive[field], expect[field])

    def __assert_error(self, receive, expect):
        field = 'app_info'
        expect_app_info = expect[field]

        if type(expect_app_info) is dict and len(expect_app_info) > 0:
            for key, val in expect_app_info.items():
                self.assert_eq_val(receive[field][key], expect_app_info[key])
        else:
            self.assert_eq_val(receive[field], expect[field])

        field = 'data'
        self.assert_eq_val(receive[field], expect[field])

        field = 'info'
        self.assert_eq_val(receive[field], expect[field])

        field = 'success'
        self.assert_eq_val(receive[field], expect[field])
