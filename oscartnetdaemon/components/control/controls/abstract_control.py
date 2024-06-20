from typing import Any

from oscartnetdaemon.entities.control.control_info import ControlInfo


# FIXME : will we need control subtypes ? This seems to be sufficient
class AbstractControl:

    def __init__(self, info: ControlInfo):
        self.info = info
        self.value: Any = None

    def set_value(self, value: Any):
        self.value = value
        print(f"Value set {self.info.name}={value}")
