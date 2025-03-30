from unicodedata import category

from podcast import CSVDataReader
from podcast.adapters.repository import AbstractRepository, RepositoryException
from podcast.domainmodel.model import Category, Episode, Author, Podcast, User, Review, Playlist
from bisect import insort_left


# TO DO: ADD EXTRA COOL METHODS
class MemoryRepository(AbstractRepository):

    def __init__(self):
        self.__podcasts = []
        self.__sorted_podcasts = []
        self.__episodes = []
        self.__authors = {}
        self.__categories = {}
        self.__users = []
        self.__reviews = []

    def get_playlists_by_user(self, owner: User):
        if len(owner.playlists()) == 0:
            return Playlist(owner.id, owner, owner.username + "'s Playlist")
        else:
            print(owner.playlists())
            return owner.playlists()[0]

    def add_podcast(self, podcast: Podcast):
        self.__podcasts.append(podcast)
        insort_left(self.__sorted_podcasts, podcast)

    def get_podcasts(self) -> list[Podcast]:
        return self.__podcasts

    def get_sorted_podcasts(self):
        return self.__sorted_podcasts

    # The following four methods work on the SORTED list i.e. the alphabetical order (at the time of writing)
    def get_first_podcast(self) -> Podcast:
        podcast = None
        if len(self.__sorted_podcasts) > 0:
            podcast = self.__sorted_podcasts[0]
        return podcast

    def get_last_podcast(self) -> Podcast:
        podcast = None
        if len(self.__sorted_podcasts) > 0:
            podcast = self.__sorted_podcasts[-1]
        return podcast

    def get_next_podcast(self, podcast) -> Podcast:
        next_podcast = None
        index = self.__sorted_podcasts.index(podcast)
        if index < len(self.__sorted_podcasts) - 1:
            next_podcast = self.__sorted_podcasts[index + 1]
        return next_podcast

    def get_previous_podcast(self, podcast) -> Podcast:
        previous_podcast = None
        index = self.__sorted_podcasts.index(podcast)
        if index > 0:
            previous_podcast = self.__sorted_podcasts[index - 1]
        return previous_podcast

    def get_podcast_by_id(self, podcast_id: int) -> Podcast:
        return next((podcast for podcast in self.__podcasts if podcast.id == podcast_id), None)

    def get_podcasts_by_title(self, podcast_title: str) -> list[Podcast]:
        # Case-insensitive partial matching of podcast title
        title_podcasts = [podcast for podcast in self.__podcasts if podcast_title.lower() in podcast.title.lower()]
        if title_podcasts:
            return title_podcasts
        return []

    def get_podcasts_by_category(self, podcast_cat: str) -> list[Podcast]:
        category_podcasts = []
        for podcast in self.__podcasts:
            for pod_cat in podcast.categories:
                if pod_cat.name.lower() in pod_cat.name.lower():
                    category_podcasts.append(podcast)
        if category_podcasts:
            return category_podcasts
        return []

    def get_podcasts_by_author(self, podcast_author: str) -> list[Podcast]:
        author_podcasts = [podcast for podcast in self.__podcasts if
                           podcast_author.lower() in podcast.author.name.lower()]
        if author_podcasts:
            return author_podcasts
        return []

    def add_episode(self, episode: Episode):
        super().add_episode(episode)
        self.__episodes.append(episode)

    def get_episodes(self) -> list[Episode]:
        return self.__episodes

    def get_episode_by_id(self, episode_id: int) -> Episode:
        return next((episode for episode in self.__episodes if episode.id == episode_id), None)

    def get_episodes_by_date(self, episode_date: str) -> list[Episode]:
        valid_episodes = []
        for episode in self.__episodes:
            if episode.pub_date == episode_date:
                valid_episodes.append(episode)
        return valid_episodes

    def add_author(self, author: Author):
        self.__authors[author.name] = author

    def get_authors(self) -> dict[Author]:
        return self.__authors

    def get_author_by_id(self, author_id: int) -> Author:
        valid_author = None
        for author in self.__authors.values():
            if author.id == author_id:
                valid_author = author
        return valid_author

    def get_author_by_name(self, author_name: str) -> Author:
        return self.__authors.get(author_name, None)

    def add_category(self, category: Category):
        self.__categories[category.name] = category

    def get_categories(self) -> dict[Category]:
        return self.__categories

    def get_category_by_id(self, category_id: int) -> Category:
        valid_category = None
        for category in self.__categories.values():
            if category.id == category_id:
                valid_category = category
        return valid_category

    def get_category_by_name(self, category_name: str) -> Category:
        return self.__categories.get(category_name)

    def add_user(self, user: User):
        self.__users.append(user)

    def get_users(self) -> list[User]:
        return self.__users

    def get_user_by_name(self, user_name: str):
        for _user in self.__users:
            if _user.username == user_name:
                return _user
        return None

    def get_user_by_id(self, user_id: int):
        for _user in self.__users:
            if _user.user_id == user_id:
                return _user
        return None

    def add_review(self, user: User, podcast: Podcast, rating: int, comment: str):
        review_id = len(self.__reviews) + 1
        review = Review(review_id, user, podcast, rating, comment)
        self.__reviews.append(review)
        podcast.add_review(review)
        return Review

    def get_reviews(self, podcast_id) -> list[Review]:
        return self.get_podcast_by_id(podcast_id).reviews

    def add_playlist(self, owner: User, playlist: Playlist):
        owner.playlists().append(playlist)

    def add_playlist_id(self, owner: User, playlist: Playlist):
        owner.playlists().append(playlist)

    def get_number_of_podcasts(self):
        return len(self.__podcasts)

# Automatically reads data from ...adapters/data.
def populate(repo: MemoryRepository, route='default'):
    app_data = CSVDataReader(route)
    for podcast in app_data.podcast_list:
        repo.add_podcast(podcast)
    for episode in app_data.episode_list:
        repo.add_episode(episode)
    for author in app_data.author_dict.values():
        repo.add_author(author)
    for category in app_data.cat_dict.values():
        repo.add_category(category)
