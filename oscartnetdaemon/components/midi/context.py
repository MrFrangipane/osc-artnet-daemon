from oscartnetdaemon.components.midi.layer_group_info import MIDILayerGroupInfo
from oscartnetdaemon.components.midi.pagination_info import MIDIPaginationInfo
from oscartnetdaemon.python_extensions.singleton_metaclass import SingletonMetaclass


class MIDIContext(metaclass=SingletonMetaclass):
    def __init__(self):
        self.pagination_infos: dict[str, MIDIPaginationInfo] = dict()
        self.layer_group_infos: dict[str, MIDILayerGroupInfo] = dict()
