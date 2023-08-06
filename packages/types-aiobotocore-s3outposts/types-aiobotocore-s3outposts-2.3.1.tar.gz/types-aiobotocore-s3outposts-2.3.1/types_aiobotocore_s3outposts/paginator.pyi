"""
Type annotations for s3outposts service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3outposts/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_s3outposts.client import S3OutpostsClient
    from types_aiobotocore_s3outposts.paginator import (
        ListEndpointsPaginator,
        ListSharedEndpointsPaginator,
    )

    session = get_session()
    with session.create_client("s3outposts") as client:
        client: S3OutpostsClient

        list_endpoints_paginator: ListEndpointsPaginator = client.get_paginator("list_endpoints")
        list_shared_endpoints_paginator: ListSharedEndpointsPaginator = client.get_paginator("list_shared_endpoints")
    ```
"""
import sys
from typing import Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListEndpointsResultTypeDef,
    ListSharedEndpointsResultTypeDef,
    PaginatorConfigTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import AsyncIterator
else:
    from typing_extensions import AsyncIterator

__all__ = ("ListEndpointsPaginator", "ListSharedEndpointsPaginator")

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListEndpointsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3outposts.html#S3Outposts.Paginator.ListEndpoints)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3outposts/paginators/#listendpointspaginator)
    """

    def paginate(
        self, *, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListEndpointsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3outposts.html#S3Outposts.Paginator.ListEndpoints.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3outposts/paginators/#listendpointspaginator)
        """

class ListSharedEndpointsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3outposts.html#S3Outposts.Paginator.ListSharedEndpoints)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3outposts/paginators/#listsharedendpointspaginator)
    """

    def paginate(
        self, *, OutpostId: str, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListSharedEndpointsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3outposts.html#S3Outposts.Paginator.ListSharedEndpoints.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3outposts/paginators/#listsharedendpointspaginator)
        """
