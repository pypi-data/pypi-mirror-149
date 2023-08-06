"""
Type annotations for s3outposts service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3outposts/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_s3outposts.client import S3OutpostsClient

    session = get_session()
    async with session.create_client("s3outposts") as client:
        client: S3OutpostsClient
    ```
"""
import sys
from typing import Any, Dict, Mapping, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import EndpointAccessTypeType
from .paginator import ListEndpointsPaginator, ListSharedEndpointsPaginator
from .type_defs import (
    CreateEndpointResultTypeDef,
    ListEndpointsResultTypeDef,
    ListSharedEndpointsResultTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("S3OutpostsClient",)

class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class S3OutpostsClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3outposts.html#S3Outposts.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3outposts/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        S3OutpostsClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3outposts.html#S3Outposts.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3outposts/client/#exceptions)
        """
    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3outposts.html#S3Outposts.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3outposts/client/#can_paginate)
        """
    async def create_endpoint(
        self,
        *,
        OutpostId: str,
        SubnetId: str,
        SecurityGroupId: str,
        AccessType: EndpointAccessTypeType = ...,
        CustomerOwnedIpv4Pool: str = ...
    ) -> CreateEndpointResultTypeDef:
        """
        Creates an endpoint and associates it with the specified Outpost.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3outposts.html#S3Outposts.Client.create_endpoint)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3outposts/client/#create_endpoint)
        """
    async def delete_endpoint(self, *, EndpointId: str, OutpostId: str) -> None:
        """
        Deletes an endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3outposts.html#S3Outposts.Client.delete_endpoint)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3outposts/client/#delete_endpoint)
        """
    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3outposts.html#S3Outposts.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3outposts/client/#generate_presigned_url)
        """
    async def list_endpoints(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> ListEndpointsResultTypeDef:
        """
        Lists endpoints associated with the specified Outpost.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3outposts.html#S3Outposts.Client.list_endpoints)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3outposts/client/#list_endpoints)
        """
    async def list_shared_endpoints(
        self, *, OutpostId: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListSharedEndpointsResultTypeDef:
        """
        Lists all endpoints associated with an Outpost that has been shared by Amazon
        Web Services Resource Access Manager (RAM).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3outposts.html#S3Outposts.Client.list_shared_endpoints)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3outposts/client/#list_shared_endpoints)
        """
    @overload
    def get_paginator(self, operation_name: Literal["list_endpoints"]) -> ListEndpointsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3outposts.html#S3Outposts.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3outposts/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_shared_endpoints"]
    ) -> ListSharedEndpointsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3outposts.html#S3Outposts.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3outposts/client/#get_paginator)
        """
    async def __aenter__(self) -> "S3OutpostsClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3outposts.html#S3Outposts.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3outposts/client/)
        """
    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3outposts.html#S3Outposts.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3outposts/client/)
        """
