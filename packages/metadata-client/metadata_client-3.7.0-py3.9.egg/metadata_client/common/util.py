"""Util Class with helper methods"""
from time import gmtime, strftime


class Util(object):
    @staticmethod
    def get_formatted_date(dt_format, epoch_val=None, dt_extra=None):
        # formatted_time_str
        if epoch_val is None:
            formatted_time_str = strftime(dt_format, gmtime())
        else:
            formatted_time_str = strftime(dt_format, gmtime(epoch_val))

        # timezone
        if dt_extra is None:
            fractional_and_timezone = ''
        else:
            fractional_and_timezone = dt_extra

        return '{0}{1}'.format(formatted_time_str, fractional_and_timezone)

    @staticmethod
    def int_to_bool(int_value):
        int_str_value = str(int_value)

        if int_str_value == '1':
            return 'true'
        else:
            return 'false'

    @staticmethod
    def get_opt_dict_val(h, element_name, def_val=''):
        if element_name in h:
            return h[element_name]
        else:
            return def_val

    @staticmethod
    def get_opt_val(value, def_val=''):
        if value:
            return str(value)
        else:
            return def_val
