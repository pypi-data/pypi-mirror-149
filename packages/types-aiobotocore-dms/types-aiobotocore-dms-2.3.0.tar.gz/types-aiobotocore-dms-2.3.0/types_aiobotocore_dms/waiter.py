"""
Type annotations for dms service client waiters.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/waiters/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_dms.client import DatabaseMigrationServiceClient
    from types_aiobotocore_dms.waiter import (
        EndpointDeletedWaiter,
        ReplicationInstanceAvailableWaiter,
        ReplicationInstanceDeletedWaiter,
        ReplicationTaskDeletedWaiter,
        ReplicationTaskReadyWaiter,
        ReplicationTaskRunningWaiter,
        ReplicationTaskStoppedWaiter,
        TestConnectionSucceedsWaiter,
    )

    session = get_session()
    async with session.create_client("dms") as client:
        client: DatabaseMigrationServiceClient

        endpoint_deleted_waiter: EndpointDeletedWaiter = client.get_waiter("endpoint_deleted")
        replication_instance_available_waiter: ReplicationInstanceAvailableWaiter = client.get_waiter("replication_instance_available")
        replication_instance_deleted_waiter: ReplicationInstanceDeletedWaiter = client.get_waiter("replication_instance_deleted")
        replication_task_deleted_waiter: ReplicationTaskDeletedWaiter = client.get_waiter("replication_task_deleted")
        replication_task_ready_waiter: ReplicationTaskReadyWaiter = client.get_waiter("replication_task_ready")
        replication_task_running_waiter: ReplicationTaskRunningWaiter = client.get_waiter("replication_task_running")
        replication_task_stopped_waiter: ReplicationTaskStoppedWaiter = client.get_waiter("replication_task_stopped")
        test_connection_succeeds_waiter: TestConnectionSucceedsWaiter = client.get_waiter("test_connection_succeeds")
    ```
"""
from typing import Sequence

from aiobotocore.waiter import AIOWaiter

from .type_defs import FilterTypeDef, WaiterConfigTypeDef

__all__ = (
    "EndpointDeletedWaiter",
    "ReplicationInstanceAvailableWaiter",
    "ReplicationInstanceDeletedWaiter",
    "ReplicationTaskDeletedWaiter",
    "ReplicationTaskReadyWaiter",
    "ReplicationTaskRunningWaiter",
    "ReplicationTaskStoppedWaiter",
    "TestConnectionSucceedsWaiter",
)


class EndpointDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Waiter.EndpointDeleted)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/waiters/#endpointdeletedwaiter)
    """

    async def wait(
        self,
        *,
        Filters: Sequence["FilterTypeDef"] = ...,
        MaxRecords: int = ...,
        Marker: str = ...,
        WaiterConfig: "WaiterConfigTypeDef" = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Waiter.EndpointDeleted.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/waiters/#endpointdeletedwaiter)
        """


class ReplicationInstanceAvailableWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Waiter.ReplicationInstanceAvailable)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/waiters/#replicationinstanceavailablewaiter)
    """

    async def wait(
        self,
        *,
        Filters: Sequence["FilterTypeDef"] = ...,
        MaxRecords: int = ...,
        Marker: str = ...,
        WaiterConfig: "WaiterConfigTypeDef" = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Waiter.ReplicationInstanceAvailable.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/waiters/#replicationinstanceavailablewaiter)
        """


class ReplicationInstanceDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Waiter.ReplicationInstanceDeleted)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/waiters/#replicationinstancedeletedwaiter)
    """

    async def wait(
        self,
        *,
        Filters: Sequence["FilterTypeDef"] = ...,
        MaxRecords: int = ...,
        Marker: str = ...,
        WaiterConfig: "WaiterConfigTypeDef" = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Waiter.ReplicationInstanceDeleted.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/waiters/#replicationinstancedeletedwaiter)
        """


class ReplicationTaskDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Waiter.ReplicationTaskDeleted)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/waiters/#replicationtaskdeletedwaiter)
    """

    async def wait(
        self,
        *,
        Filters: Sequence["FilterTypeDef"] = ...,
        MaxRecords: int = ...,
        Marker: str = ...,
        WithoutSettings: bool = ...,
        WaiterConfig: "WaiterConfigTypeDef" = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Waiter.ReplicationTaskDeleted.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/waiters/#replicationtaskdeletedwaiter)
        """


class ReplicationTaskReadyWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Waiter.ReplicationTaskReady)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/waiters/#replicationtaskreadywaiter)
    """

    async def wait(
        self,
        *,
        Filters: Sequence["FilterTypeDef"] = ...,
        MaxRecords: int = ...,
        Marker: str = ...,
        WithoutSettings: bool = ...,
        WaiterConfig: "WaiterConfigTypeDef" = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Waiter.ReplicationTaskReady.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/waiters/#replicationtaskreadywaiter)
        """


class ReplicationTaskRunningWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Waiter.ReplicationTaskRunning)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/waiters/#replicationtaskrunningwaiter)
    """

    async def wait(
        self,
        *,
        Filters: Sequence["FilterTypeDef"] = ...,
        MaxRecords: int = ...,
        Marker: str = ...,
        WithoutSettings: bool = ...,
        WaiterConfig: "WaiterConfigTypeDef" = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Waiter.ReplicationTaskRunning.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/waiters/#replicationtaskrunningwaiter)
        """


class ReplicationTaskStoppedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Waiter.ReplicationTaskStopped)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/waiters/#replicationtaskstoppedwaiter)
    """

    async def wait(
        self,
        *,
        Filters: Sequence["FilterTypeDef"] = ...,
        MaxRecords: int = ...,
        Marker: str = ...,
        WithoutSettings: bool = ...,
        WaiterConfig: "WaiterConfigTypeDef" = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Waiter.ReplicationTaskStopped.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/waiters/#replicationtaskstoppedwaiter)
        """


class TestConnectionSucceedsWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Waiter.TestConnectionSucceeds)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/waiters/#testconnectionsucceedswaiter)
    """

    async def wait(
        self,
        *,
        Filters: Sequence["FilterTypeDef"] = ...,
        MaxRecords: int = ...,
        Marker: str = ...,
        WaiterConfig: "WaiterConfigTypeDef" = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dms.html#DatabaseMigrationService.Waiter.TestConnectionSucceeds.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dms/waiters/#testconnectionsucceedswaiter)
        """
