import unittest
import json
from flask import Flask


class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.testing = True
        self.app_context = self.app.app_context()
        self.app_context.push()
        notes_functions.notes.clear()  # Clear notes for testing

    def tearDown(self):
        self.app_context.pop()

    def test_create_note_route(self):
        test_client = self.app.test_client()
        note_data = {
            "note_title": "Test Note",
            "note_content": "This is a test note"
        }
        response = test_client.post('/notas', json=note_data)
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.data)
        self.assertIn('id', response_data[0])
        self.assertEqual(response_data[0]['note_title'], "Test Note")
        self.assertEqual(response_data[0]['note_content'], "This is a test note")

    # Add more tests for other routes

if __name__ == '__main__':
    unittest.main()

