import requests

from typing import Dict, Tuple
from urllib.parse import urljoin

from src.errors import ErrorApiConnexionError

class ApiHelper:
    """
        This class provide a class reference which may be used to call any API.
    """

    def __init__(self, root_api: str, default_query_params: Dict):
        self.__set_root_api(root_api)
        self.__set_default_query_params(default_query_params)

    @staticmethod
    def __build_query_params_uri(query_params: Dict):
        return '?' + '&'.join(
            [
                "{}={}".format(
                    key,
                    query_params[key]
                ) for key in query_params.keys()
            ]
        )

    def _get(self, ressource_path: str, path_param: Tuple = None, query_params: Dict = None):
        # First we define query params (which are the ones after the '?')
        if query_params is None:
            query_params = self.default_query_params
        else:
            query_params = dict(self.default_query_params, **query_params)
        query_params_str = ApiHelper.__build_query_params_uri(query_params)

        # the we build the complete path
        if path_param is None:
            url = urljoin(self.root_api, ressource_path) + query_params_str
        else:
            if type(path_param) is int:
                path_param = (path_param,)
            url = urljoin(self.root_api, ressource_path.format(*path_param)) + query_params_str

        print("Built url : {}".format(url))
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        elif response.status_code >= 400:
            raise ErrorApiConnexionError
        return None

    @property
    def root_api(self):
        return self.__root_api

    def __set_root_api(self, root_api: str):
        if type(root_api) is not str:
            raise TypeError("Root API should be a string")
        else:
            self.__root_api = root_api

    @property
    def default_query_params(self):
        return self.__default_query_params

    def __set_default_query_params(self, default_query_params: Dict):
        if type(default_query_params) is not dict:
            raise TypeError("Default query params API should be a dict")
        else:
            self.__default_query_params = default_query_params

    def get_trending(self, page=1):
        return self._get("trending/tv/week", None, {"page": page})

    ####
    # to be implemented methods by children classes
    ####
    def get_show(self, show_id: int):
        raise NotImplementedError

    def get_season(self, show_id: int, season_number: int):
        raise NotImplementedError

    def get_episode(self, show_id: int, season_number: int, episode_number: int):
        raise NotImplementedError

    def get_search(self, query: str):
        raise NotImplementedError

    def _api_json_search_to_show(self, result_json: Dict):
        raise NotImplementedError

    def _api_json_to_show(self, show_json: Dict):
        raise NotImplementedError

    def _api_json_to_season(self, season_json: Dict, id_show: int):
        raise NotImplementedError

    def _api_json_to_episode(self, episode_json: Dict):
        raise NotImplementedError
