import logging

from oscartnetdaemon.domain_contract.abstract_io import AbstractIO
from oscartnetdaemon.domain_contract.service_components import ServiceComponents

from advanceddmxconsole.io.artnet_server import ArtnetServer
from advanceddmxconsole.io.message import ArtnetIOMessage
from advanceddmxconsole.configuration import ArtnetConfiguration
from advanceddmxconsole.advanced_dmx_console import AdvancedDmxConsole


_logger = logging.getLogger(__name__)


class ArtnetIO(AbstractIO):  # FIXME create an interface mixin with set_universe(universe)

    def __init__(self, components: ServiceComponents):
        super().__init__(components)
        self.components: ServiceComponents = components  # FIXME: circular import forbids type hinting, maybe a singleton ?
        self.servers: list[ArtnetServer] = list()
        self._is_bypass: bool = False
        self.universe = bytearray(512)

    def set_bypass(self, is_bypass: bool):
        if is_bypass != self._is_bypass:
            self._is_bypass = is_bypass

            if is_bypass:
                self.shutdown()
            else:
                self.start_servers()

    def start(self):
        """
        Start IO loop without blocking, deal with in and out queues
        If needed, initialize variables values
        (broadcast happens after all services are started, in service registration order)
        """
        _logger.info("Starting")
        self.start_servers()

        # Initialize after servers are started (to send default fixtures values)
        AdvancedDmxConsole().initialize(self, self.components)  # FIXME hack to give self instead of IO

    def set_universe(self, universe: bytearray):
        self.universe = universe
        for server in self.servers:
            server.set_universe(universe)

    def start_servers(self):
        configuration: ArtnetConfiguration = self.components.configuration

        for target_node in configuration.target_nodes:
            new_server = ArtnetServer(
                target_node=target_node,
                universe_number=configuration.universe
            )
            new_server.start()
            new_server.set_universe(self.universe)
            self.servers.append(new_server)

    def shutdown(self):
        """
        Gracefully shutdown all IO, Thread, Process, ... that start() may have opened
        """
        for server in self.servers:
            server.stop()

    def send_io_message(self, message: ArtnetIOMessage):
        pass
