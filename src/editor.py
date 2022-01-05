from PyQt5.QtWidgets import QWidget
from aqt import editor


class Editor:
    def __init__(self, mw):
        self._editor = editor.Editor(mw, QWidget(), mw, True)
        self.widget = self._editor.widget

    def set_note(self, note):
        return self._editor.set_note(note, focusTo=0)

    def note(self):
        return self._editor.note
