from dataclasses import dataclass

from dataclasses_json import dataclass_json, LetterCase

from oscartnetdaemon.entities.osc.widget import OSCWidget


@dataclass_json(letter_case=LetterCase.KEBAB)
@dataclass
class OSCConfiguration:
    server_ip_address: str
    server_ip_address_autodetect: bool
    server_port: int
    widgets: list[OSCWidget]
