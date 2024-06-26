import mido
import yaml

from oscartnetdaemon.components.new_midi.configuration import MIDIConfiguration
from oscartnetdaemon.components.new_midi.io.device_info import MIDIDeviceInfo
from oscartnetdaemon.components.new_midi.variable_info import MIDIVariableInfo
from oscartnetdaemon.domain_contract.abstract_configuration_loader import AbstractConfigurationLoader


def _find_in_list(item: str, items: list[str]) -> str:
    for item_ in items:
        if item in item_:
            return item_

    return ""


class MIDIConfigurationLoader(AbstractConfigurationLoader):

    def __init__(self, filepaths):
        super().__init__(filepaths)

        self.in_port_names: list[str] = list()
        self.out_port_names: list[str] = list()

        self.content = dict()

        self.device_infos: dict[str, MIDIDeviceInfo] = dict()
        self.variable_infos: list[MIDIVariableInfo] = list()

    def load_devices(self):
        for device in self.content.get('devices', list()):
            in_port_name = _find_in_list(device['midi-port-pattern'], self.in_port_names)
            if not in_port_name:
                print(f"MIDI Device '{device['name']}' not found")
                continue

            out_port_name = _find_in_list(device['midi-port-pattern'], self.out_port_names)

            self.device_infos[device['name']] = MIDIDeviceInfo(
                name=device['name'],
                in_port_name=in_port_name,
                out_port_name=out_port_name
            )

            self.load_device_variables(device)

    def load_device_variables(self, device):
        for variable_dict in device['variables']:
            variable_dict['device_name'] = device['name']
            self.variable_infos.append(MIDIVariableInfo.from_dict(variable_dict))

    def load(self) -> MIDIConfiguration:
        self.in_port_names = mido.get_input_names()
        self.out_port_names = mido.get_output_names()

        for filepath in self.filepaths:
            with open(filepath, 'r') as file:
                self.content = yaml.safe_load(file)

            self.load_devices()

        return MIDIConfiguration(
            devices=self.device_infos,
            variable_infos=self.variable_infos
        )
