class Collection:
    def __init__(self, mw):
        self._mw = mw

    def new_note(self):
        return self._mw.col.newNote()

    def note_count(self):
        return self._mw.col.note_count()