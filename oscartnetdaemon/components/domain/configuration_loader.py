from copy import deepcopy
import os.path

import yaml

from oscartnetdaemon.components.domain.entities.control_info import DomainControlInfo


def load_controls_configuration(filenames: list[str], root_folder: str):
    controls = dict()
    for filename in filenames:
        filepath = os.path.join(root_folder, filename)
        with open(filepath, 'r') as yaml_controls_file:
            yaml_content = yaml.safe_load(yaml_controls_file)

        for control_content in yaml_content['controls']:
            name = control_content['name']
            if name in controls:
                raise ValueError(f"Control with name '{name}' already defined")

            controls[name] = DomainControlInfo.from_dict(control_content)

    return deepcopy(controls)
