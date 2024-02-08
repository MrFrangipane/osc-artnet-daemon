import logging

from stupidArtnet import StupidArtnet

_logger = logging.getLogger(__name__)


class ArtnetServer:

    def __init__(self, target_node_ip, universe_number):
        self.target_node_ip = target_node_ip
        self.universe_number = universe_number
        self._stupid_artnet: StupidArtnet = None

    def start(self):
        _logger.info("Starting Artnet server")
        self._stupid_artnet = StupidArtnet(target_ip=self.target_node_ip, universe=self.universe_number, fps=40)
        self._stupid_artnet.start()
        _logger.info(f"ArtnetServer started (target_node_ip={self.target_node_ip}, universe_number={self.universe_number})")

    def set_universe(self, universe: bytearray):
        self._stupid_artnet.set(universe)

    def stop(self):
        self._stupid_artnet.stop()
        self._stupid_artnet.close()
        _logger.info("Artnet server stopped")
