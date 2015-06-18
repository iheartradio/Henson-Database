===============
Henson-Database
===============

Provides SQLAlchemy support to Henson Applications.

Quickstart
==========

.. code::

    from henson import Application
    from henson_database import Database

    app = Henson(__name__)
    database = Database(app)

    with db.session() as session:
        session.execute('SELECT 1;')

Configuration
=============

The following settings are used by Henson-Database. See `Engine Configuration
<http://docs.sqlalchemy.org/en/latest/core/engines.html>`_ for full information
on SQLAlchemy database URIs.

=====================   =======================================================
``DATABASE_DRIVER``     The Python driver used to connect to the database.
                        default: `'pymssql'`
``DATABASE_HOST``       The hostname to use in the SQLAlchemy database URI.
                        default: `'localhost'`
``DATABASE_PASSWORD``   default: `None`
``DATABASE_PORT``       The port the database server is listening on.
                        default: `1443`
``DATABASE_USERNAME``   default: `None`
``DATABASE_TYPE``       The database application.
                        default: `'mssql'`
=====================   =======================================================

Contents:

.. toctree::
   :maxdepth: 1

   api


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

