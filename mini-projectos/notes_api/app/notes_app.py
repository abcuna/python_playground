from flask import Flask, jsonify, request, send_file
from werkzeug.utils import secure_filename
import os
from recursos import notes_functions
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

notes = notes_functions.notes

UPLOAD_DIRECTORY = "./"
ALLOWED_EXTENSIONS = {'csv'}

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/notas', methods=['GET'])
def get_all_notes():
    all_notes = [{'id': note_id, **note} for note_id, note in notes.items()]
    return jsonify(all_notes)


@app.route('/notas', methods=['POST'])
def create_note():
    note = request.json
    if not notes_functions.valid_note(note):
        return jsonify({'error': 'Invalid note properties.'}), 400
    return jsonify([notes_functions.create_note(note["note_title"], note["note_content"])]), 201


@app.route('/notas/<int:note_id>', methods=['GET'])
def get_note(note_id: int):
    note = notes_functions.get_note(note_id)
    if note == {}:
        return jsonify([{'error': 'Note does not exist'}]), 404
    note_with_id = [{'id': note_id, **note}]
    return jsonify(note_with_id)


@app.route('/notas/<int:note_id>', methods=['PUT'])
def edit_note(note_id: int):
    note = request.json
    if not notes_functions.valid_note(note):
        return jsonify([{'error': 'Invalid note properties.'}]), 400
    for n in note:
        notes_functions.edit_note(note_id, n, note[n])
    return get_note(note_id), 200


@app.route('/notas/<int:note_id>', methods=['DELETE'])
def delete_note(note_id: int):
    note = notes_functions.get_note(note_id)
    if note == {}:
        return jsonify([{'error': 'Note does not exist'}]), 404
    note_title = note['note_title']
    notes_functions.delete_note(note_id)
    return jsonify([{"message": f"Note '{note_title}' deleted."}]), 200


@app.route('/notas/<notes_list>/export', methods=['GET'])
def export_notes(notes_list):
    note_ids = notes_list.split('&')
    notes_to_export = []
    for note_id in note_ids:
        note_id = int(note_id)
        if notes_functions.get_note(note_id):
            notes_to_export.append(note_id)
        else:
            return jsonify([{'error': 'Note does not exist'}]), 404
    file_path = notes_functions.export_notes(notes_to_export)
    zip_file_path = os.path.join(UPLOAD_DIRECTORY, file_path)
    return send_file(zip_file_path, as_attachment=True)


@app.route('/notas/import', methods=['POST'])
def import_notes():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and file.filename.lower().endswith('.csv'):
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_DIRECTORY, filename))
        notes_functions.import_notes(filename)
        return jsonify([{'message': 'Notes imported successfully'}]), 200
    else:
        return jsonify({'error': 'Invalid file type, only .csv files are allowed'}), 400


if __name__ == '__main__':
   app.run(port=5001)
