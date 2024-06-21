from copy import deepcopy
import os.path

import yaml

from oscartnetdaemon.entities.osc.configuration import OSCConfiguration


def load_osc_configuration(osc: dict, root_folder: str) -> OSCConfiguration:
    config: dict = deepcopy(osc)
    filenames = config['widgets']
    config.pop("widgets")

    for filename in filenames:
        filepath = os.path.join(root_folder, filename)
        with open(filepath, 'r') as yaml_osc_file:
            yaml_content = yaml.safe_load(yaml_osc_file)
            # FIXME this is not safe, one could override other things in OSC config
            config.update(yaml_content)

    return OSCConfiguration.from_dict(config)
