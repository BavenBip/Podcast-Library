from sqlalchemy import select, inspect

from podcast.adapters.orm import metadata, categories_table


def test_database_populate_inspect_table_names(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    print(inspector.get_table_names())
    assert inspector.get_table_names() == ['authors', 'categories', 'episodes', 'playlist_episodes', 'playlists', 'podcast_categories', 'podcasts', 'reviews', 'users']

def test_database_populate_select_all_categories(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_categories_table = inspector.get_table_names()[1]

    with database_engine.connect() as connection:
        # query for records in table categories
        select_table = metadata.tables[name_of_categories_table]
        select_statement = select(select_table)
        result = connection.execute(select_statement)

        all_category_names = []
        for row in result:
            all_category_names.append(row[1]) #list of category names

        assert all_category_names == ['Religion & Spirituality', 'Food', 'Chairs']

def test_database_populate_select_all_users(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_users_table = inspector.get_table_names()[8]

    with database_engine.connect() as connection:
        # query for records in table users
        select_statement = select(metadata.tables[name_of_users_table])
        result = connection.execute(select_statement)

        all_users = []
        for row in result:
            all_users.append(row[1]) #list of user names - which is empty

        assert all_users == []

def test_database_populate_select_all_authors(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_authors_table = inspector.get_table_names()[0]

    with database_engine.connect() as connection:
        # query for records in table users
        select_statement = select(metadata.tables[name_of_authors_table])
        result = connection.execute(select_statement)

        all_authors = []
        for row in result:
            all_authors.append(row[1]) #list of author names

        assert all_authors == ['Hamish Prasad', 'AM Zapata', 'Becky Cheng']

def test_database_populate_select_all_podcasts(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_podcasts_table = inspector.get_table_names()[6]

    with database_engine.connect() as connection:
        # query for records in table users
        select_statement = select(metadata.tables[name_of_podcasts_table])
        result = connection.execute(select_statement)

        all_podcasts = []
        for row in result:
            all_podcasts.append(row[1]) #list of podcast names

        print(all_podcasts)

        assert all_podcasts == ['My Favourite Animals', 'My Favourite Dessert', 'My Favourite Ice Cream', 'My Favourite Chairs']

def test_database_populate_select_all_episodes(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_episodes_table = inspector.get_table_names()[2]

    with database_engine.connect() as connection:
        # query for records in table users
        select_statement = select(metadata.tables[name_of_episodes_table])
        result = connection.execute(select_statement)

        all_episodes = []
        for row in result:
            all_episodes.append(row[2]) #list of episode names

        assert all_episodes == ['The Buzzy Bee Battle', 'The Bees won', 'The Tiramisu Terror', 'Mmmm Tiramisu', 'The Pistachio Panic!', 'Tasty Pistachio Surprise']

def test_database_populate_select_all_playlists(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_playlists_table = inspector.get_table_names()[4]

    with database_engine.connect() as connection:
        # query for records in table playlists
        select_statement = select(metadata.tables[name_of_playlists_table])
        result = connection.execute(select_statement)

        all_playlists = []
        for row in result:
            all_playlists.append(row[2]) #list of playlist names - which is empty

        assert all_playlists == [] # playlists are empty when populating the database!

