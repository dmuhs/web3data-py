=====
Usage
=====

To use web3data-py in a project:

.. code-block:: python

    from web3data import Web3Data

    w3d = Web3Data("<your key>")
    print(w3d.eth.address.information("0x06012c8cf97bead5deae237070f9587f8e7a266d"))

This will print the raw response, such as:

.. code-block:: python

        {'status': 200,
         'title': 'OK',
         'description': 'Successful request',
         'payload': {'balance': '5296672643815245964',
          'balanceIn': '3.0894905437937322715551e+22',
          'balanceOut': '3.0889608765293507469587e+22',
          'addressType': 'contract',
          'changeInPrice': None,
          'contractTypes': ['ERC721'],
          'decimals': '0',
          'name': 'CryptoKitties',
          'numHolders': '84753',
          'numTokens': '1860119',
          'numTransfers': '2723659',
          'symbol': 'CK',
          'totalSupply': '1860119.0000000000000000',
          'totalValueUSD': None,
          'unitValueUSD': None}}


Supported Chains and Handlers
-----------------------------

Each endpoint of the Amberdata web3 API can be hit for a specified chain. :code:`web3data-py`
follows the paradigm set by `web3data-js <https://github.com/web3data/web3data-js>`_ and allows
easy switching between chains by providing them as client attributes. Each attribute implements
a sub-handler for several kinds of data, such as address-, market-, or transaction-related
information.

The methods for each chain are fixed, however some chains might raise an :code:`APIError` if the
data is unavailable. For example, token-related queries on Bitcoin will raise an exception, because
Bitcoin does not allow for smart-contracts and token implementations on-chain.

.. code-block:: python

    In [1]: w3d.eth.token.supply_latest("0x9f8f72aa9304c8b593d555f12ef6589cc3a579a2")
    Out[1]:
    {'status': 200,
     'title': 'OK',
     'description': 'Successful request',
     'payload': {'decimals': '18',
      'circulatingSupply': '985776.2571660122663385',
      'totalBurned': '1014178.1439074671310546',
      'totalMinted': '1999953.40106534372698',
      'totalSupply': '985775.2571578765959254',
      'totalTransfers': '678572'}}

And on the other hand:

.. code-block:: python

    In [1]: w3d.btc.token.supply_latest("0x9f8f72aa9304c8b593d555f12ef6589cc3a579a2")
    ---------------------------------------------------------------------------
    APIError                                  Traceback (most recent call last)
    <ipython-input-12-93158fe945ad> in <module>
    ----> 1 w3d.btc.token.supply_latest("0x9f8f72aa9304c8b593d555f12ef6589cc3a579a2")

    ~/repos/web3data-py/web3data/handlers/token.py in supply_latest(self, address)
        115         :return: The API response parsed into a dict
        116         """
    --> 117         self._check_chain_supported()
        118         return self._token_query(address, "supplies/latest", {})
        119

    ~/repos/web3data-py/web3data/handlers/base.py in _check_chain_supported(self)
         34     def _check_chain_supported(self):
         35         if self.chain in self.LIMITED:
    ---> 36             raise APIError(f"This method is not supported for {self.chain}")
         37
         38     @staticmethod

    APIError: This method is not supported for Chains.BTC

This behaviour aims to notify the developer as early as possible about invalid code and
business logic errors that need fixing right away.

Currently, Amberdata supports the following chains, which are implemented as client instance
attributes:

 - :code:`w3d.aion`
 - :code:`w3d.bch`
 - :code:`w3d.bsv`
 - :code:`w3d.btc`
 - :code:`w3d.eth`
 - :code:`w3d.eth_rinkeby`
 - :code:`w3d.ltc`
 - :code:`w3d.xlm`
 - :code:`w3d.zec`

Each chain attribute implements the following sub-handlers for specific API queries:

 - :code:`address`
 - :code:`block`
 - :code:`contract`
 - :code:`market`
 - :code:`signature`
 - :code:`token`
 - :code:`transaction`

Further information on the implementation details can be found in the
`package documentation <https://web3data-py.readthedocs.io/web3data.html>`_.
