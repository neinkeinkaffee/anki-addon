# import the main window object (mw) from aqt
import time
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QVBoxLayout

import aqt
from aqt import gui_hooks, mw
from aqt.deckchooser import DeckChooser
from anki.decks import DeckId
from aqt.editor import Editor
from aqt.operations.note import add_note
from aqt.sound import av_player
from aqt.utils import showInfo, shortcut, tooltip, tr
from aqt.qt import *

# We're going to add a menu item below. First we want to create a function to
# be called when the menu item is activated.

def show_card_count() -> None:
    # get the number of cards in the current collection, which is stored in
    # the main window
    cardCount = mw.col.card_count()
    # show a message box
    showInfo("Current card count: %d" % cardCount)

def show_label() -> None:
    label = QLabel("Hello World!", mw)
    label.show()

def show_message_box() -> None:
    box = QMessageBox(mw)
    box.setTextFormat(Qt.PlainText)
    box.setText("Hello, how's it going?")
    box.setIcon(QMessageBox.Information)
    box.setWindowTitle("Question of the day")
    button = box.addButton(QMessageBox.Ok)
    button.setDefault(True)
    box.show()


class TextDialogWindow(QDialog):
    def __init__(self):
        self.initialize_dialog_window()
        self.add_text_widget()
        self.add_close_button()

    def initialize_dialog_window(self):
        parent = mw.app.activeWindow() or mw
        super().__init__(parent)
        self.setMinimumHeight(500)
        self.setMinimumWidth(500)
        layout = QVBoxLayout(self)
        self.setWindowTitle("Text of the day")
        self.setLayout(layout)

    def add_text_widget(self):
        text = QTextBrowser()
        text.setOpenExternalLinks(True)
        text.setHtml("Hello, how's it <i>going</i>? Go <a href='https://duckduckgo.com'>there</a>")
        self.layout().addWidget(text)

    def add_close_button(self):
        box = QDialogButtonBox(QDialogButtonBox.Close)
        self.layout().addWidget(box)

        def onReject() -> None:
            QDialog.reject(self)

        qconnect(box.rejected, onReject)

def show_text() -> None:
    dialog_window = TextDialogWindow()
    dialog_window.show()


class WidgetWindow(QDialog):
    def __init__(self):
        parent = mw.app.activeWindow() or mw
        super().__init__(parent) # create default constructor for QWidget
        self.initializeUI()

    def initializeUI(self):
        """
        Initialize the window and display its contents to the screen.
        """
        self.setGeometry(100, 100, 250, 200)
        self.setWindowTitle('QPushButton Widget')
        self.displayButton() # call our displayButton function
        self.show()

    def displayButton(self):
        '''
        Setup the button widget.
        '''
        name_label = QLabel(self)
        name_label.setText("Don't push the button.")
        name_label.move(60, 30) # arrange label
        button = QPushButton('Push Me', self)
        button.clicked.connect(self.buttonClicked)
        button.move(80, 70) # arrange button

    def buttonClicked(self):
        '''
        Print message to the terminal,
        and close the window when button is clicked.
        '''
        print("The window has been closed.")
        self.close()

def show_widget() -> None:
    dialog_window = WidgetWindow()
    dialog_window.show()


class BrowserTab(QWebEngineView):
    def __init__(self, parent, editor):
        self.parent = parent
        self.editor = editor
        super().__init__(parent)
        self.loadFinished.connect(self.load_finished)
        self.load(QUrl("https://duckduckgo.com"))
        self.copy_to_back_action = QAction("Copy to back of card", self)
        qconnect(self.copy_to_back_action.triggered, self.copy_to_back)

    def copy_to_back(self):
        note = mw.col.newNote()
        note.fields[1] = self.selectedText()
        self.editor.set_note(note, focusTo=0)

    def load_finished(self, success):
        print("Got here, load finished")
        self.parent.setTabText(0, self.title())

    def contextMenuEvent(self, event):
        self.menu = QMenu()
        if self.selectedText():
            self.menu.addAction(self.copy_to_back_action)
        self.menu.popup(event.globalPos())

class MiniBrowser(QDialog):
    def __init__(self):
        self.mw = mw
        self.col = mw.col
        gui_hooks.editor_did_init.append(lambda x: print("Editor initialized"))
        parent = mw.app.activeWindow() or mw
        super().__init__(parent) # create default constructor for QWidget

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
    mini_browser = MiniBrowser()
    mini_browser.show()

# create a new menu item, "test"
action = QAction("test", mw)
# set it to call testFunction when it's clicked
qconnect(action.triggered, show_mini_browser)
# and add it to the tools menu
mw.form.menuTools.addAction(action)