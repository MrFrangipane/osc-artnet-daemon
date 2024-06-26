from dataclasses import dataclass

from oscartnetdaemon.components.new_midi.variable_info import MIDIVariableInfo


@dataclass
class MIDIPaginationInfo:
    name: str
    page_count: int
    button_up: MIDIVariableInfo
    button_down: MIDIVariableInfo
    variables: list[list[MIDIVariableInfo]]
    current_page: int = 0

    def up(self) -> bool:
        previous_page = self.current_page
        self.current_page = min(self.page_count - 1, self.current_page + 1)
        return previous_page != self.current_page

    def down(self):
        previous_page = self.current_page
        self.current_page = max(0, self.current_page - 1)
        return previous_page != self.current_page
