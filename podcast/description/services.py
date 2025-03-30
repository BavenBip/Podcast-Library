from typing import List, Iterable
from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import Author, Podcast, Category, User, Episode, Review, Playlist


class NonExistentPodcastException(Exception):
    pass


# PODCASTS #
def get_podcast_by_id(repo: AbstractRepository, podcast_id: int):  # Don't change this
    return repo.get_podcast_by_id(podcast_id)


def get_podcast_description(repo: AbstractRepository, podcast_description: str):
    podcast_from_description = repo.get_podcast_description(podcast_description)
    if podcast_from_description:
        return get_podcast_description(podcast_from_description)
    return "No description found with this podcast"


# def get_episodes_by_date(repo: AbstractRepository, episode_date: str):
#     episodes_from_date = repo.get_episodes_by_date(episode_date)
#     if episodes_from_date:
#         return episodes_from_date
#     return "No episodes found with this date"

def get_first_podcast(repo: AbstractRepository):
    podcast = repo.get_first_podcast()
    return podcast_to_dict(podcast)


def get_last_podcast(repo: AbstractRepository):
    podcast = repo.get_last_podcast()
    return podcast_to_dict(podcast)


# EPISODES #
def get_episode(episode_id: int, repo: AbstractRepository):
    episode = repo.get_podcasts(episode_id)

    if episode is None:
        raise NonExistentPodcastException

    return podcast_to_dict(episode)


def get_episode_by_id(repo: AbstractRepository, episode_id: int):
    episodes_from_id = repo.get_episode_by_id(episode_id)
    if episodes_from_id:
        return episode_to_dict(episodes_from_id)
    return "No episodes found with this id"


def get_episode_for_podcast(repo: AbstractRepository, podcast_id):
    podcast = repo.get_podcast_by_id(podcast_id)

    if podcast is None:
        raise NonExistentPodcastException

    return episodes_to_dict(podcast.episodes)


def get_first_episode(repo: AbstractRepository):
    podcast = repo.get_first_episode()

    return podcast_to_dict(podcast)


def get_last_episode(repo: AbstractRepository):
    podcast = repo.get_last_episode()
    return podcast_to_dict(podcast)


##############################
def podcast_to_dict(podcast: Podcast):
    podcast_dict = {
        'id': podcast.id,
        'author': podcast.author.name,
        'title': podcast.title,
        'image': podcast.image,
        'description': podcast.description,
        'language': podcast.language,
        'website': podcast.website,
        'category': categories_to_dict(podcast.categories),
        'itunes_id': podcast.itunes_id,
    }
    return podcast_dict


def podcasts_to_dict(podcasts: Iterable[Podcast]):
    return [podcast_to_dict(podcast) for podcast in podcasts]


def dict_to_podcast(dict):
    podcast = Podcast(dict.id, dict.author, dict.title, dict.image, dict.description, dict.language, dict.website,
                      dict.itunes_id)
    return podcast


def category_to_dict(category: Category):
    category_dict = {
        "id": category.id,
        "name": category.name
    }

    return category_dict


def categories_to_dict(category: Iterable[Category]):
    return [category_to_dict(cat) for cat in category]


def episode_to_dict(episode: Episode):
    episode_dict = {
        "id": episode.id,
        "linked_podcast": episode.linked_podcast.id,
        "title": episode.title,
        "audio": episode.audio,
        "audio_length": episode.audio_length,
        "description": episode.description,
        "pub_date": episode.pub_date
    }

    return episode_dict


def episodes_to_dict(episode: Iterable[Episode]):
    return [episode_to_dict(ep) for ep in episode]


def dict_to_episode(dict):
    episode = Episode(dict.id, dict.linked_podcast, dict.title, dict.audio, dict.audio_length, dict.description,
                      dict.pub_date)
    return episode


def add_review(podcast: Podcast, data: str, user: User, rating: int, repo: AbstractRepository):
    repo.add_review(user, podcast, rating, data)


def get_reviews(podcast_id: int, repo: AbstractRepository):
    return repo.get_reviews(podcast_id)


def get_podcast_average_rating(repo: AbstractRepository, podcast_id: int):
    total = 0
    count = 0
    reviews = repo.get_reviews(podcast_id)
    for review in reviews:
        count += 1
        total += review.rating
    if count == 0:
        count = 1
    return round(total / count, 1)


def get_user_by_name(repo: AbstractRepository, user_name: str):
    for user in repo.get_users():
        if user.username == user_name:
            return user
    return None
