from copy import deepcopy
import os.path

import yaml

from oscartnetdaemon.components.osc.entities.configuration import OSCConfiguration
from oscartnetdaemon.components.configuration.entities.configuration import ConfigurationInfo


def load_osc_configuration(configuration_info: ConfigurationInfo) -> OSCConfiguration:
    config: dict = deepcopy(configuration_info.osc_raw_configuration)
    filenames = config['controls']
    config.pop("controls")

    for filename in filenames:
        filepath = os.path.join(configuration_info.root_folder, filename)
        with open(filepath, 'r') as yaml_osc_file:
            yaml_content = yaml.safe_load(yaml_osc_file)
            # FIXME this is not safe, one could override other things in OSC config
            config.update(yaml_content)

    return OSCConfiguration.from_dict(config)
