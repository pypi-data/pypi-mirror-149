from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import apricatewrapper

@dataclass
class Metrics:
    api: 'apricatewrapper.ApricateAPI'

    def users(self) -> dict:
        '''Returns a list of all users.

           Returns:
                dict: the response of the api call
        '''
        return self.api._get_request("/users")

    def metrics(self) -> dict:
        '''Returns a list of various server metrics.

           Returns:
                dict: the response of the api call
        '''
        return self.api._get_request("/metrics")