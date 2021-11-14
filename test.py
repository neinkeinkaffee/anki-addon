from PyQt5 import QtCore
from pytest_anki import AnkiSession, AnkiWebViewType
from selenium import webdriver
from aqt import importing
from aqt.main import AnkiQt
import pytest

def test_my_addon(anki_session: AnkiSession, monkeypatch):
    def dummy_func(): pass
    monkeypatch.setattr(AnkiQt, "handleImport", dummy_func)

    my_addon = anki_session.load_addon("myaddon")
    with anki_session.profile_loaded():
        from myaddon import action
        action.trigger()

        def select_text_on_webpage(driver: webdriver.Chrome):
            xpath = driver.find_element_by_xpath("//*[text()='This is a test.']")
            print(xpath)
            xpath.click()

        anki_session.run_with_chrome_driver(select_text_on_webpage)
