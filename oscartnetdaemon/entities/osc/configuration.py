from dataclasses import dataclass

from dataclasses_json import dataclass_json, LetterCase

from oscartnetdaemon.entities.osc.widget_info import OSCWidgetInfo
from oscartnetdaemon.entities.osc.recall_group_info import OSCRecallGroupInfo


@dataclass_json(letter_case=LetterCase.KEBAB)
@dataclass
class OSCConfiguration:
    server_ip_address: str
    server_ip_address_autodetect: bool
    server_port: int
    widgets: list[OSCWidgetInfo]
    recall_groups: list[OSCRecallGroupInfo]
