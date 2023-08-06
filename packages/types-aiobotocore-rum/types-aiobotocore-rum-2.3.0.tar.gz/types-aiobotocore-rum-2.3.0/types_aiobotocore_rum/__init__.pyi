"""
Main interface for rum service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_rum import (
        Client,
        CloudWatchRUMClient,
        GetAppMonitorDataPaginator,
        ListAppMonitorsPaginator,
    )

    session = get_session()
    async with session.create_client("rum") as client:
        client: CloudWatchRUMClient
        ...


    get_app_monitor_data_paginator: GetAppMonitorDataPaginator = client.get_paginator("get_app_monitor_data")
    list_app_monitors_paginator: ListAppMonitorsPaginator = client.get_paginator("list_app_monitors")
    ```
"""
from .client import CloudWatchRUMClient
from .paginator import GetAppMonitorDataPaginator, ListAppMonitorsPaginator

Client = CloudWatchRUMClient

__all__ = (
    "Client",
    "CloudWatchRUMClient",
    "GetAppMonitorDataPaginator",
    "ListAppMonitorsPaginator",
)
