import yaml

from oscartnetdaemon.components.osc.argument_parser import parse_command_line_args
from oscartnetdaemon.components.osc.configuration import OSCConfiguration
from oscartnetdaemon.components.osc.recall.recall_group_info import OSCRecallGroupInfo
from oscartnetdaemon.components.osc.variable_info import OSCVariableInfo
from oscartnetdaemon.domain_contract.abstract_configuration_loader import AbstractConfigurationLoader
from oscartnetdaemon.domain_contract.variable_type_enum import VariableType
from oscartnetdaemon.components.osc.recall.recall_group_repository import OSCRecallGroupRepository


class OSCConfigurationLoader(AbstractConfigurationLoader):
    """
    At least returns a BaseConfiguration object
    Subtype of BaseConfiguration can be created to load additional IO specific configuration
    """

    def __init__(self, filepaths):
        self.filepaths = parse_command_line_args()
        self.files_content: list[dict] = list()
        self.root_params: dict[str: str | bool | int] = dict()
        self.variables: dict[str, OSCVariableInfo] = dict()
        self.recall_groups: dict[str, OSCRecallGroupInfo] = dict()

    def load(self) -> OSCConfiguration:
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
        self.files_content = list()
        self.root_params = dict()

        for filepath in self.filepaths:
            with open(filepath, 'r') as file:
                content = yaml.safe_load(file)
                self.files_content.append(content)
                self.root_params.update(content)

        self.root_params.pop('variables', None)
        self.root_params.pop('recall-groups', None)

    def load_variables(self):
        self.variables = dict()

        for content in self.files_content:
            for variable_dict in content['variables']:
                if variable_dict['name'] in self.variables:
                    raise ValueError(f"Variable '{variable_dict['name']}' already assigned")
                self.variables[variable_dict['name']] = OSCVariableInfo.from_dict(variable_dict)

    def load_recall_groups(self):
        self.recall_groups = dict()

        for content in self.files_content:
            for recall_group_dict in content.get('recall-groups', list()):
                if recall_group_dict['name'] in self.recall_groups:
                    raise ValueError(f"Recall group '{recall_group_dict['name']}' already assigned")

                new_recall_group = OSCRecallGroupInfo(
                    name=recall_group_dict['name'],
                    target_variables=dict(),
                    recall_slots=dict()
                )

                for variable_name in recall_group_dict['variables']:
                    if variable_name not in self.variables:
                        raise ValueError(f"Variable '{variable_name}' not found")

                    variable = self.variables[variable_name]
                    if variable.type == VariableType.RecallSlot:
                        variable.is_recall_slot = True
                        variable.recall_group_name = new_recall_group.name
                        new_recall_group.recall_slots[variable_name] = variable
                    else:
                        new_recall_group.target_variables[variable_name] = variable

                self.recall_groups[new_recall_group.name] = new_recall_group

        OSCRecallGroupRepository().create_groups(self.recall_groups)
