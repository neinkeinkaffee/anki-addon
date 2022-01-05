from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QDialogButtonBox, QVBoxLayout
from anki.decks import DeckId
from aqt import tr
from aqt.operations.note import add_note


class AddDialog(QWidget):
    def __init__(self, collection, editor):
        super().__init__()

        self.collection = collection

        self.vbox = QVBoxLayout()
        self.setLayout(self.vbox)

        self.editor = editor
        self.vbox.addWidget(self.editor.widget)

        self.button_box = QDialogButtonBox(self)
        self.button_box.setOrientation(Qt.Horizontal)
        self.add_button = self.button_box.addButton(tr.actions_add(), QDialogButtonBox.ActionRole)
        self.add_button.clicked.connect(self.add_current_note)
        self.vbox.addWidget(self.button_box)

        self.set_new_note()

        self.show()

    def create_card_with_back(self, back):
        note = self.collection.new_note()
        note.fields[1] = back
        self.editor.set_note(note)

    def set_new_note(self):
        note = self.collection.new_note()
        self.editor.set_note(note)

    def add_current_note(self):
        note = self.editor.note()
        if note.fields[0] and note.fields[1]:
            deck_id = DeckId(0)
            add_note(parent=None, note=note, target_deck_id=deck_id).run_in_background()
            self.set_new_note()
