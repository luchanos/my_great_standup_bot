from typing import Union

import requests


class TelegramClient:
    def __init__(self, token: str, base_url: str):
        self.token = token
        self.base_url = base_url

    @staticmethod
    def prepare_data_and_params(data: Union[None, dict], params: Union[None, dict]) -> tuple:
        if params is None:
            params = {}
        if data is None:
            data = {}
        return params, data

    def prepare_url(self, method: str):
        result_url = f"{self.base_url}/bot{self.token}/"
        if method != "":
            result_url += method
        return result_url

    def post(self, method: str = "", params: dict = None, data: dict = None):
        params, data = self.prepare_data_and_params(params=params, data=data)
        url = self.prepare_url(method)
        resp = requests.post(url, params=params, data=data)
        return resp.json()

    def get(self, method: str = "", params: dict = None, data: dict = None):
        params, data = self.prepare_data_and_params(params=params, data=data)
        url = self.prepare_url(method)
        resp = requests.get(url, params=params, data=data)
        return resp.json()


token = "5499043180:AAEmbgJJ5shiKCQ9KnvN5S-2yAfw3PhBVuU"
telegram_client = TelegramClient(token, base_url="https://api.telegram.org")
my_params = {"chat_id": 362857450, "text": "sampleTEXT"}
my_data = {"chat_id": 362857450, "text": "sampleTEXT"}
telegram_client.post(method="sendMessage", params=my_params, data=my_data)
