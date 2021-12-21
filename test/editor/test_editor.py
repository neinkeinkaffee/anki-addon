from aqt.main import AnkiQt

from test.editor.editor_driver import AddDialogDriver


def test_can_add_note(anki_session, qtbot, monkeypatch):
    prevent_import_window_from_opening(monkeypatch)

    with anki_session.profile_loaded():
        editor = AddDialogDriver(qtbot, anki_session.mw)
        addon = anki_session.load_addon(package_name="src")
        addon.open_window_action.trigger()

        editor.enter_new_note("passion fruit green tea", "百香果綠茶")
        editor.hit_add_button()

        editor.note_got_added()


def prevent_import_window_from_opening(monkeypatch):
    def dummy_func(*args, **kwargs): pass

    monkeypatch.setattr(AnkiQt, "handleImport", dummy_func)