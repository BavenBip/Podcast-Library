import os
from datetime import datetime

import pytest

from podcast.adapters.memory_repository import MemoryRepository, populate
from podcast.domainmodel.model import Author, Podcast, Category, User, PodcastSubscription, Episode, Review, Playlist
from podcast.adapters.datareader.csvdatareader import CSVDataReader


def test_author_initialization():
    author1 = Author(1, "Brian Denny")
    assert repr(author1) == "<Author 1: Brian Denny>"
    assert author1.name == "Brian Denny"

    with pytest.raises(ValueError):
        author2 = Author(2, "")

    with pytest.raises(ValueError):
        author3 = Author(3, 123)

    author4 = Author(4, " USA Radio   ")
    assert author4.name == "USA Radio"

    author4.name = "Jackson Mumey"
    assert repr(author4) == "<Author 4: Jackson Mumey>"


def test_author_eq():
    author1 = Author(1, "Author A")
    author2 = Author(1, "Author A")
    author3 = Author(3, "Author B")
    assert author1 == author2
    assert author1 != author3
    assert author3 != author2
    assert author3 == author3


def test_author_lt():
    author1 = Author(1, "Jackson Mumey")
    author2 = Author(2, "USA Radio")
    author3 = Author(3, "Jesmond Parish Church")
    assert author1 < author2
    assert author2 > author3
    assert author1 < author3
    author_list = [author3, author2, author1]
    assert sorted(author_list) == [author1, author3, author2]


def test_author_hash():
    authors = set()
    author1 = Author(1, "Doctor Squee")
    author2 = Author(2, "USA Radio")
    author3 = Author(3, "Jesmond Parish Church")
    authors.add(author1)
    authors.add(author2)
    authors.add(author3)
    assert len(authors) == 3
    assert repr(
        sorted(authors)) == "[<Author 1: Doctor Squee>, <Author 3: Jesmond Parish Church>, <Author 2: USA Radio>]"
    authors.discard(author1)
    assert repr(sorted(authors)) == "[<Author 3: Jesmond Parish Church>, <Author 2: USA Radio>]"


def test_author_name_setter():
    author = Author(1, "Doctor Squee")
    author.name = "   USA Radio  "
    assert repr(author) == "<Author 1: USA Radio>"

    with pytest.raises(ValueError):
        author.name = ""

    with pytest.raises(ValueError):
        author.name = 123


def test_category_initialization():
    category1 = Category(1, "Comedy")
    assert repr(category1) == "<Category 1: Comedy>"
    category2 = Category(2, " Christianity ")
    assert repr(category2) == "<Category 2: Christianity>"

    with pytest.raises(ValueError):
        category3 = Category(3, 300)

    category5 = Category(5, " Religion & Spirituality  ")
    assert category5.name == "Religion & Spirituality"

    with pytest.raises(ValueError):
        category1 = Category(4, "")


def test_category_name_setter():
    category1 = Category(6, "Category A")
    assert category1.name == "Category A"

    with pytest.raises(ValueError):
        category1 = Category(7, "")

    with pytest.raises(ValueError):
        category1 = Category(8, 123)


def test_category_eq():
    category1 = Category(9, "Action")
    category2 = Category(10, "Indie")
    category3 = Category(11, "Sports")
    assert category1 == category1
    assert category1 != category2
    assert category2 != category3
    assert category1 != "9: Adventure"
    assert category2 != 105


def test_category_hash():
    category1 = Category(9, "Action")
    category2 = Category(10, "Indie")
    category3 = Category(11, "Sports")
    category_set = set()
    category_set.add(category1)
    category_set.add(category2)
    category_set.add(category3)
    assert sorted(category_set) == [category1, category2, category3]
    category_set.discard(category2)
    category_set.discard(category1)
    assert sorted(category_set) == [category3]


def test_category_lt():
    category1 = Category(9, "Action")
    category2 = Category(10, "Indie")
    category3 = Category(11, "Sports")
    assert category1 < category2
    assert category2 < category3
    assert category3 > category1
    category_list = [category3, category2, category1]
    assert sorted(category_list) == [category1, category2, category3]


# Fixtures to reuse in multiple tests
@pytest.fixture
def my_author():
    return Author(1, "Joe Toste")


