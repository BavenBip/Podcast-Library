from typing import List, Iterable
from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import Author, Podcast, Category, User, PodcastSubscription, Episode, Review, Playlist



def get_home_data(repo: AbstractRepository):
    podcasts = repo.get_podcasts()
    return podcasts


def get_podcast_by_title(repo: AbstractRepository, title):
    podcast_title = repo.get_podcast_by_title(title)
    return podcast_title


# def get_author_by_name(repo: AbstractRepository):
#     author_name = repo.get_author_by_name()
#     return get_author_by_name((author_name))



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
        'episodes': episodes_to_dict(podcast.categories)
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
        "linked_podcast": episode.linked_podcast,  #podcast id
        "title": episode.title,
        "audio": episode.audio,
        "audio_length": episode.audio_length,
        "description": episode.description,
        "pub_date": episode.pub_date
    }

    return episode_dict


def episodes_to_dict(episode: Iterable[Episode]):
    return [episode_to_dict(ep) for ep in episode]
