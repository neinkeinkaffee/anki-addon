from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextBrowser, QDialogButtonBox
from aqt import mw, qconnect


class TextDialogWindow(QDialog):
    def __init__(self):
        self.initialize_dialog_window()
        self.add_text_widget()
        self.add_close_button()

    def initialize_dialog_window(self):
        parent = mw.app.activeWindow() or mw
        super().__init__(parent)
        self.setMinimumHeight(500)
        self.setMinimumWidth(500)
        layout = QVBoxLayout(self)
        self.setWindowTitle("Text of the day")
        self.setLayout(layout)

    def add_text_widget(self):
        text = QTextBrowser()
        text.setOpenExternalLinks(True)
        text.setHtml("Hello, how's it <i>going</i>? Go <a href='https://duckduckgo.com'>there</a>")
        self.layout().addWidget(text)

    def add_close_button(self):
        box = QDialogButtonBox(QDialogButtonBox.Close)
        self.layout().addWidget(box)

        def onReject() -> None:
            QDialog.reject(self)

        qconnect(box.rejected, onReject)


def show_text() -> None:
    dialog_window = TextDialogWindow()
    dialog_window.show()