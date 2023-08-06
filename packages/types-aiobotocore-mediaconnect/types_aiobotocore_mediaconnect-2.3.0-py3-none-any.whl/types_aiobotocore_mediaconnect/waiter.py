"""
Type annotations for mediaconnect service client waiters.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/waiters/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_mediaconnect.client import MediaConnectClient
    from types_aiobotocore_mediaconnect.waiter import (
        FlowActiveWaiter,
        FlowDeletedWaiter,
        FlowStandbyWaiter,
    )

    session = get_session()
    async with session.create_client("mediaconnect") as client:
        client: MediaConnectClient

        flow_active_waiter: FlowActiveWaiter = client.get_waiter("flow_active")
        flow_deleted_waiter: FlowDeletedWaiter = client.get_waiter("flow_deleted")
        flow_standby_waiter: FlowStandbyWaiter = client.get_waiter("flow_standby")
    ```
"""
from aiobotocore.waiter import AIOWaiter

from .type_defs import WaiterConfigTypeDef

__all__ = ("FlowActiveWaiter", "FlowDeletedWaiter", "FlowStandbyWaiter")


class FlowActiveWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Waiter.FlowActive)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/waiters/#flowactivewaiter)
    """

    async def wait(self, *, FlowArn: str, WaiterConfig: "WaiterConfigTypeDef" = ...) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Waiter.FlowActive.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/waiters/#flowactivewaiter)
        """


class FlowDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Waiter.FlowDeleted)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/waiters/#flowdeletedwaiter)
    """

    async def wait(self, *, FlowArn: str, WaiterConfig: "WaiterConfigTypeDef" = ...) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Waiter.FlowDeleted.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/waiters/#flowdeletedwaiter)
        """


class FlowStandbyWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Waiter.FlowStandby)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/waiters/#flowstandbywaiter)
    """

    async def wait(self, *, FlowArn: str, WaiterConfig: "WaiterConfigTypeDef" = ...) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Waiter.FlowStandby.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/waiters/#flowstandbywaiter)
        """
