from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import apricatewrapper

@dataclass
class Magic:
    api: 'apricatewrapper.ApricateAPI'

    def rites(self) -> dict:
        '''Returns a list of all rites.

           Returns:
                dict: the response of the api call
        '''
        return self.api._get_request("/rites")

    def specific_rite(self, runic_symbol: str) -> dict:
        ''' Returns data on a specific rite.

            Args:
                runic_symbol (str): The symbol of the specific rite.

            Returns:
                dict: the response of the api call
        '''
        return self.api._get_request(f"/rites/{runic_symbol}")

    def cast_ritual(self, location_symbol: str, runic_symbol: str) -> dict:
        ''' Returns data on a specific rite.
        
            Requires auth token. 

            Args:
                location_symbol (str): The location where the ritual should be cast.
                runic_symbol (str): The symbol of the specific rite, that should be cast.

            Returns:
                dict: the response of the api call
        '''
        return self.api._patch_request(f"/my/farms/{location_symbol}/ritual/{runic_symbol}", secure = True)