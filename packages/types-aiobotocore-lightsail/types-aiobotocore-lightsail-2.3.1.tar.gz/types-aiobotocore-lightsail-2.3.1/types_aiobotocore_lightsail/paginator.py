"""
Type annotations for lightsail service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_lightsail.client import LightsailClient
    from types_aiobotocore_lightsail.paginator import (
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

    session = get_session()
    with session.create_client("lightsail") as client:
        client: LightsailClient

        get_active_names_paginator: GetActiveNamesPaginator = client.get_paginator("get_active_names")
        get_blueprints_paginator: GetBlueprintsPaginator = client.get_paginator("get_blueprints")
        get_bundles_paginator: GetBundlesPaginator = client.get_paginator("get_bundles")
        get_cloud_formation_stack_records_paginator: GetCloudFormationStackRecordsPaginator = client.get_paginator("get_cloud_formation_stack_records")
        get_disk_snapshots_paginator: GetDiskSnapshotsPaginator = client.get_paginator("get_disk_snapshots")
        get_disks_paginator: GetDisksPaginator = client.get_paginator("get_disks")
        get_domains_paginator: GetDomainsPaginator = client.get_paginator("get_domains")
        get_export_snapshot_records_paginator: GetExportSnapshotRecordsPaginator = client.get_paginator("get_export_snapshot_records")
        get_instance_snapshots_paginator: GetInstanceSnapshotsPaginator = client.get_paginator("get_instance_snapshots")
        get_instances_paginator: GetInstancesPaginator = client.get_paginator("get_instances")
        get_key_pairs_paginator: GetKeyPairsPaginator = client.get_paginator("get_key_pairs")
        get_load_balancers_paginator: GetLoadBalancersPaginator = client.get_paginator("get_load_balancers")
        get_operations_paginator: GetOperationsPaginator = client.get_paginator("get_operations")
        get_relational_database_blueprints_paginator: GetRelationalDatabaseBlueprintsPaginator = client.get_paginator("get_relational_database_blueprints")
        get_relational_database_bundles_paginator: GetRelationalDatabaseBundlesPaginator = client.get_paginator("get_relational_database_bundles")
        get_relational_database_events_paginator: GetRelationalDatabaseEventsPaginator = client.get_paginator("get_relational_database_events")
        get_relational_database_parameters_paginator: GetRelationalDatabaseParametersPaginator = client.get_paginator("get_relational_database_parameters")
        get_relational_database_snapshots_paginator: GetRelationalDatabaseSnapshotsPaginator = client.get_paginator("get_relational_database_snapshots")
        get_relational_databases_paginator: GetRelationalDatabasesPaginator = client.get_paginator("get_relational_databases")
        get_static_ips_paginator: GetStaticIpsPaginator = client.get_paginator("get_static_ips")
    ```
"""
import sys
from typing import Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    GetActiveNamesResultTypeDef,
    GetBlueprintsResultTypeDef,
    GetBundlesResultTypeDef,
    GetCloudFormationStackRecordsResultTypeDef,
    GetDiskSnapshotsResultTypeDef,
    GetDisksResultTypeDef,
    GetDomainsResultTypeDef,
    GetExportSnapshotRecordsResultTypeDef,
    GetInstanceSnapshotsResultTypeDef,
    GetInstancesResultTypeDef,
    GetKeyPairsResultTypeDef,
    GetLoadBalancersResultTypeDef,
    GetOperationsResultTypeDef,
    GetRelationalDatabaseBlueprintsResultTypeDef,
    GetRelationalDatabaseBundlesResultTypeDef,
    GetRelationalDatabaseEventsResultTypeDef,
    GetRelationalDatabaseParametersResultTypeDef,
    GetRelationalDatabaseSnapshotsResultTypeDef,
    GetRelationalDatabasesResultTypeDef,
    GetStaticIpsResultTypeDef,
    PaginatorConfigTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import AsyncIterator
else:
    from typing_extensions import AsyncIterator


__all__ = (
    "GetActiveNamesPaginator",
    "GetBlueprintsPaginator",
    "GetBundlesPaginator",
    "GetCloudFormationStackRecordsPaginator",
    "GetDiskSnapshotsPaginator",
    "GetDisksPaginator",
    "GetDomainsPaginator",
    "GetExportSnapshotRecordsPaginator",
    "GetInstanceSnapshotsPaginator",
    "GetInstancesPaginator",
    "GetKeyPairsPaginator",
    "GetLoadBalancersPaginator",
    "GetOperationsPaginator",
    "GetRelationalDatabaseBlueprintsPaginator",
    "GetRelationalDatabaseBundlesPaginator",
    "GetRelationalDatabaseEventsPaginator",
    "GetRelationalDatabaseParametersPaginator",
    "GetRelationalDatabaseSnapshotsPaginator",
    "GetRelationalDatabasesPaginator",
    "GetStaticIpsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class GetActiveNamesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Paginator.GetActiveNames)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getactivenamespaginator)
    """

    def paginate(
        self, *, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[GetActiveNamesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Paginator.GetActiveNames.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getactivenamespaginator)
        """


class GetBlueprintsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Paginator.GetBlueprints)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getblueprintspaginator)
    """

    def paginate(
        self, *, includeInactive: bool = ..., PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[GetBlueprintsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Paginator.GetBlueprints.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getblueprintspaginator)
        """


class GetBundlesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Paginator.GetBundles)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getbundlespaginator)
    """

    def paginate(
        self, *, includeInactive: bool = ..., PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[GetBundlesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Paginator.GetBundles.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getbundlespaginator)
        """


class GetCloudFormationStackRecordsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Paginator.GetCloudFormationStackRecords)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getcloudformationstackrecordspaginator)
    """

    def paginate(
        self, *, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[GetCloudFormationStackRecordsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Paginator.GetCloudFormationStackRecords.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getcloudformationstackrecordspaginator)
        """


class GetDiskSnapshotsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Paginator.GetDiskSnapshots)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getdisksnapshotspaginator)
    """

    def paginate(
        self, *, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[GetDiskSnapshotsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Paginator.GetDiskSnapshots.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getdisksnapshotspaginator)
        """


class GetDisksPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Paginator.GetDisks)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getdiskspaginator)
    """

    def paginate(
        self, *, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[GetDisksResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Paginator.GetDisks.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getdiskspaginator)
        """


class GetDomainsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Paginator.GetDomains)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getdomainspaginator)
    """

    def paginate(
        self, *, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[GetDomainsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Paginator.GetDomains.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getdomainspaginator)
        """


class GetExportSnapshotRecordsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Paginator.GetExportSnapshotRecords)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getexportsnapshotrecordspaginator)
    """

    def paginate(
        self, *, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[GetExportSnapshotRecordsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Paginator.GetExportSnapshotRecords.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getexportsnapshotrecordspaginator)
        """


class GetInstanceSnapshotsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Paginator.GetInstanceSnapshots)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getinstancesnapshotspaginator)
    """

    def paginate(
        self, *, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[GetInstanceSnapshotsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Paginator.GetInstanceSnapshots.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getinstancesnapshotspaginator)
        """


class GetInstancesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Paginator.GetInstances)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getinstancespaginator)
    """

    def paginate(
        self, *, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[GetInstancesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Paginator.GetInstances.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getinstancespaginator)
        """


class GetKeyPairsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Paginator.GetKeyPairs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getkeypairspaginator)
    """

    def paginate(
        self, *, includeDefaultKeyPair: bool = ..., PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[GetKeyPairsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Paginator.GetKeyPairs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getkeypairspaginator)
        """


class GetLoadBalancersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Paginator.GetLoadBalancers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getloadbalancerspaginator)
    """

    def paginate(
        self, *, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[GetLoadBalancersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Paginator.GetLoadBalancers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getloadbalancerspaginator)
        """


class GetOperationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Paginator.GetOperations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getoperationspaginator)
    """

    def paginate(
        self, *, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[GetOperationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Paginator.GetOperations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getoperationspaginator)
        """


class GetRelationalDatabaseBlueprintsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Paginator.GetRelationalDatabaseBlueprints)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getrelationaldatabaseblueprintspaginator)
    """

    def paginate(
        self, *, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[GetRelationalDatabaseBlueprintsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Paginator.GetRelationalDatabaseBlueprints.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getrelationaldatabaseblueprintspaginator)
        """


class GetRelationalDatabaseBundlesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Paginator.GetRelationalDatabaseBundles)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getrelationaldatabasebundlespaginator)
    """

    def paginate(
        self, *, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[GetRelationalDatabaseBundlesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Paginator.GetRelationalDatabaseBundles.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getrelationaldatabasebundlespaginator)
        """


class GetRelationalDatabaseEventsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Paginator.GetRelationalDatabaseEvents)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getrelationaldatabaseeventspaginator)
    """

    def paginate(
        self,
        *,
        relationalDatabaseName: str,
        durationInMinutes: int = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[GetRelationalDatabaseEventsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Paginator.GetRelationalDatabaseEvents.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getrelationaldatabaseeventspaginator)
        """


class GetRelationalDatabaseParametersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Paginator.GetRelationalDatabaseParameters)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getrelationaldatabaseparameterspaginator)
    """

    def paginate(
        self, *, relationalDatabaseName: str, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[GetRelationalDatabaseParametersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Paginator.GetRelationalDatabaseParameters.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getrelationaldatabaseparameterspaginator)
        """


class GetRelationalDatabaseSnapshotsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Paginator.GetRelationalDatabaseSnapshots)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getrelationaldatabasesnapshotspaginator)
    """

    def paginate(
        self, *, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[GetRelationalDatabaseSnapshotsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Paginator.GetRelationalDatabaseSnapshots.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getrelationaldatabasesnapshotspaginator)
        """


class GetRelationalDatabasesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Paginator.GetRelationalDatabases)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getrelationaldatabasespaginator)
    """

    def paginate(
        self, *, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[GetRelationalDatabasesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Paginator.GetRelationalDatabases.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getrelationaldatabasespaginator)
        """


class GetStaticIpsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Paginator.GetStaticIps)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getstaticipspaginator)
    """

    def paginate(
        self, *, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[GetStaticIpsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Paginator.GetStaticIps.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lightsail/paginators/#getstaticipspaginator)
        """
