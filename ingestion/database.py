"""Database plugin for the Ingestion Pipeline."""

from contextlib import contextmanager

from ingestion.service import registry
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

__all__ = ('Database',)


def connection_url(settings):
    """Return a SQLAlchemy database URI."""
    settings = from_settings(settings)
    template = \
        '{type}+{driver}://{username}:{password}@{host}:{port}/{database}'
    return template.format(**settings)


def from_settings(settings):
    """Return a dict created from application settings."""
    return {
        k.replace('DATABASE_', '', 1).lower(): v
        for k, v in settings.items()
        if k.startswith('DATABASE_')}


def get_app(app=None):
    """Return an application.

    If not application is provided through ``app``, the application
    registry will be checked for the most recently registered
    application.

    Args:
        app (:class:`~ingestion.service.Application`, optional): An
          application that will be returned if provided.

    Returns:
        :class:`~ingestion.service.Application`: The application

    Raises:
        RuntimeError: There is no application.
    """
    if app is not None:
        return app

    app = registry.current_application
    if app is not None:
        return app

    raise RuntimeError(
        'The database is not registered to an application and no '
        'application is available.')


def to_settings(settings):
    """Return a dict of application settings."""
    return {'DATABASE_{}'.format(k.upper()): v for k, v in settings.items()}


class Database:

    """An interface to interact with a relational database.

    Args:
        app (optional): An application instance that has an attribute
          named settings that contains a mapping of settings to interact
          with a database.
    """

    def __init__(self, app=None):
        """Initialize an instance."""
        self._engine = None
        self._model_base = None
        self._sessionmaker = None

        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Initialize an application for use with the database.

        Args:
            app: Application instance that has an attribute named
              settings that contains a mapping of settings needed to
              interact with the database.
        """
        app.settings.setdefault('DATABASE_HOST', 'localhost')
        app.settings.setdefault('DATABASE_PORT', 1433)
        app.settings.setdefault('DATABASE_TYPE', 'mssql')
        app.settings.setdefault('DATABASE_DRIVER', 'pymssql')

        if 'DATABASE' in app.settings:
            app.settings.update(to_settings(app.settings['DATABASE']))

    @property
    def engine(self):
        """Return the SQLAlchemy engine."""
        if not self._engine:
            app = get_app(self.app)
            self._engine = create_engine(connection_url(app.settings))

        return self._engine

    @property
    def Model(self):  # NOQA, not really serving as a function
        """Return the SQLAlchemy base declarative model."""
        if not self._model_base:
            self._model_base = declarative_base()

        return self._model_base

    @contextmanager
    def session(self):
        """Return a context manager for a SQLAlchemy session.

        Yields:
            The session.
        """
        session = self.sessionmaker()
        try:
            yield session
        finally:
            session.close()

    @property
    def sessionmaker(self):
        """Return the SQLAlchemy session maker."""
        if not self._sessionmaker:
            self._sessionmaker = sessionmaker(bind=self.engine)

        return self._sessionmaker
