# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ecs_composex_mongodb_iam_user']

package_data = \
{'': ['*']}

install_requires = \
['ecs_composex>=0.18.0,<0.19.0']

setup_kwargs = {
    'name': 'ecs-composex-mongodb-iam-user',
    'version': '0.1.0',
    'description': 'Compose-X Module to manage MongoDb::Atlas::AwsIamDatabaseUser',
    'long_description': '################\nmongodb_iam_user\n################\n\n.. image:: https://img.shields.io/pypi/v/ecs_composex_mongodb_iam_user.svg\n        :target: https://pypi.python.org/pypi/ecs_composex_mongodb_iam_user\n\nCompose-X Module to manage MongoDb::Atlas::AwsIamDatabaseUser\n\n\nUse with ECS Compose-X\n========================\n\nInstall\n-----------\n\n.. code-block:: bash\n\n    python3 -m venv venv\n    source venv/bin/activate\n    pip install .\n\nUse\n-----\n\n.. code-block:: yaml\n\n    services:\n      frontend:\n        image: nginx\n\n    x-mongodb_iam_user:\n      Properties: {}\n      Lookup: {}\n      Settings: {}\n      Services: {}\n',
    'author': 'johnpreston',
    'author_email': 'john@compose-x.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
