# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eventsourcing_axonserver', 'eventsourcing_axonserver.axonserver']

package_data = \
{'': ['*']}

install_requires = \
['axonclient>=0.1.2,<0.2.0', 'eventsourcing>=9.2.11,<9.3.0']

setup_kwargs = {
    'name': 'eventsourcing-axonserver',
    'version': '0.1.2',
    'description': 'Python package for eventsourcing with Axon Server',
    'long_description': '# Event Sourcing with Axon Server\n\nThis package supports using the Python\n[eventsourcing](https://github.com/pyeventsourcing/eventsourcing) library\nwith [Axon Server](https://developer.axoniq.io/axon-server).\n\n## Installation\n\nUse pip to install the stable distribution from the Python Package Index.\n\n    $ pip install eventsourcing-axonserver\n\nPlease note, it is recommended to install Python packages into a Python virtual environment.\n\n## Getting started\n\nDefine aggregates and applications in the usual way. Please note, aggregate\nsequences  in Axon Server start from position `0`, so set INITIAL_VERSION\non your aggregate classes accordingly.\n\n```python\nfrom eventsourcing.application import Application\nfrom eventsourcing.domain import Aggregate, event\nfrom uuid import uuid5, NAMESPACE_URL\n\n\nclass TrainingSchool(Application):\n    def register(self, name):\n        dog = Dog(name)\n        self.save(dog)\n\n    def add_trick(self, name, trick):\n        dog = self.repository.get(Dog.create_id(name))\n        dog.add_trick(trick)\n        self.save(dog)\n\n    def get_tricks(self, name):\n        dog = self.repository.get(Dog.create_id(name))\n        return dog.tricks\n\n\nclass Dog(Aggregate):\n    INITIAL_VERSION = 0\n\n    @event(\'Registered\')\n    def __init__(self, name):\n        self.name = name\n        self.tricks = []\n\n    @staticmethod\n    def create_id(name):\n        return uuid5(NAMESPACE_URL, f\'/dogs/{name}\')\n\n    @event(\'TrickAdded\')\n    def add_trick(self, trick):\n        self.tricks.append(trick)\n```\n\nConfigure the application to use Axon Server. Set environment variable\n`PERSISTENCE_MODULE` to `\'eventsourcing_axonserver\'`, and set\n`AXONSERVER_URI` to the host and port of your Axon Server.\n\n```python\nschool = TrainingSchool(env={\n    "PERSISTENCE_MODULE": "eventsourcing_axonserver",\n    "AXONSERVER_URI": "localhost:8124",\n})\n```\n\nThe application\'s methods may be then called, from tests and\nuser interfaces.\n\n```python\nschool.register(\'Fido\')\nschool.add_trick(\'Fido\', \'roll over\')\nschool.add_trick(\'Fido\', \'play dead\')\ntricks = school.get_tricks(\'Fido\')\nassert tricks == [\'roll over\', \'play dead\']\n```\n\nFor more information, please refer to the Python\n[eventsourcing](https://github.com/johnbywater/eventsourcing) library\nand the [Axon Server](https://developer.axoniq.io/axon-server) project.\n\n## Developers\n\nClone the eventsourcing-axonserver repository, set up a virtual\nenvironment, and install dependencies.\n\nUse your IDE (e.g. PyCharm) to open the project repository. Create a\nPoetry virtual environment, and then update packages.\n\n    $ make update-packages\n\nAlternatively, use the ``make install`` command to create a dedicated\nPython virtual environment for this project.\n\n    $ make install\n\nStart Axon Server.\n\n    $ make start-axon-server\n\nRun tests.\n\n    $ make test\n\nAdd tests in `./tests`. Add code in `./eventsourcing_axonserver`.\n\nCheck the formatting of the code.\n\n    $ make lint\n\nReformat the code.\n\n    $ make fmt\n\nAdd dependencies in `pyproject.toml` and then update installed packages.\n\n    $ make update-packages\n\nStop Axon Server.\n\n    $ make stop-axon-server\n',
    'author': 'John Bywater',
    'author_email': 'john.bywater@appropriatesoftware.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pyeventsourcing/eventsourcing-axonserver',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
