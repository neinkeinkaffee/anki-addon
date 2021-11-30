from aqt import mw
from aqt.qt import *

from myaddon.browser.embedded_browser import show_mini_browser

open_addon_window = QAction("myaddon", mw)
qconnect(open_addon_window.triggered, show_mini_browser)
if mw:
    mw.form.menuTools.addAction(open_addon_window)