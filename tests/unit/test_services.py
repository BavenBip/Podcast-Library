import pytest
from podcast.description.services import NonExistentPodcastException
from podcast.description import services as description_services


def test_podcast_id_is_valid(test_mem_repo):
    podcast_id = 1

    podcast = description_services.get_podcast_by_id(test_mem_repo, podcast_id)

    assert podcast is not None
    podcast_dict = description_services.podcast_to_dict(podcast)  # Use dict
    assert podcast_dict['id'] == podcast_id

def test_cannot_get_podcast_with_non_existent_id(test_mem_repo):
    podcast_id = 9999

    podcast = description_services.get_podcast_by_id(test_mem_repo, podcast_id)

    assert podcast is None

def test_can_get_first_podcast(test_mem_repo):
    podcast = description_services.get_first_podcast(test_mem_repo)

    assert podcast is not None
    assert podcast['id'] == 1  # Assuming the first podcast has id 1

def test_can_get_last_podcast(test_mem_repo):
    podcast = description_services.get_last_podcast(test_mem_repo)

    assert podcast is not None
    assert podcast['id'] > 1

def test_can_get_episode_by_id(test_mem_repo):
    episode_id = 1

    episode = description_services.get_episode_by_id(test_mem_repo, episode_id)

    assert episode is not None
    assert episode['id'] == episode_id

def test_cannot_get_episode_with_non_existent_id(test_mem_repo):
    episode_id = 9999

    episode = description_services.get_episode_by_id(test_mem_repo, episode_id)

    assert episode == "No episodes found with this id"

def test_can_get_episodes_for_podcast(test_mem_repo):
    podcast_id = 1

    episodes = description_services.get_episode_for_podcast(test_mem_repo, podcast_id)
    assert len(episodes) > 0
    for ep in episodes:
        assert ep['linked_podcast'] == podcast_id, f"Episode {ep['id']} is linked to {ep['linked_podcast']} instead of {podcast_id}"

def test_cannot_get_episodes_for_non_existent_podcast(test_mem_repo):
    podcast_id = 9999

    with pytest.raises(NonExistentPodcastException):
        description_services.get_episode_for_podcast(test_mem_repo, podcast_id)

def test_podcast_to_dict(test_mem_repo):
    podcast = test_mem_repo.get_podcast_by_id(1)
    podcast_dict = description_services.podcast_to_dict(podcast)

    assert isinstance(podcast_dict, dict)
    assert podcast_dict['id'] == podcast.id

def test_episodes_to_dict(test_mem_repo):
    episode_ids = [1, 2, 3]
    episodes = [test_mem_repo.get_episode_by_id(ep_id) for ep_id in episode_ids]
    episodes_dict = description_services.episodes_to_dict(episodes)

    assert isinstance(episodes_dict, list)
    assert all(isinstance(ep, dict) for ep in episodes_dict)
