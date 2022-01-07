from src.add_dialog import AddDialog
from test.drivers.add_dialog_driver import AddDialogDriver
from test.pyqt_integration.mocks import MockCollection, MockEditor


def test_can_add_note(qtbot):
    add_dialog_instance = AddDialog(MockCollection(), MockEditor())
    add_dialog = AddDialogDriver(add_dialog_instance, qtbot)

    add_dialog.shows_empty_note()

    add_dialog.enter_new_note("passion fruit green tea", "百香果綠茶")
    add_dialog.hit_add_button()

    add_dialog.note_got_added()
