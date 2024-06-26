import yaml

from oscartnetdaemon.domain_contract.abstract_configuration_loader import AbstractConfigurationLoader
from oscartnetdaemon.components.new_osc.variable_info import OSCVariableInfo
from oscartnetdaemon.components.new_osc.configuration import OSCConfiguration


class OSCConfigurationLoader(AbstractConfigurationLoader):

    def __init__(self, filepath):
        super().__init__(filepath)

    def load(self) -> OSCConfiguration:
        with open(self.filepath, 'r') as file:
            content = yaml.safe_load(file)

        variable_infos = list()
        for variable_dict in content['variables']:
            variable_infos.append(OSCVariableInfo.from_dict(variable_dict))

        return OSCConfiguration(
            server_ip_address=content['server-ip-address'],
            server_ip_address_autodetect=content['server-ip-address-autodetect'],
            server_port=content['server-port'],
            variable_infos=variable_infos
        )
