"""
Type annotations for marketplace-entitlement service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_entitlement/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_marketplace_entitlement.client import MarketplaceEntitlementServiceClient
    from types_aiobotocore_marketplace_entitlement.paginator import (
        GetEntitlementsPaginator,
    )

    session = get_session()
    with session.create_client("marketplace-entitlement") as client:
        client: MarketplaceEntitlementServiceClient

        get_entitlements_paginator: GetEntitlementsPaginator = client.get_paginator("get_entitlements")
    ```
"""
import sys
from typing import Generic, Iterator, Mapping, Sequence, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .literals import GetEntitlementFilterNameType
from .type_defs import GetEntitlementsResultTypeDef, PaginatorConfigTypeDef

if sys.version_info >= (3, 8):
    from typing import AsyncIterator
else:
    from typing_extensions import AsyncIterator


__all__ = ("GetEntitlementsPaginator",)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class GetEntitlementsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-entitlement.html#MarketplaceEntitlementService.Paginator.GetEntitlements)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_entitlement/paginators/#getentitlementspaginator)
    """

    def paginate(
        self,
        *,
        ProductCode: str,
        Filter: Mapping[GetEntitlementFilterNameType, Sequence[str]] = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[GetEntitlementsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-entitlement.html#MarketplaceEntitlementService.Paginator.GetEntitlements.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_entitlement/paginators/#getentitlementspaginator)
        """
