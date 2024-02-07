from dataclasses import dataclass

from oscartnetdaemon.components.artnet_server import ArtNetServer
from oscartnetdaemon.components.discovery.abstract import AbstractDiscovery
from oscartnetdaemon.components.fixtures_updater.abstract import AbstractFixturesUpdater
from oscartnetdaemon.components.mood_store.abstract import AbstractMoodStore
from oscartnetdaemon.components.osc.abstract_message_sender import AbstractOSCMessageSender
from oscartnetdaemon.components.osc.server_abstract import AbstractOSCServer
from oscartnetdaemon.core.mood import Mood
from oscartnetdaemon.python_extensions.singleton_metaclass import SingletonMetaclass


@dataclass
class Components(metaclass=SingletonMetaclass):
    artnet: ArtNetServer = None
    discovery: AbstractDiscovery = None
    fixture_updater: AbstractFixturesUpdater = None
    mood_store: AbstractMoodStore = None
    osc_server: AbstractOSCServer = None
    osc_message_sender: AbstractOSCMessageSender = None
    mood: Mood = Mood()
