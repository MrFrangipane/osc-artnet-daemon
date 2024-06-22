from dataclasses import dataclass


from oscartnetdaemon.entities.midi.layer_info import MIDIControlLayerInfo


@dataclass
class MIDIContext:
    current_page: int
    current_layer: MIDIControlLayerInfo
