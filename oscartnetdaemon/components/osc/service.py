from queue import Queue
from threading import Thread

from pythonosc.osc_server import ThreadingOSCUDPServer

from oscartnetdaemon.components.components_singleton import Components
from oscartnetdaemon.components.osc.dispatcher_configurer import OSCDispatcherConfigurer
from oscartnetdaemon.components.osc.message_handler import OSCMessageHandler
from oscartnetdaemon.components.osc.message_queue_item import OSCMessageQueueItem
from oscartnetdaemon.components.osc.message_queue_item_sender import OSCMessageQueueItemSender


class OSCService:

    def __init__(self):
        self.clients_pool: OSCMessageQueueItemSender = None
        self.message_queue: Queue[OSCMessageQueueItem] = Queue()
        self.dispatcher_configurer: OSCDispatcherConfigurer = None
        self.message_handler: OSCMessageHandler = None
        self.server: ThreadingOSCUDPServer = None

        self._server_thread: Thread = None
        self._clients_pool_thread: Thread = None

    def _initialize(self):
        configuration = Components().osc_configuration

        self.message_handler = OSCMessageHandler(message_queue=self.message_queue)
        self.dispatcher_configurer = OSCDispatcherConfigurer(self.message_handler)
        self.dispatcher_configurer.load(configuration.widgets)

        address = configuration.server_ip_address
        port = configuration.server_port
        self.server = ThreadingOSCUDPServer(
            server_address=(address, port),
            dispatcher=self.dispatcher_configurer.dispatcher
        )
        self.clients_pool = OSCMessageQueueItemSender(message_queue=self.message_queue)

    def start(self):
        self._initialize()

        self._server_thread: Thread = Thread(target=self.server.serve_forever, daemon=True)
        self._server_thread.start()

        self._clients_pool_thread: Thread = Thread(target=self.clients_pool.start, daemon=True)
        self._clients_pool_thread.start()

    def stop(self):
        raise NotImplementedError()
