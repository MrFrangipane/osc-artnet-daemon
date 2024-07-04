import logging

from oscartnetdaemon.components.midi.service_registerer import MIDIServiceRegisterer
from oscartnetdaemon.components.osc.service_registerer import OSCServiceRegisterer
from oscartnetdaemon.components.service_repository import ServiceRepository


logging.basicConfig(level=logging.INFO)


if __name__ == '__main__':
    service_repository = ServiceRepository()

    service_repository.register(MIDIServiceRegisterer)
    service_repository.register(OSCServiceRegisterer)

    service_repository.exec()
