from oscartnetdaemon.components.new_midi.pagination_info import MIDIPaginationInfo
from oscartnetdaemon.python_extensions.singleton_metaclass import SingletonMetaclass


class MIDIContext(metaclass=SingletonMetaclass):
    def __init__(self):
        self.pagination_infos: dict[str, MIDIPaginationInfo] = dict()
