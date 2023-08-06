"""
Type annotations for medialive service client waiters.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/waiters/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_medialive.client import MediaLiveClient
    from types_aiobotocore_medialive.waiter import (
        ChannelCreatedWaiter,
        ChannelDeletedWaiter,
        ChannelRunningWaiter,
        ChannelStoppedWaiter,
        InputAttachedWaiter,
        InputDeletedWaiter,
        InputDetachedWaiter,
        MultiplexCreatedWaiter,
        MultiplexDeletedWaiter,
        MultiplexRunningWaiter,
        MultiplexStoppedWaiter,
    )

    session = get_session()
    async with session.create_client("medialive") as client:
        client: MediaLiveClient

        channel_created_waiter: ChannelCreatedWaiter = client.get_waiter("channel_created")
        channel_deleted_waiter: ChannelDeletedWaiter = client.get_waiter("channel_deleted")
        channel_running_waiter: ChannelRunningWaiter = client.get_waiter("channel_running")
        channel_stopped_waiter: ChannelStoppedWaiter = client.get_waiter("channel_stopped")
        input_attached_waiter: InputAttachedWaiter = client.get_waiter("input_attached")
        input_deleted_waiter: InputDeletedWaiter = client.get_waiter("input_deleted")
        input_detached_waiter: InputDetachedWaiter = client.get_waiter("input_detached")
        multiplex_created_waiter: MultiplexCreatedWaiter = client.get_waiter("multiplex_created")
        multiplex_deleted_waiter: MultiplexDeletedWaiter = client.get_waiter("multiplex_deleted")
        multiplex_running_waiter: MultiplexRunningWaiter = client.get_waiter("multiplex_running")
        multiplex_stopped_waiter: MultiplexStoppedWaiter = client.get_waiter("multiplex_stopped")
    ```
"""
from aiobotocore.waiter import AIOWaiter

from .type_defs import WaiterConfigTypeDef

__all__ = (
    "ChannelCreatedWaiter",
    "ChannelDeletedWaiter",
    "ChannelRunningWaiter",
    "ChannelStoppedWaiter",
    "InputAttachedWaiter",
    "InputDeletedWaiter",
    "InputDetachedWaiter",
    "MultiplexCreatedWaiter",
    "MultiplexDeletedWaiter",
    "MultiplexRunningWaiter",
    "MultiplexStoppedWaiter",
)


class ChannelCreatedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Waiter.ChannelCreated)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/waiters/#channelcreatedwaiter)
    """

    async def wait(self, *, ChannelId: str, WaiterConfig: "WaiterConfigTypeDef" = ...) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Waiter.ChannelCreated.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/waiters/#channelcreatedwaiter)
        """


class ChannelDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Waiter.ChannelDeleted)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/waiters/#channeldeletedwaiter)
    """

    async def wait(self, *, ChannelId: str, WaiterConfig: "WaiterConfigTypeDef" = ...) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Waiter.ChannelDeleted.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/waiters/#channeldeletedwaiter)
        """


class ChannelRunningWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Waiter.ChannelRunning)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/waiters/#channelrunningwaiter)
    """

    async def wait(self, *, ChannelId: str, WaiterConfig: "WaiterConfigTypeDef" = ...) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Waiter.ChannelRunning.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/waiters/#channelrunningwaiter)
        """


class ChannelStoppedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Waiter.ChannelStopped)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/waiters/#channelstoppedwaiter)
    """

    async def wait(self, *, ChannelId: str, WaiterConfig: "WaiterConfigTypeDef" = ...) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Waiter.ChannelStopped.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/waiters/#channelstoppedwaiter)
        """


class InputAttachedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Waiter.InputAttached)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/waiters/#inputattachedwaiter)
    """

    async def wait(self, *, InputId: str, WaiterConfig: "WaiterConfigTypeDef" = ...) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Waiter.InputAttached.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/waiters/#inputattachedwaiter)
        """


class InputDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Waiter.InputDeleted)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/waiters/#inputdeletedwaiter)
    """

    async def wait(self, *, InputId: str, WaiterConfig: "WaiterConfigTypeDef" = ...) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Waiter.InputDeleted.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/waiters/#inputdeletedwaiter)
        """


class InputDetachedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Waiter.InputDetached)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/waiters/#inputdetachedwaiter)
    """

    async def wait(self, *, InputId: str, WaiterConfig: "WaiterConfigTypeDef" = ...) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Waiter.InputDetached.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/waiters/#inputdetachedwaiter)
        """


class MultiplexCreatedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Waiter.MultiplexCreated)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/waiters/#multiplexcreatedwaiter)
    """

    async def wait(self, *, MultiplexId: str, WaiterConfig: "WaiterConfigTypeDef" = ...) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Waiter.MultiplexCreated.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/waiters/#multiplexcreatedwaiter)
        """


class MultiplexDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Waiter.MultiplexDeleted)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/waiters/#multiplexdeletedwaiter)
    """

    async def wait(self, *, MultiplexId: str, WaiterConfig: "WaiterConfigTypeDef" = ...) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Waiter.MultiplexDeleted.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/waiters/#multiplexdeletedwaiter)
        """


class MultiplexRunningWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Waiter.MultiplexRunning)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/waiters/#multiplexrunningwaiter)
    """

    async def wait(self, *, MultiplexId: str, WaiterConfig: "WaiterConfigTypeDef" = ...) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Waiter.MultiplexRunning.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/waiters/#multiplexrunningwaiter)
        """


class MultiplexStoppedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Waiter.MultiplexStopped)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/waiters/#multiplexstoppedwaiter)
    """

    async def wait(self, *, MultiplexId: str, WaiterConfig: "WaiterConfigTypeDef" = ...) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Waiter.MultiplexStopped.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/waiters/#multiplexstoppedwaiter)
        """
