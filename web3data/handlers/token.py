"""This module contains the address subhandler."""

from typing import Dict

from web3data.chains import Chains
from web3data.handlers.base import BaseHandler


class TokenHandler(BaseHandler):
    """The subhandler for token-related queries."""

    def __init__(self, initial_headers: Dict[str, str], chain: Chains):
        """Return a new :code:`TokenHandler` instance.

        :param initial_headers: Base headers to attach to every request
        :param chain: The blockchain to fetch the information for
        """

        super().__init__(chain)
        self.initial_headers = initial_headers

    def _token_query(self, address: str, route: str, params: Dict[str, str]):
        """Helper method for token-related API queries.

        :param route: The endpoint route to query
        :param params: The request's query parameters
        :param address: The token address string to query for
        :return: The parsed API response
        """
        self._check_chain_supported()
        return self.raw_query(
            base_url=f"https://web3api.io/api/v2/tokens/{address}/",
            route=route,
            headers=self.initial_headers,
            params=params,
        )

    def holders_historical(self, address: str, **kwargs) -> Dict:
        """Retrieves the historical (time series) token holders for the
        specified token address.

        :param address: The token's smart contract address
        :key holderAddresses: A comma separated list of addresses for which the historical
            holdings are to be retrieved. (str)
        :key timeFormat: The time format to use for the timestamps: milliseconds/ms or iso/iso861. (str)
        :key timeFrame: The time frame to return the historical data in:
            by day (1d, 2d, ..., all),
            by hour (1h, 2h, ..., 72h),
            by minute (1m, 2m, ..., 360m) or
            by tick (1t, 10t, ..., 1000t). (str)
        :key includePrice: Indicates whether or not to include price data
            with the results. (bool)
        :key currency: The currency of the price information. Options: usd, btc.
            Only used in conjunction with includePrice. (str)
        :return: The API response parsed into a dict
        """
        self._check_chain_supported()
        return self._token_query(address, "holders/historical", kwargs)

    def holders_latest(self, address: str, **kwargs) -> Dict:
        """Retrieves the token holders for the specified address.

        :param address: The token's smart contract address
        :key numTokens: Filter by token holders who own the specified amount
            of tokens. (int)
        :key numTokensGt: Filter by token holders who own more than the
            specified amount of tokens (int)
        :key numTokensGte: Filter by token holders who own more than or equal
            to the specified amount of tokens (int)
        :key numTokensLt: Fitler by token holders who own less than the
            specified amount of tokens (int)
        :key numTokensLte: Filter by token holders who own less than or equal
            to the specified amount of tokens (int)
        :key tokenAddress: Filter by token holders for this token (mandatory) (str)
        :key timestampGt: Filter by token holders who started holding the token
            after the specified date (int)
        :key timestampGte: Filter by token holders who started holding the token
            after or equal to the specified date (int)
        :key timestampLt: Filter by token holders who started holding the token
            before the specified date (int)
        :key timestampLte: Filter by token holders who started holding the token
            before or equal to the specified date (int)
        :key includePrice: Indicates whether or not to include price data with
            the results. Options: true, false. (bool)
        :key currency: The currency of the price information (usd or btc.)
            - only used in conjunction with includePrice. (str)
        :key page: The page number to return. (int)
        :key size: Number of records per page (int)
        :return: The API response parsed into a dict
        """
        self._check_chain_supported()
        return self._token_query(address, "holders/latest", kwargs)

    def supply_historical(self, address: str, **kwargs) -> Dict:
        """Retrieves the historical token supplies (and derivatives) for the
        specified address.

        :param address: The token's smart contract address
        :param kwargs: Additional query parameter options
        :key timeFormat: The time format to use for the timestamps:
            milliseconds/ms or iso/iso861. (str)
        :key timeInterval: The time interval to return the historical data in:
            by day (days) or by hour (hours). (str)
        :key startDate: Filter by token prices after this date
            - note that the interval can not exceed 6 months (d), or 30 days (h). (int)
        :key endDate: Filter by token prices before this date
            - note that the interval can not exceed 6 months (d), or 30 days (h). (int)
        :return: The API response parsed into a dict
        """
        self._check_chain_supported()
        return self._token_query(address, "supplies/historical", kwargs)

    def supply_latest(self, address: str) -> Dict:
        """Retrieves the latest token supplies (and derivatives) for the
        specified address.

        :param address: The token's smart contract address
        :return: The API response parsed into a dict
        """
        self._check_chain_supported()
        return self._token_query(address, "supplies/latest", {})

    def transfers(self, address: str, **kwargs) -> Dict:
        """Retrieves all token transfers involving the specified address.

        :param address: The token's smart contract address
        :key amount: Filter by token transfers which value is equal to this amount. (int)
        :key amountGt: Filter by token transfers which value is greater than this amount. (int)
        :key amountGte: Filter by token transfers which value is greater than or equal
            to this amount. (int)
        :key amountLt: Filter by token transfers which value is less than this amount. (int)
        :key amountLte: Filter by token transfers which value is less than or equal
            to this amount (int)
        :key blockNumber: Filter by token transfers with this block number. (int)
        :key recipientAddress: Filter by token transfers which recipient is the
            specified address. (str)
        :key senderAddress: Filter by token transfers which sender is the
            specified address. (str)
        :key startDate: Filter by token transfers which happened after this date. (int)
        :key endDate: Filter by token transfers which happened before this date. (int)
        :key tokenAddress: Filter by token transfers for this token. (str)
        :key transactionHash: Filter by token transfers for this transaction hash. (str)
        :key page: The page number to return. (int)
        :key size: Number of records per page. (int)
        :key validationMethod: The validation method to be added to the response:
            none, basic, full. Default: none. (str)
        :key includePrice: Indicates whether or not to include price data with the results.
            Options: true, false. (bool)
        :key currency: The currency of the price information. Options: usd, btc.
            Only used in conjunction with includePrice. (str)
        :return: The API response parsed into a dict
        """
        self._check_chain_supported()
        return self._token_query(address, "transfers", kwargs)

    def velocity(self, address: str, **kwargs) -> Dict:
        """Retrieves the historical velocity for the specified address.

        :param address: The token's smart contract address
        :key timeFormat: The time format to use with the timestamps: milliseconds/ms or iso/iso8611 (str)
        :key timeFrame: The time frame to return the historical data in:
            by day (1d, 2d, ..., all),
            by hour (1h, 2h, ..., 72h) or
            by minute (1m, 2m, ..., 360m) (str)
        :return: The API response parsed into a dict
        """
        self._check_chain_supported()
        return self._token_query(address, "velocity", kwargs)

    def volume(self, address: str, **kwargs) -> Dict:
        """Retrieves the historical number of transfers for the specified
        address.

        :param address: The token's smart contract address
        :key timeFormat: The time format to use with the timestamps: milliseconds/ms or iso/iso8611 (str)
        :key timeFrame: The time frame to return the historical data in:
            by day (1d, 2d, ..., all),
            by hour (1h, 2h, ..., 72h) or
            by minute (1m, 2m, ..., 360m) (str)
        :return: The API response parsed into a dict
        """
        self._check_chain_supported()
        return self._token_query(address, "volume", kwargs)
