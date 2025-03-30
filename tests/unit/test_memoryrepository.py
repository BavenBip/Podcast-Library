from datetime import datetime

import pytest

from podcast.adapters.repository import RepositoryException
from podcast.domainmodel.model import Author, Podcast, Category, User, PodcastSubscription, Episode, Review, Playlist


def test_repository_add_podcast(test_mem_repo):
    podcast1 = Podcast(60, Author(10, 'Maple'), 'The Lost Pancake')
    test_mem_repo.add_podcast(podcast1)

    assert test_mem_repo.get_podcast_by_id(60) is podcast1


def test_repository_get_podcasts(test_mem_repo):
    podcasts = test_mem_repo.get_podcasts()

    assert podcasts[0].title == 'My Favourite Animals'
    assert podcasts[1].description == 'Tiramisu is pretty cool'
    assert podcasts[2].language == 'English'


def test_repository_get_sorted_podcasts(test_mem_repo):
    podcasts = test_mem_repo.get_sorted_podcasts()

    # Test requires checking for an alphabetical sort
    assert podcasts[0].title == 'My Favourite Animals'
    assert podcasts[1].title == 'My Favourite Chairs'
    assert podcasts[2].title == 'My Favourite Dessert'
    assert podcasts[3].title == 'My Favourite Ice Cream'


def test_repository_get_first_podcast(test_mem_repo):
    podcast1 = test_mem_repo.get_first_podcast()

    assert podcast1.title == 'My Favourite Animals'
    assert podcast1.id == 1
    assert podcast1.description == 'Bees are pretty cool'


def test_repository_get_last_podcast(test_mem_repo):
    podcast1 = test_mem_repo.get_last_podcast()

    assert podcast1.title == 'My Favourite Ice Cream'
    assert podcast1.id == 3
    assert podcast1.description == 'Pistachio is pretty cool'


def test_repository_get_next_podcast(test_mem_repo):
    podcast1 = test_mem_repo.get_podcasts()[0]
    podcast2 = test_mem_repo.get_next_podcast(podcast1)

    assert podcast2.title == 'My Favourite Chairs'
    assert podcast2.id == 4
    assert podcast2.description == 'Chairs are NOT pretty cool'


def test_repository_get_next_podcast_out_of_range(test_mem_repo):
    podcast1 = test_mem_repo.get_podcasts()[2]
    podcast2 = test_mem_repo.get_next_podcast(podcast1)

    assert podcast2 is None


def test_repository_get_previous_podcast(test_mem_repo):
    podcast1 = test_mem_repo.get_podcasts()[3]
    podcast2 = test_mem_repo.get_previous_podcast(podcast1)

    assert podcast2.title == 'My Favourite Animals'
    assert podcast2.id == 1
    assert podcast2.description == 'Bees are pretty cool'


def test_repository_get_previous_podcast_out_of_range(test_mem_repo):
    podcast1 = test_mem_repo.get_podcasts()[0]
    podcast2 = test_mem_repo.get_previous_podcast(podcast1)

    assert podcast2 is None


def test_repository_get_podcast_by_id(test_mem_repo):
    podcast1 = test_mem_repo.get_podcast_by_id(1)

    author1 = Author(1, 'Hamish Prasad')
    assert podcast1 == Podcast(1, author1, 'My Favourite Animals', 'no_image', 'Bees are pretty cool', 'no_website',
                               101, 'English')


def test_repository_get_podcasts_by_title(test_mem_repo):
    podcast1 = test_mem_repo.get_podcasts_by_title('My Favourite Dessert')

    author1 = Author(2, 'AM Zapata')
    assert podcast1 != Podcast(2, author1, 'My Favourite Dessert', 'no_image', 'Tiramisu is pretty cool', 'no_website',
                               102, 'English')


def test_repository_get_podcast_by_category(test_mem_repo):
    category1 = Category(2, 'Food')
    podcasts = test_mem_repo.get_podcasts_by_category(category1)

    assert podcasts[0].title == 'My Favourite Animals'
    assert podcasts[1].title == 'My Favourite Dessert'


def test_repository_getting_podcast_with_invalid_requests_returns_none_or_empty(test_mem_repo):
    podcast1 = test_mem_repo.get_podcast_by_id(100)
    podcast2 = test_mem_repo.get_podcasts_by_title('My Favourite Pizza')
    category1 = Category(200, 'Cats')
    podcast3 = test_mem_repo.get_podcasts_by_category(category1)

    assert podcast1 is None
    assert podcast2 is not None
    assert podcast3 is not None


