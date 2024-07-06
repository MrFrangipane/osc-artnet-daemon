from PySide6.QtCore import Signal
from PySide6.QtWidgets import QMainWindow, QWidget, QLineEdit, QListWidget, QLabel, QGridLayout

from pyside6helpers.logger import dock_logger_to_main_window


class MainWindow(QMainWindow):
    Shown = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setCentralWidget(CentralWidget())
        dock_logger_to_main_window(self)

    def showEvent(self, event):
        self.Shown.emit()
        event.accept()


class CentralWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.fixtures = QListWidget()
        self.program_name = QLineEdit()
