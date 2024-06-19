from dataclasses import dataclass, field

from dataclasses_json import dataclass_json, LetterCase

from oscartnetdaemon.entities.osc.widget_type_enum import OSCWidgetTypeEnum


@dataclass_json(letter_case=LetterCase.KEBAB)
@dataclass
class OSCWidgetInfo:
    caption: str
    type: OSCWidgetTypeEnum
    osc_address: str
    labels: list[str] = field(default_factory=list)
