"""
Main interface for resource-groups service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_resource_groups import (
        Client,
        ListGroupResourcesPaginator,
        ListGroupsPaginator,
        ResourceGroupsClient,
        SearchResourcesPaginator,
    )

    session = get_session()
    async with session.create_client("resource-groups") as client:
        client: ResourceGroupsClient
        ...


    list_group_resources_paginator: ListGroupResourcesPaginator = client.get_paginator("list_group_resources")
    list_groups_paginator: ListGroupsPaginator = client.get_paginator("list_groups")
    search_resources_paginator: SearchResourcesPaginator = client.get_paginator("search_resources")
    ```
"""
from .client import ResourceGroupsClient
from .paginator import ListGroupResourcesPaginator, ListGroupsPaginator, SearchResourcesPaginator

Client = ResourceGroupsClient

__all__ = (
    "Client",
    "ListGroupResourcesPaginator",
    "ListGroupsPaginator",
    "ResourceGroupsClient",
    "SearchResourcesPaginator",
)
