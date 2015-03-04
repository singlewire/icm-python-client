# InformaCast Mobile REST Python Client

A simple, easy to use REST client based on [requests](https://github.com/kennethreitz/requests) and
[Hammock](https://github.com/kadirpekel/hammock)

## Installation

Installation should be straight forward with pip:

```shell
pip install icm-python-client
```

## Usage

Import the client:

```python
from icm_client import ICMClient
```

Create an instance of the client:

```python
icm_client = ICMClient.create('<My Access Token>')
```

Have fun!

```python
# Get all users
print icm_client.users().GET().json()

# Get a specific user
print icm_client.users('de7b51a0-5a1e-11e4-ab31-8a1d033dd637').GET().json()

# Get a specific user's devices
print icm_client.users('de7b51a0-5a1e-11e4-ab31-8a1d033dd637').devices().GET().json()

# Create a user
user = icm_client.users().POST(params={'name': 'Jim Bob', 'email': 'jim.bob@aol.com'}).json()
print user

# Update the created user
print icm_client.users(user['id']).PUT(params={'name': 'Jim Bob The Second'}).json()

# Delete the updated user
print icm_client.users(user['id']).DELETE().json()
```

## License

TODO