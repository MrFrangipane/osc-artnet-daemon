from PySide6.QtWidgets import QWidget, QLineEdit, QListWidget, QLabel, QGridLayout

from pyside6helpers.logger.widget import LoggerWidget


class MainWindow(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.fixtures = QListWidget()
        self.program_name = QLineEdit()
        self.logger = LoggerWidget()

