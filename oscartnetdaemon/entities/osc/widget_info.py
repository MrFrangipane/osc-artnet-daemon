from dataclasses import dataclass

from dataclasses_json import dataclass_json, LetterCase

from oscartnetdaemon.entities.osc.widget_type_enum import OSCWidgetTypeEnum


@dataclass_json(letter_case=LetterCase.KEBAB)
@dataclass
class OSCWidgetInfo:
    name: str
    type: OSCWidgetTypeEnum
    osc_address: str
