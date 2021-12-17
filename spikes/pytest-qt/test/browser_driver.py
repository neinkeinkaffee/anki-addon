import os

from PyQt5.QtCore import QEventLoop, Qt, QObject, pyqtSignal, QUrl
from browser import Browser

TEST_RESOURCES_DIR = "spikes/pytest-qt/test/fixtures"

class BrowserDriver:
    def __init__(self, qtbot, monkeypatch):
        self._qtbot = qtbot
        self._monkeypatch = monkeypatch
        self._browser = Browser()
        self._reader = PageReader()
        qtbot.addWidget(self._browser)

    def patch_qurl_with_local_files(self, test_pages):
        def serve_test_page(url):
            return QUrl.fromLocalFile(os.path.join(os.getcwd(), TEST_RESOURCES_DIR, test_pages[url]))
        self._monkeypatch.setattr(QUrl, "fromUserInput", serve_test_page)

    def enter_address_and_hit_return(self, text):
        self._browser.address.clear()
        self._qtbot.keyClicks(self._browser.address, text)
        self._qtbot.keyClick(self._browser.address, Qt.Key_Return)

    def click_backward_button(self):
        self._qtbot.mouseClick(self._browser.backBtn, Qt.MouseButton.LeftButton)

    def click_forward_button(self):
        self._qtbot.mouseClick(self._browser.forBtn, Qt.MouseButton.LeftButton)

    def open_new_tab(self):
        self._qtbot.keyClicks(self._browser.tabs, "T", Qt.ControlModifier)

    def assert_active_browser_tab_title(self, expected_title):
        self._qtbot.waitUntil(lambda: self._browser.tabs.currentWidget().title() == expected_title)

    def assert_active_browser_tab_contains_html(self, expected_text):
        browser_page = self._browser.tabs.currentWidget().page()
        html_content = self._reader.read_html(browser_page)
        assert expected_text in html_content

    def assert_tab_count(self, expected_count):
        assert self._browser.tabs.count() == expected_count

    def assert_address_bar_contains(self, expected_string):
        assert expected_string in self._browser.address.text()


class PageReader(QObject):
    finished_storing_html = pyqtSignal()
    stored_html = ""

    def store_html(self, html):
        self.stored_html = html
        self.finished_storing_html.emit()

    def loop_until_signal_emitted(self, signal):
        loop = QEventLoop()
        signal.connect(loop.quit)
        loop.exec_()

    def read_html(self, page):
        page.toHtml(self.store_html)
        self.loop_until_signal_emitted(self.finished_storing_html)
        return self.stored_html
