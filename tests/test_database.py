"""Test Database."""

from henson_database import Database


def test_engine(test_app):
    """Test that an engine is made."""
    db = Database(test_app)

    assert db.engine


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
