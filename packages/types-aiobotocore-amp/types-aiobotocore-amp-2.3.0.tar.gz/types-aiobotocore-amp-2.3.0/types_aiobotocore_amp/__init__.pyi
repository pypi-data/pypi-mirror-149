"""
Main interface for amp service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_amp import (
        Client,
        ListRuleGroupsNamespacesPaginator,
        ListWorkspacesPaginator,
        PrometheusServiceClient,
        WorkspaceActiveWaiter,
        WorkspaceDeletedWaiter,
    )

    session = get_session()
    async with session.create_client("amp") as client:
        client: PrometheusServiceClient
        ...


    workspace_active_waiter: WorkspaceActiveWaiter = client.get_waiter("workspace_active")
    workspace_deleted_waiter: WorkspaceDeletedWaiter = client.get_waiter("workspace_deleted")

    list_rule_groups_namespaces_paginator: ListRuleGroupsNamespacesPaginator = client.get_paginator("list_rule_groups_namespaces")
    list_workspaces_paginator: ListWorkspacesPaginator = client.get_paginator("list_workspaces")
    ```
"""
from .client import PrometheusServiceClient
from .paginator import ListRuleGroupsNamespacesPaginator, ListWorkspacesPaginator
from .waiter import WorkspaceActiveWaiter, WorkspaceDeletedWaiter

Client = PrometheusServiceClient

__all__ = (
    "Client",
    "ListRuleGroupsNamespacesPaginator",
    "ListWorkspacesPaginator",
    "PrometheusServiceClient",
    "WorkspaceActiveWaiter",
    "WorkspaceDeletedWaiter",
)
