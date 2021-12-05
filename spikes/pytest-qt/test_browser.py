import PyQt5
from PyQt5.QtCore import QEventLoop, Qt
from PyQt5.QtCore import *

from browser import Browser


class PageReader(QObject):
    store_html_finished = pyqtSignal()
    stored_html = ""

    def store_html(self, html):
        self.stored_html = html
        self.store_html_finished.emit()

    def loop_until_signal_emitted(self, signal):
        loop = QEventLoop()
        signal.connect(loop.quit)
        loop.exec_()

    def read_html(self, page):
        page.toHtml(self.store_html)
        self.loop_until_signal_emitted(self.store_html_finished)
        return self.stored_html


class BrowserDriver:
    def __init__(self, qtbot):
        self.browser = Browser()
        qtbot.addWidget(self.browser)
        self.qtbot = qtbot
        self.reader = PageReader()

    def enter_address_and_hit_return(self, text):
        self.qtbot.keyClicks(self.browser.address, text)
        self.qtbot.keyClick(self.browser.address, Qt.Key_Return)

    def assert_browser_window_title(self, expected_title):
        self.qtbot.waitUntil(lambda: self.browser.windowTitle() == expected_title)

    def assert_page_contains(self, expected_text):
        browser_page = self.browser.webEngineView.page()
        html_content = self.reader.read_html(browser_page)
        assert expected_text in html_content

def test_loads_page(qtbot):
    browser_driver = BrowserDriver(qtbot)
    browser_driver.enter_address_and_hit_return("www.duckduckgo.com")
    browser_driver.assert_browser_window_title("DuckDuckGo — Privacy, simplified.")
    browser_driver.assert_page_contains("DuckDuckGo")




