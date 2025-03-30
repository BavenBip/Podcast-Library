import math
from encodings import search_function
from idlelib.searchengine import search_reverse

from flask import Blueprint, render_template, request, request_started

import podcast.catalogue.services as services
import podcast.adapters.repository as repository

catalogue_blueprint = Blueprint('catalogue_bp', __name__)

podcasts = sorted(services.get_podcast_data(repository.repo_instance))

@catalogue_blueprint.route('/podcasts', methods=['GET'])
def catalogue():
    # pagination
    page = request.args.get('page', 1, type=int)
    page_amount = 10
    page_start = (page - 1) * page_amount
    page_end = page_start + page_amount
    total_pages = math.ceil(len(podcasts) / page_amount)
    items_on_page = podcasts[page_start:page_end]

    return render_template('/catalogue/catalogue.html', podcasts_on_page=items_on_page, total_pages=total_pages, page=page)
