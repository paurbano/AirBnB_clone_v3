#!/usr/bin/python3
"""index"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/stats', strict_slashes=False)
def stats():
    """ count all objects given a Class name"""
    dictStats = {
            "amenities": storage.count("Amenity"),
            "cities": storage.count("City"),
            "places": storage.count("Place"),
            "reviews": storage.count("Review"),
            "states": storage.count("State"),
            "users": storage.count("User")
            }
    return jsonify(dictStats)


@app_views.route("/status", strict_slashes=False)
def status():
    """return 200 status """
    status = {"status": "OK"}
    return jsonify(status), 200
