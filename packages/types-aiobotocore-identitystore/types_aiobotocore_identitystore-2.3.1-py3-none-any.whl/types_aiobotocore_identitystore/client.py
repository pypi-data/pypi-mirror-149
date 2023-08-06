"""
Type annotations for identitystore service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_identitystore/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_identitystore.client import IdentityStoreClient

    session = get_session()
    async with session.create_client("identitystore") as client:
        client: IdentityStoreClient
    ```
"""
from typing import Any, Dict, Mapping, Sequence, Type

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .type_defs import (
    DescribeGroupResponseTypeDef,
    DescribeUserResponseTypeDef,
    FilterTypeDef,
    ListGroupsResponseTypeDef,
    ListUsersResponseTypeDef,
)

__all__ = ("IdentityStoreClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class IdentityStoreClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore.html#IdentityStore.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_identitystore/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        IdentityStoreClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore.html#IdentityStore.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_identitystore/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore.html#IdentityStore.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_identitystore/client/#can_paginate)
        """

    async def describe_group(
        self, *, IdentityStoreId: str, GroupId: str
    ) -> DescribeGroupResponseTypeDef:
        """
        Retrieves the group metadata and attributes from `GroupId` in an identity store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore.html#IdentityStore.Client.describe_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_identitystore/client/#describe_group)
        """

    async def describe_user(
        self, *, IdentityStoreId: str, UserId: str
    ) -> DescribeUserResponseTypeDef:
        """
        Retrieves the user metadata and attributes from `UserId` in an identity store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore.html#IdentityStore.Client.describe_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_identitystore/client/#describe_user)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore.html#IdentityStore.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_identitystore/client/#generate_presigned_url)
        """

    async def list_groups(
        self,
        *,
        IdentityStoreId: str,
        MaxResults: int = ...,
        NextToken: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...
    ) -> ListGroupsResponseTypeDef:
        """
        Lists the attribute name and value of the group that you specified in the
        search.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore.html#IdentityStore.Client.list_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_identitystore/client/#list_groups)
        """

    async def list_users(
        self,
        *,
        IdentityStoreId: str,
        MaxResults: int = ...,
        NextToken: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...
    ) -> ListUsersResponseTypeDef:
        """
        Lists the attribute name and value of the user that you specified in the search.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore.html#IdentityStore.Client.list_users)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_identitystore/client/#list_users)
        """

    async def __aenter__(self) -> "IdentityStoreClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore.html#IdentityStore.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_identitystore/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore.html#IdentityStore.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_identitystore/client/)
        """
