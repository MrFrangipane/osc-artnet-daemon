from dataclasses import dataclass, field

from oscartnetdaemon.components.artnet_server import ArtnetServer
from oscartnetdaemon.components.discovery.abstract import AbstractDiscovery
from oscartnetdaemon.components.fixtures_updater.abstract import AbstractFixturesUpdater
from oscartnetdaemon.components.mood_store.abstract import AbstractMoodStore
from oscartnetdaemon.components.osc.abstract_message_sender import AbstractOSCMessageSender
from oscartnetdaemon.components.osc.server_abstract import AbstractOSCServer

from oscartnetdaemon.core.configuration import Configuration
from oscartnetdaemon.core.osc.state_model import OSCStateModel

from oscartnetdaemon.python_extensions.singleton_metaclass import SingletonMetaclass


@dataclass
class Components(metaclass=SingletonMetaclass):
    #
    # Services
    artnet_servers: list[ArtnetServer] = field(default_factory=list)
    discovery: AbstractDiscovery = None
    fixture_updater: AbstractFixturesUpdater = None
    mood_store: AbstractMoodStore = None
    osc_server: AbstractOSCServer = None
    osc_message_sender: AbstractOSCMessageSender = None

    #
    # Models
    configuration: Configuration = None
    osc_state_model: OSCStateModel = field(default_factory=OSCStateModel)
