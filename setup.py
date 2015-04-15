from distutils.core import setup
import os

local_file = lambda *f: \
    open(os.path.join(os.path.dirname(__file__), *f)).read()

setup(
    name='icm-python-client',
    packages=['icm_python_client'],
    version='0.0.2',
    description='A simple python client for InformaCast Mobile based on requests and Hammock',
    long_description=local_file('README.rst'),
    author='Vincent Pizzo',
    author_email='vincent.pizzo@singlewire.com',
    url='https://github.com/singlewire/icm-python-client',
    download_url='https://github.com/singlewire/icm-python-client/tarball/0.1',
    keywords=['InformaCast', 'Mobile', 'REST', 'API'],
    license='Apache 2.0',
    install_requires=[
        'hammock>=0.2.4',
        'requests>=2.5.3'
    ],
    classifiers=[],
    tests_require=[
        'httpretty>=0.8.8',
        'sure>=1.2.10'
    ],
)