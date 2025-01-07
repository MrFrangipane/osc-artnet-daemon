import logging

from oscartnetdaemon.components.argument_parser import parse_args
from oscartnetdaemon.components.project_persistence.project import Project
from oscartnetdaemon.core.components import Components


_logger = logging.getLogger(__name__)


class ProjectPersistence:

    def __init__(self):
        self._project = Project(
            name="New project",
            configuration=parse_args(),
            fixtures=[
                ["OctostripBar", "OctostripBar", "OctostripBar", "OctostripBar", "OctostripBar", "OctostripBar", "OctostripBar", "OctostripBar"],
                ["Tristan200", "Tristan200"],
                ["TwoBrightPar", "TwoBrightPar", "TwoBrightPar", "TwoBrightPar", "TwoBrightPar"],
                ["HeroWash", "HeroWash"],
                ["RGBPixel", "RGBPixel"]
            ]
        )

    def load(self, filepath: str) -> Project:
        if not filepath:
            _logger.info(f"Loading project from command line arguments with no fixtures")

        Components().configuration = self._project.configuration
        Components().show_store.load_show(self._project.fixtures)
        return self._project
