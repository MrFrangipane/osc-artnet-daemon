import logging
import time

from oscartnetdaemon.components.components_singleton import Components
from oscartnetdaemon.components.configuration.loader import ConfigurationLoader
from oscartnetdaemon.components.discovery.service import DiscoveryService
from oscartnetdaemon.components.osc.service import OSCService


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    ConfigurationLoader.load_from_file('./resources/template-widgets-mapping.yml')

    Components().osc_service = OSCService()
    Components().osc_service.start()

    discovery_service = DiscoveryService(
        server_name="Frangitron's OSC Artnet",
        server_port=8080
    )
    discovery_service.start()

    try:
        while True:
            time.sleep(.1)
    except KeyboardInterrupt:
        discovery_service.stop()
        # osc_service.stop()
