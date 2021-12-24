from aqt.main import AnkiQt

from test.add_dialog.add_dialog_driver import AddDialogDriver


def test_can_add_note(anki_session, qtbot, monkeypatch):
    prevent_import_window_from_opening(monkeypatch)

    with anki_session.profile_loaded():
        add_dialog = AddDialogDriver(qtbot, anki_session.mw)
        addon = anki_session.load_addon(package_name="src")

        addon.open_window_action.trigger()
        add_dialog.shows_empty_note()

        add_dialog.enter_new_note("passion fruit green tea", "百香果綠茶")
        add_dialog.hit_add_button()
        add_dialog.note_got_added()


def prevent_import_window_from_opening(monkeypatch):
    def dummy_func(*args, **kwargs): pass

    monkeypatch.setattr(AnkiQt, "handleImport", dummy_func)