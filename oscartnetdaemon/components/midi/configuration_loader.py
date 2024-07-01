import fnmatch
from copy import copy, deepcopy

import mido
import yaml

from oscartnetdaemon.components.midi.argument_parser import parse_command_line_args
from oscartnetdaemon.components.midi.configuration import MIDIConfiguration
from oscartnetdaemon.components.midi.context import MIDIContext
from oscartnetdaemon.components.midi.io.device_info import MIDIDeviceInfo
from oscartnetdaemon.components.midi.layer_group_info import MIDILayerGroupInfo
from oscartnetdaemon.components.midi.layer_info import MIDILayerInfo
from oscartnetdaemon.components.midi.page_direction_enum import MIDIPageDirection
from oscartnetdaemon.components.midi.pagination_info import MIDIPaginationInfo
from oscartnetdaemon.components.midi.variable_info import MIDIVariableInfo
from oscartnetdaemon.domain_contract.abstract_configuration_loader import AbstractConfigurationLoader


def _find_in_list(item: str, items: list[str]) -> str:
    for item_ in items:
        if item in item_:
            return item_

    return ""


class MIDIConfigurationLoader(AbstractConfigurationLoader):
    """
    At least returns a BaseConfiguration object ()
    Subtype of BaseConfiguration can be created to load additional IO specific configuration
    """

    def __init__(self):
        self.filepaths = parse_command_line_args()

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
        MIDIContext().layer_group_infos = self.layer_groups

        # from pprint import pp
        # pp(configuration, width=500)
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
            name = variable_dict['name']
            if has_wildcards(name):
                raise ValueError(f"Wildcards not allowed in variable name '{name}'")

            variable_dict['device_name'] = device['name']
            variable_dict['midi-parsing']['bytes_as_str'] = variable_dict['midi-parsing'].get('bytes', list())

            if name in self.variables:
                raise ValueError(f"MIDI Variable '{name}' already assigned")

            self.variables[name] = MIDIVariableInfo.from_dict(variable_dict)

    #
    # PAGES
    def load_pages(self):
        variable_to_pop_names: list[str] = list()
        original_variables_names = copy(list(self.variables.keys()))  # Keep a copy for wildcard filtering
        for pagination in self.content.get('pages', list()):
            ignored_variable_names: list[str] = list()
            button_up = self.make_page_button(pagination, MIDIPageDirection.Up)
            button_down = self.make_page_button(pagination, MIDIPageDirection.Down)

            if button_up is None or button_down is None:
                continue

            new_pagination = MIDIPaginationInfo(
                name=pagination['name'],
                page_count=pagination['page-count'],
                button_up=button_up,
                button_down=button_down,
                variables=list()
            )

            for page_number in range(new_pagination.page_count):
                new_pagination.variables.append(list())
                for variable_name in apply_wildcards(pagination['variables'], original_variables_names):
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

    def make_page_button(self, pagination, direction: MIDIPageDirection) -> MIDIVariableInfo | None:
        button_name = pagination['button-up' if direction == MIDIPageDirection.Up else 'button-down']
        button = self.variables.get(button_name, None)
        if button is None:
            print(f"Pagination '{pagination['name']}': unable to find Button '{button_name}'")
            return
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
        original_variables_names = copy(list(self.variables.keys()))  # Keep a copy for wildcard filtering
        layer_groups = self.content.get('layer-groups', list())
        content = unify_layer_groups(layer_groups, original_variables_names)
        variable_to_pop_names: list[str] = list()
        for layer_group in content:
            ignored_variable_names: list[str] = list()

            new_layer_group = MIDILayerGroupInfo(
                name=layer_group['name'],
                layers=dict(),
                current_layer_name=""
            )

            for layer in layer_group['layers']:
                button_activate = self.make_layer_button(
                    button_name=layer['button-activate'],
                    layer_name=layer['name'],
                    layer_group_name=layer_group['name']
                )
                if button_activate is None:
                    continue

                new_layer = MIDILayerInfo(
                    name=layer['name'],
                    button_activate=button_activate,
                    variables=list()
                )

                for mapping_dict in layer['mappings']:
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

                    if new_layered_variable.pagination_name:
                        page_variables = self.paginations[new_layered_variable.pagination_name].variables[new_layered_variable.page_number]
                        for i, page_variable in enumerate(copy(page_variables)):
                            if page_variable.name == source_name:
                                page_variables.pop(i)
                        page_variables.append(new_layered_variable)

                    new_layer.variables.append(new_layered_variable)
                    self.variables[new_layered_variable.name] = new_layered_variable

                new_layer_group.layers[new_layer.name] = new_layer

            if new_layer_group.layers:
                self.layer_groups[new_layer_group.name] = new_layer_group
                print(f"Layer Group '{new_layer_group.name}' not found Variables: {', '.join(set(ignored_variable_names))}")
            else:
                print(f"Layer Group ignored '{new_layer_group.name}': unable to create any layer for it")

        for variable_to_pop_name in set(variable_to_pop_names):
            self.variables.pop(variable_to_pop_name)

    def make_layer_button(self, button_name: str, layer_name: str, layer_group_name: str) -> MIDIVariableInfo | None:
        button = self.variables.get(button_name, None)
        if button is None:
            print(f"Layer group '{layer_group_name}': unable to find button '{button_name}'")
            return

        if button.is_page_button:
            print(f"Button '{button_name}' is already used for Pagination '{button.pagination_name}'")
            return

        button.is_layer_button = True
        button.layer_name = layer_name
        button.layer_group_name = layer_group_name
        return button

    def make_layered_variable(self, source_name, target_name, layer_name, layer_group_name) -> MIDIVariableInfo:
        new_variable = deepcopy(self.variables[source_name])
        new_variable.name = target_name
        new_variable.layer_name = layer_name
        new_variable.layer_group_name = layer_group_name

        return new_variable


def has_wildcards(name):
    return "$" in name or "*" in name


def apply_wildcards(names: list[str], original_variables_names: list[str]) -> list[str]:
    parsed_names = list()
    for name in names:
        if not has_wildcards(name):
            parsed_names.append(name)

        else:
            parsed_names += fnmatch.filter(original_variables_names, name)

    print(parsed_names)

    return list(set(parsed_names))


def unify_layer_groups(layer_groups: list[dict], original_variables_names: list[str]) -> list[dict]:
    """Ensure all concerned Variables are mapped in all groups"""
    for group in layer_groups:
        all_sources = apply_wildcards(group.get('variables', list()), original_variables_names)
        all_mappings = [{'source': name, 'target': name} for name in all_sources]

        for layer in group['layers']:
            for mapping in layer.get('mappings', list()):
                if mapping['source'] not in all_sources:
                    all_sources.append(mapping['source'])  # FIXME a bit hacky ?
                    all_mappings.append({'source': mapping['source'], 'target': mapping['source']})

        for layer in group['layers']:
            layer['mappings'] = _updated_mappings(
                layer_name=layer['name'],
                original_mappings=layer.get('mappings', list()),
                all_mappings=all_mappings
            )

    return layer_groups


def _updated_mappings(layer_name:str, original_mappings: list, all_mappings: list) -> list:
    copied_originals = deepcopy(original_mappings)

    for mapping in all_mappings:
        if mapping not in copied_originals:
            new_mapping = deepcopy(mapping)
            new_mapping['target'] = f"{layer_name}.{new_mapping['target']}"
            copied_originals.append(new_mapping)

    return copied_originals
