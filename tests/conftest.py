"""Test utiltities."""

import pytest


class Application:

    """A stub application that can be used for testing.

    Args:
        **settings: Keyword arguments that will be used as settings.
    """

    def __init__(self, **settings):
        """Initialize the instance."""
        self.name = 'testing'
        self.settings = settings


@pytest.fixture
def test_app():
    """Return a test application."""
    app = Application(
        DATABASE_USERNAME='test',
        DATABASE_PASSWORD='test',
        DATABASE_DATABASE='test',
    )
    return app
