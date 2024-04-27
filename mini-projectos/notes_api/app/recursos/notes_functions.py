from datetime import datetime
import csv


notes = {
    1: {
        'note_title': 'Note 1',
        'note_content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed non risus. Suspendisse lectus tortor, dignissim sit amet, adipiscing nec, ultricies sed, dolor.',
        'created_at': '2024-04-24 19:39:59.582078'
    },
    2: {
        'note_title': 'Note 2',
        'note_content': 'Praesent vestibulum dapibus nibh. Etiam iaculis nunc ac metus. Ut id nisl quis enim dignissim sagittis. Etiam sollicitudin, ipsum eu pulvinar rutrum, tellus ipsum laoreet sapien, quis venenatis ante odio sit amet eros.',
        'created_at': '2024-04-24 19:40:21.333580'
    },
    3: {
        'note_title': 'Note 3',
        'note_content': 'Nullam sit amet magna in magna gravida vehicula. Integer tempor. Curabitur ligula sapien, tincidunt non, euismod vitae, posuere imperdiet, leo.',
        'created_at': '2024-04-25 10:00:00'
    },
    4: {
        'note_title': 'Note 4',
        'note_content': 'Praesent egestas neque eu enim. Ut id nisl quis enim dignissim sagittis. Donec sit amet nisl. Aliquam semper ipsum sit amet velit.',
        'created_at': '2024-04-25 10:00:00'
    },
    5: {
        'note_title': 'Note 5',
        'note_content': 'Sed consequat, leo eget bibendum sodales, augue velit cursus nunc, quis gravida magna mi a libero. Fusce vulputate eleifend sapien. Vestibulum purus quam, scelerisque ut, mollis sed, nonummy id, metus.',
        'created_at': '2024-04-25 10:00:00'
    },
    6: {
        'note_title': 'Note 6',
        'note_content': 'Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus. Vivamus elementum semper nisi.',
        'created_at': '2024-04-25 10:00:00'
    },
    7: {
        'note_title': 'Note 7',
        'note_content': 'Aenean vulputate eleifend tellus. Aenean leo ligula, porttitor eu, consequat vitae, eleifend ac, enim. Aliquam lorem ante, dapibus in, viverra quis, feugiat a, tellus.',
        'created_at': '2024-04-25 10:00:00'
    },
    8: {
        'note_title': 'Note 8',
        'note_content': 'Phasellus viverra nulla ut metus varius laoreet. Quisque rutrum. Aenean imperdiet. Etiam ultricies nisi vel augue.',
        'created_at': '2024-04-25 10:00:00'
    },
    9: {
        'note_title': 'Note 9',
        'note_content': 'Curabitur ullamcorper ultricies nisi. Nam eget dui. Etiam rhoncus. Maecenas tempus, tellus eget condimentum rhoncus, sem quam semper libero, sit amet adipiscing sem neque sed ipsum.',
        'created_at': '2024-04-25 10:00:00'
    },
    10: {
        'note_title': 'Note 10',
        'note_content': 'Nam quam nunc, blandit vel, luctus pulvinar, hendrerit id, lorem. Maecenas nec odio et ante tincidunt tempus. Donec vitae sapien ut libero venenatis faucibus.',
        'created_at': '2024-04-25 10:00:00'
    }
}



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
