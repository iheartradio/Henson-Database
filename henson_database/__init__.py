"""Database plugin for Henson."""

from contextlib import contextmanager
import os
import pkg_resources

try:
    # Try to import Alembic to determine if command line migrations
    # should be enabled.
    import alembic.command as alembic
    from alembic.config import Config as AlembicConfig
except ImportError:
    alembic = None
from henson import Extension
from henson.cli import register_commands
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


if alembic:
    # This class is only needed when migrations are enabled.
    class Config(AlembicConfig):
        def get_template_directory(self):
            return os.path.join(os.path.dirname(__file__), 'templates')


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

    .. versionchanged:: 0.4.0

        Alembic migrations are supported.
    """

    DEFAULT_SETTINGS = {
        'DATABASE_MIGRATIONS_DIRECTORY': 'migrations',
    }

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

    def register_cli(self):
        """Register the command line interface.

        .. versionadded:: 0.4.0
        """
        # A try/except is being used here rather than suppress so that
        # any ImportErrors raised as a result of registering the
        # commands aren't swallowed.
        try:
            #
            import alembic  # NOQA
        except ImportError:
            # Don't enable migrations.
            pass
        else:
            # Alembic is installed so the CLI should be enabled.
            register_commands('db', (
                branches,
                current,
                downgrade,
                edit,
                generate,
                heads,
                history,
                init,
                merge,
                revision,
                show,
                stamp,
                upgrade,
            ))

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


def branches(app, *, verbose: 'use more verbose output' = False):
    """Show current branch points."""
    alembic.branches(_get_config(app), verbose=verbose)


def current(app, *, verbose: 'use more verbose output' = False):
    """Display the current revision for a database."""
    alembic.current(_get_config(app), verbose=verbose)


def downgrade(app,
              revision: 'revision identifier' = '-1',
              *,
              sql: (
                  "don't emit SQL to database - dump to standard "
                  "output/file instead"
              ) = False,
              tag: (
                  "arbitrary 'tag' name - can be used by custom env.py "
                  "scripts"
              ) = None):
    """Revert to a previous version."""
    alembic.downgrade(_get_config(app), revision=revision, sql=sql, tag=tag)


def edit(app, rev):
    """Edit revision script(s) using $EDITOR."""
    alembic.edit(_get_config(app), rev=rev)


def generate(app,
             *,
             message: "message string to use with 'revision'" = None,
             sql: (
                 "don't emit SQL to database - dump to standard "
                 "output/file instead"
             ) = False,
             head: (
                 'specify head revision or <branchname>@head to base '
                 'new revision on'
             ) = 'head',
             splice: (
                 "allow a non-head revision as the 'head' to splice "
                 "onto"
             ) = False,
             branch_label: (
                 'specify a branch label to apply to the new revision') = None,
             version_path: (
                 'specify specific path from config for version file') = None,
             rev_id: (
                 'specify a hardcoded revision id instead of '
                 'generating one'
             ) = None,
             depends_on: (
                 'specify one or more revision identifiers which this '
                 'revision should depend on'
             ) = None):
    """Generate a revision (alias for 'revision --autogenerate')."""
    revision(
        app,
        message=message,
        autogenerate=True,
        sql=sql,
        head=head,
        splice=splice,
        branch_label=branch_label,
        version_path=version_path,
        rev_id=rev_id,
        depends_on=depends_on,
    )


def heads(app,
          *,
          verbose: 'use more verbose output' = False,
          resolve_dependencies: (
              'treat dependency versions as down revisions') = False):
    """Show current available heads in the script directory."""
    alembic.heads(
        _get_config(app),
        verbose=verbose,
        resolve_dependencies=resolve_dependencies,
    )


def history(app,
            *,
            rev_range: (
                'specify a revision range; format is [start]:[end]') = None,
            verbose: 'use more verbose output' = False):
    """List changeset scripts in chronological order."""
    alembic.history(_get_config(app), rev_range=rev_range, verbose=verbose)


def init(app, directory: 'location of scripts directory' = None):
    """Initialize a new scripts directory."""
    directory = directory or app.settings['DATABASE_MIGRATIONS_DIRECTORY']

    config = Config()
    config.set_main_option('script_location', directory)
    config.config_file_name = os.path.join(directory, 'alembic.ini')

    alembic.init(config, directory=directory, template='henson')


def merge(app,
          revisions: "one or more revisions, or 'heads' for all heads",
          *,
          message: "message string to use with 'revision'" = None,
          branch_label: 'specify a branch apply to the new revision' = None,
          rev_id: (
              'specify a hardcoded revision id instead of generating '
              'one'
          ) = None):
    """Merge two revisions together. Creates a new migration file."""
    alembic.merge(
        _get_config(app),
        revisions=revisions,
        message=message,
        branch_label=branch_label,
        rev_id=rev_id,
    )


def revision(app,
             *,
             message: "message string to use with 'revision'" = None,
             autogenerate: (
                 'populate revision script with candidate migration '
                 'operations, based on comparison of database to model'
             ) = False,
             sql: (
                 "don't emit SQL to database - dump to standard "
                 "output/file instead"
             ) = False,
             head: (
                 'specify head revision or <branchname>@head to base '
                 'new revision on'
             ) = 'head',
             splice: (
                 "allow a non-head revision as the 'head' to splice "
                 "onto"
             ) = False,
             branch_label: (
                 'specify a branch label to apply to the new revision') = None,
             version_path: (
                 'specify specific path from config for version file') = None,
             rev_id: (
                 'specify a hardcoded revision id instead of '
                 'generating one'
             ) = None,
             depends_on: (
                 'specify one or more revision identifiers which this '
                 'revision should depend on'
             ) = None):
    """Create a new revision file."""
    alembic.revision(
        _get_config(app),
        message=message,
        autogenerate=autogenerate,
        sql=sql,
        head=head,
        splice=splice,
        branch_label=branch_label,
        version_path=version_path,
        rev_id=rev_id,
        depends_on=depends_on,
    )


def show(app, rev):
    """Show the revision(s) denoted by the given symbol."""
    alembic.show(_get_config(app), rev=rev)


def stamp(app,
          revision: 'revision identifier',
          *,
          sql: (
              "don't emit SQL to database - dump to standard "
              "output/file instead"
          ) = False,
          tag: (
              "arbitrary 'tag' name - can be used by custom env.py "
              "scripts"
          ) = None):
    """‘stamp’ the revision table with the given revision; don’t run any migrations."""  # NOQA
    alembic.stamp(_get_config(app), revision=revision, sql=sql, tag=tag)


def upgrade(app,
            revision: 'revision identifier' = 'head',
            *,
            sql: (
                "don't emit SQL to database - dump to standard "
                "output/file instead"
            ) = False,
            tag: (
                "arbitrary 'tag' name - can be used by custom env.py "
                "scripts"
            ) = None):
    """Upgrade to a later version."""
    alembic.upgrade(_get_config(app), revision=revision, sql=sql, tag=tag)


def _get_config(app):
    directory = app.settings['DATABASE_MIGRATIONS_DIRECTORY']
    config = Config(os.path.join(directory, 'alembic.ini'))
    config.set_main_option('script_location', directory)

    # Alembic's env.py needs access to the application instance to get
    # the metadata for the database. Because Henson has no application
    # context, there's no way to get the application through the henson
    # package. Fortuantely Alembic's Config provides an attributes
    # dictionary to pass arbitrary values into it.
    config.attributes['henson_application'] = app

    return config
