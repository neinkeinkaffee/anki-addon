from PyQt5 import QtCore
from aqt.main import AnkiQt
from pytest_anki import AnkiSession
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

from myaddon.browser.embedded_browser import Browser


def test_browser(anki_session: AnkiSession, monkeypatch):
    prevent_import_window_from_opening(monkeypatch)

    with anki_session.profile_loaded():
        browser = Browser(anki_session.mw)
        browser.show()
        anki_session.qtbot.addWidget(browser)
        anki_session.qtbot.mouseClick(browser.editor.widget, QtCore.Qt.LeftButton)

def prevent_import_window_from_opening(monkeypatch):
    def dummy_func(*args, **kwargs): pass

    monkeypatch.setattr(AnkiQt, "handleImport", dummy_func)
