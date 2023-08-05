from flask.testing import FlaskClient

from .schemas import LoginResponseSchema, LoginResponseData


class MyLassiApiClient:
    def __init__(self, server: str = 'https://api.mylassi.xyz/', api_token: str = None,
                 client=None, test: bool = False):
        self._test = test

        import requests
        if client is None:
            self._request = requests
        else:
            self._request = client

        if server[-1] == '/':
            server = server[:-1]
        self.__server = server

        self.token = api_token

    def _build_url(self, url) -> str:
        assert url[0] == '/', "The url must start with '/'"

        if self._test:
            return url

        return f'{self.__server}{url}'

    def post(self, url, request_data, content_type='application/json') -> dict:
        url = self._build_url(url)
        headers = dict()

        if self.token:
            headers['X-API-Key'] = self.token

        kwargs = {
            'headers': headers,
        }

        if content_type == 'application/json':
            kwargs['json'] = request_data
        else:
            kwargs['data'] = request_data

        response = self._request.post(url, **kwargs)

        if isinstance(response.json, dict):
            data: dict = response.json
        else:
            data: dict = response.json()

        if response.status_code != 200:
            raise Exception(data)

        return data

    def get(self, url, params=None) -> dict:
        url = self._build_url(url)
        headers = dict()

        if self.token:
            headers['X-API-Key'] = self.token

        kwargs = {
            'headers': headers,
        }

        if isinstance(self._request, FlaskClient):
            kwargs['query_string'] = params
        else:
            kwargs['params'] = params

        response = self._request.get(url, **kwargs)

        if isinstance(response.json, dict):
            data: dict = response.json
        else:
            data: dict = response.json()

        if response.status_code != 200:
            raise Exception(data)

        return data

    def login(self, username: str, password: str) -> LoginResponseData:
        response = self.post('/api/v2/login', {
            'username': username,
            'password': password,
        })

        response_data: LoginResponseData = LoginResponseSchema.load(response)

        self.token = response_data.token

        return response_data
