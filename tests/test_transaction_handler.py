from itertools import product

import pytest
import requests_mock

from web3data.chains import Chains
from web3data.exceptions import APIError
from web3data.handlers.transaction import TransactionHandler

from . import API_PREFIX, CHAINS, HEADERS, RESPONSE

LIMITED_CHAINS = (
    Chains.BCH,
    Chains.BSV,
    Chains.BTC,
    Chains.LTC,
    Chains.ZEC,
)
TRANSACTION_HANDLER_METHODS = (
    ["volume", (), ()],
    ["token_transfers", ("TRANSACTION_HASH",), LIMITED_CHAINS],
    ["metrics", (), ()],
    ["information", ("TRANSACTION_HASH",), ()],
    ["find", (), ()],
    ["gas_percentiles", (), LIMITED_CHAINS],
    ["gas_predictions", (), LIMITED_CHAINS],
)

TRANSACTION_PARAMS = []
for chain_value, call in product(CHAINS, TRANSACTION_HANDLER_METHODS):
    TRANSACTION_PARAMS.append([chain_value] + call[:2] + [chain_value in call[2]])


@pytest.mark.parametrize("chain,method,parameters,raises", TRANSACTION_PARAMS)
def test_transaction_handler(chain, method, parameters, raises):
    handler = TransactionHandler(initial_headers=HEADERS, chain=chain)
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
