from PyQt5.QtCore import QEventLoop, Qt, QObject, pyqtSignal

from src.browser import Browser


class BrowserDriver:
    def __init__(self, qtbot):
        self._qtbot = qtbot
        self._browser = Browser(create_card_callback=self._callback_spy)
        self._reader = PageReader()
        self._selected_text = ""
        qtbot.addWidget(self._browser)

    def enter_address_and_hit_return(self, text):
        with self._qtbot.waitSignal(self._browser.tabs.currentWidget().loadFinished):
            self._browser.address_bar.clear()
            self._qtbot.keyClicks(self._browser.address_bar, text)
            self._qtbot.keyClick(self._browser.address_bar, Qt.Key_Return)

    def click_backward_button(self):
        with self._qtbot.waitSignal(self._browser.address_bar.textChanged):
            self._qtbot.mouseClick(self._browser.backBtn, Qt.MouseButton.LeftButton)

    def click_forward_button(self):
        with self._qtbot.waitSignal(self._browser.address_bar.textChanged):
            self._qtbot.mouseClick(self._browser.forBtn, Qt.MouseButton.LeftButton)

    def open_new_tab(self):
        with self._qtbot.waitSignal(self._browser.tabs.currentWidget().loadFinished):
            self._qtbot.keyClicks(self._browser.tabs, "T", Qt.ControlModifier)

    def switch_to_tab(self, index):
        with self._qtbot.waitSignal(self._browser.tabs.currentChanged):
            self._browser.tabs.setCurrentIndex(index)

    def close_active_tab(self):
        self._qtbot.keyClicks(self._browser.tabs, "W", Qt.ControlModifier)

    def select_test_span_and_trigger_copy_to_card_action(self):
        with self._qtbot.waitSignal(self._browser.tabs.currentWidget().selectionChanged):
            self._select_element_with_target_id(self._browser.tabs.currentWidget())
        self._qtbot.keyClick(self._browser.tabs.currentWidget(), Qt.Key_Enter, Qt.AltModifier)

    def _select_element_with_target_id(self, widget):
        # https://stackoverflow.com/a/987376
        widget.page().runJavaScript(("""
            node = document.getElementById('target');
            const selection = window.getSelection();
            const range = document.createRange();
            range.selectNodeContents(node);
            selection.removeAllRanges();
            selection.addRange(range);
        """))

    def _callback_spy(self, selected_text):
        self._selected_text = selected_text

    def active_tab_has_title(self, expected_title):
        self._qtbot.waitUntil(lambda: self._browser.tabs.currentWidget().title() == expected_title)

    def active_tab_contains_html(self, expected_text):
        browser_page = self._browser.tabs.currentWidget().page()
        html_content = self._reader.read_html(browser_page)
        assert expected_text in html_content

    def has_open_tabs(self, expected_count):
        assert self._browser.tabs.count() == expected_count

    def address_bar_contains(self, expected_string):
        assert expected_string in self._browser.address_bar.text()

    def backward_button_is_disabled(self):
        assert not self._browser.backBtn.isEnabled()

    def backward_button_is_enabled(self):
        self._qtbot.waitUntil(lambda: self._browser.backBtn.isEnabled())

    def forward_button_is_disabled(self):
        assert not self._browser.forBtn.isEnabled()

    def forward_button_is_enabled(self):
        self._qtbot.waitUntil(lambda: self._browser.forBtn.isEnabled())

    def callback_invoked_with_expected_text(self, expected_text):
        assert self._selected_text == expected_text


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
