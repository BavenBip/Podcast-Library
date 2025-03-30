from __future__ import annotations

import bisect
from datetime import datetime
from typing import List, Iterable

def validate_non_negative_int(value):
    if not isinstance(value, int) or value < 0:
        raise ValueError("ID must be a non-negative integer.")


def validate_non_empty_string(value, field_name="value"):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


class Author:
    def __init__(self, author_id: int, name: str):
        validate_non_negative_int(author_id)
        validate_non_empty_string(name, "Author name")
        self._id = author_id
        self._name = name.strip()
        self.podcast_list = []

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: str):
        validate_non_empty_string(new_name, "New name")
        self._name = new_name.strip()

    def add_podcast(self, podcast: Podcast):
        if not isinstance(podcast, Podcast):
            raise TypeError("Expected a Podcast instance.")
        if podcast not in self.podcast_list:
            self.podcast_list.append(podcast)

    def remove_podcast(self, podcast: Podcast):
        if podcast in self.podcast_list:
            self.podcast_list.remove(podcast)

    def __repr__(self) -> str:
        return f"<Author {self._id}: {self._name}>"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Author):
            return False
        return self._id == other._id

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Author):
            return False
        return self._name < other._name

    def __hash__(self) -> int:
        return hash(self._id)


class Podcast:
    def __init__(self, podcast_id: int, author: Author, title: str = "Untitled", image: str = None,
                 description: str = "", website: str = "", itunes_id: int = None, language: str = "Unspecified"):
        validate_non_negative_int(podcast_id)
        self._id = podcast_id
        self._author = author
        validate_non_empty_string(title, "Podcast title")
        self._title = title.strip()
        self._image = image
        self._description = description
        self._language = language
        self._website = website
        self._itunes_id = itunes_id
        self._categories = []
        self.episodes = []
        self._reviews = []

    @property
    def id(self) -> int:
        return self._id

    @property
    def author(self) -> Author:
        return self._author

    @property
    def itunes_id(self) -> int:
        return self._itunes_id

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, new_title: str):
        validate_non_empty_string(new_title, "Podcast title")
        self._title = new_title.strip()

    @property
    def image(self) -> str:
        return self._image

    @image.setter
    def image(self, new_image: str):
        if new_image is not None and not isinstance(new_image, str):
            raise TypeError("Podcast image must be a string or None.")
        self._image = new_image

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, new_description: str):
        if not isinstance(new_description, str):
            validate_non_empty_string(new_description, "Podcast description")
        self._description = new_description

    @property
    def language(self) -> str:
        return self._language

    @language.setter
    def language(self, new_language: str):
        if not isinstance(new_language, str):
            raise TypeError("Podcast language must be a string.")
        self._language = new_language

    @property
    def website(self) -> str:
        return self._website

    @website.setter
    def website(self, new_website: str):
        validate_non_empty_string(new_website, "Podcast website")
        self._website = new_website

    def add_category(self, category: Category):
        if not isinstance(category, Category):
            raise TypeError("Expected a Category instance.")
        if category not in self._categories:
            self._categories.append(category)

    def remove_category(self, category: Category):
        if category in self._categories:
            self._categories.remove(category)

    def add_episode(self, episode: Episode):
        if not isinstance(episode, Episode):
            raise TypeError("Expected an Episode instance.")
        if episode not in self.episodes:
            bisect.insort(self.episodes, episode)

    def remove_episode(self, episode: Episode):
        if episode in self.episodes:
            self.episodes.remove(episode)

    def add_review(self, review: Review):
        if not isinstance(review, Review):
            raise TypeError("Expected an Review instance.")
        bisect.insort(self._reviews, review)

    def remove_review(self, review: Review):
        if review in self._reviews:
            self._reviews.remove(review)

    def __repr__(self):
        return f"<Podcast {self.id}: '{self.title}' by {self.author.name}>"

    def __eq__(self, other):
        if not isinstance(other, Podcast):
            return False
        return self.id == other.id

    def __lt__(self, other):
        if not isinstance(other, Podcast):
            return False
        return self.title < other.title

    def __hash__(self):
        return hash(self.id)

    @property
    def categories(self):
        return self._categories

    @property
    def reviews(self):
        return self._reviews


