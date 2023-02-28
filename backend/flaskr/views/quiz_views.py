from flask import Blueprint
from models import Category, Question, db
from flask import jsonify
from sqlalchemy import select

bp = Blueprint("quiz", __name__, url_prefix="/play")
session = db.session

"""
@TODO:
Create a POST endpoint to get questions to play the quiz.
This endpoint should take category and previous question parameters
and return a random questions within the given category,
if provided, and that is not one of the previous questions.

TEST: In the "Play" tab, after a user selects "All" or a category,
one question at a time is displayed, the user is allowed to answer
and shown whether they were correct or not.
"""
