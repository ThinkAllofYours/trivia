import unittest
import json
import random
from flaskr import create_app
from models import Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}/{}".format(
            "localhost:5432", self.database_name
        )
        self.app = create_app(test_config=self.database_path)
        self.client = self.app.test_client()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    # test categories
    def test_get_categories(self):
        res = self.client.get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["categories"]))
        self.assertTrue(data["categories"])

    # test questions
    def test_get_questions(self):
        res = self.client.get("/questions?page=1")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

        # check data exists
        self.assertTrue(data["total_questions"])
        self.assertIsNone(data["current_category"])

        # check pagination
        self.assertEqual(len(data["questions"]), 10)

    def test_create_question(self):
        res = self.client.post(
            "/questions",
            json={
                "question": "What is the capital of Korea?",
                "answer": "Seoul",
                "difficulty": 1,
                "category": 3,
            },
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_delete_question(self):
        res = self.client.post(
            "/questions",
            json={
                "question": "What is the capital of Korea?",
                "answer": "Seoul",
                "difficulty": 1,
                "category": 3,
            },
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data.get("question_id"))

        question_id = data.get("question_id")
        res = self.client.delete(f"/questions/{question_id}")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_search_question(self):
        # create a question
        res = self.client.post(
            "/questions",
            json={
                "question": "What is the capital of Korea?",
                "answer": "Seoul",
                "difficulty": 1,
                "category": 3,
            },
        )
        data = json.loads(res.data)
        question = data.get("question")

        res = self.client.post("/questions/search", json={"searchTerm": question})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["questions"]))

    def test_get_questions_by_category(self):
        # create a category
        category = Category(type="Test Category")
        with self.app.app_context():
            category.insert()

        with self.app.app_context():
            category = Category.query.filter_by(type="Test Category").first()

        # create a question
        question1 = Question(
            question="What is the capital of Korea1?",
            answer="Seoul",
            difficulty=1,
            category=category.id,
        )

        question2 = Question(
            question="What is the capital of Korea2?",
            answer="Seoul",
            difficulty=1,
            category=category.id,
        )

        with self.app.app_context():
            question1.insert()
            question2.insert()

        res = self.client.get(f"/categories/{category.id}/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["total_questions"], 2)
        self.assertEqual(data["current_category"], category.id)

        with self.app.app_context():
            question1.delete()
            question2.delete()
            category.delete()

    def test_play_quiz(self):
        # get category
        with self.app.app_context():
            category = Category.query.all()
            category = random.choice(category)

        # get questions
        res = self.client.get(f"/categories/{category.id}/questions")
        data = json.loads(res.data)
        questions = data["questions"]

        # play quiz
        previous_questions = []
        if len(questions) > 2:
            previous_questions.append(questions[0]["id"])
            previous_questions.append(questions[1]["id"])

        res = self.client.post(
            "/quizzes",
            json={
                "previous_questions": previous_questions,
                "quiz_category": {"type": category.type, "id": category.id},
            },
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["question"])
        self.assertTrue(data["question"]["id"] not in previous_questions)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
