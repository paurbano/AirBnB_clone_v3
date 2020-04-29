#!/usr/bin/python3
"""views"""
from flask import Flask, Blueprint, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.errorhandler(404)
def error_404(error):
    """ return 404 error """
    errorF = {"error": "Not found"}
    return jsonify(errorF), 404


@app.teardown_appcontext
def teardown(self):
    """close """
    storage.close()

if __name__ == "__main__":
    app.run(host=getenv('HBNB_API_HOST', '0.0.0.0'),
            port=getenv('HBNB_API_PORT', '5000'), threaded=True)
