import logging

from zeroconf import ServiceBrowser, ServiceStateChange, Zeroconf

from oscartnetdaemon.python_extensions.network import bytes_as_ip

_logger = logging.getLogger(__name__)


class DiscoveryClients:
    _zeroconf_service = "_osc._udp.local."

    def __init__(self):
        self._browser: ServiceBrowser = None
        self._zeroconf = Zeroconf()

    def start(self):
        _logger.info("Starting clients discovery...")
        self._browser = ServiceBrowser(
            self._zeroconf, self._zeroconf_service,
            handlers=[self._on_service_change]
        )
        _logger.info("Clients discovery started")

    def stop(self):
        self._zeroconf.close()
        _logger.info("Clients discovery stopped")

    @staticmethod
    def _on_service_change(zeroconf: Zeroconf, service_type: str, name: str, state_change: ServiceStateChange):
        info = zeroconf.get_service_info(service_type, name)
        if info is None:
            return

        if state_change is ServiceStateChange.Added:
            # fixme: check if IP and port are the same as Discovery Server
            _logger.info(f"Registering Client '{info.name.split('.')[0]}' at {bytes_as_ip(info.addresses[0])}")
            # info.addresses[0],  # FIXME compare to server address mask ?
            # info.properties[b'IID'],
            # info.name.split('.')[0],
            # info.port

        elif state_change is ServiceStateChange.Removed:
            _logger.info(f"Unregistering Client {info.name.split('.')[0]} at {info.addresses[0]}")
