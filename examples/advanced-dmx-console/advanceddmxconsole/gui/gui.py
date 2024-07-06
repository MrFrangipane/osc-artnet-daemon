from threading import Thread

from PySide6.QtCore import QObject
from PySide6.QtWidgets import QApplication
from pyside6helpers import css

from oscartnetdaemon.components.midi.service_registerer import MIDIServiceRegisterer
from oscartnetdaemon.components.service_repository import ServiceRepository

from advanceddmxconsole.service_registerer import ArtnetServiceRegisterer
from advanceddmxconsole.gui.main_window import MainWindow


class GUI(QObject):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.service_repository = ServiceRepository()
        self.service_repository.register(MIDIServiceRegisterer)
        self.service_repository.register(ArtnetServiceRegisterer)  # Register last to initialize Variables from there
        self.thread = Thread(target=self.service_repository.exec, daemon=True)

        self.q_application = QApplication()
        self.q_application.aboutToQuit.connect(self.service_repository.shutdown)
        css.load_onto(self.q_application)

        self.main_window = MainWindow()
        self.main_window.Shown.connect(self.thread.start)

    def exec(self):
        self.main_window.show()
        self.q_application.exec()
