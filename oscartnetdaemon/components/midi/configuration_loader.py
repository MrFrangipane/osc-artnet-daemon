import os.path

import mido
import yaml

from oscartnetdaemon.entities.midi.configuration import MIDIConfiguration
from oscartnetdaemon.entities.midi.control_info import MIDIControlInfo
from oscartnetdaemon.entities.midi.device_info import MIDIDeviceInfo
from oscartnetdaemon.entities.midi.layer_group_info import MIDIControlLayerGroupInfo
from oscartnetdaemon.entities.midi.layer_info import MIDIControlLayerInfo


def _find_in_list(item, items):
    for item_ in items:
        if item in item_:
            return item_

    raise ValueError(f"Not found '{item}'")


def load_midi_configuration(midi_devices: list[str], root_folder: str) -> MIDIConfiguration:
    in_port_names = mido.get_input_names()
    out_port_names = mido.get_output_names()

    devices = dict()
    controls = dict()
    layer_groups = dict()
    for filename in midi_devices:
        filepath = os.path.join(root_folder, filename)
        with open(filepath, 'r') as yaml_controls_file:
            yaml_content = yaml.safe_load(yaml_controls_file)

        for device_content in yaml_content['devices']:
            name = device_content['name']
            if name in devices:
                raise ValueError(f"MIDI device with name '{name}' already defined")

            pattern = device_content['midi_port_pattern']
            in_port_name = _find_in_list(pattern, in_port_names)
            out_port_name = _find_in_list(pattern, out_port_names)
            new_device = MIDIDeviceInfo(
                name=name,
                in_port_name=in_port_name,
                out_port_name=out_port_name
            )
            devices[name] = new_device

            for control_content in device_content['controls']:
                name = control_content['name']
                if name in controls:
                    raise ValueError(f"MIDI control with name '{name}' already defined")

                control_content['device'] = new_device
                controls[name] = MIDIControlInfo.from_dict(control_content)

        for layer_group_content in yaml_content['layer-groups']:
            name = layer_group_content['name']
            if name in layer_groups:
                raise ValueError(f"MIDI control layer group with name '{name}' already defined")

            layers = dict()
            for layer_content in layer_group_content['layers']:
                name_layer = layer_content['name']
                if name_layer in layers:
                    raise ValueError(f"MIDI control layer group name '{name_layer}' already defined")

                layers[name] = MIDIControlLayerInfo(
                    name=name,
                    trigger=controls[layer_content['trigger']]
                )

            new_layer_group = MIDIControlLayerGroupInfo(
                name=name,
                layers=layers,
                controls=[control for name, control in controls.items() if name in layer_group_content['controls']]
            )
            layer_groups[name] = new_layer_group

    return MIDIConfiguration(
        devices=devices,
        controls=controls,
        layer_groups=layer_groups
    )
