"""Test handling of apps."""

import pytest

from henson_database import get_app


def test_get_app_with_app():
    """Test that get_app returns the provided app."""
    expected = object()
    actual = get_app(expected)
    assert actual == expected


def test_get_app_with_registry(test_app):
    """Test that get_app returns an app from the registry."""
    actual = get_app()
    assert actual == test_app


def test_get_app_with_no_app_raises_runtimeerror():
    """Test that get_app raises RuntimeError when there is no app."""
    with pytest.raises(RuntimeError):
        get_app()
