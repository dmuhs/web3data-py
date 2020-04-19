import pytest
import requests_mock

from web3data.chains import Chains
from web3data.exceptions import APIError, EmptyResponseError
from web3data.handlers.base import BaseHandler

CHAINS = (
    Chains.AION,
    Chains.BCH,
    Chains.BSV,
    Chains.BTC,
    Chains.ETH,
    Chains.ETH_RINKEBY,
    Chains.LTC,
    Chains.XLM,
    Chains.ZEC,
)
PARAMS = {"test": "value"}
HEADERS = {"foo": "bar"}
RESPONSE = {"baz": "qux"}


def assert_request_mock(m):
    assert m.call_count == 1
    assert (
        m.request_history[0].url == "http://example.com/test-route?test=value"
    )
    # assert header kv pairs are in request headers
    assert set(HEADERS.items()).issubset(
        set(m.request_history[0].headers.items())
    )


@pytest.mark.parametrize("chain", CHAINS)
def test_base_handler_empty_response(chain):
    handler = BaseHandler(chain)
    with requests_mock.Mocker() as m:
        m.register_uri(requests_mock.ANY, requests_mock.ANY, text="")

        with pytest.raises(EmptyResponseError):
            handler.raw_query(
                "http://example.com/", "test-route", HEADERS, PARAMS
            )

        assert m.call_count == 1
        assert_request_mock(m)


@pytest.mark.parametrize("chain", CHAINS)
def test_base_handler_empty_json_response(chain):
    handler = BaseHandler(chain)
    with requests_mock.Mocker() as m:
        m.register_uri(requests_mock.ANY, requests_mock.ANY, json={})

        with pytest.raises(EmptyResponseError):
            handler.raw_query(
                "http://example.com/", "test-route", HEADERS, PARAMS
            )

        assert m.call_count == 1
        assert_request_mock(m)


@pytest.mark.parametrize("chain", CHAINS)
def test_base_handler_invalid_response(chain):
    handler = BaseHandler(chain)
    with requests_mock.Mocker() as m:
        m.register_uri(requests_mock.ANY, requests_mock.ANY, text="invalid")

        with pytest.raises(APIError):
            handler.raw_query(
                "http://example.com/", "test-route", HEADERS, PARAMS
            )

        assert m.call_count == 1
        assert_request_mock(m)


@pytest.mark.parametrize("chain", CHAINS)
def test_base_handler_valid_response(chain):
    handler = BaseHandler(chain)
    with requests_mock.Mocker() as m:
        m.register_uri(requests_mock.ANY, requests_mock.ANY, json=RESPONSE)

        resp = handler.raw_query(
            "http://example.com/", "test-route", HEADERS, PARAMS
        )

        assert resp == RESPONSE
        assert_request_mock(m)
