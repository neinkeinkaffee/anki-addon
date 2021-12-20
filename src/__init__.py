from aqt import mw
from aqt.qt import *
from PyQt5.QtWidgets import QAction

from .window import Window


def open_window():
    Window()


open_window_action = QAction("Browser", mw)
qconnect(open_window_action.triggered, open_window)
if mw:
    mw.form.menuTools.addAction(open_window_action)