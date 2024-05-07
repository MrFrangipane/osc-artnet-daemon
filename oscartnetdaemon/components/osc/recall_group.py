# fixme: move to entities ?
from dataclasses import dataclass, field
from typing import Any

from oscartnetdaemon.components.osc.widgets.abstract import OSCAbstractWidget


@dataclass
class OSCMemorySlot:
    osc_address: str
    widgets_values: dict[str, Any] = field(default_factory=dict)  # fixme create a OSCWidgetValues dataclass ?


@dataclass
class OSCRecallGroup:
    name: str
    widgets: list[OSCAbstractWidget]
    memory_slots: dict[str, OSCMemorySlot]
