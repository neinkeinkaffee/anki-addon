import sys

from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineView
from PyQt5.QtWidgets import (QApplication, QLineEdit, QMainWindow, QPushButton, QToolBar, QTabWidget, QShortcut)


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

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        QShortcut(QKeySequence("Ctrl+T"), self, self.add_new_tab)
        QShortcut(QKeySequence("Ctrl+W"), self, self.close_active_tab)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tabs)

        self.add_new_tab(QUrl("https://duckduckgo.com"))

        self.setGeometry(300, 300, 500, 400)
        self.setWindowTitle("QWebEnginePage")
        self.show()

    def load(self):
        url = QUrl.fromUserInput(self.address.text())
        self.tabs.currentWidget().setUrl(url)

    def back(self):
        self.tabs.currentWidget().page().triggerAction(QWebEnginePage.Back)

    def forward(self):
        self.tabs.currentWidget().page().triggerAction(QWebEnginePage.Forward)

    def add_new_tab(self, qurl = None, label = "Blank"):
        if qurl is None:
            qurl = QUrl.fromUserInput("about:blank")
        browser_tab = QWebEngineView()
        i = self.tabs.addTab(browser_tab, label)
        self.tabs.setCurrentIndex(i)
        browser_tab.urlChanged.connect(lambda qurl, browser_tab = browser_tab: self.update_address_bar(qurl, browser_tab))
        browser_tab.loadFinished.connect(lambda _, i = i, browser_tab = browser_tab: self.on_load_finished(i, browser_tab))
        browser_tab.setUrl(qurl)

    def close_active_tab(self):
        self.close_tab(self.tabs.currentIndex())

    def close_tab(self, i):
        if self.tabs.count() < 2:
            return
        self.tabs.removeTab(i)

    def on_load_finished(self, i, browser_tab):
        self.tabs.setTabText(i, browser_tab.page().title())
        self.toggle_browser_history_buttons()

    def toggle_browser_history_buttons(self):
        self.backBtn.setEnabled(self.tabs.currentWidget().history().canGoBack())
        self.forBtn.setEnabled(self.tabs.currentWidget().history().canGoForward())

    def url_changed(self, url):
        self.address.setText(url.toString())

    def current_tab_changed(self, i):
        qurl = self.tabs.currentWidget().url()
        self.update_address_bar(qurl, self.tabs.currentWidget())
        self.toggle_browser_history_buttons()

    def update_address_bar(self, qurl, browser_tab):
        if browser_tab != self.tabs.currentWidget():
            return
        self.address.setText(qurl.toString())
        self.address.setCursorPosition(0)


def main():
    app = QApplication(sys.argv)
    ex = Browser()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
