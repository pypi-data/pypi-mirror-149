"""DataSourceGroupVersionApi module class"""

import json

from ..common.base import Base
from ..common.config import *


class DataSourceGroupVersionApi(Base):
    def get_data_source_group_version_api(self,
                                          data_source_group_id, version_name):
        api_url = self.__get_api_url()
        return self.api_get(
            api_url,
            params={'data_source_group_id': data_source_group_id,
                    'name': version_name, })

    def update_data_source_group_version_api(self, id, params):
        api_url = self.__get_api_url(id)
        return self.api_put(api_url, data=json.dumps(params))

    #
    # Private Methods
    #
    def __get_api_url(self, api_specifics=''):
        model_name = 'data_source_group_versions/'
        return self.get_api_url(model_name, api_specifics)
