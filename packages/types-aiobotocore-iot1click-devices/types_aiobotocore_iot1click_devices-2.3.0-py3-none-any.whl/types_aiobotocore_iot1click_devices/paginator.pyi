"""
Type annotations for iot1click-devices service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot1click_devices/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_iot1click_devices.client import IoT1ClickDevicesServiceClient
    from types_aiobotocore_iot1click_devices.paginator import (
        ListDeviceEventsPaginator,
        ListDevicesPaginator,
    )

    session = get_session()
    with session.create_client("iot1click-devices") as client:
        client: IoT1ClickDevicesServiceClient

        list_device_events_paginator: ListDeviceEventsPaginator = client.get_paginator("list_device_events")
        list_devices_paginator: ListDevicesPaginator = client.get_paginator("list_devices")
    ```
"""
import sys
from datetime import datetime
from typing import Generic, Iterator, TypeVar, Union

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListDeviceEventsResponseTypeDef,
    ListDevicesResponseTypeDef,
    PaginatorConfigTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import AsyncIterator
else:
    from typing_extensions import AsyncIterator

__all__ = ("ListDeviceEventsPaginator", "ListDevicesPaginator")

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListDeviceEventsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-devices.html#IoT1ClickDevicesService.Paginator.ListDeviceEvents)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot1click_devices/paginators/#listdeviceeventspaginator)
    """

    def paginate(
        self,
        *,
        DeviceId: str,
        FromTimeStamp: Union[datetime, str],
        ToTimeStamp: Union[datetime, str],
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListDeviceEventsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-devices.html#IoT1ClickDevicesService.Paginator.ListDeviceEvents.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot1click_devices/paginators/#listdeviceeventspaginator)
        """

class ListDevicesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-devices.html#IoT1ClickDevicesService.Paginator.ListDevices)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot1click_devices/paginators/#listdevicespaginator)
    """

    def paginate(
        self, *, DeviceType: str = ..., PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListDevicesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot1click-devices.html#IoT1ClickDevicesService.Paginator.ListDevices.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot1click_devices/paginators/#listdevicespaginator)
        """
