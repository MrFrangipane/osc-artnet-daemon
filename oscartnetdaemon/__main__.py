import logging

from oscartnetdaemon.components.components_singleton import Components
from oscartnetdaemon.components.configuration.loader import ConfigurationLoader
# from oscartnetdaemon.components.discovery.service import DiscoveryService
from oscartnetdaemon.components.domain.service import DomainService
from oscartnetdaemon.components.midi.service import MIDIService
from oscartnetdaemon.components.osc.service import OSCService


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    ConfigurationLoader.load_from_file('./resources/tmrld24.yml')

    # discovery_service = DiscoveryService(
    #     server_name="Frangitron's OSC Artnet",
    #     server_port=8080
    # )
    # discovery_service.start()

    Components().domain_service = DomainService(Components().configuration_info)  # FIXME: use a configuration singleton ?
    Components().domain_service.create_controls(Components().domain_control_infos)
    Components().domain_service.register_implementation_type(MIDIService)
    Components().domain_service.register_implementation_type(OSCService)

    try:
        Components().domain_service.run_forever()
    except KeyboardInterrupt:
        # discovery_service.stop()
        Components().domain_service.stop()
