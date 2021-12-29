import os

from aqt.main import AnkiQt
from pytest_anki import AnkiSession

from test.add_dialog.add_dialog_driver import AddDialogDriver
from test.browser.browser_driver import BrowserDriver


FIXTURES_PATH = f"file://{os.getcwd()}/test/addon/fixtures"


def test_copy_text_to_back(anki_session: AnkiSession, qtbot, monkeypatch):
    prevent_import_window_from_opening(monkeypatch)

    with anki_session.profile_loaded():
        addon = anki_session.load_addon(package_name="src")
        addon.open_window_action.trigger()
        add_dialog_instance = anki_session.mw.app.activeWindow().add_dialog
        browser_instance = anki_session.mw.app.activeWindow().browser

        add_dialog = AddDialogDriver(add_dialog_instance, qtbot, anki_session.mw)
        browser_instance.set_create_card_callback(add_dialog_instance.create_card_with_back)
        browser = BrowserDriver(browser_instance, qtbot)
        browser.enter_address_and_hit_return(f"{FIXTURES_PATH}/page_with_test_span.html")
        browser.select_test_span_and_trigger_copy_to_card_action()
        add_dialog.enter_note_front("passion fruit green tea")
        add_dialog.hit_add_button()

        add_dialog.note_got_added()


def prevent_import_window_from_opening(monkeypatch):
    def dummy_func(*args, **kwargs): pass

    monkeypatch.setattr(AnkiQt, "handleImport", dummy_func)
