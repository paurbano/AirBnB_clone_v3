#!/usr/bin/python3
""" cities """
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.city import City


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['GET'])
def get_cistates(state_id=None):
    """ cities of a state """
    cistalist = []
    state = storage.get('State', state_id)
    if state:
        cities = state.cities
        for city in cities:
            cistalist.append(city.to_dict())
        return(jsonify(cistalist)), 200
    abort(404)


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['GET'])
def get_city(city_id):
    """ returns a city """
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['DELETE'])
def del_city(city_id):
    """ deletes a city """
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['POST'])
def create_city(state_id):
    """ creates a city """
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    cont = request.get_json()
    if cont is None:
        abort(400, 'Not a JSON')
    if 'name' not in cont:
        abort(400, 'Missing name')
    ncity = City(name=cont['name'], state_id=state_id)
    storage.new(ncity)
    storage.save()
    return jsonify(ncity.to_dict()), 201


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['PUT'])
def update_city(city_id):
    """ updates a city """
    cont = request.get_json()
    if cont is None:
        abort(400, 'Not a JSON')
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    ignore = ['id', 'created_at', 'updated_at', 'state_id']
    for i, j in cont.items():
        if i not in ignore:
            setattr(city, i, j)
    storage.save()
    return jsonify(city.to_dict()), 200
