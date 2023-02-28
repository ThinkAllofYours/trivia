import os
from flask import Flask, request, abort, jsonify
from flask_cors import CORS

import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app, test_config)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "DELETE"]}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """

    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
        response.headers.add("Access-Control-Allow-Methods", "GET, POST, DELETE")
        return response


    from .views import question_views, form_views, quiz_views
    app.register_blueprint(question_views.bp)
    app.register_blueprint(form_views.bp)
    app.register_blueprint(quiz_views.bp)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    return app
