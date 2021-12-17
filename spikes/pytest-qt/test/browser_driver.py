import os

from PyQt5.QtCore import QEventLoop, Qt, QObject, pyqtSignal, QUrl

from browser import Browser

TEST_RESOURCES_DIR = "spikes/pytest-qt/test/fixtures"

class BrowserDriver:
    def __init__(self, qtbot, monkeypatch):
        self.browser = Browser()
        qtbot.addWidget(self.browser)
        self.qtbot = qtbot
        self.monkeypatch = monkeypatch
        self.reader = PageReader()

    def patch_qurl_with_local_files(self, test_pages):
        def serve_test_page(url):
            return QUrl.fromLocalFile(os.path.join(os.getcwd(), TEST_RESOURCES_DIR, test_pages[url]))
        self.monkeypatch.setattr(QUrl, "fromUserInput", serve_test_page)

    def enter_address_and_hit_return(self, text):
        self.browser.address.clear()
        self.qtbot.keyClicks(self.browser.address, text)
        self.qtbot.keyClick(self.browser.address, Qt.Key_Return)

    def click_backwards_button(self):
        self.qtbot.mouseClick(self.browser.backBtn, Qt.MouseButton.LeftButton)

    def click_forwards_button(self):
        self.qtbot.mouseClick(self.browser.forBtn, Qt.MouseButton.LeftButton)

    def assert_browser_window_title(self, expected_title):
        self.qtbot.waitUntil(lambda: self.browser.windowTitle() == expected_title)

    def assert_page_contains(self, expected_text):
        browser_page = self.browser.webEngineView.page()
        html_content = self.reader.read_html(browser_page)
        assert expected_text in html_content


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
