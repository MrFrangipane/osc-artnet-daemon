import logging
import os.path

import yaml

from oscartnetdaemon.components.components_singleton import Components
from oscartnetdaemon.components.domain.configuration_loader import load_controls_configuration
from oscartnetdaemon.components.configuration.entities.configuration import ConfigurationInfo


_logger = logging.getLogger(__name__)


class ConfigurationLoader:

    @staticmethod
    def load_from_file(filepath):
        root_folder = os.path.dirname(filepath)
        _logger.info(f"Loading configuration from {filepath}...")

        with open(filepath, 'r') as yaml_file:
            yaml_content = yaml.safe_load(yaml_file)

        Components().configuration_info = ConfigurationInfo(
            root_folder=os.path.dirname(filepath),
            midi_filenames=yaml_content['midi-filenames']
        )

        Components().domain_control_infos = load_controls_configuration(
            filenames=yaml_content['controls'],
            root_folder=root_folder
        )

        _logger.info(f"Done")
