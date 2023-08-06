"""
Type annotations for backup-gateway service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_backup_gateway.client import BackupGatewayClient

    session = get_session()
    async with session.create_client("backup-gateway") as client:
        client: BackupGatewayClient
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import ListGatewaysPaginator, ListHypervisorsPaginator, ListVirtualMachinesPaginator
from .type_defs import (
    AssociateGatewayToServerOutputTypeDef,
    CreateGatewayOutputTypeDef,
    DeleteGatewayOutputTypeDef,
    DeleteHypervisorOutputTypeDef,
    DisassociateGatewayFromServerOutputTypeDef,
    ImportHypervisorConfigurationOutputTypeDef,
    ListGatewaysOutputTypeDef,
    ListHypervisorsOutputTypeDef,
    ListTagsForResourceOutputTypeDef,
    ListVirtualMachinesOutputTypeDef,
    PutMaintenanceStartTimeOutputTypeDef,
    TagResourceOutputTypeDef,
    TagTypeDef,
    UntagResourceOutputTypeDef,
    UpdateGatewayInformationOutputTypeDef,
    UpdateHypervisorOutputTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("BackupGatewayClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class BackupGatewayClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway.html#BackupGateway.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        BackupGatewayClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway.html#BackupGateway.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/client/#exceptions)
        """

    async def associate_gateway_to_server(
        self, *, GatewayArn: str, ServerArn: str
    ) -> AssociateGatewayToServerOutputTypeDef:
        """
        Associates a backup gateway with your server.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway.html#BackupGateway.Client.associate_gateway_to_server)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/client/#associate_gateway_to_server)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway.html#BackupGateway.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/client/#can_paginate)
        """

    async def create_gateway(
        self,
        *,
        ActivationKey: str,
        GatewayDisplayName: str,
        GatewayType: Literal["BACKUP_VM"],
        Tags: Sequence["TagTypeDef"] = ...
    ) -> CreateGatewayOutputTypeDef:
        """
        Creates a backup gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway.html#BackupGateway.Client.create_gateway)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/client/#create_gateway)
        """

    async def delete_gateway(self, *, GatewayArn: str) -> DeleteGatewayOutputTypeDef:
        """
        Deletes a backup gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway.html#BackupGateway.Client.delete_gateway)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/client/#delete_gateway)
        """

    async def delete_hypervisor(self, *, HypervisorArn: str) -> DeleteHypervisorOutputTypeDef:
        """
        Deletes a hypervisor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway.html#BackupGateway.Client.delete_hypervisor)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/client/#delete_hypervisor)
        """

    async def disassociate_gateway_from_server(
        self, *, GatewayArn: str
    ) -> DisassociateGatewayFromServerOutputTypeDef:
        """
        Disassociates a backup gateway from the specified server.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway.html#BackupGateway.Client.disassociate_gateway_from_server)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/client/#disassociate_gateway_from_server)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway.html#BackupGateway.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/client/#generate_presigned_url)
        """

    async def import_hypervisor_configuration(
        self,
        *,
        Host: str,
        Name: str,
        KmsKeyArn: str = ...,
        Password: str = ...,
        Tags: Sequence["TagTypeDef"] = ...,
        Username: str = ...
    ) -> ImportHypervisorConfigurationOutputTypeDef:
        """
        Connect to a hypervisor by importing its configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway.html#BackupGateway.Client.import_hypervisor_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/client/#import_hypervisor_configuration)
        """

    async def list_gateways(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListGatewaysOutputTypeDef:
        """
        Lists backup gateways owned by an Amazon Web Services account in an Amazon Web
        Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway.html#BackupGateway.Client.list_gateways)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/client/#list_gateways)
        """

    async def list_hypervisors(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListHypervisorsOutputTypeDef:
        """
        Lists your hypervisors.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway.html#BackupGateway.Client.list_hypervisors)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/client/#list_hypervisors)
        """

    async def list_tags_for_resource(self, *, ResourceArn: str) -> ListTagsForResourceOutputTypeDef:
        """
        Lists the tags applied to the resource identified by its Amazon Resource Name
        (ARN).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway.html#BackupGateway.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/client/#list_tags_for_resource)
        """

    async def list_virtual_machines(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListVirtualMachinesOutputTypeDef:
        """
        Lists your virtual machines.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway.html#BackupGateway.Client.list_virtual_machines)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/client/#list_virtual_machines)
        """

    async def put_maintenance_start_time(
        self,
        *,
        GatewayArn: str,
        HourOfDay: int,
        MinuteOfHour: int,
        DayOfMonth: int = ...,
        DayOfWeek: int = ...
    ) -> PutMaintenanceStartTimeOutputTypeDef:
        """
        Set the maintenance start time for a gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway.html#BackupGateway.Client.put_maintenance_start_time)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/client/#put_maintenance_start_time)
        """

    async def tag_resource(
        self, *, ResourceARN: str, Tags: Sequence["TagTypeDef"]
    ) -> TagResourceOutputTypeDef:
        """
        Tag the resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway.html#BackupGateway.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/client/#tag_resource)
        """

    async def test_hypervisor_configuration(
        self, *, GatewayArn: str, Host: str, Password: str = ..., Username: str = ...
    ) -> Dict[str, Any]:
        """
        Tests your hypervisor configuration to validate that backup gateway can connect
        with the hypervisor and its resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway.html#BackupGateway.Client.test_hypervisor_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/client/#test_hypervisor_configuration)
        """

    async def untag_resource(
        self, *, ResourceARN: str, TagKeys: Sequence[str]
    ) -> UntagResourceOutputTypeDef:
        """
        Removes tags from the resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway.html#BackupGateway.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/client/#untag_resource)
        """

    async def update_gateway_information(
        self, *, GatewayArn: str, GatewayDisplayName: str = ...
    ) -> UpdateGatewayInformationOutputTypeDef:
        """
        Updates a gateway's name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway.html#BackupGateway.Client.update_gateway_information)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/client/#update_gateway_information)
        """

    async def update_hypervisor(
        self, *, HypervisorArn: str, Host: str = ..., Password: str = ..., Username: str = ...
    ) -> UpdateHypervisorOutputTypeDef:
        """
        Updates a hypervisor metadata, including its host, username, and password.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway.html#BackupGateway.Client.update_hypervisor)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/client/#update_hypervisor)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_gateways"]) -> ListGatewaysPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway.html#BackupGateway.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_hypervisors"]
    ) -> ListHypervisorsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway.html#BackupGateway.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_virtual_machines"]
    ) -> ListVirtualMachinesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway.html#BackupGateway.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/client/#get_paginator)
        """

    async def __aenter__(self) -> "BackupGatewayClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway.html#BackupGateway.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup-gateway.html#BackupGateway.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup_gateway/client/)
        """
