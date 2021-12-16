from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QDialog, QLineEdit, QTabWidget


class Browser(QDialog):
    def __init__(self, parent=None):
        super(Browser, self).__init__(parent)
        self.setWindowTitle("Embedded Browser")
        self.searchbar = SearchBar(self)
        self.tab = Tab(self)


class SearchBar(QLineEdit):
    def __init__(self, parent):
        super(QLineEdit, self).__init__(parent)


class Tabs(QTabWidget):
    def __init__(self, parent):
        super(QTabWidget, self).__init__(parent)
        self.first = QWebEngineView(self)
        self.first.page().titleChanged.connect(self.setWindowTitle)
        self.first.load(QUrl.fromLocalFile("/spikes/addon/test.html"))

    def __getitem__(self, item):
        return self.first

class Tab(QWebEngineView):
    def __init__(self, parent):
        super(QWebEngineView, self).__init__(parent)
        self.titleChanged.connect(lambda x: print("HURRA"))
        self.load(QUrl.fromLocalFile("/spikes/addon/test.html"))
