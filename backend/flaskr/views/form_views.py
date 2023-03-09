from flask import Blueprint, abort
from models import Category, Question, db
from flask import jsonify
from sqlalchemy import select

bp = Blueprint("categories", __name__, url_prefix="/")
session = db.session

# define endpoint to get all categories
"""
@TODO:
Create an endpoint to handle GET requests
for all available categories.
"""


@bp.route("/categories", methods=["GET"])
def get_categories():
    try:
        categories = session.query(Category).all()
        formatted_categories = {category.id: category.type for category in categories}
        return jsonify({"success": True, "categories": formatted_categories})
    except:
        abort(500)


