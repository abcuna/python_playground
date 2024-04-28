import unittest, json, sys, os
sys.path.append(os.path.abspath('..'))
from app.notes_app import app
from app.recursos import notes_functions

class NotesCreator():
    def create_new_note_test(self):
        note_data = {
            "note_title": "Test Note",
            "note_content": "This is a test note"
        }
        return note_data


class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        notes_functions.notes.clear()

    def tearDown(self):
        self.app_context.pop()

    def test_create_note_route(self):
        response = self.app.post('/notas', json=NotesCreator().create_new_note_test())
        self.assertEqual(response.status_code, 201)

        response = self.app.get('/notas/1')
        response_data = json.loads(response.data)
        self.assertEqual(response_data[0]['note_title'], "Test Note")
        self.assertEqual(response_data[0]['note_content'], "This is a test note")
        self.app.delete('/notas/1')

    def test_delete_note(self):
        response = self.app.post('/notas', json=NotesCreator().create_new_note_test())
        response = self.app.delete('/notas/1')
        self.assertEqual(response.status_code, 200)

        response = self.app.delete('/notas/1')
        self.assertEqual(response.status_code, 404)

    def test_edit_note(self):
        response = self.app.post('/notas', json=NotesCreator().create_new_note_test())
        note_data = {"note_title": "Edited Note", "note_content": "This is a test note"}
        response = self.app.put('/notas/1', json=note_data)
        self.assertEqual(response.status_code, 200)

        response_data = json.loads(response.data)
        self.assertEqual(response_data[0]['note_title'], "Edited Note")
        self.assertEqual(response_data[0]['note_content'], "This is a test note")

    def test_import_notes(self):
        with open('test.csv', 'w') as f:
            f.write('note_title,note_content,created_at,updated_at\n')
            f.write('Test Note,This is a test note,2024-01-01,2024-01-01\n')

        with open('test.csv', 'rb') as f:
            response = self.app.post('/notas/import', data={'file': (f, 'test.csv')})

        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(response_data[0]['message'], 'Notes imported successfully')


if __name__ == '__main__':
    unittest.main()
