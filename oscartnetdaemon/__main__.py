from oscartnetdaemon.components.main import Main

from oscartnetdaemon.components.new_midi.configuration_loader import MIDIConfigurationLoader
from oscartnetdaemon.components.new_midi.io.io import MIDIIO
from oscartnetdaemon.components.new_midi.variable.float import MIDIFloat
from oscartnetdaemon.components.new_osc.configuration_loader import OSCConfigurationLoader
from oscartnetdaemon.components.new_osc.io.io import OSCIO
from oscartnetdaemon.components.new_osc.variable.float import OSCFloat
from oscartnetdaemon.domain_contract.service_registration_info import ServiceRegistrationInfo
from oscartnetdaemon.domain_contract.variable_type_enum import VariableType


if __name__ == '__main__':
    main = Main()

    osc_configuration_loader = OSCConfigurationLoader(filepath="resources/develop/osc.yml")
    main.register_io_service(ServiceRegistrationInfo(
        configuration_loader=osc_configuration_loader,
        io_type=OSCIO,
        variable_types={
            VariableType.Float: OSCFloat
        }
    ))

    midi_configuration_loader = MIDIConfigurationLoader(filepath="resources/develop/midi.yml")
    main.register_io_service(ServiceRegistrationInfo(
        configuration_loader=midi_configuration_loader,
        io_type=MIDIIO,
        variable_types={
            VariableType.Float: MIDIFloat
        }
    ))

    main.exec()
