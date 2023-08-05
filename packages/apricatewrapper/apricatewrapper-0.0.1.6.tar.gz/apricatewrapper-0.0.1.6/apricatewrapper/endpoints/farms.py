from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import apricatewrapper

@dataclass
class Farms:
    api: 'apricatewrapper.ApricateAPI'

    def my_farms(self) -> dict:
        '''Returns a list of all farms.
        
           Requires auth token. 

           Returns:
                dict: the response of the api call
        '''
        return self.api._get_request("/my/farms", secure = True)

    def my_specific_farm(self, location_symbol: str) -> dict:
        ''' Returns data on a specific farm.
        
            Requires auth token. 

            Args:
                id (int): The id of the farm.

            Returns:
                dict: the response of the api call
        '''
        return self.api._get_request(f"/my/farms/{location_symbol}", secure = True)