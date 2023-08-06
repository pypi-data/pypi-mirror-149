"""
Type annotations for transfer service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_transfer.client import TransferClient

    session = get_session()
    async with session.create_client("transfer") as client:
        client: TransferClient
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import (
    CustomStepStatusType,
    DomainType,
    EndpointTypeType,
    HomeDirectoryTypeType,
    IdentityProviderTypeType,
    ProtocolType,
)
from .paginator import (
    ListAccessesPaginator,
    ListExecutionsPaginator,
    ListSecurityPoliciesPaginator,
    ListServersPaginator,
    ListTagsForResourcePaginator,
    ListUsersPaginator,
    ListWorkflowsPaginator,
)
from .type_defs import (
    CreateAccessResponseTypeDef,
    CreateServerResponseTypeDef,
    CreateUserResponseTypeDef,
    CreateWorkflowResponseTypeDef,
    DescribeAccessResponseTypeDef,
    DescribeExecutionResponseTypeDef,
    DescribeSecurityPolicyResponseTypeDef,
    DescribeServerResponseTypeDef,
    DescribeUserResponseTypeDef,
    DescribeWorkflowResponseTypeDef,
    EndpointDetailsTypeDef,
    HomeDirectoryMapEntryTypeDef,
    IdentityProviderDetailsTypeDef,
    ImportSshPublicKeyResponseTypeDef,
    ListAccessesResponseTypeDef,
    ListExecutionsResponseTypeDef,
    ListSecurityPoliciesResponseTypeDef,
    ListServersResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListUsersResponseTypeDef,
    ListWorkflowsResponseTypeDef,
    PosixProfileTypeDef,
    ProtocolDetailsTypeDef,
    TagTypeDef,
    TestIdentityProviderResponseTypeDef,
    UpdateAccessResponseTypeDef,
    UpdateServerResponseTypeDef,
    UpdateUserResponseTypeDef,
    WorkflowDetailsTypeDef,
    WorkflowStepTypeDef,
)
from .waiter import ServerOfflineWaiter, ServerOnlineWaiter

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("TransferClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServiceError: Type[BotocoreClientError]
    InvalidNextTokenException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    ResourceExistsException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]


class TransferClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        TransferClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#can_paginate)
        """

    async def create_access(
        self,
        *,
        Role: str,
        ServerId: str,
        ExternalId: str,
        HomeDirectory: str = ...,
        HomeDirectoryType: HomeDirectoryTypeType = ...,
        HomeDirectoryMappings: Sequence["HomeDirectoryMapEntryTypeDef"] = ...,
        Policy: str = ...,
        PosixProfile: "PosixProfileTypeDef" = ...
    ) -> CreateAccessResponseTypeDef:
        """
        Used by administrators to choose which groups in the directory should have
        access to upload and download files over the enabled protocols using Amazon Web
        Services Transfer Family.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.create_access)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#create_access)
        """

    async def create_server(
        self,
        *,
        Certificate: str = ...,
        Domain: DomainType = ...,
        EndpointDetails: "EndpointDetailsTypeDef" = ...,
        EndpointType: EndpointTypeType = ...,
        HostKey: str = ...,
        IdentityProviderDetails: "IdentityProviderDetailsTypeDef" = ...,
        IdentityProviderType: IdentityProviderTypeType = ...,
        LoggingRole: str = ...,
        PostAuthenticationLoginBanner: str = ...,
        PreAuthenticationLoginBanner: str = ...,
        Protocols: Sequence[ProtocolType] = ...,
        ProtocolDetails: "ProtocolDetailsTypeDef" = ...,
        SecurityPolicyName: str = ...,
        Tags: Sequence["TagTypeDef"] = ...,
        WorkflowDetails: "WorkflowDetailsTypeDef" = ...
    ) -> CreateServerResponseTypeDef:
        """
        Instantiates an auto-scaling virtual server based on the selected file transfer
        protocol in Amazon Web Services.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.create_server)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#create_server)
        """

    async def create_user(
        self,
        *,
        Role: str,
        ServerId: str,
        UserName: str,
        HomeDirectory: str = ...,
        HomeDirectoryType: HomeDirectoryTypeType = ...,
        HomeDirectoryMappings: Sequence["HomeDirectoryMapEntryTypeDef"] = ...,
        Policy: str = ...,
        PosixProfile: "PosixProfileTypeDef" = ...,
        SshPublicKeyBody: str = ...,
        Tags: Sequence["TagTypeDef"] = ...
    ) -> CreateUserResponseTypeDef:
        """
        Creates a user and associates them with an existing file transfer protocol-
        enabled server.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.create_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#create_user)
        """

    async def create_workflow(
        self,
        *,
        Steps: Sequence["WorkflowStepTypeDef"],
        Description: str = ...,
        OnExceptionSteps: Sequence["WorkflowStepTypeDef"] = ...,
        Tags: Sequence["TagTypeDef"] = ...
    ) -> CreateWorkflowResponseTypeDef:
        """
        Allows you to create a workflow with specified steps and step details the
        workflow invokes after file transfer completes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.create_workflow)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#create_workflow)
        """

    async def delete_access(self, *, ServerId: str, ExternalId: str) -> None:
        """
        Allows you to delete the access specified in the `ServerID` and `ExternalID`
        parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.delete_access)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#delete_access)
        """

    async def delete_server(self, *, ServerId: str) -> None:
        """
        Deletes the file transfer protocol-enabled server that you specify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.delete_server)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#delete_server)
        """

    async def delete_ssh_public_key(
        self, *, ServerId: str, SshPublicKeyId: str, UserName: str
    ) -> None:
        """
        Deletes a user's Secure Shell (SSH) public key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.delete_ssh_public_key)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#delete_ssh_public_key)
        """

    async def delete_user(self, *, ServerId: str, UserName: str) -> None:
        """
        Deletes the user belonging to a file transfer protocol-enabled server you
        specify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.delete_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#delete_user)
        """

    async def delete_workflow(self, *, WorkflowId: str) -> None:
        """
        Deletes the specified workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.delete_workflow)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#delete_workflow)
        """

    async def describe_access(
        self, *, ServerId: str, ExternalId: str
    ) -> DescribeAccessResponseTypeDef:
        """
        Describes the access that is assigned to the specific file transfer protocol-
        enabled server, as identified by its `ServerId` property and its `ExternalID` .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.describe_access)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#describe_access)
        """

    async def describe_execution(
        self, *, ExecutionId: str, WorkflowId: str
    ) -> DescribeExecutionResponseTypeDef:
        """
        You can use `DescribeExecution` to check the details of the execution of the
        specified workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.describe_execution)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#describe_execution)
        """

    async def describe_security_policy(
        self, *, SecurityPolicyName: str
    ) -> DescribeSecurityPolicyResponseTypeDef:
        """
        Describes the security policy that is attached to your file transfer protocol-
        enabled server.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.describe_security_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#describe_security_policy)
        """

    async def describe_server(self, *, ServerId: str) -> DescribeServerResponseTypeDef:
        """
        Describes a file transfer protocol-enabled server that you specify by passing
        the `ServerId` parameter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.describe_server)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#describe_server)
        """

    async def describe_user(self, *, ServerId: str, UserName: str) -> DescribeUserResponseTypeDef:
        """
        Describes the user assigned to the specific file transfer protocol-enabled
        server, as identified by its `ServerId` property.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.describe_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#describe_user)
        """

    async def describe_workflow(self, *, WorkflowId: str) -> DescribeWorkflowResponseTypeDef:
        """
        Describes the specified workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.describe_workflow)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#describe_workflow)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#generate_presigned_url)
        """

    async def import_ssh_public_key(
        self, *, ServerId: str, SshPublicKeyBody: str, UserName: str
    ) -> ImportSshPublicKeyResponseTypeDef:
        """
        Adds a Secure Shell (SSH) public key to a user account identified by a
        `UserName` value assigned to the specific file transfer protocol-enabled server,
        identified by `ServerId` .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.import_ssh_public_key)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#import_ssh_public_key)
        """

    async def list_accesses(
        self, *, ServerId: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListAccessesResponseTypeDef:
        """
        Lists the details for all the accesses you have on your server.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.list_accesses)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#list_accesses)
        """

    async def list_executions(
        self, *, WorkflowId: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListExecutionsResponseTypeDef:
        """
        Lists all executions for the specified workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.list_executions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#list_executions)
        """

    async def list_security_policies(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListSecurityPoliciesResponseTypeDef:
        """
        Lists the security policies that are attached to your file transfer protocol-
        enabled servers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.list_security_policies)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#list_security_policies)
        """

    async def list_servers(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListServersResponseTypeDef:
        """
        Lists the file transfer protocol-enabled servers that are associated with your
        Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.list_servers)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#list_servers)
        """

    async def list_tags_for_resource(
        self, *, Arn: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists all of the tags associated with the Amazon Resource Name (ARN) that you
        specify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#list_tags_for_resource)
        """

    async def list_users(
        self, *, ServerId: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListUsersResponseTypeDef:
        """
        Lists the users for a file transfer protocol-enabled server that you specify by
        passing the `ServerId` parameter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.list_users)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#list_users)
        """

    async def list_workflows(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListWorkflowsResponseTypeDef:
        """
        Lists all of your workflows.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.list_workflows)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#list_workflows)
        """

    async def send_workflow_step_state(
        self, *, WorkflowId: str, ExecutionId: str, Token: str, Status: CustomStepStatusType
    ) -> Dict[str, Any]:
        """
        Sends a callback for asynchronous custom steps.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.send_workflow_step_state)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#send_workflow_step_state)
        """

    async def start_server(self, *, ServerId: str) -> None:
        """
        Changes the state of a file transfer protocol-enabled server from `OFFLINE` to
        `ONLINE`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.start_server)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#start_server)
        """

    async def stop_server(self, *, ServerId: str) -> None:
        """
        Changes the state of a file transfer protocol-enabled server from `ONLINE` to
        `OFFLINE`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.stop_server)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#stop_server)
        """

    async def tag_resource(self, *, Arn: str, Tags: Sequence["TagTypeDef"]) -> None:
        """
        Attaches a key-value pair to a resource, as identified by its Amazon Resource
        Name (ARN).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#tag_resource)
        """

    async def test_identity_provider(
        self,
        *,
        ServerId: str,
        UserName: str,
        ServerProtocol: ProtocolType = ...,
        SourceIp: str = ...,
        UserPassword: str = ...
    ) -> TestIdentityProviderResponseTypeDef:
        """
        If the `IdentityProviderType` of a file transfer protocol-enabled server is
        `AWS_DIRECTORY_SERVICE` or `API_Gateway` , tests whether your identity provider
        is set up successfully.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.test_identity_provider)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#test_identity_provider)
        """

    async def untag_resource(self, *, Arn: str, TagKeys: Sequence[str]) -> None:
        """
        Detaches a key-value pair from a resource, as identified by its Amazon Resource
        Name (ARN).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#untag_resource)
        """

    async def update_access(
        self,
        *,
        ServerId: str,
        ExternalId: str,
        HomeDirectory: str = ...,
        HomeDirectoryType: HomeDirectoryTypeType = ...,
        HomeDirectoryMappings: Sequence["HomeDirectoryMapEntryTypeDef"] = ...,
        Policy: str = ...,
        PosixProfile: "PosixProfileTypeDef" = ...,
        Role: str = ...
    ) -> UpdateAccessResponseTypeDef:
        """
        Allows you to update parameters for the access specified in the `ServerID` and
        `ExternalID` parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.update_access)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#update_access)
        """

    async def update_server(
        self,
        *,
        ServerId: str,
        Certificate: str = ...,
        ProtocolDetails: "ProtocolDetailsTypeDef" = ...,
        EndpointDetails: "EndpointDetailsTypeDef" = ...,
        EndpointType: EndpointTypeType = ...,
        HostKey: str = ...,
        IdentityProviderDetails: "IdentityProviderDetailsTypeDef" = ...,
        LoggingRole: str = ...,
        PostAuthenticationLoginBanner: str = ...,
        PreAuthenticationLoginBanner: str = ...,
        Protocols: Sequence[ProtocolType] = ...,
        SecurityPolicyName: str = ...,
        WorkflowDetails: "WorkflowDetailsTypeDef" = ...
    ) -> UpdateServerResponseTypeDef:
        """
        Updates the file transfer protocol-enabled server's properties after that server
        has been created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.update_server)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#update_server)
        """

    async def update_user(
        self,
        *,
        ServerId: str,
        UserName: str,
        HomeDirectory: str = ...,
        HomeDirectoryType: HomeDirectoryTypeType = ...,
        HomeDirectoryMappings: Sequence["HomeDirectoryMapEntryTypeDef"] = ...,
        Policy: str = ...,
        PosixProfile: "PosixProfileTypeDef" = ...,
        Role: str = ...
    ) -> UpdateUserResponseTypeDef:
        """
        Assigns new properties to a user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.update_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#update_user)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_accesses"]) -> ListAccessesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_executions"]) -> ListExecutionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_security_policies"]
    ) -> ListSecurityPoliciesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_servers"]) -> ListServersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_tags_for_resource"]
    ) -> ListTagsForResourcePaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_users"]) -> ListUsersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_workflows"]) -> ListWorkflowsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#get_paginator)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["server_offline"]) -> ServerOfflineWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["server_online"]) -> ServerOnlineWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#get_waiter)
        """

    async def __aenter__(self) -> "TransferClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/)
        """
