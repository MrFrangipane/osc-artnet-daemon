from yourproject.template.configuration_loader import TemplateConfigurationLoader
from yourproject.template.io.io import TemplateIO
from yourproject.template.variable.fader import TemplateFader

from oscartnetdaemon.domain_contract.abstract_service_registerer import AbstractServiceRegisterer
from oscartnetdaemon.domain_contract.service_registration_info import ServiceRegistrationInfo
from oscartnetdaemon.domain_contract.variable_type_enum import VariableType


class TemplateServiceRegisterer(AbstractServiceRegisterer):

    @staticmethod
    def make_registration_info() -> ServiceRegistrationInfo:
        configuration_loader = TemplateConfigurationLoader()
        return ServiceRegistrationInfo(
            configuration_loader=configuration_loader,
            io_type=TemplateIO,
            variable_types={
                VariableType.Fader: TemplateFader
            }
        )
