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
        self.database_path = "postgresql://{}/{}".format("localhost:5432", self.database_name)
        self.app = create_app(test_config=self.database_path)
        self.client = self.app.test_client()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

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

    def test_get_questions_failure(self):
        res = self.client.get("/questions?page=1000000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Not found")

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

    def test_create_question_failure(self):
        res = self.client.post(
            "/questions", json={"answer": "Seoul", "difficulty": 1, "category": 3}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Bad request")

        res = self.client.post(
            "/questions",
            json={
                "question": "What is the capital of Korea?",
                "answer": "Seoul",
                "difficulty": 11,
                "category": 3,
            },
        )

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Bad request")

        res = self.client.post(
            "/questions",
            json={
                "question": "What is the capital of Korea?",
                "answer": "Seoul",
                "difficulty": 1,
                "category": 100000,
            },
        )

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Bad request")

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

    def test_delete_question_failure(self):
        res = self.client.delete(f"/questions/{10000}")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Bad request")

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
        res = self.client.post("/questions/search", json={"searchTerm": "what"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["questions"]))

    def test_search_question_failure(self):
        res = self.client.post("/questions/search", json={"searchFaile": "what"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Bad request")

        res = self.client.post("/questions/search", json={"searchTerm": "d;flkaj123df!!hat"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Not found")

    def test_get_questions_by_category(self):
        # get question by category
        category_id = 1
        res = self.client.get(f"/categories/{category_id}/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertNotEqual(data["total_questions"], 0)
        self.assertEqual(data["current_category"], category_id)

    def test_get_questions_by_category_failure(self):
        # get question by category
        category_id = 100000
        res = self.client.get(f"/categories/{category_id}/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Not found")

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

    def test_play_quiz_failure(self):
        res = self.client.post(
            "/quizzes",
            json={
                "previous_questions": [],
            },
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Can not process the request")

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
