from pytest_anki import AnkiSession, AnkiWebViewType
from selenium import webdriver
from time import sleep


def test_my_addon(anki_session: AnkiSession):
    def switch_to_deck_view(driver: webdriver.Chrome):
        driver.find_element_by_xpath("//*[text()='Default']").click()

    def mw_state_switched():
        assert anki_session.mw.state == "overview"

    my_addon = anki_session.load_addon("myaddon")
    with anki_session.profile_loaded():
        assert anki_session.mw.state == "deckBrowser"
        anki_session.run_with_chrome_driver(
            switch_to_deck_view, AnkiWebViewType.main_webview
        )

        from myaddon import action
        action.trigger()

        anki_session.qtbot.wait_until(mw_state_switched)



