from PyQt5.QtWidgets import QWidget

from src.add_dialog import AddDialog
from test.add_dialog.add_dialog_driver import AddDialogDriver


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


def test_can_add_note(qtbot):
    add_dialog_instance = AddDialog(MockCollection(), MockEditor())
    add_dialog = AddDialogDriver(add_dialog_instance, qtbot)

    add_dialog.shows_empty_note()

    add_dialog.enter_new_note("passion fruit green tea", "百香果綠茶")
    add_dialog.hit_add_button()

    add_dialog.note_got_added()
