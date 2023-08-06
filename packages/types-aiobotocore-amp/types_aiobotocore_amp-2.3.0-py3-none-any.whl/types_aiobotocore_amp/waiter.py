"""
Type annotations for amp service client waiters.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amp/waiters/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_amp.client import PrometheusServiceClient
    from types_aiobotocore_amp.waiter import (
        WorkspaceActiveWaiter,
        WorkspaceDeletedWaiter,
    )

    session = get_session()
    async with session.create_client("amp") as client:
        client: PrometheusServiceClient

        workspace_active_waiter: WorkspaceActiveWaiter = client.get_waiter("workspace_active")
        workspace_deleted_waiter: WorkspaceDeletedWaiter = client.get_waiter("workspace_deleted")
    ```
"""
from aiobotocore.waiter import AIOWaiter

from .type_defs import WaiterConfigTypeDef

__all__ = ("WorkspaceActiveWaiter", "WorkspaceDeletedWaiter")


class WorkspaceActiveWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amp.html#PrometheusService.Waiter.WorkspaceActive)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amp/waiters/#workspaceactivewaiter)
    """

    async def wait(self, *, workspaceId: str, WaiterConfig: "WaiterConfigTypeDef" = ...) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amp.html#PrometheusService.Waiter.WorkspaceActive.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amp/waiters/#workspaceactivewaiter)
        """


class WorkspaceDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amp.html#PrometheusService.Waiter.WorkspaceDeleted)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amp/waiters/#workspacedeletedwaiter)
    """

    async def wait(self, *, workspaceId: str, WaiterConfig: "WaiterConfigTypeDef" = ...) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amp.html#PrometheusService.Waiter.WorkspaceDeleted.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amp/waiters/#workspacedeletedwaiter)
        """
