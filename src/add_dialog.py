from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QDialogButtonBox, QVBoxLayout

SAVE_NOTE_TEXT = "Add"


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
        self.add_button = self.button_box.addButton(SAVE_NOTE_TEXT, QDialogButtonBox.ActionRole)
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
        self.collection.save_note(note)
        self.set_new_note()
