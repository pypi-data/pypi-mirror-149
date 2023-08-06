"""
Type annotations for apigatewaymanagementapi service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewaymanagementapi/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_apigatewaymanagementapi.client import ApiGatewayManagementApiClient

    session = get_session()
    async with session.create_client("apigatewaymanagementapi") as client:
        client: ApiGatewayManagementApiClient
    ```
"""
from typing import IO, Any, Dict, Mapping, Type, Union

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.response import StreamingBody

from .type_defs import GetConnectionResponseTypeDef

__all__ = ("ApiGatewayManagementApiClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    ForbiddenException: Type[BotocoreClientError]
    GoneException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    PayloadTooLargeException: Type[BotocoreClientError]


class ApiGatewayManagementApiClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewaymanagementapi.html#ApiGatewayManagementApi.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewaymanagementapi/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ApiGatewayManagementApiClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewaymanagementapi.html#ApiGatewayManagementApi.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewaymanagementapi/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewaymanagementapi.html#ApiGatewayManagementApi.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewaymanagementapi/client/#can_paginate)
        """

    async def delete_connection(self, *, ConnectionId: str) -> None:
        """
        Delete the connection with the provided id.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewaymanagementapi.html#ApiGatewayManagementApi.Client.delete_connection)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewaymanagementapi/client/#delete_connection)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewaymanagementapi.html#ApiGatewayManagementApi.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewaymanagementapi/client/#generate_presigned_url)
        """

    async def get_connection(self, *, ConnectionId: str) -> GetConnectionResponseTypeDef:
        """
        Get information about the connection with the provided id.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewaymanagementapi.html#ApiGatewayManagementApi.Client.get_connection)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewaymanagementapi/client/#get_connection)
        """

    async def post_to_connection(
        self, *, Data: Union[str, bytes, IO[Any], StreamingBody], ConnectionId: str
    ) -> None:
        """
        Sends the provided data to the specified connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewaymanagementapi.html#ApiGatewayManagementApi.Client.post_to_connection)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewaymanagementapi/client/#post_to_connection)
        """

    async def __aenter__(self) -> "ApiGatewayManagementApiClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewaymanagementapi.html#ApiGatewayManagementApi.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewaymanagementapi/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewaymanagementapi.html#ApiGatewayManagementApi.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewaymanagementapi/client/)
        """
