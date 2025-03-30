import abc

from podcast.domainmodel.model import Podcast, Category, Episode, Author, User, Review, Playlist

repo_instance = None


class RepositoryException(Exception):
    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add_podcast(self, podcast: Podcast):
        """adds a podcast to the repository"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_podcasts(self) -> list[Podcast]:
        """retrieves all podcasts from repository

        returns empty list if no podcasts are found
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_sorted_podcasts(self) -> list[Podcast]:
        """retrieves all podcasts from repository in alphabetical order of podcast title

        returns empty list if no podcasts are found
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_first_podcast(self) -> Podcast:
        """retrieves the first podcast (where podcast_id = 1) from repository

        returns None if no such podcast is found
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_last_podcast(self) -> Podcast:
        """retrieves the last podcast (where podcast_id = len(get_podcasts)-1) from repository

        returns None if no such podcast is found
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_next_podcast(self, podcast: Podcast) -> Podcast:
        """retrieves the next podcast (where podcast_id = 1+current_podcast_id) from repository

        returns None if no such podcast is found
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_previous_podcast(self, podcast: Podcast) -> Podcast:
        """retrieves the previous podcast (where podcast_id = current_podcast_id-1) from repository

        returns None if no such podcast is found
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_podcast_by_id(self, podcast_id: int) -> Podcast:
        """retrieves the podcast that has the specified id from repository

        returns None if no such podcast is found
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_podcasts_by_title(self, podcast_title: str) -> list[Podcast]:
        """retrieves podcasts from repository with titles that contain a substring of the given input string

        returns empty list if no such podcast is found
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_podcasts_by_category(self, podcast_cat: str) -> list[Podcast]:
        """retrieves podcasts from repository with categories that contain a substring of the given input string

        returns empty list if no such podcast is found
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_podcasts_by_author(self, podcast_author: str) -> list[Podcast]:
        """retrieves podcasts from repository with author names that contain a substring of the given input string

        returns empty list if no such podcast is found
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_episode(self, episode: Episode):
        """adds an episode to the repository"""
        if episode.linked_podcast is None or episode not in episode.linked_podcast.episodes:
            raise RepositoryException('Episode did not get added to linked podcast')

    @abc.abstractmethod
    def get_episodes(self) -> list[Episode]:
        """retrieves all episodes from the repository"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_episode_by_id(self, episode_id: int) -> Episode:
        """retrieves an episode from a podcast that matches the given id

        returns None if no such episode is found"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_episodes_by_date(self, episode_date: str) -> list[Episode]:
        """retrieves an episode from a podcast that matches the given date

        returns empty list if no episodes are found"""
        raise NotImplementedError

    @abc.abstractmethod
    def add_author(self, author: Author):
        """adds an author to the repository"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_authors(self) -> dict[Author]:
        """retrieves a list of all authors from repository"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_author_by_id(self, author_id: int) -> Author:
        """retrieves an author that matches the given id

        returns None if no such author is found"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_author_by_name(self, author_name: str) -> Author:
        """retrieves an author that matches the given name

        returns None if no such author is found"""
        raise NotImplementedError

    @abc.abstractmethod
    def add_category(self, category: Category):
        """adds a category to the repository"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_categories(self) -> dict[Category]:
        """retrieves a list of all categories from the repository

        returns empty list if no categories are found
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_category_by_id(self, category_id: int) -> Category:
        """retrieves a category that matches the given id

        returns None if no such category is found
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_category_by_name(self, category_name: str) -> Category:
        """retrieves a category that matches the given name

        returns None if no such category is found
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_user(self, category: User):
        """adds a user to the repository"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_users(self) -> list[User]:
        """retrieves a list of all users from the repository

        returns empty list if none are found
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user_by_name(self, user_name: str) -> User:
        """retrieves a user that matches the given name

        returns None if no such user is found
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user_by_id(self, user_id: int) -> User:
        """retrieves a user that matches the given id

        returns None if no such user is found
        """
        raise NotImplementedError

    def add_review(self, user: User, podcast: Podcast, rating: int, comment: str):
        """adds a review which is linked to a podcast, to the repository"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_reviews(self, podcast_id) -> list[Review]:
        """returns a list of all reviews from repository

        returns an empty list if none are found
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_playlist(self, owner: User, name: str):
        """adds a playlist to the repository using a given name"""
        raise NotImplementedError

    def add_playlist_id(self, owner: User, playlist: Playlist):
        """adds a playlist to the repository using a given id"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_playlists_by_user(self, owner: User):
        """retrieves all playlists linked (owned) by a given user

        returns empty list if none are found
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_podcasts(self):
        """calculates and returns the number of total podcasts from the repository"""
        raise NotImplementedError