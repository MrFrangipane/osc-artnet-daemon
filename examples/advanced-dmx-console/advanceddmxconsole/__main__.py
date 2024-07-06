import logging

from oscartnetdaemon.components.midi.service_registerer import MIDIServiceRegisterer
from oscartnetdaemon.components.service_repository import ServiceRepository

from advanceddmxconsole.service_registerer import ArtnetServiceRegisterer
from advanceddmxconsole.gui.gui import GUI


logging.basicConfig(level=logging.INFO)


class Main:
    def __init__(self):
        self.service_repository = ServiceRepository()
        self.service_repository.register(MIDIServiceRegisterer)
        # Register last to ensure Variable initialization will happen last
        artnet_service = self.service_repository.register(ArtnetServiceRegisterer)

        self.gui = GUI(artnet_components=artnet_service.components)

    def exec(self):
        self.gui.exec_in_thead()
        self.service_repository.exec()


if __name__ == '__main__':
    Main().exec()
