from dataclasses import dataclass

from oscartnetdaemon.components.artnet_server import ArtNetServer
from oscartnetdaemon.core.configuration import Configuration
from oscartnetdaemon.components.discovery.abstract import AbstractDiscovery
from oscartnetdaemon.components.fixtures_updater.abstract import AbstractFixturesUpdater
from oscartnetdaemon.components.osc.message_sender import OSCMessageSender
from oscartnetdaemon.components.osc.server_abstract import AbstractOSCServer
from oscartnetdaemon.core.mood import Mood
from oscartnetdaemon.python_extensions.singleton_metaclass import SingletonMetaclass


@dataclass
class Components(metaclass=SingletonMetaclass):
    artnet: ArtNetServer = None
    configuration: Configuration = None
    discovery: AbstractDiscovery = None
    fixture_updater: AbstractFixturesUpdater = None
    osc_server: AbstractOSCServer = None
    osc_message_sender: OSCMessageSender = None
    mood: Mood = Mood()
