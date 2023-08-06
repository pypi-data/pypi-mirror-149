# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['axonclient', 'axonclient.protos']

package_data = \
{'': ['*']}

install_requires = \
['grpcio>=1.44.0,<1.45.0', 'protobuf>=3.20.0,<3.21.0']

setup_kwargs = {
    'name': 'axonclient',
    'version': '0.1.1',
    'description': 'Python client for Axon Server',
    'long_description': '[*please edit this file according to the needs of your project*]\n\n# Welcome to Axon Client\n\n[*please summarise what your project provides to users*]\n\n## Installation\n\n[*indicate how users can install your project*]\n\n## Getting started\n\n[*indicate how users can use your project*]\n\n## Developers\n\nAfter cloning the axonclient repository, set up a virtual\nenvironment and install dependencies by running the following command in the\nroot folder.\n\n    $ make install\n\nThe ``make install`` command uses the build tool Poetry to create a dedicated\nPython virtual environment for this project, and installs popular development\ndependencies such as Black, isort and pytest.\n\nAdd tests in `./tests`. Add code in `./axonclient`.\n\nRun tests.\n\n    $ make test\n\nCheck the formatting of the code.\n\n    $ make lint\n\nReformat the code.\n\n    $ make fmt\n\nAdd dependencies in `pyproject.toml` and then update installed packages.\n\n    $ make update-packages\n',
    'author': 'John Bywater',
    'author_email': 'john.bywater@appropriatesoftware.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
