"""
Type annotations for workspaces service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_workspaces.client import WorkSpacesClient

    session = get_session()
    async with session.create_client("workspaces") as client:
        client: WorkSpacesClient
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import (
    ApplicationType,
    ImageTypeType,
    TargetWorkspaceStateType,
    TenancyType,
    WorkspaceImageIngestionProcessType,
)
from .paginator import (
    DescribeAccountModificationsPaginator,
    DescribeIpGroupsPaginator,
    DescribeWorkspaceBundlesPaginator,
    DescribeWorkspaceDirectoriesPaginator,
    DescribeWorkspaceImagesPaginator,
    DescribeWorkspacesConnectionStatusPaginator,
    DescribeWorkspacesPaginator,
    ListAvailableManagementCidrRangesPaginator,
)
from .type_defs import (
    AssociateConnectionAliasResultTypeDef,
    ClientPropertiesTypeDef,
    ComputeTypeTypeDef,
    ConnectionAliasPermissionTypeDef,
    CopyWorkspaceImageResultTypeDef,
    CreateConnectClientAddInResultTypeDef,
    CreateConnectionAliasResultTypeDef,
    CreateIpGroupResultTypeDef,
    CreateUpdatedWorkspaceImageResultTypeDef,
    CreateWorkspaceBundleResultTypeDef,
    CreateWorkspacesResultTypeDef,
    DescribeAccountModificationsResultTypeDef,
    DescribeAccountResultTypeDef,
    DescribeClientPropertiesResultTypeDef,
    DescribeConnectClientAddInsResultTypeDef,
    DescribeConnectionAliasesResultTypeDef,
    DescribeConnectionAliasPermissionsResultTypeDef,
    DescribeIpGroupsResultTypeDef,
    DescribeTagsResultTypeDef,
    DescribeWorkspaceBundlesResultTypeDef,
    DescribeWorkspaceDirectoriesResultTypeDef,
    DescribeWorkspaceImagePermissionsResultTypeDef,
    DescribeWorkspaceImagesResultTypeDef,
    DescribeWorkspacesConnectionStatusResultTypeDef,
    DescribeWorkspaceSnapshotsResultTypeDef,
    DescribeWorkspacesResultTypeDef,
    ImportWorkspaceImageResultTypeDef,
    IpRuleItemTypeDef,
    ListAvailableManagementCidrRangesResultTypeDef,
    MigrateWorkspaceResultTypeDef,
    RebootRequestTypeDef,
    RebootWorkspacesResultTypeDef,
    RebuildRequestTypeDef,
    RebuildWorkspacesResultTypeDef,
    RootStorageTypeDef,
    SelfservicePermissionsTypeDef,
    StartRequestTypeDef,
    StartWorkspacesResultTypeDef,
    StopRequestTypeDef,
    StopWorkspacesResultTypeDef,
    TagTypeDef,
    TerminateRequestTypeDef,
    TerminateWorkspacesResultTypeDef,
    UserStorageTypeDef,
    WorkspaceAccessPropertiesTypeDef,
    WorkspaceCreationPropertiesTypeDef,
    WorkspacePropertiesTypeDef,
    WorkspaceRequestTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("WorkSpacesClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    InvalidParameterValuesException: Type[BotocoreClientError]
    InvalidResourceStateException: Type[BotocoreClientError]
    OperationInProgressException: Type[BotocoreClientError]
    OperationNotSupportedException: Type[BotocoreClientError]
    ResourceAlreadyExistsException: Type[BotocoreClientError]
    ResourceAssociatedException: Type[BotocoreClientError]
    ResourceCreationFailedException: Type[BotocoreClientError]
    ResourceLimitExceededException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ResourceUnavailableException: Type[BotocoreClientError]
    UnsupportedNetworkConfigurationException: Type[BotocoreClientError]
    UnsupportedWorkspaceConfigurationException: Type[BotocoreClientError]
    WorkspacesDefaultRoleNotFoundException: Type[BotocoreClientError]


class WorkSpacesClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        WorkSpacesClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/client/#exceptions)
        """

    async def associate_connection_alias(
        self, *, AliasId: str, ResourceId: str
    ) -> AssociateConnectionAliasResultTypeDef:
        """
        Associates the specified connection alias with the specified directory to enable
        cross-Region redirection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client.associate_connection_alias)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/client/#associate_connection_alias)
        """

    async def associate_ip_groups(
        self, *, DirectoryId: str, GroupIds: Sequence[str]
    ) -> Dict[str, Any]:
        """
        Associates the specified IP access control group with the specified directory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client.associate_ip_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/client/#associate_ip_groups)
        """

    async def authorize_ip_rules(
        self, *, GroupId: str, UserRules: Sequence["IpRuleItemTypeDef"]
    ) -> Dict[str, Any]:
        """
        Adds one or more rules to the specified IP access control group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client.authorize_ip_rules)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/client/#authorize_ip_rules)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/client/#can_paginate)
        """

    async def copy_workspace_image(
        self,
        *,
        Name: str,
        SourceImageId: str,
        SourceRegion: str,
        Description: str = ...,
        Tags: Sequence["TagTypeDef"] = ...
    ) -> CopyWorkspaceImageResultTypeDef:
        """
        Copies the specified image from the specified Region to the current Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client.copy_workspace_image)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/client/#copy_workspace_image)
        """

    async def create_connect_client_add_in(
        self, *, ResourceId: str, Name: str, URL: str
    ) -> CreateConnectClientAddInResultTypeDef:
        """
        Creates a client-add-in for Amazon Connect within a directory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client.create_connect_client_add_in)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/client/#create_connect_client_add_in)
        """

    async def create_connection_alias(
        self, *, ConnectionString: str, Tags: Sequence["TagTypeDef"] = ...
    ) -> CreateConnectionAliasResultTypeDef:
        """
        Creates the specified connection alias for use with cross-Region redirection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client.create_connection_alias)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/client/#create_connection_alias)
        """

    async def create_ip_group(
        self,
        *,
        GroupName: str,
        GroupDesc: str = ...,
        UserRules: Sequence["IpRuleItemTypeDef"] = ...,
        Tags: Sequence["TagTypeDef"] = ...
    ) -> CreateIpGroupResultTypeDef:
        """
        Creates an IP access control group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client.create_ip_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/client/#create_ip_group)
        """

    async def create_tags(self, *, ResourceId: str, Tags: Sequence["TagTypeDef"]) -> Dict[str, Any]:
        """
        Creates the specified tags for the specified WorkSpaces resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/client/#create_tags)
        """

    async def create_updated_workspace_image(
        self, *, Name: str, Description: str, SourceImageId: str, Tags: Sequence["TagTypeDef"] = ...
    ) -> CreateUpdatedWorkspaceImageResultTypeDef:
        """
        Creates a new updated WorkSpace image based on the specified source image.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client.create_updated_workspace_image)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/client/#create_updated_workspace_image)
        """

    async def create_workspace_bundle(
        self,
        *,
        BundleName: str,
        BundleDescription: str,
        ImageId: str,
        ComputeType: "ComputeTypeTypeDef",
        UserStorage: "UserStorageTypeDef",
        RootStorage: "RootStorageTypeDef" = ...,
        Tags: Sequence["TagTypeDef"] = ...
    ) -> CreateWorkspaceBundleResultTypeDef:
        """
        Creates the specified WorkSpace bundle.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client.create_workspace_bundle)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/client/#create_workspace_bundle)
        """

    async def create_workspaces(
        self, *, Workspaces: Sequence["WorkspaceRequestTypeDef"]
    ) -> CreateWorkspacesResultTypeDef:
        """
        Creates one or more WorkSpaces.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client.create_workspaces)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/client/#create_workspaces)
        """

    async def delete_connect_client_add_in(
        self, *, AddInId: str, ResourceId: str
    ) -> Dict[str, Any]:
        """
        Deletes a client-add-in for Amazon Connect that is configured within a
        directory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client.delete_connect_client_add_in)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/client/#delete_connect_client_add_in)
        """

    async def delete_connection_alias(self, *, AliasId: str) -> Dict[str, Any]:
        """
        Deletes the specified connection alias.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client.delete_connection_alias)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/client/#delete_connection_alias)
        """

    async def delete_ip_group(self, *, GroupId: str) -> Dict[str, Any]:
        """
        Deletes the specified IP access control group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client.delete_ip_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/client/#delete_ip_group)
        """

    async def delete_tags(self, *, ResourceId: str, TagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Deletes the specified tags from the specified WorkSpaces resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client.delete_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/client/#delete_tags)
        """

    async def delete_workspace_bundle(self, *, BundleId: str = ...) -> Dict[str, Any]:
        """
        Deletes the specified WorkSpace bundle.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client.delete_workspace_bundle)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/client/#delete_workspace_bundle)
        """

    async def delete_workspace_image(self, *, ImageId: str) -> Dict[str, Any]:
        """
        Deletes the specified image from your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client.delete_workspace_image)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/client/#delete_workspace_image)
        """

    async def deregister_workspace_directory(self, *, DirectoryId: str) -> Dict[str, Any]:
        """
        Deregisters the specified directory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client.deregister_workspace_directory)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/client/#deregister_workspace_directory)
        """

    async def describe_account(self) -> DescribeAccountResultTypeDef:
        """
        Retrieves a list that describes the configuration of Bring Your Own License
        (BYOL) for the specified account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client.describe_account)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/client/#describe_account)
        """

    async def describe_account_modifications(
        self, *, NextToken: str = ...
    ) -> DescribeAccountModificationsResultTypeDef:
        """
        Retrieves a list that describes modifications to the configuration of Bring Your
        Own License (BYOL) for the specified account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client.describe_account_modifications)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/client/#describe_account_modifications)
        """

    async def describe_client_properties(
        self, *, ResourceIds: Sequence[str]
    ) -> DescribeClientPropertiesResultTypeDef:
        """
        Retrieves a list that describes one or more specified Amazon WorkSpaces clients.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client.describe_client_properties)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/client/#describe_client_properties)
        """

    async def describe_connect_client_add_ins(
        self, *, ResourceId: str, NextToken: str = ..., MaxResults: int = ...
    ) -> DescribeConnectClientAddInsResultTypeDef:
        """
        Retrieves a list of Amazon Connect client add-ins that have been created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client.describe_connect_client_add_ins)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/client/#describe_connect_client_add_ins)
        """

    async def describe_connection_alias_permissions(
        self, *, AliasId: str, NextToken: str = ..., MaxResults: int = ...
    ) -> DescribeConnectionAliasPermissionsResultTypeDef:
        """
        Describes the permissions that the owner of a connection alias has granted to
        another Amazon Web Services account for the specified connection alias.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client.describe_connection_alias_permissions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/client/#describe_connection_alias_permissions)
        """

    async def describe_connection_aliases(
        self,
        *,
        AliasIds: Sequence[str] = ...,
        ResourceId: str = ...,
        Limit: int = ...,
        NextToken: str = ...
    ) -> DescribeConnectionAliasesResultTypeDef:
        """
        Retrieves a list that describes the connection aliases used for cross-Region
        redirection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client.describe_connection_aliases)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/client/#describe_connection_aliases)
        """

    async def describe_ip_groups(
        self, *, GroupIds: Sequence[str] = ..., NextToken: str = ..., MaxResults: int = ...
    ) -> DescribeIpGroupsResultTypeDef:
        """
        Describes one or more of your IP access control groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client.describe_ip_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/client/#describe_ip_groups)
        """

    async def describe_tags(self, *, ResourceId: str) -> DescribeTagsResultTypeDef:
        """
        Describes the specified tags for the specified WorkSpaces resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client.describe_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/client/#describe_tags)
        """

    async def describe_workspace_bundles(
        self, *, BundleIds: Sequence[str] = ..., Owner: str = ..., NextToken: str = ...
    ) -> DescribeWorkspaceBundlesResultTypeDef:
        """
        Retrieves a list that describes the available WorkSpace bundles.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client.describe_workspace_bundles)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/client/#describe_workspace_bundles)
        """

    async def describe_workspace_directories(
        self, *, DirectoryIds: Sequence[str] = ..., Limit: int = ..., NextToken: str = ...
    ) -> DescribeWorkspaceDirectoriesResultTypeDef:
        """
        Describes the available directories that are registered with Amazon WorkSpaces.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client.describe_workspace_directories)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/client/#describe_workspace_directories)
        """

    async def describe_workspace_image_permissions(
        self, *, ImageId: str, NextToken: str = ..., MaxResults: int = ...
    ) -> DescribeWorkspaceImagePermissionsResultTypeDef:
        """
        Describes the permissions that the owner of an image has granted to other Amazon
        Web Services accounts for an image.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client.describe_workspace_image_permissions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/client/#describe_workspace_image_permissions)
        """

    async def describe_workspace_images(
        self,
        *,
        ImageIds: Sequence[str] = ...,
        ImageType: ImageTypeType = ...,
        NextToken: str = ...,
        MaxResults: int = ...
    ) -> DescribeWorkspaceImagesResultTypeDef:
        """
        Retrieves a list that describes one or more specified images, if the image
        identifiers are provided.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client.describe_workspace_images)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/client/#describe_workspace_images)
        """

    async def describe_workspace_snapshots(
        self, *, WorkspaceId: str
    ) -> DescribeWorkspaceSnapshotsResultTypeDef:
        """
        Describes the snapshots for the specified WorkSpace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client.describe_workspace_snapshots)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/client/#describe_workspace_snapshots)
        """

    async def describe_workspaces(
        self,
        *,
        WorkspaceIds: Sequence[str] = ...,
        DirectoryId: str = ...,
        UserName: str = ...,
        BundleId: str = ...,
        Limit: int = ...,
        NextToken: str = ...
    ) -> DescribeWorkspacesResultTypeDef:
        """
        Describes the specified WorkSpaces.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client.describe_workspaces)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/client/#describe_workspaces)
        """

    async def describe_workspaces_connection_status(
        self, *, WorkspaceIds: Sequence[str] = ..., NextToken: str = ...
    ) -> DescribeWorkspacesConnectionStatusResultTypeDef:
        """
        Describes the connection status of the specified WorkSpaces.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client.describe_workspaces_connection_status)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/client/#describe_workspaces_connection_status)
        """

    async def disassociate_connection_alias(self, *, AliasId: str) -> Dict[str, Any]:
        """
        Disassociates a connection alias from a directory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client.disassociate_connection_alias)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/client/#disassociate_connection_alias)
        """

    async def disassociate_ip_groups(
        self, *, DirectoryId: str, GroupIds: Sequence[str]
    ) -> Dict[str, Any]:
        """
        Disassociates the specified IP access control group from the specified
        directory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client.disassociate_ip_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/client/#disassociate_ip_groups)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/client/#generate_presigned_url)
        """

    async def import_workspace_image(
        self,
        *,
        Ec2ImageId: str,
        IngestionProcess: WorkspaceImageIngestionProcessType,
        ImageName: str,
        ImageDescription: str,
        Tags: Sequence["TagTypeDef"] = ...,
        Applications: Sequence[ApplicationType] = ...
    ) -> ImportWorkspaceImageResultTypeDef:
        """
        Imports the specified Windows 10 Bring Your Own License (BYOL) image into Amazon
        WorkSpaces.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client.import_workspace_image)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/client/#import_workspace_image)
        """

    async def list_available_management_cidr_ranges(
        self, *, ManagementCidrRangeConstraint: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListAvailableManagementCidrRangesResultTypeDef:
        """
        Retrieves a list of IP address ranges, specified as IPv4 CIDR blocks, that you
        can use for the network management interface when you enable Bring Your Own
        License (BYOL).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client.list_available_management_cidr_ranges)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/client/#list_available_management_cidr_ranges)
        """

    async def migrate_workspace(
        self, *, SourceWorkspaceId: str, BundleId: str
    ) -> MigrateWorkspaceResultTypeDef:
        """
        Migrates a WorkSpace from one operating system or bundle type to another, while
        retaining the data on the user volume.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client.migrate_workspace)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/client/#migrate_workspace)
        """

    async def modify_account(
        self,
        *,
        DedicatedTenancySupport: Literal["ENABLED"] = ...,
        DedicatedTenancyManagementCidrRange: str = ...
    ) -> Dict[str, Any]:
        """
        Modifies the configuration of Bring Your Own License (BYOL) for the specified
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client.modify_account)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/client/#modify_account)
        """

    async def modify_client_properties(
        self, *, ResourceId: str, ClientProperties: "ClientPropertiesTypeDef"
    ) -> Dict[str, Any]:
        """
        Modifies the properties of the specified Amazon WorkSpaces clients.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client.modify_client_properties)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/client/#modify_client_properties)
        """

    async def modify_selfservice_permissions(
        self, *, ResourceId: str, SelfservicePermissions: "SelfservicePermissionsTypeDef"
    ) -> Dict[str, Any]:
        """
        Modifies the self-service WorkSpace management capabilities for your users.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client.modify_selfservice_permissions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/client/#modify_selfservice_permissions)
        """

    async def modify_workspace_access_properties(
        self, *, ResourceId: str, WorkspaceAccessProperties: "WorkspaceAccessPropertiesTypeDef"
    ) -> Dict[str, Any]:
        """
        Specifies which devices and operating systems users can use to access their
        WorkSpaces.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client.modify_workspace_access_properties)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/client/#modify_workspace_access_properties)
        """

    async def modify_workspace_creation_properties(
        self, *, ResourceId: str, WorkspaceCreationProperties: "WorkspaceCreationPropertiesTypeDef"
    ) -> Dict[str, Any]:
        """
        Modify the default properties used to create WorkSpaces.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client.modify_workspace_creation_properties)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/client/#modify_workspace_creation_properties)
        """

    async def modify_workspace_properties(
        self, *, WorkspaceId: str, WorkspaceProperties: "WorkspacePropertiesTypeDef"
    ) -> Dict[str, Any]:
        """
        Modifies the specified WorkSpace properties.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client.modify_workspace_properties)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/client/#modify_workspace_properties)
        """

    async def modify_workspace_state(
        self, *, WorkspaceId: str, WorkspaceState: TargetWorkspaceStateType
    ) -> Dict[str, Any]:
        """
        Sets the state of the specified WorkSpace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client.modify_workspace_state)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/client/#modify_workspace_state)
        """

    async def reboot_workspaces(
        self, *, RebootWorkspaceRequests: Sequence["RebootRequestTypeDef"]
    ) -> RebootWorkspacesResultTypeDef:
        """
        Reboots the specified WorkSpaces.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client.reboot_workspaces)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/client/#reboot_workspaces)
        """

    async def rebuild_workspaces(
        self, *, RebuildWorkspaceRequests: Sequence["RebuildRequestTypeDef"]
    ) -> RebuildWorkspacesResultTypeDef:
        """
        Rebuilds the specified WorkSpace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client.rebuild_workspaces)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/client/#rebuild_workspaces)
        """

    async def register_workspace_directory(
        self,
        *,
        DirectoryId: str,
        EnableWorkDocs: bool,
        SubnetIds: Sequence[str] = ...,
        EnableSelfService: bool = ...,
        Tenancy: TenancyType = ...,
        Tags: Sequence["TagTypeDef"] = ...
    ) -> Dict[str, Any]:
        """
        Registers the specified directory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client.register_workspace_directory)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/client/#register_workspace_directory)
        """

    async def restore_workspace(self, *, WorkspaceId: str) -> Dict[str, Any]:
        """
        Restores the specified WorkSpace to its last known healthy state.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client.restore_workspace)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/client/#restore_workspace)
        """

    async def revoke_ip_rules(self, *, GroupId: str, UserRules: Sequence[str]) -> Dict[str, Any]:
        """
        Removes one or more rules from the specified IP access control group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client.revoke_ip_rules)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/client/#revoke_ip_rules)
        """

    async def start_workspaces(
        self, *, StartWorkspaceRequests: Sequence["StartRequestTypeDef"]
    ) -> StartWorkspacesResultTypeDef:
        """
        Starts the specified WorkSpaces.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client.start_workspaces)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/client/#start_workspaces)
        """

    async def stop_workspaces(
        self, *, StopWorkspaceRequests: Sequence["StopRequestTypeDef"]
    ) -> StopWorkspacesResultTypeDef:
        """
        Stops the specified WorkSpaces.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client.stop_workspaces)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/client/#stop_workspaces)
        """

    async def terminate_workspaces(
        self, *, TerminateWorkspaceRequests: Sequence["TerminateRequestTypeDef"]
    ) -> TerminateWorkspacesResultTypeDef:
        """
        Terminates the specified WorkSpaces.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client.terminate_workspaces)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/client/#terminate_workspaces)
        """

    async def update_connect_client_add_in(
        self, *, AddInId: str, ResourceId: str, Name: str = ..., URL: str = ...
    ) -> Dict[str, Any]:
        """
        Updates a Amazon Connect client add-in.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client.update_connect_client_add_in)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/client/#update_connect_client_add_in)
        """

    async def update_connection_alias_permission(
        self, *, AliasId: str, ConnectionAliasPermission: "ConnectionAliasPermissionTypeDef"
    ) -> Dict[str, Any]:
        """
        Shares or unshares a connection alias with one account by specifying whether
        that account has permission to associate the connection alias with a directory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client.update_connection_alias_permission)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/client/#update_connection_alias_permission)
        """

    async def update_rules_of_ip_group(
        self, *, GroupId: str, UserRules: Sequence["IpRuleItemTypeDef"]
    ) -> Dict[str, Any]:
        """
        Replaces the current rules of the specified IP access control group with the
        specified rules.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client.update_rules_of_ip_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/client/#update_rules_of_ip_group)
        """

    async def update_workspace_bundle(
        self, *, BundleId: str = ..., ImageId: str = ...
    ) -> Dict[str, Any]:
        """
        Updates a WorkSpace bundle with a new image.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client.update_workspace_bundle)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/client/#update_workspace_bundle)
        """

    async def update_workspace_image_permission(
        self, *, ImageId: str, AllowCopyImage: bool, SharedAccountId: str
    ) -> Dict[str, Any]:
        """
        Shares or unshares an image with one account in the same Amazon Web Services
        Region by specifying whether that account has permission to copy the image.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client.update_workspace_image_permission)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/client/#update_workspace_image_permission)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_account_modifications"]
    ) -> DescribeAccountModificationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_ip_groups"]
    ) -> DescribeIpGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_workspace_bundles"]
    ) -> DescribeWorkspaceBundlesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_workspace_directories"]
    ) -> DescribeWorkspaceDirectoriesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_workspace_images"]
    ) -> DescribeWorkspaceImagesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_workspaces"]
    ) -> DescribeWorkspacesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_workspaces_connection_status"]
    ) -> DescribeWorkspacesConnectionStatusPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_available_management_cidr_ranges"]
    ) -> ListAvailableManagementCidrRangesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/client/#get_paginator)
        """

    async def __aenter__(self) -> "WorkSpacesClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces.html#WorkSpaces.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/client/)
        """
