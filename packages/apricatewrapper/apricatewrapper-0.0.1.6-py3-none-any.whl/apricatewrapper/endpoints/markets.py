from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import apricatewrapper

@dataclass
class Markets:
    api: 'apricatewrapper.ApricateAPI'

    def my_markets(self) -> dict:
        '''Returns a list of all markets visible to the user.
        
           Requires auth token. 

           Returns:
                dict: the response of the api call
        '''
        return self.api._get_request("/my/markets", secure = True)

    def my_specific_market(self, location_symbol: str) -> dict:
        ''' Returns data on a specific market visible to the user.
        
            Requires auth token. 

            Args:
                location_symbol (str): The symbol of the specific market.

            Returns:
                dict: the response of the api call
        '''
        return self.api._get_request(f"/my/markets/{location_symbol}", secure = True)

    def place_market_order(self, location_symbol: str, transaction_type: str, item_category: str, item_name: str, quantity: int, order_type: str = "MARKET") -> dict:
        ''' Places an order at the given market, with the given order information.
        
            Requires auth token. 

            Args:
                location_symbol (str): The symbol of the market, where the order should be placed.
                transaction_type (str): The type of transaction. values=[BUY|SELL]
                item_category (str): The category of the item. values=[TOOLS|GOODS|PRODUCE|SEEDS]
                item_name (str): The name of the item.
                quantity (int): The amount of the item.
                order_type (str): The type of the order. values=[MARKET]

            Returns:
                dict: the response of the api call
        '''
        data = {
            "order_type": order_type,
            "transaction_type": transaction_type,
            "item_category": item_category,
            "item_name": item_name,
            "quantity": quantity
        }
        return self.api._patch_request(f"/my/markets/{location_symbol}/order", data, secure = True)