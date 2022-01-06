import pytest
from aqt.main import AnkiQt

from src.collection import Collection
from src.editor import Editor


@pytest.mark.parametrize("anki_session", [dict(load_profile=True)], indirect=True)
def test_gets_and_sets_note(anki_session, monkeypatch):
    prevent_import_window_from_opening(monkeypatch)

    collection = Collection(anki_session._mw)
    editor = Editor(anki_session._mw)

    note_1 = collection.new_note()
    note_1.fields = "front", "back"
    editor.set_note(note_1)
    note_2 = editor.note()

    assert note_1 == note_2


def prevent_import_window_from_opening(monkeypatch):
    def dummy_func(*args, **kwargs): pass

    monkeypatch.setattr(AnkiQt, "handleImport", dummy_func)