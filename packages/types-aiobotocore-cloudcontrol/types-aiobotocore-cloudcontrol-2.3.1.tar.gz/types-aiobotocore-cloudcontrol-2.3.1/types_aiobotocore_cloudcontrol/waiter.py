"""
Type annotations for cloudcontrol service client waiters.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudcontrol/waiters/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_cloudcontrol.client import CloudControlApiClient
    from types_aiobotocore_cloudcontrol.waiter import (
        ResourceRequestSuccessWaiter,
    )

    session = get_session()
    async with session.create_client("cloudcontrol") as client:
        client: CloudControlApiClient

        resource_request_success_waiter: ResourceRequestSuccessWaiter = client.get_waiter("resource_request_success")
    ```
"""
from aiobotocore.waiter import AIOWaiter

from .type_defs import WaiterConfigTypeDef

__all__ = ("ResourceRequestSuccessWaiter",)


class ResourceRequestSuccessWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudcontrol.html#CloudControlApi.Waiter.ResourceRequestSuccess)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudcontrol/waiters/#resourcerequestsuccesswaiter)
    """

    async def wait(self, *, RequestToken: str, WaiterConfig: "WaiterConfigTypeDef" = ...) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudcontrol.html#CloudControlApi.Waiter.ResourceRequestSuccess.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudcontrol/waiters/#resourcerequestsuccesswaiter)
        """
