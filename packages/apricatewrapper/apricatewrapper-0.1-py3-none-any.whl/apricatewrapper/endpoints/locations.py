from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import apricatewrapper

@dataclass
class Locations:
    api: 'apricatewrapper.ApricateAPI'

    def islands(self) -> dict:
        '''Returns a list of all islands.

           Returns:
                dict: the response of the api call
        '''
        return self.api._get_request("/islands")

    def specific_island(self, location_symbol: str) -> dict:
        ''' Returns data on a specific island.

            Args:
                location_symbol (str): The symbol of the specific location.

            Returns:
                dict: the response of the api call
        '''
        return self.api._get_request(f"/islands/{location_symbol}")

    def regions(self) -> dict:
        '''Returns a list of all regions.

           Returns:
                dict: the response of the api call
        '''
        return self.api._get_request("/regions")

    def specific_region(self, location_symbol: str) -> dict:
        ''' Returns data on a specific region.

            Args:
                location_symbol (str): The symbol of the specific location.

            Returns:
                dict: the response of the api call
        '''
        return self.api._get_request(f"/regions/{location_symbol}")

    def my_locations(self) -> dict:
        '''Returns a list of all locations visible through fog of war.

           Returns:
                dict: the response of the api call
        '''
        return self.api._get_request("/my/locations", secure = True)
    
    def my_specific_location(self, location_symbol: str) -> dict:
        ''' Returns data on a specific location visible through fog of war.

            Args:
                location_symbol (str): The symbol of the specific location.

            Returns:
                dict: the response of the api call
        '''
        return self.api._get_request(f"/my/locations/{location_symbol}", secure = True)

    def my_nearby_locations(self) -> dict:
        '''Returns a list of all locations visible through fog of war, with sub-maps of locations on those islands.

           Returns:
                dict: the response of the api call
        '''
        return self.api._get_request("/my/nearby-locations", secure = True)