from threading import Thread

from PySide6.QtWidgets import QApplication, QWidget

from oscartnetdaemon.domain_contract.service_components import ServiceComponents


class GUI:

    def __init__(self, artnet_components: ServiceComponents):
        self.components = artnet_components

    def exec_in_thead(self):
        thread = Thread(target=self.exec)
        thread.start()

    def exec(self):
        q_application = QApplication()

        main_window = QWidget()
        main_window.show()

        q_application.exec()
