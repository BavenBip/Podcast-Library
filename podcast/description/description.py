import math
from flask import Blueprint, render_template, request

import podcast.description.services as services
import podcast.adapters.repository as repository
from podcast.authentication.authentication import login_required

from datetime import date

from flask import Blueprint
from flask import request, render_template, redirect, url_for, session

from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, ValidationError, NumberRange

from better_profanity import profanity

description_blueprint = Blueprint('description_bp', __name__)

@description_blueprint.route('/podcastDescription/<int:podcast_id>', methods=['GET'])
def description(podcast_id: int):

    podcast = services.get_podcast_by_id(repository.repo_instance, podcast_id)
    episode_list = sorted(podcast.episodes)
    podcast_dict = services.podcast_to_dict(podcast)
    podcast_dict['review_url'] = url_for('description_bp.review_podcast', podcast=podcast_dict['id'])

    # pagination
    page = request.args.get('page', 1, type=int)
    page_amount = 3  # Number of episodes per page
    page_start = (page - 1) * page_amount
    page_end = page_start + page_amount
    total_pages = math.ceil(len(episode_list) / page_amount)
    episodes_on_page = episode_list[page_start:page_end]
    avg_rating = services.get_podcast_average_rating(repository.repo_instance, podcast_id)
    reviews = services.get_reviews(podcast_id, repository.repo_instance)

    # return render_template('/podcastDescription.html', podcast=podcast, episode_list=episode_list)
    return render_template(
        '/podcastDescription/podcastDescription.html',
        podcast=podcast,
        podcast_dict=podcast_dict,
        episodes_on_page=episodes_on_page,
        total_pages=total_pages,
        page=page,
        start_index=page_start,
        avg_rating=avg_rating,
        reviews = reviews
    )


@description_blueprint.route('/review', methods=['GET', 'POST'])
@login_required
def review_podcast():
    # Obtain the user name of the currently logged in user.
    user_name = session['user_name']

    # Create form. The form maintains state, e.g. when this method is called with a HTTP GET request and populates
    # the form with an article id, when subsequently called with a HTTP POST request, the article id remains in the
    # form.
    form = CommentForm()

    if form.validate_on_submit():
        # Successful POST, i.e. the comment text has passed data validation.
        # Extract the article id, representing the commented article, from the form.
        podcast_id = int(form.podcast_id.data)

        # Use the service layer to store the new comment.
        user = services.get_user_by_name(repository.repo_instance, user_name)
        podcast = services.get_podcast_by_id(repository.repo_instance, podcast_id)
        services.add_review(podcast, form.comment.data, user, int(form.rating.data), repository.repo_instance)

        podcast_dict = services.podcast_to_dict(podcast)
        podcast_dict['review_url'] = url_for('description_bp.review_podcast', podcast=podcast_dict['id'])
        return redirect(url_for('description_bp.description', podcast_id=podcast_dict['id']))

    if request.method == 'GET':
        # Request is a HTTP GET to display the form.
        # Extract the article id, representing the article to comment, from a query parameter of the GET request.
        podcast_id = int(request.args.get('podcast'))

        # Store the article id in the form.
        form.podcast_id.data = podcast_id
    else:
        # Request is a HTTP POST where form validation has failed.

        podcast_id = int(form.podcast_id.data)

    # For a GET or an unsuccessful POST return a Web page that allows
    # the user to enter a comment. The generated Web page includes a form object.
    podcast = services.get_podcast_by_id(repository.repo_instance, podcast_id)
    episode_list = sorted(podcast.episodes)
    podcast_dict = services.podcast_to_dict(podcast)
    podcast_dict['review_url'] = url_for('description_bp.review_podcast', podcast=podcast_dict['id'])

    # pagination
    page = request.args.get('page', 1, type=int)
    page_amount = 3  # Number of episodes per page
    page_start = (page - 1) * page_amount
    page_end = page_start + page_amount
    total_pages = math.ceil(len(episode_list) / page_amount)
    episodes_on_page = episode_list[page_start:page_end]
    avg_rating = services.get_podcast_average_rating(repository.repo_instance, podcast_id)
    reviews = services.get_reviews(podcast_id, repository.repo_instance)

    return render_template(
        'podcastDescription/podcastComments.html',
        title='Review Article',
        podcast=podcast,
        podcast_dict=podcast_dict,
        form=form,
        handler_url=url_for('description_bp.review_podcast'),
        episodes_on_page=episodes_on_page,
        total_pages=total_pages,
        page=page,
        start_index=page_start,
        avg_rating=avg_rating,
        reviews = reviews
    )


class ProfanityFree:
    def __init__(self, message=None):
        if not message:
            message = u'Field must not contain profanity'
        self.message = message

    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise ValidationError(self.message)


class CommentForm(FlaskForm):
    comment = TextAreaField('Comment', [
        DataRequired(),
        Length(min=4, message='Your comment is too short'),
        ProfanityFree(message='Your comment must not contain profanity')])
    rating = IntegerField('Rating', [
        DataRequired(),
        NumberRange(min=1, max=5, message='Rating must be between 1 and 5 (inclusive)')])
    podcast_id = HiddenField("Podcast id")
    submit = SubmitField('Submit')

