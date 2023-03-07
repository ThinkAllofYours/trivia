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
Create an endpoint to POST a new question,
which will require the question and answer text,
category, and difficulty score.

TEST: When you submit a question on the "Add" tab,
the form will clear and the question will appear at the end of the last page
of the questions list in the "List" tab.
"""


@bp.route("/questions", methods=["POST"])
def create_question():
    body = request.get_json()

    new_question = body.get("question", None)
    new_answer = body.get("answer", None)
    category_id = body.get("category", None)
    difficulty = body.get("difficulty", None)

    if not new_question or not new_answer or not category_id or not difficulty:
        abort(400)

    try:
        new_item = Question(
            question=new_question,
            answer=new_answer,
            category=category_id,
            difficulty=difficulty,
        )
        new_item.insert()

        return jsonify({"success": True, "question_id": new_item.id})
    except:
        abort(422)


"""
@TODO:
Create an endpoint to DELETE question using a question ID.

TEST: When you click the trash icon next to a question, the question will be removed.
This removal will persist in the database and when you refresh the page.
"""


@bp.route("/questions/<int:question_id>", methods=["DELETE"])
def delete_question(question_id):
    stmt = select(Question).where(Question.id == question_id)
    question = session.scalars(stmt).one()
    if question is None:
        abort(404)
    try:
        question.delete()
        return jsonify({"success": True})
    except:
        abort(422)


"""
@TODO:
Create a POST endpoint to get questions based on a search term.
It should return any questions for whom the search term
is a substring of the question.

TEST: Search by any phrase. The questions list will update to include
only question that include that string within their question.
Try using the word "title" to start.
"""


@bp.route("/questions/search", methods=["POST"])
def search_questions():
    body = request.get_json()
    search_term = body.get("searchTerm", None)

    if search_term is not None:
        stmt = select(Question).where(Question.question.ilike(f"%{search_term}%"))
        questions = session.scalars(stmt).all()
    else:
        questions = session.query(Question).all()

    if len(questions) == 0:
        abort(404)

    formatted_questions = [question.format() for question in questions]
    return jsonify(
        {
            "success": True,
            "questions": formatted_questions,
            "total_questions": len(formatted_questions),
            "current_category": None,
        }
    )


"""
@TODO:
Create a GET endpoint to get questions based on category.

TEST: In the "List" tab / main screen, clicking on one of the
categories in the left column will cause only questions of that
category to be shown.
"""


@bp.route("/categories/<int:category_id>/questions", methods=["GET"])
def get_questions_by_category(category_id):
    stmt = select(Question).where(Question.category == category_id)
    questions = session.scalars(stmt).all()
    if len(questions) == 0:
        abort(404)
    formatted_questions = [question.format() for question in questions]
    return jsonify(
        {
            "success": True,
            "questions": formatted_questions,
            "total_questions": len(formatted_questions),
            "current_category": category_id,
        }
    )
