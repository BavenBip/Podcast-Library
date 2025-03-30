import pytest

import datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy import text

from podcast.domainmodel.model import User, Review, Podcast, PodcastSubscription, Author, Playlist, Episode, Category


def insert_user(empty_session, values=None):
    new_id = 1
    new_name = "Andrew"
    new_password = "1234"

    if values is not None:
        new_id = values[0]
        new_name = values[1]
        new_password = values[2]

    empty_session.execute(text('INSERT INTO users (user_id, user_name, password) VALUES (:user_id, :user_name, :password)'),
                          {'user_id': new_id, 'user_name': new_name, 'password': new_password})
    row = empty_session.execute(text('SELECT user_id from users where user_name = :user_name'),
                                {'user_name': new_name}).fetchone()
    return row


def insert_users(empty_session, values):
    for value in values:
        empty_session.execute(text('INSERT INTO users (user_id, user_name, password) VALUES (:user_id, :user_name, :password)'),
                              {'user_id': value[0], 'user_name': value[1], 'password': value[2]})
    rows = list(empty_session.execute(text('SELECT user_id from users')))
    keys = tuple(row[0] for row in rows)
    return keys


def insert_podcast(empty_session, values=None):
    new_id = 6
    new_title = 'Podcast Six'
    new_image_url = 'no image url'
    new_description = 'welcome to the world of podcast six!'
    new_language = 'English'
    new_website_url = 'no website url'
    new_author_id = 2
    new_itunes_id = 5

    if values is not None:
        new_id = values[0]
        new_title = values[1]
        new_image_url = values[2]
        new_description = values[3]
        new_language = values[4]
        new_website_url = values[5]
        new_author_id = values[6]
        new_itunes_id = values[7]

    empty_session.execute(text('INSERT INTO podcasts (podcast_id, title, image_url, description, language, website_url, author_id, itunes_id) VALUES (:podcast_id, :title, :image_url, :description, :language, :website_url, :author_id, :itunes_id)'),
                          {'podcast_id': new_id, 'title': new_title, 'image_url': new_image_url, 'description': new_description, 'language': new_language, 'website_url': new_website_url, 'author_id': new_author_id, 'itunes_id': new_itunes_id})
    row = empty_session.execute(text('SELECT podcast_id from podcasts')).fetchone()
    return row[0]


def insert_categories(empty_session):
    empty_session.execute(
        text('INSERT INTO categories (category_id, category_name) VALUES (5, "Religion & Spirituality")'))
    rows = list(empty_session.execute(text('SELECT category_id from categories')))
    keys = tuple(row[0] for row in rows)
    return keys


def insert_reviewed_podcast(empty_session):
    podcast_key = int(insert_podcast(empty_session))
    user_key = int(insert_user(empty_session)[0])
    rating = 5
    comment = 'this is a comment'

    empty_session.execute(
        text('INSERT INTO reviews (user_id, podcast_id, rating, comment) VALUES (:user_id, :podcast_id, :rating, :comment)'),
        {'user_id': user_key, 'podcast_id': podcast_key, 'rating': rating, 'comment': comment}
    )

    row = empty_session.execute(text('SELECT id from reviews')).fetchone()
    return row[0]


def make_podcast():
    podcast = Podcast(5, Author(4, "Tree"), "Tallin Country Church", "Tallin Messages", "description of Podcast Five", "https://resources.stuff.co.nz/content/dam/images/1/z/e/3/w/n/image.related.StuffLandscapeSixteenByNine.1240x700.1zduvk.png/1583369866749.jpg", 1165994461, "English")
    return podcast


def make_user():
    user = User(2, "Andrew", "pw1234")
    return user


def make_category():
    category = Category("Religion & Spirituality")
    return category


def test_loading_of_users(empty_session):
    users = list()
    users.append((1, "Andrew", "pw1234"))
    users.append((2, "Cindy", "pw1111"))
    insert_users(empty_session, users)

    expected = [
        User(1, "Andrew", "pw1234"),
        User(2, "Cindy", "pw1111")
    ]
    assert empty_session.query(User).all() == expected


def test_saving_of_users(empty_session):
    user = make_user()
    empty_session.add(user)
    empty_session.commit()

    rows = list(empty_session.execute(text('SELECT user_name, password FROM users')))
    assert rows == [("Andrew", "pw1234")]


def test_saving_of_users_with_common_user_name(empty_session):
    insert_user(empty_session, [1, "Andrew", "1234"])
    empty_session.commit()

    with pytest.raises(IntegrityError):
        user = User(2, "Andrew", "1111")
        empty_session.add(user)
        empty_session.commit()


def test_loading_of_podcast(empty_session):
    podcast_key = insert_podcast(empty_session) # inserts new podcast and fetches id of new podcast
    fetched_podcast = empty_session.query(Podcast).one() #retrieves the podcast id

    assert podcast_key == fetched_podcast.id


def test_loading_of_reviewed_podcast(empty_session):  # Comment or Reviews?
    insert_reviewed_podcast(empty_session)

    rows = empty_session.query(Podcast).all()
    podcast = rows[0]

    for review in podcast.reviews:
        assert review.podcast is podcast


def test_saving_of_comment(empty_session):
    podcast = Podcast(5, Author(4, "Tree"), "Tallin Country Church", "Tallin Messages", "description of Podcast Five", "https://resources.stuff.co.nz/content/dam/images/1/z/e/3/w/n/image.related.StuffLandscapeSixteenByNine.1240x700.1zduvk.png/1583369866749.jpg", 1165994461, "English")
    user = User(1, "Andrew", "pw1234")
    comment = "Some comment text."
    review = Review(100, user, podcast, 5, comment)

    empty_session.add(review)
    empty_session.commit()

    rows = list(empty_session.execute(text('SELECT user_id, podcast_id, comment FROM reviews')))
    assert rows == [(1, 5, 'Some comment text.')]


def test_save_reviewed_podcast(empty_session):  # Comment or Reviews?
    insert_reviewed_podcast(empty_session)

    rows = empty_session.query(Podcast).all()
    podcast = rows[0]

    rows = list(empty_session.execute(text('SELECT user_id, podcast_id, comment FROM reviews')))
    assert rows == [(1, 6, 'this is a comment')] # this is the same as: [(user_key, podcast_key, comment_text)]

