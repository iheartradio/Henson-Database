"""Database plugin for Henson."""

from contextlib import contextmanager
import os
import pkg_resources

from henson import Extension
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

__all__ = ('Database',)

try:
    _dist = pkg_resources.get_distribution(__package__)
    if not __file__.startswith(os.path.join(_dist.location, __package__)):
        # Manually raise the exception if there is a distribution but
        # it's installed from elsewhere.
        raise pkg_resources.DistributionNotFound
except pkg_resources.DistributionNotFound:
    __version__ = 'development'
else:
    __version__ = _dist.version


def from_settings(settings):
    """Return a dict created from application settings.

    Args:
        settings (dict): An application's settings.

    Returns:
        dict: The database-specific settings, formatted to use with
            :func:`connection_url`.
    """
    return {
        k.replace('DATABASE_', '', 1).lower(): v
        for k, v in settings.items()
        if k.startswith('DATABASE_')}


def to_settings(settings):
    """Return a dict of application settings.

    Args:
        settings (dict): Database-specific settings, formatted to use
            with :func:`connection_url`.

    Returns:
        dict: Application-level settings.
    """
    return {'DATABASE_{}'.format(k.upper()): v for k, v in settings.items()}


class Database(Extension):
    """An interface to interact with a relational database.

    Args:
        app (Optional[henson.base.Application]): An application instance
            that has an attribute named settings that contains a mapping
            of settings to interact with a database.
    """

    REQUIRED_SETTINGS = (
        'DATABASE_URI',
    )

    def __init__(self, app=None):
        """Initialize an instance."""
        self._engine = None
        self._model_base = None
        self._sessionmaker = None

        super().__init__(app)

    def init_app(self, app):
        """Initialize an application for use with the database.

        If database settings are provided by app as a dict rather than
        individual keys and values, expands them to the format expected by the
        extension's internal create_engine call.

        Args:
            app (henson.base.Application): Application instance that has
                an attribute named settings that contains a mapping of
                settings needed to interact with the database.
        """
        super().init_app(app)

        if 'DATABASE' in app.settings:
            app.settings.update(to_settings(app.settings['DATABASE']))

    @property
    def engine(self):
        """Return the engine.

        Returns:
            sqlalchemy.engine.Engine: The engine.
        """
        if not self._engine:
            self._engine = create_engine(self.app.settings['DATABASE_URI'])

        return self._engine

    @property
    def metadata(self):
        """Return the metadata associated with ``db.Model``.

        Returns:
            sqlalchemy.MetaData: The metadata.
        """
        return self.Model.metadata

    @property
    def Model(self):  # NOQA, not really serving as a function
        """Return a base class for creating models.

        Returns:
            sqlalchemy.ext.declarative.declarative_base: The base class
                to use for creating new models.
        """
        if not self._model_base:
            self._model_base = declarative_base()

        return self._model_base

    @contextmanager
    def session(self):
        """Yield a context manager for a SQLAlchemy session.

        Yields:
            sqlalchemy.orm.session.Session: A new session instance.
        """
        session = self.sessionmaker()
        try:
            yield session
        finally:
            session.close()

    @property
    def sessionmaker(self):
        """Return a function to get a new session.

        Returns:
            callable: A function that can be used to get a new session.
        """
        if not self._sessionmaker:
            self._sessionmaker = sessionmaker(bind=self.engine)

        return self._sessionmaker
