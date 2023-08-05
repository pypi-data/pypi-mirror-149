"""Main module."""
import requests
from loguru import logger

from typing import Dict


class TiingoNewsAPI:
    def __init__(self, api_token: str):
        """
        Init
        @param api_token:
        @type api_token:
        """
        self.headers = {"Content-Type": "application/json"}

        self.base_url = "https://api.tiingo.com/tiingo"
        self.payload = {"token": api_token}

    def get_tiingo_data(self, api_endpoint: str, **kwargs) -> Dict:
        """

        @param api_endpoint:
        @type api_endpoint:
        @param kwargs:
        @type kwargs:
        @return:
        @rtype:
        """
        params = {**self.payload, **kwargs}
        response = requests.get(api_endpoint, headers=self.headers, params=params)

        if response.status_code == 200:
            logger.info("Request successful")
            return response.json()
        else:
            logger.error("Request error")
            logger.error(response.status_code)
            raise ConnectionError(response)

    def get_news(self, **kwargs) -> Dict:
        """

        @param kwargs:
        @type kwargs:
        @return:
        @rtype:
        """
        api_endpoint = f"{self.base_url}/news"
        data = self.get_tiingo_data(api_endpoint, **kwargs)
        return data

    def get_eod_metadata(self, ticker: str) -> Dict:
        """

        @param ticker:
        @type ticker:
        @return:
        @rtype:
        """
        api_endpoint = f"{self.base_url}/daily/{ticker}"
        data = self.get_tiingo_data(api_endpoint)
        return data

    def get_eod_latest_price(self, ticker: str) -> Dict:
        """

        @param ticker:
        @type ticker:
        @return:
        @rtype:
        """
        api_endpoint = f"{self.base_url}/daily/{ticker}/prices"
        data = self.get_tiingo_data(api_endpoint)
        return data

    def get_crypto(self, endpoint: str = "", **kwargs):
        """

        @param endpoint: Defines endpoint to hit, if left blank will hit base endpoint,
        other current available endpoints are `prices`/`top`.
        Top returns top of book data, prices returns latest price.
        @type endpoint: str
        @param kwargs:
        @type kwargs:
        @return:
        @rtype:
        """
        if endpoint != "":
            api_endpoint = f"{self.base_url}/crypto/{endpoint}"
        else:
            api_endpoint = f"{self.base_url}/crypto/"
        data = self.get_tiingo_data(api_endpoint, **kwargs)
        return data

    def get_iex(self, ticker: str = "", **kwargs) -> Dict:
        """

        @param ticker:
        @type ticker:
        @param kwargs:
        @type kwargs:
        @return:
        @rtype:
        """
        if ticker != "":
            api_endpoint = f"{self.base_url}/iex/{ticker}"
        else:
            api_endpoint = f"{self.base_url}/iex/"
        data = self.get_tiingo_data(api_endpoint, **kwargs)
        return data
