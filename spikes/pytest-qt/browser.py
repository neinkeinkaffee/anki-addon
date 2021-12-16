import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QLineEdit, QMainWindow, QPushButton, QToolBar)
from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineView


class Browser(QMainWindow):
    def __init__(self):
        super(Browser, self).__init__()
        self.initUI()

    def initUI(self):
        self.toolBar = QToolBar(self)
        self.addToolBar(self.toolBar)

        self.backBtn = QPushButton(self)
        self.backBtn.setEnabled(False)
        self.backBtn.setIcon(QIcon(":/qt-project.org/styles/commonstyle/images/left-32.png"))
        self.backBtn.clicked.connect(self.back)
        self.toolBar.addWidget(self.backBtn)

        self.forBtn = QPushButton(self)
        self.forBtn.setEnabled(False)
        self.forBtn.setIcon(QIcon(":/qt-project.org/styles/commonstyle/images/right-32.png"))
        self.forBtn.clicked.connect(self.forward)
        self.toolBar.addWidget(self.forBtn)

        self.address = QLineEdit(self)
        self.address.returnPressed.connect(self.load)
        self.toolBar.addWidget(self.address)

        self.webEngineView = QWebEngineView(self)
        self.webEngineView.page().urlChanged.connect(self.onLoadFinished)
        self.webEngineView.page().titleChanged.connect(self.setWindowTitle)
        self.webEngineView.page().urlChanged.connect(self.urlChanged)
        self.setCentralWidget(self.webEngineView)

        self.setGeometry(300, 300, 500, 400)
        self.setWindowTitle("QWebEnginePage")
        self.show()

    def onLoadFinished(self):
        self.backBtn.setEnabled(self.webEngineView.history().canGoBack())
        self.forBtn.setEnabled(self.webEngineView.history().canGoForward())

    def load(self):
        url = QUrl.fromUserInput(self.address.text())
        if url.isValid():
            self.webEngineView.load(url)

    def back(self):
        self.webEngineView.page().triggerAction(QWebEnginePage.Back)

    def forward(self):
        self.webEngineView.page().triggerAction(QWebEnginePage.Forward)

    def urlChanged(self, url):
        self.address.setText(url.toString())


def main():
    app = QApplication(sys.argv)
    ex = Browser()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
