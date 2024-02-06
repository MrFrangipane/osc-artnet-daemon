from dataclasses import dataclass

from oscartnet.components.artnet_server import ArtNetServer
from oscartnet.components.fixtures_updater.abstract import AbstractFixturesUpdater
from oscartnet.components.osc_server.abstract import AbstractOSCServer
from oscartnet.core.mood import Mood
from oscartnet.python_extensions.singleton_metaclass import SingletonMetaclass


@dataclass
class Components(metaclass=SingletonMetaclass):
    artnet: ArtNetServer = ArtNetServer()
    fixture_updater: AbstractFixturesUpdater = None
    osc: AbstractOSCServer = None
    mood: Mood = Mood()
