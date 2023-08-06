"""User module class"""
import inspect

from ..common.base import Base
from ..common.config import *

MODULE_NAME = USER


class User:
    def __init__(self, metadata_client,
                 name, email, uid, first_name, last_name):
        self.metadata_client = metadata_client
        self.id = None
        self.name = name
        self.email = email
        self.uid = uid
        self.first_name = first_name
        self.last_name = last_name

    @staticmethod
    def get_by_id(mdc_client, user_id):
        response = mdc_client.get_user_by_id_api(user_id)

        curr_method_name = inspect.currentframe().f_code.co_name
        Base.cal_debug(MODULE_NAME, curr_method_name, response)
        return Base.format_response(response, GET, OK, MODULE_NAME)

    def __get_resource(self):
        user = {
            MODULE_NAME: {
                'name': self.name,
                'email': self.email,
                'uid': self.uid,
                'first_name': self.first_name,
                'last_name': self.last_name
            }
        }

        return user
