from itertools import product

import pytest
import requests_mock

from web3data.chains import Chains
from web3data.exceptions import APIError
from web3data.handlers.market import MarketHandler

from . import API_PREFIX, CHAINS, HEADERS, RESPONSE

LIMITED_CHAINS = (
    Chains.BCH,
    Chains.BSV,
    Chains.BTC,
    Chains.LTC,
    Chains.ZEC,
)
MARKET_HANDLER_METHODS = (
    ["base_wap_latest", ("BASE",), ()],
    ["exchanges", (), ()],
    ["ohlcv", (), ()],
    ["ohlcv_pair_historical", ("PAIR",), ()],
    ["ohlcv_pair_latest", ("PAIR",), ()],
    ["order_best_bid_historical", ("PAIR",), ()],
    ["order_best_bid_latest", ("PAIR",), ()],
    ["order_book", ("PAIR",), ()],
    ["order_book_updates", ("PAIR",), ()],
    ["pairs", (), ()],
    ["price_pair_historical", ("PAIR",), ()],
    ["price_pair_latest", ("PAIR",), ()],
    ["price_pairs", (), ()],
    ["rankings", (), ()],
    ["ticker_bid_ask_historical", ("PAIR",), ()],
    ["ticker_bid_ask_latest", ("PAIR",), ()],
    ["ticker_pairs", (), ()],
    ["token_price_historical", ("TOKEN_ADDRESS",), ()],
    ["token_price_latest", ("TOKEN_ADDRESS",), ()],
    ["token_rankings_historical", (), LIMITED_CHAINS],
    ["token_rankings_latest", (), LIMITED_CHAINS],
    ["trade_pairs_historical", ("PAIR",), ()],
    ["trades", (), ()],
    ["uniswap_liquidity", ("PAIR",), ()],
)

MARKET_PARAMS = []
for chain_value, call in product(CHAINS, MARKET_HANDLER_METHODS):
    MARKET_PARAMS.append([chain_value] + call[:2] + [chain_value in call[2]])


@pytest.mark.parametrize("chain,method,parameters,raises", MARKET_PARAMS)
def test_market_handler(chain, method, parameters, raises):
    handler = MarketHandler(initial_headers=HEADERS, chain=chain)
    method = getattr(handler, method, None)

    if raises:
        with pytest.raises(APIError):
            method(*parameters)
    else:
        with requests_mock.Mocker() as m:
            m.register_uri(requests_mock.ANY, requests_mock.ANY, json=RESPONSE)
            response = method(*parameters)

            assert m.call_count == 1
            assert response == RESPONSE
            assert m.request_history[0].url.startswith(API_PREFIX)
            # assert header kv pairs are in request headers
            assert set(HEADERS.items()).issubset(
                set(m.request_history[0].headers.items())
            )
