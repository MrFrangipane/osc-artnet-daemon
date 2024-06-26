from copy import deepcopy

import mido
import yaml

from oscartnetdaemon.components.new_midi.configuration import MIDIConfiguration
from oscartnetdaemon.components.new_midi.io.device_info import MIDIDeviceInfo
from oscartnetdaemon.components.new_midi.pagination_info import MIDIPaginationInfo
from oscartnetdaemon.components.new_midi.variable_info import MIDIVariableInfo
from oscartnetdaemon.domain_contract.abstract_configuration_loader import AbstractConfigurationLoader
from oscartnetdaemon.components.new_midi.page_direction_enum import MIDIPageDirection
from oscartnetdaemon.components.new_midi.context import MIDIContext


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
        self.variable_infos: dict[str, MIDIVariableInfo] = dict()
        self.pagination_infos: dict[str, MIDIPaginationInfo] = dict()

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
            self.variable_infos[variable_dict['name']] = MIDIVariableInfo.from_dict(variable_dict)

    def make_page_button(self, pagination, direction: MIDIPageDirection):
        button_name = pagination['up' if direction == MIDIPageDirection.Up else 'down']
        button = self.variable_infos[button_name]
        button.is_page_button = True
        button.pagination_name = pagination['name']
        button.page_direction = direction
        return button

    def make_paginated_variable_info(self, variable_name, page_number, pagination_name):
        new_variable_info = deepcopy(self.variable_infos[variable_name])
        new_variable_name = f"{variable_name}:{page_number}"
        new_variable_info.name = new_variable_name
        new_variable_info.pagination_name = pagination_name
        new_variable_info.page_number = page_number

        return new_variable_info

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
                    if variable_name not in self.variable_infos:
                        ignored_variable_names.append(variable_name)
                        continue

                    variable_to_pop_names.append(variable_name)
                    new_paginated_variable_info = self.make_paginated_variable_info(
                        variable_name=variable_name,
                        page_number=page_number,
                        pagination_name=new_pagination.name
                    )
                    new_pagination.variables[page_number].append(new_paginated_variable_info)
                    self.variable_infos[new_paginated_variable_info.name] = new_paginated_variable_info

            self.pagination_infos[new_pagination.name] = new_pagination
            print(f"Pages '{new_pagination.name}' not found Variables: {', '.join(set(ignored_variable_names))}")

        for variable_to_pop_name in set(variable_to_pop_names):
            self.variable_infos.pop(variable_to_pop_name)

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

        configuration = MIDIConfiguration(
            device_infos=self.device_infos,
            variable_infos=self.variable_infos,
            pagination_infos=self.pagination_infos
        )

        # Install PaginationInfos in MIDIContext
        MIDIContext().pagination_infos = self.pagination_infos

        from pprint import pp
        pp(configuration, width=500)
        return configuration
