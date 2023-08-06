"""ExperimentApi module class"""

import json

from ..common.base import Base
from ..common.config import *


class ExperimentApi(Base):
    def create_experiment_api(self, experiment):
        api_url = self.__get_api_url()
        return self.api_post(api_url, data=json.dumps(experiment))

    def delete_experiment_api(self, experiment_id):
        api_url = self.__get_api_url(experiment_id)
        return self.api_delete(api_url)

    def update_experiment_api(self, experiment_id, experiment):
        api_url = self.__get_api_url(experiment_id)
        return self.api_put(api_url, data=json.dumps(experiment))

    def get_experiment_by_id_api(self, experiment_id):
        api_url = self.__get_api_url(experiment_id)
        return self.api_get(api_url, params={})

    def get_all_experiments_by_name_and_proposal_id_api(
            self, name, proposal_id,
            page=DEF_PAGE, page_size=DEF_PAGE_SIZE):
        api_url = self.__get_api_url()
        return self.api_get(api_url,
                            params={'name': name, 'proposal_id': proposal_id,
                                    'page': page, 'page_size': page_size})

    def get_all_experiments_by_proposal_id_api(self, proposal_id,
                                               page=DEF_PAGE,
                                               page_size=DEF_PAGE_SIZE):
        api_url = self.__get_api_url()
        return self.api_get(api_url, params={'proposal_id': proposal_id,
                                             'page': page,
                                             'page_size': page_size})

    #
    # Private Methods
    #
    def __get_api_url(self, api_specifics=''):
        model_name = 'experiments/'
        return self.get_api_url(model_name, api_specifics)
