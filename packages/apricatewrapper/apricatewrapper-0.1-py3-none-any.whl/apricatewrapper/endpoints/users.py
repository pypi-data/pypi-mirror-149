from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import apricatewrapper

@dataclass
class Users:
    api: 'apricatewrapper.ApricateAPI'

    def create_user(self, username: str) -> dict:
        ''' Creates a user with the given username, if available. 

            Args:
                username (str): The username.

            Returns:
                dict: the response of the api call
        '''
        return self.api._post_request(f"/users/{username}/claim")

    def public_user_info(self, username: str) -> dict:
        ''' Returns the public information of a user.

            Args:
                username (str): The username of the user.

            Returns:
                dict: the response of the api call
        '''
        return self.api._get_request(f"/users/{username}")

    def my_user_info(self) -> dict:
        '''Returns the info of the user.
        
           Requires auth token. 

           Returns:
                dict: the response of the api call
        '''
        return self.api._get_request("/my/user", secure = True)