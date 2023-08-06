"""UserApi module class"""

from ..common.base import Base
from ..common.config import *


class UserApi(Base):
    def get_current_user(self):
        api_url = self.__get_api_url(model_name='me')
        return self.api_get(api_url)

    def get_user_by_id_api(self, user_id, ):
        api_url = self.__get_api_url(model_name='users/',
                                     api_specifics=user_id)
        return self.api_get(api_url, params={})

    #
    # Private Helper Methods
    #

    def __get_api_url(self, model_name='user', api_specifics=''):
        return self.get_api_url(model_name, api_specifics)
