from PyQt5.QtWidgets import QHBoxLayout, QDialog

from .add_dialog import AddDialog
from .browser import Browser
from .collection import Collection


class Window(QDialog):
    def __init__(self, mw):
        parent = mw.app.activeWindow() if mw else None
        super(QDialog, self).__init__(parent)
        hbox = QHBoxLayout()

        self.add_dialog = AddDialog(mw, Collection(mw))
        self.browser = Browser()
        self.browser.create_card_signal.connect(self.add_dialog.create_card_with_back)
        hbox.addWidget(self.add_dialog)
        hbox.addWidget(self.browser)

        self.setLayout(hbox)
        self.show()
