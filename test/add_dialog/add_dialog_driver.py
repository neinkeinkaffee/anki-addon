from PyQt5.QtCore import Qt

from src.add_dialog import AddDialog


class AddDialogDriver:
    def __init__(self, qtbot, mw):
        self._qtbot = qtbot
        self.mw = mw
        self._add_dialog = AddDialog(mw)
        self._editor = self._add_dialog.editor

    def enter_new_note(self, front, back):
        note = self.mw.col.newNote()
        self._editor.set_note(note)
        self._editor.note.fields[0] = front
        self._editor.note.fields[1] = back

    def hit_add_button(self):
        self._qtbot.mouseClick(self._add_dialog.add_button, Qt.MouseButton.LeftButton)

    def note_got_added(self):
        self._qtbot.waitUntil(lambda: self.mw.col.note_count() == 1)

    def shows_empty_note(self):
        assert self._editor.note.fields[0] == ""
        assert self._editor.note.fields[1] == ""
