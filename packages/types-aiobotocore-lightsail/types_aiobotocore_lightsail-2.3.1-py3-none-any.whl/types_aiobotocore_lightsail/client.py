"""
Type annotations for lightsail service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_lightsail.client import LightsailClient

    session = get_session()
    async with session.create_client("lightsail") as client:
        client: LightsailClient
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, Mapping, Sequence, Type, Union, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import (
    AlarmStateType,
    BucketMetricNameType,
    CertificateStatusType,
    ComparisonOperatorType,
    ContactProtocolType,
    ContainerServiceMetricNameType,
    ContainerServicePowerNameType,
    DistributionMetricNameType,
    InstanceAccessProtocolType,
    InstanceMetricNameType,
    IpAddressTypeType,
    LoadBalancerAttributeNameType,
    LoadBalancerMetricNameType,
    MetricNameType,
    MetricStatisticType,
    MetricUnitType,
    RegionNameType,
    RelationalDatabaseMetricNameType,
    RelationalDatabasePasswordVersionType,
    ResourceBucketAccessType,
    ResourceTypeType,
    TreatMissingDataType,
)
from .paginator import (
    GetActiveNamesPaginator,
    GetBlueprintsPaginator,
    GetBundlesPaginator,
    GetCloudFormationStackRecordsPaginator,
    GetDiskSnapshotsPaginator,
    GetDisksPaginator,
    GetDomainsPaginator,
    GetExportSnapshotRecordsPaginator,
    GetInstanceSnapshotsPaginator,
    GetInstancesPaginator,
    GetKeyPairsPaginator,
    GetLoadBalancersPaginator,
    GetOperationsPaginator,
    GetRelationalDatabaseBlueprintsPaginator,
    GetRelationalDatabaseBundlesPaginator,
    GetRelationalDatabaseEventsPaginator,
    GetRelationalDatabaseParametersPaginator,
    GetRelationalDatabaseSnapshotsPaginator,
    GetRelationalDatabasesPaginator,
    GetStaticIpsPaginator,
)
from .type_defs import (
    AccessRulesTypeDef,
    AddOnRequestTypeDef,
    AllocateStaticIpResultTypeDef,
    AttachCertificateToDistributionResultTypeDef,
    AttachDiskResultTypeDef,
    AttachInstancesToLoadBalancerResultTypeDef,
    AttachLoadBalancerTlsCertificateResultTypeDef,
    AttachStaticIpResultTypeDef,
    BucketAccessLogConfigTypeDef,
    CacheBehaviorPerPathTypeDef,
    CacheBehaviorTypeDef,
    CacheSettingsTypeDef,
    CloseInstancePublicPortsResultTypeDef,
    ContainerServiceDeploymentRequestTypeDef,
    ContainerServicesListResultTypeDef,
    ContainerTypeDef,
    CopySnapshotResultTypeDef,
    CreateBucketAccessKeyResultTypeDef,
    CreateBucketResultTypeDef,
    CreateCertificateResultTypeDef,
    CreateCloudFormationStackResultTypeDef,
    CreateContactMethodResultTypeDef,
    CreateContainerServiceDeploymentResultTypeDef,
    CreateContainerServiceRegistryLoginResultTypeDef,
    CreateContainerServiceResultTypeDef,
    CreateDiskFromSnapshotResultTypeDef,
    CreateDiskResultTypeDef,
    CreateDiskSnapshotResultTypeDef,
    CreateDistributionResultTypeDef,
    CreateDomainEntryResultTypeDef,
    CreateDomainResultTypeDef,
    CreateInstancesFromSnapshotResultTypeDef,
    CreateInstanceSnapshotResultTypeDef,
    CreateInstancesResultTypeDef,
    CreateKeyPairResultTypeDef,
    CreateLoadBalancerResultTypeDef,
    CreateLoadBalancerTlsCertificateResultTypeDef,
    CreateRelationalDatabaseFromSnapshotResultTypeDef,
    CreateRelationalDatabaseResultTypeDef,
    CreateRelationalDatabaseSnapshotResultTypeDef,
    DeleteAlarmResultTypeDef,
    DeleteAutoSnapshotResultTypeDef,
    DeleteBucketAccessKeyResultTypeDef,
    DeleteBucketResultTypeDef,
    DeleteCertificateResultTypeDef,
    DeleteContactMethodResultTypeDef,
    DeleteDiskResultTypeDef,
    DeleteDiskSnapshotResultTypeDef,
    DeleteDistributionResultTypeDef,
    DeleteDomainEntryResultTypeDef,
    DeleteDomainResultTypeDef,
    DeleteInstanceResultTypeDef,
    DeleteInstanceSnapshotResultTypeDef,
    DeleteKeyPairResultTypeDef,
    DeleteKnownHostKeysResultTypeDef,
    DeleteLoadBalancerResultTypeDef,
    DeleteLoadBalancerTlsCertificateResultTypeDef,
    DeleteRelationalDatabaseResultTypeDef,
    DeleteRelationalDatabaseSnapshotResultTypeDef,
    DetachCertificateFromDistributionResultTypeDef,
    DetachDiskResultTypeDef,
    DetachInstancesFromLoadBalancerResultTypeDef,
    DetachStaticIpResultTypeDef,
    DisableAddOnResultTypeDef,
    DiskMapTypeDef,
    DomainEntryTypeDef,
    DownloadDefaultKeyPairResultTypeDef,
    EnableAddOnResultTypeDef,
    EndpointRequestTypeDef,
    ExportSnapshotResultTypeDef,
    GetActiveNamesResultTypeDef,
    GetAlarmsResultTypeDef,
    GetAutoSnapshotsResultTypeDef,
    GetBlueprintsResultTypeDef,
    GetBucketAccessKeysResultTypeDef,
    GetBucketBundlesResultTypeDef,
    GetBucketMetricDataResultTypeDef,
    GetBucketsResultTypeDef,
    GetBundlesResultTypeDef,
    GetCertificatesResultTypeDef,
    GetCloudFormationStackRecordsResultTypeDef,
    GetContactMethodsResultTypeDef,
    GetContainerAPIMetadataResultTypeDef,
    GetContainerImagesResultTypeDef,
    GetContainerLogResultTypeDef,
    GetContainerServiceDeploymentsResultTypeDef,
    GetContainerServiceMetricDataResultTypeDef,
    GetContainerServicePowersResultTypeDef,
    GetDiskResultTypeDef,
    GetDiskSnapshotResultTypeDef,
    GetDiskSnapshotsResultTypeDef,
    GetDisksResultTypeDef,
    GetDistributionBundlesResultTypeDef,
    GetDistributionLatestCacheResetResultTypeDef,
    GetDistributionMetricDataResultTypeDef,
    GetDistributionsResultTypeDef,
    GetDomainResultTypeDef,
    GetDomainsResultTypeDef,
    GetExportSnapshotRecordsResultTypeDef,
    GetInstanceAccessDetailsResultTypeDef,
    GetInstanceMetricDataResultTypeDef,
    GetInstancePortStatesResultTypeDef,
    GetInstanceResultTypeDef,
    GetInstanceSnapshotResultTypeDef,
    GetInstanceSnapshotsResultTypeDef,
    GetInstancesResultTypeDef,
    GetInstanceStateResultTypeDef,
    GetKeyPairResultTypeDef,
    GetKeyPairsResultTypeDef,
    GetLoadBalancerMetricDataResultTypeDef,
    GetLoadBalancerResultTypeDef,
    GetLoadBalancersResultTypeDef,
    GetLoadBalancerTlsCertificatesResultTypeDef,
    GetOperationResultTypeDef,
    GetOperationsForResourceResultTypeDef,
    GetOperationsResultTypeDef,
    GetRegionsResultTypeDef,
    GetRelationalDatabaseBlueprintsResultTypeDef,
    GetRelationalDatabaseBundlesResultTypeDef,
    GetRelationalDatabaseEventsResultTypeDef,
    GetRelationalDatabaseLogEventsResultTypeDef,
    GetRelationalDatabaseLogStreamsResultTypeDef,
    GetRelationalDatabaseMasterUserPasswordResultTypeDef,
    GetRelationalDatabaseMetricDataResultTypeDef,
    GetRelationalDatabaseParametersResultTypeDef,
    GetRelationalDatabaseResultTypeDef,
    GetRelationalDatabaseSnapshotResultTypeDef,
    GetRelationalDatabaseSnapshotsResultTypeDef,
    GetRelationalDatabasesResultTypeDef,
    GetStaticIpResultTypeDef,
    GetStaticIpsResultTypeDef,
    ImportKeyPairResultTypeDef,
    InputOriginTypeDef,
    InstanceEntryTypeDef,
    IsVpcPeeredResultTypeDef,
    OpenInstancePublicPortsResultTypeDef,
    PeerVpcResultTypeDef,
    PortInfoTypeDef,
    PutAlarmResultTypeDef,
    PutInstancePublicPortsResultTypeDef,
    RebootInstanceResultTypeDef,
    RebootRelationalDatabaseResultTypeDef,
    RegisterContainerImageResultTypeDef,
    RelationalDatabaseParameterTypeDef,
    ReleaseStaticIpResultTypeDef,
    ResetDistributionCacheResultTypeDef,
    SendContactMethodVerificationResultTypeDef,
    SetIpAddressTypeResultTypeDef,
    SetResourceAccessForBucketResultTypeDef,
    StartInstanceResultTypeDef,
    StartRelationalDatabaseResultTypeDef,
    StopInstanceResultTypeDef,
    StopRelationalDatabaseResultTypeDef,
    TagResourceResultTypeDef,
    TagTypeDef,
    TestAlarmResultTypeDef,
    UnpeerVpcResultTypeDef,
    UntagResourceResultTypeDef,
    UpdateBucketBundleResultTypeDef,
    UpdateBucketResultTypeDef,
    UpdateContainerServiceResultTypeDef,
    UpdateDistributionBundleResultTypeDef,
    UpdateDistributionResultTypeDef,
    UpdateDomainEntryResultTypeDef,
    UpdateLoadBalancerAttributeResultTypeDef,
    UpdateRelationalDatabaseParametersResultTypeDef,
    UpdateRelationalDatabaseResultTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("LightsailClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    AccountSetupInProgressException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    InvalidInputException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    OperationFailureException: Type[BotocoreClientError]
    ServiceException: Type[BotocoreClientError]
    UnauthenticatedException: Type[BotocoreClientError]


class LightsailClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        LightsailClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#exceptions)
        """

    async def allocate_static_ip(self, *, staticIpName: str) -> AllocateStaticIpResultTypeDef:
        """
        Allocates a static IP address.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.allocate_static_ip)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#allocate_static_ip)
        """

    async def attach_certificate_to_distribution(
        self, *, distributionName: str, certificateName: str
    ) -> AttachCertificateToDistributionResultTypeDef:
        """
        Attaches an SSL/TLS certificate to your Amazon Lightsail content delivery
        network (CDN) distribution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.attach_certificate_to_distribution)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#attach_certificate_to_distribution)
        """

    async def attach_disk(
        self, *, diskName: str, instanceName: str, diskPath: str
    ) -> AttachDiskResultTypeDef:
        """
        Attaches a block storage disk to a running or stopped Lightsail instance and
        exposes it to the instance with the specified disk name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.attach_disk)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#attach_disk)
        """

    async def attach_instances_to_load_balancer(
        self, *, loadBalancerName: str, instanceNames: Sequence[str]
    ) -> AttachInstancesToLoadBalancerResultTypeDef:
        """
        Attaches one or more Lightsail instances to a load balancer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.attach_instances_to_load_balancer)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#attach_instances_to_load_balancer)
        """

    async def attach_load_balancer_tls_certificate(
        self, *, loadBalancerName: str, certificateName: str
    ) -> AttachLoadBalancerTlsCertificateResultTypeDef:
        """
        Attaches a Transport Layer Security (TLS) certificate to your load balancer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.attach_load_balancer_tls_certificate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#attach_load_balancer_tls_certificate)
        """

    async def attach_static_ip(
        self, *, staticIpName: str, instanceName: str
    ) -> AttachStaticIpResultTypeDef:
        """
        Attaches a static IP address to a specific Amazon Lightsail instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.attach_static_ip)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#attach_static_ip)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#can_paginate)
        """

    async def close_instance_public_ports(
        self, *, portInfo: "PortInfoTypeDef", instanceName: str
    ) -> CloseInstancePublicPortsResultTypeDef:
        """
        Closes ports for a specific Amazon Lightsail instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.close_instance_public_ports)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#close_instance_public_ports)
        """

    async def copy_snapshot(
        self,
        *,
        targetSnapshotName: str,
        sourceRegion: RegionNameType,
        sourceSnapshotName: str = ...,
        sourceResourceName: str = ...,
        restoreDate: str = ...,
        useLatestRestorableAutoSnapshot: bool = ...
    ) -> CopySnapshotResultTypeDef:
        """
        Copies a manual snapshot of an instance or disk as another manual snapshot, or
        copies an automatic snapshot of an instance or disk as a manual snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.copy_snapshot)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#copy_snapshot)
        """

    async def create_bucket(
        self,
        *,
        bucketName: str,
        bundleId: str,
        tags: Sequence["TagTypeDef"] = ...,
        enableObjectVersioning: bool = ...
    ) -> CreateBucketResultTypeDef:
        """
        Creates an Amazon Lightsail bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.create_bucket)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#create_bucket)
        """

    async def create_bucket_access_key(
        self, *, bucketName: str
    ) -> CreateBucketAccessKeyResultTypeDef:
        """
        Creates a new access key for the specified Amazon Lightsail bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.create_bucket_access_key)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#create_bucket_access_key)
        """

    async def create_certificate(
        self,
        *,
        certificateName: str,
        domainName: str,
        subjectAlternativeNames: Sequence[str] = ...,
        tags: Sequence["TagTypeDef"] = ...
    ) -> CreateCertificateResultTypeDef:
        """
        Creates an SSL/TLS certificate for an Amazon Lightsail content delivery network
        (CDN) distribution and a container service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.create_certificate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#create_certificate)
        """

    async def create_cloud_formation_stack(
        self, *, instances: Sequence["InstanceEntryTypeDef"]
    ) -> CreateCloudFormationStackResultTypeDef:
        """
        Creates an AWS CloudFormation stack, which creates a new Amazon EC2 instance
        from an exported Amazon Lightsail snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.create_cloud_formation_stack)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#create_cloud_formation_stack)
        """

    async def create_contact_method(
        self, *, protocol: ContactProtocolType, contactEndpoint: str
    ) -> CreateContactMethodResultTypeDef:
        """
        Creates an email or SMS text message contact method.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.create_contact_method)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#create_contact_method)
        """

    async def create_container_service(
        self,
        *,
        serviceName: str,
        power: ContainerServicePowerNameType,
        scale: int,
        tags: Sequence["TagTypeDef"] = ...,
        publicDomainNames: Mapping[str, Sequence[str]] = ...,
        deployment: "ContainerServiceDeploymentRequestTypeDef" = ...
    ) -> CreateContainerServiceResultTypeDef:
        """
        Creates an Amazon Lightsail container service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.create_container_service)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#create_container_service)
        """

    async def create_container_service_deployment(
        self,
        *,
        serviceName: str,
        containers: Mapping[str, "ContainerTypeDef"] = ...,
        publicEndpoint: "EndpointRequestTypeDef" = ...
    ) -> CreateContainerServiceDeploymentResultTypeDef:
        """
        Creates a deployment for your Amazon Lightsail container service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.create_container_service_deployment)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#create_container_service_deployment)
        """

    async def create_container_service_registry_login(
        self,
    ) -> CreateContainerServiceRegistryLoginResultTypeDef:
        """
        Creates a temporary set of log in credentials that you can use to log in to the
        Docker process on your local machine.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.create_container_service_registry_login)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#create_container_service_registry_login)
        """

    async def create_disk(
        self,
        *,
        diskName: str,
        availabilityZone: str,
        sizeInGb: int,
        tags: Sequence["TagTypeDef"] = ...,
        addOns: Sequence["AddOnRequestTypeDef"] = ...
    ) -> CreateDiskResultTypeDef:
        """
        Creates a block storage disk that can be attached to an Amazon Lightsail
        instance in the same Availability Zone (e.g., `us-east-2a` ).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.create_disk)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#create_disk)
        """

    async def create_disk_from_snapshot(
        self,
        *,
        diskName: str,
        availabilityZone: str,
        sizeInGb: int,
        diskSnapshotName: str = ...,
        tags: Sequence["TagTypeDef"] = ...,
        addOns: Sequence["AddOnRequestTypeDef"] = ...,
        sourceDiskName: str = ...,
        restoreDate: str = ...,
        useLatestRestorableAutoSnapshot: bool = ...
    ) -> CreateDiskFromSnapshotResultTypeDef:
        """
        Creates a block storage disk from a manual or automatic snapshot of a disk.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.create_disk_from_snapshot)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#create_disk_from_snapshot)
        """

    async def create_disk_snapshot(
        self,
        *,
        diskSnapshotName: str,
        diskName: str = ...,
        instanceName: str = ...,
        tags: Sequence["TagTypeDef"] = ...
    ) -> CreateDiskSnapshotResultTypeDef:
        """
        Creates a snapshot of a block storage disk.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.create_disk_snapshot)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#create_disk_snapshot)
        """

    async def create_distribution(
        self,
        *,
        distributionName: str,
        origin: "InputOriginTypeDef",
        defaultCacheBehavior: "CacheBehaviorTypeDef",
        bundleId: str,
        cacheBehaviorSettings: "CacheSettingsTypeDef" = ...,
        cacheBehaviors: Sequence["CacheBehaviorPerPathTypeDef"] = ...,
        ipAddressType: IpAddressTypeType = ...,
        tags: Sequence["TagTypeDef"] = ...
    ) -> CreateDistributionResultTypeDef:
        """
        Creates an Amazon Lightsail content delivery network (CDN) distribution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.create_distribution)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#create_distribution)
        """

    async def create_domain(
        self, *, domainName: str, tags: Sequence["TagTypeDef"] = ...
    ) -> CreateDomainResultTypeDef:
        """
        Creates a domain resource for the specified domain (e.g., example.com).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.create_domain)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#create_domain)
        """

    async def create_domain_entry(
        self, *, domainName: str, domainEntry: "DomainEntryTypeDef"
    ) -> CreateDomainEntryResultTypeDef:
        """
        Creates one of the following domain name system (DNS) records in a domain DNS
        zone: Address (A), canonical name (CNAME), mail exchanger (MX), name server
        (NS), start of authority (SOA), service locator (SRV), or text (TXT).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.create_domain_entry)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#create_domain_entry)
        """

    async def create_instance_snapshot(
        self, *, instanceSnapshotName: str, instanceName: str, tags: Sequence["TagTypeDef"] = ...
    ) -> CreateInstanceSnapshotResultTypeDef:
        """
        Creates a snapshot of a specific virtual private server, or *instance*.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.create_instance_snapshot)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#create_instance_snapshot)
        """

    async def create_instances(
        self,
        *,
        instanceNames: Sequence[str],
        availabilityZone: str,
        blueprintId: str,
        bundleId: str,
        customImageName: str = ...,
        userData: str = ...,
        keyPairName: str = ...,
        tags: Sequence["TagTypeDef"] = ...,
        addOns: Sequence["AddOnRequestTypeDef"] = ...,
        ipAddressType: IpAddressTypeType = ...
    ) -> CreateInstancesResultTypeDef:
        """
        Creates one or more Amazon Lightsail instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.create_instances)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#create_instances)
        """

    async def create_instances_from_snapshot(
        self,
        *,
        instanceNames: Sequence[str],
        availabilityZone: str,
        bundleId: str,
        attachedDiskMapping: Mapping[str, Sequence["DiskMapTypeDef"]] = ...,
        instanceSnapshotName: str = ...,
        userData: str = ...,
        keyPairName: str = ...,
        tags: Sequence["TagTypeDef"] = ...,
        addOns: Sequence["AddOnRequestTypeDef"] = ...,
        ipAddressType: IpAddressTypeType = ...,
        sourceInstanceName: str = ...,
        restoreDate: str = ...,
        useLatestRestorableAutoSnapshot: bool = ...
    ) -> CreateInstancesFromSnapshotResultTypeDef:
        """
        Creates one or more new instances from a manual or automatic snapshot of an
        instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.create_instances_from_snapshot)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#create_instances_from_snapshot)
        """

    async def create_key_pair(
        self, *, keyPairName: str, tags: Sequence["TagTypeDef"] = ...
    ) -> CreateKeyPairResultTypeDef:
        """
        Creates a custom SSH key pair that you can use with an Amazon Lightsail
        instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.create_key_pair)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#create_key_pair)
        """

    async def create_load_balancer(
        self,
        *,
        loadBalancerName: str,
        instancePort: int,
        healthCheckPath: str = ...,
        certificateName: str = ...,
        certificateDomainName: str = ...,
        certificateAlternativeNames: Sequence[str] = ...,
        tags: Sequence["TagTypeDef"] = ...,
        ipAddressType: IpAddressTypeType = ...
    ) -> CreateLoadBalancerResultTypeDef:
        """
        Creates a Lightsail load balancer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.create_load_balancer)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#create_load_balancer)
        """

    async def create_load_balancer_tls_certificate(
        self,
        *,
        loadBalancerName: str,
        certificateName: str,
        certificateDomainName: str,
        certificateAlternativeNames: Sequence[str] = ...,
        tags: Sequence["TagTypeDef"] = ...
    ) -> CreateLoadBalancerTlsCertificateResultTypeDef:
        """
        Creates an SSL/TLS certificate for an Amazon Lightsail load balancer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.create_load_balancer_tls_certificate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#create_load_balancer_tls_certificate)
        """

    async def create_relational_database(
        self,
        *,
        relationalDatabaseName: str,
        relationalDatabaseBlueprintId: str,
        relationalDatabaseBundleId: str,
        masterDatabaseName: str,
        masterUsername: str,
        availabilityZone: str = ...,
        masterUserPassword: str = ...,
        preferredBackupWindow: str = ...,
        preferredMaintenanceWindow: str = ...,
        publiclyAccessible: bool = ...,
        tags: Sequence["TagTypeDef"] = ...
    ) -> CreateRelationalDatabaseResultTypeDef:
        """
        Creates a new database in Amazon Lightsail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.create_relational_database)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#create_relational_database)
        """

    async def create_relational_database_from_snapshot(
        self,
        *,
        relationalDatabaseName: str,
        availabilityZone: str = ...,
        publiclyAccessible: bool = ...,
        relationalDatabaseSnapshotName: str = ...,
        relationalDatabaseBundleId: str = ...,
        sourceRelationalDatabaseName: str = ...,
        restoreTime: Union[datetime, str] = ...,
        useLatestRestorableTime: bool = ...,
        tags: Sequence["TagTypeDef"] = ...
    ) -> CreateRelationalDatabaseFromSnapshotResultTypeDef:
        """
        Creates a new database from an existing database snapshot in Amazon Lightsail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.create_relational_database_from_snapshot)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#create_relational_database_from_snapshot)
        """

    async def create_relational_database_snapshot(
        self,
        *,
        relationalDatabaseName: str,
        relationalDatabaseSnapshotName: str,
        tags: Sequence["TagTypeDef"] = ...
    ) -> CreateRelationalDatabaseSnapshotResultTypeDef:
        """
        Creates a snapshot of your database in Amazon Lightsail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.create_relational_database_snapshot)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#create_relational_database_snapshot)
        """

    async def delete_alarm(self, *, alarmName: str) -> DeleteAlarmResultTypeDef:
        """
        Deletes an alarm.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.delete_alarm)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#delete_alarm)
        """

    async def delete_auto_snapshot(
        self, *, resourceName: str, date: str
    ) -> DeleteAutoSnapshotResultTypeDef:
        """
        Deletes an automatic snapshot of an instance or disk.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.delete_auto_snapshot)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#delete_auto_snapshot)
        """

    async def delete_bucket(
        self, *, bucketName: str, forceDelete: bool = ...
    ) -> DeleteBucketResultTypeDef:
        """
        Deletes a Amazon Lightsail bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.delete_bucket)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#delete_bucket)
        """

    async def delete_bucket_access_key(
        self, *, bucketName: str, accessKeyId: str
    ) -> DeleteBucketAccessKeyResultTypeDef:
        """
        Deletes an access key for the specified Amazon Lightsail bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.delete_bucket_access_key)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#delete_bucket_access_key)
        """

    async def delete_certificate(self, *, certificateName: str) -> DeleteCertificateResultTypeDef:
        """
        Deletes an SSL/TLS certificate for your Amazon Lightsail content delivery
        network (CDN) distribution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.delete_certificate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#delete_certificate)
        """

    async def delete_contact_method(
        self, *, protocol: ContactProtocolType
    ) -> DeleteContactMethodResultTypeDef:
        """
        Deletes a contact method.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.delete_contact_method)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#delete_contact_method)
        """

    async def delete_container_image(self, *, serviceName: str, image: str) -> Dict[str, Any]:
        """
        Deletes a container image that is registered to your Amazon Lightsail container
        service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.delete_container_image)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#delete_container_image)
        """

    async def delete_container_service(self, *, serviceName: str) -> Dict[str, Any]:
        """
        Deletes your Amazon Lightsail container service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.delete_container_service)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#delete_container_service)
        """

    async def delete_disk(
        self, *, diskName: str, forceDeleteAddOns: bool = ...
    ) -> DeleteDiskResultTypeDef:
        """
        Deletes the specified block storage disk.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.delete_disk)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#delete_disk)
        """

    async def delete_disk_snapshot(
        self, *, diskSnapshotName: str
    ) -> DeleteDiskSnapshotResultTypeDef:
        """
        Deletes the specified disk snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.delete_disk_snapshot)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#delete_disk_snapshot)
        """

    async def delete_distribution(
        self, *, distributionName: str = ...
    ) -> DeleteDistributionResultTypeDef:
        """
        Deletes your Amazon Lightsail content delivery network (CDN) distribution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.delete_distribution)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#delete_distribution)
        """

    async def delete_domain(self, *, domainName: str) -> DeleteDomainResultTypeDef:
        """
        Deletes the specified domain recordset and all of its domain records.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.delete_domain)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#delete_domain)
        """

    async def delete_domain_entry(
        self, *, domainName: str, domainEntry: "DomainEntryTypeDef"
    ) -> DeleteDomainEntryResultTypeDef:
        """
        Deletes a specific domain entry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.delete_domain_entry)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#delete_domain_entry)
        """

    async def delete_instance(
        self, *, instanceName: str, forceDeleteAddOns: bool = ...
    ) -> DeleteInstanceResultTypeDef:
        """
        Deletes an Amazon Lightsail instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.delete_instance)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#delete_instance)
        """

    async def delete_instance_snapshot(
        self, *, instanceSnapshotName: str
    ) -> DeleteInstanceSnapshotResultTypeDef:
        """
        Deletes a specific snapshot of a virtual private server (or *instance* ).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.delete_instance_snapshot)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#delete_instance_snapshot)
        """

    async def delete_key_pair(
        self, *, keyPairName: str, expectedFingerprint: str = ...
    ) -> DeleteKeyPairResultTypeDef:
        """
        Deletes the specified key pair by removing the public key from Amazon Lightsail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.delete_key_pair)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#delete_key_pair)
        """

    async def delete_known_host_keys(
        self, *, instanceName: str
    ) -> DeleteKnownHostKeysResultTypeDef:
        """
        Deletes the known host key or certificate used by the Amazon Lightsail browser-
        based SSH or RDP clients to authenticate an instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.delete_known_host_keys)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#delete_known_host_keys)
        """

    async def delete_load_balancer(
        self, *, loadBalancerName: str
    ) -> DeleteLoadBalancerResultTypeDef:
        """
        Deletes a Lightsail load balancer and all its associated SSL/TLS certificates.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.delete_load_balancer)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#delete_load_balancer)
        """

    async def delete_load_balancer_tls_certificate(
        self, *, loadBalancerName: str, certificateName: str, force: bool = ...
    ) -> DeleteLoadBalancerTlsCertificateResultTypeDef:
        """
        Deletes an SSL/TLS certificate associated with a Lightsail load balancer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.delete_load_balancer_tls_certificate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#delete_load_balancer_tls_certificate)
        """

    async def delete_relational_database(
        self,
        *,
        relationalDatabaseName: str,
        skipFinalSnapshot: bool = ...,
        finalRelationalDatabaseSnapshotName: str = ...
    ) -> DeleteRelationalDatabaseResultTypeDef:
        """
        Deletes a database in Amazon Lightsail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.delete_relational_database)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#delete_relational_database)
        """

    async def delete_relational_database_snapshot(
        self, *, relationalDatabaseSnapshotName: str
    ) -> DeleteRelationalDatabaseSnapshotResultTypeDef:
        """
        Deletes a database snapshot in Amazon Lightsail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.delete_relational_database_snapshot)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#delete_relational_database_snapshot)
        """

    async def detach_certificate_from_distribution(
        self, *, distributionName: str
    ) -> DetachCertificateFromDistributionResultTypeDef:
        """
        Detaches an SSL/TLS certificate from your Amazon Lightsail content delivery
        network (CDN) distribution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.detach_certificate_from_distribution)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#detach_certificate_from_distribution)
        """

    async def detach_disk(self, *, diskName: str) -> DetachDiskResultTypeDef:
        """
        Detaches a stopped block storage disk from a Lightsail instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.detach_disk)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#detach_disk)
        """

    async def detach_instances_from_load_balancer(
        self, *, loadBalancerName: str, instanceNames: Sequence[str]
    ) -> DetachInstancesFromLoadBalancerResultTypeDef:
        """
        Detaches the specified instances from a Lightsail load balancer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.detach_instances_from_load_balancer)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#detach_instances_from_load_balancer)
        """

    async def detach_static_ip(self, *, staticIpName: str) -> DetachStaticIpResultTypeDef:
        """
        Detaches a static IP from the Amazon Lightsail instance to which it is attached.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.detach_static_ip)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#detach_static_ip)
        """

    async def disable_add_on(
        self, *, addOnType: Literal["AutoSnapshot"], resourceName: str
    ) -> DisableAddOnResultTypeDef:
        """
        Disables an add-on for an Amazon Lightsail resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.disable_add_on)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#disable_add_on)
        """

    async def download_default_key_pair(self) -> DownloadDefaultKeyPairResultTypeDef:
        """
        Downloads the regional Amazon Lightsail default key pair.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.download_default_key_pair)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#download_default_key_pair)
        """

    async def enable_add_on(
        self, *, resourceName: str, addOnRequest: "AddOnRequestTypeDef"
    ) -> EnableAddOnResultTypeDef:
        """
        Enables or modifies an add-on for an Amazon Lightsail resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.enable_add_on)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#enable_add_on)
        """

    async def export_snapshot(self, *, sourceSnapshotName: str) -> ExportSnapshotResultTypeDef:
        """
        Exports an Amazon Lightsail instance or block storage disk snapshot to Amazon
        Elastic Compute Cloud (Amazon EC2).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.export_snapshot)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#export_snapshot)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#generate_presigned_url)
        """

    async def get_active_names(self, *, pageToken: str = ...) -> GetActiveNamesResultTypeDef:
        """
        Returns the names of all active (not deleted) resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_active_names)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_active_names)
        """

    async def get_alarms(
        self, *, alarmName: str = ..., pageToken: str = ..., monitoredResourceName: str = ...
    ) -> GetAlarmsResultTypeDef:
        """
        Returns information about the configured alarms.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_alarms)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_alarms)
        """

    async def get_auto_snapshots(self, *, resourceName: str) -> GetAutoSnapshotsResultTypeDef:
        """
        Returns the available automatic snapshots for an instance or disk.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_auto_snapshots)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_auto_snapshots)
        """

    async def get_blueprints(
        self, *, includeInactive: bool = ..., pageToken: str = ...
    ) -> GetBlueprintsResultTypeDef:
        """
        Returns the list of available instance images, or *blueprints*.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_blueprints)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_blueprints)
        """

    async def get_bucket_access_keys(self, *, bucketName: str) -> GetBucketAccessKeysResultTypeDef:
        """
        Returns the existing access key IDs for the specified Amazon Lightsail bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_bucket_access_keys)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_bucket_access_keys)
        """

    async def get_bucket_bundles(
        self, *, includeInactive: bool = ...
    ) -> GetBucketBundlesResultTypeDef:
        """
        Returns the bundles that you can apply to a Amazon Lightsail bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_bucket_bundles)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_bucket_bundles)
        """

    async def get_bucket_metric_data(
        self,
        *,
        bucketName: str,
        metricName: BucketMetricNameType,
        startTime: Union[datetime, str],
        endTime: Union[datetime, str],
        period: int,
        statistics: Sequence[MetricStatisticType],
        unit: MetricUnitType
    ) -> GetBucketMetricDataResultTypeDef:
        """
        Returns the data points of a specific metric for an Amazon Lightsail bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_bucket_metric_data)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_bucket_metric_data)
        """

    async def get_buckets(
        self, *, bucketName: str = ..., pageToken: str = ..., includeConnectedResources: bool = ...
    ) -> GetBucketsResultTypeDef:
        """
        Returns information about one or more Amazon Lightsail buckets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_buckets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_buckets)
        """

    async def get_bundles(
        self, *, includeInactive: bool = ..., pageToken: str = ...
    ) -> GetBundlesResultTypeDef:
        """
        Returns the list of bundles that are available for purchase.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_bundles)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_bundles)
        """

    async def get_certificates(
        self,
        *,
        certificateStatuses: Sequence[CertificateStatusType] = ...,
        includeCertificateDetails: bool = ...,
        certificateName: str = ...
    ) -> GetCertificatesResultTypeDef:
        """
        Returns information about one or more Amazon Lightsail SSL/TLS certificates.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_certificates)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_certificates)
        """

    async def get_cloud_formation_stack_records(
        self, *, pageToken: str = ...
    ) -> GetCloudFormationStackRecordsResultTypeDef:
        """
        Returns the CloudFormation stack record created as a result of the `create cloud
        formation stack` operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_cloud_formation_stack_records)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_cloud_formation_stack_records)
        """

    async def get_contact_methods(
        self, *, protocols: Sequence[ContactProtocolType] = ...
    ) -> GetContactMethodsResultTypeDef:
        """
        Returns information about the configured contact methods.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_contact_methods)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_contact_methods)
        """

    async def get_container_api_metadata(self) -> GetContainerAPIMetadataResultTypeDef:
        """
        Returns information about Amazon Lightsail containers, such as the current
        version of the Lightsail Control (lightsailctl) plugin.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_container_api_metadata)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_container_api_metadata)
        """

    async def get_container_images(self, *, serviceName: str) -> GetContainerImagesResultTypeDef:
        """
        Returns the container images that are registered to your Amazon Lightsail
        container service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_container_images)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_container_images)
        """

    async def get_container_log(
        self,
        *,
        serviceName: str,
        containerName: str,
        startTime: Union[datetime, str] = ...,
        endTime: Union[datetime, str] = ...,
        filterPattern: str = ...,
        pageToken: str = ...
    ) -> GetContainerLogResultTypeDef:
        """
        Returns the log events of a container of your Amazon Lightsail container
        service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_container_log)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_container_log)
        """

    async def get_container_service_deployments(
        self, *, serviceName: str
    ) -> GetContainerServiceDeploymentsResultTypeDef:
        """
        Returns the deployments for your Amazon Lightsail container service A deployment
        specifies the settings, such as the ports and launch command, of containers that
        are deployed to your container service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_container_service_deployments)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_container_service_deployments)
        """

    async def get_container_service_metric_data(
        self,
        *,
        serviceName: str,
        metricName: ContainerServiceMetricNameType,
        startTime: Union[datetime, str],
        endTime: Union[datetime, str],
        period: int,
        statistics: Sequence[MetricStatisticType]
    ) -> GetContainerServiceMetricDataResultTypeDef:
        """
        Returns the data points of a specific metric of your Amazon Lightsail container
        service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_container_service_metric_data)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_container_service_metric_data)
        """

    async def get_container_service_powers(self) -> GetContainerServicePowersResultTypeDef:
        """
        Returns the list of powers that can be specified for your Amazon Lightsail
        container services.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_container_service_powers)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_container_service_powers)
        """

    async def get_container_services(
        self, *, serviceName: str = ...
    ) -> ContainerServicesListResultTypeDef:
        """
        Returns information about one or more of your Amazon Lightsail container
        services.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_container_services)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_container_services)
        """

    async def get_disk(self, *, diskName: str) -> GetDiskResultTypeDef:
        """
        Returns information about a specific block storage disk.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_disk)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_disk)
        """

    async def get_disk_snapshot(self, *, diskSnapshotName: str) -> GetDiskSnapshotResultTypeDef:
        """
        Returns information about a specific block storage disk snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_disk_snapshot)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_disk_snapshot)
        """

    async def get_disk_snapshots(self, *, pageToken: str = ...) -> GetDiskSnapshotsResultTypeDef:
        """
        Returns information about all block storage disk snapshots in your AWS account
        and region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_disk_snapshots)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_disk_snapshots)
        """

    async def get_disks(self, *, pageToken: str = ...) -> GetDisksResultTypeDef:
        """
        Returns information about all block storage disks in your AWS account and
        region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_disks)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_disks)
        """

    async def get_distribution_bundles(self) -> GetDistributionBundlesResultTypeDef:
        """
        Returns the bundles that can be applied to your Amazon Lightsail content
        delivery network (CDN) distributions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_distribution_bundles)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_distribution_bundles)
        """

    async def get_distribution_latest_cache_reset(
        self, *, distributionName: str = ...
    ) -> GetDistributionLatestCacheResetResultTypeDef:
        """
        Returns the timestamp and status of the last cache reset of a specific Amazon
        Lightsail content delivery network (CDN) distribution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_distribution_latest_cache_reset)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_distribution_latest_cache_reset)
        """

    async def get_distribution_metric_data(
        self,
        *,
        distributionName: str,
        metricName: DistributionMetricNameType,
        startTime: Union[datetime, str],
        endTime: Union[datetime, str],
        period: int,
        unit: MetricUnitType,
        statistics: Sequence[MetricStatisticType]
    ) -> GetDistributionMetricDataResultTypeDef:
        """
        Returns the data points of a specific metric for an Amazon Lightsail content
        delivery network (CDN) distribution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_distribution_metric_data)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_distribution_metric_data)
        """

    async def get_distributions(
        self, *, distributionName: str = ..., pageToken: str = ...
    ) -> GetDistributionsResultTypeDef:
        """
        Returns information about one or more of your Amazon Lightsail content delivery
        network (CDN) distributions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_distributions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_distributions)
        """

    async def get_domain(self, *, domainName: str) -> GetDomainResultTypeDef:
        """
        Returns information about a specific domain recordset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_domain)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_domain)
        """

    async def get_domains(self, *, pageToken: str = ...) -> GetDomainsResultTypeDef:
        """
        Returns a list of all domains in the user's account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_domains)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_domains)
        """

    async def get_export_snapshot_records(
        self, *, pageToken: str = ...
    ) -> GetExportSnapshotRecordsResultTypeDef:
        """
        Returns all export snapshot records created as a result of the `export snapshot`
        operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_export_snapshot_records)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_export_snapshot_records)
        """

    async def get_instance(self, *, instanceName: str) -> GetInstanceResultTypeDef:
        """
        Returns information about a specific Amazon Lightsail instance, which is a
        virtual private server.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_instance)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_instance)
        """

    async def get_instance_access_details(
        self, *, instanceName: str, protocol: InstanceAccessProtocolType = ...
    ) -> GetInstanceAccessDetailsResultTypeDef:
        """
        Returns temporary SSH keys you can use to connect to a specific virtual private
        server, or *instance* .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_instance_access_details)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_instance_access_details)
        """

    async def get_instance_metric_data(
        self,
        *,
        instanceName: str,
        metricName: InstanceMetricNameType,
        period: int,
        startTime: Union[datetime, str],
        endTime: Union[datetime, str],
        unit: MetricUnitType,
        statistics: Sequence[MetricStatisticType]
    ) -> GetInstanceMetricDataResultTypeDef:
        """
        Returns the data points for the specified Amazon Lightsail instance metric,
        given an instance name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_instance_metric_data)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_instance_metric_data)
        """

    async def get_instance_port_states(
        self, *, instanceName: str
    ) -> GetInstancePortStatesResultTypeDef:
        """
        Returns the firewall port states for a specific Amazon Lightsail instance, the
        IP addresses allowed to connect to the instance through the ports, and the
        protocol.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_instance_port_states)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_instance_port_states)
        """

    async def get_instance_snapshot(
        self, *, instanceSnapshotName: str
    ) -> GetInstanceSnapshotResultTypeDef:
        """
        Returns information about a specific instance snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_instance_snapshot)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_instance_snapshot)
        """

    async def get_instance_snapshots(
        self, *, pageToken: str = ...
    ) -> GetInstanceSnapshotsResultTypeDef:
        """
        Returns all instance snapshots for the user's account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_instance_snapshots)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_instance_snapshots)
        """

    async def get_instance_state(self, *, instanceName: str) -> GetInstanceStateResultTypeDef:
        """
        Returns the state of a specific instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_instance_state)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_instance_state)
        """

    async def get_instances(self, *, pageToken: str = ...) -> GetInstancesResultTypeDef:
        """
        Returns information about all Amazon Lightsail virtual private servers, or
        *instances* .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_instances)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_instances)
        """

    async def get_key_pair(self, *, keyPairName: str) -> GetKeyPairResultTypeDef:
        """
        Returns information about a specific key pair.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_key_pair)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_key_pair)
        """

    async def get_key_pairs(
        self, *, pageToken: str = ..., includeDefaultKeyPair: bool = ...
    ) -> GetKeyPairsResultTypeDef:
        """
        Returns information about all key pairs in the user's account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_key_pairs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_key_pairs)
        """

    async def get_load_balancer(self, *, loadBalancerName: str) -> GetLoadBalancerResultTypeDef:
        """
        Returns information about the specified Lightsail load balancer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_load_balancer)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_load_balancer)
        """

    async def get_load_balancer_metric_data(
        self,
        *,
        loadBalancerName: str,
        metricName: LoadBalancerMetricNameType,
        period: int,
        startTime: Union[datetime, str],
        endTime: Union[datetime, str],
        unit: MetricUnitType,
        statistics: Sequence[MetricStatisticType]
    ) -> GetLoadBalancerMetricDataResultTypeDef:
        """
        Returns information about health metrics for your Lightsail load balancer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_load_balancer_metric_data)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_load_balancer_metric_data)
        """

    async def get_load_balancer_tls_certificates(
        self, *, loadBalancerName: str
    ) -> GetLoadBalancerTlsCertificatesResultTypeDef:
        """
        Returns information about the TLS certificates that are associated with the
        specified Lightsail load balancer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_load_balancer_tls_certificates)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_load_balancer_tls_certificates)
        """

    async def get_load_balancers(self, *, pageToken: str = ...) -> GetLoadBalancersResultTypeDef:
        """
        Returns information about all load balancers in an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_load_balancers)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_load_balancers)
        """

    async def get_operation(self, *, operationId: str) -> GetOperationResultTypeDef:
        """
        Returns information about a specific operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_operation)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_operation)
        """

    async def get_operations(self, *, pageToken: str = ...) -> GetOperationsResultTypeDef:
        """
        Returns information about all operations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_operations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_operations)
        """

    async def get_operations_for_resource(
        self, *, resourceName: str, pageToken: str = ...
    ) -> GetOperationsForResourceResultTypeDef:
        """
        Gets operations for a specific resource (e.g., an instance or a static IP).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_operations_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_operations_for_resource)
        """

    async def get_regions(
        self,
        *,
        includeAvailabilityZones: bool = ...,
        includeRelationalDatabaseAvailabilityZones: bool = ...
    ) -> GetRegionsResultTypeDef:
        """
        Returns a list of all valid regions for Amazon Lightsail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_regions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_regions)
        """

    async def get_relational_database(
        self, *, relationalDatabaseName: str
    ) -> GetRelationalDatabaseResultTypeDef:
        """
        Returns information about a specific database in Amazon Lightsail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_relational_database)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_relational_database)
        """

    async def get_relational_database_blueprints(
        self, *, pageToken: str = ...
    ) -> GetRelationalDatabaseBlueprintsResultTypeDef:
        """
        Returns a list of available database blueprints in Amazon Lightsail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_relational_database_blueprints)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_relational_database_blueprints)
        """

    async def get_relational_database_bundles(
        self, *, pageToken: str = ...
    ) -> GetRelationalDatabaseBundlesResultTypeDef:
        """
        Returns the list of bundles that are available in Amazon Lightsail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_relational_database_bundles)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_relational_database_bundles)
        """

    async def get_relational_database_events(
        self, *, relationalDatabaseName: str, durationInMinutes: int = ..., pageToken: str = ...
    ) -> GetRelationalDatabaseEventsResultTypeDef:
        """
        Returns a list of events for a specific database in Amazon Lightsail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_relational_database_events)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_relational_database_events)
        """

    async def get_relational_database_log_events(
        self,
        *,
        relationalDatabaseName: str,
        logStreamName: str,
        startTime: Union[datetime, str] = ...,
        endTime: Union[datetime, str] = ...,
        startFromHead: bool = ...,
        pageToken: str = ...
    ) -> GetRelationalDatabaseLogEventsResultTypeDef:
        """
        Returns a list of log events for a database in Amazon Lightsail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_relational_database_log_events)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_relational_database_log_events)
        """

    async def get_relational_database_log_streams(
        self, *, relationalDatabaseName: str
    ) -> GetRelationalDatabaseLogStreamsResultTypeDef:
        """
        Returns a list of available log streams for a specific database in Amazon
        Lightsail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_relational_database_log_streams)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_relational_database_log_streams)
        """

    async def get_relational_database_master_user_password(
        self,
        *,
        relationalDatabaseName: str,
        passwordVersion: RelationalDatabasePasswordVersionType = ...
    ) -> GetRelationalDatabaseMasterUserPasswordResultTypeDef:
        """
        Returns the current, previous, or pending versions of the master user password
        for a Lightsail database.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_relational_database_master_user_password)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_relational_database_master_user_password)
        """

    async def get_relational_database_metric_data(
        self,
        *,
        relationalDatabaseName: str,
        metricName: RelationalDatabaseMetricNameType,
        period: int,
        startTime: Union[datetime, str],
        endTime: Union[datetime, str],
        unit: MetricUnitType,
        statistics: Sequence[MetricStatisticType]
    ) -> GetRelationalDatabaseMetricDataResultTypeDef:
        """
        Returns the data points of the specified metric for a database in Amazon
        Lightsail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_relational_database_metric_data)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_relational_database_metric_data)
        """

    async def get_relational_database_parameters(
        self, *, relationalDatabaseName: str, pageToken: str = ...
    ) -> GetRelationalDatabaseParametersResultTypeDef:
        """
        Returns all of the runtime parameters offered by the underlying database
        software, or engine, for a specific database in Amazon Lightsail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_relational_database_parameters)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_relational_database_parameters)
        """

    async def get_relational_database_snapshot(
        self, *, relationalDatabaseSnapshotName: str
    ) -> GetRelationalDatabaseSnapshotResultTypeDef:
        """
        Returns information about a specific database snapshot in Amazon Lightsail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_relational_database_snapshot)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_relational_database_snapshot)
        """

    async def get_relational_database_snapshots(
        self, *, pageToken: str = ...
    ) -> GetRelationalDatabaseSnapshotsResultTypeDef:
        """
        Returns information about all of your database snapshots in Amazon Lightsail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_relational_database_snapshots)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_relational_database_snapshots)
        """

    async def get_relational_databases(
        self, *, pageToken: str = ...
    ) -> GetRelationalDatabasesResultTypeDef:
        """
        Returns information about all of your databases in Amazon Lightsail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_relational_databases)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_relational_databases)
        """

    async def get_static_ip(self, *, staticIpName: str) -> GetStaticIpResultTypeDef:
        """
        Returns information about an Amazon Lightsail static IP.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_static_ip)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_static_ip)
        """

    async def get_static_ips(self, *, pageToken: str = ...) -> GetStaticIpsResultTypeDef:
        """
        Returns information about all static IPs in the user's account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_static_ips)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_static_ips)
        """

    async def import_key_pair(
        self, *, keyPairName: str, publicKeyBase64: str
    ) -> ImportKeyPairResultTypeDef:
        """
        Imports a public SSH key from a specific key pair.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.import_key_pair)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#import_key_pair)
        """

    async def is_vpc_peered(self) -> IsVpcPeeredResultTypeDef:
        """
        Returns a Boolean value indicating whether your Lightsail VPC is peered.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.is_vpc_peered)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#is_vpc_peered)
        """

    async def open_instance_public_ports(
        self, *, portInfo: "PortInfoTypeDef", instanceName: str
    ) -> OpenInstancePublicPortsResultTypeDef:
        """
        Opens ports for a specific Amazon Lightsail instance, and specifies the IP
        addresses allowed to connect to the instance through the ports, and the
        protocol.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.open_instance_public_ports)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#open_instance_public_ports)
        """

    async def peer_vpc(self) -> PeerVpcResultTypeDef:
        """
        Peers the Lightsail VPC with the user's default VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.peer_vpc)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#peer_vpc)
        """

    async def put_alarm(
        self,
        *,
        alarmName: str,
        metricName: MetricNameType,
        monitoredResourceName: str,
        comparisonOperator: ComparisonOperatorType,
        threshold: float,
        evaluationPeriods: int,
        datapointsToAlarm: int = ...,
        treatMissingData: TreatMissingDataType = ...,
        contactProtocols: Sequence[ContactProtocolType] = ...,
        notificationTriggers: Sequence[AlarmStateType] = ...,
        notificationEnabled: bool = ...
    ) -> PutAlarmResultTypeDef:
        """
        Creates or updates an alarm, and associates it with the specified metric.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.put_alarm)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#put_alarm)
        """

    async def put_instance_public_ports(
        self, *, portInfos: Sequence["PortInfoTypeDef"], instanceName: str
    ) -> PutInstancePublicPortsResultTypeDef:
        """
        Opens ports for a specific Amazon Lightsail instance, and specifies the IP
        addresses allowed to connect to the instance through the ports, and the
        protocol.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.put_instance_public_ports)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#put_instance_public_ports)
        """

    async def reboot_instance(self, *, instanceName: str) -> RebootInstanceResultTypeDef:
        """
        Restarts a specific instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.reboot_instance)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#reboot_instance)
        """

    async def reboot_relational_database(
        self, *, relationalDatabaseName: str
    ) -> RebootRelationalDatabaseResultTypeDef:
        """
        Restarts a specific database in Amazon Lightsail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.reboot_relational_database)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#reboot_relational_database)
        """

    async def register_container_image(
        self, *, serviceName: str, label: str, digest: str
    ) -> RegisterContainerImageResultTypeDef:
        """
        Registers a container image to your Amazon Lightsail container service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.register_container_image)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#register_container_image)
        """

    async def release_static_ip(self, *, staticIpName: str) -> ReleaseStaticIpResultTypeDef:
        """
        Deletes a specific static IP from your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.release_static_ip)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#release_static_ip)
        """

    async def reset_distribution_cache(
        self, *, distributionName: str = ...
    ) -> ResetDistributionCacheResultTypeDef:
        """
        Deletes currently cached content from your Amazon Lightsail content delivery
        network (CDN) distribution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.reset_distribution_cache)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#reset_distribution_cache)
        """

    async def send_contact_method_verification(
        self, *, protocol: Literal["Email"]
    ) -> SendContactMethodVerificationResultTypeDef:
        """
        Sends a verification request to an email contact method to ensure it's owned by
        the requester.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.send_contact_method_verification)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#send_contact_method_verification)
        """

    async def set_ip_address_type(
        self, *, resourceType: ResourceTypeType, resourceName: str, ipAddressType: IpAddressTypeType
    ) -> SetIpAddressTypeResultTypeDef:
        """
        Sets the IP address type for an Amazon Lightsail resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.set_ip_address_type)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#set_ip_address_type)
        """

    async def set_resource_access_for_bucket(
        self, *, resourceName: str, bucketName: str, access: ResourceBucketAccessType
    ) -> SetResourceAccessForBucketResultTypeDef:
        """
        Sets the Amazon Lightsail resources that can access the specified Lightsail
        bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.set_resource_access_for_bucket)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#set_resource_access_for_bucket)
        """

    async def start_instance(self, *, instanceName: str) -> StartInstanceResultTypeDef:
        """
        Starts a specific Amazon Lightsail instance from a stopped state.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.start_instance)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#start_instance)
        """

    async def start_relational_database(
        self, *, relationalDatabaseName: str
    ) -> StartRelationalDatabaseResultTypeDef:
        """
        Starts a specific database from a stopped state in Amazon Lightsail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.start_relational_database)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#start_relational_database)
        """

    async def stop_instance(
        self, *, instanceName: str, force: bool = ...
    ) -> StopInstanceResultTypeDef:
        """
        Stops a specific Amazon Lightsail instance that is currently running.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.stop_instance)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#stop_instance)
        """

    async def stop_relational_database(
        self, *, relationalDatabaseName: str, relationalDatabaseSnapshotName: str = ...
    ) -> StopRelationalDatabaseResultTypeDef:
        """
        Stops a specific database that is currently running in Amazon Lightsail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.stop_relational_database)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#stop_relational_database)
        """

    async def tag_resource(
        self, *, resourceName: str, tags: Sequence["TagTypeDef"], resourceArn: str = ...
    ) -> TagResourceResultTypeDef:
        """
        Adds one or more tags to the specified Amazon Lightsail resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#tag_resource)
        """

    async def test_alarm(self, *, alarmName: str, state: AlarmStateType) -> TestAlarmResultTypeDef:
        """
        Tests an alarm by displaying a banner on the Amazon Lightsail console.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.test_alarm)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#test_alarm)
        """

    async def unpeer_vpc(self) -> UnpeerVpcResultTypeDef:
        """
        Unpeers the Lightsail VPC from the user's default VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.unpeer_vpc)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#unpeer_vpc)
        """

    async def untag_resource(
        self, *, resourceName: str, tagKeys: Sequence[str], resourceArn: str = ...
    ) -> UntagResourceResultTypeDef:
        """
        Deletes the specified set of tag keys and their values from the specified Amazon
        Lightsail resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#untag_resource)
        """

    async def update_bucket(
        self,
        *,
        bucketName: str,
        accessRules: "AccessRulesTypeDef" = ...,
        versioning: str = ...,
        readonlyAccessAccounts: Sequence[str] = ...,
        accessLogConfig: "BucketAccessLogConfigTypeDef" = ...
    ) -> UpdateBucketResultTypeDef:
        """
        Updates an existing Amazon Lightsail bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.update_bucket)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#update_bucket)
        """

    async def update_bucket_bundle(
        self, *, bucketName: str, bundleId: str
    ) -> UpdateBucketBundleResultTypeDef:
        """
        Updates the bundle, or storage plan, of an existing Amazon Lightsail bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.update_bucket_bundle)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#update_bucket_bundle)
        """

    async def update_container_service(
        self,
        *,
        serviceName: str,
        power: ContainerServicePowerNameType = ...,
        scale: int = ...,
        isDisabled: bool = ...,
        publicDomainNames: Mapping[str, Sequence[str]] = ...
    ) -> UpdateContainerServiceResultTypeDef:
        """
        Updates the configuration of your Amazon Lightsail container service, such as
        its power, scale, and public domain names.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.update_container_service)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#update_container_service)
        """

    async def update_distribution(
        self,
        *,
        distributionName: str,
        origin: "InputOriginTypeDef" = ...,
        defaultCacheBehavior: "CacheBehaviorTypeDef" = ...,
        cacheBehaviorSettings: "CacheSettingsTypeDef" = ...,
        cacheBehaviors: Sequence["CacheBehaviorPerPathTypeDef"] = ...,
        isEnabled: bool = ...
    ) -> UpdateDistributionResultTypeDef:
        """
        Updates an existing Amazon Lightsail content delivery network (CDN)
        distribution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.update_distribution)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#update_distribution)
        """

    async def update_distribution_bundle(
        self, *, distributionName: str = ..., bundleId: str = ...
    ) -> UpdateDistributionBundleResultTypeDef:
        """
        Updates the bundle of your Amazon Lightsail content delivery network (CDN)
        distribution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.update_distribution_bundle)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#update_distribution_bundle)
        """

    async def update_domain_entry(
        self, *, domainName: str, domainEntry: "DomainEntryTypeDef"
    ) -> UpdateDomainEntryResultTypeDef:
        """
        Updates a domain recordset after it is created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.update_domain_entry)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#update_domain_entry)
        """

    async def update_load_balancer_attribute(
        self,
        *,
        loadBalancerName: str,
        attributeName: LoadBalancerAttributeNameType,
        attributeValue: str
    ) -> UpdateLoadBalancerAttributeResultTypeDef:
        """
        Updates the specified attribute for a load balancer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.update_load_balancer_attribute)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#update_load_balancer_attribute)
        """

    async def update_relational_database(
        self,
        *,
        relationalDatabaseName: str,
        masterUserPassword: str = ...,
        rotateMasterUserPassword: bool = ...,
        preferredBackupWindow: str = ...,
        preferredMaintenanceWindow: str = ...,
        enableBackupRetention: bool = ...,
        disableBackupRetention: bool = ...,
        publiclyAccessible: bool = ...,
        applyImmediately: bool = ...,
        caCertificateIdentifier: str = ...
    ) -> UpdateRelationalDatabaseResultTypeDef:
        """
        Allows the update of one or more attributes of a database in Amazon Lightsail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.update_relational_database)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#update_relational_database)
        """

    async def update_relational_database_parameters(
        self,
        *,
        relationalDatabaseName: str,
        parameters: Sequence["RelationalDatabaseParameterTypeDef"]
    ) -> UpdateRelationalDatabaseParametersResultTypeDef:
        """
        Allows the update of one or more parameters of a database in Amazon Lightsail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.update_relational_database_parameters)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#update_relational_database_parameters)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_active_names"]) -> GetActiveNamesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_blueprints"]) -> GetBlueprintsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_bundles"]) -> GetBundlesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_cloud_formation_stack_records"]
    ) -> GetCloudFormationStackRecordsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_disk_snapshots"]
    ) -> GetDiskSnapshotsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_disks"]) -> GetDisksPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_domains"]) -> GetDomainsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_export_snapshot_records"]
    ) -> GetExportSnapshotRecordsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_instance_snapshots"]
    ) -> GetInstanceSnapshotsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_instances"]) -> GetInstancesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_key_pairs"]) -> GetKeyPairsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_load_balancers"]
    ) -> GetLoadBalancersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_operations"]) -> GetOperationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_relational_database_blueprints"]
    ) -> GetRelationalDatabaseBlueprintsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_relational_database_bundles"]
    ) -> GetRelationalDatabaseBundlesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_relational_database_events"]
    ) -> GetRelationalDatabaseEventsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_relational_database_parameters"]
    ) -> GetRelationalDatabaseParametersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_relational_database_snapshots"]
    ) -> GetRelationalDatabaseSnapshotsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_relational_databases"]
    ) -> GetRelationalDatabasesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_static_ips"]) -> GetStaticIpsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/#get_paginator)
        """

    async def __aenter__(self) -> "LightsailClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/client/)
        """
