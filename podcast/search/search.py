import math
# from encodings import search_function
# from idlelib.searchengine import search_reverse

from flask import Blueprint, render_template, request, request_started

import podcast.catalogue.services as services
import podcast.adapters.repository as repository

search_blueprint = Blueprint('search_bp', __name__)

podcasts = sorted(services.get_podcast_data(repository.repo_instance))

@search_blueprint.route('/search_results', methods=['GET'])
def search():
    # pagination
    page = request.args.get('page', 1, type=int)
    page_amount = 10
    search_result = []
    search_input = request.args.get('input_text', '').lower()
    filter_input = request.args.get('filter_input', '')
    if search_input == '':
        search_result = podcasts
    elif filter_input == 'title' and search_input:
        search_result = services.get_podcasts_by_title(repository.repo_instance, search_input)
    elif filter_input == 'category' and search_input:
        search_result = services.get_podcasts_by_category(repository.repo_instance, search_input)
    elif filter_input == 'author' and search_input:
        search_result = services.get_podcasts_by_author(repository.repo_instance, search_input)
    page_start = (page - 1) * page_amount
    page_end = page_start + page_amount
    total_pages = math.ceil(len(search_result) / page_amount)

    if not search_result:
        search_result = []

    items_on_page = search_result[page_start:page_end]

    return render_template('/search/search.html', podcasts_on_page=items_on_page, total_pages=total_pages, page=page, input_text=search_input, filter_input=filter_input)

