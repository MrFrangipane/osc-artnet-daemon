from advanceddmxconsole.fixture.dmx_channel import DMXChannel
from advanceddmxconsole.fixture.fixture_info import FixtureInfo
from advanceddmxconsole.program.fixture_snapshot import FixtureSnapshot


class Fixture:

    def __init__(self, info: FixtureInfo):
        self.info: FixtureInfo = info
        self.universe_address: int = -1
        self.channels: list[DMXChannel] = list()

    def create_channels(self, universe_address: int):
        self.universe_address = universe_address

        self.channels = list()
        for channel_number, channel_info in enumerate(self.info.type.channels):
            value_default = float(channel_info.default_int) / 255.0
            new_channel = DMXChannel(
                name=channel_info.name,
                unused=channel_info.unused,
                value=value_default,
                value_default=value_default,
                channel_number=channel_number,
                master_dimmed=channel_info.master_dimmed
            )
            self.channels.append(new_channel)

    def snapshot(self) -> FixtureSnapshot:
        return FixtureSnapshot(
            info=self.info,
            channel_values=[channel.value for channel in self.channels]
        )
