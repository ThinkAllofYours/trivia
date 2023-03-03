from flask import Blueprint, jsonify, request
from models import Question, db
from flask import jsonify
from sqlalchemy import select
import random

bp = Blueprint("quiz", __name__, url_prefix="/")
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


@bp.route("/quizzes", methods=["POST"])
def play_quiz():
    body = request.get_json()
    previous_questions = body.get("previous_questions", [])
    quiz_category = body.get("quiz_category", None)

    if quiz_category and quiz_category["id"]:
        stmt = (
            select(Question)
            .where(Question.category == quiz_category["id"])
            .where(Question.id.notin_(previous_questions))
        )
    else:
        stmt = select(Question).where(Question.id.notin_(previous_questions))

    questions = session.scalars(stmt).all()
    if questions is not None:
        question = random.choice(questions)
        response = jsonify({"success": True, "question": question.format()})
    else:
        response = jsonify({"success": True, "question": None})

    return response
