"""RunApi module class"""

import json

from ..common.base import Base
from ..common.config import *


class RunApi(Base):
    def create_run_api(self, run):
        api_url = self.__get_api_url()
        return self.api_post(api_url, data=json.dumps(run))

    def delete_run_api(self, run_id):
        api_url = self.__get_api_url(run_id)
        return self.api_delete(api_url)

    def update_run_api(self, run_id, run):
        api_url = self.__get_api_url(run_id)
        return self.api_put(api_url, data=json.dumps(run))

    def get_run_by_id_api(self, run_id):
        api_url = self.__get_api_url(run_id)
        return self.api_get(api_url, params={})

    def get_all_runs_by_run_number_api(self, run_number,
                                       page=DEF_PAGE, page_size=DEF_PAGE_SIZE):
        api_url = self.__get_api_url()
        return self.api_get(api_url, params={'run_number': run_number,
                                             'page': page,
                                             'page_size': page_size})

    def get_all_runs_by_proposal_number_api(self, proposal_number,
                                            page=DEF_PAGE,
                                            page_size=DEF_PAGE_SIZE):
        api_url = self.__get_api_url('runs_by_proposal')
        return self.api_get(api_url,
                            params={'proposal_number': proposal_number,
                                    'page': page, 'page_size': page_size})

    def get_run_by_run_number_and_experiment_id_api(self,
                                                    run_number,
                                                    experiment_id):
        api_url = self.__get_api_url()
        return self.api_get(api_url, params={'run_number': run_number,
                                             'experiment_id': experiment_id})

    def get_run_all_raw_data_groups_ids_api(self, run_number, proposal_number):
        api_url = self.__get_api_url('all_raw_data_groups_ids')
        return self.api_get(api_url,
                            params={'run_number': run_number,
                                    'proposal_number': proposal_number})

    #
    # Private Methods
    #
    def __get_api_url(self, api_specifics=''):
        model_name = 'runs/'
        return self.get_api_url(model_name, api_specifics)
