import logging

from oscartnetdaemon.components.midi.service_registerer import MIDIServiceRegisterer
from oscartnetdaemon.components.osc.service_registerer import OSCServiceRegisterer
from oscartnetdaemon.components.qusb.service_registerer import QuSbServiceRegisterer
from oscartnetdaemon.components.service_repository import ServiceRepository

from yourproject.template.service_registerer import TemplateServiceRegisterer


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    service_repository = ServiceRepository()

    # service_repository.register(MIDIServiceRegisterer)
    # service_repository.register(OSCServiceRegisterer)
    service_repository.register(QuSbServiceRegisterer)

    # service_repository.register(TemplateServiceRegisterer)

    service_repository.exec()
