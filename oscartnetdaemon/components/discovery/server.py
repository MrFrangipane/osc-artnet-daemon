import logging
import socket

from zeroconf import ServiceInfo, Zeroconf

from oscartnetdaemon.python_extensions.network import detect_local_ip, ip_as_bytes

_logger = logging.getLogger(__name__)


class DiscoveryServer:
    _zeroconf_service_type = "_osc._udp.local."

    def __init__(self, name: str, port: int):
        self.name = name
        self.port = port
        self._service_info: ServiceInfo = None
        self._zeroconf: Zeroconf = None

    def start(self):
        _logger.info(f"Starting Discovery server...")

        local_ip = detect_local_ip()
        _logger.info(f"Detected local IP address {local_ip}")

        self._service_info = ServiceInfo(
            type_=self._zeroconf_service_type,
            name=f"{self.name}.{self._zeroconf_service_type}",
            addresses=[ip_as_bytes(local_ip)],
            port=self.port,
            properties={'description': 'My Test Service'}
        )
        self._zeroconf = Zeroconf()
        self._zeroconf.register_service(self._service_info)

        _logger.info(f"Discovery server started")

    def stop(self):
        self._zeroconf.unregister_service(self._service_info)
        self._zeroconf.close()
        _logger.info(f"Discovery server stopped")
