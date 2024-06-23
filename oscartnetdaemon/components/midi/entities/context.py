from dataclasses import dataclass


from oscartnetdaemon.components.midi.entities.layer_info import MIDIControlLayerInfo


@dataclass
class MIDIContext:
    current_page: int
    current_layer: MIDIControlLayerInfo
