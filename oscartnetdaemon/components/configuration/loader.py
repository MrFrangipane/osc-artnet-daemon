import logging
import os.path

import yaml

from oscartnetdaemon.components.components_singleton import Components
# from oscartnetdaemon.components.midi.configuration_loader import load_midi_configuration
# from oscartnetdaemon.components.osc.configuration_loader import load_osc_configuration
from oscartnetdaemon.components.domain.configuration_loader import load_controls_configuration


_logger = logging.getLogger(__name__)


class ConfigurationLoader:

    @staticmethod
    def load_from_file(filepath):
        root_folder = os.path.dirname(filepath)
        _logger.info(f"Loading configuration from {filepath}...")

        with open(filepath, 'r') as yaml_file:
            yaml_content = yaml.safe_load(yaml_file)

        Components().domain_controls_infos = load_controls_configuration(
            filenames=yaml_content['controls'],
            root_folder=root_folder
        )
        # Components().osc_configuration = load_osc_configuration(
        #     osc=yaml_content['osc'],
        #     root_folder=root_folder
        # )
        # Components().midi_configuration = load_midi_configuration(
        #     filenames=yaml_content['midi-devices'],
        #     root_folder=root_folder
        # )

        _logger.info(f"Done")
