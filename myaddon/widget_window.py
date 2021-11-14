from PyQt5.QtWidgets import QDialog, QLabel, QPushButton
from aqt import mw


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