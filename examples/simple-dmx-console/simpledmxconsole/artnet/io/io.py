from oscartnetdaemon.domain_contract.abstract_io import AbstractIO
from oscartnetdaemon.domain_contract.service_components import ServiceComponents

from simpledmxconsole.artnet.io.artnet_server import ArtnetServer
from simpledmxconsole.artnet.io.message import ArtnetIOMessage
from simpledmxconsole.fixture.fixture_repository import FixtureRepository


class ArtnetIO(AbstractIO):

    def __init__(self, components: ServiceComponents):
        super().__init__(components)
        self.components: ServiceComponents = components  # FIXME: circular import forbids type hinting, maybe a singleton ?

        self.server = ArtnetServer()
        self.universe = bytearray(512)

        self.fixture_repository = FixtureRepository()

    def start(self):
        """
        Start IO loop without blocking, deal with in and out queues
        If needed, initialize variables values
        (broadcast happens after all services are started, in service registration order)
        """
        variables = list(self.components.variable_repository.variables.values())
        for fixture in self.fixture_repository.fixtures:
            for channel in fixture.channels:
                variable = variables[channel.channel_number - 1]
                variable.info.caption = channel.function
                variable.value.value = float(channel.value_default / 255.0)

        self.server.start()

    def shutdown(self):
        """
        Gracefully shutdown all IO, Thread, Process, ... that start() may have opened
        """
        self.server.stop()

    def send_io_message(self, message: ArtnetIOMessage):
        self.universe[message.channel] = message.value
        self.server.set_universe(self.universe)
