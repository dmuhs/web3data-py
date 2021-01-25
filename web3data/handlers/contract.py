"""This module contains the address subhandler."""

from typing import Dict

from web3data.chains import Chains
from web3data.handlers.base import BaseHandler


class ContractHandler(BaseHandler):
    """The subhandler for contract-related queries."""

    def __init__(self, initial_headers: Dict[str, str], chain: Chains):
        """Return a new :code:`ContractHandler` instance.

        :param initial_headers: Base headers to attach to every request
        :param chain: The blockchain to fetch the information for
        """

        super().__init__(chain)
        self.initial_headers = initial_headers
        self.base_url = "https://web3api.io/api/v2/contracts/{hash}/"

    def _contract_query(
        self,
        route: str,
        headers: Dict[str, str],
        params: Dict[str, str],
        address: str = "",
    ) -> Dict:
        """Helper method for contract-related API queries.

        :param route: The endpoint route to query
        :param headers: The headers to attach to the request
        :param params: The request's query parameters
        :param address: The contract address string to query for
        :return: The parsed API response
        """

        self._check_chain_supported()
        return self.raw_query(
            base_url=self.base_url.format(hash=address),
            route=route,
            headers=headers,
            params=params,
        )

    def audit(self, address: str, **kwargs) -> Dict:
        """Retrieves the vulnerabilities audit for the specified contract (if
        available).

        The automated security checks are provided by MythX. Check out their
        stellar service over at https://mythx.io/.

        :param address: The address to fetch information for
        :param kwargs: Additional query parameter options
        :return: The API response parsed into a dict
        """

        self._check_chain_supported()
        return self._contract_query(
            address=address,
            route="audit",
            headers=self.initial_headers,
            params=kwargs,
        )

    def details(self, address: str, **kwargs) -> Dict:
        """Retrieves all the detailed information for the specified contract
        (ABI, bytecode, sourcecode...).

        :param address: The address to fetch information for
        :param kwargs: Additional query parameter options
        :return: The API response parsed into a dict
        """

        self._check_chain_supported()
        return self._contract_query(
            address=address,
            route="",
            headers=self.initial_headers,
            params=kwargs,
        )

    def functions(self, address: str, **kwargs) -> Dict:
        """Retrieves the functions of the specified contract (if available).

        If not available on chain, the byte code is decompiled and a list
        of functions is extracted from it.

        :param address: The address to fetch information for
        :param kwargs: Additional query parameter options
        :return: The API response parsed into a dict
        """

        self._check_chain_supported()
        return self._contract_query(
            address=address,
            route="functions",
            headers=self.initial_headers,
            params=kwargs,
        )
