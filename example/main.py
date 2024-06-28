from oscartnetdaemon.components.service_repository import ServiceRepository
from oscartnetdaemon.domain_contract.service_registration_info import ServiceRegistrationInfo
from oscartnetdaemon.domain_contract.variable_type_enum import VariableType

from midi.configuration_loader import MIDIConfigurationLoader
from midi.io.io import MIDIIO
from midi.variable.float import MIDIFloat
from osc.configuration_loader import OSCConfigurationLoader
from osc.io.io import OSCIO
from osc.variable.float import OSCFloat


if __name__ == '__main__':
    main = ServiceRepository()

    osc_configuration_loader = OSCConfigurationLoader(filepath="configuration/osc.yml")
    main.register(ServiceRegistrationInfo(
        configuration_loader=osc_configuration_loader,
        io_type=OSCIO,
        variable_types={
            VariableType.Float: OSCFloat
        }
    ))

    midi_configuration_loader = MIDIConfigurationLoader(filepath="configuration/midi.yml")
    main.register(ServiceRegistrationInfo(
        configuration_loader=midi_configuration_loader,
        io_type=MIDIIO,
        variable_types={
            VariableType.Float: MIDIFloat
        }
    ))

    main.exec()
