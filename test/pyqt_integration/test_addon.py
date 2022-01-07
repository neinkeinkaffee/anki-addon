import os

from src.add_dialog import AddDialog
from src.browser import Browser
from test.drivers.add_dialog_driver import AddDialogDriver
from test.drivers.browser_driver import BrowserDriver
from test.pyqt_integration.mocks import MockCollection, MockEditor

FIXTURES_PATH = f"file://{os.getcwd()}/test/fixtures"


def test_copy_text_to_back(qtbot):
    add_dialog_instance = AddDialog(MockCollection(), MockEditor())
    add_dialog = AddDialogDriver(add_dialog_instance, qtbot)
    browser = BrowserDriver(Browser(), qtbot)
    browser.connect_create_card_signal_to_slot(add_dialog_instance.create_card_with_back)

    browser.enter_address_and_hit_return(f"{FIXTURES_PATH}/page_with_test_span.html")
    browser.select_test_span_and_trigger_copy_to_card_action()
    add_dialog.enter_note_front("passion fruit green tea")
    add_dialog.hit_add_button()

    add_dialog.note_got_added()
