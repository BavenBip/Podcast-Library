from datetime import date, datetime

import pytest

import podcast.adapters.repository as repository
from podcast.adapters.database_repository import SqlAlchemyRepository
from podcast.adapters.orm import reviews_table
from podcast.description.services import add_review, get_podcast_by_id
from podcast.domainmodel.model import Author, Podcast, Category, User, PodcastSubscription, Episode, Review, Playlist
from podcast.adapters.datareader.csvdatareader import CSVDataReader
from podcast.adapters.repository import RepositoryException


def test_repository_can_add_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user1 = User(1, 'AM', 'AM123456789')
    repo.add_user(user1)
    repo.add_user(User(2, 'Hamish', 'Hamish123456789'))
    user3 = repo.get_user_by_name('AM')

    assert user3 == user1

def test_repository_can_retrieve_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user1 = User(1, 'AM321', '123456789AM')
    repo.add_user(user1)
    user2 = repo.get_user_by_name('AM321')
    assert user2 == User(1, 'AM321', '123456789AM')

def test_repository_does_not_retrieve_a_non_existent_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = repo.get_user_by_name('Tree the Cat')
    assert user is None

def test_repository_can_add_podcast(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    number_of_podcasts = repo.get_number_of_podcasts()
    new_podcast_id = number_of_podcasts + 1

    podcast5 = Podcast(new_podcast_id, Author(6, "AM"), "Podcast5")
    repo.add_podcast(podcast5)

    assert podcast5 == repo.get_podcast_by_id(new_podcast_id)

def test_repository_does_not_retrieve_a_non_existent_podcast(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    podcast7 = repo.get_podcast_by_id(500)
    assert podcast7 is None

def test_repository_can_get_first_podcast(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    podcast = repo.get_first_podcast()
    assert podcast.title == 'My Favourite Animals'

def test_repository_can_get_last_podcast(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    podcast = repo.get_last_podcast()
    assert podcast.title == 'My Favourite Chairs'

def test_repository_does_not_retrieve_podcast_for_non_existent_id(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    podcast = repo.get_podcast_by_id(100)
    assert podcast is None

def test_repository_returns_none_when_there_are_no_previous_podcasts(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    podcast = repo.get_podcast_by_id(1)
    previous_podcast = repo.get_previous_podcast(podcast)

    assert previous_podcast is None


def test_repository_returns_none_when_there_are_no_subsequent_podcasts(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    podcast = repo.get_podcast_by_id(4)
    next_podcast = repo.get_next_podcast(podcast)

    assert next_podcast is None

def test_repository_can_add_a_category(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    category = Category(3, 'Food')
    repo.add_category(category)

    assert category in repo.get_categories()

def test_repository_can_add_a_review(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user1 = User(1, 'AM321', '123456789AM')
    repo.add_user(user1)

    podcast5 = Podcast(5, Author(6, "AM"), "Podcast5", None, "", "", None, "English")
    repo.add_podcast(podcast5)
    review = repo.add_review(user1, podcast5, 4, "Tree's onto it!")

    assert review in repo.get_reviews(5)

#BELOW MUST BE FIXED
def make_review(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user1 = User(1, 'AM321', '123456789AM')
    repo.add_user(user1)
    user = repo.get_podcast_by_id(1)

    podcast5 = Podcast(5, Author(6, "AM"), "Podcast5", None, "", "", None, "English")
    repo.add_podcast(podcast5)
    podcast = repo.get_podcast_by_id(5)

    review = repo.add_review(podcast, "Tree's onto it!", user, 4)

    assert review in repo.get_reviews(5)


