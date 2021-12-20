from PyQt5.QtWidgets import QDialog, QHBoxLayout

from .browser import Browser


class Window(QDialog):
    def __init__(self):
        layout = QHBoxLayout()
        browser = Browser()
        layout.addWidget(browser)