from oscartnetdaemon.components.main import Main

from oscartnetdaemon.domain_contract.service_registration_info import ServiceRegistrationInfo
from oscartnetdaemon.domain_contract.variable_type_enum import VariableType

from oscartnetdaemon.components.new_midi.configuration_loader import MIDIConfigurationLoader
from oscartnetdaemon.components.new_midi.io.io import MIDIIO
from oscartnetdaemon.components.new_midi.variable.fader import MIDIFader

from oscartnetdaemon.components.new_osc.configuration_loader import OSCConfigurationLoader
from oscartnetdaemon.components.new_osc.io.io import OSCIO
from oscartnetdaemon.components.new_osc.variable.fader import OSCFader


if __name__ == '__main__':
    main = Main()

    # TODO create an interface to allow implementation of this in one line
    osc_configuration_loader = OSCConfigurationLoader(filepaths=[
        "resources/develop/osc.yml"
    ])
    main.register_io_service(ServiceRegistrationInfo(
        configuration_loader=osc_configuration_loader,
        io_type=OSCIO,
        variable_types={
            VariableType.Fader: OSCFader
        }
    ))

    # TODO create an interface to allow implementation of this in one line
    midi_configuration_loader = MIDIConfigurationLoader(filepaths=[
        "resources/develop/midi-devices.yml",
        "resources/develop/midi-pages.yml",
        "resources/develop/midi-layer-groups.yml"
    ])
    main.register_io_service(ServiceRegistrationInfo(
        configuration_loader=midi_configuration_loader,
        io_type=MIDIIO,
        variable_types={
            VariableType.Fader: MIDIFader
        }
    ))

    main.exec()
