"""
Type annotations for kinesis service client waiters.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/waiters/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_kinesis.client import KinesisClient
    from types_aiobotocore_kinesis.waiter import (
        StreamExistsWaiter,
        StreamNotExistsWaiter,
    )

    session = get_session()
    async with session.create_client("kinesis") as client:
        client: KinesisClient

        stream_exists_waiter: StreamExistsWaiter = client.get_waiter("stream_exists")
        stream_not_exists_waiter: StreamNotExistsWaiter = client.get_waiter("stream_not_exists")
    ```
"""
from aiobotocore.waiter import AIOWaiter

from .type_defs import WaiterConfigTypeDef

__all__ = ("StreamExistsWaiter", "StreamNotExistsWaiter")


class StreamExistsWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis.html#Kinesis.Waiter.StreamExists)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/waiters/#streamexistswaiter)
    """

    async def wait(
        self,
        *,
        StreamName: str,
        Limit: int = ...,
        ExclusiveStartShardId: str = ...,
        WaiterConfig: "WaiterConfigTypeDef" = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis.html#Kinesis.Waiter.StreamExists.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/waiters/#streamexistswaiter)
        """


class StreamNotExistsWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis.html#Kinesis.Waiter.StreamNotExists)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/waiters/#streamnotexistswaiter)
    """

    async def wait(
        self,
        *,
        StreamName: str,
        Limit: int = ...,
        ExclusiveStartShardId: str = ...,
        WaiterConfig: "WaiterConfigTypeDef" = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis.html#Kinesis.Waiter.StreamNotExists.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis/waiters/#streamnotexistswaiter)
        """
