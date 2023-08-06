################
mongodb_iam_user
################

.. image:: https://img.shields.io/pypi/v/ecs_composex_mongodb_iam_user.svg
        :target: https://pypi.python.org/pypi/ecs_composex_mongodb_iam_user

Compose-X Module to manage MongoDb::Atlas::AwsIamDatabaseUser


Use with ECS Compose-X
========================

Install
-----------

.. code-block:: bash

    python3 -m venv venv
    source venv/bin/activate
    pip install .

Use
-----

.. code-block:: yaml

    services:
      frontend:
        image: nginx

    x-mongodb_iam_user:
      Properties: {}
      Lookup: {}
      Settings: {}
      Services: {}
