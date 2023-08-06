"""
Main interface for kinesisanalyticsv2 service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_kinesisanalyticsv2 import (
        Client,
        KinesisAnalyticsV2Client,
        ListApplicationSnapshotsPaginator,
        ListApplicationsPaginator,
    )

    session = get_session()
    async with session.create_client("kinesisanalyticsv2") as client:
        client: KinesisAnalyticsV2Client
        ...


    list_application_snapshots_paginator: ListApplicationSnapshotsPaginator = client.get_paginator("list_application_snapshots")
    list_applications_paginator: ListApplicationsPaginator = client.get_paginator("list_applications")
    ```
"""
from .client import KinesisAnalyticsV2Client
from .paginator import ListApplicationSnapshotsPaginator, ListApplicationsPaginator

Client = KinesisAnalyticsV2Client

__all__ = (
    "Client",
    "KinesisAnalyticsV2Client",
    "ListApplicationSnapshotsPaginator",
    "ListApplicationsPaginator",
)
