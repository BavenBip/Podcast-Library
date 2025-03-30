from abc import ABC
import os
from typing import List, Optional
import sqlalchemy
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import scoped_session, joinedload, sessionmaker
from sqlalchemy.orm.exc import NoResultFound, DetachedInstanceError
from sqlalchemy import desc, asc
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from podcast.adapters.repository import AbstractRepository
from sqlalchemy.orm import scoped_session
from podcast.domainmodel.model import Podcast, Author, Category, User, Review, Episode, Playlist
from podcast import CSVDataReader
from bisect import insort_left


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            self.rollback()
        self.close_current_session()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory)

    def close_current_session(self):
        if self.__session:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository, ABC):
    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.close_current_session()
        self._session_cm = SessionContextManager(self._session_cm.__session_factory)

    ################
    def get_playlists_by_user(self, owner: User): # Asma told me to remove the -> List[Playlist]
        # Task 5
        playlist = None
        try:
            playlist = self._session_cm.session.query(Playlist).join(User).filter(User._id == owner._id).one()

        except NoResultFound:
            print("Playlist no result found")
        print(playlist)
        return playlist


    def get_podcasts(self) -> List[Podcast]:
        return self._session_cm.session.query(Podcast).all()

    def get_sorted_podcasts(self) -> List[Podcast]:
        with self._session_cm as scm:
            return scm.session.query(Podcast).order_by(Podcast.title).all()

    def get_first_podcast(self):
        # I'm not really sure if this is used anywhere

        # Task 6 aka testing, i dont think this is used anywhere.
        with self._session_cm as scm:
            return scm.session.query(Podcast).order_by(Podcast._id).first()

    def get_last_podcast(self) -> Optional[Podcast]:
        # I'm not really sure if this is used anywhere

        # Task 6 aka testing, i dont think this is used anywhere.
        return self._session_cm.session.query(Podcast).order_by(desc(Podcast._id)).first()

    def add_podcast(self, podcast: Podcast):
        with self._session_cm as scm:
            try:
                podcast = scm.session.merge(podcast)
                scm.commit()
                scm.session.refresh(podcast)
                scm.session.flush()
            except IntegrityError:
                scm.rollback()
                print(f"Error occurred while adding podcast '{podcast.title}'.")

    def get_next_podcast(self, podcast: Podcast) -> Optional[Podcast]:
        try:
            with self._session_cm as scm:
                return (
                    scm.session.query(Podcast)
                    .filter(Podcast._id > podcast.id)
                    .order_by(Podcast._id.asc())
                    .first()
                )
        except NoResultFound:
            #ignores and passes
            pass
        return None

    def get_previous_podcast(self, podcast: Podcast) -> Optional[Podcast]:
        try:
            with self._session_cm as scm:
                return (
                    scm.session.query(Podcast)
                    .filter(Podcast._id < podcast.id)
                    .order_by(Podcast._id.desc())
                    .first()
                )
        except NoResultFound:
            #ignores and passes
            pass
        return None

    def get_podcast_by_id(self, podcast_id: int) -> Podcast:
        podcast = None
        try:
            with self._session_cm as scm:
                podcast = (
                    scm.session.query(Podcast)
                    .options(
                        joinedload(Podcast.episodes),
                        joinedload(Podcast._author),
                        joinedload(Podcast._categories),
                    )  # Eager loading, to be used later
                    .filter(Podcast._id == podcast_id)
                    .one()
                )
        except NoResultFound:
            print("Podcast no result found")

        return podcast


    def get_podcasts_by_title(self, title_string: str) -> List[Podcast]:
        # Retrieve podcasts whose title contains the title_string passed by the user.
        title_string = title_string.lower()
        podcasts = self._session_cm.session.query(Podcast).all()
        filtered = []
        for podcast in podcasts:
            if title_string in podcast.title.lower():
                filtered.append(podcast)
        return filtered


    def get_podcasts_by_author(self, author_name: str) -> List[Podcast]:
        # Retrieve podcasts whose author contains the author_name passed by the user.
        author_name = author_name.lower()
        podcasts = self._session_cm.session.query(Podcast).all()
        filtered = []
        for podcast in podcasts:
            if author_name in podcast.author.name.lower():
                filtered.append(podcast)
        return filtered


    def get_podcasts_by_category(self, category_string: str) -> List[Podcast]:
        # Retrieve podcasts whose category contains the category_string passed by the user.
        category_string = category_string.lower()
        podcasts = self._session_cm.session.query(Podcast).all()
        filtered = []
        for podcast in podcasts:
            for categories in podcast.categories:
                if category_string in categories.name.lower():
                    filtered.append(podcast)
        return filtered


    def get_number_of_podcasts(self):
        with self._session_cm as scm:
            return len(self._session_cm.session.query(Podcast).all())

    def get_episodes(self) -> List[Episode]:
        with self._session_cm as scm:
            return scm.session.query(Episode).all()

    def get_episode_by_id(self, episode_id: int) -> Optional[Episode]:
        with self._session_cm as scm:
            episode = (
                scm.session.query(Episode)
                .options(
                    joinedload(Episode._linked_podcast),
                )  # Eager loading, to be used later
                .filter(Episode._id == episode_id)
                .one()
            )
            return episode

    def add_episode(self, episode: Episode):
        with self._session_cm as scm:
            try:
                episode = scm.session.merge(episode)
                scm.commit()
                scm.session.refresh(episode)
            except IntegrityError:
                scm.rollback()
                print(f"Error occurred while adding episode '{episode.title}'.")

    def get_episode_by_id(self, episode_id: int) -> Optional[Episode]:
        # This is the same as the function two above except this one won't work bc it doesnt have joinedload
        # We should delete this I think
        episode = None
        try:
            episode = self._session_cm.session.query(Episode).filter(Episode._id == episode_id).first()

        except NoResultFound:
            print("Episode no result found")
        return episode

    def get_episodes_by_date(self, episode_date: str) -> List[Episode]:
        # Task 6 aka testing, i dont think this is used anywhere.
        return self._session_cm.session.query(Episode).filter(Episode._pub_date == episode_date).all()

    def get_authors(self) -> List[Author]:
        with self._session_cm as scm:
            return scm.session.query(Author).all()

    def add_author(self, author: Author):
        with self._session_cm as scm:
            try:
                author = scm.session.merge(author)
                scm.commit()
                scm.session.refresh(author)
            except IntegrityError:
                scm.rollback()
                print(f"Error occurred while adding author '{author.name}'.")

    def get_author_by_id(self, author_id: int) -> Optional[Author]:
        author = None
        try:
            return self._session_cm.session.query(Author).filter(Author._id == author_id).first()
        except NoResultFound:
            # ignores and returns None
            pass

        return author

    def get_author_by_name(self, author_name: str) -> Optional[Author]:
        author = None
        try:
            return self._session_cm.session.query(Author).filter(Author._name == author_name).first()
        except NoResultFound:
            # ignores and returns None
            pass

    def get_categories(self) -> List[Category]:
        with self._session_cm as scm:
            return scm.session.query(Category).all()

    def add_category(self, category: Category):
        with self._session_cm as scm:
            try:
                category = scm.session.merge(category)
                scm.commit()
                scm.session.refresh(category)
            except IntegrityError:
                scm.rollback()
                print(f"Error occurred while adding category '{category.name}'.")

    def get_category_by_id(self, category_id: int) -> Optional[Category]:
        category = None
        try:
            return self._session_cm.session.query(Category).filter(Category._id == category_id).one_or_none()
        except NoResultFound:
            # ignores and returns None
            pass

        return category

    def get_category_by_name(self, category_name: str) -> Optional[Category]:
        categories = []
        try:
            return self._session_cm.session.query(Category).filter(Category._name == category_name).first()

        except NoResultFound:
            # ignores and returns None
            pass

        return categories

    # User
    def add_user(self, user: User):
        with self._session_cm as scm:
            try:
                user = scm.session.merge(user)
                scm.commit()
                scm.session.refresh(user)
            except IntegrityError:
                scm.rollback()
                print(f"Error occurred while adding user '{user.username}'.")

    def get_users(self) -> List[User]:
        with self._session_cm as scm:
            return scm.session.query(User).all()

    def get_user_by_name(self, username: str) -> Optional[User]:
        user = None

        with self._session_cm as scm:
            user = (
                scm.session.query(User)
                .filter(User._username == username)
                .one_or_none()
            )
            if user is None:
                pass
            return user

    def get_user_by_id(self, user_id: int) -> User:
        with self._session_cm as scm:
            user = (scm.session.query(User.filter(User._id == user_id).one()))
            return user

    def get_reviews(self, podcast_id: int) -> List[Review]:
        # I am clueless as to why it's not Review._podcast_id but I think it's fine???
        with self._session_cm as scm:
            reviews = (
                scm.session.query(Review)
                .filter(Review.podcast_id == podcast_id)
                .all()
            )
            print("reviews = " + str(reviews))
            return reviews

    def add_review(self, user: User, podcast: Podcast, rating: int, comment: str):
        with self._session_cm as scm:
            podcast = scm.session.merge(podcast)
            user = scm.session.merge(user)
            # review = Review(None, podcast=podcast, comment=comment, user=user, rating=rating)
            review = Review(None, user, podcast, rating, comment)
            scm.session.add(review)
            scm.session.flush()
            podcast.add_review(review)
            scm.commit()
            scm.session.refresh(review)
        return review

    ################
    def add_playlist_id(self, owner: User, playlist: Playlist):
        with self._session_cm as scm:
            # playlist = Playlist(None, owner=owner, name="My playlist")
            print("Add playlist to database")
            scm.session.merge(playlist)
            scm.session.commit()

    def add_playlist(self, owner: User, name: str): # We can just have this as pass
        pass
