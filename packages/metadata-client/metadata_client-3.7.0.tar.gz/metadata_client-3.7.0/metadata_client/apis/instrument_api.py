"""InstrumentApi module class"""

from ..common.base import Base
from ..common.config import *


class InstrumentApi(Base):
    def get_instrument_by_id_api(self, instrument_id):
        api_url = self.__get_api_url(instrument_id)
        return self.api_get(api_url, params={})

    def get_all_instruments_api(self, page=DEF_PAGE, page_size=DEF_PAGE_SIZE):
        api_url = self.__get_api_url()
        return self.api_get(api_url, params={'page': page,
                                             'page_size': page_size})

    def get_all_instruments_by_identifier_api(self, identifier,
                                              page=DEF_PAGE,
                                              page_size=DEF_PAGE_SIZE):
        api_url = self.__get_api_url()
        return self.api_get(api_url, params={'identifier': identifier,
                                             'page': page,
                                             'page_size': page_size})

    def get_all_instruments_by_facility_id_api(self, facility_id,
                                               page=DEF_PAGE,
                                               page_size=DEF_PAGE_SIZE):
        api_url = self.__get_api_url()
        return self.api_get(api_url, params={'facility_id': facility_id,
                                             'page': page,
                                             'page_size': page_size})

    def get_all_instruments_by_topic_id_api(self, topic_id,
                                            page=DEF_PAGE,
                                            page_size=DEF_PAGE_SIZE):
        api_url = self.__get_api_url()
        return self.api_get(api_url, params={'topic_id': topic_id,
                                             'page': page,
                                             'page_size': page_size})

    def get_instrument_active_proposal_api(self, instrument_id):
        api_specific = '{0}/active_proposal'.format(instrument_id)
        api_url = self.__get_api_url(api_specific)
        return self.api_get(api_url, params={})

    #
    # Private Methods
    #
    def __get_api_url(self, api_specifics=''):
        model_name = 'instruments/'
        return self.get_api_url(model_name, api_specifics)
