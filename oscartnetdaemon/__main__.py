import logging

from oscartnetdaemon.components.components_singleton import Components
from oscartnetdaemon.components.configuration.loader import ConfigurationLoader
from oscartnetdaemon.components.discovery.service import DiscoveryService
from oscartnetdaemon.components.domain.service import DomainService
from oscartnetdaemon.components.midi.service import MIDIService
from oscartnetdaemon.components.osc.service import OSCService


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    ConfigurationLoader.load_from_file('./resources/tmrld24.yml')

    discovery_service = DiscoveryService(
        server_name="Frangitron's OSC Artnet",
        server_port=8080
    )

    Components().domain_service = DomainService(Components().configuration_info)  # FIXME: use a configuration singleton ?
    Components().domain_service.create_controls(Components().domain_control_infos)

    Components().domain_service.register_implementation_type(MIDIService)

    Components().domain_service.register_implementation_type(OSCService)
    Components().osc_service = Components().domain_service.implementation_repository.get_implementation(OSCService)
    Components().osc_service.initialize()

    discovery_service.start()

    try:
        Components().domain_service.run_forever()
    except KeyboardInterrupt:
        discovery_service.stop()
        Components().domain_service.stop()
