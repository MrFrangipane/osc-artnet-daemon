from abc import ABC, abstractmethod

from oscartnetdaemon.core.osc_client_info import OSCClientInfo


# FIXME find a better name than MoodStore
class AbstractMoodStore(ABC):
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
    def recall(self, sender, scene_name):
        pass

    @abstractmethod
    def set_punch(self, sender, scene_name, is_punch):
        pass

    @abstractmethod
    def set_temporary_modifier(self, sender, is_active):
        pass
