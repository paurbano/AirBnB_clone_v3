#!/usr/bin/python3
"""index"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status", strict_slashes=False)
def status():
    """return 200 status """
    status = {"status": "OK"}
    return jsonify(status), 200
