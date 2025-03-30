import csv
import os
import sys
from bisect import insort

from podcast.domainmodel.model import Podcast, Episode, Author, Category
from datetime import datetime


# TO DO:
# MAKE VARIABLES PUBLIC/PRIVATE/PROTECTED
def validate_non_negative_int(value):
    if not isinstance(value, int) or value < 0:
        return False
    return True


def validate_non_empty_string(value, field_name="value"):
    if not isinstance(value, str) or not value.strip() or value.strip() == "":
        return False
    return True


# CSVDataReader has attributes podcast_list, episode_list, author_dict, cat_dict
# E.g. TestReader = CSVDataReader(), episodes = TestReader.episode_list()
class CSVDataReader:
    def __init__(self, specific_route='default'):
        # In the order it appears in podcasts.csv
        self.podcast_list = []
        # In the order it appears in episodes.csv
        self.episode_list = []
        # In the order it appears in podcasts.csv, however due to duplicates line number != id number
        self.author_dict = {}
        # In the order it appears in podcasts.csv, however due to duplicates line number != id number
        self.cat_dict = {}

        if specific_route == 'default':
            file_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'podcasts.csv')
        else:
            file_dir = os.path.join(specific_route, 'podcasts.csv')
        with open(file_dir, newline='') as csvfile:
            file = csv.reader(csvfile)
            self.file = file
            next(file)

            for row in file:
                __current_id, __current_title, __current_image, __current_desc, __current_lang, \
                    __current_cats, __current_website, __current_author, __current_itunesID = row
                __current_id = int(__current_id)
                __current_itunesID = int(__current_itunesID)
                if not validate_non_empty_string(__current_title, "Podcast title"):
                    __current_title = "N/A"
                if not validate_non_empty_string(__current_image, "Podcast image"):
                    __current_image = "N/A"
                if not validate_non_empty_string(__current_desc, "Podcast desc"):
                    __current_desc = "N/A"
                if not validate_non_empty_string(__current_lang, "Podcast lang"):
                    __current_lang = "N/A"
                if not validate_non_empty_string(__current_website, "Podcast website"):
                    __current_website = "N/A"
                if not validate_non_empty_string(__current_author, "Podcast author"):
                    __current_author = "Unknown"

                __current_author = __current_author.strip()
                if __current_author in self.author_dict:
                    __new_author = self.author_dict[__current_author]  # Retrieve the existing author
                else:
                    __new_author = Author(len(self.author_dict) + 1, __current_author)  # Create a new author
                    self.author_dict[__current_author] = __new_author  # Add to the dictionary

                __new_podcast = Podcast(__current_id, __new_author, __current_title, __current_image,
                                        __current_desc, __current_website, __current_itunesID, __current_lang)

                __current_cats = [cat.strip() for cat in __current_cats.split("|")]
                for __current_cat in __current_cats:
                    __new_cat = Category(len(self.cat_dict) + 1, __current_cat)
                    if __current_cat not in self.cat_dict.keys():
                        self.cat_dict[__current_cat] = __new_cat
                        __new_podcast.add_category(__new_cat)
                    else:
                        __existing_cat = self.cat_dict[__current_cat]
                        __new_podcast.add_category(__existing_cat)

                self.podcast_list.append(__new_podcast)
                self.author_dict[__current_author].add_podcast(__new_podcast)

        if specific_route == 'default':
            file_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'episodes.csv')
        else:
            file_dir = os.path.join(specific_route, 'episodes.csv')
        with open(file_dir, newline='') as csvfile:
            file = csv.reader(csvfile)
            self.file = file
            next(file)
            for row in file:

                __current_id, __current_podcast_id, __current_title, __current_audio, __current_audio_length, \
                    __current_description, __current_pub_date = row
                __current_id = int(__current_id)
                __current_podcast = self.podcast_list[int(__current_podcast_id) - 1]
                __current_audio_length = int(__current_audio_length)

                if not validate_non_empty_string(__current_title, "Episode title"):
                    __current_title = "N/A"
                if not validate_non_empty_string(__current_audio, "Episode audio"):
                    __current_audio = "N/A"
                if not validate_non_empty_string(__current_description, "Episode desc"):
                    __current_description = "N/A"
                if not validate_non_empty_string(__current_pub_date, "Episode pub date"):
                    __current_pub_date = "9999-01-01 01:01:01+00"
                if not validate_non_negative_int(__current_audio_length):
                    __current_audio_length = 0

                formatting = "%Y-%d-%m %H:%M:%S%z"
                try:
                    __current_pub_date = datetime.strptime(__current_pub_date + "00", formatting)
                except ValueError:
                    __current_pub_date = datetime.strptime("9999-01-01 01:01:01+0000", formatting)

                __new_episode = Episode(__current_id, __current_podcast, __current_title,
                                        __current_audio, __current_audio_length,
                                        __current_description, __current_pub_date)

                self.episode_list.append(__new_episode)
                __current_podcast.add_episode(__new_episode)
