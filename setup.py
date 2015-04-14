from distutils.core import setup

setup(
    name='icm-python-client',
    packages=['icm_python_client'],
    version='0.0.1',
    description='A simple python client for InformaCast Mobile based on requests and Hammock',
    author='Vincent Pizzo',
    author_email='vincent.pizzo@singlewire.com',
    url='https://github.com/singlewire/icm-python-client',
    download_url='https://github.com/singlewire/icm-python-client/tarball/0.1',
    keywords=['InformaCast', 'Mobile', 'REST', 'API'],
    license='Apache 2.0',
    install_requires=[
        'hammock>=0.2.4'
    ],
    classifiers=[],
)