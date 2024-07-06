import logging

from oscartnetdaemon.components.midi.service_registerer import MIDIServiceRegisterer
from oscartnetdaemon.components.service_repository import ServiceRepository

from advanceddmxconsole.service_registerer import ArtnetServiceRegisterer


logging.basicConfig(level=logging.INFO)


if __name__ == '__main__':
    service_repository = ServiceRepository()

    service_repository.register(MIDIServiceRegisterer)

    # Register last to ensure Variable initialization will happen last
    service_repository.register(ArtnetServiceRegisterer)

    service_repository.exec()
