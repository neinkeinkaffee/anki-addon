from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QDialogButtonBox, QVBoxLayout
from anki.decks import DeckId
from aqt import editor, tr
from aqt.operations.note import add_note
from aqt.qt import qconnect

class AddDialog(QWidget):
    def __init__(self, mw):
        super().__init__()

        self.mw = mw

        self.vbox = QVBoxLayout()
        self.setLayout(self.vbox)

        self.editor = editor.Editor(mw, QWidget(self), self, True)
        self.vbox.addWidget(self.editor.widget)

        self.button_box = QDialogButtonBox(self)
        self.button_box.setOrientation(Qt.Horizontal)
        self.add_button = self.button_box.addButton(tr.actions_add(), QDialogButtonBox.ActionRole)
        qconnect(self.add_button.clicked, self.add_current_note)
        self.vbox.addWidget(self.button_box)

        self.set_new_note()

        self.show()

    def create_card_with_back(self, back):
        from aqt.utils import showInfo
        showInfo("Got the text: %s" % back)
        note = self.mw.col.newNote()
        note.fields[1] = back
        self.editor.set_note(note, focusTo=0)

    def set_new_note(self):
        note = self.mw.col.newNote()
        self.editor.set_note(note)

    def add_current_note(self):
        note = self.editor.note
        if note.fields[0] and note.fields[1]:
            deck_id = DeckId(0)
            add_note(parent=self, note=note, target_deck_id=deck_id).run_in_background()
            self.set_new_note()
