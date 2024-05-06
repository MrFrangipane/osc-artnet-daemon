# fixme: move to entities ?
from dataclasses import dataclass, field
from typing import Any

from oscartnetdaemon.components.osc.widgets.abstract import OSCAbstractWidget


@dataclass
class OSCRecallGroup:
    name: str
    widgets: list[OSCAbstractWidget] = field(default_factory=list)
    values: dict[str, Any] = field(default_factory=dict)
