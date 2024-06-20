from abc import ABC, abstractmethod
from typing import Any

from oscartnetdaemon.components.control.repository import ControlRepository
from oscartnetdaemon.entities.control.control_update_origin_enum import ControlUpdateOrigin


class AbstractControlsService(ABC):
    def __init__(self):
        self.control_repository: ControlRepository = None

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def send_control_update(self, origin: ControlUpdateOrigin, control_name: str, value: Any):
        pass
