from abc import ABC, abstractmethod

from oscartnetdaemon.core.osc_client_info import OSCClientInfo


# FIXME find better names for FourMoods and MoodStore
class AbstractMoodStore(ABC):
    _before_punch = "before_punch"

    @abstractmethod
    def register_client(self, info: OSCClientInfo):
        pass

    @abstractmethod
    def unregister_client(self, info: OSCClientInfo):
        pass

    @abstractmethod
    def save(self, sender, scene_name):
        pass

    @abstractmethod
    def load(self, sender, scene_name):
        pass

    @abstractmethod
    def set_punch(self, sender, scene_name, is_punch):
        pass
