from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QDialog, QTabWidget, QHBoxLayout, QVBoxLayout, QDialogButtonBox, QShortcut
from anki.decks import DeckId
from aqt import qconnect, mw, gui_hooks, tr
from aqt.editor import Editor
from aqt.operations.note import add_note
from aqt.sound import av_player
from aqt.utils import shortcut, tooltip

from .browser_tab import BrowserTab


class Browser(QDialog):
    def __init__(self, mw):
        self.mw = mw
        self.col = mw.col
        gui_hooks.editor_did_init.append(lambda x: print("Editor initialized"))
        parent = mw.app.activeWindow() or mw
        super().__init__(parent)

        addWidget = QtWidgets.QWidget(self)
        self.editor = Editor(self.mw, addWidget, self, True)
        self.editor.set_note(self.mw.col.newNote(), focusTo=0)
        self.defaults = self.col.defaults_for_adding(
            current_review_card=self.mw.reviewer.card
        )
        self.setWindowTitle("Mini Browser")
        tabs = QTabWidget(self)
        tab = BrowserTab(tabs, self.editor)
        tabs.insertTab(0, tab, "New Tab")

        innerLayout = QHBoxLayout()
        innerLayout.addWidget(addWidget)
        innerLayout.addWidget(tabs)

        outerLayout = QVBoxLayout()
        self.buttonbox = QtWidgets.QDialogButtonBox(self)
        self.buttonbox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonbox.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.buttonbox.accepted.connect(self.accept)
        self.buttonbox.rejected.connect(self.reject)
        QtCore.QMetaObject.connectSlotsByName(self)
        self.setupButtons()

        outerLayout.addLayout(innerLayout)
        outerLayout.addWidget(self.buttonbox)
        self.setLayout(outerLayout)

    def setupButtons(self) -> None:
        bb = self.buttonbox
        ar = QDialogButtonBox.ActionRole
        self.addButton = bb.addButton(tr.actions_add(), ar)
        qconnect(self.addButton.clicked, self.add_current_note)
        self.addButton.setShortcut(QKeySequence("Ctrl+Return"))
        # qt5.14 doesn't handle numpad enter on Windows
        self.compat_add_shorcut = QShortcut(QKeySequence("Ctrl+Enter"), self)
        qconnect(self.compat_add_shorcut.activated, self.addButton.click)
        self.addButton.setToolTip(shortcut(tr.adding_add_shortcut_ctrlandenter()))

    def add_current_note(self) -> None:
        self.editor.call_after_note_saved(self._add_current_note)

    def _add_current_note(self) -> None:
        note = self.editor.note

        # if not self._note_can_be_added(note):
        #     return

        # target_deck_id = self.deck_chooser.selected_deck_id
        target_deck_id = DeckId(self.defaults.deck_id)

        def on_success(changes) -> None:
            # only used for detecting changed sticky fields on close
            self._last_added_note = note

            # self.addHistory(note)

            # workaround for PyQt focus bug
            # self.editor.hideCompleters()

            tooltip(tr.adding_added(), period=500)
            av_player.stop_and_clear_queue()
            self._load_new_note(sticky_fields_from=note)
            gui_hooks.add_cards_did_add_note(note)

        add_note(parent=self, note=note, target_deck_id=target_deck_id).success(
            on_success
        ).run_in_background()

    # def _note_can_be_added(self, note: Note) -> bool:
    #     result = note.fields_check()
    #     # no problem, duplicate, and confirmed cloze cases
    #     problem = None
    #     if result == NoteFieldsCheckResult.EMPTY:
    #         problem = tr.adding_the_first_field_is_empty()
    #     elif result == NoteFieldsCheckResult.MISSING_CLOZE:
    #         if not askUser(tr.adding_you_have_a_cloze_deletion_note()):
    #             return False
    #     elif result == NoteFieldsCheckResult.NOTETYPE_NOT_CLOZE:
    #         problem = tr.adding_cloze_outside_cloze_notetype()
    #     elif result == NoteFieldsCheckResult.FIELD_NOT_CLOZE:
    #         problem = tr.adding_cloze_outside_cloze_field()
    #
    #     # filter problem through add-ons
    #     problem = gui_hooks.add_cards_will_add_note(problem, note)
    #     if problem is not None:
    #         showWarning(problem, help=HelpPage.ADDING_CARD_AND_NOTE)
    #         return False
    #
    #     return True

    def _load_new_note(self, sticky_fields_from) -> None:
        note = self._new_note()
        if old_note := sticky_fields_from:
            flds = note.note_type()["flds"]
            # copy fields from old note
            if old_note:
                for n in range(min(len(note.fields), len(old_note.fields))):
                    if flds[n]["sticky"]:
                        note.fields[n] = old_note.fields[n]
            # and tags
            note.tags = old_note.tags
        self.setAndFocusNote(note)

    def _new_note(self):
        return self.col.new_note(self.defaults.notetype_id)

    def setAndFocusNote(self, note) -> None:
        self.editor.set_note(note, focusTo=0)


def show_mini_browser() -> None:
    mini_browser = Browser(mw)
    mini_browser.show()