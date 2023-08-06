"""ParameterTypeApi module class"""

import json

from ..common.base import Base
from ..common.config import *


class ParameterTypeApi(Base):
    def create_parameter_type_api(self, parameter_type):
        api_url = self.__get_api_url()
        return self.api_post(api_url, data=json.dumps(parameter_type))

    def delete_parameter_type_api(self, parameter_type_id):
        api_url = self.__get_api_url(parameter_type_id)
        return self.api_delete(api_url)

    def update_parameter_type_api(self, parameter_type_id, parameter_type):
        api_url = self.__get_api_url(parameter_type_id)
        return self.api_put(api_url, data=json.dumps(parameter_type))

    def get_parameter_type_by_id_api(self, parameter_type_id):
        api_url = self.__get_api_url(parameter_type_id)
        return self.api_get(api_url, params={})

    def get_all_parameter_types_by_name_api(self, name,
                                            page=DEF_PAGE,
                                            page_size=DEF_PAGE_SIZE):
        api_url = self.__get_api_url()
        return self.api_get(api_url, params={'name': name,
                                             'page': page,
                                             'page_size': page_size})

    #
    # Private Methods
    #
    def __get_api_url(self, api_specifics=''):
        model_name = 'parameter_types/'
        return self.get_api_url(model_name, api_specifics)
