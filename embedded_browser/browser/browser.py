import sys

from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineView
from PyQt5.QtWidgets import (QApplication, QLineEdit, QMainWindow, QPushButton, QToolBar, QTabWidget, QShortcut)


WINDOW_DIMENSIONS = (300, 300, 500, 400)
BACK_ARROW_URI = ":/qt-project.org/styles/commonstyle/images/left-32.png"
FORWARD_ARROW_URI = ":/qt-project.org/styles/commonstyle/images/right-32.png"
FIRST_TAB_DEFAULT_URL = "https://duckduckgo.com"
NEW_TABS_DEFAULT_URL = "about:blank"
WINDOW_TITLE = "Browser"
CLOSE_TAB_KEY_SEQUENCE = "Ctrl+W"
OPEN_TAB_KEY_SEQUENCE = "Ctrl+T"


class Browser(QMainWindow):
    def __init__(self, create_card_callback=None):
        super(Browser, self).__init__()
        self.anki_create_card_callback = create_card_callback
        self.initUI()

    def initUI(self):
        self.toolBar = QToolBar(self)
        self.addToolBar(self.toolBar)

        self.backBtn = QPushButton(self)
        self.backBtn.setEnabled(False)
        self.backBtn.setIcon(QIcon(BACK_ARROW_URI))
        self.backBtn.clicked.connect(self.back)
        self.toolBar.addWidget(self.backBtn)

        self.forBtn = QPushButton(self)
        self.forBtn.setEnabled(False)
        self.forBtn.setIcon(QIcon(FORWARD_ARROW_URI))
        self.forBtn.clicked.connect(self.forward)
        self.toolBar.addWidget(self.forBtn)

        self.address_bar = QLineEdit(self)
        self.address_bar.returnPressed.connect(self.load)
        self.toolBar.addWidget(self.address_bar)

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        QShortcut(QKeySequence(OPEN_TAB_KEY_SEQUENCE), self, self.add_new_tab)
        QShortcut(QKeySequence(CLOSE_TAB_KEY_SEQUENCE), self, self.close_active_tab)
        QShortcut(QKeySequence(Qt.Key_Enter + Qt.AltModifier), self, self.call_create_card_callback)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tabs)

        self.add_new_tab(QUrl(FIRST_TAB_DEFAULT_URL))

        self.setGeometry(*WINDOW_DIMENSIONS)
        self.setWindowTitle(WINDOW_TITLE)
        self.show()

    def load(self):
        url = QUrl.fromUserInput(self.address_bar.text())
        self.tabs.currentWidget().setUrl(url)

    def back(self):
        self.tabs.currentWidget().page().triggerAction(QWebEnginePage.Back)

    def forward(self):
        self.tabs.currentWidget().page().triggerAction(QWebEnginePage.Forward)

    def add_new_tab(self, qurl = None, label = "Default"):
        if qurl is None:
            qurl = QUrl.fromUserInput(NEW_TABS_DEFAULT_URL)
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
        self.address_bar.setText(url.toString())

    def current_tab_changed(self, i):
        qurl = self.tabs.currentWidget().url()
        self.update_address_bar(qurl, self.tabs.currentWidget())
        self.toggle_browser_history_buttons()

    def update_address_bar(self, qurl, browser_tab):
        if browser_tab != self.tabs.currentWidget():
            return
        self.address_bar.setText(qurl.toString())
        self.address_bar.setCursorPosition(0)

    def call_create_card_callback(self):
        if self.anki_create_card_callback:
            self.anki_create_card_callback(self.tabs.currentWidget().selectedText())


def main():
    app = QApplication(sys.argv)
    ex = Browser()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
