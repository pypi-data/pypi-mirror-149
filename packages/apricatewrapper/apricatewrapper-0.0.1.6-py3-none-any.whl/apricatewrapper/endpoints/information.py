from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import apricatewrapper

@dataclass
class Information:
    api: 'apricatewrapper.ApricateAPI'

    def about(self) -> dict:
        '''Returns a info about other /about endpoints.

           Returns:
                dict: the response of the api call
        '''
        return self.api._get_request("/about")

    def about_sizes(self) -> dict:
        '''Returns a info about plots and crop sizes.

           Returns:
                dict: the response of the api call
        '''
        return self.about("/about/sizes")

    def about_magic(self) -> dict:
        '''Returns a info about magic and rites.

           Returns:
                dict: the response of the api call
        '''
        return self.about("/about/magic")

    def about_plants(self) -> dict:
        '''Returns a info about plants.

           Returns:
                dict: the response of the api call
        '''
        return self.about("/about/plants")

    def about_world(self) -> dict:
        '''Returns a info about lore of the world, the player and the grouping of locations.

           Returns:
                dict: the response of the api call
        '''
        return self.about("/about/world")