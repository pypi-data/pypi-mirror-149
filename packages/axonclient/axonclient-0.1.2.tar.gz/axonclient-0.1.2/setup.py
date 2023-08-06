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
    'version': '0.1.2',
    'description': 'Python client for Axon Server',
    'long_description': "# Python Client for Axon Server\n\nThis package provides a Python client for\n[Axon Server](https://developer.axoniq.io/axon-server).\n\n## Installation\n\nUse pip to install the stable distribution from the Python Package Index.\n\n    $ pip install axonserver\n\nPlease note, it is recommended to install Python packages into a Python virtual environment.\n\n## Getting started\n\nStart an [Axon Server](https://developer.axoniq.io/axon-server).\n\n    $ docker run -d --name my-axon-server -p 8024:8024 -p 8124:8124 axoniq/axonserver axonserver\n\nConstruct the `AxonClient` class with a `uri` that includes the host and port of your Axon Server.\n\n```python\nfrom axonclient.client import AxonClient\n\naxon_client = AxonClient(uri='localhost:8024')\n```\nCall client methods to append and list events in Axon Server.\n\nSee the [Python eventsourcing extension project for Axon Server](https://github.com/pyeventsourcing/eventsourcing-axonserver)\nfor an example of use.\n\n## Developers\n\nAfter cloning the axonclient repository, set up a virtual\nenvironment and install dependencies by running the following command in the\nroot folder.\n\n    $ make install\n\nThe ``make install`` command uses the build tool Poetry to create a dedicated\nPython virtual environment for this project, and installs popular development\ndependencies such as Black, isort and pytest.\n\nAdd tests in `./tests`. Add code in `./axonclient`.\n\nRun tests.\n\n    $ make test\n\nCheck the formatting of the code.\n\n    $ make lint\n\nReformat the code.\n\n    $ make fmt\n\nAdd dependencies in `pyproject.toml` and then update installed packages.\n\n    $ make update-packages\n",
    'author': 'John Bywater',
    'author_email': 'john.bywater@appropriatesoftware.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pyeventsourcing/axonclient',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
