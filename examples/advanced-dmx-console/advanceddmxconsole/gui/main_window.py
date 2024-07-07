from PySide6.QtCore import Signal
from PySide6.QtWidgets import QMainWindow

from pyside6helpers.logger import dock_logger_to_main_window

from advanceddmxconsole.gui.central_widget import CentralWidget


class MainWindow(QMainWindow):
    Shown = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.central_widget = CentralWidget()
        self.setCentralWidget(self.central_widget)
        dock_logger_to_main_window(self)

        self.resize(600, 360)

    def showEvent(self, event):
        self.Shown.emit()
        event.accept()
