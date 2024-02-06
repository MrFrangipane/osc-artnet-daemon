from dataclasses import dataclass

from oscartnetdaemon.components.artnet_server import ArtNetServer
from oscartnetdaemon.components.fixtures_updater.abstract import AbstractFixturesUpdater
from oscartnetdaemon.components.osc_server.abstract import AbstractOSCServer
from oscartnetdaemon.core.mood import Mood
from oscartnetdaemon.python_extensions.singleton_metaclass import SingletonMetaclass


@dataclass
class Components(metaclass=SingletonMetaclass):
    artnet: ArtNetServer = ArtNetServer()
    fixture_updater: AbstractFixturesUpdater = None
    osc: AbstractOSCServer = None
    mood: Mood = Mood()