@pytest.fixture
def my_podcast(my_author):
    return Podcast(100, my_author, "Joe Toste Podcast - Sales Training Expert")


@pytest.fixture
def my_user():
    return User(1, "Shyamli", "pw12345")


@pytest.fixture
def my_subscription(my_user, my_podcast):
    return PodcastSubscription(1, my_user, my_podcast)


def test_podcast_initialization():
    author1 = Author(1, "Doctor Squee")
    podcast1 = Podcast(2, author1, "My First Podcast")
    assert podcast1.id == 2
    assert podcast1.author == author1
    assert podcast1.title == "My First Podcast"
    assert podcast1.description == ""
    assert podcast1.website == ""

    assert repr(podcast1) == "<Podcast 2: 'My First Podcast' by Doctor Squee>"

    with pytest.raises(ValueError):
        podcast3 = Podcast(-123, author1)

    podcast4 = Podcast(123, author1)
    assert podcast4.title is 'Untitled'
    assert podcast4.image is None


def test_podcast_change_title(my_podcast):
    my_podcast.title = "TourMix Podcast"
    assert my_podcast.title == "TourMix Podcast"

    with pytest.raises(ValueError):
        my_podcast.title = ""


def test_podcast_add_category(my_podcast):
    category = Category(12, "TV & Film")
    my_podcast.add_category(category)
    assert category in my_podcast.categories
    assert len(my_podcast.categories) == 1

    my_podcast.add_category(category)
    my_podcast.add_category(category)
    assert len(my_podcast.categories) == 1


def test_podcast_remove_category(my_podcast):
    category1 = Category(13, "Technology")
    my_podcast.add_category(category1)
    my_podcast.remove_category(category1)
    assert len(my_podcast.categories) == 0

    category2 = Category(14, "Science")
    my_podcast.add_category(category1)
    my_podcast.remove_category(category2)
    assert len(my_podcast.categories) == 1


def test_podcast_title_setter(my_podcast):
    my_podcast.title = "Dark Throne"
    assert my_podcast.title == 'Dark Throne'

    with pytest.raises(ValueError):
        my_podcast.title = " "

    with pytest.raises(ValueError):
        my_podcast.title = ""


def test_podcast_eq():
    author1 = Author(1, "Author A")
    author2 = Author(2, "Author C")
    author3 = Author(3, "Author B")
    podcast1 = Podcast(100, author1, "Joe Toste Podcast - Sales Training Expert")
    podcast2 = Podcast(200, author2, "Voices in AI")
    podcast3 = Podcast(101, author3, "Law Talk")
    assert podcast1 == podcast1
    assert podcast1 != podcast2
    assert podcast2 != podcast3


def test_podcast_hash():
    author1 = Author(1, "Author A")
    author2 = Author(2, "Author C")
    author3 = Author(3, "Author B")
    podcast1 = Podcast(100, author1, "Joe Toste Podcast - Sales Training Expert")
    podcast2 = Podcast(100, author2, "Voices in AI")
    podcast3 = Podcast(101, author3, "Law Talk")
    podcast_set = {podcast1, podcast2, podcast3}
    assert len(podcast_set) == 2  # Since podcast1 and podcast2 have the same ID


def test_podcast_lt():
    author1 = Author(1, "Author A")
    author2 = Author(2, "Author C")
    author3 = Author(3, "Author B")
    podcast1 = Podcast(100, author1, "Joe Toste Podcast - Sales Training Expert")
    podcast2 = Podcast(200, author2, "Voices in AI")
    podcast3 = Podcast(101, author3, "Law Talk")
    assert podcast1 < podcast2
    assert podcast2 > podcast3
    assert podcast3 > podcast1


def test_user_initialization():
    user1 = User(1, "Shyamli", "pw12345")
    user2 = User(2, "asma", "pw67890")
    user3 = User(3, "JeNNy  ", "pw87465")
    assert repr(user1) == "<User 1: Shyamli>"
    assert repr(user2) == "<User 2: asma>"
    assert repr(user3) != "<User 3: jenny>"
    assert user2.password == "pw67890"
    with pytest.raises(ValueError):
        user4 = User(4, "xyz  ", "")
    with pytest.raises(ValueError):
        user4 = User(5, "    ", "qwerty12345")


