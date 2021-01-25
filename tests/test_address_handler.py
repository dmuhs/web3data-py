from itertools import product

import pytest
import requests_mock

from web3data.chains import Chains
from web3data.exceptions import APIError
from web3data.handlers.address import AddressHandler

from . import API_PREFIX, CHAINS, HEADERS, RESPONSE

LIMITED_CHAINS = (
    Chains.BCH,
    Chains.BSV,
    Chains.BTC,
    Chains.LTC,
    Chains.ZEC,
)
ADDRESS_HANDLER_METHODS = (
    ["total", (), ()],
    ["adoption", ("ADDRESS",), ()],
    ["balance_historical", ("ADDRESS",), ()],
    ["balance_latest", ("ADDRESS",), ()],
    ["balances", ("ADDRESS",), ()],
    ["balances_batch", ("ADDRESS",), ()],
    ["information", ("ADDRESS",), ()],
    ["internal_messages", ("ADDRESS",), LIMITED_CHAINS],
    ["logs", ("ADDRESS",), LIMITED_CHAINS],
    ["metadata", ("ADDRESS",), ()],
    ["metrics", (), ()],
    ["pending_transactions", ("ADDRESS",), ()],
    ["token_balances_historical", ("ADDRESS",), LIMITED_CHAINS],
    ["token_balances_latest", ("ADDRESS",), LIMITED_CHAINS],
    ["token_transfers", ("ADDRESS",), LIMITED_CHAINS],
    ["transactions", ("ADDRESS",), ()],
    ["usage", ("ADDRESS",), ()],
)

ADDRESS_PARAMS = []
for chain_value, call in product(CHAINS, ADDRESS_HANDLER_METHODS):
    ADDRESS_PARAMS.append([chain_value] + call[:-1] + [chain_value in call[-1]])


@pytest.mark.parametrize("chain,method,parameters,raises", ADDRESS_PARAMS)
def test_address_handler(chain, method, parameters, raises):
    handler = AddressHandler(initial_headers=HEADERS, chain=chain)
    method = getattr(handler, method)

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