class Category:
    def __init__(self, category_id: int, name: str):
        validate_non_negative_int(category_id)
        validate_non_empty_string(name, "Category name")
        self._id = category_id
        self._name = name.strip()

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: str):
        validate_non_empty_string(new_name, "New name")
        self._name = new_name.strip()

    def __str__(self) -> str: # Gets rid of <Category> representation in __repr__
        return self._name

    def __repr__(self) -> str:
        return f"<Category {self._id}: {self._name}>"

    def __eq__(self, other):
        if not isinstance(other, Category):
            return False
        return self.id == other.id

    def __lt__(self, other):
        if not isinstance(other, Category):
            return False
        return self._name < other.name

    def __hash__(self):
        return hash(self._id)


class User:
    def __init__(self, user_id: int, username: str, password: str):
        validate_non_negative_int(user_id)
        validate_non_empty_string(username, "Username")
        validate_non_empty_string(password, "Password")
        self._id = user_id
        self._username = username
        self._password = password
        self._subscription_list = []
        self._playlists = []

    @property
    def id(self) -> int:
        return self._id

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password

    @property
    def subscription_list(self):
        return self._subscription_list

    def add_subscription(self, subscription: PodcastSubscription):
        if not isinstance(subscription, PodcastSubscription):
            raise TypeError("Subscription must be a PodcastSubscription object.")
        if subscription not in self._subscription_list:
            self._subscription_list.append(subscription)

    def remove_subscription(self, subscription: PodcastSubscription):
        if subscription in self._subscription_list:
            self._subscription_list.remove(subscription)

    def playlists(self):
        return self._playlists

    def add_playlist(self, playlist: Playlist):
        if not isinstance(playlist, Playlist):
            raise TypeError("Playlist must be a Playlist object.")
        if playlist not in self._playlists:
            self._playlists.append(playlist)

    def __repr__(self):
        return f"<User {self.id}: {self.username}>"

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return self.id == other.id

    def __lt__(self, other):
        if not isinstance(other, User):
            return False
        return self.username.lower().strip() < other.username.lower().strip()

    def __hash__(self):
        return hash(self.id)


class PodcastSubscription:
    def __init__(self, sub_id: int, owner: User, podcast: Podcast):
        validate_non_negative_int(sub_id)
        if not isinstance(owner, User):
            raise TypeError("Owner must be a User object.")
        if not isinstance(podcast, Podcast):
            raise TypeError("Podcast must be a Podcast object.")
        self._id = sub_id
        self._owner = owner
        self._podcast = podcast

    @property
    def id(self) -> int:
        return self._id

    @property
    def owner(self) -> User:
        return self._owner

    @owner.setter
    def owner(self, new_owner: User):
        if not isinstance(new_owner, User):
            raise TypeError("Owner must be a User object.")
        self._owner = new_owner

    @property
    def podcast(self) -> Podcast:
        return self._podcast

    @podcast.setter
    def podcast(self, new_podcast: Podcast):
        if not isinstance(new_podcast, Podcast):
            raise TypeError("Podcast must be a Podcast object.")
        self._podcast = new_podcast

    def __repr__(self):
        return f"<PodcastSubscription {self.id}: Owned by {self.owner.username}>"

    def __eq__(self, other):
        if not isinstance(other, PodcastSubscription):
            return False
        return self.id == other.id and self.owner == other.owner and self.podcast == other.podcast

    def __lt__(self, other):
        if not isinstance(other, PodcastSubscription):
            return False
        return self.podcast < other.podcast

    def __hash__(self):
        return hash((self.id, self.owner, self.podcast))


