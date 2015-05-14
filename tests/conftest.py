"""Test utiltities."""

from henson.base import registry
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

        # Register the app with the registry just like a real one would
        # do.
        registry.current_application = self


@pytest.fixture
def clean_up_registry(request):
    """Clean up the application registry after the test is run."""
    original = registry._applications
    registry._applications = []

    def teardown():
        registry._applications = original
    request.addfinalizer(teardown)

    return registry


@pytest.fixture
def test_app(clean_up_registry):
    """Return a test application."""
    app = Application(
        DATABASE_USERNAME='test',
        DATABASE_PASSWORD='test',
        DATABASE_DATABASE='test',
    )
    return app
