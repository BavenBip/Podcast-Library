import os

import pytest

from podcast.adapters.database_repository import SqlAlchemyRepository
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from podcast.adapters import database_repository, repository_populate
from podcast.adapters.orm import metadata, map_model_to_tables

TEST_DATA_PATH_DATABASE_FULL = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'adapters', 'data')
TEST_DATA_PATH_DATABASE_LIMITED = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'tests', 'data')

TEST_DATABASE_URI_IN_MEMORY = 'sqlite://'
TEST_DATABASE_URI_FILE = 'sqlite:///podcasts-test.db'


@pytest.fixture
def database_engine():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_FILE)
    metadata.create_all(engine)  # Conditionally create database tables.
    with engine.connect() as connection:
        for table in reversed(metadata.sorted_tables):  # Remove any data from the tables.
            connection.execute(table.delete())
    map_model_to_tables()
    # Create the database session factory using sessionmaker (this has to be done once, in a global manner)
    session_factory = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    # Create the SQLAlchemy DatabaseRepository instance for an sqlite3-based repository.
    repo_instance = database_repository.SqlAlchemyRepository(session_factory)
    testing = True
    repository_populate.populate(TEST_DATA_PATH_DATABASE_LIMITED, repo_instance, testing)
    yield engine
    metadata.drop_all(engine)

@pytest.fixture
def session_factory():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    metadata.create_all(engine)
    with engine.connect() as connection:
        for table in reversed(metadata.sorted_tables):
            connection.execute(table.delete())
    map_model_to_tables()
    # Create the database session factory using sessionmaker (this has to be done once, in a global manner)
    session_factory = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    # Create the SQLAlchemy DatabaseRepository instance for an sqlite3-based repository.
    repo_instance = database_repository.SqlAlchemyRepository(session_factory)
    testing = True
    repository_populate.populate(TEST_DATA_PATH_DATABASE_FULL, repo_instance, testing)
    yield session_factory
    metadata.drop_all(engine)

@pytest.fixture
def empty_session():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    metadata.create_all(engine)
    with engine.connect() as connection:
        for table in reversed(metadata.sorted_tables):
            connection.execute(table.delete())
    map_model_to_tables()
    session_factory = sessionmaker(bind=engine)
    yield session_factory()
    metadata.drop_all(engine)

