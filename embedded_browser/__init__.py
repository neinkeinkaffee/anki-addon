from aqt import mw
from aqt.qt import *

from embedded_browser.browser import Browser


def show_browser():
    browser = Browser(mw)
    browser.show()

open_addon_window = QAction("Embedded Browser", mw)
qconnect(open_addon_window.triggered, show_browser)
if mw:
    mw.form.menuTools.addAction(open_addon_window)