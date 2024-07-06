from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QApplication
from pyside6helpers import css

from oscartnetdaemon.components.midi.service_registerer import MIDIServiceRegisterer
from oscartnetdaemon.components.service_repository import ServiceRepository
from oscartnetdaemon.domain_contract.service_components import ServiceComponents

from advanceddmxconsole.service_registerer import ArtnetServiceRegisterer
from advanceddmxconsole.gui.main_window import MainWindow


class GUI(QObject):
    InitDone = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.service_repository = ServiceRepository()

    def post_init(self):
        # TODO move to a QThread
        self.service_repository.register(MIDIServiceRegisterer)
        # Register last to ensure Variable initialization will happen last
        self.service_repository.register(ArtnetServiceRegisterer)
        self.service_repository.exec()

    def exec(self):
        q_application = QApplication()
        # css.load_onto(q_application)

        main_window = MainWindow()
        main_window.Shown.connect(self.post_init)
        main_window.show()

        q_application.exec()
