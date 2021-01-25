"""This module contains the address subhandler."""

from typing import Dict

from web3data.chains import Chains
from web3data.handlers.base import BaseHandler


class TransactionHandler(BaseHandler):
    """The subhandler for transaction-related queries."""

    def __init__(self, initial_headers: Dict[str, str], chain: Chains):
        """Return a new :code:`TranscationHandler` instance.

        :param initial_headers: Base headers to attach to every request
        :param chain: The blockchain to fetch the information for
        """

        super().__init__(chain)
        self.initial_headers = initial_headers
        self.base_url = "https://web3api.io/api/v2/transactions/"

    def information(self, tx_hash: str, **kwargs) -> Dict:
        """Retrieves the transaction information for the specified hash.

        :param tx_hash: The transaction hash to fetch information for
        :key validationMethod: The validation method to be added to the response:
            none, basic, full. Default: none. (str)
        :key includePrice: Indicates whether or not to include price data with the results.
            Options: true, false. (bool)
        :key currency: The currency of the price information (usd or btc.)
            - only used in conjunction with includePrice. (str)
        :return: The API response parsed into a dict
        """
        return self.raw_query(
            base_url=self.base_url,
            route=tx_hash,
            headers=self.initial_headers,
            params=kwargs,
        )

    def token_transfers(self, tx_hash: str) -> Dict:
        """Retrieves the token transfers that took place in the specified
        transaction.

        :param tx_hash: The transaction hash to fetch information for
        :return: The API response parsed into a dict
        """

        self._check_chain_supported()
        return self.raw_query(
            base_url=self.base_url,
            route=f"{tx_hash}/token-transfers",
            headers=self.initial_headers,
            params={},
        )

    def find(self, **kwargs) -> Dict:
        """Retrieves all transactions matching the specified filters.

        :key status: Filter by the status of the transactions to retrieve
            (all, completed, failed, pending). (str)
        :key startDate: Filter by transactions executed after this date. Note that the interval
            can not exceed 1 minute (startDate and endDate should be both specified, or both empty) (int)
        :key endDate: Filter by transactions executed before this date. Note that the interval
            can not exceed 1 minute (startDate and endDate should be both specified, or both empty). (int)
        :key validationMethod: The validation method to be added to the response:
            none, basic, full. Default: none. (str)
        :key includePrice: Indicates whether or not to include price data with the results.
            Options: true, false. (bool)
        :key currency: The currency of the price information (usd or btc.)
            - only used in conjunction with includePrice. (str)
        :key size: The number of results to return. (int)
        :key includeFunctions: Indicates whether or not to include log
            information for each transaction, if available (false|true) (bool)
        :key includeLogs: Indicates whether or not to include price information (false|true) (bool)
        :key includeTokenTransfers: Indicates whether or not to include token
            transfers information for each transaction, if available (false|true) (bool)
        :return: The API response parsed into a dict
        """
        return self.raw_query(
            base_url=self.base_url,
            route="",
            headers=self.initial_headers,
            params=kwargs,
        )

    def gas_percentiles(self, **kwargs) -> Dict:
        """Retrieves the latest gas price percentiles for the transactions.

        :key numBlocks: Number of past blocks on which to base the percentiles. (int)
        :return: The API response parsed into a dict
        """
        self._check_chain_supported()
        return self.raw_query(
            base_url=self.base_url,
            route="gas/percentiles",
            headers=self.initial_headers,
            params=kwargs,
        )

    def gas_predictions(self) -> Dict:
        """Retrieves the latest gas predictions for the transactions.

        :return: The API response parsed into a dict
        """
        self._check_chain_supported()
        return self.raw_query(
            base_url=self.base_url,
            route="gas/percentiles",
            headers=self.initial_headers,
            params={},
        )

    def metrics(self) -> Dict:
        """Get metrics for recent confirmed transactions for a given
        blockchain.

        :return: The API response parsed into a dict
        """
        return self.raw_query(
            base_url=self.base_url,
            route="metrics/latest",
            headers=self.initial_headers,
            params={},
        )

    def volume(self, **kwargs) -> Dict:
        """Retrieves the historical (time series) volume of transactions.

        :param kwargs: Additional query parameter options
        :key timeFormat: The time format to use for the timestamps: milliseconds/ms or iso/iso861. (str)
        :key timeFrame: The time frame to return the historical data in:
            by day (1d, 2d, ..., all),
            by hour (1h, 2h, ..., 72h) or
            by minute (1m, 2m, ..., 360m) (str)
        :return: The API response parsed into a dict
        """
        return self.raw_query(
            base_url=self.base_url,
            route="volume",
            headers=self.initial_headers,
            params=kwargs,
        )
