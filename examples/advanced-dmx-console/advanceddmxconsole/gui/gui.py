import logging
import sys

from threading import Thread

from PySide6.QtCore import QObject, Qt, Signal, QTimer
from PySide6.QtWidgets import QApplication
from pyside6helpers import css

from oscartnetdaemon.components.midi.service_registerer import MIDIServiceRegisterer
from oscartnetdaemon.components.qusb.service_registerer import QuSbServiceRegisterer
from oscartnetdaemon.components.service_repository import ServiceRepository

from advanceddmxconsole.gui.main_window import MainWindow
from advanceddmxconsole.service_registerer import ArtnetServiceRegisterer
from advanceddmxconsole.shared_data import ArtnetSharedData


_logger = logging.getLogger(__name__)


class GUI(QObject):

    ServicesInitialized = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.service_repository = ServiceRepository()
        self.service_repository.register(MIDIServiceRegisterer)

        # Register last to initialize Variables from there
        self.service_repository.register(ArtnetServiceRegisterer)
        self.service_repository.register(QuSbServiceRegisterer)

        self.thread = Thread(
            target=self.service_repository.exec,
            kwargs={'post_initialize_callback': self._post_initialize_callback},
            daemon=True
        )

        self.q_application = QApplication()
        self.q_application.aboutToQuit.connect(self.service_repository.shutdown)

        self.main_window = MainWindow()
        css.load_onto(self.main_window)
        self.main_window.Shown.connect(self.thread.start)
        self.main_window.central_widget.ProgramNameChanged.connect(self.program_name_changed)
        self.ServicesInitialized.connect(self.on_services_initialized)

        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_from_service)

    def exec(self):
        if sys.platform == 'win32':
            self.main_window.show()
        else:
            self.main_window.setWindowFlag(Qt.FramelessWindowHint, True)
            self.main_window.showFullScreen()

        self.q_application.exec()

    def on_services_initialized(self):
        self.update_from_service()
        self.update_timer.start(250)

    def update_from_service(self):
        shared_data: ArtnetSharedData = self.service_repository.shared_data(ArtnetSharedData)

        self.main_window.central_widget.set_fixture_names(
            [fixture for fixture in shared_data.get_fixture_names()]
        )
        self.main_window.central_widget.set_selected_fixture(
            shared_data.get_selected_fixture_index()
        )

        if shared_data.get_has_current_program_changed():
            self.main_window.central_widget.set_program_name(shared_data.get_current_program_name())
            shared_data.set_has_current_program_changed(False)

    def program_name_changed(self, name: str):
        shared_data: ArtnetSharedData = self.service_repository.shared_data(ArtnetSharedData)
        shared_data.set_current_program_name(name)

    def _post_initialize_callback(self):
        self.ServicesInitialized.emit()
