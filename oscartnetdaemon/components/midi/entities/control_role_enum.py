from enum import Enum


class MIDIControlRole(Enum):
    Unused = 'Unused'
    Mapped = 'Mapped'
    PageSelector = 'PageSelector'
    LayerTrigger = 'LayerTrigger'
