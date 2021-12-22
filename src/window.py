from PyQt5.QtWidgets import QHBoxLayout, QDialog

from .add_dialog import AddDialog
from .browser import Browser


class Window(QDialog):
    def __init__(self, mw):
        parent = mw.app.activeWindow() or mw
        super().__init__(parent)
        hbox = QHBoxLayout()

        add_dialog = AddDialog(mw)
        browser = Browser()
        hbox.addWidget(add_dialog)
        hbox.addWidget(browser)

        self.setLayout(hbox)
        self.show()
