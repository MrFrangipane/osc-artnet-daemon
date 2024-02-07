import time
import logging

from zeroconf import ServiceBrowser, ServiceStateChange, Zeroconf

from oscartnetdaemon.components.discovery.abstract import AbstractDiscovery
from oscartnetdaemon.core.components import Components
from oscartnetdaemon.core.osc_client_info import OSCClientInfo

_logger = logging.getLogger(__name__)


class Discovery(AbstractDiscovery):
    _zeroconf_service = "_osc._udp.local."

    def __init__(self, address_mask):
        super().__init__(address_mask)
        self._zeroconf = Zeroconf()
        self._browser: ServiceBrowser = None
        self._is_running = False

    def start(self):
        _logger.info("Discovery service starting...")
        self._browser = ServiceBrowser(
            self._zeroconf, self._zeroconf_service,
            handlers=[self._on_service_change]
        )

        self._is_running = True
        while self._is_running:
            time.sleep(1)

    def stop(self):
        self._is_running = False
        self._zeroconf.close()
        _logger.info("Discovery service stopped")

    @staticmethod
    def _on_service_change(zeroconf: Zeroconf, service_type: str, name: str, state_change: ServiceStateChange):
        info = zeroconf.get_service_info(service_type, name)
        if info is None:
            return

        if state_change is ServiceStateChange.Added:
            Components().osc_message_sender.create_client(OSCClientInfo(
                address=info.addresses[0],  # FIXME compare to server address mask ?
                id=info.properties[b'IID'],
                name=info.name.split('.')[0],
                port=info.port
            ))

        elif state_change is ServiceStateChange.Removed:
            Components().osc_message_sender.delete_client(info.properties[b'IID'])
