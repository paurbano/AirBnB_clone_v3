#!/usr/bin/python3
""" users """
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, make_response
from flask import request
from models.user import User


@app_views.route('/users',  methods=['GET'], strict_slashes=False)
@app_views.route('/users/<string:user_id>', methods=['GET'],
                 strict_slashes=False)
def get_users(user_id=None):
    """ get user(s) information """
    if user_id is None:
        list_users = []
        users = storage.all("User").values()
        for user in users:
            list_users.append(user.to_dict())
        return jsonify(list_users)
    else:
        user = storage.get("User", user_id)
        if user is None:
            abort(404)
        else:
            return jsonify(user.to_dict())


@app_views.route('/users/<string:user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_User(user_id):
    """ delete a User """
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users/', methods=['POST'], strict_slashes=False)
def create_User():
    """ create a User """
    req = request.get_json()
    if req is None:
        abort(400, "Not a JSON")
    if 'email' not in req:
        abort(400, "Missing email")
    if 'password' not in req:
        abort(400, "Missing password")
    new_user = User(email=req['email'], password=req['password'])
    new_user.save()
    return make_response(jsonify((new_user.to_dict())), 201)


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_User(user_id):
    """ update a User """
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    req = request.get_json()
    if req is None:
        abort(400, "Not a JSON")
    ignore = ['id', 'created_at', 'updated_at', 'email']
    for attribute, value in req.items():
        if attribute not in ignore:
            setattr(user, attribute, value)
    user.save()
    return make_response(jsonify((user.to_dict())), 200)
