import logging
import time

from multiprocessing import Event, Process, Queue

from mido.sockets import BaseIOPort, connect
from mido.messages import Message

from oscartnetdaemon.domain_contract.abstract_io import AbstractIO
from oscartnetdaemon.domain_contract.service_components import ServiceComponents
from oscartnetdaemon.components.qusb.io.message import QuSbIOMessage
from oscartnetdaemon.components.qusb.constants import QuSbConstants


_logger = logging.getLogger(__name__)


def process(host: str, port: int, queue_in: "Queue[Message]", queue_out: "Queue[Message]", should_stop: Event):
    midi_tcp: BaseIOPort = connect(host, port)

    request_message = Message(
        type='sysex',
        data=QuSbConstants.SYSEX_REQUEST_STATE
    )
    midi_tcp.send(request_message)
    while True:
        message = midi_tcp.receive()
        print(message)
        if bytearray(message.bytes()[1:-1]) == QuSbConstants.SYSEX_REQUEST_STATE_END:
            break

    while not should_stop.is_set():
        message = midi_tcp.receive(block=False)
        if message is not None:
            queue_in.put(message)

        while not queue_out.empty():
            midi_tcp.send(queue_out.get())


class QuSbIO(AbstractIO):

    def __init__(self, components: ServiceComponents):
        super().__init__(components)
        self.components: ServiceComponents = components  # FIXME: circular import forbids type hinting, maybe a singleton ?
        self.should_stop: Event | None = None
        self.process: Process | None = None
        self.queue_in: Queue[Message] | None = None
        self.queue_out: Queue[Message] | None = None

    def start(self):
        """
        Start IO loop without blocking, deal with in and out queues
        If needed, initialize variables values
        (broadcast happens after all services are started, in service registration order)
        """
        self.should_stop = Event()

        self.queue_in = Queue()
        self.queue_out = Queue()

        self.process = Process(target=process, args=(
            self.components.configuration.host,
            self.components.configuration.port,
            self.queue_in,
            self.queue_out,
            self.should_stop
        ))
        self.process.start()

    def shutdown(self):
        """
        Gracefully shutdown all IO, Thread, Process, ... that start() may have opened
        """
        self.should_stop.set()
        while self.process.is_alive():
            time.sleep(0.01)

        _logger.info("Shut down")

    def send_io_message(self, message: QuSbIOMessage):
        pass
