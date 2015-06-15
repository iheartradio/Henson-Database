"""Test handling of apps."""

import pytest

from henson import Application
from henson_database import Database


def test_app_access_with_app():
    """Test that Database.app returns the provided app."""
    app = Application('test_app')
    database = Database(app)
    assert database.app == app


def test_app_access_with_init_app(test_app):
    """Test that Database.app returns an app set by init_app."""
    app = Application('test_app')
    database = Database()
    database.init_app(app)
    assert database.app == app


def test_app_access_with_no_app_raises_runtimeerror():
    """Test that Database.app raises RuntimeError when there is no app."""
    with pytest.raises(RuntimeError):
        Database().app
