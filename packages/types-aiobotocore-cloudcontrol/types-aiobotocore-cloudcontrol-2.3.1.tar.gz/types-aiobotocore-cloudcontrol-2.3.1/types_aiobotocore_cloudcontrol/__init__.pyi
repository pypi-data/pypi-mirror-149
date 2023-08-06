"""
Main interface for cloudcontrol service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_cloudcontrol import (
        Client,
        CloudControlApiClient,
        ResourceRequestSuccessWaiter,
    )

    session = get_session()
    async with session.create_client("cloudcontrol") as client:
        client: CloudControlApiClient
        ...


    resource_request_success_waiter: ResourceRequestSuccessWaiter = client.get_waiter("resource_request_success")
    ```
"""
from .client import CloudControlApiClient
from .waiter import ResourceRequestSuccessWaiter

Client = CloudControlApiClient

__all__ = ("Client", "CloudControlApiClient", "ResourceRequestSuccessWaiter")
