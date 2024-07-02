import logging
import socket

from stupidArtnet import StupidArtnet

from oscartnetdaemon.python_extensions.network import ping

_logger = logging.getLogger(__name__)


class ArtnetServer:

    def __init__(self):
        self.target_node: str = "192.168.20.12"
        self.target_node_ip: str = ""
        self.universe_number = 1
        self._stupid_artnet: StupidArtnet | None = None
        self._is_running = False

    def start(self):
        try:
            self.target_node_ip = socket.gethostbyname(self.target_node)
            if self.target_node_ip != self.target_node:
                _logger.info(f"Found target node ip address '{self.target_node}' {self.target_node_ip}")
            else:
                if not ping(self.target_node_ip):
                    _logger.warning(f"Target node ip address doesn't respond to ping '{self.target_node}'")
                    _logger.warning(f"Server not started '{self.target_node}'")
                    return
        except socket.gaierror:
            _logger.warning(f"Target node ip address not found '{self.target_node}'")
            _logger.warning(f"Server not started '{self.target_node}'")
            return

        self._stupid_artnet = StupidArtnet(target_ip=self.target_node_ip, universe=self.universe_number, fps=40)
        self._stupid_artnet.start()
        _logger.info(f"ArtnetServer started {self.target_node_ip} for universe {self.universe_number}")
        self._is_running = True

    def set_universe(self, universe: bytearray):
        if self._is_running:
            self._stupid_artnet.set(universe)

    def stop(self):
        if self._is_running:
            self._is_running = False
            self._stupid_artnet.stop()
            self._stupid_artnet.close()
            _logger.info(f"Artnet server stopped '{self.target_node}'")
        else:
            _logger.info(f"Artnet was server started '{self.target_node}'")
