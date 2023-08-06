"""ProposalApi module class"""

import json

from ..common.base import Base
from ..common.config import *


class ProposalApi(Base):
    def create_proposal_api(self, proposal):
        api_url = self.__get_api_url()
        return self.api_post(api_url, data=json.dumps(proposal))

    def delete_proposal_api(self, proposal_id):
        api_url = self.__get_api_url(proposal_id)
        return self.api_delete(api_url)

    def update_proposal_api(self, proposal_id, proposal):
        api_url = self.__get_api_url(proposal_id)
        return self.api_put(api_url, data=json.dumps(proposal))

    def get_proposal_by_id_api(self, proposal_id):
        api_url = self.__get_api_url(proposal_id)
        return self.api_get(api_url, params={})

    def get_proposal_by_number_api(self, number):
        api_url = self.__get_api_url('{0}{1}'.format('/by_number/', number))
        return self.api_get(api_url, params={})

    def get_proposal_by_number_daq_info_api(self, number):
        api_url = self.__get_api_url('{0}{1}'.format('/by_number_daq_info/',
                                                     number))
        return self.api_get(api_url, params={})

    def get_runs_by_proposal_number_api(
            self, proposal_number, run_number=None,
            page=DEF_PAGE, page_size=DEF_PAGE_SIZE):
        api_specifics = '{0}{1}{2}'.format('by_number/',
                                           proposal_number, '/runs')
        if run_number:
            api_specifics = '{0}/{1}'.format(api_specifics, run_number)
        api_url = self.__get_api_url(api_specifics)
        return self.api_get(api_url,
                            params={'page': page, 'page_size': page_size})

    def get_all_proposals_by_number_api(self, number, page=DEF_PAGE,
                                        page_size=DEF_PAGE_SIZE):
        api_url = self.__get_api_url()
        return self.api_get(api_url, params={'number': number,
                                             'page': page,
                                             'page_size': page_size})

    #
    # Private Methods
    #
    def __get_api_url(self, api_specifics=''):
        model_name = 'proposals/'
        return self.get_api_url(model_name, api_specifics)
