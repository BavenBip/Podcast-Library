from sqlalchemy import (
    Table, Column, Integer, Float, String, DateTime, ForeignKey, Text, MetaData
)
from sqlalchemy.orm import registry, mapper, relationship
from sqlalchemy.orm import class_mapper, exc as orm_exc
from datetime import datetime

from podcast.domainmodel.model import User, Review, Podcast, PodcastSubscription, Playlist, Author, Episode, Category

# Global variable giving access to the MetaData (schema) information of the database
metadata = MetaData()
mapper_registry = registry()

authors_table = Table(
    'authors', metadata,
    Column('author_id', Integer, primary_key=True),
    Column('name', String(255), nullable=False)
)

podcast_table = Table(
    'podcasts', metadata,
    Column('podcast_id', Integer, primary_key=True),
    Column('title', Text, nullable=True),
    Column('image_url', Text, nullable=True),
    Column('description', String(255), nullable=True),
    Column('language', String(255), nullable=True),
    Column('website_url', String(255), nullable=True),
    Column('author_id', ForeignKey('authors.author_id')),
    Column('itunes_id', Integer, nullable=True)
)

episode_table = Table(
    'episodes', metadata,
    Column('episode_id', Integer, primary_key=True),
    Column('podcast_id', ForeignKey('podcasts.podcast_id')),
    Column('title', Text, nullable=True),
    Column('audio_url', Text, nullable=True),
    Column('description', String(255), nullable=True),
    Column('pub_date', DateTime, nullable=True)
)

categories_table = Table(
    'categories', metadata,
    Column('category_id', Integer, primary_key=True, autoincrement=True),
    Column('category_name', String(64), nullable=False)
)

podcast_categories_table = Table(
    'podcast_categories', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('podcast_id', ForeignKey('podcasts.podcast_id')),
    Column('category_id', ForeignKey('categories.category_id'))
)

users_table = Table(
    'users', metadata,
    Column('user_id', Integer, primary_key=True, autoincrement=True),
    Column('user_name', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False)
)

reviews_table = Table(
    'reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.user_id')),
    Column('podcast_id', ForeignKey('podcasts.podcast_id')),
    Column('rating', Integer, nullable=False),
    Column('comment', String(1024), nullable=False),
)

playlists_table = Table(
    'playlists', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.user_id')),
    Column('name', String(255), nullable=False)
)


playlist_episodes_table = Table(
    'playlist_episodes', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('playlist_id', ForeignKey('playlists.id')),
    Column('episode_id', ForeignKey('episodes.episode_id')),
)


def is_mapped(class_type):
    try:
        class_mapper(class_type)
        return True
    except orm_exc.UnmappedClassError:
        return False


def map_model_to_tables():
    # Author
    if not is_mapped(Author):
        mapper_registry.map_imperatively(Author, authors_table, properties={
            '_id': authors_table.c.author_id,
            '_name': authors_table.c.name,
            '_podcast_list': relationship(Podcast, back_populates='_author')  # Back reference
        })

    # Category
    if not is_mapped(Category):
        mapper_registry.map_imperatively(Category, categories_table, properties={
            '_id': categories_table.c.category_id,
            '_name': categories_table.c.category_name,
        })

    # Podcast
    if not is_mapped(Podcast):
        mapper_registry.map_imperatively(Podcast, podcast_table, properties={
            '_id': podcast_table.c.podcast_id,
            '_title': podcast_table.c.title,
            '_image': podcast_table.c.image_url,
            '_description': podcast_table.c.description,
            '_language': podcast_table.c.language,
            '_website': podcast_table.c.website_url,
            '_itunes_id': podcast_table.c.itunes_id,
            '_author': relationship(Author, back_populates='_podcast_list'),
            'episodes': relationship(Episode, back_populates='_linked_podcast'),
            '_categories': relationship(Category, secondary=podcast_categories_table, backref='podcasts'),
            '_reviews': relationship(Review, back_populates='_podcast'),
        })

    # Episode
    if not is_mapped(Episode):
        mapper_registry.map_imperatively(Episode, episode_table, properties={
            '_id': episode_table.c.episode_id,
            '_linked_podcast': relationship(Podcast, back_populates='episodes'),
            '_title': episode_table.c.title,
            '_audio': episode_table.c.audio_url,
            '_description': episode_table.c.description,
            '_pub_date': episode_table.c.pub_date,
        })

    # User
    if not is_mapped(User):
        mapper_registry.map_imperatively(User, users_table, properties={
            '_id': users_table.c.user_id,
            '_username': users_table.c.user_name,
            '_password': users_table.c.password,
            '_playlists': relationship(Playlist, back_populates='_owner')
        })

    # Review
    if not is_mapped(Review):
        mapper_registry.map_imperatively(Review, reviews_table, properties={
            '_id': reviews_table.c.id,
            '_user': relationship(User),
            '_podcast': relationship(Podcast, back_populates='_reviews'),
            '_rating': reviews_table.c.rating,
            '_comment': reviews_table.c.comment,
        })

    # Playlist
    if not is_mapped(Playlist):
        mapper_registry.map_imperatively(Playlist, playlists_table, properties={
            '_id': playlists_table.c.id,
            '_name': playlists_table.c.name,
            '_owner': relationship(User, back_populates='_playlists'),
            '_playlist': relationship(Episode, secondary=playlist_episodes_table),
        })
