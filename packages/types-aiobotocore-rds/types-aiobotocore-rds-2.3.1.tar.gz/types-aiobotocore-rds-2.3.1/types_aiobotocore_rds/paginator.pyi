"""
Type annotations for rds service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_rds.client import RDSClient
    from types_aiobotocore_rds.paginator import (
        DescribeCertificatesPaginator,
        DescribeCustomAvailabilityZonesPaginator,
        DescribeDBClusterBacktracksPaginator,
        DescribeDBClusterEndpointsPaginator,
        DescribeDBClusterParameterGroupsPaginator,
        DescribeDBClusterParametersPaginator,
        DescribeDBClusterSnapshotsPaginator,
        DescribeDBClustersPaginator,
        DescribeDBEngineVersionsPaginator,
        DescribeDBInstanceAutomatedBackupsPaginator,
        DescribeDBInstancesPaginator,
        DescribeDBLogFilesPaginator,
        DescribeDBParameterGroupsPaginator,
        DescribeDBParametersPaginator,
        DescribeDBProxiesPaginator,
        DescribeDBProxyEndpointsPaginator,
        DescribeDBProxyTargetGroupsPaginator,
        DescribeDBProxyTargetsPaginator,
        DescribeDBSecurityGroupsPaginator,
        DescribeDBSnapshotsPaginator,
        DescribeDBSubnetGroupsPaginator,
        DescribeEngineDefaultClusterParametersPaginator,
        DescribeEngineDefaultParametersPaginator,
        DescribeEventSubscriptionsPaginator,
        DescribeEventsPaginator,
        DescribeExportTasksPaginator,
        DescribeGlobalClustersPaginator,
        DescribeInstallationMediaPaginator,
        DescribeOptionGroupOptionsPaginator,
        DescribeOptionGroupsPaginator,
        DescribeOrderableDBInstanceOptionsPaginator,
        DescribePendingMaintenanceActionsPaginator,
        DescribeReservedDBInstancesPaginator,
        DescribeReservedDBInstancesOfferingsPaginator,
        DescribeSourceRegionsPaginator,
        DownloadDBLogFilePortionPaginator,
    )

    session = get_session()
    with session.create_client("rds") as client:
        client: RDSClient

        describe_certificates_paginator: DescribeCertificatesPaginator = client.get_paginator("describe_certificates")
        describe_custom_availability_zones_paginator: DescribeCustomAvailabilityZonesPaginator = client.get_paginator("describe_custom_availability_zones")
        describe_db_cluster_backtracks_paginator: DescribeDBClusterBacktracksPaginator = client.get_paginator("describe_db_cluster_backtracks")
        describe_db_cluster_endpoints_paginator: DescribeDBClusterEndpointsPaginator = client.get_paginator("describe_db_cluster_endpoints")
        describe_db_cluster_parameter_groups_paginator: DescribeDBClusterParameterGroupsPaginator = client.get_paginator("describe_db_cluster_parameter_groups")
        describe_db_cluster_parameters_paginator: DescribeDBClusterParametersPaginator = client.get_paginator("describe_db_cluster_parameters")
        describe_db_cluster_snapshots_paginator: DescribeDBClusterSnapshotsPaginator = client.get_paginator("describe_db_cluster_snapshots")
        describe_db_clusters_paginator: DescribeDBClustersPaginator = client.get_paginator("describe_db_clusters")
        describe_db_engine_versions_paginator: DescribeDBEngineVersionsPaginator = client.get_paginator("describe_db_engine_versions")
        describe_db_instance_automated_backups_paginator: DescribeDBInstanceAutomatedBackupsPaginator = client.get_paginator("describe_db_instance_automated_backups")
        describe_db_instances_paginator: DescribeDBInstancesPaginator = client.get_paginator("describe_db_instances")
        describe_db_log_files_paginator: DescribeDBLogFilesPaginator = client.get_paginator("describe_db_log_files")
        describe_db_parameter_groups_paginator: DescribeDBParameterGroupsPaginator = client.get_paginator("describe_db_parameter_groups")
        describe_db_parameters_paginator: DescribeDBParametersPaginator = client.get_paginator("describe_db_parameters")
        describe_db_proxies_paginator: DescribeDBProxiesPaginator = client.get_paginator("describe_db_proxies")
        describe_db_proxy_endpoints_paginator: DescribeDBProxyEndpointsPaginator = client.get_paginator("describe_db_proxy_endpoints")
        describe_db_proxy_target_groups_paginator: DescribeDBProxyTargetGroupsPaginator = client.get_paginator("describe_db_proxy_target_groups")
        describe_db_proxy_targets_paginator: DescribeDBProxyTargetsPaginator = client.get_paginator("describe_db_proxy_targets")
        describe_db_security_groups_paginator: DescribeDBSecurityGroupsPaginator = client.get_paginator("describe_db_security_groups")
        describe_db_snapshots_paginator: DescribeDBSnapshotsPaginator = client.get_paginator("describe_db_snapshots")
        describe_db_subnet_groups_paginator: DescribeDBSubnetGroupsPaginator = client.get_paginator("describe_db_subnet_groups")
        describe_engine_default_cluster_parameters_paginator: DescribeEngineDefaultClusterParametersPaginator = client.get_paginator("describe_engine_default_cluster_parameters")
        describe_engine_default_parameters_paginator: DescribeEngineDefaultParametersPaginator = client.get_paginator("describe_engine_default_parameters")
        describe_event_subscriptions_paginator: DescribeEventSubscriptionsPaginator = client.get_paginator("describe_event_subscriptions")
        describe_events_paginator: DescribeEventsPaginator = client.get_paginator("describe_events")
        describe_export_tasks_paginator: DescribeExportTasksPaginator = client.get_paginator("describe_export_tasks")
        describe_global_clusters_paginator: DescribeGlobalClustersPaginator = client.get_paginator("describe_global_clusters")
        describe_installation_media_paginator: DescribeInstallationMediaPaginator = client.get_paginator("describe_installation_media")
        describe_option_group_options_paginator: DescribeOptionGroupOptionsPaginator = client.get_paginator("describe_option_group_options")
        describe_option_groups_paginator: DescribeOptionGroupsPaginator = client.get_paginator("describe_option_groups")
        describe_orderable_db_instance_options_paginator: DescribeOrderableDBInstanceOptionsPaginator = client.get_paginator("describe_orderable_db_instance_options")
        describe_pending_maintenance_actions_paginator: DescribePendingMaintenanceActionsPaginator = client.get_paginator("describe_pending_maintenance_actions")
        describe_reserved_db_instances_paginator: DescribeReservedDBInstancesPaginator = client.get_paginator("describe_reserved_db_instances")
        describe_reserved_db_instances_offerings_paginator: DescribeReservedDBInstancesOfferingsPaginator = client.get_paginator("describe_reserved_db_instances_offerings")
        describe_source_regions_paginator: DescribeSourceRegionsPaginator = client.get_paginator("describe_source_regions")
        download_db_log_file_portion_paginator: DownloadDBLogFilePortionPaginator = client.get_paginator("download_db_log_file_portion")
    ```
"""
import sys
from datetime import datetime
from typing import Generic, Iterator, Sequence, TypeVar, Union

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .literals import SourceTypeType
from .type_defs import (
    CertificateMessageTypeDef,
    CustomAvailabilityZoneMessageTypeDef,
    DBClusterBacktrackMessageTypeDef,
    DBClusterEndpointMessageTypeDef,
    DBClusterMessageTypeDef,
    DBClusterParameterGroupDetailsTypeDef,
    DBClusterParameterGroupsMessageTypeDef,
    DBClusterSnapshotMessageTypeDef,
    DBEngineVersionMessageTypeDef,
    DBInstanceAutomatedBackupMessageTypeDef,
    DBInstanceMessageTypeDef,
    DBParameterGroupDetailsTypeDef,
    DBParameterGroupsMessageTypeDef,
    DBSecurityGroupMessageTypeDef,
    DBSnapshotMessageTypeDef,
    DBSubnetGroupMessageTypeDef,
    DescribeDBLogFilesResponseTypeDef,
    DescribeDBProxiesResponseTypeDef,
    DescribeDBProxyEndpointsResponseTypeDef,
    DescribeDBProxyTargetGroupsResponseTypeDef,
    DescribeDBProxyTargetsResponseTypeDef,
    DescribeEngineDefaultClusterParametersResultTypeDef,
    DescribeEngineDefaultParametersResultTypeDef,
    DownloadDBLogFilePortionDetailsTypeDef,
    EventsMessageTypeDef,
    EventSubscriptionsMessageTypeDef,
    ExportTasksMessageTypeDef,
    FilterTypeDef,
    GlobalClustersMessageTypeDef,
    InstallationMediaMessageTypeDef,
    OptionGroupOptionsMessageTypeDef,
    OptionGroupsTypeDef,
    OrderableDBInstanceOptionsMessageTypeDef,
    PaginatorConfigTypeDef,
    PendingMaintenanceActionsMessageTypeDef,
    ReservedDBInstanceMessageTypeDef,
    ReservedDBInstancesOfferingMessageTypeDef,
    SourceRegionMessageTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import AsyncIterator
else:
    from typing_extensions import AsyncIterator

__all__ = (
    "DescribeCertificatesPaginator",
    "DescribeCustomAvailabilityZonesPaginator",
    "DescribeDBClusterBacktracksPaginator",
    "DescribeDBClusterEndpointsPaginator",
    "DescribeDBClusterParameterGroupsPaginator",
    "DescribeDBClusterParametersPaginator",
    "DescribeDBClusterSnapshotsPaginator",
    "DescribeDBClustersPaginator",
    "DescribeDBEngineVersionsPaginator",
    "DescribeDBInstanceAutomatedBackupsPaginator",
    "DescribeDBInstancesPaginator",
    "DescribeDBLogFilesPaginator",
    "DescribeDBParameterGroupsPaginator",
    "DescribeDBParametersPaginator",
    "DescribeDBProxiesPaginator",
    "DescribeDBProxyEndpointsPaginator",
    "DescribeDBProxyTargetGroupsPaginator",
    "DescribeDBProxyTargetsPaginator",
    "DescribeDBSecurityGroupsPaginator",
    "DescribeDBSnapshotsPaginator",
    "DescribeDBSubnetGroupsPaginator",
    "DescribeEngineDefaultClusterParametersPaginator",
    "DescribeEngineDefaultParametersPaginator",
    "DescribeEventSubscriptionsPaginator",
    "DescribeEventsPaginator",
    "DescribeExportTasksPaginator",
    "DescribeGlobalClustersPaginator",
    "DescribeInstallationMediaPaginator",
    "DescribeOptionGroupOptionsPaginator",
    "DescribeOptionGroupsPaginator",
    "DescribeOrderableDBInstanceOptionsPaginator",
    "DescribePendingMaintenanceActionsPaginator",
    "DescribeReservedDBInstancesPaginator",
    "DescribeReservedDBInstancesOfferingsPaginator",
    "DescribeSourceRegionsPaginator",
    "DownloadDBLogFilePortionPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class DescribeCertificatesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Paginator.DescribeCertificates)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describecertificatespaginator)
    """

    def paginate(
        self,
        *,
        CertificateIdentifier: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[CertificateMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Paginator.DescribeCertificates.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describecertificatespaginator)
        """

class DescribeCustomAvailabilityZonesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Paginator.DescribeCustomAvailabilityZones)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describecustomavailabilityzonespaginator)
    """

    def paginate(
        self,
        *,
        CustomAvailabilityZoneId: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[CustomAvailabilityZoneMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Paginator.DescribeCustomAvailabilityZones.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describecustomavailabilityzonespaginator)
        """

class DescribeDBClusterBacktracksPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Paginator.DescribeDBClusterBacktracks)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbclusterbacktrackspaginator)
    """

    def paginate(
        self,
        *,
        DBClusterIdentifier: str,
        BacktrackIdentifier: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DBClusterBacktrackMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Paginator.DescribeDBClusterBacktracks.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbclusterbacktrackspaginator)
        """

class DescribeDBClusterEndpointsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Paginator.DescribeDBClusterEndpoints)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbclusterendpointspaginator)
    """

    def paginate(
        self,
        *,
        DBClusterIdentifier: str = ...,
        DBClusterEndpointIdentifier: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DBClusterEndpointMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Paginator.DescribeDBClusterEndpoints.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbclusterendpointspaginator)
        """

class DescribeDBClusterParameterGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Paginator.DescribeDBClusterParameterGroups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbclusterparametergroupspaginator)
    """

    def paginate(
        self,
        *,
        DBClusterParameterGroupName: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DBClusterParameterGroupsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Paginator.DescribeDBClusterParameterGroups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbclusterparametergroupspaginator)
        """

class DescribeDBClusterParametersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Paginator.DescribeDBClusterParameters)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbclusterparameterspaginator)
    """

    def paginate(
        self,
        *,
        DBClusterParameterGroupName: str,
        Source: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DBClusterParameterGroupDetailsTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Paginator.DescribeDBClusterParameters.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbclusterparameterspaginator)
        """

class DescribeDBClusterSnapshotsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Paginator.DescribeDBClusterSnapshots)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbclustersnapshotspaginator)
    """

    def paginate(
        self,
        *,
        DBClusterIdentifier: str = ...,
        DBClusterSnapshotIdentifier: str = ...,
        SnapshotType: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        IncludeShared: bool = ...,
        IncludePublic: bool = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DBClusterSnapshotMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Paginator.DescribeDBClusterSnapshots.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbclustersnapshotspaginator)
        """

class DescribeDBClustersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Paginator.DescribeDBClusters)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbclusterspaginator)
    """

    def paginate(
        self,
        *,
        DBClusterIdentifier: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        IncludeShared: bool = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DBClusterMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Paginator.DescribeDBClusters.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbclusterspaginator)
        """

class DescribeDBEngineVersionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Paginator.DescribeDBEngineVersions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbengineversionspaginator)
    """

    def paginate(
        self,
        *,
        Engine: str = ...,
        EngineVersion: str = ...,
        DBParameterGroupFamily: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        DefaultOnly: bool = ...,
        ListSupportedCharacterSets: bool = ...,
        ListSupportedTimezones: bool = ...,
        IncludeAll: bool = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DBEngineVersionMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Paginator.DescribeDBEngineVersions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbengineversionspaginator)
        """

class DescribeDBInstanceAutomatedBackupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Paginator.DescribeDBInstanceAutomatedBackups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbinstanceautomatedbackupspaginator)
    """

    def paginate(
        self,
        *,
        DbiResourceId: str = ...,
        DBInstanceIdentifier: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        DBInstanceAutomatedBackupsArn: str = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DBInstanceAutomatedBackupMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Paginator.DescribeDBInstanceAutomatedBackups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbinstanceautomatedbackupspaginator)
        """

class DescribeDBInstancesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Paginator.DescribeDBInstances)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbinstancespaginator)
    """

    def paginate(
        self,
        *,
        DBInstanceIdentifier: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DBInstanceMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Paginator.DescribeDBInstances.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbinstancespaginator)
        """

class DescribeDBLogFilesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Paginator.DescribeDBLogFiles)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedblogfilespaginator)
    """

    def paginate(
        self,
        *,
        DBInstanceIdentifier: str,
        FilenameContains: str = ...,
        FileLastWritten: int = ...,
        FileSize: int = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DescribeDBLogFilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Paginator.DescribeDBLogFiles.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedblogfilespaginator)
        """

class DescribeDBParameterGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Paginator.DescribeDBParameterGroups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbparametergroupspaginator)
    """

    def paginate(
        self,
        *,
        DBParameterGroupName: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DBParameterGroupsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Paginator.DescribeDBParameterGroups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbparametergroupspaginator)
        """

class DescribeDBParametersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Paginator.DescribeDBParameters)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbparameterspaginator)
    """

    def paginate(
        self,
        *,
        DBParameterGroupName: str,
        Source: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DBParameterGroupDetailsTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Paginator.DescribeDBParameters.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbparameterspaginator)
        """

class DescribeDBProxiesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Paginator.DescribeDBProxies)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbproxiespaginator)
    """

    def paginate(
        self,
        *,
        DBProxyName: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DescribeDBProxiesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Paginator.DescribeDBProxies.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbproxiespaginator)
        """

class DescribeDBProxyEndpointsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Paginator.DescribeDBProxyEndpoints)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbproxyendpointspaginator)
    """

    def paginate(
        self,
        *,
        DBProxyName: str = ...,
        DBProxyEndpointName: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DescribeDBProxyEndpointsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Paginator.DescribeDBProxyEndpoints.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbproxyendpointspaginator)
        """

class DescribeDBProxyTargetGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Paginator.DescribeDBProxyTargetGroups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbproxytargetgroupspaginator)
    """

    def paginate(
        self,
        *,
        DBProxyName: str,
        TargetGroupName: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DescribeDBProxyTargetGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Paginator.DescribeDBProxyTargetGroups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbproxytargetgroupspaginator)
        """

class DescribeDBProxyTargetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Paginator.DescribeDBProxyTargets)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbproxytargetspaginator)
    """

    def paginate(
        self,
        *,
        DBProxyName: str,
        TargetGroupName: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DescribeDBProxyTargetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Paginator.DescribeDBProxyTargets.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbproxytargetspaginator)
        """

class DescribeDBSecurityGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Paginator.DescribeDBSecurityGroups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbsecuritygroupspaginator)
    """

    def paginate(
        self,
        *,
        DBSecurityGroupName: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DBSecurityGroupMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Paginator.DescribeDBSecurityGroups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbsecuritygroupspaginator)
        """

class DescribeDBSnapshotsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Paginator.DescribeDBSnapshots)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbsnapshotspaginator)
    """

    def paginate(
        self,
        *,
        DBInstanceIdentifier: str = ...,
        DBSnapshotIdentifier: str = ...,
        SnapshotType: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        IncludeShared: bool = ...,
        IncludePublic: bool = ...,
        DbiResourceId: str = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DBSnapshotMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Paginator.DescribeDBSnapshots.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbsnapshotspaginator)
        """

class DescribeDBSubnetGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Paginator.DescribeDBSubnetGroups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbsubnetgroupspaginator)
    """

    def paginate(
        self,
        *,
        DBSubnetGroupName: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DBSubnetGroupMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Paginator.DescribeDBSubnetGroups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describedbsubnetgroupspaginator)
        """

class DescribeEngineDefaultClusterParametersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Paginator.DescribeEngineDefaultClusterParameters)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describeenginedefaultclusterparameterspaginator)
    """

    def paginate(
        self,
        *,
        DBParameterGroupFamily: str,
        Filters: Sequence["FilterTypeDef"] = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DescribeEngineDefaultClusterParametersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Paginator.DescribeEngineDefaultClusterParameters.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describeenginedefaultclusterparameterspaginator)
        """

class DescribeEngineDefaultParametersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Paginator.DescribeEngineDefaultParameters)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describeenginedefaultparameterspaginator)
    """

    def paginate(
        self,
        *,
        DBParameterGroupFamily: str,
        Filters: Sequence["FilterTypeDef"] = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DescribeEngineDefaultParametersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Paginator.DescribeEngineDefaultParameters.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describeenginedefaultparameterspaginator)
        """

class DescribeEventSubscriptionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Paginator.DescribeEventSubscriptions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describeeventsubscriptionspaginator)
    """

    def paginate(
        self,
        *,
        SubscriptionName: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[EventSubscriptionsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Paginator.DescribeEventSubscriptions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describeeventsubscriptionspaginator)
        """

class DescribeEventsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Paginator.DescribeEvents)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describeeventspaginator)
    """

    def paginate(
        self,
        *,
        SourceIdentifier: str = ...,
        SourceType: SourceTypeType = ...,
        StartTime: Union[datetime, str] = ...,
        EndTime: Union[datetime, str] = ...,
        Duration: int = ...,
        EventCategories: Sequence[str] = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[EventsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Paginator.DescribeEvents.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describeeventspaginator)
        """

class DescribeExportTasksPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Paginator.DescribeExportTasks)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describeexporttaskspaginator)
    """

    def paginate(
        self,
        *,
        ExportTaskIdentifier: str = ...,
        SourceArn: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ExportTasksMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Paginator.DescribeExportTasks.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describeexporttaskspaginator)
        """

class DescribeGlobalClustersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Paginator.DescribeGlobalClusters)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describeglobalclusterspaginator)
    """

    def paginate(
        self,
        *,
        GlobalClusterIdentifier: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[GlobalClustersMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Paginator.DescribeGlobalClusters.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describeglobalclusterspaginator)
        """

class DescribeInstallationMediaPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Paginator.DescribeInstallationMedia)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describeinstallationmediapaginator)
    """

    def paginate(
        self,
        *,
        InstallationMediaId: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[InstallationMediaMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Paginator.DescribeInstallationMedia.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describeinstallationmediapaginator)
        """

class DescribeOptionGroupOptionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Paginator.DescribeOptionGroupOptions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describeoptiongroupoptionspaginator)
    """

    def paginate(
        self,
        *,
        EngineName: str,
        MajorEngineVersion: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[OptionGroupOptionsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Paginator.DescribeOptionGroupOptions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describeoptiongroupoptionspaginator)
        """

class DescribeOptionGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Paginator.DescribeOptionGroups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describeoptiongroupspaginator)
    """

    def paginate(
        self,
        *,
        OptionGroupName: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        EngineName: str = ...,
        MajorEngineVersion: str = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[OptionGroupsTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Paginator.DescribeOptionGroups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describeoptiongroupspaginator)
        """

class DescribeOrderableDBInstanceOptionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Paginator.DescribeOrderableDBInstanceOptions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describeorderabledbinstanceoptionspaginator)
    """

    def paginate(
        self,
        *,
        Engine: str,
        EngineVersion: str = ...,
        DBInstanceClass: str = ...,
        LicenseModel: str = ...,
        AvailabilityZoneGroup: str = ...,
        Vpc: bool = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[OrderableDBInstanceOptionsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Paginator.DescribeOrderableDBInstanceOptions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describeorderabledbinstanceoptionspaginator)
        """

class DescribePendingMaintenanceActionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Paginator.DescribePendingMaintenanceActions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describependingmaintenanceactionspaginator)
    """

    def paginate(
        self,
        *,
        ResourceIdentifier: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[PendingMaintenanceActionsMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Paginator.DescribePendingMaintenanceActions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describependingmaintenanceactionspaginator)
        """

class DescribeReservedDBInstancesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Paginator.DescribeReservedDBInstances)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describereserveddbinstancespaginator)
    """

    def paginate(
        self,
        *,
        ReservedDBInstanceId: str = ...,
        ReservedDBInstancesOfferingId: str = ...,
        DBInstanceClass: str = ...,
        Duration: str = ...,
        ProductDescription: str = ...,
        OfferingType: str = ...,
        MultiAZ: bool = ...,
        LeaseId: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ReservedDBInstanceMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Paginator.DescribeReservedDBInstances.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describereserveddbinstancespaginator)
        """

class DescribeReservedDBInstancesOfferingsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Paginator.DescribeReservedDBInstancesOfferings)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describereserveddbinstancesofferingspaginator)
    """

    def paginate(
        self,
        *,
        ReservedDBInstancesOfferingId: str = ...,
        DBInstanceClass: str = ...,
        Duration: str = ...,
        ProductDescription: str = ...,
        OfferingType: str = ...,
        MultiAZ: bool = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ReservedDBInstancesOfferingMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Paginator.DescribeReservedDBInstancesOfferings.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describereserveddbinstancesofferingspaginator)
        """

class DescribeSourceRegionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Paginator.DescribeSourceRegions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describesourceregionspaginator)
    """

    def paginate(
        self,
        *,
        RegionName: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[SourceRegionMessageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Paginator.DescribeSourceRegions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#describesourceregionspaginator)
        """

class DownloadDBLogFilePortionPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Paginator.DownloadDBLogFilePortion)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#downloaddblogfileportionpaginator)
    """

    def paginate(
        self,
        *,
        DBInstanceIdentifier: str,
        LogFileName: str,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DownloadDBLogFilePortionDetailsTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Paginator.DownloadDBLogFilePortion.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/paginators/#downloaddblogfileportionpaginator)
        """
