===============
Henson-Database
===============

Provides SQLAlchemy support to Henson Applications.

Installation
============

You can install Henson-Database using Pip::

    $ python -m pip install henso-databasen

You can also install it from source::

    $ python setup.py install

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

================   ============================================================
``DATABASE_URI``   The URI to use to connect to the database.
================   ============================================================

Contents:

.. toctree::
   :maxdepth: 1

   api
   changes


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

