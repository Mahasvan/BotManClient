import json

import aiohttp


class Internet:
    def __init__(self, host: str, port: int):
        self.session = aiohttp.ClientSession(trust_env=True)
        self.host = host
        self.port = port

    def url_builder(self, endpoint: str):
        return f"http://{self.host}:{self.port}/{endpoint.lstrip('/')}"

    async def get_text(self, endpoint: str, **kwargs):
        url = self.url_builder(endpoint)
        async with self.session.get(url, **kwargs) as response:
            response = (await response.content.read()).decode('utf-8')
        return response

    async def get_binary(self, endpoint: str, **kwargs):
        url = self.url_builder(endpoint)
        async with self.session.get(url, **kwargs) as response:
            response = (await response.content.read())
        return response

    async def get_json(self, endpoint: str, **kwargs):
        url = self.url_builder(endpoint)
        async with self.session.get(url, **kwargs) as response:
            response = (await response.json())

        return response

    async def post(self, endpoint: str, data: dict = None, params: dict = None):
        url = self.url_builder(endpoint)
        async with self.session.post(url, data=data, params=params) as response:
            response = (await response.content.read()).decode('utf-8')
        return response

    async def post_binary(self, endpoint: str, data: dict = None, params: dict = None):
        url = self.url_builder(endpoint)
        async with self.session.post(url, data=data, params=params) as response:
            response = (await response.content.read())
        return response

    async def post_json(self, endpoint: str, headers: dict = None, data: dict = None, params: dict = None):
        url = self.url_builder(endpoint)
        async with self.session.post(url, headers=headers, data=data, params=params) as response:
            response = (await response.json())
            # todo: response might be "Internal Server Error"
        return response
