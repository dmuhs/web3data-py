======================
web3data-py Python API
======================

.. image:: https://img.shields.io/pypi/v/web3data.svg
    :target: https://pypi.python.org/pypi/web3data

.. image:: https://img.shields.io/travis/dmuhs/web3data-py.svg
    :target: https://travis-ci.org/github/dmuhs/web3data-py

.. image:: https://readthedocs.org/projects/web3data-py/badge/?version=latest
    :target: https://web3data-py.readthedocs.io/?badge=latest
    :alt: Documentation Status

.. image:: https://pyup.io/repos/github/dmuhs/web3data-py/shield.svg
    :target: https://pyup.io/repos/github/dmuhs/web3data-py/
    :alt: Updates

.. image:: https://coveralls.io/repos/github/dmuhs/web3data-py/badge.svg?branch=master
    :target: https://coveralls.io/github/dmuhs/web3data-py?branch=master


Obtaining an API Key
--------------------

Visit `Amberdata.io <https://amberdata.io/pricing>`_ and select the developer plan to get started!
Pass your API key to the client instance, either has a hardcoded string, or through an environment
variable:

.. code-block:: python

    from web3data import Web3Data
    w3d = Web3Data("<your key>")

... and start querying!


Installation
------------

To install web3data-py, run this command in your terminal:

.. code-block:: console

    $ pip install web3data

For alternative ways to install the package, check out the
`installation instructions <https://web3data-py.readthedocs.io/installation.html>`_


Usage
-----

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


Development
-----------

Check out our `contribution guidelines <https://web3data-py.readthedocs.io/contributing.html>`_
to see how to install the development version and run the test suite!

Don't have the time to contribute? Open up an issue and we'll get it fixed!
Simply like the project? Tip me some `BAT <https://brave.com/dmu968>`_ to sponsor development! :)


Resources
---------

* Free software: MIT license
* Documentation: https://web3data-py.readthedocs.io.


Credits
-------

The initial version of this package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
