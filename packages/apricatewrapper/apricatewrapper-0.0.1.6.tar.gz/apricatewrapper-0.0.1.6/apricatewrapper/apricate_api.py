import requests
from dataclasses import dataclass
from apricatewrapper.endpoints import Information, Metrics, Locations, Warehouses, Users, Quests, Plots, Plants, Markets, Magic, Farms, Caravans, Assistants

class MissingAuthTokenException(Exception):
    pass

@dataclass
class ApricateAPI:

    def __init__(self):
        self.base_url = 'https://apricate.io/api'
        self._auth_token: str = None
        self.assistants = Assistants(self)
        self.caravans = Caravans(self)
        self.farms = Farms(self)
        self.information = Information(self)
        self.locations = Locations(self)
        self.magic = Magic(self)
        self.markets = Markets(self)
        self.metrics = Metrics(self)
        self.plants = Plants(self)
        self.plots = Plots(self)
        self.quests = Quests(self)
        self.users = Users(self)
        self.warehouses = Warehouses(self)

    def set_token(self, token):
        self._auth_token = token

    def has_auth_token(self) -> bool:
        return self._auth_token is not None

    def __headers(self, secure:bool):
        if secure and self._auth_token is None:
            raise MissingAuthTokenException

        return {'Authorization': f'Bearer {self._auth_token}'} if secure else None

    def _get_request(self, endpoint: str, secure:bool = False) -> dict:
        url = self.base_url + endpoint
        header = self.__headers(secure)
        r = requests.get(url, headers=header)
        return r.json()

    def _post_request(self, endpoint: str, data: dict = None, secure:bool = False) -> dict:
        url = self.base_url + endpoint
        header = self.__headers(secure)
        r = requests.post(url, headers=header, data=data)
        return r.json()

    def _patch_request(self, endpoint: str, data: dict = None, secure:bool = False) -> dict:
        url = self.base_url + endpoint
        header = self.__headers(secure)
        r = requests.patch(url, headers=header, data=data)
        return r.json()

    def _put_request(self, endpoint: str, secure:bool = False) -> dict:
        url = self.base_url + endpoint
        header = self.__headers(secure)
        r = requests.post(url, headers=header)
        return r.json()

    def _delete_request(self, endpoint: str, secure:bool = False) -> dict:
        url = self.base_url + endpoint
        header = self.__headers(secure)
        r = requests.delete(url, headers=header)
        return r.json()

    