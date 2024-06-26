from copy import deepcopy

import mido
import yaml

from oscartnetdaemon.components.new_midi.configuration import MIDIConfiguration
from oscartnetdaemon.components.new_midi.context import MIDIContext
from oscartnetdaemon.components.new_midi.io.device_info import MIDIDeviceInfo
from oscartnetdaemon.components.new_midi.layer_group_info import MIDILayerGroupInfo
from oscartnetdaemon.components.new_midi.layer_info import MIDILayerInfo
from oscartnetdaemon.components.new_midi.page_direction_enum import MIDIPageDirection
from oscartnetdaemon.components.new_midi.pagination_info import MIDIPaginationInfo
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

        self.devices: dict[str, MIDIDeviceInfo] = dict()
        self.variables: dict[str, MIDIVariableInfo] = dict()
        self.paginations: dict[str, MIDIPaginationInfo] = dict()
        self.layer_groups: dict[str, MIDILayerGroupInfo] = dict()

    def load(self) -> MIDIConfiguration:
        self.in_port_names = mido.get_input_names()
        self.out_port_names = mido.get_output_names()

        file_contents = list()
        for filepath in self.filepaths:
            with open(filepath, 'r') as file:
                file_contents.append(yaml.safe_load(file))

        for file_content in file_contents:
            self.content = file_content
            self.load_devices()

        for file_content in file_contents:
            self.content = file_content
            self.load_pages()

        for file_content in file_contents:
            self.content = file_content
            self.load_layer_groups()

        configuration = MIDIConfiguration(
            device_infos=self.devices,
            variable_infos=self.variables,
            pagination_infos=self.paginations,
            layer_group_infos=self.layer_groups
        )

        # Install PaginationInfos in MIDIContext
        MIDIContext().pagination_infos = self.paginations

        from pprint import pp
        pp(configuration, width=500)
        return configuration

    #
    # DEVICES
    def load_devices(self):
        for device in self.content.get('devices', list()):
            in_port_name = _find_in_list(device['midi-port-pattern'], self.in_port_names)
            if not in_port_name:
                print(f"MIDI Device '{device['name']}' not found")
                continue

            out_port_name = _find_in_list(device['midi-port-pattern'], self.out_port_names)

            self.devices[device['name']] = MIDIDeviceInfo(
                name=device['name'],
                in_port_name=in_port_name,
                out_port_name=out_port_name
            )

            self.load_device_variables(device)

    def load_device_variables(self, device):
        for variable_dict in device['variables']:
            variable_dict['device_name'] = device['name']
            self.variables[variable_dict['name']] = MIDIVariableInfo.from_dict(variable_dict)

    #
    # PAGES
    def load_pages(self):
        variable_to_pop_names: list[str] = list()
        for pagination in self.content.get('pages', list()):
            ignored_variable_names: list[str] = list()
            button_up = self.make_page_button(pagination, MIDIPageDirection.Up)
            button_down = self.make_page_button(pagination, MIDIPageDirection.Down)

            new_pagination = MIDIPaginationInfo(
                name=pagination['name'],
                page_count=pagination['page-count'],
                button_up=button_up,
                button_down=button_down,
                variables=list()
            )

            for page_number in range(new_pagination.page_count):
                new_pagination.variables.append(list())
                for variable_name in pagination['variables']:
                    if variable_name not in self.variables:
                        ignored_variable_names.append(variable_name)
                        continue

                    variable_to_pop_names.append(variable_name)
                    new_paginated_variable = self.make_paginated_variable(
                        variable_name=variable_name,
                        page_number=page_number,
                        pagination_name=new_pagination.name
                    )
                    new_pagination.variables[page_number].append(new_paginated_variable)
                    self.variables[new_paginated_variable.name] = new_paginated_variable

            self.paginations[new_pagination.name] = new_pagination
            print(f"Pages '{new_pagination.name}' not found Variables: {', '.join(set(ignored_variable_names))}")

        for variable_to_pop_name in set(variable_to_pop_names):
            self.variables.pop(variable_to_pop_name)

    def make_page_button(self, pagination, direction: MIDIPageDirection) -> MIDIVariableInfo:
        button_name = pagination['button-up' if direction == MIDIPageDirection.Up else 'button-down']
        button = self.variables[button_name]
        button.is_page_button = True
        button.pagination_name = pagination['name']
        button.page_direction = direction
        return button

    def make_paginated_variable(self, variable_name, page_number, pagination_name) -> MIDIVariableInfo:
        new_variable = deepcopy(self.variables[variable_name])
        new_variable.name = f"{variable_name}:{page_number}"
        new_variable.pagination_name = pagination_name
        new_variable.page_number = page_number

        return new_variable

    #
    # LAYER GROUPS
    def load_layer_groups(self):
        variable_to_pop_names: list[str] = list()
        for layer_group in self.content.get('layer-groups', list()):
            ignored_variable_names: list[str] = list()

            new_layer_group = MIDILayerGroupInfo(
                name=layer_group['name'],
                layers=dict(),
                current_layer_name=""
            )

            for layer in layer_group['layers']:
                button_activate = self.make_layer_button(
                    button_name=layer['button-activate'],
                    layer_name=layer['name']
                )
                new_layer = MIDILayerInfo(
                    name=layer['name'],
                    button_activate=button_activate,
                    variables=list()
                )

                for mapping_dict in layer['variables']:
                    source_name = mapping_dict['source']
                    if source_name not in self.variables:
                        ignored_variable_names.append(source_name)
                        continue

                    variable_to_pop_names.append(source_name)
                    new_layered_variable = self.make_layered_variable(
                        source_name=source_name,
                        target_name=mapping_dict['target'],
                        layer_name=layer['name'],
                        layer_group_name=layer_group['name']
                    )
                    new_layer.variables.append(new_layered_variable)
                    self.variables[new_layered_variable.name] = new_layered_variable

                new_layer_group.layers[new_layer.name] = new_layer

            self.layer_groups[new_layer_group.name] = new_layer_group
            print(f"Layer Group '{new_layer_group.name}' not found Variables: {', '.join(set(ignored_variable_names))}")

        for variable_to_pop_name in set(variable_to_pop_names):
            self.variables.pop(variable_to_pop_name)

    def make_layer_button(self, button_name: str, layer_name: str) -> MIDIVariableInfo:
        button = self.variables[button_name]
        if button.is_page_button:
            raise AttributeError(f"Button '{button_name}' is already used for Pagination '{button.pagination_name}'")

        button.is_layer_button = True
        button.layer_name = layer_name
        return button

    def make_layered_variable(self, source_name, target_name, layer_name, layer_group_name) -> MIDIVariableInfo:
        new_variable = deepcopy(self.variables[source_name])
        new_variable.name = target_name
        new_variable.layer_name = layer_name
        new_variable.layer_group_name = layer_group_name

        return new_variable
