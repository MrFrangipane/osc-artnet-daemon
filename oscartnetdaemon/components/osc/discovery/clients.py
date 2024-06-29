import logging

from zeroconf import ServiceBrowser, ServiceStateChange, Zeroconf

from oscartnetdaemon.components.osc.client_info import OSCClientInfo
# FIXME circular import
# from oscartnetdaemon.components.new_osc.io.io import OSCIO

_logger = logging.getLogger(__name__)


class OSCDiscoveryClients:
    _zeroconf_service = "_osc._udp.local."

    def __init__(self, io):
        self._io = io
        self._browser: ServiceBrowser | None = None
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

    def _on_service_change(self, zeroconf: Zeroconf, service_type: str, name: str, state_change: ServiceStateChange):
        info = zeroconf.get_service_info(service_type, name)
        if info is None:
            return

        if state_change is ServiceStateChange.Added:
            if b'IID' not in info.properties:
                return

            self._io.register_client(OSCClientInfo(
                address=info.addresses[0],
                id=info.properties[b'IID'],
                name=info.name.split('.')[0],
                port=info.port
            ))

        elif state_change is ServiceStateChange.Removed:
            self._io.unregister_client(OSCClientInfo(
                address=info.addresses[0],
                id=info.properties[b'IID'],
                name=info.name.split('.')[0],
                port=info.port
            ))