class Episode:
    # TODO: Complete the implementation of the Episode class.
    def __init__(self, episode_id: int, linked_podcast: Podcast, title: str, audio: str, audio_length: int, description: str, pub_date: datetime):
        validate_non_negative_int(episode_id)
        validate_non_negative_int(audio_length)
        validate_non_empty_string(title, "Episode title")
        validate_non_empty_string(audio, "Episode audio")
        self._id = episode_id
        self._linked_podcast = linked_podcast
        self._title = title.strip()
        self._audio = audio                  # Audio link
        self._audio_length = audio_length
        self._description = description
        self._pub_date = pub_date

    @property
    def id(self) -> int:
        return self._id

    @property
    def linked_podcast(self) -> Podcast:
        return self._linked_podcast

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, new_title: str):
        validate_non_empty_string(new_title, "Episode title")
        self._title = new_title.strip()

    @property
    def audio(self) -> str:
        return self._audio

    @audio.setter
    def audio(self, new_audio: str):
        validate_non_empty_string(new_audio, "Episode audio")
        self._audio = new_audio

    @property
    def audio_length(self) -> int:
        return self._audio_length

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, new_description: str):
        if not isinstance(new_description, str):
            validate_non_empty_string(new_description, "Episode description")
        self._description = new_description

    @property
    def pub_date(self) -> datetime:
        return self._pub_date

    def __repr__(self) -> str:
        return f"<Episode {self.id}: {self.title} {self.pub_date}>"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Episode):
            return False
        return self.id == other.id

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Episode):
            return False
        return self.pub_date < other.pub_date

    def __hash__(self) -> int:
        return hash(self.id)


class Review: # Reviewing a podcast instead of an episode
    def __init__(self, review_id: int, user: User, podcast: Podcast, rating: int, comment: str):
        validate_non_negative_int(rating)
        self._id = review_id
        self._user = user
        self._podcast = podcast
        self._rating = rating
        self._comment = comment

    @property
    def id(self) -> int:
        return self._id
    @property
    def user(self) -> User:
        return self._user

    @property
    def podcast(self) -> Podcast:
        return self._podcast

    @property
    def rating(self) -> int:
        return self._rating

    @rating.setter
    def rating(self, new_rating):
        self._rating = new_rating

    @property
    def comment(self) -> str:
        return self._comment

    @comment.setter
    def comment(self, new_comment: str):
        self._comment = new_comment

    def __repr__(self):
        return f"<Review {self.id}: {self.podcast} reviewed by {self.user}>"

    def __eq__(self, other):
        if not isinstance(other, Review):
            return False
        return self.id == other.id

    def __lt__(self, other):
        if not isinstance(other, Review):
            return False
        return self.id < other.id # Not sure

    def __hash__(self):
        return hash(self.id)


class Playlist:
    # TODO: Complete the implementation of the Playlist class.
    def __init__(self, playlist_id: int, owner: User, name: str):
        validate_non_negative_int(playlist_id)
        validate_non_empty_string(name, "Playlist name")
        self._id = playlist_id
        self._owner = owner # Owner of playlist
        self._name = name
        self._playlist = []

    @property
    def id(self) -> int:
        return self._id

    @property
    def owner(self) -> User:
        return self._owner

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: str):
        validate_non_empty_string(new_name, "New name")
        self._name = new_name

    @property
    def playlist(self):
        return self._playlist

    def add_episode(self, episode: Episode):
        if not isinstance(episode, Episode):
            raise TypeError("Episode must be an Episode object.")
        if episode not in self._playlist:
            self._playlist.append(episode)

    def add_podcast(self, podcast: Podcast):
        if not isinstance(podcast, Podcast):
            raise TypeError("Podcast must be a Podcast object.")
        for episode in podcast.episodes:
            self.add_episode(episode)

    def remove_episode(self, episode: Episode):
        if episode in self._playlist:
            self._playlist.remove(episode)
        
    def remove_podcast(self, podcast: Podcast):
        for episode in podcast.episodes:
            self.remove_episode(episode)

    def __repr__(self):
        return f"<Playlist {self.id}: {self.name} by {self.owner}>"

    def __eq__(self, other):
        if not isinstance(other, Playlist):
            return False
        return self.id == other.id and self.name.lower().strip() == other.name.lower().strip()

    def __lt__(self, other):
        if not isinstance(other, Playlist):
            return False
        return self.name.lower().strip() < other.name.lower().strip()

    def __hash__(self):
        return hash((self.id, self.owner, self.name))
