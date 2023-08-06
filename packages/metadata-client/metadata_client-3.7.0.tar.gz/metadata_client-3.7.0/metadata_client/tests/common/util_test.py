"""UtilTest class"""

import unittest
from time import gmtime, strftime

from ...common.util import Util


class UtilTest(unittest.TestCase):
    def test_get_formatted_date(self):
        dt_str = Util.get_formatted_date('%Y-%m-%dT%H:%M:%S',
                                         epoch_val=0,
                                         dt_extra='.000+00:00')
        self.assertEqual(dt_str, '1970-01-01T00:00:00.000+00:00')

        dt_str = Util.get_formatted_date('%Y-%m-%dT%H:%M:%S', epoch_val=0)
        self.assertEqual(dt_str, '1970-01-01T00:00:00')

        # This test may periodically fail
        dt_str = Util.get_formatted_date('%Y-%m-%dT%H:%M:%S')
        dt_now = strftime("%Y-%m-%dT%H:%M:%S", gmtime())
        self.assertEqual(dt_str, dt_now)

    def test_int_to_bool(self):
        self.assertEqual(Util.int_to_bool(-1), 'false')
        self.assertEqual(Util.int_to_bool(0), 'false')
        self.assertEqual(Util.int_to_bool(1), 'true')
        self.assertEqual(Util.int_to_bool(2), 'false')
        self.assertEqual(Util.int_to_bool(3), 'false')
        self.assertEqual(Util.int_to_bool(99), 'false')

    def test_get_opt_dict_val(self):
        h01 = {
            'test_01': 'value_01',
            'test_02': 'value_02',
            # 'test_03': '',
            'test_04': ''
        }
        val01 = Util.get_opt_dict_val(h01, 'test_01', "I'm the default value!")
        val01_without_default = Util.get_opt_dict_val(h01, 'test_01')
        self.assertEqual(val01, 'value_01')
        self.assertEqual(val01_without_default, 'value_01')

        val02 = Util.get_opt_dict_val(h01, 'test_02', "I'm the default value!")
        val02_without_default = Util.get_opt_dict_val(h01, 'test_02')
        self.assertEqual(val02, 'value_02')
        self.assertEqual(val02_without_default, 'value_02')

        val03 = Util.get_opt_dict_val(h01, 'test_03', "I'm the default value!")
        val03_without_default = Util.get_opt_dict_val(h01, 'test_03')
        self.assertEqual(val03, "I'm the default value!")
        self.assertEqual(val03_without_default, '')

        val04 = Util.get_opt_dict_val(h01, 'test_04', "I'm the default value!")
        val04_without_default = Util.get_opt_dict_val(h01, 'test_04')
        self.assertEqual(val04, '')
        self.assertEqual(val04_without_default, '')


if __name__ == '__main__':
    unittest.main()
