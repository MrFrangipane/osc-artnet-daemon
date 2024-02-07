from dataclasses import dataclass

from oscartnetdaemon.components.artnet_server import ArtNetServer
from oscartnetdaemon.core.configuration import Configuration
from oscartnetdaemon.components.discovery.abstract import AbstractDiscovery
from oscartnetdaemon.components.fixtures_updater.abstract import AbstractFixturesUpdater
from oscartnetdaemon.components.osc_clients import OSCClients
from oscartnetdaemon.components.osc_server.abstract import AbstractOSCServer
from oscartnetdaemon.core.mood import Mood
from oscartnetdaemon.python_extensions.singleton_metaclass import SingletonMetaclass


@dataclass
class Components(metaclass=SingletonMetaclass):
    artnet: ArtNetServer = None
    configuration: Configuration = None
    discovery: AbstractDiscovery = None
    fixture_updater: AbstractFixturesUpdater = None
    osc_server: AbstractOSCServer = None
    osc_clients: OSCClients = None
    mood: Mood = Mood()
