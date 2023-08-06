# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eventsourcing_axonserver', 'eventsourcing_axonserver.axonserver']

package_data = \
{'': ['*']}

install_requires = \
['axonclient>=0.1.1,<0.2.0', 'eventsourcing>=9.2.11,<9.3.0']

setup_kwargs = {
    'name': 'eventsourcing-axonserver',
    'version': '0.1',
    'description': 'Eventsourcing with Axon Server',
    'long_description': '# Welcome to Eventsourcing with Axon Server\n\nThis package supports using the Python\n[eventsourcing](https://github.com/pyeventsourcing/eventsourcing) library\nwith Axon Server.\n\n## Installation\n\n[*indicate how users can install your project*]\n\n## Getting started\n\n[*indicate how users can use your project*]\n\n## Developers\n\nAfter cloning the eventsourcing-axonserver repository, set up a virtual\nenvironment and install dependencies by running the following command in the\nroot folder.\n\n    $ make install\n\nThe ``make install`` command uses the build tool Poetry to create a dedicated\nPython virtual environment for this project, and installs popular development\ndependencies such as Black, isort and pytest.\n\nAdd tests in `./tests`. Add code in `./eventsourcing_axonserver`.\n\nStart Axon Server.\n\n    $ make start-axon-server\n\nRun tests.\n\n    $ make test\n\nCheck the formatting of the code.\n\n    $ make lint\n\nReformat the code.\n\n    $ make fmt\n\nAdd dependencies in `pyproject.toml` and then update installed packages.\n\n    $ make update-packages\n\nStop Axon Server.\n\n    $ make stop-axon-server\n',
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
