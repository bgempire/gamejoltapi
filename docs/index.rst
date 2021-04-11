Game Jolt API for Python - Reference
====================================

This module is a single threaded Python interface for the 
`Game Jolt API <https://gamejolt.com/game-api/doc>`_ running through HTTP requests.
It contains all Game Jolt API endpoints and aims to simplify its use where it's possible.
The source code of this module can be found `here <https://github.com/bgempire/gamejoltapi>`_.

Installing
----------

This module is available on the `Python Package Index <https://pypi.org/project/gamejoltapi/>`_. 
To install it on your Python distribution, simply run on the console:

.. code-block:: bash
   
   pip install gamejoltapi
   
Or if you want to download it manually, just download the latest 
`gamejoltapi.py <https://github.com/bgempire/gamejoltapi/blob/main/gamejoltapi.py>`_ 
from the source code repository.
   
Basic Usage
-----------

To instance the main class just provide the required data and you're ready to call any of the API methods.

.. code-block:: python
   
   import gamejoltapi

   GAME_ID = "602381"
   PRIVATE_KEY = "de7ac4c81d064cdc1121b495e2165b53"
   USERNAME = "bgempire"
   TOKEN = "bgempire"
   
   api = gamejoltapi.GameJoltAPI(
      GAME_ID, 
      PRIVATE_KEY, 
      username=USERNAME, 
      userToken=TOKEN,
      responseFormat="json",
      submitRequests=True
   )

Classes
-------

 .. autoclass:: gamejoltapi.GameJoltAPI
    :members:

Exceptions
----------

.. autoclass:: gamejoltapi.GameJoltDataRequired
   :members:

.. autoclass:: gamejoltapi.GameJoltDataCollision
   :members:
