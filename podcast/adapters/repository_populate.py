import os, csv

from podcast.adapters.repository import AbstractRepository
from podcast.adapters.datareader.csvdatareader import CSVDataReader


def populate(data_path: str, repo: AbstractRepository, testing: bool = False):
    if testing:
        data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'tests', 'data')
    else:
        data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'adapters', 'data')

    reader = CSVDataReader(data_dir)

    authors = reader.author_dict
    podcasts = reader.podcast_list
    categories = reader.cat_dict
    episodes = reader.episode_list

    # Add authors to the repo

    for podcast in podcasts:
        repo.add_podcast(podcast)

    for episode in episodes:
        repo.add_episode(episode)

    for author in authors.values():
        repo.add_author(author)

    for category in categories.values():
        repo.add_category(category)
