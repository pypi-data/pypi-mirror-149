"""DataTypeApi module class"""

import json

from ..common.base import Base
from ..common.config import *


class DataTypeApi(Base):
    def create_data_type_api(self, data_type):
        api_url = self.__get_api_url()
        return self.api_post(api_url, data=json.dumps(data_type))

    def delete_data_type_api(self, data_type_id):
        api_url = self.__get_api_url(data_type_id)
        return self.api_delete(api_url)

    def update_data_type_api(self, data_type_id, data_type):
        api_url = self.__get_api_url(data_type_id)
        return self.api_put(api_url, data=json.dumps(data_type))

    def get_data_type_by_id_api(self, data_type_id):
        api_url = self.__get_api_url(data_type_id)
        return self.api_get(api_url, params={})

    def get_all_data_types_by_name_api(self, name, page=DEF_PAGE,
                                       page_size=DEF_PAGE_SIZE):
        api_url = self.__get_api_url()
        return self.api_get(api_url, params={'name': name,
                                             'page': page,
                                             'page_size': page_size})

    #
    # Private Methods
    #
    def __get_api_url(self, api_specifics=''):
        model_name = 'data_types/'
        return self.get_api_url(model_name, api_specifics)
