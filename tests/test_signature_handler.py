from itertools import product

import pytest
import requests_mock

from web3data.chains import Chains
from web3data.exceptions import APIError
from web3data.handlers.token import TokenHandler

from . import API_PREFIX, CHAINS, HEADERS, RESPONSE

LIMITED_CHAINS = (
    Chains.BCH,
    Chains.BSV,
    Chains.BTC,
    Chains.LTC,
    Chains.ZEC,
)
TOKEN_HANDLER_METHODS = (
    ["holders_historical", ("TOKEN_ADDRESS",), LIMITED_CHAINS],
    ["holders_latest", ("TOKEN_ADDRESS",), LIMITED_CHAINS],
    ["supply_historical", ("TOKEN_ADDRESS",), LIMITED_CHAINS],
    ["supply_latest", ("TOKEN_ADDRESS",), LIMITED_CHAINS],
    ["transfers", ("TOKEN_ADDRESS",), LIMITED_CHAINS],
    ["velocity", ("TOKEN_ADDRESS",), LIMITED_CHAINS],
    ["volume", ("TOKEN_ADDRESS",), LIMITED_CHAINS],
)

TOKEN_PARAMS = []
for chain_value, call in product(CHAINS, TOKEN_HANDLER_METHODS):
    TOKEN_PARAMS.append([chain_value] + call[:2] + [chain_value in call[2]])


@pytest.mark.parametrize("chain,method,parameters,raises", TOKEN_PARAMS)
def test_token_handler(chain, method, parameters, raises):
    handler = TokenHandler(initial_headers=HEADERS, chain=chain)
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
