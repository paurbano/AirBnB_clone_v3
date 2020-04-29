#!/usr/bin/python3
""" states """
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, make_response
from flask import request
from models.state import State


@app_views.route('/states',  methods=['GET'], strict_slashes=False)
@app_views.route('/states/<string:state_id>', methods=['GET'],
                 strict_slashes=False)
def get_states(state_id=None):
    """ get state(s) information """
    if state_id is None:
        list_states = []
        states = storage.all("State").values()
        for state in states:
            list_states.append(state.to_dict())
        return jsonify(list_states)
    else:
        state = storage.get("State", state_id)
        if state is None:
            abort(404)
        else:
            return jsonify(state.to_dict())


@app_views.route('/states/<string:state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """ delete a state """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def create_state():
    """ create a state """
    req = request.get_json()
    # print(type(req))
    if req is None:
        abort(400, "Not a JSON")
    if 'name' not in req:
        abort(400, "Missing name")
    new_state = State(name=req['name'])
    new_state.save()
    return make_response(jsonify((new_state.to_dict())), 201)


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    """ update a state """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    req = request.get_json()
    if req is None:
        abort(400, "Not a JSON")
    ignore = ['id', 'created_at', 'updated_at']
    for attribute, value in req.items():
        if attribute not in ignore:
            setattr(state, attribute, value)
    state.save()
    return make_response(jsonify((state.to_dict())), 200)
