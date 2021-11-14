from aqt import mw
from aqt.qt import *

from myaddon.embedded_browser import show_mini_browser

action = QAction("test", mw)
qconnect(action.triggered, show_mini_browser)
mw.form.menuTools.addAction(action)