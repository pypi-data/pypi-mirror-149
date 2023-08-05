from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import apricatewrapper

@dataclass
class Assistants:
    api: 'apricatewrapper.ApricateAPI'

    def my_assistants(self) -> dict:
        '''Returns a list of all assistants.
        
           Requires auth token. 

           Returns:
                dict: the response of the api call
        '''
        return self.api._get_request("/my/assistants", secure = True)

    def my_specific_assistant(self, id: int) -> dict:
        ''' Returns data on a specific assistant.
        
            Requires auth token. 

            Args:
                id (int): The id of the assistant.

            Returns:
                dict: the response of the api call
        '''
        return self.api._get_request(f"/my/assistants/{id}", secure = True)