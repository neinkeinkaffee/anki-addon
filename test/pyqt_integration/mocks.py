from PyQt5.QtWidgets import QWidget


class MockNote:
    def __init__(self):
        self.fields = ["", ""]


class MockCollection:
    def __init__(self):
        self.notes = []

    def new_note(self):
        return MockNote()

    def note_count(self):
        return len(self.notes)

    def save_note(self, note):
        if note.fields[0] and note.fields[1]:
            self.notes.append(note)


class MockEditor:
    def __init__(self):
        self._note = MockNote()
        self.widget = QWidget()

    def set_note(self, note):
        self._note = note

    def note(self):
        return self._note