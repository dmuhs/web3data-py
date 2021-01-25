"""This module contains the API handler's base class."""

from json.decoder import JSONDecodeError
from typing import Dict, Union

import requests
from requests.compat import urljoin

from web3data.chains import Chains
from web3data.exceptions import APIError, EmptyResponseError


class BaseHandler:
    """The API handler base class.

    This class defines the basic methods of performing REST API endpoint queries as well as RPC
    queries, which are implemented across all handler classes to standardize API requests.
    """

    LIMITED = (
        Chains.BTC,
        Chains.BCH,
        Chains.BSV,
        Chains.LTC,
        Chains.ZEC,
    )

    def __init__(self, chain: Chains):
        self.chain = chain

    def _check_chain_supported(self):
        if self.chain in self.LIMITED:
            raise APIError(f"This method is not supported for {self.chain}")

    @staticmethod
    def raw_query(
        base_url: str,
        route: str,
        headers: Dict[str, str],
        params: Dict[str, str],
    ) -> Union[Dict, str]:
        """Perform an HTTP GET request on an API REST endpoint.

        :param base_url: The API base URL (common prefix)
        :param route: The endpoint route after the base (variable suffix)
        :param headers: Headers to attach to the API request
        :param params: Query parameters to attach to the URL
        :return: The API response parsed into a dict
        """
        resp = requests.get(
            url=urljoin(base_url, route), headers=headers, params=params
        )

        if not resp.content:
            # triggered if the API returns empty response body
            raise EmptyResponseError("The API returned an empty JSON response")

        if params.get("format", "") == "csv":
            return resp.text

        try:
            result = resp.json()
        except JSONDecodeError:
            # triggered e.g. when API returns empty response or XML error message
            raise APIError(f"Unable to parse API response to JSON: {resp.content}")
        if not result:
            # triggered if the API returns empty JSON object response
            raise EmptyResponseError("The API returned an empty JSON response")

        return result
