"""This module contains the address subhandler."""

from typing import Any, Dict

from web3data.chains import Chains
from web3data.handlers.base import BaseHandler


class BlockHandler(BaseHandler):
    """The subhandler for block-related queries."""

    def __init__(self, initial_headers: Dict[str, str], chain: Chains):
        """Return a new :code:`BlockHandler` instance.

        :param initial_headers: Base headers to attach to every request
        :param chain: The blockchain to fetch the information for
        """

        super().__init__(chain)
        self.initial_headers = initial_headers
        self.base_url = "https://web3api.io/api/v2/blocks/{id}/"

    def _block_query(
        self,
        route: str,
        headers: Dict[str, str],
        params: Dict[str, Any],
        block_id: str = "",
    ) -> Dict:
        """Helper method for block-related API queries.

        :param route: The endpoint route to query
        :param headers: The headers to attach to the request
        :param params: The request's query parameters
        :param block_id: The block ID to query for
        :return: The parsed API response
        """
        return self.raw_query(
            base_url=self.base_url.format(id=block_id),
            route=route,
            headers=headers,
            params=params,
        )

    def single(self, block_id: str, **kwargs) -> Dict:
        """Retrieves the block specified by its id (number or hash).

        :param block_id: The block's ID to fetch information for
        :key validationMethod: The validation method to be added to the response: none, basic, full.
            Default: none. (str)
        :key timeFormat: The time format to use for the timestamps (milliseconds, ms, iso, iso8611). (str)
        :return: The API response parsed into a dict
        """
        return self._block_query(
            block_id=block_id,
            route="",
            headers=self.initial_headers,
            params=kwargs,
        )

    def total(self, **kwargs) -> Dict:
        """Retrieves all the blocks within the specified range.

        :key startNumber: The range of blocks to return, inclusive (startNumber and endNumber
            should be both specified, or both empty) (str)
        :key endNumber: The end of the range of blocks to return, exclusive (startNumber and endNumber
            should be both specified, or both empty) (str)
        :key size: The number of results to return. (int)
        :key validationMethod: The validation method to be added to the response:
            none, basic, full. Default: none. (str)
        :return: The API response parsed into a dict
        """
        return self._block_query(route="", headers=self.initial_headers, params=kwargs)

    def functions(self, block_id: str, **kwargs) -> Dict:
        """Retrieves all the functions which were called at the specified block
        number or hash.

        :param block_id: The block's ID to fetch information for
        :key validationMethod: The validation method to be added to the response:
            none, basic, full. Default: none. (str)
        :return: The API response parsed into a dict
        """

        self._check_chain_supported()
        return self._block_query(
            block_id=block_id,
            route="functions",
            headers=self.initial_headers,
            params=kwargs,
        )

    def logs(self, block_id: str, **kwargs) -> Dict:
        """Retrieves all the logs at the specified block number or hash.

        :param block_id: The block's ID to fetch information for
        :key validationMethod: The validation method to be added to the response:
            none, basic, full. Default: none. (str)
        :key transactionHash: Filter by logs for this transaction. (str)
        :return: The API response parsed into a dict
        """

        self._check_chain_supported()
        return self._block_query(
            block_id=block_id,
            route="logs",
            headers=self.initial_headers,
            params=kwargs,
        )

    def token_transfers(self, block_id: str, **kwargs) -> Dict:
        """Retrieves all the token which were transferred at the specified
        block number.

        :param block_id: The block's ID to fetch information for
        :key amount: Filter by tokens transfers where the number of tokens is equal
            to the specified amount. (int)
        :key amountGt: Filter by token transfers where the number of tokens is more than
            the specified amount. (int)
        :key amountGte: Filter by token transfers where the number of tokens is more
            than or equal to the specified amount. (int)
        :key amountLt: Filter by token transfers where the number of tokens is less
            than the specified amount. (int)
        :key amountLte: Filter by token transfers where the number of tokens is less
            than or equal to the specified amount. (int)
        :key from: Filter by token transfers originating from this address. (str)
        :key to: Filter token transfers received by this address. (str)
        :key tokenAddress: Filter by token transfers for this token. (str)
        :key transactionHash: Filter by token transfers for this transaction. (str)
        :key includePrice: Indicates whether or not to include price data with the results. (bool)
        :key currency: The currency of the price information. Options: usd, btc.
            Only used in conjunction with includePrice. (str)
        :return: The API response parsed into a dict
        """

        self._check_chain_supported()
        return self._block_query(
            block_id=block_id,
            route="token-transfers",
            headers=self.initial_headers,
            params=kwargs,
        )

    def transactions(self, block_id: str, **kwargs) -> Dict:
        """Retrieves all the transactions included in a specified block id.

        :param block_id: The block's ID to fetch information for
        :key includeFunctions: Indicates whether or not to include functions (aka internal messages)
            information for each transaction, if available. Options: true, false. (bool)
        :key includeTokenTransfers: Indicates whether or not to include token transfers information
            for each transaction, if available. Options: true, false. (bool)
        :key includeLogs: Indicates whether or not to include log information for each transaction,
            if available. Options: true, false. (bool)
        :key validationMethod: The validation method to be added to the response: none, basic, full.
            Default: none. (str)
        :key currency: The currency of the price information. Options: usd, btc. Only used in
            conjunction with includePrice. (str)
        :key includePrice: Indicates whether or not to include price data with the results.
            Options: true, false. (bool)
        :key startDate: Filter by transactions executed after this date. Note that the interval
            can not exceed 1 minute (startDate and endDate should be both specified, or both empty) (int)
        :key endDate: Filter by transactions executed before this date. Note that the interval
            can not exceed 1 minute (startDate and endDate should be both specified, or both empty). (int)
        :key size: The number of results to return. (int)
        :return: The API response parsed into a dict
        """
        return self._block_query(
            block_id=block_id,
            route="transactions",
            headers=self.initial_headers,
            params=kwargs,
        )

    def metrics_latest(self, **kwargs) -> Dict:
        """Get metrics for recent confirmed blocks for a given blockchain.

        :key timeFormat: The time format to use for the timestamps (milliseconds, ms, iso, iso8611). (str)
        :return: The API response parsed into a dict
        """
        return self._block_query(
            route="metrics/latest", headers=self.initial_headers, params=kwargs
        )

    def metrics_historical(self, **kwargs) -> Dict:
        """Get metrics for historical confirmed blocks for a given blockchain.

        :key timeFormat: The time format to use for the timestamps (milliseconds, ms, iso, iso8611). (str)
        :key timeFrame: time frame to return the historical data in, options: (1m, 5m, 1h, 1d, 1w) (str)
        :key startDate: Filter by data after this date. (str)
        :key endDate: Filter by data before this date. (str)
        :return: The API response parsed into a dict
        """
        return self._block_query(
            route="metrics/historical",
            headers=self.initial_headers,
            params=kwargs,
        )
