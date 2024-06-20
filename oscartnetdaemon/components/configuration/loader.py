import os.path
from copy import deepcopy
import logging

import yaml

from oscartnetdaemon.components.components_singleton import Components
from oscartnetdaemon.entities.osc.configuration import OSCConfiguration
from oscartnetdaemon.entities.control.control_info import ControlInfo


_logger = logging.getLogger(__name__)


class ConfigurationLoader:

    @staticmethod
    def load_from_file(filepath):
        _logger.info(f"Loading configuration from {filepath}...")

        with open(filepath, 'r') as yaml_file:
            yaml_content = yaml.safe_load(yaml_file)

        #
        # Controls
        controls = dict()
        for filename_controls in yaml_content['controls']:
            filepath_controls = os.path.join(os.path.dirname(filepath), filename_controls)
            with open(filepath_controls, 'r') as yaml_controls_file:
                yaml_controls_content = yaml.safe_load(yaml_controls_file)

            for control_content in yaml_controls_content['controls']:
                name = control_content['name']
                if name in controls:
                    raise ValueError(f"Control named '{name}' already exists")

                controls[name] = ControlInfo.from_dict(control_content)

        Components().controls_infos = deepcopy(controls)

        #
        # OSC
        osc_config: dict = deepcopy(yaml_content['osc'])
        widget_definition_files = deepcopy(osc_config['widgets'])
        osc_config.pop("widgets")

        for filename_osc in widget_definition_files:
            filepath_osc = os.path.join(os.path.dirname(filepath), filename_osc)
            with open(filepath_osc, 'r') as yaml_osc_file:
                yaml_osc_content = yaml.safe_load(yaml_osc_file)
                # FIXME this is not safe, one could override other things in OSC config
                osc_config.update(yaml_osc_content)

        Components().osc_configuration = OSCConfiguration.from_dict(osc_config)
