import pytest
from aqt.main import AnkiQt

from src.collection import Collection


@pytest.mark.parametrize("anki_session", [dict(load_profile=True)], indirect=True)
def test_saves_non_empty_note(anki_session, monkeypatch):
    prevent_import_window_from_opening(monkeypatch)

    collection = Collection(anki_session._mw)

    note = collection.new_note()
    note.fields = "", ""
    collection.save_note(note)
    actual_count = collection.note_count()

    assert 0 == actual_count

    note = collection.new_note()
    note.fields = "front", "back"
    collection.save_note(note)
    actual_count = collection.note_count()

    assert 1 == actual_count


def prevent_import_window_from_opening(monkeypatch):
    def dummy_func(*args, **kwargs): pass

    monkeypatch.setattr(AnkiQt, "handleImport", dummy_func)