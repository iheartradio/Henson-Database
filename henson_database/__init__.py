"""Database plugin for Henson."""

from contextlib import contextmanager
from pkg_resources import get_distribution

from henson import Extension
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

__all__ = ('Database',)
__version__ = get_distribution(__package__).version


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


def to_settings(settings):
    """Return a dict of application settings."""
    return {'DATABASE_{}'.format(k.upper()): v for k, v in settings.items()}


class Database(Extension):
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

        super().__init__(app)

    DEFAULT_SETTINGS = {
        'DATABASE_HOST': 'localhost',
        'DATABASE_PORT': 1433,
        'DATABASE_TYPE': 'mssql',
        'DATABASE_DRIVER': 'pymssql',
    }

    def init_app(self, app):
        """Initialize an application for use with the database.

        If database settings are provided by app as a dict rather than
        individual keys and values, expands them to the format expected by the
        extension's internal create_engine call.

        Args:
            app: Application instance that has an attribute named
              settings that contains a mapping of settings needed to
              interact with the database.
        """
        super().init_app(app)

        if 'DATABASE' in app.settings:
            app.settings.update(to_settings(app.settings['DATABASE']))

    @property
    def engine(self):
        """Return the :class:`~sqlalchemy.engine.Engine`."""
        if not self._engine:
            self._engine = create_engine(connection_url(self.app.settings))

        return self._engine

    @property
    def metadata(self):
        """Return the :class:`~sqlalchemy.MetaData` instance."""
        return self.Model.metadata

    @property
    def Model(self):  # NOQA, not really serving as a function
        """Return the :func:`~sqlalchemy.ext.declarative.declarative_base`."""
        if not self._model_base:
            self._model_base = declarative_base()

        return self._model_base

    @contextmanager
    def session(self):
        """Yield a context manager for a SQLAlchemy session.

        Yields:
            The :class:`~sqlalchemy.orm.session.Session`.
        """
        session = self.sessionmaker()
        try:
            yield session
        finally:
            session.close()

    @property
    def sessionmaker(self):
        """Return the :class:`~sqlalchemy.orm.session.sessionmaker`."""
        if not self._sessionmaker:
            self._sessionmaker = sessionmaker(bind=self.engine)

        return self._sessionmaker
