"""Test Database."""

import logging

from ingestion.database import Database


def test_engine(test_app):
    """Test that an engine is made."""
    db = Database(test_app)

    assert db.engine


def test_init_app_defaults(test_app):
    """Test the default settings are added."""
    test_app.settings = {}

    db = Database()
    db.init_app(test_app)

    default_settings = (
        'DATABASE_HOST', 'DATABASE_PORT', 'DATABASE_TYPE', 'DATABASE_DRIVER')
    assert all(k in test_app.settings for k in default_settings)


def test_init_app_settings_from_database_key(test_app):
    """Test that init_app properly handles a DATABASE setting dict."""
    test_app.settings['DATABASE'] = {'host': 'hostname', 'port': 'portnumber'}

    db = Database()
    db.init_app(test_app)

    assert test_app.settings['DATABASE_HOST'] == 'hostname'
    assert test_app.settings['DATABASE_PORT'] == 'portnumber'


def test_session(test_app):
    """Test the session context manager."""
    db = Database(test_app)

    with db.session() as session:
        assert hasattr(session, 'commit')
        assert hasattr(session, 'rollback')


def test_sessionmaker(test_app):
    """Test that a sessionmaker is made."""
    db = Database(test_app)

    assert db.sessionmaker
