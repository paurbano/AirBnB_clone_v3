#!/usr/bin/python3
""" reviews """
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=['GET'])
def get_reviews(place_id=None):
    """ reviews of a place """
    place_list = []
    place = storage.get('Place', place_id)
    if place:
        reviews = place.reviews
        for review in reviews:
            place_list.append(review.to_dict())
        return(jsonify(place_list)), 200
    abort(404)


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['GET'])
def get_review(review_id):
    """ returns a review """
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_review(review_id):
    """ deletes a review """
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=['POST'])
def create_review(place_id):
    """ creates a review """
    review = storage.get('Place', place_id)
    if review is None:
        abort(404)
    cont = request.get_json()
    if cont is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in cont:
        abort(400, 'Missing user_id')
    if 'text' not in cont:
        abort(400, 'Missing text')
    user = storage.get("User", cont['user_id'])
    if user is None:
        abort(404)
    ncity = Review(text=cont['text'], user_id=user.id,
                   place_id=place_id)
    storage.new(ncity)
    storage.save()
    return jsonify(ncity.to_dict()), 201


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['PUT'])
def update_review(review_id):
    """ updates a review """
    cont = request.get_json()
    if cont is None:
        abort(400, 'Not a JSON')
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    ignore = ['id', 'created_at', 'updated_at', 'user_id', 'place_id']
    for attribute, value in cont.items():
        if attribute not in ignore:
            setattr(review, attribute, value)
    storage.save()
    return jsonify(review.to_dict()), 200
