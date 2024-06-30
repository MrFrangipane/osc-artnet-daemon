from oscartnetdaemon.components.midi.configuration_loader import MIDIConfigurationLoader
from oscartnetdaemon.components.midi.io.io import MIDIIO
from oscartnetdaemon.components.midi.variable.button import MIDIButton
from oscartnetdaemon.components.midi.variable.fader import MIDIFader
from oscartnetdaemon.components.midi.variable.text import MIDIText

from oscartnetdaemon.domain_contract.abstract_service_registerer import AbstractServiceRegisterer
from oscartnetdaemon.domain_contract.service_registration_info import ServiceRegistrationInfo
from oscartnetdaemon.domain_contract.variable_type_enum import VariableType


class MIDIServiceRegisterer(AbstractServiceRegisterer):

    @staticmethod
    def make_registration_info() -> ServiceRegistrationInfo:
        midi_configuration_loader = MIDIConfigurationLoader()

        return ServiceRegistrationInfo(
            configuration_loader=midi_configuration_loader,
            io_type=MIDIIO,
            variable_types={
                VariableType.Button: MIDIButton,
                VariableType.Fader: MIDIFader,
                VariableType.Text: MIDIText
            }
        )
