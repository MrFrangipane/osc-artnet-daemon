from oscartnetdaemon.domain_contract.abstract_service_registerer import AbstractServiceRegisterer
from oscartnetdaemon.domain_contract.service_registration_info import ServiceRegistrationInfo
from oscartnetdaemon.domain_contract.variable_type_enum import VariableType

from advanceddmxconsole.artnet.io.io import ArtnetIO
from advanceddmxconsole.artnet.variable.button import ArtnetButton
from advanceddmxconsole.artnet.variable.fader import ArtnetFader
from advanceddmxconsole.configuration_loader import ArtnetConfigurationLoader
from advanceddmxconsole.variable_repository import ArtnetVariableRepository


class ArtnetServiceRegisterer(AbstractServiceRegisterer):

    @staticmethod
    def make_registration_info() -> ServiceRegistrationInfo:
        configuration_loader = ArtnetConfigurationLoader()
        return ServiceRegistrationInfo(
            configuration_loader=configuration_loader,
            io_type=ArtnetIO,
            variable_types={
                VariableType.Fader: ArtnetFader,
                VariableType.Button: ArtnetButton
            },
            variable_repository_type=ArtnetVariableRepository
        )
