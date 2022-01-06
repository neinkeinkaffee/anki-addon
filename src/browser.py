import re
import sys

from PyQt5.QtCore import QUrl, pyqtSignal
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineView
from PyQt5.QtWidgets import (QApplication, QLineEdit, QPushButton, QToolBar, QTabWidget, QShortcut,
                             QWidget, QVBoxLayout)

BACK_ARROW_URI = ":/qt-project.org/styles/commonstyle/images/left-32.png"
FORWARD_ARROW_URI = ":/qt-project.org/styles/commonstyle/images/right-32.png"
FIRST_TAB_DEFAULT_URL = "https://duckduckgo.com"
NEW_TABS_DEFAULT_URL = "about:blank"
CLOSE_TAB_KEY_SEQUENCE = "Ctrl+W"
OPEN_TAB_KEY_SEQUENCE = "Ctrl+T"
CREATE_CARD_KEY_SEQUENCE = "Ctrl+L"
LAUNCH_QUERY_KEY_SEQUENCE = "Ctrl+K"
# Source: https://gist.github.com/gruber/249502
URL_REGEX = re.compile(r'(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)'
                       r'(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)'
                       r'|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))')


class Tab(QWebEngineView):
    open_link_in_tab_requested = pyqtSignal(QUrl)

    def __init__(self):
        super().__init__()

    def contextMenuEvent(self, event):
        menu = self.page().createStandardContextMenu()
        if self._link_was_clicked():
            open_new_tab_action = menu.actions()[0]
            open_new_tab_action.triggered.connect(self._emit_open_tab_signal)
            open_new_window_action = menu.actions()[1]
            open_new_window_action.setVisible(False)
        menu.exec_(event.globalPos())

    def _link_was_clicked(self):
        return not self.page().contextMenuData().linkUrl().isEmpty()

    def _emit_open_tab_signal(self):
        self.open_link_in_tab_requested.emit(self.page().contextMenuData().linkUrl())


class Browser(QWidget):
    create_card_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.create_card_callback = None
        self.initUI()

    def initUI(self):
        QShortcut(QKeySequence(CREATE_CARD_KEY_SEQUENCE), self, self.emit_create_card_signal)
        QShortcut(QKeySequence(LAUNCH_QUERY_KEY_SEQUENCE), self, self.launch_query)

        self.vbox = QVBoxLayout()
        self.setLayout(self.vbox)

        self.toolbar = QToolBar(self)
        self.vbox.addWidget(self.toolbar)

        self.backBtn = QPushButton(self)
        self.backBtn.setEnabled(False)
        self.backBtn.setIcon(QIcon(BACK_ARROW_URI))
        self.backBtn.clicked.connect(self.back)
        self.toolbar.addWidget(self.backBtn)

        self.forBtn = QPushButton(self)
        self.forBtn.setEnabled(False)
        self.forBtn.setIcon(QIcon(FORWARD_ARROW_URI))
        self.forBtn.clicked.connect(self.forward)
        self.toolbar.addWidget(self.forBtn)

        self.address_bar = QLineEdit(self)
        self.address_bar.returnPressed.connect(self.load)
        self.toolbar.addWidget(self.address_bar)

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        QShortcut(QKeySequence(OPEN_TAB_KEY_SEQUENCE), self, self.add_new_tab)
        QShortcut(QKeySequence(CLOSE_TAB_KEY_SEQUENCE), self, self.close_active_tab)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.vbox.addWidget(self.tabs)

        self.add_new_tab(QUrl(FIRST_TAB_DEFAULT_URL))

        self.show()

    def load(self):
        address_bar_input = self.address_bar.text()
        if re.match(URL_REGEX, address_bar_input):
            url = QUrl.fromUserInput(address_bar_input)
        else:
            url = QUrl("https://duckduckgo.com")
            url.setQuery("q=" + address_bar_input)
        self.tabs.currentWidget().setUrl(url)

    def back(self):
        self.tabs.currentWidget().page().triggerAction(QWebEnginePage.Back)

    def forward(self):
        self.tabs.currentWidget().page().triggerAction(QWebEnginePage.Forward)

    def add_new_tab(self, qurl = None, label = "Default"):
        if qurl is None:
            qurl = QUrl.fromUserInput(NEW_TABS_DEFAULT_URL)
        tab = Tab()
        i = self.tabs.addTab(tab, label)
        self.tabs.setCurrentIndex(i)
        tab.urlChanged.connect(lambda qurl, browser_tab = tab: self.update_address_bar(qurl, browser_tab))
        tab.loadFinished.connect(lambda _, i = i, browser_tab = tab: self.on_load_finished(i, browser_tab))
        tab.open_link_in_tab_requested.connect(self.add_new_tab)
        tab.setUrl(qurl)

    def close_active_tab(self):
        self.close_tab(self.tabs.currentIndex())

    def close_tab(self, i):
        if self.tabs.count() < 2:
            return
        self.tabs.removeTab(i)

    def launch_query(self):
        query = self.tabs.currentWidget().selectedText()
        qurl = QUrl("https://duckduckgo.com?q=" + query)
        self.add_new_tab(qurl)

    def on_load_finished(self, i, browser_tab):
        self.tabs.setTabText(i, browser_tab.page().title())
        self.toggle_browser_history_buttons()

    def toggle_browser_history_buttons(self):
        self.backBtn.setEnabled(self.tabs.currentWidget().history().canGoBack())
        self.forBtn.setEnabled(self.tabs.currentWidget().history().canGoForward())

    def url_changed(self, url):
        self.address_bar.setText(url.toString())

    def current_tab_changed(self):
        qurl = self.tabs.currentWidget().url()
        self.update_address_bar(qurl, self.tabs.currentWidget())
        self.toggle_browser_history_buttons()

    def update_address_bar(self, qurl, browser_tab):
        if browser_tab != self.tabs.currentWidget():
            return
        self.address_bar.setText(qurl.toString())
        self.address_bar.setCursorPosition(0)

    def emit_create_card_signal(self):
        self.create_card_signal.emit(self.tabs.currentWidget().selectedText())


def main():
    app = QApplication(sys.argv)
    ex = Browser()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
