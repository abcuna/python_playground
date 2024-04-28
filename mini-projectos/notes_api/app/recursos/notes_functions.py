from datetime import datetime
import csv


notes = {}



def valid_note(note):
    for key in note.keys():
        if key not in ['note_title', 'note_content']:
            return False
    return True


def create_note(note_title, note_content, created_at=None, updated_at=None):
    if created_at is None:
        created_at = f"{datetime.now()}"
    if updated_at is None:
        updated_at = f"{datetime.now()}"

    # getting the id of the last element on the dictionary and adding one.
    new_note_id = max(notes.keys(), default=0) + 1
    notes[new_note_id] = {
        "note_title": note_title,
        "note_content": note_content,
        "created_at": created_at,
        "updated_at": updated_at
    }
    return notes[new_note_id]


def get_all_notes() -> dict:
    return notes


def get_note(note_id: int):
    return notes.get(note_id, {})


def get_notes(notes_list):
    return [notes[note_id] for note_id in notes_list if note_id in notes]


def delete_note(note_id: int):
    if note_id in notes:
        del notes[note_id]
        return True
    return False


def edit_note(note_id: int, criteria: str, data):
    if get_note(note_id) != {}:
        if criteria in notes[note_id]:
            notes[note_id][criteria] = data
            notes[note_id]['updated_at'] = datetime.now().isoformat()
            return True
    return False


def export_notes(notes_list):
    exported_notes = get_notes(notes_list)
    csv_filename = f"notes_export.csv"
    header = ["note_title", "note_content", "created_at", "updated_at"]

    with open(csv_filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(exported_notes)

    return csv_filename


def import_notes(ficheiro: str):
    with open(f"{ficheiro}", 'r') as f:
        notes_reader = csv.DictReader(f)
        for note in notes_reader:
            if note["updated_at"] != "":
                imported_notes = create_note(note["note_title"], note["note_content"], note["created_at"], note["updated_at"])
            else:
                imported_notes = create_note(note["note_title"], note["note_content"], note["created_at"])
    return imported_notes
