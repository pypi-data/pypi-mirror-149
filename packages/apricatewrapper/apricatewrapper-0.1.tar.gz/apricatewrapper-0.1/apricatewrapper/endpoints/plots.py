from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import apricatewrapper

@dataclass
class Plots:
    api: 'apricatewrapper.ApricateAPI'

    def __format_id(self, location_symbol:str, plot_id: int):
        return f"{location_symbol}!Plot-{plot_id}"

    def my_plots(self) -> dict:
        '''Returns a list of all plots for the user.
        
           Requires auth token. 

           Returns:
                dict: the response of the api call
        '''
        return self.api._get_request("/my/plots", secure = True)

    def my_specific_plot(self, location_symbol: str, plot_id: int) -> dict:
        ''' Returns data on a specific plot.
        
            Requires auth token. 

            Args:
                location_symbol (str): The location of the plot.
                plot_id (int): The id of the plot.

            Returns:
                dict: the response of the api call
        '''
        id = self.__format_id(location_symbol, plot_id)
        return self.api._post_request(f"/my/plots/{id}", secure = True)

    def my_plot_plant(self, location_symbol: str, plot_id: int, name: str, quantity: int, size: str) -> dict:
        ''' Plants seeds on a plot.
        
            Requires auth token. 

            Args:
                location_symbol (str): The location of the plot.
                plot_id (int): The id of the plot.
                name (str): The name of the plant to plant.
                quantity (int): The amount to plant.
                size (str): The size of the seeds to plant.

            Returns:
                dict: the response of the api call
        '''
        id = self.__format_id(location_symbol, plot_id)
        data = {
            "name":name,
            "quantity":quantity,
            "size":size
        }
        return self.api._post_request(f"/my/plots/{id}/plant", data, secure = True)
    
    def my_plot_clear(self, location_symbol: str, plot_id: int) -> dict:
        ''' Clears a plot.
        
            Requires auth token. 

            Args:
                location_symbol (str): The location of the plot.
                plot_id (int): The id of the plot.

            Returns:
                dict: the response of the api call
        '''
        id = self.__format_id(location_symbol, plot_id)
        return self.api._put_request(f"/my/plots/{id}/clear", secure = True)

    def my_plot_interact(self, location_symbol: str, plot_id: int, action: str, consumable: str = None) -> dict:
        ''' Interacts with a plot.
        
            Requires auth token. 

            Args:
                location_symbol (str): The location of the plot.
                plot_id (int): The id of the plot.
                action (str): The action to do with the plot.
                consumable (str, optional): The consumable to use with the action.

            Returns:
                dict: the response of the api call
        '''
        id = self.__format_id(location_symbol, plot_id)
        data = {"action":action}
        if consumable is not None:
            data["consumable"] = consumable
        return self.api._patch_request(f"/my/plots/{id}/interact", data, secure = True)
