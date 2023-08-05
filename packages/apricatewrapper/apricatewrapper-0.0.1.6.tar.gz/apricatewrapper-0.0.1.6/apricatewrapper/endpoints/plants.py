from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import apricatewrapper

@dataclass
class Plants:
    api: 'apricatewrapper.ApricateAPI'

    def plants(self) -> dict:
        '''Returns a list of all plants.

           Returns:
                dict: the response of the api call
        '''
        return self.api._get_request(f"/plants")

    def specific_plant(self, name: str) -> dict:
        ''' Returns data on a specific plant. 

            Args:
                name (str): The name of the specific plant.

            Returns:
                dict: the response of the api call
        '''
        return self.api._get_request(f"/plants/{name}")

    def specific_plant_growthstage(self, name: str, stage: int) -> dict:
        ''' Returns data on a specific growthstage, for a specific plant. 

            Args:
                name (str): The name of the specific plant.
                stage (int): The index of the growthstage

            Returns:
                dict: the response of the api call
        '''
        return self.api._get_request(f"/plants/{name}/stage/{stage}")