"""Test utiltities."""

from henson import Application
import pytest


@pytest.fixture
def test_app():
    """Return a test application."""
    app = Application('tesitng')
    app.settings['DATABASE_URI'] = 'sqlite://'
    return app
