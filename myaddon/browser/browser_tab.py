from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QAction, QMenu
from aqt import qconnect, mw


class BrowserTab(QWebEngineView):
    def __init__(self, parent, editor):
        self.parent = parent
        self.editor = editor
        super().__init__(parent)
        self.loadFinished.connect(self.load_finished)
        self.load(QUrl("file:///Users/gesa/repos/anki-addon/test.html"))
        self.copy_to_back_action = QAction("Copy to back of card", self)
        qconnect(self.copy_to_back_action.triggered, self.copy_to_back)
        self.menu = QMenu("BrowserTabContextMenu", self)

    def copy_to_back(self):
        note = mw.col.newNote()
        note.fields[1] = self.selectedText()
        self.editor.set_note(note, focusTo=0)

    def load_finished(self, success):
        print("Page loaded")
        self.parent.setTabText(0, self.title())

    def contextMenuEvent(self, event):
        if self.selectedText():
            self.menu.addAction(self.copy_to_back_action)
        self.menu.popup(event.globalPos())