def test_repository_add_episode(test_mem_repo):
    formatting = "%Y-%d-%m %H:%M:%S%z"
    date1 = datetime.strptime('2003-17-12 00:00:00+0000', formatting)
    episode1 = Episode(7, test_mem_repo.get_podcast_by_id(3), 'Kinder Surprise', 'sorry_no_link', 69,
                       'Chocolate tastes good', date1)
    test_mem_repo.get_podcast_by_id(3).add_episode(episode1)
    test_mem_repo.add_episode(episode1)

    assert test_mem_repo.get_episode_by_id(7) is episode1


def test_repository_add_episode_not_connected_to_podcast_properly(test_mem_repo):
    formatting = "%Y-%d-%m %H:%M:%S%z"
    date1 = datetime.strptime('2003-17-12 00:00:00+0000', formatting)
    episode1 = Episode(7, None, 'Kinder Surprise', 'sorry_no_link', 69,
                       'Chocolate tastes good', date1)

    with pytest.raises(RepositoryException):
        test_mem_repo.add_episode(episode1)


def test__repository_get_episodes(test_mem_repo):
    episodes = test_mem_repo.get_episodes()

    assert episodes[3].title == 'Mmmm Tiramisu'
    assert episodes[4].description == 'Mmmm Ice Cream'
    assert episodes[5].audio == 'sorry_no_link'


def test_repository_get_episode_by_id(test_mem_repo):
    episode1 = test_mem_repo.get_episode_by_id(1)

    assert episode1.title == 'The Buzzy Bee Battle'
    assert episode1.description == 'Buzz Buzz'
    assert episode1.id == 1
    assert episode1.audio_length == 812


def test_repository_get_episodes_by_date(test_mem_repo):
    formatting = "%Y-%d-%m %H:%M:%S%z"
    episodes = test_mem_repo.get_episodes_by_date(datetime.strptime('2003-17-12 00:00:00+0000', formatting))

    assert episodes[0].title == 'The Bees won'
    assert episodes[0].id == 2
    assert episodes[1].title == 'The Tiramisu Terror'
    assert episodes[1].id == 3


def test_repository_getting_episode_with_invalid_requests_returns_none_or_empty(test_mem_repo):
    formatting = "%Y-%d-%m %H:%M:%S%z"
    episode1 = test_mem_repo.get_episode_by_id(101)
    episode2 = test_mem_repo.get_episodes_by_date(datetime.strptime('3000-17-12 00:00:00+0000', formatting))

    assert episode1 is None
    assert episode2 == []


def test_repository_add_author(test_mem_repo):
    author1 = Author(10, 'Maple')
    test_mem_repo.add_author(author1)

    assert test_mem_repo.get_author_by_id(10) is author1


def test_repository_get_authors(test_mem_repo):
    authors = test_mem_repo.get_authors()

    assert isinstance(authors['Hamish Prasad'], Author)
    assert authors['AM Zapata'].id == 2
    assert len(authors['Becky Cheng'].podcast_list) == 1


def test_repository_get_author_by_id(test_mem_repo):
    author1 = test_mem_repo.get_author_by_id(1)

    assert author1.name == 'Hamish Prasad'
    assert author1.id == 1
    assert len(author1.podcast_list) == 2


def test_repository_get_author_by_name(test_mem_repo):
    author1 = test_mem_repo.get_author_by_name('Becky Cheng')

    assert author1.name == 'Becky Cheng'
    assert author1.id == 3
    assert len(author1.podcast_list) == 1


def test_repository_getting_author_with_invalid_requests_returns_none_or_empty(test_mem_repo):
    author1 = test_mem_repo.get_author_by_id(102)
    author2 = test_mem_repo.get_author_by_name('Fred McGee')

    assert author1 is None
    assert author2 is None


def test_repository_add_category(test_mem_repo):
    category1 = Category(11, 'Cheesy')
    test_mem_repo.add_category(category1)

    assert test_mem_repo.get_category_by_id(11) is category1


def test_repository_get_categories(test_mem_repo):
    categories = test_mem_repo.get_categories()

    assert categories['Religion & Spirituality'].id == 1
    assert categories['Religion & Spirituality'].name == 'Religion & Spirituality'
    assert categories['Food'].id == 2
    assert categories['Food'].name == 'Food'
    assert categories['Chairs'].id == 3
    assert categories['Chairs'].name == 'Chairs'


def test_repository_get_categories_by_id(test_mem_repo):
    category1 = test_mem_repo.get_category_by_id(2)

    assert category1.id == 2
    assert category1.name == 'Food'


def test_repository_get_categories_by_name(test_mem_repo):
    category1 = test_mem_repo.get_category_by_name('Chairs')

    assert category1.id == 3
    assert category1.name == 'Chairs'


def test_repository_getting_categories_with_invalid_requests_returns_none_or_empty(test_mem_repo):
    category1 = test_mem_repo.get_category_by_id(103)
    category2 = test_mem_repo.get_category_by_name('Pizzas')

    assert category1 is None
    assert category2 is None
