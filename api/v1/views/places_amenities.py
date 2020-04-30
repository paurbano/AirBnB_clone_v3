#!/usr/bin/python3
"""places amenities"""
from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models import storage
from models.amenity import Amenity
from models.place import Place
import os


@app_views.route('/places/<string:place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_plamenities(place_id):
    """get amenity"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    ameList = []
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        amenities = place.amenities
    else:
        amenities = place.amenity_ids
    for amenity in amenities:
        ameList.append(amenity.to_dict())
    return jsonify(ameList)


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_plamenities(place_id, amenity_id):
    """deletes an amenity"""
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    if place is None:
        abort(404)
    if amenity is None:
        abort(404)
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        pamenities = place.amenities
    else:
        pamenities = place.amenity_ids
    if amenity not in pamenities:
        abort(404)
    pamenities.remove(amenity)
    place.save()
    return jsonify({})


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['POST'], strict_slashes=False)
def create_plamenities(place_id, amenity_id):
    """adds an amenity"""
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    if place is None:
        abort(404)
    if amenity is None:
        abort(404)
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        pamenities = place.amenities
    else:
        pamenities = place.amenity_ids
    if amenity in pamenities:
        return jsonify(amenity.to_dict())
    pamenities.append(amenity)
    place.save()
    return make_response(jsonify(amenity.to_dict()), 201)
