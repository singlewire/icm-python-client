InformaCast Mobile REST Python Client
=====================================

A simple, easy to use REST client based on `requests`_ and `Hammock`_

Installation
------------

Installation should be straight forward with pip:

.. code:: shell

    pip install icm-python-client

Usage
-----

Import the client:

.. code:: python

    from icm_python_client.icm_client import ICMClient

Create an instance of the client (`session`_ kwargs may also be
provided):

.. code:: python

    icm_client = ICMClient.create('<My Access Token>')

Have fun!

.. code:: python

    # Get first page of users
    icm_client.users().GET().json()

    # Paginate through all users
    for user in icm_client.users().LIST():
        print user
        
    # Search for a user named Jim
    icm_client.users().GET(params={'limit': 10, 'q': 'Jim'}).json()

    # Get a specific user
    icm_client.users('de7b51a0-5a1e-11e4-ab31-8a1d033dd637').GET().json()

    # Get a specific user's devices
    icm_client.users('de7b51a0-5a1e-11e4-ab31-8a1d033dd637').devices().GET().json()

    # Create a user
    user = icm_client.users().POST(params={'name': 'Jim Bob', 'email': 'jim.bob@aol.com'}).json()

    # Update the created user
    icm_client.users(user['id']).PUT(params={'name': 'Jim Bob The Second'}).json()

    # Delete the updated user
    icm_client.users(user['id']).DELETE().json()

License
-------

Copyright 2015 Singlewire LLC

Licensed under the Apache License, Version 2.0 (the “License”); you may
not use this file except in compliance with the License. You may obtain
a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an “AS IS” BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

.. _requests: https://github.com/kennethreitz/requests
.. _Hammock: https://github.com/kadirpekel/hammock
.. _session: http://docs.python-requests.org/en/latest/user/advanced/#session-objects