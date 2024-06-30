from oscartnetdaemon.components.osc.argument_parser import parse_command_line_args
from oscartnetdaemon.components.osc.configuration_loader import OSCConfigurationLoader
from oscartnetdaemon.components.osc.io.io import OSCIO
from oscartnetdaemon.components.osc.variable.fader import OSCFader
from oscartnetdaemon.components.osc.variable.recall_slot import OSCRecallSlot


from oscartnetdaemon.domain_contract.abstract_service_registerer import AbstractServiceRegisterer
from oscartnetdaemon.domain_contract.service_registration_info import ServiceRegistrationInfo
from oscartnetdaemon.domain_contract.variable_type_enum import VariableType


class OSCServiceRegisterer(AbstractServiceRegisterer):

    @staticmethod
    def make_registration_info() -> ServiceRegistrationInfo:
        osc_configuration_loader = OSCConfigurationLoader(filepaths=parse_command_line_args())
        return ServiceRegistrationInfo(
            configuration_loader=osc_configuration_loader,
            io_type=OSCIO,
            variable_types={
                VariableType.Fader: OSCFader,
                VariableType.RecallSlot: OSCRecallSlot
            }
        )
