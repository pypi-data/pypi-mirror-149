"""
Type annotations for es service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_es/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_es.client import ElasticsearchServiceClient

    session = get_session()
    async with session.create_client("es") as client:
        client: ElasticsearchServiceClient
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import EngineTypeType, ESPartitionInstanceTypeType, LogTypeType
from .paginator import (
    DescribeReservedElasticsearchInstanceOfferingsPaginator,
    DescribeReservedElasticsearchInstancesPaginator,
    GetUpgradeHistoryPaginator,
    ListElasticsearchInstanceTypesPaginator,
    ListElasticsearchVersionsPaginator,
)
from .type_defs import (
    AcceptInboundCrossClusterSearchConnectionResponseTypeDef,
    AdvancedSecurityOptionsInputTypeDef,
    AssociatePackageResponseTypeDef,
    AutoTuneOptionsInputTypeDef,
    AutoTuneOptionsTypeDef,
    CancelElasticsearchServiceSoftwareUpdateResponseTypeDef,
    CognitoOptionsTypeDef,
    CreateElasticsearchDomainResponseTypeDef,
    CreateOutboundCrossClusterSearchConnectionResponseTypeDef,
    CreatePackageResponseTypeDef,
    DeleteElasticsearchDomainResponseTypeDef,
    DeleteInboundCrossClusterSearchConnectionResponseTypeDef,
    DeleteOutboundCrossClusterSearchConnectionResponseTypeDef,
    DeletePackageResponseTypeDef,
    DescribeDomainAutoTunesResponseTypeDef,
    DescribeDomainChangeProgressResponseTypeDef,
    DescribeElasticsearchDomainConfigResponseTypeDef,
    DescribeElasticsearchDomainResponseTypeDef,
    DescribeElasticsearchDomainsResponseTypeDef,
    DescribeElasticsearchInstanceTypeLimitsResponseTypeDef,
    DescribeInboundCrossClusterSearchConnectionsResponseTypeDef,
    DescribeOutboundCrossClusterSearchConnectionsResponseTypeDef,
    DescribePackagesFilterTypeDef,
    DescribePackagesResponseTypeDef,
    DescribeReservedElasticsearchInstanceOfferingsResponseTypeDef,
    DescribeReservedElasticsearchInstancesResponseTypeDef,
    DissociatePackageResponseTypeDef,
    DomainEndpointOptionsTypeDef,
    DomainInformationTypeDef,
    EBSOptionsTypeDef,
    ElasticsearchClusterConfigTypeDef,
    EncryptionAtRestOptionsTypeDef,
    FilterTypeDef,
    GetCompatibleElasticsearchVersionsResponseTypeDef,
    GetPackageVersionHistoryResponseTypeDef,
    GetUpgradeHistoryResponseTypeDef,
    GetUpgradeStatusResponseTypeDef,
    ListDomainNamesResponseTypeDef,
    ListDomainsForPackageResponseTypeDef,
    ListElasticsearchInstanceTypesResponseTypeDef,
    ListElasticsearchVersionsResponseTypeDef,
    ListPackagesForDomainResponseTypeDef,
    ListTagsResponseTypeDef,
    LogPublishingOptionTypeDef,
    NodeToNodeEncryptionOptionsTypeDef,
    PackageSourceTypeDef,
    PurchaseReservedElasticsearchInstanceOfferingResponseTypeDef,
    RejectInboundCrossClusterSearchConnectionResponseTypeDef,
    SnapshotOptionsTypeDef,
    StartElasticsearchServiceSoftwareUpdateResponseTypeDef,
    TagTypeDef,
    UpdateElasticsearchDomainConfigResponseTypeDef,
    UpdatePackageResponseTypeDef,
    UpgradeElasticsearchDomainResponseTypeDef,
    VPCOptionsTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("ElasticsearchServiceClient",)

class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    BaseException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    DisabledOperationException: Type[BotocoreClientError]
    InternalException: Type[BotocoreClientError]
    InvalidPaginationTokenException: Type[BotocoreClientError]
    InvalidTypeException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ResourceAlreadyExistsException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class ElasticsearchServiceClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_es/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ElasticsearchServiceClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_es/client/#exceptions)
        """
    async def accept_inbound_cross_cluster_search_connection(
        self, *, CrossClusterSearchConnectionId: str
    ) -> AcceptInboundCrossClusterSearchConnectionResponseTypeDef:
        """
        Allows the destination domain owner to accept an inbound cross-cluster search
        connection request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.accept_inbound_cross_cluster_search_connection)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_es/client/#accept_inbound_cross_cluster_search_connection)
        """
    async def add_tags(self, *, ARN: str, TagList: Sequence["TagTypeDef"]) -> None:
        """
        Attaches tags to an existing Elasticsearch domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.add_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_es/client/#add_tags)
        """
    async def associate_package(
        self, *, PackageID: str, DomainName: str
    ) -> AssociatePackageResponseTypeDef:
        """
        Associates a package with an Amazon ES domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.associate_package)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_es/client/#associate_package)
        """
    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_es/client/#can_paginate)
        """
    async def cancel_elasticsearch_service_software_update(
        self, *, DomainName: str
    ) -> CancelElasticsearchServiceSoftwareUpdateResponseTypeDef:
        """
        Cancels a scheduled service software update for an Amazon ES domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.cancel_elasticsearch_service_software_update)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_es/client/#cancel_elasticsearch_service_software_update)
        """
    async def create_elasticsearch_domain(
        self,
        *,
        DomainName: str,
        ElasticsearchVersion: str = ...,
        ElasticsearchClusterConfig: "ElasticsearchClusterConfigTypeDef" = ...,
        EBSOptions: "EBSOptionsTypeDef" = ...,
        AccessPolicies: str = ...,
        SnapshotOptions: "SnapshotOptionsTypeDef" = ...,
        VPCOptions: "VPCOptionsTypeDef" = ...,
        CognitoOptions: "CognitoOptionsTypeDef" = ...,
        EncryptionAtRestOptions: "EncryptionAtRestOptionsTypeDef" = ...,
        NodeToNodeEncryptionOptions: "NodeToNodeEncryptionOptionsTypeDef" = ...,
        AdvancedOptions: Mapping[str, str] = ...,
        LogPublishingOptions: Mapping[LogTypeType, "LogPublishingOptionTypeDef"] = ...,
        DomainEndpointOptions: "DomainEndpointOptionsTypeDef" = ...,
        AdvancedSecurityOptions: "AdvancedSecurityOptionsInputTypeDef" = ...,
        AutoTuneOptions: "AutoTuneOptionsInputTypeDef" = ...,
        TagList: Sequence["TagTypeDef"] = ...
    ) -> CreateElasticsearchDomainResponseTypeDef:
        """
        Creates a new Elasticsearch domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.create_elasticsearch_domain)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_es/client/#create_elasticsearch_domain)
        """
    async def create_outbound_cross_cluster_search_connection(
        self,
        *,
        SourceDomainInfo: "DomainInformationTypeDef",
        DestinationDomainInfo: "DomainInformationTypeDef",
        ConnectionAlias: str
    ) -> CreateOutboundCrossClusterSearchConnectionResponseTypeDef:
        """
        Creates a new cross-cluster search connection from a source domain to a
        destination domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.create_outbound_cross_cluster_search_connection)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_es/client/#create_outbound_cross_cluster_search_connection)
        """
    async def create_package(
        self,
        *,
        PackageName: str,
        PackageType: Literal["TXT-DICTIONARY"],
        PackageSource: "PackageSourceTypeDef",
        PackageDescription: str = ...
    ) -> CreatePackageResponseTypeDef:
        """
        Create a package for use with Amazon ES domains.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.create_package)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_es/client/#create_package)
        """
    async def delete_elasticsearch_domain(
        self, *, DomainName: str
    ) -> DeleteElasticsearchDomainResponseTypeDef:
        """
        Permanently deletes the specified Elasticsearch domain and all of its data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.delete_elasticsearch_domain)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_es/client/#delete_elasticsearch_domain)
        """
    async def delete_elasticsearch_service_role(self) -> None:
        """
        Deletes the service-linked role that Elasticsearch Service uses to manage and
        maintain VPC domains.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.delete_elasticsearch_service_role)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_es/client/#delete_elasticsearch_service_role)
        """
    async def delete_inbound_cross_cluster_search_connection(
        self, *, CrossClusterSearchConnectionId: str
    ) -> DeleteInboundCrossClusterSearchConnectionResponseTypeDef:
        """
        Allows the destination domain owner to delete an existing inbound cross-cluster
        search connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.delete_inbound_cross_cluster_search_connection)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_es/client/#delete_inbound_cross_cluster_search_connection)
        """
    async def delete_outbound_cross_cluster_search_connection(
        self, *, CrossClusterSearchConnectionId: str
    ) -> DeleteOutboundCrossClusterSearchConnectionResponseTypeDef:
        """
        Allows the source domain owner to delete an existing outbound cross-cluster
        search connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.delete_outbound_cross_cluster_search_connection)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_es/client/#delete_outbound_cross_cluster_search_connection)
        """
    async def delete_package(self, *, PackageID: str) -> DeletePackageResponseTypeDef:
        """
        Delete the package.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.delete_package)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_es/client/#delete_package)
        """
    async def describe_domain_auto_tunes(
        self, *, DomainName: str, MaxResults: int = ..., NextToken: str = ...
    ) -> DescribeDomainAutoTunesResponseTypeDef:
        """
        Provides scheduled Auto-Tune action details for the Elasticsearch domain, such
        as Auto-Tune action type, description, severity, and scheduled date.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.describe_domain_auto_tunes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_es/client/#describe_domain_auto_tunes)
        """
    async def describe_domain_change_progress(
        self, *, DomainName: str, ChangeId: str = ...
    ) -> DescribeDomainChangeProgressResponseTypeDef:
        """
        Returns information about the current blue/green deployment happening on a
        domain, including a change ID, status, and progress stages.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.describe_domain_change_progress)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_es/client/#describe_domain_change_progress)
        """
    async def describe_elasticsearch_domain(
        self, *, DomainName: str
    ) -> DescribeElasticsearchDomainResponseTypeDef:
        """
        Returns domain configuration information about the specified Elasticsearch
        domain, including the domain ID, domain endpoint, and domain ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.describe_elasticsearch_domain)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_es/client/#describe_elasticsearch_domain)
        """
    async def describe_elasticsearch_domain_config(
        self, *, DomainName: str
    ) -> DescribeElasticsearchDomainConfigResponseTypeDef:
        """
        Provides cluster configuration information about the specified Elasticsearch
        domain, such as the state, creation date, update version, and update date for
        cluster options.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.describe_elasticsearch_domain_config)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_es/client/#describe_elasticsearch_domain_config)
        """
    async def describe_elasticsearch_domains(
        self, *, DomainNames: Sequence[str]
    ) -> DescribeElasticsearchDomainsResponseTypeDef:
        """
        Returns domain configuration information about the specified Elasticsearch
        domains, including the domain ID, domain endpoint, and domain ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.describe_elasticsearch_domains)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_es/client/#describe_elasticsearch_domains)
        """
    async def describe_elasticsearch_instance_type_limits(
        self,
        *,
        InstanceType: ESPartitionInstanceTypeType,
        ElasticsearchVersion: str,
        DomainName: str = ...
    ) -> DescribeElasticsearchInstanceTypeLimitsResponseTypeDef:
        """
        Describe Elasticsearch Limits for a given InstanceType and ElasticsearchVersion.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.describe_elasticsearch_instance_type_limits)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_es/client/#describe_elasticsearch_instance_type_limits)
        """
    async def describe_inbound_cross_cluster_search_connections(
        self,
        *,
        Filters: Sequence["FilterTypeDef"] = ...,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> DescribeInboundCrossClusterSearchConnectionsResponseTypeDef:
        """
        Lists all the inbound cross-cluster search connections for a destination domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.describe_inbound_cross_cluster_search_connections)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_es/client/#describe_inbound_cross_cluster_search_connections)
        """
    async def describe_outbound_cross_cluster_search_connections(
        self,
        *,
        Filters: Sequence["FilterTypeDef"] = ...,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> DescribeOutboundCrossClusterSearchConnectionsResponseTypeDef:
        """
        Lists all the outbound cross-cluster search connections for a source domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.describe_outbound_cross_cluster_search_connections)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_es/client/#describe_outbound_cross_cluster_search_connections)
        """
    async def describe_packages(
        self,
        *,
        Filters: Sequence["DescribePackagesFilterTypeDef"] = ...,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> DescribePackagesResponseTypeDef:
        """
        Describes all packages available to Amazon ES.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.describe_packages)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_es/client/#describe_packages)
        """
    async def describe_reserved_elasticsearch_instance_offerings(
        self,
        *,
        ReservedElasticsearchInstanceOfferingId: str = ...,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> DescribeReservedElasticsearchInstanceOfferingsResponseTypeDef:
        """
        Lists available reserved Elasticsearch instance offerings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.describe_reserved_elasticsearch_instance_offerings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_es/client/#describe_reserved_elasticsearch_instance_offerings)
        """
    async def describe_reserved_elasticsearch_instances(
        self,
        *,
        ReservedElasticsearchInstanceId: str = ...,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> DescribeReservedElasticsearchInstancesResponseTypeDef:
        """
        Returns information about reserved Elasticsearch instances for this account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.describe_reserved_elasticsearch_instances)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_es/client/#describe_reserved_elasticsearch_instances)
        """
    async def dissociate_package(
        self, *, PackageID: str, DomainName: str
    ) -> DissociatePackageResponseTypeDef:
        """
        Dissociates a package from the Amazon ES domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.dissociate_package)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_es/client/#dissociate_package)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_es/client/#generate_presigned_url)
        """
    async def get_compatible_elasticsearch_versions(
        self, *, DomainName: str = ...
    ) -> GetCompatibleElasticsearchVersionsResponseTypeDef:
        """
        Returns a list of upgrade compatible Elastisearch versions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.get_compatible_elasticsearch_versions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_es/client/#get_compatible_elasticsearch_versions)
        """
    async def get_package_version_history(
        self, *, PackageID: str, MaxResults: int = ..., NextToken: str = ...
    ) -> GetPackageVersionHistoryResponseTypeDef:
        """
        Returns a list of versions of the package, along with their creation time and
        commit message.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.get_package_version_history)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_es/client/#get_package_version_history)
        """
    async def get_upgrade_history(
        self, *, DomainName: str, MaxResults: int = ..., NextToken: str = ...
    ) -> GetUpgradeHistoryResponseTypeDef:
        """
        Retrieves the complete history of the last 10 upgrades that were performed on
        the domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.get_upgrade_history)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_es/client/#get_upgrade_history)
        """
    async def get_upgrade_status(self, *, DomainName: str) -> GetUpgradeStatusResponseTypeDef:
        """
        Retrieves the latest status of the last upgrade or upgrade eligibility check
        that was performed on the domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.get_upgrade_status)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_es/client/#get_upgrade_status)
        """
    async def list_domain_names(
        self, *, EngineType: EngineTypeType = ...
    ) -> ListDomainNamesResponseTypeDef:
        """
        Returns the name of all Elasticsearch domains owned by the current user's
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.list_domain_names)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_es/client/#list_domain_names)
        """
    async def list_domains_for_package(
        self, *, PackageID: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListDomainsForPackageResponseTypeDef:
        """
        Lists all Amazon ES domains associated with the package.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.list_domains_for_package)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_es/client/#list_domains_for_package)
        """
    async def list_elasticsearch_instance_types(
        self,
        *,
        ElasticsearchVersion: str,
        DomainName: str = ...,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> ListElasticsearchInstanceTypesResponseTypeDef:
        """
        List all Elasticsearch instance types that are supported for given
        ElasticsearchVersion See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/es-2015-01-01/ListElasticsearchInstanceTypes).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.list_elasticsearch_instance_types)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_es/client/#list_elasticsearch_instance_types)
        """
    async def list_elasticsearch_versions(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListElasticsearchVersionsResponseTypeDef:
        """
        List all supported Elasticsearch versions See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/es-2015-01-01/ListElasticsearchVersions).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.list_elasticsearch_versions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_es/client/#list_elasticsearch_versions)
        """
    async def list_packages_for_domain(
        self, *, DomainName: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListPackagesForDomainResponseTypeDef:
        """
        Lists all packages associated with the Amazon ES domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.list_packages_for_domain)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_es/client/#list_packages_for_domain)
        """
    async def list_tags(self, *, ARN: str) -> ListTagsResponseTypeDef:
        """
        Returns all tags for the given Elasticsearch domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.list_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_es/client/#list_tags)
        """
    async def purchase_reserved_elasticsearch_instance_offering(
        self,
        *,
        ReservedElasticsearchInstanceOfferingId: str,
        ReservationName: str,
        InstanceCount: int = ...
    ) -> PurchaseReservedElasticsearchInstanceOfferingResponseTypeDef:
        """
        Allows you to purchase reserved Elasticsearch instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.purchase_reserved_elasticsearch_instance_offering)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_es/client/#purchase_reserved_elasticsearch_instance_offering)
        """
    async def reject_inbound_cross_cluster_search_connection(
        self, *, CrossClusterSearchConnectionId: str
    ) -> RejectInboundCrossClusterSearchConnectionResponseTypeDef:
        """
        Allows the destination domain owner to reject an inbound cross-cluster search
        connection request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.reject_inbound_cross_cluster_search_connection)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_es/client/#reject_inbound_cross_cluster_search_connection)
        """
    async def remove_tags(self, *, ARN: str, TagKeys: Sequence[str]) -> None:
        """
        Removes the specified set of tags from the specified Elasticsearch domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.remove_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_es/client/#remove_tags)
        """
    async def start_elasticsearch_service_software_update(
        self, *, DomainName: str
    ) -> StartElasticsearchServiceSoftwareUpdateResponseTypeDef:
        """
        Schedules a service software update for an Amazon ES domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.start_elasticsearch_service_software_update)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_es/client/#start_elasticsearch_service_software_update)
        """
    async def update_elasticsearch_domain_config(
        self,
        *,
        DomainName: str,
        ElasticsearchClusterConfig: "ElasticsearchClusterConfigTypeDef" = ...,
        EBSOptions: "EBSOptionsTypeDef" = ...,
        SnapshotOptions: "SnapshotOptionsTypeDef" = ...,
        VPCOptions: "VPCOptionsTypeDef" = ...,
        CognitoOptions: "CognitoOptionsTypeDef" = ...,
        AdvancedOptions: Mapping[str, str] = ...,
        AccessPolicies: str = ...,
        LogPublishingOptions: Mapping[LogTypeType, "LogPublishingOptionTypeDef"] = ...,
        DomainEndpointOptions: "DomainEndpointOptionsTypeDef" = ...,
        AdvancedSecurityOptions: "AdvancedSecurityOptionsInputTypeDef" = ...,
        NodeToNodeEncryptionOptions: "NodeToNodeEncryptionOptionsTypeDef" = ...,
        EncryptionAtRestOptions: "EncryptionAtRestOptionsTypeDef" = ...,
        AutoTuneOptions: "AutoTuneOptionsTypeDef" = ...,
        DryRun: bool = ...
    ) -> UpdateElasticsearchDomainConfigResponseTypeDef:
        """
        Modifies the cluster configuration of the specified Elasticsearch domain,
        setting as setting the instance type and the number of instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.update_elasticsearch_domain_config)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_es/client/#update_elasticsearch_domain_config)
        """
    async def update_package(
        self,
        *,
        PackageID: str,
        PackageSource: "PackageSourceTypeDef",
        PackageDescription: str = ...,
        CommitMessage: str = ...
    ) -> UpdatePackageResponseTypeDef:
        """
        Updates a package for use with Amazon ES domains.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.update_package)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_es/client/#update_package)
        """
    async def upgrade_elasticsearch_domain(
        self, *, DomainName: str, TargetVersion: str, PerformCheckOnly: bool = ...
    ) -> UpgradeElasticsearchDomainResponseTypeDef:
        """
        Allows you to either upgrade your domain or perform an Upgrade eligibility check
        to a compatible Elasticsearch version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.upgrade_elasticsearch_domain)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_es/client/#upgrade_elasticsearch_domain)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["describe_reserved_elasticsearch_instance_offerings"]
    ) -> DescribeReservedElasticsearchInstanceOfferingsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_es/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["describe_reserved_elasticsearch_instances"]
    ) -> DescribeReservedElasticsearchInstancesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_es/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["get_upgrade_history"]
    ) -> GetUpgradeHistoryPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_es/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_elasticsearch_instance_types"]
    ) -> ListElasticsearchInstanceTypesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_es/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_elasticsearch_versions"]
    ) -> ListElasticsearchVersionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_es/client/#get_paginator)
        """
    async def __aenter__(self) -> "ElasticsearchServiceClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_es/client/)
        """
    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_es/client/)
        """
