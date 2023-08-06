"""DataSourceGroup module class"""

import inspect

from ..common.base import Base
from ..common.config import *

MODULE_NAME = DATA_SOURCE_GROUP


class DataSourceGroup:
    def __init__(self,
                 name, identifier,
                 flg_available, description=''):
        self.id = None
        self.name = name
        self.identifier = identifier
        self.flg_available = flg_available
        self.description = description

    @staticmethod
    def get_by_name(mdc_client, name):
        response = mdc_client.get_data_source_group_by_name_api(name)

        curr_method_name = inspect.currentframe().f_code.co_name
        Base.cal_debug(MODULE_NAME, curr_method_name, response)
        return Base.format_response(response, GET, OK, MODULE_NAME)
