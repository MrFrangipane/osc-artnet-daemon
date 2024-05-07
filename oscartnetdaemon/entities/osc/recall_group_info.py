from dataclasses import dataclass

from dataclasses_json import dataclass_json, LetterCase

from oscartnetdaemon.entities.osc.widget_info import OSCWidgetInfo


@dataclass_json(letter_case=LetterCase.KEBAB)
@dataclass
class OSCRecallGroupInfo:
    name: str
    widget_osc_addresses: list[str]
