from simpledmxconsole.fixture.base_definition import BaseFixtureDefinition
from simpledmxconsole.fixture.dmx_channel import DMXChannel, DMXChannelFloat


class VarytecHeroWash300FC(BaseFixtureDefinition):
    Channels = [
        DMXChannelFloat("Pan"),  # 1 2
        DMXChannelFloat("Tilt"),  # 3 4
        DMXChannel("Speed"),  # 5
        DMXChannel("Zoom"),  # 6
        DMXChannel("Dimmer", value_default=255),  # 7
        DMXChannel("Strobe", value_default=255),  # 8
        DMXChannel('Red 1'),  # 9
        DMXChannel('Green 1'),  # 10
        DMXChannel('Blue 1'),  # 11
        DMXChannel('White 1'),  # 12
        DMXChannel('Red 2'),  # 13
        DMXChannel('Green 2'),  # 14
        DMXChannel('Blue 2'),  # 15
        DMXChannel('White 2'),  # 16
        DMXChannel('Red 3'),  # 17
        DMXChannel('Green 3'),  # 18
        DMXChannel('Blue 3'),  # 19
        DMXChannel('White 3'),  # 20
        DMXChannel('Color Temperature', unused=True),  # 21
        DMXChannel('Color Macro', unused=True),  # 22
        DMXChannel('Segment Pattern', unused=True),  # 23
        DMXChannel('Segment Transition', unused=True),  # 24
        DMXChannel('Zoom Auto', unused=True),  # 25
        DMXChannel('Pan-Tilt Auto', unused=True),  # 26
    ]
