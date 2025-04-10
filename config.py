"""Flask configuration variables"""
import os
from os import environ
from dotenv import load_dotenv

load_dotenv()


class Config :
    """Set Flask configuration from .env file"""

    # Flask configuration
    FLASK_APP = environ.get('FLASK_APP')
    FLASK_ENV = environ.get('FLASK_ENV')
    SECRET_KEY = os.urandom(24)
    TESTING = environ.get('TESTING')
    REPOSITORY = environ.get('REPOSITORY')

    # Database configuration
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')

    echo_string = environ.get('SQLALCHEMY_ECHO')
    SQLALCHEMY_ECHO = False
    if echo_string.lower().strip() == "true":
        SQLALCHEMY_ECHO = True
