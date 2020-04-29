#!/usr/bin/python3
""" amenities """
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False,
                 methods=['GET'])
def get_amenities():
    """ all amenities """
    amelist = []
    amenities = storage.all("Amenity")
    for amenity in amenities.values():
        amelist.append(amenity.to_dict())
    return(jsonify(amelist)), 200


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['GET'])
def get_amenity(amenity_id):
    """ returns an amenity """
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['DELETE'])
def del_amenity(amenity_id):
    """ deletes an amenity """
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', strict_slashes=False,
                 methods=['POST'])
def create_amenity():
    """ creates an amenity """
    cont = request.get_json()
    if cont is None:
        abort(400, 'Not a JSON')
    if 'name' not in cont:
        abort(400, 'Missing name')
    amenity = Amenity(name=cont['name'])
    storage.new(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['PUT'])
def update_amenity(amenity_id):
    """ updates an amenity """
    cont = request.get_json()
    if cont is None:
        abort(400, 'Not a JSON')
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    for i, j in cont.items():
        if i != 'id' and i != 'created_at' and i != 'updated_at':
            setattr(amenity, i, j)
    storage.save()
    return jsonify(amenity.to_dict()), 200
