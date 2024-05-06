import logging

from zeroconf import ServiceBrowser, ServiceStateChange, Zeroconf

from oscartnetdaemon.components.components_singleton import Components
from oscartnetdaemon.entities.osc.client_info import OSCClientInfo

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
            if b'IID' not in info.properties:
                return

            Components().osc_service.register_client(OSCClientInfo(
                address=info.addresses[0],
                id=info.properties[b'IID'],
                name=info.name.split('.')[0],
                port=info.port
            ))

        elif state_change is ServiceStateChange.Removed:
            Components().osc_service.unregister_client(OSCClientInfo(
                address=info.addresses[0],
                id=info.properties[b'IID'],
                name=info.name.split('.')[0],
                port=info.port
            ))
