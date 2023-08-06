from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import apricatewrapper

@dataclass
class Quests:
    api: 'apricatewrapper.ApricateAPI'

    def my_contracts(self) -> dict:
        '''Returns a list of all contracts.
        
           Requires auth token. 

           Returns:
                dict: the response of the api call
        '''
        return self.api._get_request("/my/contracts", secure = True)

    def my_specific_contract(self, id: int) -> dict:
        ''' Returns data on a specific contract.
        
            Requires auth token. 

            Args:
                id (int): The id of the contract.

            Returns:
                dict: the response of the api call
        '''
        return self.api._get_request(f"/my/contracts/{id}", secure = True)