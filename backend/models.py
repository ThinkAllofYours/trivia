import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json

db = SQLAlchemy()
migrate = Migrate()

"""
setup_db(app)
    binds a flask application and a SQLAlchemy service
"""


def setup_db(app, test_config=None):
    with app.app_context():
        db.init_app(app)
        migrate.init_app(app, db)
        db.create_all()


class BaseModel(db.Model):
    __abstract__ = True

    def __init__(self):
        pass

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        raise NotImplementedError


"""
Question

"""


class Question(BaseModel):
    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String)
    answer = db.Column(db.String)
    difficulty = db.Column(db.Integer)

    category = db.Column(db.Integer, db.ForeignKey("categories.id"))

    def __init__(self, question, answer, category, difficulty):
        self.question = question
        self.answer = answer
        self.category = category
        self.difficulty = difficulty

    def format(self):
        return {
            "id": self.id,
            "question": self.question,
            "answer": self.answer,
            "category": self.category,
            "difficulty": self.difficulty,
        }


"""
Category

"""


class Category(BaseModel):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String)

    def __init__(self, type):
        self.type = type

    def format(self):
        return {"id": self.id, "type": self.type}