def test_user_eq():
    user1 = User(1, "Shyamli", "pw12345")
    user2 = User(2, "asma", "pw67890")
    user3 = User(3, "JeNNy  ", "pw87465")
    user4 = User(1, "Shyamli", "pw12345")
    assert user1 == user4
    assert user1 != user2
    assert user2 != user3


def test_user_hash():
    user1 = User(1, "   Shyamli", "pw12345")
    user2 = User(2, "asma", "pw67890")
    user3 = User(3, "JeNNy  ", "pw87465")
    user_set = set()
    user_set.add(user1)
    user_set.add(user2)
    user_set.add(user3)
    assert sorted(user_set) == [user2, user3, user1]
    user_set.discard(user1)
    user_set.discard(user2)
    assert list(user_set) == [user3]


def test_user_lt():
    user1 = User(1, "Shyamli", "pw12345")
    user2 = User(2, "asma", "pw67890")
    user3 = User(3, "JeNNy  ", "pw87465")
    assert user1 > user2
    assert user2 < user3
    assert user3 < user1
    user_list = [user3, user2, user1]
    assert sorted(user_list) == [user2, user3, user1]


def test_user_add_remove_favourite_podcasts(my_user, my_subscription):
    my_user.add_subscription(my_subscription)
    assert repr(my_user.subscription_list) == "[<PodcastSubscription 1: Owned by Shyamli>]"
    my_user.add_subscription(my_subscription)
    assert len(my_user.subscription_list) == 1
    my_user.remove_subscription(my_subscription)
    assert repr(my_user.subscription_list) == "[]"


def test_podcast_subscription_initialization(my_subscription):
    assert my_subscription.id == 1
    assert repr(my_subscription.owner) == "<User 1: Shyamli>"
    assert repr(my_subscription.podcast) == "<Podcast 100: 'Joe Toste Podcast - Sales Training Expert' by Joe Toste>"
    assert repr(my_subscription) == "<PodcastSubscription 1: Owned by Shyamli>"


def test_podcast_subscription_set_owner(my_subscription):
    new_user = User(2, "asma", "pw67890")
    my_subscription.owner = new_user
    assert my_subscription.owner == new_user

    with pytest.raises(TypeError):
        my_subscription.owner = "not a user"


def test_podcast_subscription_set_podcast(my_subscription):
    author2 = Author(2, "Author C")
    new_podcast = Podcast(200, author2, "Voices in AI")
    my_subscription.podcast = new_podcast
    assert my_subscription.podcast == new_podcast

    with pytest.raises(TypeError):
        my_subscription.podcast = "not a podcast"


def test_podcast_subscription_equality(my_user, my_podcast):
    sub1 = PodcastSubscription(1, my_user, my_podcast)
    sub2 = PodcastSubscription(1, my_user, my_podcast)
    sub3 = PodcastSubscription(2, my_user, my_podcast)
    assert sub1 == sub2
    assert sub1 != sub3


def test_podcast_subscription_hash(my_user, my_podcast):
    sub1 = PodcastSubscription(1, my_user, my_podcast)
    sub2 = PodcastSubscription(1, my_user, my_podcast)
    sub_set = {sub1, sub2}  # Should only contain one element since hash should be the same
    assert len(sub_set) == 1


