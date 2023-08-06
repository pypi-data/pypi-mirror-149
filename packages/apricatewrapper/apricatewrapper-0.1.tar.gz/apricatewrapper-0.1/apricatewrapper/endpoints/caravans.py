from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import apricatewrapper

@dataclass
class Caravans:
    api: 'apricatewrapper.ApricateAPI'

    def my_caravans(self) -> dict:
        '''Returns a list of all caravans.
        
           Requires auth token. 

           Returns:
                dict: the response of the api call
        '''
        return self.api._get_request("/my/caravans", secure = True)

    def my_specific_caravan(self, id: int) -> dict:
        ''' Returns data on a specific caravan.
        
            Requires auth token. 

            Args:
                id (int): The id of the caravan.

            Returns:
                dict: the response of the api call
        '''
        return self.api._get_request(f"/my/caravans/{id}", secure = True)

    def charter_caravan(self, origin_symbol:str, destination_symbol:str, assistants:list[int], 
        tools:dict[str, int]=None, goods:dict[str, int]=None, produce:dict[str, int]=None, seeds:dict[str, int]=None) -> dict:
        ''' Assembles a caravan and starts the travel.
        
            Requires auth token. 

            Args:
                origin_symbol (str): The symbol of the location where the caravan starts.
                destination_symbol (str): The symbol of the location where the caravan is heading.
                assistants (list[int]): A list of assistant id's, which will be part of the caravan.
                tools (map[str, int], optional): The tools to bring along.
                goods (map[str, int], optional): The goods to bring along.
                produce (map[str, int], optional): The produce to bring along.
                seeds (map[str, int], optional): The seeds to bring along.

            Returns:
                dict: the response of the api call
        '''
        data = {
            "origin": origin_symbol,
            "destination": destination_symbol,
            "assistants": assistants
        }
        if tools or goods or produce or seeds:
            wares = {}
            if tools: wares["tools"] = tools
            if goods: wares["goods"] = goods
            if produce: wares["produce"] = produce
            if seeds: wares["seeds"] = seeds
            data["wares"] = wares
        return self.api._patch_request(f"/my/caravans", data, secure = True)
    
    def unpack_caravan(self, id: int) -> dict:
        ''' Unpacks the caravan, unloading assistants and resources.
        
            Requires auth token. 

            Args:
                id (int): The id of the caravan.

            Returns:
                dict: the response of the api call
        '''
        return self.api._delete_request(f"/my/caravans/{id}", secure = True)