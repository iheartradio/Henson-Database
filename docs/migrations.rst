==========
Migrations
==========

Henson-Database offers support for `Alembic <http://alembic.zzzcomputing.com>`_
migrations. To enable them, install Henson-Database with the migrations extra::

    $ python -m pip install Henson-Database[migrations]

This enables the following commands through the ``db`` namespace::

    $ henson --app APP_PATH db --help

.. hensoncli:: henson_database:Database
   :prog: henson --app APP_PATH
   :start_command: db
