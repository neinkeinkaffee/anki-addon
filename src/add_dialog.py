from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QDialog, QDialogButtonBox
from anki.decks import DeckId
from aqt import editor, tr
from aqt.operations.note import add_note
from aqt.qt import qconnect

class AddDialog(QDialog):
    def __init__(self, mw):
        super().__init__()
        self.editor = editor.Editor(mw, QWidget(), self, True)
        self.button_box = QDialogButtonBox(self)
        self.button_box.setOrientation(Qt.Horizontal)
        self.add_button = self.button_box.addButton(tr.actions_add(), QDialogButtonBox.ActionRole)
        qconnect(self.add_button.clicked, self.add_current_note)

    def add_current_note(self):
        note = self.editor.note
        deck_id = DeckId(0)
        add_note(parent=self, note=note, target_deck_id=deck_id).run_in_background()
