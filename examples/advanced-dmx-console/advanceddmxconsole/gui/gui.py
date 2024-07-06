import logging
from threading import Thread

from PySide6.QtCore import QObject
from PySide6.QtWidgets import QApplication
from pyside6helpers import css

from oscartnetdaemon.components.midi.service_registerer import MIDIServiceRegisterer
from oscartnetdaemon.components.service_repository import ServiceRepository

from advanceddmxconsole.advanced_dmx_console import AdvancedDmxConsole
from advanceddmxconsole.service_registerer import ArtnetServiceRegisterer
from advanceddmxconsole.gui.main_window import MainWindow


_logger = logging.getLogger(__name__)


class GUI(QObject):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.service_repository = ServiceRepository()
        self.service_repository.register(MIDIServiceRegisterer)
        self.service_repository.register(ArtnetServiceRegisterer)  # Register last to initialize Variables from there
        self.thread = Thread(
            target=self.service_repository.exec,
            kwargs={'post_initialize_callback': self.post_initialize_callback},
            daemon=True
        )

        self.q_application = QApplication()
        self.q_application.aboutToQuit.connect(self.service_repository.shutdown)
        css.load_onto(self.q_application)

        self.main_window = MainWindow()
        self.main_window.Shown.connect(self.thread.start)

    def exec(self):
        self.main_window.show()
        self.q_application.exec()

    def post_initialize_callback(self):
        # FIXME: we have nothing here because the real class is in another process
        _logger.info(AdvancedDmxConsole().fixture_repository.fixtures)
