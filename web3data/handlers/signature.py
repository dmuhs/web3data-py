"""This module contains the address subhandler."""

from typing import Dict

from web3data.chains import Chains
from web3data.handlers.base import BaseHandler


class SignatureHandler(BaseHandler):
    """The subhandler for signature-related queries."""

    def __init__(self, initial_headers: Dict[str, str], chain: Chains):
        """Return a new :code:`SignatureHandler` instance.

        :param initial_headers: Base headers to attach to every request
        :param chain: The blockchain to fetch the information for
        """

        super().__init__(chain)
        self.initial_headers = initial_headers
        self.base_url = "https://web3api.io/api/v2/signatures/"

    def details(self, signature: str) -> Dict:
        """Retrieves detailed information about the specified signature hash.

        :param signature: The signature string to look up
        :return: The API response parsed into a dict
        """

        self._check_chain_supported()
        return self.raw_query(
            base_url=self.base_url,
            route=signature,
            headers=self.initial_headers,
            params={},
        )
