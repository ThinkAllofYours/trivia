from flask import Blueprint
from models import Category, Question, db
from flask import jsonify, request, abort
from sqlalchemy import select
from flaskr import QUESTIONS_PER_PAGE

bp = Blueprint("main", __name__, url_prefix="/")
session = db.session

"""
@TODO:
Create an endpoint to handle GET requests for ,
including pagination (every 10 questions).
This endpoint should return a list of questions,
number of total questions, current category, categories.

TEST: At this point, when you start the application
you should see questions and categories generated,
ten questions per page and pagination at the bottom of the screen for three pages.
Clicking on the page numbers should update the questions.
"""

@bp.route("/questions", methods=["GET"])
def get_questions():
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = Question.query.all()
    formatted_questions = [question.format() for question in questions]
    categories = Category.query.all()
    formatted_categories = {category.id: category.type for category in categories}
    current_category = None
    total_questions = len(formatted_questions)
    return jsonify(
        {
            "success": True,
            "questions": formatted_questions[start:end],
            "total_questions": total_questions,
            "categories": formatted_categories,
            "current_category": current_category,
        }
    )


"""
@TODO:
Create an endpoint to DELETE question using a question ID.

TEST: When you click the trash icon next to a question, the question will be removed.
This removal will persist in the database and when you refresh the page.
"""


"""
@TODO:
Create a POST endpoint to get questions based on a search term.
It should return any questions for whom the search term
is a substring of the question.

TEST: Search by any phrase. The questions list will update to include
only question that include that string within their question.
Try using the word "title" to start.
"""


"""
@TODO:
Create a GET endpoint to get questions based on category.

TEST: In the "List" tab / main screen, clicking on one of the
categories in the left column will cause only questions of that
category to be shown.
"""
