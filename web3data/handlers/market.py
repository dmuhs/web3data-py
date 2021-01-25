"""This module contains the address subhandler."""

from typing import Dict

from web3data.chains import Chains
from web3data.handlers.base import BaseHandler


class MarketHandler(BaseHandler):
    """The subhandler for market-related queries."""

    def __init__(self, initial_headers: Dict[str, str], chain: Chains):
        """Return a new :code:`MarketHandler` instance.

        :param initial_headers: Base headers to attach to every request
        :param chain: The blockchain to fetch the information for
        """

        super().__init__(chain)
        self.initial_headers = initial_headers
        self.base_url = "https://web3api.io/api/v2/"

    def exchanges(self, **kwargs) -> Dict:
        """Retrieves information about supported exchange-pairs.

        These types of data are supported:
        - ticker
        - ohlc (open-high-low-close)
        - trade
        - order_book
        - order_book_update

        :key exchange: only return data for the given exchanges (comma separated) (str)
        :key pair: only return data for the given pairs (comma separated) (str)
        :return: The API response parsed into a dict
        """
        return self.raw_query(
            base_url=self.base_url,
            route="market/exchanges",
            headers=self.initial_headers,
            params=kwargs,
        )

    def ohlcv(self, **kwargs) -> Dict:
        """Retrieves information about supported exchange-pairs for ohlcv.

        :key exchange: Filter by data for the given exchanges (comma separated). (str)
        :return: The API response parsed into a dict
        """
        return self.raw_query(
            base_url=self.base_url,
            route="market/ohlcv/information",
            headers=self.initial_headers,
            params=kwargs,
        )

    def pairs(self, **kwargs) -> Dict:
        """Retrieves information about supported exchange-pairs. These types of
        data are supported:

        - ticker
        - ohlc (open-high-low-close)
        - trade
        - order_book
        - order_book_update

        :key exchange: only return data for the given exchanges (comma separated) (str)
        :key pair: only return data for the given pairs (comma separated) (str)
        :return: The API response parsed into a dict
        """
        return self.raw_query(
            base_url=self.base_url,
            route="market/pairs",
            headers=self.initial_headers,
            params=kwargs,
        )

    def rankings(self, **kwargs) -> Dict:
        """Retrieves the top ranked assets by a specific metric.

        :key direction: The sort order in which assets are ranked ascending
            or descending. (str)
        :key sortType: The metric used to rank the assets.
            Options: changeInPrice, currentPrice, liquidMarketCap, marketCap,
            tokenVelocity, tradeVolume, transactionVolume, uniqueAddresses (str)
        :key timeInterval: The time interval in which to return
            the historical data days or hours. (str)
        :key type: The type(s) of assets to include in the rankings:
            erc20|, erc721, erc777, erc884, erc998. Note: leaving this
            parameter empty means all tokens will be included. (str)
        :key page: The page number to return. (int)
        :key size: The number of records per page. (int)
        :return: The API response parsed into a dict
        """
        return self.raw_query(
            base_url=self.base_url,
            route="market/rankings",
            headers=self.initial_headers,
            params=kwargs,
        )

    def price_pairs(self) -> Dict:
        """Retrieves the assets for which latest prices are available.

        :return: The API response parsed into a dict
        """
        return self.raw_query(
            base_url=self.base_url,
            route="market/prices/pairs",
            headers=self.initial_headers,
            params={},
        )

    def ticker_pairs(self, **kwargs) -> Dict:
        """Retrieves the list of all available market tickers.

        :key exchange: Only return data for the given exchanges (comma separated). (str)
        :return: The API response parsed into a dict
        """
        return self.raw_query(
            base_url=self.base_url,
            route="market/tickers/information",
            headers=self.initial_headers,
            params=kwargs,
        )

    def trades(self, **kwargs) -> Dict:
        """Retrieves the list of all available market trade data sets.

        :key exchange: Only return data for the given exchanges (comma separated). (str)
        :return: The API response parsed into a dict
        """
        return self.raw_query(
            base_url=self.base_url,
            route="market/trades/information",
            headers=self.initial_headers,
            params=kwargs,
        )

    def order_best_bid_historical(self, pair: str, **kwargs) -> Dict:
        """Retrieves historical best bid and offer information for the
        specified pair.

        :param pair: The asset pair to look up
        :key exchange: The exchange(s) for which to retrieve order book data.
            Example: exchange=bitfinex,bitstamp (str)
        :key timeFormat: The timestamp format to use for the timestamps:
            milliseconds/ms or iso/iso8611. (str)
        :key startDate: Filter by pairs after this date. (int)
        :key endDate: Filter by pairs before this date. (int)
        :return: The API response parsed into a dict
        """
        return self.raw_query(
            base_url=self.base_url,
            route=f"market/orders/{pair}/bbo/historical",
            headers=self.initial_headers,
            params=kwargs,
        )

    def order_best_bid_latest(self, pair: str, **kwargs) -> Dict:
        """Retrieves the latest best bid and offer information for the
        specified pair and exchange.

        :param pair: The asset pair to look up
        :key exchange: The exchange(s) for which to retrieve order book data.
            Example: exchange=bitfinex,bitstamp (str)
        :key timeFormat: The timestamp format to use for the timestamps:
            milliseconds/ms or iso/iso8611. (str)
        :return: The API response parsed into a dict
        """
        return self.raw_query(
            base_url=self.base_url,
            route=f"market/orders/{pair}/bbo",
            headers=self.initial_headers,
            params=kwargs,
        )

    def order_book_updates(self, pair: str, **kwargs) -> Dict:
        """

        :param pair: The asset pair to look up
        :key exchange: The exchange(s) for which to retrieve order book data.
            Example: exchange=bitfinex,bitstamp (str)
        :key timeFormat: The timestamp format to use for the timestamps:
            milliseconds/ms or iso/iso8611. (str)
        :key startDate: Filter by pairs after this date. (int)
        :key endDate: Filter by pairs before this date. (int)
        :return: The API response parsed into a dict
        """
        return self.raw_query(
            base_url=self.base_url,
            route=f"market/orders/{pair}/update",
            headers=self.initial_headers,
            params=kwargs,
        )

    def order_book(self, pair: str, **kwargs) -> Dict:
        """Retrieves the order book data for the specified pair.

        :param pair: The asset pair to look up
        :key exchange: The exchange(s) for which to retrieve order book data.
            Example: exchange=bitfinex,bitstamp (str)
        :key timestamp: The timestamp at which to return the order book information
            (closest match, lower or equal to the timestamp specified). (str)
        :key timeFormat: The timestamp format to use for the timestamps:
            milliseconds/ms or iso/iso8611. (str)
        :key startDate: Filter by pairs after this date. Formats:
            milliseconds, iso, or iso8611 (str)
        :key endDate: Filter by pairs before this date. Formats:
            milliseconds, iso, or iso8611.
            Note: Must be greater than startDate and cannot exceed 10 minutes. (str)
        :return: The API response parsed into a dict
        """
        return self.raw_query(
            base_url=self.base_url,
            route=f"market/orders/{pair}",
            headers=self.initial_headers,
            params=kwargs,
        )

    def uniswap_liquidity(self, pair: str, **kwargs) -> Dict:
        """Retrieves the Uniswap-specific ether and token balance pairs over
        time.

        Note: This endpoint returns a max of 6 months of historical data. In order
        to get more than 6 months you must use the startDate & endDate parameters
        to move the time frame window to get the next n days/months of data.

        :param pair: The asset pair to look up
        :key timeFormat: The timestamp format to use for the timestamps:
            milliseconds/ms or iso/iso8611. (str)
        :key startDate: Filter to liquidity changes after this date (int)
        :key endDate: Filter to liquidity changes before this date (int)
        :return: The API response parsed into a dict
        """
        return self.raw_query(
            base_url=self.base_url,
            route=f"market/orders/uniswap/{pair}/liquidity",
            headers=self.initial_headers,
            params=kwargs,
        )

    def trade_pairs_historical(self, pair: str, **kwargs) -> Dict:
        """Retrieves the historical (time series) trade data for the specified
        pair.

        Note: This endpoint returns a max of 6 months of historical data. In order to
        get more than 6 months you must use the startDate & endDate parameters to move
        the time frame window to get the next n days/months of data.

        :param pair: The asset pair to look up
        :key exchange: The exchange(s) for which to retrieve market trades. (str)
        :key startDate: Filter by trades after this date. (int)
        :key endDate: Filter by trades before this date. (int)
        :return: The API response parsed into a dict
        """
        return self.raw_query(
            base_url=self.base_url,
            route=f"market/trades/{pair}/historical",
            headers=self.initial_headers,
            params=kwargs,
        )

    def ohlcv_pair_latest(self, pair: str, **kwargs) -> Dict:
        """Retrieves the latest open-high-low-close for the specified pair.

        :param pair: The asset pair to look up
        :key exchange: The exchange(s) for which to retrieve OHLCV.
            Example: exchange=bitfinex,bitstamp (str)
        :return: The API response parsed into a dict
        """
        return self.raw_query(
            base_url=self.base_url,
            route=f"market/ohlcv/{pair}/latest",
            headers=self.initial_headers,
            params=kwargs,
        )

    def ohlcv_pair_historical(self, pair: str, **kwargs) -> Dict:
        """Retrieves the historical (time series) open-high-low-close for the
        specified pair.

        Note: This endpoint returns a max of 6 months of historical data. In order to get more
        than 6 months you must use the startDate & endDate parameters to move the time frame
        window to get the next n days/months of data.

        :param pair: The asset pair to look up
        :key exchange: The exchange(s) for which to retrieve OHLCV.
            Example: exchange=bitfinex,bitstamp (str)
        :key startDate: Filter by pairs after this date. (int)
        :key endDate: Filter by pairs before this date. (int)
        :key timeInterval: Time interval to return the historical data
            in ("days" | "hours" | "minutes") (str)
        :key timeFormat: Time format to use for the timestamps
            ( "milliseconds" | "ms" | "iso" | "iso8611" ) (str)
        :return: The API response parsed into a dict
        """
        return self.raw_query(
            base_url=self.base_url,
            route=f"market/ohlcv/{pair}/historical",
            headers=self.initial_headers,
            params=kwargs,
        )

    def price_pair_historical(self, pair: str, **kwargs) -> Dict:
        """Retrieves the historical prices for the specified asset.

        :param pair: The asset pair to look up
        :key timeFormat: Time format to use for the timestamps
            (Options: milliseconds, ms, iso, iso8611) (str)
        :key startDate: Filter by prices after this date. (str)
        :key endDate: Filter by prices before this date. (str)
        :key timeInterval: Time interval to return the historical data
            in ("days" | "hours" | "minutes") (str)
        :return: The API response parsed into a dict
        """
        return self.raw_query(
            base_url=self.base_url,
            route=f"market/spot/prices/pairs/{pair}/historical",
            headers=self.initial_headers,
            params=kwargs,
        )

    def price_pair_latest(self, pair: str, **kwargs) -> Dict:
        """Retrieves the latest price for the specified asset.

        :param pair: The asset pair to look up
        :key timeFormat: Time format to use for the timestamps
            (Options: milliseconds, ms, iso, iso8611) (str)
        :return: The API response parsed into a dict
        """
        return self.raw_query(
            base_url=self.base_url,
            route=f"market/spot/prices/pairs/{pair}/latest",
            headers=self.initial_headers,
            params=kwargs,
        )

    def base_wap_latest(self, base: str, **kwargs) -> Dict:
        """Retrieves the latest VWAP & TWAP price for the specified base.

        :param base: The pair's base
        :key quote: The currency of the pair. Example: if pair is "eth_usd", then quote is "usd" (str)
        :key timeFormat: Time format to use for the timestamps
            (Options: milliseconds, ms, iso, iso8611) (str)
        :return: The API response parsed into a dict
        """
        return self.raw_query(
            base_url=self.base_url,
            route=f"market/prices/{base}/wap/latest",
            headers=self.initial_headers,
            params=kwargs,
        )

    def ticker_bid_ask_latest(self, pair: str, **kwargs) -> Dict:
        """Retrieves the latest market ticker Bid/Ask/Mid/Last for the
        specified pair.

        :param pair: The asset pair to look up
        :key exchange: The exchange(s) for which to retrieve market tickers. Example: exchange=bitfinex,bitstamp (str)
        :return: The API response parsed into a dict
        """
        return self.raw_query(
            base_url=self.base_url,
            route=f"market/tickers/{pair}/latest",
            headers=self.initial_headers,
            params=kwargs,
        )

    def ticker_bid_ask_historical(self, pair: str, **kwargs) -> Dict:
        """Retrieves the historical ticker, bid/ask/mid/last, for the specified
        pair.

        Note: This endpoint returns a max of 6 months of historical data. In order to get more
        than 6 months you must use the startDate & endDate parameters to move the time frame
        window to get the next n days/months of data.

        :param pair: The asset pair to look up
        :key exchange: The exchange(s) for which to retrieve market tickers.
            Example: exchange=bitfinex,bitstamp (str)
        :key startDate: Filter by ticker pairs after this date. (int)
        :key endDate: Filter by ticker pairs before this date. (int)
        :return: The API response parsed into a dict
        """
        return self.raw_query(
            base_url=self.base_url,
            route=f"market/tickers/{pair}/historical",
            headers=self.initial_headers,
            params=kwargs,
        )

    def token_price_historical(self, address: str, **kwargs) -> Dict:
        """

        :param address: The token's smart contract address
        :key currency: The additional currency (other than ETH and USD) for which
            to return price info. (str)
        :key timeFormat: The time format to use for the timestamps: milliseconds/ms
            or iso/iso861. (str)
        :key timeInterval: The time interval to return the historical data in:
            by day (d),
            by hour (h), or
            by minute (m). (str)
        :key startDate: Filter by prices after this date. Note that the interval can not exceed
            6 months (d), 30 days (h) or 24 hours (m). (int)
        :key endDate: Filter by prices before this date. Note that the interval can not exceed
            6 months (d), 30 days (h) or 24 hours (m). (int)
        :return: The API response parsed into a dict
        """
        return self.raw_query(
            base_url=self.base_url,
            route=f"market/tokens/prices/{address}/historical",
            headers=self.initial_headers,
            params=kwargs,
        )

    def token_price_latest(self, address: str, **kwargs) -> Dict:
        """Retrieves the latest price (and other market information) for the
        specified token.

        :param address: The token's smart contract address
        :key currency: The additional currency (other than ETH and USD)
            for which to return price info. (str)
        :return: The API response parsed into a dict
        """
        return self.raw_query(
            base_url=self.base_url,
            route=f"market/tokens/prices/{address}/latest",
            headers=self.initial_headers,
            params=kwargs,
        )

    def token_rankings_historical(self, **kwargs) -> Dict:
        """Retrieves the top ranked tokens by a specific metric, with a
        lookback window.

        Useful for viewing token trends.

        :key direction: The sort order in which tokens are ranked
            (ascending or descending). (str)
        :key sortType: The metric used to rank the tokens (changeInPrice,
            currentPrice, marketCap, tokenVelocity, transactionVolume &
            uniqueAddresses). (str)
        :key topN: Number denominating top ranking tokens to return.
            Example: If given "5", results with return top 5 token
            rankings for past timeframe, where there are 5 results
            per day. (str)
        :return: The API response parsed into a dict
        """

        self._check_chain_supported()
        return self.raw_query(
            base_url=self.base_url,
            route="tokens/rankings/historical",
            headers=self.initial_headers,
            params=kwargs,
        )

    def token_rankings_latest(self, **kwargs) -> Dict:
        """Retrieves the top ranked tokens by a specific metric.

        :key direction: The sort order in which tokens are ranked
            (ascending or descending). (str)
        :key sortType: The metric used to rank the tokens (changeInPrice,
            currentPrice, marketCap, tokenVelocity, transactionVolume &
            uniqueAddresses). (str)
        :key timeInterval: The time interval to return the historical
            data in: by day (days) or by hour (hours). (str)
        :key type: The type(s) of tokens to include in the rankings
            (erc20, erc721, erc777, erc884, erc998) (str)
        :key page: The page number to return. (int)
        :key size: Number of records per page (int)
        :return: The API response parsed into a dict
        """

        self._check_chain_supported()
        return self.raw_query(
            base_url=self.base_url,
            route="tokens/rankings",
            headers=self.initial_headers,
            params=kwargs,
        )
