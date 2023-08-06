"""
Type annotations for qldb-session service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qldb_session/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_qldb_session.client import QLDBSessionClient

    session = get_session()
    async with session.create_client("qldb-session") as client:
        client: QLDBSessionClient
    ```
"""
from typing import Any, Dict, Mapping, Type

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .type_defs import (
    CommitTransactionRequestTypeDef,
    ExecuteStatementRequestTypeDef,
    FetchPageRequestTypeDef,
    SendCommandResultTypeDef,
    StartSessionRequestTypeDef,
)

__all__ = ("QLDBSessionClient",)

class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    BadRequestException: Type[BotocoreClientError]
    CapacityExceededException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    InvalidSessionException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    OccConflictException: Type[BotocoreClientError]
    RateExceededException: Type[BotocoreClientError]

class QLDBSessionClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qldb-session.html#QLDBSession.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qldb_session/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        QLDBSessionClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qldb-session.html#QLDBSession.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qldb_session/client/#exceptions)
        """
    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qldb-session.html#QLDBSession.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qldb_session/client/#can_paginate)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qldb-session.html#QLDBSession.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qldb_session/client/#generate_presigned_url)
        """
    async def send_command(
        self,
        *,
        SessionToken: str = ...,
        StartSession: "StartSessionRequestTypeDef" = ...,
        StartTransaction: Mapping[str, Any] = ...,
        EndSession: Mapping[str, Any] = ...,
        CommitTransaction: "CommitTransactionRequestTypeDef" = ...,
        AbortTransaction: Mapping[str, Any] = ...,
        ExecuteStatement: "ExecuteStatementRequestTypeDef" = ...,
        FetchPage: "FetchPageRequestTypeDef" = ...
    ) -> SendCommandResultTypeDef:
        """
        Sends a command to an Amazon QLDB ledger.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qldb-session.html#QLDBSession.Client.send_command)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qldb_session/client/#send_command)
        """
    async def __aenter__(self) -> "QLDBSessionClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qldb-session.html#QLDBSession.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qldb_session/client/)
        """
    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qldb-session.html#QLDBSession.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qldb_session/client/)
        """
