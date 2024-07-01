from simpledmxconsole.fixture.definition.varytec_hero_wash_300_fc import VarytecHeroWash300FC


class FixtureRepository:

    def __init__(self):
        self.fixtures = [
            VarytecHeroWash300FC(),
            VarytecHeroWash300FC()
        ]

        start_channel = 1
        for fixture in self.fixtures:
            fixture.create_channels(start_channel)
            start_channel += len(fixture.Channels) + 2
