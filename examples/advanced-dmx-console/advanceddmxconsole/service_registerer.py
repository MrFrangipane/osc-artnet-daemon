from oscartnetdaemon.domain_contract.abstract_service_registerer import AbstractServiceRegisterer
from oscartnetdaemon.domain_contract.service_registration_info import ServiceRegistrationInfo
from oscartnetdaemon.domain_contract.variable_type_enum import VariableType

from advanceddmxconsole.configuration_loader import ArtnetConfigurationLoader
from advanceddmxconsole.io.io import ArtnetIO
from advanceddmxconsole.shared_data import ArtnetSharedData
from advanceddmxconsole.variable.button import ArtnetButton
from advanceddmxconsole.variable.fader import ArtnetFader
from advanceddmxconsole.variable.indicator import ArtnetIndicator


class ArtnetServiceRegisterer(AbstractServiceRegisterer):

    @staticmethod
    def make_registration_info() -> ServiceRegistrationInfo:
        configuration_loader = ArtnetConfigurationLoader()
        return ServiceRegistrationInfo(
            configuration_loader=configuration_loader,
            io_type=ArtnetIO,
            variable_types={
                VariableType.Fader: ArtnetFader,
                VariableType.Button: ArtnetButton,
                VariableType.Indicator: ArtnetIndicator
            },
            shared_data_type=ArtnetSharedData
            # variable_repository_type=ArtnetVariableRepository  TODO
        )
