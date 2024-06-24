import os.path
from copy import copy

import mido
import yaml

from oscartnetdaemon.components.configuration.entities.configuration import ConfigurationInfo
from oscartnetdaemon.components.midi.entities.configuration import MIDIConfiguration
from oscartnetdaemon.components.midi.entities.control_info import MIDIControlInfo
from oscartnetdaemon.components.midi.entities.device_info import MIDIDeviceInfo
from oscartnetdaemon.components.midi.entities.layer_group_info import MIDIControlLayerGroupInfo
from oscartnetdaemon.components.midi.entities.layer_info import MIDIControlLayerInfo
from oscartnetdaemon.components.midi.entities.pagination_info import MIDIPaginationInfo


def _find_in_list(item, items):
    for item_ in items:
        if item in item_:
            return item_

    raise ValueError(f"Not found '{item}'")


def load_midi_configuration(configuration_info: ConfigurationInfo) -> MIDIConfiguration:
    in_port_names = mido.get_input_names()
    out_port_names = mido.get_output_names()

    devices: dict[str, MIDIDeviceInfo] = dict()
    controls: dict[str, MIDIControlInfo] = dict()
    layer_groups: dict[str, MIDIControlLayerGroupInfo] = dict()
    paginations: dict[str, MIDIPaginationInfo] = dict()

    for filename in configuration_info.midi_filenames:
        filepath = os.path.join(configuration_info.root_folder, filename)
        with open(filepath, 'r') as yaml_controls_file:
            yaml_content = yaml.safe_load(yaml_controls_file)

        #
        # Devices
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

        #
        # Pagination
        paginated_control_names = list()
        for pagination in yaml_content['pagination']:
            name = pagination['name']
            if name in paginations:
                raise ValueError(f"MIDI pagination with name '{name}' already defined")

            already_paginated_controls = list(set(paginated_control_names) & set(pagination['controls']))
            if already_paginated_controls:
                raise ValueError(
                    f"MIDI pagination '{name}': control(s) already paginated: {', '.join(already_paginated_controls)}"
                )

            pagination['left'] = controls[pagination['left']]
            pagination['right'] = controls[pagination['right']]
            paginated_control_names += pagination['controls']
            paginated_controls = list()
            for control_name in pagination['controls']:
                paginated_controls.append(controls[control_name])
                controls.pop(control_name)
            pagination['controls'] = paginated_controls

            new_pagination_info = MIDIPaginationInfo.from_dict(pagination)

            for page in range(new_pagination_info.page_count):
                for control in new_pagination_info.controls:
                    paginated_control = copy(control)
                    paginated_control.name = paginated_control.name + ":" + str(page)
                    paginated_control.page = page
                    controls[paginated_control.name] = paginated_control

            paginations[name] = new_pagination_info

        #
        # Layers
        layered_control_names = list()
        controls_to_pop_names = list()
        for layer_group_content in yaml_content['layer-groups']:
            name_group = layer_group_content['name']
            if name_group in layer_groups:
                raise ValueError(f"MIDI control layer group with name '{name_group}' already defined")

            layers = dict()
            for layer_content in layer_group_content['layers']:
                name_layer = layer_content['name']
                if name_layer in layers:
                    raise ValueError(f"MIDI control layer group name '{name_layer}' already defined")

                new_layer = MIDIControlLayerInfo(
                    name=name_layer,
                    trigger=controls[layer_content['trigger']]
                )

                layered_controls = list()
                for layered_control_content in layer_content['controls']:
                    name_control = layered_control_content['name']
                    if name_control in layered_control_names:
                        raise ValueError(f"MIDI layered control with name '{name_control}' already defined")
                    layered_control_names.append(name_control)

                    source_name = layered_control_content['control']
                    layered_control = copy(controls[source_name])
                    if source_name not in controls_to_pop_names:
                        controls_to_pop_names.append(source_name)

                    layered_control.name = name_control
                    layered_control.layer_name = new_layer.name
                    layered_control.mapped_to = layered_control_content.get('mapped_to', '')
                    layered_controls.append(layered_control)
                    controls[layered_control.name] = layered_control

                new_layer.controls = layered_controls
                layers[name_layer] = new_layer

            for name_ in controls_to_pop_names:
                controls.pop(name_)

            new_layer_group = MIDIControlLayerGroupInfo(
                name=name_group,
                layers=layers
            )
            layer_groups[name_group] = new_layer_group

    configuration = MIDIConfiguration(
        devices=devices,
        controls=controls,
        paginations=paginations,
        layer_groups=layer_groups
    )

    from pprint import pprint
    pprint(configuration)

    return configuration
