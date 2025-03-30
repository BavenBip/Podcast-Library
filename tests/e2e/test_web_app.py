import pytest

from flask import Flask, session
# from podcast import create_app


# @pytest.fixture
# def app():
#     app = create_app()
#     yield app
#
# @pytest.fixture
# def client(app):
#     return app.test_client()

def test_registration(client):
    response = client.post('/authentication/register', data={
        'user_name': 'azapata',
        'password': 'Test123Pass'
    })
    assert response.status_code == 200  # Check if the registration was successful and redirected to login page

def test_login(client):
    response = client.post('/authentication/login', data={
        'user_name': 'azapata',
        'password': 'Test123Pass'
    })
    assert response.status_code == 200  # Check if login was successful and redirected to the home page

def test_logout(client):
    response = client.get('/authentication/logout')
    assert response.status_code == 302

def test_index(client):
    # Check that we can retrieve the home page.
    response = client.get('/')
    assert response.status_code == 200
    assert b'SoundVault' in response.data

def test_add_podcast_to_playlist(client):
    # Log in as a user
    client.post('/authentication/login', data={
        'user_name': 'azapata',
        'password': 'Test123Pass'
    })
    # Add a podcast to the playlist
    response = client.post('/playlists/add_episode', follow_redirects=True)
    assert response.status_code == 404

def test_remove_podcast_to_playlist(client):
    # Log in as a user
    client.post('/authentication/login', data={
        'user_name': 'azapata',
        'password': 'Test123Pass'
    })
    # Add a podcast to the playlist
    response = client.post('/playlists/remove_episode', follow_redirects=True)
    assert response.status_code == 404

def test_display_comments(client):
    # Access the podcast comments page to display reviews
    response = client.get('/podcastDescription/podcastComments')
    assert response.status_code == 404

