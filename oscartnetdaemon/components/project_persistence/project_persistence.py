import json
import logging
import os

from oscartnetdaemon.components.argument_parser import parse_args
from oscartnetdaemon.components.project_persistence.project import Project
from oscartnetdaemon.core.components import Components


_logger = logging.getLogger(__name__)


class ProjectPersistence:

    def __init__(self):
        self._project: Project = None
        self.filepath: str = ""

    def new(self) -> None:
        self.filepath: str = ""
        self._project = Project(
            name="New project",
            configuration=parse_args()
        )
        self._load_project()

    def load(self, filepath: str) -> None:
        if not filepath or not os.path.exists(filepath):
            _logger.warning(f"No filepath provided or file does not exist. Creating new project.")
            self.new()
            return

        with open(filepath, "r") as f:
            try:
                self._project = Project.from_json(f.read())
                _logger.info(f"Loaded project from {filepath}")
            except json.JSONDecodeError:
                _logger.warning(f"Could not load project from {filepath}. Creating new project.")
                self.new()
                return

        self.filepath = filepath
        self._load_project()

    def save(self) -> str:
        self.save_as(self.filepath)
        return self.filepath

    def save_as(self, filepath: str) -> None:
        self.filepath = filepath

        self._project.patterns = Components().pattern_store.data

        with open(filepath, "w") as f:
            json.dump(self._project.to_dict(), f, indent=2)
        _logger.info(f"Saved project to {self.filepath}")

    def is_direct_save_available(self) -> bool:
        return self.filepath != ""

    def _load_project(self):
        Components().configuration = self._project.configuration
        Components().show_store.load_show(self._project.fixtures)
        Components().pattern_store.data = self._project.patterns
