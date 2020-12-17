"""This module contains an enum with names of supported chains."""

from enum import Enum


class Chains(Enum):
    """Blockchains supported by the Amberdata API."""

    BTC = 1
    BCH = 2
    BSV = 3
    ETH = 4
    ETH_RINKEBY = 5
    LTC = 6
    ZEC = 7
