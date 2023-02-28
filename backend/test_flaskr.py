import unittest
import json
from flaskr import create_app, QUESTIONS_PER_PAGE


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

    # test categories
    def test_get_categories(self):
        res = self.client.get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["categories"])
        self.assertTrue(len(data["categories"]) == 6)

    # test questions
    def test_get_questions(self):
        res = self.client.get("/questions?page=1")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

        # check data exists
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["categories"]) == 6)
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

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
