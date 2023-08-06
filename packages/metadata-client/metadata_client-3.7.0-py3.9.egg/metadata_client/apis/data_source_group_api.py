"""DataSourceGroupApi module class"""

from ..common.base import Base
from ..common.config import *


class DataSourceGroupApi(Base):
    def get_data_source_group_by_name_api(self, name):
        api_url = self.__get_api_url()

        return self.api_get(api_url, params={'name': name})

    #
    # Private Methods
    #
    def __get_api_url(self, api_specifics=''):
        model_name = 'data_source_groups/'
        return self.get_api_url(model_name, api_specifics)
