"""
Main interface for grafana service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_grafana import (
        Client,
        ListPermissionsPaginator,
        ListWorkspacesPaginator,
        ManagedGrafanaClient,
    )

    session = get_session()
    async with session.create_client("grafana") as client:
        client: ManagedGrafanaClient
        ...


    list_permissions_paginator: ListPermissionsPaginator = client.get_paginator("list_permissions")
    list_workspaces_paginator: ListWorkspacesPaginator = client.get_paginator("list_workspaces")
    ```
"""
from .client import ManagedGrafanaClient
from .paginator import ListPermissionsPaginator, ListWorkspacesPaginator

Client = ManagedGrafanaClient


__all__ = ("Client", "ListPermissionsPaginator", "ListWorkspacesPaginator", "ManagedGrafanaClient")
