"""
Type annotations for rds service client waiters.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/waiters/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_rds.client import RDSClient
    from types_aiobotocore_rds.waiter import (
        DBClusterSnapshotAvailableWaiter,
        DBClusterSnapshotDeletedWaiter,
        DBInstanceAvailableWaiter,
        DBInstanceDeletedWaiter,
        DBSnapshotAvailableWaiter,
        DBSnapshotCompletedWaiter,
        DBSnapshotDeletedWaiter,
    )

    session = get_session()
    async with session.create_client("rds") as client:
        client: RDSClient

        db_cluster_snapshot_available_waiter: DBClusterSnapshotAvailableWaiter = client.get_waiter("db_cluster_snapshot_available")
        db_cluster_snapshot_deleted_waiter: DBClusterSnapshotDeletedWaiter = client.get_waiter("db_cluster_snapshot_deleted")
        db_instance_available_waiter: DBInstanceAvailableWaiter = client.get_waiter("db_instance_available")
        db_instance_deleted_waiter: DBInstanceDeletedWaiter = client.get_waiter("db_instance_deleted")
        db_snapshot_available_waiter: DBSnapshotAvailableWaiter = client.get_waiter("db_snapshot_available")
        db_snapshot_completed_waiter: DBSnapshotCompletedWaiter = client.get_waiter("db_snapshot_completed")
        db_snapshot_deleted_waiter: DBSnapshotDeletedWaiter = client.get_waiter("db_snapshot_deleted")
    ```
"""
from typing import Sequence

from aiobotocore.waiter import AIOWaiter

from .type_defs import FilterTypeDef, WaiterConfigTypeDef

__all__ = (
    "DBClusterSnapshotAvailableWaiter",
    "DBClusterSnapshotDeletedWaiter",
    "DBInstanceAvailableWaiter",
    "DBInstanceDeletedWaiter",
    "DBSnapshotAvailableWaiter",
    "DBSnapshotCompletedWaiter",
    "DBSnapshotDeletedWaiter",
)


class DBClusterSnapshotAvailableWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Waiter.DBClusterSnapshotAvailable)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/waiters/#dbclustersnapshotavailablewaiter)
    """

    async def wait(
        self,
        *,
        DBClusterIdentifier: str = ...,
        DBClusterSnapshotIdentifier: str = ...,
        SnapshotType: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        MaxRecords: int = ...,
        Marker: str = ...,
        IncludeShared: bool = ...,
        IncludePublic: bool = ...,
        WaiterConfig: "WaiterConfigTypeDef" = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Waiter.DBClusterSnapshotAvailable.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/waiters/#dbclustersnapshotavailablewaiter)
        """


class DBClusterSnapshotDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Waiter.DBClusterSnapshotDeleted)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/waiters/#dbclustersnapshotdeletedwaiter)
    """

    async def wait(
        self,
        *,
        DBClusterIdentifier: str = ...,
        DBClusterSnapshotIdentifier: str = ...,
        SnapshotType: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        MaxRecords: int = ...,
        Marker: str = ...,
        IncludeShared: bool = ...,
        IncludePublic: bool = ...,
        WaiterConfig: "WaiterConfigTypeDef" = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Waiter.DBClusterSnapshotDeleted.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/waiters/#dbclustersnapshotdeletedwaiter)
        """


class DBInstanceAvailableWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Waiter.DBInstanceAvailable)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/waiters/#dbinstanceavailablewaiter)
    """

    async def wait(
        self,
        *,
        DBInstanceIdentifier: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        MaxRecords: int = ...,
        Marker: str = ...,
        WaiterConfig: "WaiterConfigTypeDef" = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Waiter.DBInstanceAvailable.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/waiters/#dbinstanceavailablewaiter)
        """


class DBInstanceDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Waiter.DBInstanceDeleted)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/waiters/#dbinstancedeletedwaiter)
    """

    async def wait(
        self,
        *,
        DBInstanceIdentifier: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        MaxRecords: int = ...,
        Marker: str = ...,
        WaiterConfig: "WaiterConfigTypeDef" = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Waiter.DBInstanceDeleted.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/waiters/#dbinstancedeletedwaiter)
        """


class DBSnapshotAvailableWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Waiter.DBSnapshotAvailable)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/waiters/#dbsnapshotavailablewaiter)
    """

    async def wait(
        self,
        *,
        DBInstanceIdentifier: str = ...,
        DBSnapshotIdentifier: str = ...,
        SnapshotType: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        MaxRecords: int = ...,
        Marker: str = ...,
        IncludeShared: bool = ...,
        IncludePublic: bool = ...,
        DbiResourceId: str = ...,
        WaiterConfig: "WaiterConfigTypeDef" = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Waiter.DBSnapshotAvailable.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/waiters/#dbsnapshotavailablewaiter)
        """


class DBSnapshotCompletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Waiter.DBSnapshotCompleted)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/waiters/#dbsnapshotcompletedwaiter)
    """

    async def wait(
        self,
        *,
        DBInstanceIdentifier: str = ...,
        DBSnapshotIdentifier: str = ...,
        SnapshotType: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        MaxRecords: int = ...,
        Marker: str = ...,
        IncludeShared: bool = ...,
        IncludePublic: bool = ...,
        DbiResourceId: str = ...,
        WaiterConfig: "WaiterConfigTypeDef" = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Waiter.DBSnapshotCompleted.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/waiters/#dbsnapshotcompletedwaiter)
        """


class DBSnapshotDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Waiter.DBSnapshotDeleted)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/waiters/#dbsnapshotdeletedwaiter)
    """

    async def wait(
        self,
        *,
        DBInstanceIdentifier: str = ...,
        DBSnapshotIdentifier: str = ...,
        SnapshotType: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        MaxRecords: int = ...,
        Marker: str = ...,
        IncludeShared: bool = ...,
        IncludePublic: bool = ...,
        DbiResourceId: str = ...,
        WaiterConfig: "WaiterConfigTypeDef" = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Waiter.DBSnapshotDeleted.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rds/waiters/#dbsnapshotdeletedwaiter)
        """
