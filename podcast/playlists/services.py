from typing import List, Iterable
from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import Author, Podcast, Category, User, PodcastSubscription, Episode, Review, Playlist


def get_podcast_data(repo: AbstractRepository):  # Dont' change this
    podcasts = repo.get_podcasts()
    return podcasts


def get_podcast_by_id(podcast_id: int, repo: AbstractRepository):
    return repo.get_podcast_by_id(podcast_id)


def get_playlists_by_name(username: str, repo: AbstractRepository):
    user = repo.get_user_by_name(username)
    playlists_by_user = repo.get_playlists_by_user(user)
    return playlists_by_user


def get_playlists_by_id(user_id: int, repo: AbstractRepository):
    user = repo.get_user_by_id(user_id)
    playlists_by_user = repo.get_playlists_by_user(user)
    return playlists_by_user


def get_user_from_name(username: str, repo: AbstractRepository):
    user = repo.get_user_by_name(username)
    return user


def get_user_from_id(user_id: int, repo: AbstractRepository):
    user = repo.get_user_by_id(user_id)
    return user


def get_episode_by_id(id: int, repo: AbstractRepository):
    return repo.get_episode_by_id(id)


#####################
def get_users(repo: AbstractRepository):
    users = repo.get_users()
    return users


def get_playlists_by_user(owner: User, repo: AbstractRepository):
    playlists_by_user = repo.get_playlists_by_user(owner)
    return playlists_by_user


def add_playlist(owner: User, playlist: Playlist, repo: AbstractRepository):
    print("Playlist service add_playlist_id")
    repo.add_playlist_id(owner, playlist)


def get_episodes_from_playlist(podcast: Podcast, playlist: Playlist, repo: AbstractRepository):
    episodes = []
    for pod_episode in podcast.episodes:
        for play_episode in playlist.playlist:
            if pod_episode.id == play_episode.id:
                episodes.append(pod_episode)
    return episodes

# def add_playlist(owner: User, username: str, repo: AbstractRepository):
#     repo.add_playlist_id(owner, username)
#########################
