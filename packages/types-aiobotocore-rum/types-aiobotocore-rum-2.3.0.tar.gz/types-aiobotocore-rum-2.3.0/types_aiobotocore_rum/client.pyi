"""
Type annotations for rum service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rum/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_rum.client import CloudWatchRUMClient

    session = get_session()
    async with session.create_client("rum") as client:
        client: CloudWatchRUMClient
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import GetAppMonitorDataPaginator, ListAppMonitorsPaginator
from .type_defs import (
    AppMonitorConfigurationTypeDef,
    AppMonitorDetailsTypeDef,
    CreateAppMonitorResponseTypeDef,
    GetAppMonitorDataResponseTypeDef,
    GetAppMonitorResponseTypeDef,
    ListAppMonitorsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    QueryFilterTypeDef,
    RumEventTypeDef,
    TimeRangeTypeDef,
    UserDetailsTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("CloudWatchRUMClient",)

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
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class CloudWatchRUMClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum.html#CloudWatchRUM.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rum/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CloudWatchRUMClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum.html#CloudWatchRUM.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rum/client/#exceptions)
        """
    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum.html#CloudWatchRUM.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rum/client/#can_paginate)
        """
    async def create_app_monitor(
        self,
        *,
        Domain: str,
        Name: str,
        AppMonitorConfiguration: "AppMonitorConfigurationTypeDef" = ...,
        CwLogEnabled: bool = ...,
        Tags: Mapping[str, str] = ...
    ) -> CreateAppMonitorResponseTypeDef:
        """
        Creates a Amazon CloudWatch RUM app monitor, which collects telemetry data from
        your application and sends that data to RUM.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum.html#CloudWatchRUM.Client.create_app_monitor)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rum/client/#create_app_monitor)
        """
    async def delete_app_monitor(self, *, Name: str) -> Dict[str, Any]:
        """
        Deletes an existing app monitor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum.html#CloudWatchRUM.Client.delete_app_monitor)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rum/client/#delete_app_monitor)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum.html#CloudWatchRUM.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rum/client/#generate_presigned_url)
        """
    async def get_app_monitor(self, *, Name: str) -> GetAppMonitorResponseTypeDef:
        """
        Retrieves the complete configuration information for one app monitor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum.html#CloudWatchRUM.Client.get_app_monitor)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rum/client/#get_app_monitor)
        """
    async def get_app_monitor_data(
        self,
        *,
        Name: str,
        TimeRange: "TimeRangeTypeDef",
        Filters: Sequence["QueryFilterTypeDef"] = ...,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> GetAppMonitorDataResponseTypeDef:
        """
        Retrieves the raw performance events that RUM has collected from your web
        application, so that you can do your own processing or analysis of this data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum.html#CloudWatchRUM.Client.get_app_monitor_data)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rum/client/#get_app_monitor_data)
        """
    async def list_app_monitors(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListAppMonitorsResponseTypeDef:
        """
        Returns a list of the Amazon CloudWatch RUM app monitors in the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum.html#CloudWatchRUM.Client.list_app_monitors)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rum/client/#list_app_monitors)
        """
    async def list_tags_for_resource(
        self, *, ResourceArn: str
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Displays the tags associated with a CloudWatch RUM resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum.html#CloudWatchRUM.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rum/client/#list_tags_for_resource)
        """
    async def put_rum_events(
        self,
        *,
        AppMonitorDetails: "AppMonitorDetailsTypeDef",
        BatchId: str,
        Id: str,
        RumEvents: Sequence["RumEventTypeDef"],
        UserDetails: "UserDetailsTypeDef"
    ) -> Dict[str, Any]:
        """
        Sends telemetry events about your application performance and user behavior to
        CloudWatch RUM.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum.html#CloudWatchRUM.Client.put_rum_events)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rum/client/#put_rum_events)
        """
    async def tag_resource(self, *, ResourceArn: str, Tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Assigns one or more tags (key-value pairs) to the specified CloudWatch RUM
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum.html#CloudWatchRUM.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rum/client/#tag_resource)
        """
    async def untag_resource(self, *, ResourceArn: str, TagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes one or more tags from the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum.html#CloudWatchRUM.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rum/client/#untag_resource)
        """
    async def update_app_monitor(
        self,
        *,
        Name: str,
        AppMonitorConfiguration: "AppMonitorConfigurationTypeDef" = ...,
        CwLogEnabled: bool = ...,
        Domain: str = ...
    ) -> Dict[str, Any]:
        """
        Updates the configuration of an existing app monitor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum.html#CloudWatchRUM.Client.update_app_monitor)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rum/client/#update_app_monitor)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["get_app_monitor_data"]
    ) -> GetAppMonitorDataPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum.html#CloudWatchRUM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rum/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_app_monitors"]
    ) -> ListAppMonitorsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum.html#CloudWatchRUM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rum/client/#get_paginator)
        """
    async def __aenter__(self) -> "CloudWatchRUMClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum.html#CloudWatchRUM.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rum/client/)
        """
    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum.html#CloudWatchRUM.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rum/client/)
        """
