import yaml

from oscartnetdaemon.domain_contract.abstract_configuration_loader import AbstractConfigurationLoader
from oscartnetdaemon.components.new_osc.variable_info import OSCVariableInfo
from oscartnetdaemon.components.new_osc.configuration import OSCConfiguration


class OSCConfigurationLoader(AbstractConfigurationLoader):

    def __init__(self, filepaths):
        super().__init__(filepaths)
        self.content = dict()

    def load(self) -> OSCConfiguration:
        variable_infos = list()

        for filepath in self.filepaths:
            with open(filepath, 'r') as file:
                self.content = yaml.safe_load(file)

            for variable_dict in self.content['variables']:
                variable_infos.append(OSCVariableInfo.from_dict(variable_dict))

        return OSCConfiguration(
            server_ip_address=self.content['server-ip-address'],
            server_ip_address_autodetect=self.content['server-ip-address-autodetect'],
            server_port=self.content['server-port'],
            variable_infos=variable_infos
        )
