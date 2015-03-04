from hammock import Hammock


class ICMClient(Hammock):
    @classmethod
    def create(cls, access_token=None, url='https://api.icmobile.singlewire.com/api/v1-DEV'):
        """Helper function to create a custom Hammock wrapper for InformaCast Mobile"""
        return cls(url, headers={'Authorization': 'Bearer ' + access_token})

    def __getattr__(self, name):
        """Overridden from Hammock to replace snake_case with kebab-case for unknown attributes"""
        if name.startswith('__'):
            raise AttributeError(name)
        return self._spawn(name.replace('_', '-'))
