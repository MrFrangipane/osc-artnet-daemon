from oscartnetdaemon.components.qusb.configuration_loader import QuSbConfigurationLoader
from oscartnetdaemon.components.qusb.io.io import QuSbIO
from oscartnetdaemon.components.qusb.variable.fader import QuSbFader

from oscartnetdaemon.domain_contract.abstract_service_registerer import AbstractServiceRegisterer
from oscartnetdaemon.domain_contract.service_registration_info import ServiceRegistrationInfo
from oscartnetdaemon.domain_contract.variable_type_enum import VariableType


class QuSbServiceRegisterer(AbstractServiceRegisterer):

    @staticmethod
    def make_registration_info() -> ServiceRegistrationInfo:
        configuration_loader = QuSbConfigurationLoader()
        return ServiceRegistrationInfo(
            configuration_loader=configuration_loader,
            io_type=QuSbIO,
            variable_types={
                VariableType.Fader: QuSbFader
            }
        )
