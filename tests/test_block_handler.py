from itertools import product

import pytest
import requests_mock

from web3data.chains import Chains
from web3data.exceptions import APIError
from web3data.handlers.block import BlockHandler

from . import API_PREFIX, CHAINS, HEADERS, RESPONSE

LIMITED_CHAINS = (
    Chains.BCH,
    Chains.BSV,
    Chains.BTC,
    Chains.LTC,
    Chains.ZEC,
)
BLOCK_HANDLER_METHODS = (
    ["transactions", ("BLOCK_ID",), ()],
    ["token_transfers", ("BLOCK_ID",), LIMITED_CHAINS],
    ["logs", ("BLOCK_ID",), LIMITED_CHAINS],
    ["total", (), ()],
    ["functions", ("BLOCK_ID",), LIMITED_CHAINS],
    ["metrics_historical", (), ()],
    ["metrics_latest", (), ()],
    ["single", ("BLOCK_ID",), ()],
)

BLOCK_PARAMS = []
for chain_value, call in product(CHAINS, BLOCK_HANDLER_METHODS):
    BLOCK_PARAMS.append([chain_value] + call[:2] + [chain_value in call[2]])


@pytest.mark.parametrize("chain,method,parameters,raises", BLOCK_PARAMS)
def test_block_handler(chain, method, parameters, raises):
    handler = BlockHandler(initial_headers=HEADERS, chain=chain)
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
