"""
Main interface for cloudtrail service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_cloudtrail import (
        Client,
        CloudTrailClient,
        ListPublicKeysPaginator,
        ListTagsPaginator,
        ListTrailsPaginator,
        LookupEventsPaginator,
    )

    session = get_session()
    async with session.create_client("cloudtrail") as client:
        client: CloudTrailClient
        ...


    list_public_keys_paginator: ListPublicKeysPaginator = client.get_paginator("list_public_keys")
    list_tags_paginator: ListTagsPaginator = client.get_paginator("list_tags")
    list_trails_paginator: ListTrailsPaginator = client.get_paginator("list_trails")
    lookup_events_paginator: LookupEventsPaginator = client.get_paginator("lookup_events")
    ```
"""
from .client import CloudTrailClient
from .paginator import (
    ListPublicKeysPaginator,
    ListTagsPaginator,
    ListTrailsPaginator,
    LookupEventsPaginator,
)

Client = CloudTrailClient


__all__ = (
    "Client",
    "CloudTrailClient",
    "ListPublicKeysPaginator",
    "ListTagsPaginator",
    "ListTrailsPaginator",
    "LookupEventsPaginator",
)
