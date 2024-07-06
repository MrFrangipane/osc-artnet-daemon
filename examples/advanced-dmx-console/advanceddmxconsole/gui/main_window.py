from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QLineEdit, QListWidget, QLabel, QGridLayout

from pyside6helpers.logger.widget import LoggerWidget


class MainWindow(QWidget):
    Shown = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.fixtures = QListWidget()
        self.program_name = QLineEdit()
        self.logger = LoggerWidget()

        layout = QGridLayout(self)
        layout.addWidget(self.logger)

    def showEvent(self, event):
        self.Shown.emit()
        event.accept()
