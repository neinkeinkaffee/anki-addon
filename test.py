from aqt.main import AnkiQt
from pytest_anki import AnkiSession
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains



def test_copy_text_to_back(anki_session: AnkiSession, monkeypatch):
    def dummy_func(*args, **kwargs): pass
    monkeypatch.setattr(AnkiQt, "handleImport", dummy_func)

    with anki_session.profile_loaded():
        addon = anki_session.load_addon(package_name="myaddon")
        addon.action.trigger()

        def select_text_on_webpage(driver: webdriver.Chrome):
            actionChains = ActionChains(driver)
            test_span = driver.find_element_by_xpath("//span[contains(text(), 'test')]")
            actionChains.double_click(test_span).perform()
            browser_tab = anki_session.mw.findChild(addon.browser_tab.BrowserTab)
            browser_tab.copy_to_back_action.trigger()
            def selected_text_copied_to_back():
                assert browser_tab.editor.note.fields[1] == "test"
            anki_session.qtbot.waitUntil(selected_text_copied_to_back)

        anki_session.run_with_chrome_driver(select_text_on_webpage)
