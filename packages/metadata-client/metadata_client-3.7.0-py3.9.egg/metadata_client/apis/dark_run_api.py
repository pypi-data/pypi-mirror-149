"""DarkRunApi module class"""

import json

from ..common.base import Base
from ..common.config import *


class DarkRunApi(Base):
    def create_dark_run_api(self, dark_run):
        api_url = self.__get_api_url()
        return self.api_post(api_url, data=json.dumps(dark_run))

    def delete_dark_run_api(self, dark_run_id):
        api_url = self.__get_api_url(dark_run_id)
        return self.api_delete(api_url)

    def update_dark_run_api(self, dark_run_id, dark_run):
        api_url = self.__get_api_url(dark_run_id)
        return self.api_put(api_url, data=json.dumps(dark_run))

    def get_dark_run_by_id_api(self, dark_run_id):
        api_url = self.__get_api_url(dark_run_id)
        return self.api_get(api_url, params={})

    def get_all_dark_runs_by_proposal_id_api(self, proposal_id,
                                             page=DEF_PAGE,
                                             page_size=DEF_PAGE_SIZE):
        api_url = self.__get_api_url()
        return self.api_get(api_url, params={'proposal_id': proposal_id,
                                             'page': page,
                                             'page_size': page_size})

    def get_all_dark_runs_by_detector_id_api(self, detector_id,
                                             page=DEF_PAGE,
                                             page_size=DEF_PAGE_SIZE):
        api_url = self.__get_api_url()
        return self.api_get(api_url, params={'detector_id': detector_id,
                                             'page': page,
                                             'page_size': page_size})

    #
    # Private Methods
    #
    def __get_api_url(self, api_specifics=''):
        model_name = 'dark_runs/'
        return self.get_api_url(model_name, api_specifics)
