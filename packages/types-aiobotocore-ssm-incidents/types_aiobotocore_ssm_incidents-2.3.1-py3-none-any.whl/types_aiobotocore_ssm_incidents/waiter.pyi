"""
Type annotations for ssm-incidents service client waiters.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/waiters/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_ssm_incidents.client import SSMIncidentsClient
    from types_aiobotocore_ssm_incidents.waiter import (
        WaitForReplicationSetActiveWaiter,
        WaitForReplicationSetDeletedWaiter,
    )

    session = get_session()
    async with session.create_client("ssm-incidents") as client:
        client: SSMIncidentsClient

        wait_for_replication_set_active_waiter: WaitForReplicationSetActiveWaiter = client.get_waiter("wait_for_replication_set_active")
        wait_for_replication_set_deleted_waiter: WaitForReplicationSetDeletedWaiter = client.get_waiter("wait_for_replication_set_deleted")
    ```
"""
from aiobotocore.waiter import AIOWaiter

from .type_defs import WaiterConfigTypeDef

__all__ = ("WaitForReplicationSetActiveWaiter", "WaitForReplicationSetDeletedWaiter")

class WaitForReplicationSetActiveWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents.html#SSMIncidents.Waiter.WaitForReplicationSetActive)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/waiters/#waitforreplicationsetactivewaiter)
    """

    async def wait(self, *, arn: str, WaiterConfig: "WaiterConfigTypeDef" = ...) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents.html#SSMIncidents.Waiter.WaitForReplicationSetActive.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/waiters/#waitforreplicationsetactivewaiter)
        """

class WaitForReplicationSetDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents.html#SSMIncidents.Waiter.WaitForReplicationSetDeleted)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/waiters/#waitforreplicationsetdeletedwaiter)
    """

    async def wait(self, *, arn: str, WaiterConfig: "WaiterConfigTypeDef" = ...) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents.html#SSMIncidents.Waiter.WaitForReplicationSetDeleted.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/waiters/#waitforreplicationsetdeletedwaiter)
        """