def test_csvdatareader():
    csv_test_content = CSVDataReader(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data'))
    author1 = Author(1, 'Hamish Prasad')
    podcast1 = Podcast(1, author1, 'My Favourite Animals', 'no_image', 'Bees are pretty cool', 'no_website', 101,
                       'English')
    formatting = "%Y-%d-%m %H:%M:%S%z"
    episode1 = Episode(1, podcast1, 'The Buzzy Bee Episode', 'sorry_no_link', 812, 'Buzz Buzz',
                       datetime.strptime('2003-17-11 00:00:00+0000', formatting))
    category1 = Category(1, 'Religion & Spirituality')

    assert csv_test_content.podcast_list[0] == podcast1
    assert csv_test_content.episode_list[0] == episode1
    assert csv_test_content.author_dict['Hamish Prasad'] == author1
    assert csv_test_content.cat_dict['Religion & Spirituality'] == category1


def test_episode_initialization():
    author1 = Author(1, "fish")
    podcast1 = Podcast(200, author1, "how to fish")
    formatting = "%Y-%d-%m %H:%M:%S%z"
    date1 = datetime.strptime('2003-17-11 00:00:00+0000', formatting)
    episode1 = Episode(1, podcast1, "first fish", "fish_hyperlink", 180, "fish_description",
                       date1)
    assert episode1.id == 1
    assert episode1.title == "first fish"
    assert episode1.audio == "fish_hyperlink"
    assert episode1.audio_length == 180
    assert episode1.description == "fish_description"
    assert episode1.pub_date == date1


def test_episode_title_setter():
    author1 = Author(1, "chef")
    podcast1 = Podcast(200, author1, "how to pizza")
    formatting = "%Y-%d-%m %H:%M:%S%z"
    episode1 = Episode(6, podcast1, "Pizza", "pizza_hyperlink", 180, "pizza_description",
                       datetime.strptime('2003-17-11 00:00:00+0000', formatting))
    assert episode1.title == "Pizza"
    with pytest.raises(ValueError):
        episode1.title = ""
    with pytest.raises(ValueError):
        episode1.title = 235


def test_episode_change_title():
    author1 = Author(678, "the cancelled ones")
    podcast1 = Podcast(333, author1, "conspiracy theories", "triangle", "katy perry", "website goes here", 230,
                       "English")
    formatting = "%Y-%d-%m %H:%M:%S%z"

    date1 = datetime.strptime('2003-17-11 00:00:00+0000', formatting)
    episode1 = Episode(69, podcast1, "world", "cool_hyperlink", 333, "you already know", date1)
    episode1.title = "square"
    assert episode1.title == "square"
    with pytest.raises(ValueError):
        episode1.title = " "
    with pytest.raises(ValueError):
        episode1.title = ""


def test_episode_eq():
    author1 = Author(1, "fish")
    podcast1 = Podcast(200, author1, "how to fish")
    formatting = "%Y-%d-%m %H:%M:%S%z"
    date1 = datetime.strptime('1996-12-09 00:00:00+0000', formatting)
    episode1 = Episode(1, podcast1, "first fish", "fish_hyperlink", 180, "fish1_description", date1)
    episode2 = Episode(2, podcast1, "second fish", "fish_hyperlink", 200, "fish2_description", date1)
    episode3 = Episode(3, podcast1, "third fish", "fish_hyperlink", 120, "fish3_description", date1)
    episode4 = Episode(1, podcast1, "first fish", "fish_hyperlink", 180, "fish1_description", date1)
    assert episode1 == episode4
    assert episode1 != episode2
    assert episode2 != episode3


def test_episode_lt():
    author1 = Author(1, "fish")
    formatting = "%Y-%d-%m %H:%M:%S%z"
    podcast1 = Podcast(200, author1, "how to fish")
    episode1 = Episode(1, podcast1, "first fish", "fish_hyperlink", 180, "fish1_description",
                       datetime.strptime('1996-12-09 00:00:00+0000', formatting))
    episode2 = Episode(2, podcast1, "second fish", "fish_hyperlink", 200, "fish2_description",
                       datetime.strptime('1996-18-11 00:00:00+0000', formatting))
    episode3 = Episode(3, podcast1, "third fish", "fish_hyperlink", 120, "fish3_description",
                       datetime.strptime('9149-01-12 00:00:00+0000', formatting))
    episode4 = Episode(4, podcast1, "fourth fish", "fish_hyperlink", 180, "fish4_description",
                       datetime.strptime('4921-11-01 00:00:00+0000', formatting))
    assert episode1 < episode2
    assert episode2 < episode3
    assert episode3 > episode4
    assert episode4 > episode1
    user_list = [episode4, episode3, episode2, episode1]
    assert sorted(user_list) == [episode1, episode2, episode4, episode3]


def test_episode_hash():
    author1 = Author(1, "fish")
    formatting = "%Y-%d-%m %H:%M:%S%z"
    fish_pub_date = datetime.strptime('2003-17-11 00:00:00+0000', formatting)
    podcast1 = Podcast(200, author1, "how to fish")
    episode1 = Episode(1, podcast1, "first fish", "fish_hyperlink", 180, "fish_description", fish_pub_date)
    episode2 = Episode(2, podcast1, "second fish", "fish_hyperlink", 200, "fish_description", fish_pub_date)
    episode_set = {episode1, episode2}
    assert len(episode_set) == 2


def test_review_initialization():
    user1 = User(4, "John Doe", "password123")
    author1 = Author(6, "Podcast Author")
    podcast1 = Podcast(9, author1, "Sample Podcast")
    review1 = Review(20, user1, podcast1, 5, "this podcast has completely changed my life!")
    assert review1.id == 20
    assert review1.user == user1
    assert review1.podcast == podcast1
    assert review1.rating == 5
    assert review1.comment == "this podcast has completely changed my life!"


def test_review_eq():
    user1 = User(2, "user1 ._.", "pw12345")
    author1 = Author(1, "author1")
    podcast1 = Podcast(100, author1, "podcast1")
    review1 = Review(1, user1, podcast1, 5, "great podcast!")
    review2 = Review(1, user1, podcast1, 5, "great podcast!")
    review3 = Review(2, user1, podcast1, 3, "could be better")
    assert review1 == review1
    assert review1 == review2
    assert review1 != review3


def test_review_lt():
    user1 = User(2, "user1 ._.", "pw12345")
    author1 = Author(1, "author1")
    podcast1 = Podcast(100, author1, "podcast1")
    review1 = Review(1, user1, podcast1, 5, "horribly amazing podcast!")
    review2 = Review(5, user1, podcast1, 1, "crazy bad podcast!")
    review3 = Review(3, user1, podcast1, 3, "meh podcast!")
    assert review1 < review2
    assert review2 > review3
    assert review3 < review2


def test_review_hash():
    user1 = User(2, "user1 ._.", "pw12345")
    author1 = Author(1, "author1")
    podcast1 = Podcast(100, author1, "podcast1")
    review1 = Review(1, user1, podcast1, 5, "W podcast!")
    review2 = Review(1, user1, podcast1, 5, "W podcast!")
    review_set = {review1, review2}
    assert len(review_set) == 1


def test_playlist_initialization():
    user1 = User(1, "user1", "pw12345")
    playlist1 = Playlist(1, user1, "playlist1")
    assert playlist1.id == 1
    assert playlist1.name == "playlist1"
    assert playlist1.owner == user1


def test_playlist_name_setter():
    user = User(1, "user1", "pw12345")
    playlist = Playlist(1, user, "My Playlist")
    playlist.name = "Updated Playlist"
    assert playlist.name == "Updated Playlist"

    with pytest.raises(ValueError):
        playlist.name = ""


def test_playlist_add():
    user1 = User(1, "user1", "pw12345")
    playlist1 = Playlist(1, user1, "playlist1")
    author1 = Author(1, "author1")
    formatting = "%Y-%d-%m %H:%M:%S%z"
    pub_date1 = datetime.strptime('2003-17-11 00:00:00+0000', formatting)
    podcast1 = Podcast(100, author1, "Podcast A", "image1", "description1", "website1", 200, "English")
    episode1 = Episode(1, podcast1, "first episode", "audio1 link", 180, "description1", pub_date1)
    episode4 = Episode(4, podcast1, "fourth episode", "audio1 link", 180, "description1", pub_date1)
    playlist1.add_episode(episode1)
    assert len(playlist1.playlist) == 1
    playlist1.add_episode(episode1)
    assert len(playlist1.playlist) == 1
    playlist1.add_episode(episode4)
    assert len(playlist1.playlist) == 2


def test_playlist_remove():
    user1 = User(1, "user1", "pw12345")
    playlist1 = Playlist(1, user1, "playlist1")
    author1 = Author(1, "author1")
    formatting = "%Y-%d-%m %H:%M:%S%z"
    pub_date1 = datetime.strptime('2003-17-11 00:00:00+0000', formatting)
    podcast1 = Podcast(100, author1, "Podcast A", "image1", "description1", "website1", 200, "English")
    episode1 = Episode(1, podcast1, "first episode", "audio1 link", 180, "description1", pub_date1)
    playlist1.add_episode(episode1)
    assert len(playlist1.playlist) == 1
    playlist1.remove_episode(episode1)
    assert len(playlist1.playlist) == 0
    playlist1.remove_episode(episode1)
    assert len(playlist1.playlist) == 0


def test_playlist_eq():
    user1 = User(1, "user1", "password1")
    user2 = User(22, "user2", "password2")
    user3 = User(333, "user3 <3", "password3")
    playlist1 = Playlist(1, user1, "food related podcasts")
    playlist2 = Playlist(2, user2, "motivational podcasts")
    playlist3 = Playlist(2, user3, "motivational podcasts")
    playlist4 = Playlist(1, user1, "food related podcasts")
    assert playlist1 != playlist2
    assert playlist2 == playlist3
    assert playlist1 == playlist4
    assert playlist1 == playlist1


def test_playlist_lt():
    user = User(1, "user1", "pw12345")
    playlist1 = Playlist(1, user, "A playlist")
    playlist2 = Playlist(2, user, "S playlist")
    playlist3 = Playlist(3, user, "C playlist")
    assert playlist1 < playlist2
    assert playlist2 > playlist3
    assert playlist3 > playlist1
    user_list = [playlist3, playlist2, playlist1]
    assert sorted(user_list) == [playlist1, playlist3, playlist2]


def test_playlist_hash():
    user = User(1, "user1", "pw12345")
    playlist1 = Playlist(1, user, "My Playlist")
    playlist2 = Playlist(2, user, "A Better Playlist")
    playlist_set = {playlist1, playlist2}
    assert len(playlist_set) == 2

def test_playlist_initialization():
    user1 = User(3, "JeNNy  ", "pw87465")
    playlist1 = Playlist(1, user1, "best playlist ever")

    with pytest.raises(ValueError):
        playlist1 = Playlist(4, user1, "")

    with pytest.raises(ValueError):
        playlist1 = Playlist("hello", user1, "best playlist ever")

    playlist2 = Playlist(1, user1, "second best playlist ever")
    assert playlist2.name == "second best playlist ever"

    user2 = User(3, "potato muncher", "potato123")
    playlist3 = Playlist(7, user2, "Cherry-Blossoms")
    assert repr(playlist3) != "<Playlist 5: Cherry-Blossoms by potato muncher>"

def test_add_episode_playlist():
    author1 = Author(1, "fish")
    podcast1 = Podcast(200, author1, "how to fish")
    formatting = "%Y-%d-%m %H:%M:%S%z"
    date1 = datetime.strptime('1996-12-09 00:00:00+0000', formatting)
    episode1 = Episode(1, podcast1, "first fish", "fish_hyperlink", 180, "fish1_description", date1)

    user1 = User(3, "JeNNy  ", "pw87465")
    playlist1 = Playlist(1, user1, "best playlist ever")
    playlist1.add_episode(episode1)
    assert len(playlist1.playlist()) == 1
    assert playlist1.playlist()[0] == episode1

def test_add_episode_playlist():
    author1 = Author(1, "fish")
    podcast1 = Podcast(200, author1, "how to fish")
    formatting = "%Y-%d-%m %H:%M:%S%z"
    date1 = datetime.strptime('1996-12-09 00:00:00+0000', formatting)
    episode1 = Episode(1, podcast1, "first fish", "fish_hyperlink", 180, "fish1_description", date1)
    episode2 = Episode(2, podcast1, "second fish", "fish_hyperlink", 200, "fish2_description", date1)
    episode3 = Episode(3, podcast1, "third fish", "fish_hyperlink", 120, "fish3_description", date1)
    episode4 = Episode(4, podcast1, "first fish", "fish_hyperlink", 180, "fish1_description", date1)

    user1 = User(3, "JeNNy  ", "pw87465")
    playlist1 = Playlist(1, user1, "best playlist ever")
    playlist1.add_episode(episode1)
    playlist1.add_episode(episode2)
    playlist1.add_episode(episode3)
    playlist1.remove_episode(episode4)
    playlist1.remove_episode(episode1)
    assert len(playlist1.playlist) == 2
    assert playlist1.playlist[0] == episode2

# def test_add_review_establishes_relationships(user, podcast):
#     # podcast_id, data, name, rating
#     review = add_review(podcast.id, "It was stinky", user.name, 1)
#     assert review in user.reviews
#     assert review.user is user
#     assert review in podcast.reviews
#     assert review.podcast is podcast

