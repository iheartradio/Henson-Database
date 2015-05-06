"""Test converting to and from settings."""

from ingestion.database import from_settings, to_settings


def test_from_settings():
    """Test that from_settings converts application settings."""
    expected = {'a': 1, 'b': 2}
    actual = from_settings({'DATABASE_A': 1, 'DATABASE_B': 2})
    assert actual == expected


def test_from_settings_ignores_other_settings():
    """Test that from_settings ignores non-application settings."""
    expected = {'a': 1, 'b': 2}
    actual = from_settings({'DATABASE_A': 1, 'DATABASE_B': 2, 'OTHER': 3})
    assert actual == expected


def test_to_settings():
    """Test that to_settings creates application settings."""
    expected = {'DATABASE_A': 1, 'DATABASE_B': 2}
    actual = to_settings({'a': 1, 'b': 2})
    assert actual == expected
