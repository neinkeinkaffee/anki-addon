from PyQt5.QtCore import Qt

class AddDialogDriver:
    def __init__(self, add_dialog, qtbot):
        self._qtbot = qtbot
        self._add_dialog = add_dialog
        self._qtbot.addWidget(self._add_dialog)

    def enter_new_note(self, front, back):
        note = self._add_dialog.collection.new_note()
        self._add_dialog.editor.set_note(note)
        self._add_dialog.editor.note().fields[0] = front
        self._add_dialog.editor.note().fields[1] = back

    def hit_add_button(self):
        self._qtbot.mouseClick(self._add_dialog.add_button, Qt.MouseButton.LeftButton)

    def note_got_added(self):
        self._qtbot.waitUntil(lambda: self._add_dialog.collection.note_count() == 1)

    def shows_empty_note(self):
        assert self._add_dialog.editor.note().fields[0] == ""
        assert self._add_dialog.editor.note().fields[1] == ""

    def enter_note_front(self, front):
        self._add_dialog.editor.note().fields[0] = front
