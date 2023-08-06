"""
Type annotations for resource-groups service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_resource_groups.client import ResourceGroupsClient
    from types_aiobotocore_resource_groups.paginator import (
        ListGroupResourcesPaginator,
        ListGroupsPaginator,
        SearchResourcesPaginator,
    )

    session = get_session()
    with session.create_client("resource-groups") as client:
        client: ResourceGroupsClient

        list_group_resources_paginator: ListGroupResourcesPaginator = client.get_paginator("list_group_resources")
        list_groups_paginator: ListGroupsPaginator = client.get_paginator("list_groups")
        search_resources_paginator: SearchResourcesPaginator = client.get_paginator("search_resources")
    ```
"""
import sys
from typing import Generic, Iterator, Sequence, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    GroupFilterTypeDef,
    ListGroupResourcesOutputTypeDef,
    ListGroupsOutputTypeDef,
    PaginatorConfigTypeDef,
    ResourceFilterTypeDef,
    ResourceQueryTypeDef,
    SearchResourcesOutputTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import AsyncIterator
else:
    from typing_extensions import AsyncIterator


__all__ = ("ListGroupResourcesPaginator", "ListGroupsPaginator", "SearchResourcesPaginator")


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListGroupResourcesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups.html#ResourceGroups.Paginator.ListGroupResources)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/paginators/#listgroupresourcespaginator)
    """

    def paginate(
        self,
        *,
        GroupName: str = ...,
        Group: str = ...,
        Filters: Sequence["ResourceFilterTypeDef"] = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListGroupResourcesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups.html#ResourceGroups.Paginator.ListGroupResources.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/paginators/#listgroupresourcespaginator)
        """


class ListGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups.html#ResourceGroups.Paginator.ListGroups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/paginators/#listgroupspaginator)
    """

    def paginate(
        self,
        *,
        Filters: Sequence["GroupFilterTypeDef"] = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListGroupsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups.html#ResourceGroups.Paginator.ListGroups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/paginators/#listgroupspaginator)
        """


class SearchResourcesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups.html#ResourceGroups.Paginator.SearchResources)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/paginators/#searchresourcespaginator)
    """

    def paginate(
        self,
        *,
        ResourceQuery: "ResourceQueryTypeDef",
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[SearchResourcesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups.html#ResourceGroups.Paginator.SearchResources.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/paginators/#searchresourcespaginator)
        """
