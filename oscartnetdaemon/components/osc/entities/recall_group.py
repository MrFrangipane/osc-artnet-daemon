# fixme: move to entities ?
from dataclasses import dataclass, field
from typing import Any

from oscartnetdaemon.components.osc.controls.abstract import OSCAbstractControl


@dataclass
class OSCMemorySlot:
    osc_address: str
    controls_values: dict[str, Any] = field(default_factory=dict)  # fixme create a OSCControlValues dataclass ?


@dataclass
class OSCRecallGroup:
    name: str
    controls: list[OSCAbstractControl]
    memory_slots: dict[str, OSCMemorySlot]
