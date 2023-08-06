from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import apricatewrapper

@dataclass
class Warehouses:
    api: 'apricatewrapper.ApricateAPI'

    def my_warehouses(self) -> dict:
        '''Returns a list of all warehouses for the user.
        
           Requires auth token. 

           Returns:
                dict: the response of the api call
        '''
        return self.api._get_request("/my/warehouses", secure = True)

    def my_specific_warehouse(self, location_symbol: str) -> dict:
        ''' Returns data on a specific warehouse.
        
            Requires auth token. 

            Args:
                location_symbol (str): The location of the warehouse.

            Returns:
                dict: the response of the api call
        '''
        return self.api._get_request(f"/my/warehouses/{location_symbol}", secure = True)