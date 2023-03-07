import os
from flask import Flask, jsonify
from flask_cors import CORS
from models import setup_db
from config import app_config

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    env = os.environ.get("FLASK_ENV")
    if env == "development":
        app.config.from_object(app_config["development"])
    else:
        app.config.from_object("config")
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
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type, Authorization"
        )
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

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "Bad request"}), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"success": False, "error": 404, "message": "Not found"}), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify(
                {
                    "success": False,
                    "error": 422,
                    "message": "Can not process the request",
                }
            ),
            422,
        )

    @app.errorhandler(500)
    def internal_server_error(error):
        return (
            jsonify(
                {"success": False, "error": 500, "message": "Internal server error"}
            ),
            500,
        )

    return app
