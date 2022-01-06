from anki.decks import DeckId
from aqt.operations.note import add_note


class Collection:
    def __init__(self, mw):
        self._mw = mw

    def new_note(self):
        return self._mw.col.newNote()

    def note_count(self):
        return self._mw.col.note_count()

    def save_note(self, note):
        if note.fields[0] and note.fields[1]:
            deck_id = DeckId(0)
            add_note(parent=None, note=note, target_deck_id=deck_id).run_in_background()