"""DataSourceGroupVersion module class"""

import inspect

from ..common.base import Base
from ..common.config import *

MODULE_NAME = DATA_SOURCE_GROUP_VERSION


class DataSourceGroupVersion:
    FLG_STATUS_DEPLOYED = 'D'

    def __init__(self,
                 name, identifier,
                 flg_available, description=''):
        self.id = None
        self.name = name
        self.identifier = identifier
        self.flg_available = flg_available
        self.description = description

    @staticmethod
    def get(mdc_client, data_source_group_id, version_name):
        response = mdc_client.get_data_source_group_version_api(
            data_source_group_id, version_name)

        curr_method_name = inspect.currentframe().f_code.co_name
        Base.cal_debug(MODULE_NAME, curr_method_name, response)
        return Base.format_response(response, GET, OK, MODULE_NAME)

    @staticmethod
    def update(mdc_client, id, params):
        response = mdc_client.update_data_source_group_version_api(id, params)

        curr_method_name = inspect.currentframe().f_code.co_name
        Base.cal_debug(MODULE_NAME, curr_method_name, response)
        return Base.format_response(response, GET, OK, MODULE_NAME)
