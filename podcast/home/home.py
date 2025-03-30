from flask import Blueprint, render_template, request

import podcast.home.services as services

import podcast.adapters.repository as repository

home_blueprint = Blueprint('home_bp', __name__)


podcasts = services.get_home_data(repository.repo_instance)  # Get list of podcasts


@home_blueprint.route('/', methods=['GET'])
def home():
    # some_podcast = create_some_podcast()
    # Use Jinja to customize a predefined html page rendering the layout for showing a single podcast.
    return render_template('/layout/layout.html', podcasts=podcasts)
