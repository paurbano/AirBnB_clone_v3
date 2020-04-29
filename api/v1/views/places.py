#!/usr/bin/python3
""" places """
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.place import Place


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['GET'])
def get_places(city_id=None):
    """ places of a city """
    plalist = []
    city = storage.get('City', city_id)
    if city:
        places = city.places
        for place in places:
            plalist.append(place.to_dict())
        return(jsonify(plalist)), 200
    abort(404)


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['GET'])
def get_place(place_id):
    """ returns a place """
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['DELETE'])
def del_place(place_id):
    """ deletes a place """
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['POST'])
def create_place(city_id):
    """ creates a place """
    cols = ['name', 'user_id']
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    cont = request.get_json()
    if cont is None:
        abort(400, 'Not a JSON')
    for col in cols:
        if col not in cont:
            abort(400, 'Missing {}'.format(col))
    user = storage.get('User', content['user_id'])
    if user is None:
        abort(404)
    cont['city_id'] = city_id
    place = Place(**cont)
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['PUT'])
def update_place(place_id):
    """ updates a place """
    cont = request.get_json()
    if cont is None:
        abort(400, 'Not a JSON')
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    ignore = ['id', 'created_at', 'updated_at', 'city_id', 'user_id']
    for i, j in cont.items():
        if i not in ignore:
            setattr(place, i, j)
    storage.save()
    return jsonify(place.to_dict()), 200
