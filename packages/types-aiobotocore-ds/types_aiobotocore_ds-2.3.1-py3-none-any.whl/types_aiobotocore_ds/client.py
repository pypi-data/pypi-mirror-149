"""
Type annotations for ds service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_ds.client import DirectoryServiceClient

    session = get_session()
    async with session.create_client("ds") as client:
        client: DirectoryServiceClient
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import (
    CertificateTypeType,
    DirectoryEditionType,
    DirectorySizeType,
    SelectiveAuthType,
    ShareMethodType,
    TrustDirectionType,
    TrustTypeType,
)
from .paginator import (
    DescribeDirectoriesPaginator,
    DescribeDomainControllersPaginator,
    DescribeSharedDirectoriesPaginator,
    DescribeSnapshotsPaginator,
    DescribeTrustsPaginator,
    ListIpRoutesPaginator,
    ListLogSubscriptionsPaginator,
    ListSchemaExtensionsPaginator,
    ListTagsForResourcePaginator,
)
from .type_defs import (
    AcceptSharedDirectoryResultTypeDef,
    AttributeTypeDef,
    ClientCertAuthSettingsTypeDef,
    ConnectDirectoryResultTypeDef,
    CreateAliasResultTypeDef,
    CreateComputerResultTypeDef,
    CreateDirectoryResultTypeDef,
    CreateMicrosoftADResultTypeDef,
    CreateSnapshotResultTypeDef,
    CreateTrustResultTypeDef,
    DeleteDirectoryResultTypeDef,
    DeleteSnapshotResultTypeDef,
    DeleteTrustResultTypeDef,
    DescribeCertificateResultTypeDef,
    DescribeClientAuthenticationSettingsResultTypeDef,
    DescribeConditionalForwardersResultTypeDef,
    DescribeDirectoriesResultTypeDef,
    DescribeDomainControllersResultTypeDef,
    DescribeEventTopicsResultTypeDef,
    DescribeLDAPSSettingsResultTypeDef,
    DescribeRegionsResultTypeDef,
    DescribeSharedDirectoriesResultTypeDef,
    DescribeSnapshotsResultTypeDef,
    DescribeTrustsResultTypeDef,
    DirectoryConnectSettingsTypeDef,
    DirectoryVpcSettingsTypeDef,
    GetDirectoryLimitsResultTypeDef,
    GetSnapshotLimitsResultTypeDef,
    IpRouteTypeDef,
    ListCertificatesResultTypeDef,
    ListIpRoutesResultTypeDef,
    ListLogSubscriptionsResultTypeDef,
    ListSchemaExtensionsResultTypeDef,
    ListTagsForResourceResultTypeDef,
    RadiusSettingsTypeDef,
    RegisterCertificateResultTypeDef,
    RejectSharedDirectoryResultTypeDef,
    ShareDirectoryResultTypeDef,
    ShareTargetTypeDef,
    StartSchemaExtensionResultTypeDef,
    TagTypeDef,
    UnshareDirectoryResultTypeDef,
    UnshareTargetTypeDef,
    UpdateTrustResultTypeDef,
    VerifyTrustResultTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("DirectoryServiceClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    AuthenticationFailedException: Type[BotocoreClientError]
    CertificateAlreadyExistsException: Type[BotocoreClientError]
    CertificateDoesNotExistException: Type[BotocoreClientError]
    CertificateInUseException: Type[BotocoreClientError]
    CertificateLimitExceededException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ClientException: Type[BotocoreClientError]
    DirectoryAlreadyInRegionException: Type[BotocoreClientError]
    DirectoryAlreadySharedException: Type[BotocoreClientError]
    DirectoryDoesNotExistException: Type[BotocoreClientError]
    DirectoryLimitExceededException: Type[BotocoreClientError]
    DirectoryNotSharedException: Type[BotocoreClientError]
    DirectoryUnavailableException: Type[BotocoreClientError]
    DomainControllerLimitExceededException: Type[BotocoreClientError]
    EntityAlreadyExistsException: Type[BotocoreClientError]
    EntityDoesNotExistException: Type[BotocoreClientError]
    InsufficientPermissionsException: Type[BotocoreClientError]
    InvalidCertificateException: Type[BotocoreClientError]
    InvalidClientAuthStatusException: Type[BotocoreClientError]
    InvalidLDAPSStatusException: Type[BotocoreClientError]
    InvalidNextTokenException: Type[BotocoreClientError]
    InvalidParameterException: Type[BotocoreClientError]
    InvalidPasswordException: Type[BotocoreClientError]
    InvalidTargetException: Type[BotocoreClientError]
    IpRouteLimitExceededException: Type[BotocoreClientError]
    NoAvailableCertificateException: Type[BotocoreClientError]
    OrganizationsException: Type[BotocoreClientError]
    RegionLimitExceededException: Type[BotocoreClientError]
    ServiceException: Type[BotocoreClientError]
    ShareLimitExceededException: Type[BotocoreClientError]
    SnapshotLimitExceededException: Type[BotocoreClientError]
    TagLimitExceededException: Type[BotocoreClientError]
    UnsupportedOperationException: Type[BotocoreClientError]
    UserDoesNotExistException: Type[BotocoreClientError]


class DirectoryServiceClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        DirectoryServiceClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#exceptions)
        """

    async def accept_shared_directory(
        self, *, SharedDirectoryId: str
    ) -> AcceptSharedDirectoryResultTypeDef:
        """
        Accepts a directory sharing request that was sent from the directory owner
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.accept_shared_directory)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#accept_shared_directory)
        """

    async def add_ip_routes(
        self,
        *,
        DirectoryId: str,
        IpRoutes: Sequence["IpRouteTypeDef"],
        UpdateSecurityGroupForDirectoryControllers: bool = ...
    ) -> Dict[str, Any]:
        """
        If the DNS server for your self-managed domain uses a publicly addressable IP
        address, you must add a CIDR address block to correctly route traffic to and
        from your Microsoft AD on Amazon Web Services.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.add_ip_routes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#add_ip_routes)
        """

    async def add_region(
        self, *, DirectoryId: str, RegionName: str, VPCSettings: "DirectoryVpcSettingsTypeDef"
    ) -> Dict[str, Any]:
        """
        Adds two domain controllers in the specified Region for the specified directory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.add_region)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#add_region)
        """

    async def add_tags_to_resource(
        self, *, ResourceId: str, Tags: Sequence["TagTypeDef"]
    ) -> Dict[str, Any]:
        """
        Adds or overwrites one or more tags for the specified directory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.add_tags_to_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#add_tags_to_resource)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#can_paginate)
        """

    async def cancel_schema_extension(
        self, *, DirectoryId: str, SchemaExtensionId: str
    ) -> Dict[str, Any]:
        """
        Cancels an in-progress schema extension to a Microsoft AD directory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.cancel_schema_extension)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#cancel_schema_extension)
        """

    async def connect_directory(
        self,
        *,
        Name: str,
        Password: str,
        Size: DirectorySizeType,
        ConnectSettings: "DirectoryConnectSettingsTypeDef",
        ShortName: str = ...,
        Description: str = ...,
        Tags: Sequence["TagTypeDef"] = ...
    ) -> ConnectDirectoryResultTypeDef:
        """
        Creates an AD Connector to connect to a self-managed directory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.connect_directory)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#connect_directory)
        """

    async def create_alias(self, *, DirectoryId: str, Alias: str) -> CreateAliasResultTypeDef:
        """
        Creates an alias for a directory and assigns the alias to the directory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.create_alias)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#create_alias)
        """

    async def create_computer(
        self,
        *,
        DirectoryId: str,
        ComputerName: str,
        Password: str,
        OrganizationalUnitDistinguishedName: str = ...,
        ComputerAttributes: Sequence["AttributeTypeDef"] = ...
    ) -> CreateComputerResultTypeDef:
        """
        Creates an Active Directory computer object in the specified directory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.create_computer)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#create_computer)
        """

    async def create_conditional_forwarder(
        self, *, DirectoryId: str, RemoteDomainName: str, DnsIpAddrs: Sequence[str]
    ) -> Dict[str, Any]:
        """
        Creates a conditional forwarder associated with your Amazon Web Services
        directory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.create_conditional_forwarder)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#create_conditional_forwarder)
        """

    async def create_directory(
        self,
        *,
        Name: str,
        Password: str,
        Size: DirectorySizeType,
        ShortName: str = ...,
        Description: str = ...,
        VpcSettings: "DirectoryVpcSettingsTypeDef" = ...,
        Tags: Sequence["TagTypeDef"] = ...
    ) -> CreateDirectoryResultTypeDef:
        """
        Creates a Simple AD directory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.create_directory)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#create_directory)
        """

    async def create_log_subscription(
        self, *, DirectoryId: str, LogGroupName: str
    ) -> Dict[str, Any]:
        """
        Creates a subscription to forward real-time Directory Service domain controller
        security logs to the specified Amazon CloudWatch log group in your Amazon Web
        Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.create_log_subscription)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#create_log_subscription)
        """

    async def create_microsoft_ad(
        self,
        *,
        Name: str,
        Password: str,
        VpcSettings: "DirectoryVpcSettingsTypeDef",
        ShortName: str = ...,
        Description: str = ...,
        Edition: DirectoryEditionType = ...,
        Tags: Sequence["TagTypeDef"] = ...
    ) -> CreateMicrosoftADResultTypeDef:
        """
        Creates a Microsoft AD directory in the Amazon Web Services Cloud.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.create_microsoft_ad)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#create_microsoft_ad)
        """

    async def create_snapshot(
        self, *, DirectoryId: str, Name: str = ...
    ) -> CreateSnapshotResultTypeDef:
        """
        Creates a snapshot of a Simple AD or Microsoft AD directory in the Amazon Web
        Services cloud.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.create_snapshot)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#create_snapshot)
        """

    async def create_trust(
        self,
        *,
        DirectoryId: str,
        RemoteDomainName: str,
        TrustPassword: str,
        TrustDirection: TrustDirectionType,
        TrustType: TrustTypeType = ...,
        ConditionalForwarderIpAddrs: Sequence[str] = ...,
        SelectiveAuth: SelectiveAuthType = ...
    ) -> CreateTrustResultTypeDef:
        """
        Directory Service for Microsoft Active Directory allows you to configure trust
        relationships.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.create_trust)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#create_trust)
        """

    async def delete_conditional_forwarder(
        self, *, DirectoryId: str, RemoteDomainName: str
    ) -> Dict[str, Any]:
        """
        Deletes a conditional forwarder that has been set up for your Amazon Web
        Services directory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.delete_conditional_forwarder)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#delete_conditional_forwarder)
        """

    async def delete_directory(self, *, DirectoryId: str) -> DeleteDirectoryResultTypeDef:
        """
        Deletes an Directory Service directory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.delete_directory)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#delete_directory)
        """

    async def delete_log_subscription(self, *, DirectoryId: str) -> Dict[str, Any]:
        """
        Deletes the specified log subscription.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.delete_log_subscription)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#delete_log_subscription)
        """

    async def delete_snapshot(self, *, SnapshotId: str) -> DeleteSnapshotResultTypeDef:
        """
        Deletes a directory snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.delete_snapshot)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#delete_snapshot)
        """

    async def delete_trust(
        self, *, TrustId: str, DeleteAssociatedConditionalForwarder: bool = ...
    ) -> DeleteTrustResultTypeDef:
        """
        Deletes an existing trust relationship between your Managed Microsoft AD
        directory and an external domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.delete_trust)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#delete_trust)
        """

    async def deregister_certificate(
        self, *, DirectoryId: str, CertificateId: str
    ) -> Dict[str, Any]:
        """
        Deletes from the system the certificate that was registered for secure LDAP or
        client certificate authentication.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.deregister_certificate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#deregister_certificate)
        """

    async def deregister_event_topic(self, *, DirectoryId: str, TopicName: str) -> Dict[str, Any]:
        """
        Removes the specified directory as a publisher to the specified Amazon SNS
        topic.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.deregister_event_topic)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#deregister_event_topic)
        """

    async def describe_certificate(
        self, *, DirectoryId: str, CertificateId: str
    ) -> DescribeCertificateResultTypeDef:
        """
        Displays information about the certificate registered for secure LDAP or client
        certificate authentication.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.describe_certificate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#describe_certificate)
        """

    async def describe_client_authentication_settings(
        self,
        *,
        DirectoryId: str,
        Type: Literal["SmartCard"] = ...,
        NextToken: str = ...,
        Limit: int = ...
    ) -> DescribeClientAuthenticationSettingsResultTypeDef:
        """
        Retrieves information about the type of client authentication for the specified
        directory, if the type is specified.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.describe_client_authentication_settings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#describe_client_authentication_settings)
        """

    async def describe_conditional_forwarders(
        self, *, DirectoryId: str, RemoteDomainNames: Sequence[str] = ...
    ) -> DescribeConditionalForwardersResultTypeDef:
        """
        Obtains information about the conditional forwarders for this account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.describe_conditional_forwarders)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#describe_conditional_forwarders)
        """

    async def describe_directories(
        self, *, DirectoryIds: Sequence[str] = ..., NextToken: str = ..., Limit: int = ...
    ) -> DescribeDirectoriesResultTypeDef:
        """
        Obtains information about the directories that belong to this account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.describe_directories)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#describe_directories)
        """

    async def describe_domain_controllers(
        self,
        *,
        DirectoryId: str,
        DomainControllerIds: Sequence[str] = ...,
        NextToken: str = ...,
        Limit: int = ...
    ) -> DescribeDomainControllersResultTypeDef:
        """
        Provides information about any domain controllers in your directory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.describe_domain_controllers)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#describe_domain_controllers)
        """

    async def describe_event_topics(
        self, *, DirectoryId: str = ..., TopicNames: Sequence[str] = ...
    ) -> DescribeEventTopicsResultTypeDef:
        """
        Obtains information about which Amazon SNS topics receive status messages from
        the specified directory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.describe_event_topics)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#describe_event_topics)
        """

    async def describe_ldaps_settings(
        self,
        *,
        DirectoryId: str,
        Type: Literal["Client"] = ...,
        NextToken: str = ...,
        Limit: int = ...
    ) -> DescribeLDAPSSettingsResultTypeDef:
        """
        Describes the status of LDAP security for the specified directory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.describe_ldaps_settings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#describe_ldaps_settings)
        """

    async def describe_regions(
        self, *, DirectoryId: str, RegionName: str = ..., NextToken: str = ...
    ) -> DescribeRegionsResultTypeDef:
        """
        Provides information about the Regions that are configured for multi-Region
        replication.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.describe_regions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#describe_regions)
        """

    async def describe_shared_directories(
        self,
        *,
        OwnerDirectoryId: str,
        SharedDirectoryIds: Sequence[str] = ...,
        NextToken: str = ...,
        Limit: int = ...
    ) -> DescribeSharedDirectoriesResultTypeDef:
        """
        Returns the shared directories in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.describe_shared_directories)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#describe_shared_directories)
        """

    async def describe_snapshots(
        self,
        *,
        DirectoryId: str = ...,
        SnapshotIds: Sequence[str] = ...,
        NextToken: str = ...,
        Limit: int = ...
    ) -> DescribeSnapshotsResultTypeDef:
        """
        Obtains information about the directory snapshots that belong to this account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.describe_snapshots)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#describe_snapshots)
        """

    async def describe_trusts(
        self,
        *,
        DirectoryId: str = ...,
        TrustIds: Sequence[str] = ...,
        NextToken: str = ...,
        Limit: int = ...
    ) -> DescribeTrustsResultTypeDef:
        """
        Obtains information about the trust relationships for this account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.describe_trusts)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#describe_trusts)
        """

    async def disable_client_authentication(
        self, *, DirectoryId: str, Type: Literal["SmartCard"]
    ) -> Dict[str, Any]:
        """
        Disables alternative client authentication methods for the specified directory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.disable_client_authentication)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#disable_client_authentication)
        """

    async def disable_ldaps(self, *, DirectoryId: str, Type: Literal["Client"]) -> Dict[str, Any]:
        """
        Deactivates LDAP secure calls for the specified directory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.disable_ldaps)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#disable_ldaps)
        """

    async def disable_radius(self, *, DirectoryId: str) -> Dict[str, Any]:
        """
        Disables multi-factor authentication (MFA) with the Remote Authentication Dial
        In User Service (RADIUS) server for an AD Connector or Microsoft AD directory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.disable_radius)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#disable_radius)
        """

    async def disable_sso(
        self, *, DirectoryId: str, UserName: str = ..., Password: str = ...
    ) -> Dict[str, Any]:
        """
        Disables single-sign on for a directory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.disable_sso)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#disable_sso)
        """

    async def enable_client_authentication(
        self, *, DirectoryId: str, Type: Literal["SmartCard"]
    ) -> Dict[str, Any]:
        """
        Enables alternative client authentication methods for the specified directory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.enable_client_authentication)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#enable_client_authentication)
        """

    async def enable_ldaps(self, *, DirectoryId: str, Type: Literal["Client"]) -> Dict[str, Any]:
        """
        Activates the switch for the specific directory to always use LDAP secure calls.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.enable_ldaps)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#enable_ldaps)
        """

    async def enable_radius(
        self, *, DirectoryId: str, RadiusSettings: "RadiusSettingsTypeDef"
    ) -> Dict[str, Any]:
        """
        Enables multi-factor authentication (MFA) with the Remote Authentication Dial In
        User Service (RADIUS) server for an AD Connector or Microsoft AD directory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.enable_radius)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#enable_radius)
        """

    async def enable_sso(
        self, *, DirectoryId: str, UserName: str = ..., Password: str = ...
    ) -> Dict[str, Any]:
        """
        Enables single sign-on for a directory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.enable_sso)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#enable_sso)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#generate_presigned_url)
        """

    async def get_directory_limits(self) -> GetDirectoryLimitsResultTypeDef:
        """
        Obtains directory limit information for the current Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.get_directory_limits)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#get_directory_limits)
        """

    async def get_snapshot_limits(self, *, DirectoryId: str) -> GetSnapshotLimitsResultTypeDef:
        """
        Obtains the manual snapshot limits for a directory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.get_snapshot_limits)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#get_snapshot_limits)
        """

    async def list_certificates(
        self, *, DirectoryId: str, NextToken: str = ..., Limit: int = ...
    ) -> ListCertificatesResultTypeDef:
        """
        For the specified directory, lists all the certificates registered for a secure
        LDAP or client certificate authentication.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.list_certificates)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#list_certificates)
        """

    async def list_ip_routes(
        self, *, DirectoryId: str, NextToken: str = ..., Limit: int = ...
    ) -> ListIpRoutesResultTypeDef:
        """
        Lists the address blocks that you have added to a directory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.list_ip_routes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#list_ip_routes)
        """

    async def list_log_subscriptions(
        self, *, DirectoryId: str = ..., NextToken: str = ..., Limit: int = ...
    ) -> ListLogSubscriptionsResultTypeDef:
        """
        Lists the active log subscriptions for the Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.list_log_subscriptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#list_log_subscriptions)
        """

    async def list_schema_extensions(
        self, *, DirectoryId: str, NextToken: str = ..., Limit: int = ...
    ) -> ListSchemaExtensionsResultTypeDef:
        """
        Lists all schema extensions applied to a Microsoft AD Directory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.list_schema_extensions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#list_schema_extensions)
        """

    async def list_tags_for_resource(
        self, *, ResourceId: str, NextToken: str = ..., Limit: int = ...
    ) -> ListTagsForResourceResultTypeDef:
        """
        Lists all tags on a directory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#list_tags_for_resource)
        """

    async def register_certificate(
        self,
        *,
        DirectoryId: str,
        CertificateData: str,
        Type: CertificateTypeType = ...,
        ClientCertAuthSettings: "ClientCertAuthSettingsTypeDef" = ...
    ) -> RegisterCertificateResultTypeDef:
        """
        Registers a certificate for a secure LDAP or client certificate authentication.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.register_certificate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#register_certificate)
        """

    async def register_event_topic(self, *, DirectoryId: str, TopicName: str) -> Dict[str, Any]:
        """
        Associates a directory with an Amazon SNS topic.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.register_event_topic)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#register_event_topic)
        """

    async def reject_shared_directory(
        self, *, SharedDirectoryId: str
    ) -> RejectSharedDirectoryResultTypeDef:
        """
        Rejects a directory sharing request that was sent from the directory owner
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.reject_shared_directory)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#reject_shared_directory)
        """

    async def remove_ip_routes(self, *, DirectoryId: str, CidrIps: Sequence[str]) -> Dict[str, Any]:
        """
        Removes IP address blocks from a directory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.remove_ip_routes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#remove_ip_routes)
        """

    async def remove_region(self, *, DirectoryId: str) -> Dict[str, Any]:
        """
        Stops all replication and removes the domain controllers from the specified
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.remove_region)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#remove_region)
        """

    async def remove_tags_from_resource(
        self, *, ResourceId: str, TagKeys: Sequence[str]
    ) -> Dict[str, Any]:
        """
        Removes tags from a directory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.remove_tags_from_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#remove_tags_from_resource)
        """

    async def reset_user_password(
        self, *, DirectoryId: str, UserName: str, NewPassword: str
    ) -> Dict[str, Any]:
        """
        Resets the password for any user in your Managed Microsoft AD or Simple AD
        directory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.reset_user_password)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#reset_user_password)
        """

    async def restore_from_snapshot(self, *, SnapshotId: str) -> Dict[str, Any]:
        """
        Restores a directory using an existing directory snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.restore_from_snapshot)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#restore_from_snapshot)
        """

    async def share_directory(
        self,
        *,
        DirectoryId: str,
        ShareTarget: "ShareTargetTypeDef",
        ShareMethod: ShareMethodType,
        ShareNotes: str = ...
    ) -> ShareDirectoryResultTypeDef:
        """
        Shares a specified directory (`DirectoryId` ) in your Amazon Web Services
        account (directory owner) with another Amazon Web Services account (directory
        consumer).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.share_directory)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#share_directory)
        """

    async def start_schema_extension(
        self,
        *,
        DirectoryId: str,
        CreateSnapshotBeforeSchemaExtension: bool,
        LdifContent: str,
        Description: str
    ) -> StartSchemaExtensionResultTypeDef:
        """
        Applies a schema extension to a Microsoft AD directory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.start_schema_extension)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#start_schema_extension)
        """

    async def unshare_directory(
        self, *, DirectoryId: str, UnshareTarget: "UnshareTargetTypeDef"
    ) -> UnshareDirectoryResultTypeDef:
        """
        Stops the directory sharing between the directory owner and consumer accounts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.unshare_directory)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#unshare_directory)
        """

    async def update_conditional_forwarder(
        self, *, DirectoryId: str, RemoteDomainName: str, DnsIpAddrs: Sequence[str]
    ) -> Dict[str, Any]:
        """
        Updates a conditional forwarder that has been set up for your Amazon Web
        Services directory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.update_conditional_forwarder)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#update_conditional_forwarder)
        """

    async def update_number_of_domain_controllers(
        self, *, DirectoryId: str, DesiredNumber: int
    ) -> Dict[str, Any]:
        """
        Adds or removes domain controllers to or from the directory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.update_number_of_domain_controllers)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#update_number_of_domain_controllers)
        """

    async def update_radius(
        self, *, DirectoryId: str, RadiusSettings: "RadiusSettingsTypeDef"
    ) -> Dict[str, Any]:
        """
        Updates the Remote Authentication Dial In User Service (RADIUS) server
        information for an AD Connector or Microsoft AD directory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.update_radius)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#update_radius)
        """

    async def update_trust(
        self, *, TrustId: str, SelectiveAuth: SelectiveAuthType = ...
    ) -> UpdateTrustResultTypeDef:
        """
        Updates the trust that has been set up between your Managed Microsoft AD
        directory and an self-managed Active Directory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.update_trust)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#update_trust)
        """

    async def verify_trust(self, *, TrustId: str) -> VerifyTrustResultTypeDef:
        """
        Directory Service for Microsoft Active Directory allows you to configure and
        verify trust relationships.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.verify_trust)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#verify_trust)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_directories"]
    ) -> DescribeDirectoriesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_domain_controllers"]
    ) -> DescribeDomainControllersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_shared_directories"]
    ) -> DescribeSharedDirectoriesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_snapshots"]
    ) -> DescribeSnapshotsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["describe_trusts"]) -> DescribeTrustsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_ip_routes"]) -> ListIpRoutesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_log_subscriptions"]
    ) -> ListLogSubscriptionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_schema_extensions"]
    ) -> ListSchemaExtensionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_tags_for_resource"]
    ) -> ListTagsForResourcePaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/#get_paginator)
        """

    async def __aenter__(self) -> "DirectoryServiceClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds.html#DirectoryService.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds/client/)
        """
