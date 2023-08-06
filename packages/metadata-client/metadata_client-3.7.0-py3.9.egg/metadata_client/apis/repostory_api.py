"""RepositoryApi module class"""

import json

from ..common.base import Base
from ..common.config import *


class RepositoryApi(Base):
    def create_repository_api(self, repository):
        api_url = self.__get_api_url()
        return self.api_post(api_url, data=json.dumps(repository))

    def delete_repository_api(self, repository_id):
        api_url = self.__get_api_url(repository_id)
        return self.api_delete(api_url)

    def update_repository_api(self, repository_id, repository):
        api_url = self.__get_api_url(repository_id)
        return self.api_put(api_url, data=json.dumps(repository))

    def get_repository_by_id_api(self, repository_id):
        api_url = self.__get_api_url(repository_id)
        return self.api_get(api_url, params={})

    def get_all_repositories_by_name_api(self, name,
                                         page=DEF_PAGE,
                                         page_size=DEF_PAGE_SIZE):
        api_url = self.__get_api_url()
        return self.api_get(api_url, params={'name': name,
                                             'page': page,
                                             'page_size': page_size})

    def get_all_repositories_by_identifier_api(self, identifier):
        api_url = self.__get_api_url()
        return self.api_get(api_url, params={'identifier': identifier})

    #
    # Private Methods
    #
    def __get_api_url(self, api_specifics=''):
        model_name = 'repositories/'
        return self.get_api_url(model_name, api_specifics)
