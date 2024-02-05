import logging

from stupidArtnet import StupidArtnet

_logger = logging.getLogger(__name__)


class ArtNetServer:

    def __init__(self):
        self._stupid_artnet: StupidArtnet = None

    def start(self, target_node_ip, universe_number):
        self._stupid_artnet = StupidArtnet(target_ip=target_node_ip, universe=universe_number, fps=40)
        self._stupid_artnet.start()
        _logger.info(f"ArtNetServer started (target_node_ip={target_node_ip}, universe_number={universe_number})")

    def stop(self):
        self._stupid_artnet.blackout()
        self._stupid_artnet.stop()
        self._stupid_artnet.close()

    def set_universe(self, universe: bytearray):
        self._stupid_artnet.set(universe)
