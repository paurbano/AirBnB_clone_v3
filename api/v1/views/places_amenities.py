#!/usr/bin/python3
""" places amenities """
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities',
                 strict_slashes=False, methods=['GET'])
def get_plamenities(place_id):
    """ amenities in a place """
    plamelist = []
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    amenities = place.amenities
    for amenity in amenities:
        plamelist.append(amenity.to_dict())
    return jsonify(plamelist)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False, methods=['DELETE'])
def del_plamenities(place_id, amenity_id):
    """ deletes an amenity """
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    if amenity_id not in [i.id for i in place.amenities]:
        abort(404)
    place.amenities.remove(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'])
def create_plaamenities(place_id, amenity_id):
    """ creates an amenity """
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    if amenity_id in [i.id for i in place.amenities]:
        return jsonify(amenity.to_dict()), 200
    else:
        place.amenities.append(amenity)
        storage.save()
        return jsonify(amenity.to_dict()), 201
