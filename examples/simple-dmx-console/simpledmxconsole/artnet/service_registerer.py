from oscartnetdaemon.domain_contract.abstract_service_registerer import AbstractServiceRegisterer
from oscartnetdaemon.domain_contract.service_registration_info import ServiceRegistrationInfo
from oscartnetdaemon.domain_contract.variable_type_enum import VariableType

from simpledmxconsole.artnet.configuration_loader import ArtnetConfigurationLoader
from simpledmxconsole.artnet.io.io import ArtnetIO
from simpledmxconsole.artnet.variable.fader import ArtnetFader


class ArtnetServiceRegisterer(AbstractServiceRegisterer):

    @staticmethod
    def make_registration_info() -> ServiceRegistrationInfo:
        configuration_loader = ArtnetConfigurationLoader()
        return ServiceRegistrationInfo(
            configuration_loader=configuration_loader,
            io_type=ArtnetIO,
            variable_types={
                VariableType.Fader: ArtnetFader
            }
        )
