from oscartnetdaemon.components.midi.service_registerer import MIDIServiceRegisterer
from oscartnetdaemon.components.osc.service_registerer import OSCServiceRegisterer
from oscartnetdaemon.components.service_repository import ServiceRepository

from advanceddmxconsole.artnet.service_registerer import ArtnetServiceRegisterer


if __name__ == '__main__':
    service_repository = ServiceRepository()

    service_repository.register(MIDIServiceRegisterer)
    # service_repository.register(OSCServiceRegisterer)

    # Register last to ensure Variable updates will happen last
    service_repository.register(ArtnetServiceRegisterer)

    service_repository.exec()
