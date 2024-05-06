import logging

import yaml

from oscartnetdaemon.components.components_singleton import Components
from oscartnetdaemon.entities.osc.configuration import OSCConfiguration


_logger = logging.getLogger(__name__)


class ConfigurationLoader:

    @staticmethod
    def load_from_file(filepath):
        _logger.info(f"Loading configuration from {filepath}...")

        with open(filepath, 'r') as yaml_file:
            yaml_content = yaml.safe_load(yaml_file)

        Components().osc_configuration = OSCConfiguration.from_dict(yaml_content['osc'])
