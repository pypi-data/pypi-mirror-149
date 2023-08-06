"""DataGroupRepositoryApi module class"""

import json

from ..common.base import Base
from ..common.config import *


class DataGroupRepositoryApi(Base):
    def create_data_group_repository_api(self, data_group_repository):
        api_url = self.__get_api_url()
        return self.api_post(api_url, data=json.dumps(data_group_repository))

    def delete_data_group_repository_api(self, data_group_repository_id):
        api_url = self.__get_api_url(data_group_repository_id)
        return self.api_delete(api_url)

    def update_data_group_repository_api(self, data_group_repository_id,
                                         data_group_repository):
        api_url = self.__get_api_url(data_group_repository_id)
        return self.api_put(api_url, data=json.dumps(data_group_repository))

    def get_data_group_repository_by_id_api(self, data_group_repository_id):
        api_url = self.__get_api_url(data_group_repository_id)
        return self.api_get(api_url, params={})

    def get_all_by_data_group_id_api(self, data_group_id,
                                     page=DEF_PAGE, page_size=DEF_PAGE_SIZE):
        api_url = self.__get_api_url()
        return self.api_get(api_url, params={'data_group_id': data_group_id,
                                             'page': page,
                                             'page_size': page_size})

    def get_all_by_data_group_id_and_repository_id_api(
            self, data_group_id, repository_id,
            page=DEF_PAGE, page_size=DEF_PAGE_SIZE):
        api_url = self.__get_api_url()
        return self.api_get(api_url, params={'data_group_id': data_group_id,
                                             'repository_id': repository_id,
                                             'page': page,
                                             'page_size': page_size})

    #
    # Private Methods
    #
    def __get_api_url(self, api_specifics=''):
        model_name = 'data_groups_repositories/'
        return self.get_api_url(model_name, api_specifics)
