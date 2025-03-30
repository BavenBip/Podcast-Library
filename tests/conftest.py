import os

import pytest

from podcast.adapters import memory_repository
from podcast import create_app
from podcast.adapters import memory_repository, repository_populate

TEST_DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tests', 'data')


# @pytest.fixture
# def test_mem_repo():
#     repo = memory_repository.MemoryRepository()
#     database_mode = False
#     repository_populate.populate(TEST_DATA_PATH, repo, database_mode)
#     return repo
#
#
# @pytest.fixture
# def client():
#     my_app = create_app({
#         'TESTING': True,                                # Set to True during testing.
#         'REPOSITORY': 'memory',
#         'TEST_DATA_PATH': TEST_DATA_PATH,               # Path for loading test data into the repository.
#         'WTF_CSRF_ENABLED': False                       # test_client will not send a CSRF token, so disable validation.
#     })
#
#     return my_app.test_client()
#
#
class AuthenticationManager:
    def __init__(self, client):
        self.__client = client

    def login(self, user_name='thorke', password='cLQ^C#oFXloS'):
        return self.__client.post(
            'authentication/login',
            data={'user_name': user_name, 'password': password}
        )

    def logout(self):
        return self.__client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthenticationManager(client)


@pytest.fixture
def test_mem_repo():
    repo = memory_repository.MemoryRepository()
    memory_repository.populate(repo, TEST_DATA_PATH)
    return repo


@pytest.fixture
def client():
    my_app = create_app({
        'TESTING': True,
        'TEST_DATA_PATH': TEST_DATA_PATH,
        'WTF_CRSF_ENABLED': False
    })

    return my_app.test_client()

