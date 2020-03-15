"""This module contains an enum with names of supported chains."""

from enum import Enum


class Chains(Enum):
    """Blockchains supported by the Amberdata API."""

    AION = 1
    BTC = 2
    BCH = 3
    BSV = 4
    ETH = 5
    ETH_RINKEBY = 6
    LTC = 7
    XLM = 8
    ZEC = 9
