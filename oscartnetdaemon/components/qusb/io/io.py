import logging
import time

from multiprocessing import Event, Process

from oscartnetdaemon.domain_contract.abstract_io import AbstractIO
from oscartnetdaemon.domain_contract.service_components import ServiceComponents
from oscartnetdaemon.components.qusb.io.message import QuSbIOMessage
from oscartnetdaemon.components.qusb.io.device import QuSbDevice


_logger = logging.getLogger(__name__)


class QuSbIO(AbstractIO):

    def __init__(self, components: ServiceComponents):
        super().__init__(components)
        self.components: ServiceComponents = components  # FIXME: circular import forbids type hinting, maybe a singleton ?
        self.should_stop: Event | None = None

    def start(self):
        """
        Start IO loop without blocking, deal with in and out queues
        If needed, initialize variables values
        (broadcast happens after all services are started, in service registration order)
        """
        self.should_stop = Event()
        self.device = QuSbDevice(
            host=self.components.configuration.host,
            port=self.components.configuration.port,
            queue_in=self.components.io_message_queue_in,
            should_stop=self.should_stop
        )
        self.device.start()

    def shutdown(self):
        """
        Gracefully shutdown all IO, Thread, Process, ... that start() may have opened
        """
        self.should_stop.set()
        while self.device.is_alive():
            time.sleep(0.01)

        _logger.info("Shut down")

    def send_io_message(self, message: QuSbIOMessage):
        self.device.queue_out.put(message)
