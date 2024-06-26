from oscartnetdaemon.components.main import Main

from oscartnetdaemon.aa.io import AAIO
from oscartnetdaemon.aa.configuration_loader import AAConfigurationLoader
from oscartnetdaemon.domain_contract.service_registration_info import ServiceRegistrationInfo
from oscartnetdaemon.domain_contract.variable_type_enum import VariableType
from oscartnetdaemon.aa.variable.float import AAFloat


if __name__ == '__main__':
    main = Main()

    aa_configuration_loader = AAConfigurationLoader(filepath="")
    main.register_io_service(ServiceRegistrationInfo(
        configuration_loader=aa_configuration_loader,
        io_type=AAIO,
        variable_types={
            VariableType.Float: AAFloat
        }
    ))

    main.exec()
