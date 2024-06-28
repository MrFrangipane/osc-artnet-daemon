from dataclasses import dataclass

from oscartnetdaemon.components.midi.layer_info import MIDILayerInfo


@dataclass
class MIDILayerGroupInfo:
    name: str
    layers: dict[str, MIDILayerInfo]
    current_layer_name: str = ""
