"""This module contains the address subhandler."""

from typing import Any, Dict, List

from web3data.chains import Chains
from web3data.handlers.base import BaseHandler


class AddressHandler(BaseHandler):
    """The subhandler for address-related queries."""

    def __init__(self, initial_headers: Dict[str, str], chain: Chains):
        """Return a new :code:`AddressHandler` instance.

        :param initial_headers: Base headers to attach to every request
        :param chain: The blockchain to fetch the information for
        """

        super().__init__(chain=chain)
        self.initial_headers = initial_headers
        self.chain = chain
        self.base_url = "https://web3api.io/api/v2/addresses/{hash}/"

    def _address_query(
        self,
        route: str,
        headers: Dict[str, str],
        params: Dict[str, Any],
        address: str = "",
    ) -> Dict:
        """Base method to perform address queries.

        :param route: The endpoint route to query
        :param headers: The headers to attach to the request
        :param params: The request's query parameters
        :param address: The address string to query for
        :return: The parsed API response
        """
        return self.raw_query(
            base_url=self.base_url.format(hash=address),
            route=route,
            headers=headers,
            params=params,
        )

    def total(self, **kwargs) -> Dict:
        """Retrieves every Ethereum address that has been seen on the network.

        :key hash: Filter by a specific address (str)
        :key blockNumber: Filter by addresses first encountered at this block number (int)
        :key blockNumberGt: Filter by addresses first encountered after this block number,
            not including this blocknumber (int)
        :key blockNumberGte: Filter by addresses first encountered after this block number,
            including this block number (str)
        :key blockNumberLt: Filter by addresses first encountered before this block number,
            not including this block number (int)
        :key blockNumberLte: Filter by addresses first encountered before this block number,
            including this block number (str)
        :key startDate: Filter by addresses first encountered after this date (int)
        :key endDate: Filter by addresses first encountered after before date (int)
        :key type: Filter by addresses of the specified type (EOA or CONTRACT) (str)
        :key transactionHash: Filter by addresses first encountered at this transaction hash (str)
        :key page: The page number to return. (int)
        :key size: Number of records per page. (int)
        :return: The API response parsed into a dict
        """
        return self._address_query(
            route="", headers=self.initial_headers, params=kwargs
        )

    def adoption(self, address: str, **kwargs) -> Dict:
        """Retrieves the historical adoption for the specified address.

        :param address: The address to fetch information for
        :key timeFormat: The time format to use with the timestamps: milliseconds/ms or iso/iso8611 (str)
        :key timeFrame: The time frame to return the historical data in (str):
            by day (1d, 2d, ..., all),
            by hour (1h, 2h, ..., 72h) or
            by minute (1m, 2m, ..., 360m)
        :key timePeriod: The time period (in minutes) to aggregate the historical data (str)
        :return: The API response parsed into a dict
        """
        return self._address_query(
            address=address,
            route="adoption",
            headers=self.initial_headers,
            params=kwargs,
        )

    def balance_historical(self, address: str, **kwargs) -> Dict:
        """Retrieves the historical (time series) account balances for the
        specified address.

        :param address: The address to fetch information for
        :key blockNumber: Filter by account balances at block number (int)
        :key startDate: Filter by account balances which happened after this date (int)
        :key endDate: Filter by account balances which happened before this date (int)
        :key value: Filter by account balances where the balance is equal to this value (int)
        :key valueGt: Filter by account balances where the balance is greater than this value (int)
        :key valueGte: Filter by account balances where the balance is greater than or equal to this value (int)
        :key valueLt: Filter by account balances where the balance is less than this value (int)
        :key valueLte: Filter by account balances where the balance is less than or equal to this value (int)
        :key includePrice: Indicates whether or not to include price data with the results. Options: true, false. (bool)
        :key currency: The currency of the price information (usd or btc.)
            - only used in conjunction with includePrice. (str)
        :key page: The page number to return. (int)
        :key size: Number of records per page (int)
        :return: The API response parsed into a dict
        """
        return self._address_query(
            address=address,
            route="account-balances/historical",
            headers=self.initial_headers,
            params=kwargs,
        )

    def balance_latest(self, address: str, **kwargs) -> Dict:
        """Retrieves the current account balance for the specified address.

        :param address: The address to fetch information for
        :key includePrice: Indicates whether or not to include price data with the results. Options: true, false. (str)
        :key currency: The currency of the price information. Options: usd, btc.
            Only used in conjunction with includePrice. (str)
        :return: The API response parsed into a dict
        """
        return self._address_query(
            address=address,
            route="account-balances/latest",
            headers=self.initial_headers,
            params=kwargs,
        )

    def balances_batch(self, addresses: List[str], **kwargs) -> Dict:
        """Retrieves the latest account and token balances for the specified
        addresses.

        This is super useful if you want to get an entire portfolio's summary in a single call.
        Get totals for ETH & all token amounts with market prices.

        :param addresses: The addresses to fetch information for
        :key includePrice: Indicates whether or not to include price data with the results.
            Options: true, false. (bool)
        :key currency: The currency of the price information (usd or btc.)
            - only used in conjunction with includePrice. (str)
        :key timeFormat: The time format to use for the timestamps (milliseconds, ms, iso, iso8611). (str)
        :return: The API response parsed into a dict
        """
        kwargs.update({"addresses": ",".join(addresses)})
        return self._address_query(
            route="balances", headers=self.initial_headers, params=kwargs
        )

    def balances(self, address: str, **kwargs) -> Dict:
        """Retrieves the latest account and token balances for the specified
        address.

        :param address: The address to fetch information for
        :key includePrice: Indicates whether or not to include price data with the results.
            Options: true, false. (bool)
        :key currency: The currency of the price information (usd or btc.)
            - only used in conjunction with includePrice. (str)
        :key timeFormat: The time format to use for the timestamps (milliseconds, ms, iso, iso8611). (str)
        :return: The API response parsed into a dict
        """
        return self._address_query(
            address=address,
            route="balances",
            headers=self.initial_headers,
            params=kwargs,
        )

    def information(self, address: str, **kwargs) -> Dict:
        """Retrieves information about the specified address.

        This includes network(s) and blockchain(s) this address exist within.

        :param address: The address to fetch information for
        :key includePrice: Indicates whether or not to include price data with the results.
            Options: true, false. (bool)
        :key currency: The currency of the price information (usd or btc.)
            - only used in conjunction with includePrice. (str)
        :return: The API response parsed into a dict
        """
        return self._address_query(
            address=address,
            route="information",
            headers=self.initial_headers,
            params=kwargs,
        )

    def internal_messages(self, address: str, **kwargs) -> Dict:
        """Retrieves internal messages where this address is either the
        originator or a recipient.

        :param address: The address to fetch information for
        :key blockNumber: Filter by internal messages contained within this block number (int)
        :key from: Filter by internal messages for this "from" address (str)
        :key to: Filter by internal messages for this "to" address (str)
        :key transactionHash: Filter by internal messages for this transaction (str)
        :key startDate: Filter by internal messages which happened after this date (int)
        :key endDate: Filter by internal messages which happened before this date (int)
        :key validationMethod: The validation method to be added to the response: none, basic, full.
            Default: none. (str)
        :key page: The page number to return. (int)
        :key size: Number of records per page (int)
        :return: The API response parsed into a dict
        """

        self._check_chain_supported()
        return self._address_query(
            address=address,
            route="functions",
            headers=self.initial_headers,
            params=kwargs,
        )

    def logs(self, address: str, **kwargs) -> Dict:
        """Retrieves the logs for the transactions where this address is either
        the originator or a recipient.

        :param address: The address to fetch information for
        :key blockNumber: Filter by logs contained in this block number (int)
        :key startDate: Filter by logs which happened after this date (int)
        :key endDate: Filter by logs which happened before this date (int)
        :key topic: Filter by logs containing this topic (str)
        :key page: The page number to return. (int)
        :key size: Number of records per page (int)
        :return: The API response parsed into a dict
        """

        self._check_chain_supported()
        return self._address_query(
            address=address,
            route="logs",
            headers=self.initial_headers,
            params=kwargs,
        )

    def metadata(self, address: str, **kwargs) -> Dict:
        """Retrieves statistics about the specified address: balances,
        holdings, etc.

        :param address: The address to fetch information for
        :key timeFormat: The time format to use for the timestamps (milliseconds, ms, iso, iso8611). (str)
        :return: The API response parsed into a dict
        """
        return self._address_query(
            address=address,
            route="metadata",
            headers=self.initial_headers,
            params=kwargs,
        )

    def pending_transactions(self, address: str, **kwargs) -> Dict:
        """Retrieves pending transactions the specified address is involved in.

        :param address: The address to fetch information for
        :key from: Filter by transactions for this "from" address. (str)
        :key to: Filter by transactions for this "to" address (str)
        :key startDate: Filter by transactions which happened after this date. (int)
        :key endDate: Filter by transactions which happened before this date. (int)
        :key includePrice: Indicates whether or not to include price data with the results.
            Options: true, false. (bool)
        :key currency: The currency of the price information (usd or btc.)
            - only used in conjunction with includePrice. (str)
        :key page: The page number to return. (int)
        :key size: The number of records per page. (int)
        :return: The API response parsed into a dict
        """
        return self._address_query(
            address=address,
            route="pending-transactions",
            headers=self.initial_headers,
            params=kwargs,
        )

    def token_balances_historical(self, address: str, **kwargs) -> Dict:
        """Retrieves the historical (time series) token balances for the
        specified address.

        :param address: The address to fetch information for
        :key amount: Filters by token balances which value is equal to this amount (int)
        :key amountGt: Filter by token balances which value is greater than this amount (int)
        :key amountGte: Filter by token balances which value is greater than or equal to this amount (int)
        :key amountLt: Filter by token balances which value is less than this amount (int)
        :key amountLte: Filter by token balances which value is less than or equal to this amount (int)
        :key tokenHolder: Filter by token balances which are held by this address (str)
        :key page: The page number to return. (int)
        :key size: Number of records per page (int)
        :return: The API response parsed into a dict
        """

        self._check_chain_supported()
        return self._address_query(
            address=address,
            route="token-balances",
            headers=self.initial_headers,
            params=kwargs,
        )

    def token_balances_latest(self, address: str, **kwargs) -> Dict:
        """Retrieves the tokens this address is holding.

        :param address: The address to fetch information for
        :key direction: The direction by which to sort the tokens (ascending or descending). (str)
        :key includePrice: Indicates whether or not to include price data with the results. Options: true, false. (str)
        :key currency: The currency of the price information (usd or eth.)
            - only used in conjunction with includePrice. (str)
        :key sortType: The metric by which to rank the tokens (amount, name, symbol). (str)
        :key page: The page number to return. (str)
        :key size: The number of records per page. (str)
        :return: The API response parsed into a dict
        """

        self._check_chain_supported()
        return self._address_query(
            address=address,
            route="tokens",
            headers=self.initial_headers,
            params=kwargs,
        )

    def token_transfers(self, address: str, **kwargs) -> Dict:
        """Retrieves all token transfers involving the specified address.

        :param address: The address to fetch information for
        :key amount: Filter by token transfers which value is equal to this amount. (int)
        :key amountGt: Filter by token transfers which value is greater than this amount. (int)
        :key amountGte: Filter by token transfers which value is greater than or equal to this amount. (int)
        :key amountLt: Filter by token transfers which value is less than this amount. (int)
        :key amountLte: Filter by token transfers which value is less than or equal to this amount (int)
        :key blockNumber: Filter by token transfers with this block number. (int)
        :key recipientAddress: Filter by token transfers which recipient is the specified address. (str)
        :key senderAddress: Filter by token transfers which sender is the specified address. (str)
        :key startDate: Filter by token transfers which happened after this date. (int)
        :key endDate: Filter by token transfers which happened before this date. (int)
        :key tokenAddress: Filter by token transfers for this token. (str)
        :key transactionHash: Filter by token transfers for this transaction hash. (str)
        :key page: The page number to return. (int)
        :key size: Number of records per page. (int)
        :key validationMethod: The validation method to be added to the response: none, basic, full.
            Default: none. (str)
        :key includePrice: Indicates whether or not to include price data with the results.
            Options: true, false. (bool)
        :key currency: The currency of the price information. Options: usd, btc.
            Only used in conjunction with includePrice. (str)
        :return: The API response parsed into a dict
        """

        self._check_chain_supported()
        return self._address_query(
            address=address,
            route="token-transfers",
            headers=self.initial_headers,
            params=kwargs,
        )

    def transactions(self, address: str, **kwargs) -> Dict:
        """Retrieves the transactions where this address was either the
        originator or a recipient.

        :param address: The address to fetch information for
        :key blockNumber: Filter by transactions for this block number. (int)
        :key from: Filter by transactions for this "from" address. (str)
        :key to: Filter by transactions for this "to" address (str)
        :key startDate: Filter by transactions which happened after this date. (date)
        :key endDate: Filter by transactions which happened before this date. (date)
        :key validationMethod: The validation method to be added to the response: none, basic, full.
            Default: none. (str)
        :key includeFunctions: Indicates whether or not to include functions (aka internal messages)
            information for each transaction, if available (false|true). (bool)
        :key includeLogs: Indicates whether or not to include log information for each transaction,
            if available (false|true). (bool)
        :key includeTokenTransfers: Indicates whether or not to include token transfers information for
            each transaction, if available (false|true). (bool)
        :key includePrice: Indicates whether or not to include price data with the results.
            Options: true, false. (bool)
        :key currency: The currency of the price information (usd or btc.)
            - only used in conjunction with includePrice. (str)
        :key page: The page number to return. (int)
        :key size: The number of records per page. (int)
        :return: The API response parsed into a dict
        """
        return self._address_query(
            address=address,
            route="transactions",
            headers=self.initial_headers,
            params=kwargs,
        )

    def usage(self, address: str, **kwargs) -> Dict:
        """Retrieves the historical usage for the specified address.

        :param address: The address to fetch information for
        :key timeFormat: The time format to use with the timestamps: milliseconds/ms or iso/iso8611 (str)
        :key timeFrame: The time frame to return the historical data in:
            by day (1d, 2d, ..., all),
            by hour (1h, 2h, ..., 72h) or
            by minute (1m, 2m, ..., 360m) (str)
        :key timePeriod: The time period (in minutes) to aggregate the historical data. (str)
        :return: The API response parsed into a dict
        """
        return self._address_query(
            address=address,
            route="usage",
            headers=self.initial_headers,
            params=kwargs,
        )

    def metrics(self) -> Dict:
        """Get metrics for all addresses that have exist publicly for a given
        blockchain.

        Default metrics are for Ethereum over a 24h period.

        :return: The API response parsed into a dict
        """
        return self._address_query(
            route="metrics/latest", headers=self.initial_headers, params={}
        )
