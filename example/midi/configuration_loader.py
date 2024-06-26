import mido
import yaml

from oscartnetdaemon.domain_contract.abstract_configuration_loader import AbstractConfigurationLoader
from oscartnetdaemon.components.new_midi.variable_info import MIDIVariableInfo
from oscartnetdaemon.components.new_midi.configuration import MIDIConfiguration
from oscartnetdaemon.components.new_midi.io.device_info import MIDIDeviceInfo


def _find_in_list(item: str, items: list[str]) -> str:
    for item_ in items:
        if item in item_:
            return item_

    return ""


class MIDIConfigurationLoader(AbstractConfigurationLoader):

    def __init__(self, filepath):
        super().__init__(filepath)

    def load(self) -> MIDIConfiguration:
        in_port_names = mido.get_input_names()
        out_port_names = mido.get_output_names()

        with open(self.filepath, 'r') as file:
            content = yaml.safe_load(file)

        device_infos: dict[str, MIDIDeviceInfo] = dict()
        variable_infos: list[MIDIVariableInfo] = list()
        for device in content['devices']:
            in_port_name = _find_in_list(device['midi-port-pattern'], in_port_names)
            if not in_port_name:
                print(f"MIDI Device '{device['name']}' not found")
                continue

            out_port_name = _find_in_list(device['midi-port-pattern'], out_port_names)

            device_infos[device['name']] = MIDIDeviceInfo(
                name=device['name'],
                in_port_name=in_port_name,
                out_port_name=out_port_name
            )

            for variable_dict in device['variables']:
                variable_dict['device_name'] = device['name']
                variable_infos.append(MIDIVariableInfo.from_dict(variable_dict))

        return MIDIConfiguration(
            devices=device_infos,
            variable_infos=variable_infos
        )
