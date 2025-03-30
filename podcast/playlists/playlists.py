import math
from flask import Blueprint, render_template, request, session, redirect, url_for, flash

import podcast.playlists.services as services
import podcast.adapters.repository as repository
from podcast.authentication.authentication import login_required
from podcast.description.description import review_podcast
from podcast.domainmodel.model import Playlist

playlists_blueprint = Blueprint('playlists_bp', __name__)

podcasts = sorted(services.get_podcast_data(repository.repo_instance))


# playlists = (services.get_playlists_by_user(repository.repo_instance))

#################
@playlists_blueprint.route('/playlists', methods=['GET'])
@login_required
def playlists():
    # this code makes 1 playlist for the user, when we implement more users remove this.
    user = services.get_user_from_name(session['user_name'], repository.repo_instance)

    if services.get_playlists_by_name(session['user_name'], repository.repo_instance) is None:
        playlist = Playlist(user.id, user, session['user_name'] + "'s Playlist")
        services.add_playlist(user, playlist, repository.repo_instance)
        # user.add_playlist(playlist)

    user_playlists = services.get_playlists_by_name(session['user_name'], repository.repo_instance)
    return render_template('/playlists/playlists.html', current_playlist=user_playlists, user=session['user_name'])
######################

@playlists_blueprint.route('/add_episode', methods=['POST'])
@login_required
def add_episode():
    episode_id = request.form.get('episode_id')
    return_url = request.form.get('return_url', url_for('playlists_bp.playlists')) # If a bug occurs, we go to playlists (idk where else to go)
    user = services.get_user_from_name(session['user_name'], repository.repo_instance)

    if services.get_playlists_by_name(session['user_name'], repository.repo_instance) is None:
        playlist = Playlist(user.id, user, session['user_name'] + "'s Playlist")
        services.add_playlist(user, playlist, repository.repo_instance)
        services.get_episode_by_id(int(episode_id), repository.repo_instance)

    user_playlists = services.get_playlists_by_name(session['user_name'], repository.repo_instance)
    playlist = user_playlists

    episode = services.get_episode_by_id(int(episode_id), repository.repo_instance)

    if episode:
        playlist.add_episode(episode)
        flash(f"'{episode.title}' Added", "added")
    else:
        flash("Episode could not be added", "error")

    services.add_playlist(user, playlist, repository.repo_instance)
    return redirect(return_url)


@playlists_blueprint.route('/add_podcast', methods=['POST'])
@login_required
def add_podcast():
    podcast_id = request.form.get('podcast_id')
    return_url = request.form.get('return_url', url_for('playlists_bp.playlists')) # If a bug occurs, we go to playlists (idk where else to go)
    user = services.get_user_from_name(session['user_name'], repository.repo_instance)

    if services.get_playlists_by_name(session['user_name'], repository.repo_instance) is None:
        playlist = Playlist(user.id, user, session['user_name'] + "'s Playlist")
        services.add_playlist(user, playlist, repository.repo_instance)
        services.get_podcast_by_id(int(podcast_id), repository.repo_instance)

    user_playlists = services.get_playlists_by_name(session['user_name'], repository.repo_instance)
    playlist = user_playlists

    podcast = services.get_podcast_by_id(int(podcast_id), repository.repo_instance)

    if podcast:
        playlist.add_podcast(podcast)
        flash("All Episodes From Podcast Added", "added")
    else:
        flash("Podcast could not be added", "error")

    services.add_playlist(user, playlist, repository.repo_instance)
    return redirect(return_url)


@playlists_blueprint.route('/remove_episode', methods=['POST'])
@login_required
def remove_episode():
    episode_id = request.form.get('episode_id')
    user = services.get_user_from_name(session['user_name'], repository.repo_instance)

    if services.get_playlists_by_name(session['user_name'], repository.repo_instance) is None:
        playlist = Playlist(user.id, user, session['user_name'] + "'s Playlist")
        services.add_playlist(user, playlist, repository.repo_instance)
        services.get_episode_by_id(int(episode_id), repository.repo_instance)

    user_playlists = services.get_playlists_by_name(session['user_name'], repository.repo_instance)
    playlist = user_playlists

    episode = services.get_episode_by_id(int(episode_id), repository.repo_instance)

    if episode:
        playlist.remove_episode(episode)
        flash(f"'{episode.title}' Removed", "removed")
    else:
        flash("Episode could not be removed", "error")

    services.add_playlist(user, playlist, repository.repo_instance)
    return redirect(url_for('playlists_bp.playlists'))


@playlists_blueprint.route('/remove_podcast', methods=['POST'])
@login_required
def remove_podcast():
    podcast_id = request.form.get('podcast_id')
    user = services.get_user_from_name(session['user_name'], repository.repo_instance)
    return_url = request.form.get('return_url', url_for('playlists_bp.playlists'))  # If a bug occurs, we go to playlists (idk where else to go)

    if services.get_playlists_by_name(session['user_name'], repository.repo_instance) is None:
        playlist = Playlist(user.id, user, session['user_name'] + "'s Playlist")
        services.add_playlist(user, playlist, repository.repo_instance)
        services.get_podcast_by_id(int(podcast_id), repository.repo_instance)

    user_playlists = services.get_playlists_by_name(session['user_name'], repository.repo_instance)

    playlist = user_playlists

    podcast = services.get_podcast_by_id(int(podcast_id), repository.repo_instance)
    episodes = services.get_episodes_from_playlist(podcast, playlist, repository.repo_instance)

    if episodes:
        playlist.remove_podcast(podcast)
        flash("All Episodes From Podcast Removed", "removed")
    else:
        flash("Playlist Does Not Contain Any Episodes From This Podcast", "error")

    services.add_playlist(user, playlist, repository.repo_instance)
    return redirect(return_url)
