"""
Type annotations for mediaconnect service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_mediaconnect.client import MediaConnectClient
    from types_aiobotocore_mediaconnect.paginator import (
        ListEntitlementsPaginator,
        ListFlowsPaginator,
        ListOfferingsPaginator,
        ListReservationsPaginator,
    )

    session = get_session()
    with session.create_client("mediaconnect") as client:
        client: MediaConnectClient

        list_entitlements_paginator: ListEntitlementsPaginator = client.get_paginator("list_entitlements")
        list_flows_paginator: ListFlowsPaginator = client.get_paginator("list_flows")
        list_offerings_paginator: ListOfferingsPaginator = client.get_paginator("list_offerings")
        list_reservations_paginator: ListReservationsPaginator = client.get_paginator("list_reservations")
    ```
"""
import sys
from typing import Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListEntitlementsResponseTypeDef,
    ListFlowsResponseTypeDef,
    ListOfferingsResponseTypeDef,
    ListReservationsResponseTypeDef,
    PaginatorConfigTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import AsyncIterator
else:
    from typing_extensions import AsyncIterator


__all__ = (
    "ListEntitlementsPaginator",
    "ListFlowsPaginator",
    "ListOfferingsPaginator",
    "ListReservationsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListEntitlementsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Paginator.ListEntitlements)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/paginators/#listentitlementspaginator)
    """

    def paginate(
        self, *, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListEntitlementsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Paginator.ListEntitlements.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/paginators/#listentitlementspaginator)
        """


class ListFlowsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Paginator.ListFlows)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/paginators/#listflowspaginator)
    """

    def paginate(
        self, *, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListFlowsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Paginator.ListFlows.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/paginators/#listflowspaginator)
        """


class ListOfferingsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Paginator.ListOfferings)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/paginators/#listofferingspaginator)
    """

    def paginate(
        self, *, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListOfferingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Paginator.ListOfferings.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/paginators/#listofferingspaginator)
        """


class ListReservationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Paginator.ListReservations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/paginators/#listreservationspaginator)
    """

    def paginate(
        self, *, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListReservationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconnect.html#MediaConnect.Paginator.ListReservations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconnect/paginators/#listreservationspaginator)
        """
