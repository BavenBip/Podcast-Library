"""Initialize Flask app."""
import os

# import os
from flask import Flask, render_template

# imports from SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy.pool import NullPool

from podcast.adapters.datareader.csvdatareader import CSVDataReader
from podcast.adapters import memory_repository, database_repository, repository_populate
import podcast.adapters.repository as repo
from podcast.adapters.orm import metadata, map_model_to_tables
from podcast.domainmodel.model import Podcast, Author


# def create_app(test_config=None):
#     """Construct the core application."""
#
#     # Create the Flask app object.
#     app = Flask(__name__)
#
#     data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'podcast', 'adapters', 'data')
#
#     # Configure the app from configuration-file settings.
#     app.config.from_object('config.Config')

def create_app(test_config=None):
    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)

    # Configure the app from configuration-file settings.
    app.config.from_object('config.Config')
    data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'podcast', 'adapters', 'data')

    if test_config is not None:
        # Load test configuration, and override any configuration settings.
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']

    # Here the "magic" of our repository pattern happens. We can easily switch between in memory data and
    # persistent database data storage for our application.

    if app.config['REPOSITORY'] == 'memory':
        # Create the MemoryRepository implementation for a memory-based repository.
        repo.repo_instance = memory_repository.MemoryRepository()
        # fill the content of the repository from the provided csv files (has to be done every time we start app!)
        database_mode = False
        memory_repository.populate(repo.repo_instance, data_path)

    elif app.config['REPOSITORY'] == 'database':
        # Configure database.
        database_uri = app.config['SQLALCHEMY_DATABASE_URI']

        # We create a comparatively simple SQLite database, which is based on a single file (see .env for URI).
        # For example the file database could be located locally and relative to the application in podcasts-19.db,
        # leading to a URI of "sqlite:///podcasts.db".
        # Note that create_engine does not establish any actual DB connection directly!
        database_echo = app.config['SQLALCHEMY_ECHO']
        # Please do not change the settings for connect_args and poolclass!
        database_engine = create_engine(database_uri, connect_args={"check_same_thread": False}, poolclass=NullPool,
                                        echo=database_echo)

        # Create the database session factory using sessionmaker (this has to be done once, in a global manner)
        session_factory = sessionmaker(autocommit=False, autoflush=True, bind=database_engine)
        # Create the SQLAlchemy DatabaseRepository instance for an sqlite3-based repository.
        repo.repo_instance = database_repository.SqlAlchemyRepository(session_factory)

        database_file_path = database_uri.split(":///")[-1]  # Extract the file path from the URI
        database_exists = os.path.isfile(database_file_path)

        metadata.reflect(bind=database_engine)
        if app.config['TESTING'] == 'True' or len(metadata.tables) == 0 or not database_exists:
            print("REPOPULATING DATABASE...")
            # For testing, or first-time use of the web application, reinitialise the database.
            clear_mappers()
            metadata.create_all(database_engine)  # Conditionally create database tables.
            with database_engine.connect() as connection:
                for table in reversed(metadata.sorted_tables):  # Remove any data from the tables.
                    connection.execute(table.delete())

            # Generate mappings that map domain model classes to the database tables.
            map_model_to_tables()

            database_mode = False
            repository_populate.populate(data_path, repo.repo_instance, database_mode)
            print("REPOPULATING DATABASE... FINISHED")

        else:
            # Solely generate mappings that map domain model classes to the database tables.
            map_model_to_tables()

    if test_config is not None:
        # Load test configuration, and override any configuration settings.
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']

    with app.app_context():
        # Register home bp
        from .home import home
        app.register_blueprint(home.home_blueprint)

        # Register catalogue bp
        from .catalogue import catalogue
        app.register_blueprint(catalogue.catalogue_blueprint)

        # Register search bp
        from .search import search
        app.register_blueprint(search.search_blueprint)

        # Register description bp
        from .description import description
        app.register_blueprint(description.description_blueprint)

        # Register playlists bp
        from .playlists import playlists
        app.register_blueprint(playlists.playlists_blueprint)

        from .authentication import authentication
        app.register_blueprint(authentication.authentication_blueprint)

    return app
