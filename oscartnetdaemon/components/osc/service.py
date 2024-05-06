from queue import Queue
from threading import Thread

import yaml
from pythonosc.osc_server import ThreadingOSCUDPServer

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

    def initialize_from_file(self, filepath: str):
        # fixme: create a configuration dataclass and a yaml loader for it
        with open(filepath, 'r') as yaml_file:
            yaml_content = yaml.safe_load(yaml_file)

        self.message_handler = OSCMessageHandler(message_queue=self.message_queue)

        self.dispatcher_configurer = OSCDispatcherConfigurer(self.message_handler)
        self.dispatcher_configurer.load(yaml_content['osc-mapping'])

        address = yaml_content['osc-server']['address']
        port = yaml_content['osc-server']['port']
        self.server = ThreadingOSCUDPServer(
            server_address=(address, port),
            dispatcher=self.dispatcher_configurer.dispatcher
        )
        self.clients_pool = OSCMessageQueueItemSender(message_queue=self.message_queue)

    def start(self):
        self._server_thread: Thread = Thread(target=self.server.serve_forever, daemon=True)
        self._server_thread.start()

        self._clients_pool_thread: Thread = Thread(target=self.clients_pool.start, daemon=True)
        self._clients_pool_thread.start()

    def stop(self):
        raise NotImplementedError()
