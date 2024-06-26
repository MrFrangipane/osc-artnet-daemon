from oscartnetdaemon.python_extensions.singleton_metaclass import SingletonMetaclass


class MIDIContext(metaclass=SingletonMetaclass):
    def __init__(self):
        self.current_pages: dict[str, int] = dict()
        self.current_layer_names: dict[str, str] = dict()
