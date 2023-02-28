from flask import Blueprint
from models import Category, Question, db
from flask import jsonify
from sqlalchemy import select

bp = Blueprint("categories", __name__, url_prefix="/add")
session = db.session

# define endpoint to get all categories
"""
@TODO:
Create an endpoint to handle GET requests
for all available categories.
"""

"""
@TODO:
Create an endpoint to POST a new question,
which will require the question and answer text,
category, and difficulty score.

TEST: When you submit a question on the "Add" tab,
the form will clear and the question will appear at the end of the last page
of the questions list in the "List" tab.
"""


@bp.route("/categories", methods=["GET"])
def get_categories():
    categories = session.query(Category).all()
    return jsonify({"success": True, "categories": [category.format() for category in categories]})
