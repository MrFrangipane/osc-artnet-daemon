import yaml

from oscartnetdaemon.components.new_osc.configuration import OSCConfiguration
from oscartnetdaemon.components.new_osc.variable_info import OSCVariableInfo
from oscartnetdaemon.domain_contract.abstract_configuration_loader import AbstractConfigurationLoader
from oscartnetdaemon.components.new_osc.recall.recall_group_info import OSCRecallGroupInfo


class OSCConfigurationLoader(AbstractConfigurationLoader):
    """
    At least returns a BaseConfiguration object
    Subtype of BaseConfiguration can be created to load additional IO specific configuration
    """

    def __init__(self, filepaths):
        super().__init__(filepaths)
        self.files_content: list[dict] = list()
        self.root_params: dict[str: str | bool | int] = dict()
        self.variables: dict[str, OSCVariableInfo] = dict()
        self.recall_groups: dict[str, OSCRecallGroupInfo] = dict()

    def load(self) -> OSCConfiguration:
        self.files_content = list()
        self.root_params = dict()
        self.variables = dict()
        self.recall_groups = dict()

        self.load_files_content()
        self.load_variables()
        self.load_recall_groups()

        return OSCConfiguration(
            server_ip_address=self.root_params['server-ip-address'],
            server_ip_address_autodetect=self.root_params['server-ip-address-autodetect'],
            server_port=self.root_params['server-port'],
            variable_infos=self.variables,
            recall_groups=self.recall_groups
        )

    def load_files_content(self):
        for filepath in self.filepaths:
            with open(filepath, 'r') as file:
                content = yaml.safe_load(file)
                self.files_content.append(content)
                self.root_params.update(content)

        self.root_params.pop('variables')
        self.root_params.pop('recall-groups')

        print(self.root_params)

    def load_variables(self):
        for content in self.files_content:
            for variable_dict in content['variables']:
                if variable_dict['name'] in self.variables:
                    raise ValueError(f"Variable '{variable_dict['name']}' already assigned")
                self.variables[variable_dict['name']] = OSCVariableInfo.from_dict(variable_dict)

    def load_recall_groups(self):
        pass
