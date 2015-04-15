from hammock import Hammock


class ICMClient(Hammock):
    """Extends Hammock to easily create a client configured to make requests against InformaCast Mobile"""

    @classmethod
    def create(cls, access_token=None, url='https://api.icmobile.singlewire.com/api/v1-DEV', **kwargs):
        """Helper function to create a custom Hammock wrapper for InformaCast Mobile"""
        if not access_token:
            raise ValueError('Access token must be supplied')
        if not url:
            raise ValueError('URL must be supplied')
        headers = {
            'Authorization': 'Bearer ' + access_token,
            'X-Client-Version': 'ICMPython 0.0.1'
        }
        if 'headers' in kwargs:
            headers.update(kwargs['headers'])
            kwargs['headers'] = headers
        else:
            kwargs['headers'] = headers
        return cls(url, **kwargs)

    def __getattr__(self, name):
        """Overridden from Hammock to replace snake_case with kebab-case for unknown attributes"""
        if name.startswith('__'):
            raise AttributeError(name)
        return self._spawn(name.replace('_', '-'))

    def LIST(self, *args, **kwargs):
        """Provides a generator function to perform pagination"""

        # If a limit is not set on the params, we'll use a default of 100
        default_limit = 100

        # We initially don't have a next token
        next_token = None

        # Make sure the params is both present and has a limit set
        if 'params' not in kwargs:
            kwargs['params'] = {'limit': default_limit}
        if 'limit' not in kwargs['params']:
            kwargs['params']['limit'] = default_limit

        # Continue making requests and yielding the results as they arrive
        while True:
            # If we have a next token, register it as the start param for our next request
            if next_token:
                kwargs['params']['start'] = next_token

            # Perform the request and get the response
            response = self._request('get', *args, **kwargs)

            # Validate that the response was a success before continuing
            if response.status_code is not 200:
                raise Exception('Received an invalid status code', response)

            # Process the response body as json
            response_json = response.json()

            # Yield all of the resources in the data array
            for resource in response_json['data']:
                yield resource

            # Extract the next token from the response
            next_token = response_json['next']

            # If there is no next token, stop paginating
            if not next_token:
                break