"""
Type annotations for cloudcontrol service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudcontrol/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_cloudcontrol.client import CloudControlApiClient

    session = get_session()
    async with session.create_client("cloudcontrol") as client:
        client: CloudControlApiClient
    ```
"""
import sys
from typing import Any, Dict, Mapping, Type

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .type_defs import (
    CancelResourceRequestOutputTypeDef,
    CreateResourceOutputTypeDef,
    DeleteResourceOutputTypeDef,
    GetResourceOutputTypeDef,
    GetResourceRequestStatusOutputTypeDef,
    ListResourceRequestsOutputTypeDef,
    ListResourcesOutputTypeDef,
    ResourceRequestStatusFilterTypeDef,
    UpdateResourceOutputTypeDef,
)
from .waiter import ResourceRequestSuccessWaiter

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("CloudControlApiClient",)

class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AlreadyExistsException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ClientTokenConflictException: Type[BotocoreClientError]
    ConcurrentModificationException: Type[BotocoreClientError]
    ConcurrentOperationException: Type[BotocoreClientError]
    GeneralServiceException: Type[BotocoreClientError]
    HandlerFailureException: Type[BotocoreClientError]
    HandlerInternalFailureException: Type[BotocoreClientError]
    InvalidCredentialsException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    NetworkFailureException: Type[BotocoreClientError]
    NotStabilizedException: Type[BotocoreClientError]
    NotUpdatableException: Type[BotocoreClientError]
    PrivateTypeException: Type[BotocoreClientError]
    RequestTokenNotFoundException: Type[BotocoreClientError]
    ResourceConflictException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceInternalErrorException: Type[BotocoreClientError]
    ServiceLimitExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    TypeNotFoundException: Type[BotocoreClientError]
    UnsupportedActionException: Type[BotocoreClientError]

class CloudControlApiClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudcontrol.html#CloudControlApi.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudcontrol/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CloudControlApiClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudcontrol.html#CloudControlApi.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudcontrol/client/#exceptions)
        """
    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudcontrol.html#CloudControlApi.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudcontrol/client/#can_paginate)
        """
    async def cancel_resource_request(
        self, *, RequestToken: str
    ) -> CancelResourceRequestOutputTypeDef:
        """
        Cancels the specified resource operation request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudcontrol.html#CloudControlApi.Client.cancel_resource_request)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudcontrol/client/#cancel_resource_request)
        """
    async def create_resource(
        self,
        *,
        TypeName: str,
        DesiredState: str,
        TypeVersionId: str = ...,
        RoleArn: str = ...,
        ClientToken: str = ...
    ) -> CreateResourceOutputTypeDef:
        """
        Creates the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudcontrol.html#CloudControlApi.Client.create_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudcontrol/client/#create_resource)
        """
    async def delete_resource(
        self,
        *,
        TypeName: str,
        Identifier: str,
        TypeVersionId: str = ...,
        RoleArn: str = ...,
        ClientToken: str = ...
    ) -> DeleteResourceOutputTypeDef:
        """
        Deletes the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudcontrol.html#CloudControlApi.Client.delete_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudcontrol/client/#delete_resource)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudcontrol.html#CloudControlApi.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudcontrol/client/#generate_presigned_url)
        """
    async def get_resource(
        self, *, TypeName: str, Identifier: str, TypeVersionId: str = ..., RoleArn: str = ...
    ) -> GetResourceOutputTypeDef:
        """
        Returns information about the current state of the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudcontrol.html#CloudControlApi.Client.get_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudcontrol/client/#get_resource)
        """
    async def get_resource_request_status(
        self, *, RequestToken: str
    ) -> GetResourceRequestStatusOutputTypeDef:
        """
        Returns the current status of a resource operation request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudcontrol.html#CloudControlApi.Client.get_resource_request_status)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudcontrol/client/#get_resource_request_status)
        """
    async def list_resource_requests(
        self,
        *,
        MaxResults: int = ...,
        NextToken: str = ...,
        ResourceRequestStatusFilter: "ResourceRequestStatusFilterTypeDef" = ...
    ) -> ListResourceRequestsOutputTypeDef:
        """
        Returns existing resource operation requests.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudcontrol.html#CloudControlApi.Client.list_resource_requests)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudcontrol/client/#list_resource_requests)
        """
    async def list_resources(
        self,
        *,
        TypeName: str,
        TypeVersionId: str = ...,
        RoleArn: str = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
        ResourceModel: str = ...
    ) -> ListResourcesOutputTypeDef:
        """
        Returns information about the specified resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudcontrol.html#CloudControlApi.Client.list_resources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudcontrol/client/#list_resources)
        """
    async def update_resource(
        self,
        *,
        TypeName: str,
        Identifier: str,
        PatchDocument: str,
        TypeVersionId: str = ...,
        RoleArn: str = ...,
        ClientToken: str = ...
    ) -> UpdateResourceOutputTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudcontrol.html#CloudControlApi.Client.update_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudcontrol/client/#update_resource)
        """
    def get_waiter(
        self, waiter_name: Literal["resource_request_success"]
    ) -> ResourceRequestSuccessWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudcontrol.html#CloudControlApi.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudcontrol/client/#get_waiter)
        """
    async def __aenter__(self) -> "CloudControlApiClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudcontrol.html#CloudControlApi.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudcontrol/client/)
        """
    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudcontrol.html#CloudControlApi.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudcontrol/client/)
        """
