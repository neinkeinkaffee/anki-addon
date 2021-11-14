from pytest_anki import AnkiSession
from selenium import webdriver
from aqt.main import AnkiQt

def test_my_addon(anki_session: AnkiSession, monkeypatch):
    def dummy_func(): pass
    monkeypatch.setattr(AnkiQt, "handleImport", dummy_func)

    with anki_session.profile_loaded():
        from myaddon import action
        action.trigger()

        def select_text_on_webpage(driver: webdriver.Chrome):
            xpath = driver.find_element_by_xpath("//*[text()='This is a test.']")
            print(xpath)
            xpath.click()

        anki_session.run_with_chrome_driver(select_text_on_webpage)
