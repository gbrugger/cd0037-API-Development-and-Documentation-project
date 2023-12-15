import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            'postgres', 'pass', 'localhost:5432', self.database_name)
        self.app = create_app(self.database_path)
        self.client = self.app.test_client

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_retrieve_categories_success(self):
        response = self.client().get('/categories')
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertTrue(data['success'])
        self.assertIn('categories', data)

    def test_retrieve_categories_error(self):
        response = self.client().get('/categories/123')  # Invalid endpoint
        self.assertEqual(response.status_code, 404)

    def test_retrieve_questions_success(self):
        res = self.client().get('/questions?page=1')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["categories"])

    def test_retrieve_questions_error(self):
        # Assuming no questions exist with this ID
        response = self.client().get('/questions?page=1000')
        self.assertEqual(response.status_code, 404)

    def test_delete_question_success(self):
        response = self.client().delete('/questions/22')  # Replace id on each test run
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertTrue(data['success'])
        self.assertIn('deleted', data)

    def test_delete_question_error(self):
        # Testing deletion of a non-existent question
        response = self.client().delete('/questions/9999')
        self.assertEqual(response.status_code, 404)

    def test_create_question_success(self):
        new_question_data = {
            "question": "What is Python?",
            "answer": "A programming language",
            "difficulty": 2,
            "category": 1
        }
        response = self.client().post('/questions', json=new_question_data)
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertTrue(data['success'])
        self.assertIn('created', data)
        self.assertIn('questions', data)
        self.assertIn('total_questions', data)

    def test_create_question_error(self):
        incomplete_question_data = {
            "question": "What is Python?"
            # missing 'answer', 'difficulty', and 'category'
        }
        response = self.client().post('/questions', json=incomplete_question_data)
        self.assertEqual(response.status_code, 422)

    def test_search_question_success(self):
        search_data = {"searchTerm": "author"}
        response = self.client().post('/questions/search', json=search_data)
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertTrue(data['success'])
        self.assertIn('questions', data)
        self.assertIn('total_questions', data)

    def test_search_question_error(self):
        # Testing search with a non-existent term
        search_data = {"searchTerm": "NonExistentTerm"}
        response = self.client().post('/questions/search', json=search_data)
        self.assertEqual(response.status_code, 404)

    def test_retrieve_category_questions_success(self):
        response = self.client().get('/categories/1/questions')
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertTrue(data['success'])
        self.assertIn('questions', data)
        self.assertIn('total_questions', data)

    def test_retrieve_category_questions_error(self):
        # Testing for a category with no questions available
        response = self.client().get('/categories/9999/questions')
        self.assertEqual(response.status_code, 404)

    def test_play_success(self):
        quiz_data = {
            "quiz_category": {"id": 1},
            "previous_questions": []
        }
        response = self.client().post('/quizzes', json=quiz_data)
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertTrue(data['success'])
        self.assertIn('question', data)

    def test_play_error(self):
        quiz_data = {
            "quiz_category": {"id": 9999},
            "previous_questions": []
        }
        response = self.client().post('/quizzes', json=quiz_data)
        self.assertEqual(response.status_code, 404)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
