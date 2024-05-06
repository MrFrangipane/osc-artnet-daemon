import logging
import time

from oscartnetdaemon.components.discovery.service import DiscoveryService
from oscartnetdaemon.components.osc.service import OSCService


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    # fixme: load a configuration object from file(s), use a Singleton to access it from components

    discovery_service = DiscoveryService(
        server_name="Frangitron's OSC Artnet",
        server_port=8080
    )
    discovery_service.start()

    osc_service = OSCService()
    osc_service.initialize_from_file('./resources/template-widgets-mapping.yml')
    osc_service.start()

    try:
        while True:
            time.sleep(.1)
    except KeyboardInterrupt:
        discovery_service.stop()
        # osc_service.stop()
