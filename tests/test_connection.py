"""Test connection-related functionality."""

from henson_database import connection_url


def test_connection_url():
    """Test that connection_url returns a SQLAlchemy-friendly URI."""
    expected = 'TYPE+DRIVER://USER:PASSWORD@HOST:PORT/DATABASE'
    settings = {
        'DATABASE_DRIVER': 'DRIVER',
        'DATABASE_TYPE': 'TYPE',
        'DATABASE_USERNAME': 'USER',
        'DATABASE_PASSWORD': 'PASSWORD',
        'DATABASE_HOST': 'HOST',
        'DATABASE_PORT': 'PORT',
        'DATABASE_DATABASE': 'DATABASE',
    }
    actual = connection_url(settings)
    assert actual == expected
