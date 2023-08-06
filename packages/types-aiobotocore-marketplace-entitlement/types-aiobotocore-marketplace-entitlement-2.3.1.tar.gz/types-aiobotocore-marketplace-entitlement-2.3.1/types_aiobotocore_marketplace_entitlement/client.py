"""
Type annotations for marketplace-entitlement service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_entitlement/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_marketplace_entitlement.client import MarketplaceEntitlementServiceClient

    session = get_session()
    async with session.create_client("marketplace-entitlement") as client:
        client: MarketplaceEntitlementServiceClient
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import GetEntitlementFilterNameType
from .paginator import GetEntitlementsPaginator
from .type_defs import GetEntitlementsResultTypeDef

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("MarketplaceEntitlementServiceClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    InternalServiceErrorException: Type[BotocoreClientError]
    InvalidParameterException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]


class MarketplaceEntitlementServiceClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-entitlement.html#MarketplaceEntitlementService.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_entitlement/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        MarketplaceEntitlementServiceClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-entitlement.html#MarketplaceEntitlementService.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_entitlement/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-entitlement.html#MarketplaceEntitlementService.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_entitlement/client/#can_paginate)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-entitlement.html#MarketplaceEntitlementService.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_entitlement/client/#generate_presigned_url)
        """

    async def get_entitlements(
        self,
        *,
        ProductCode: str,
        Filter: Mapping[GetEntitlementFilterNameType, Sequence[str]] = ...,
        NextToken: str = ...,
        MaxResults: int = ...
    ) -> GetEntitlementsResultTypeDef:
        """
        GetEntitlements retrieves entitlement values for a given product.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-entitlement.html#MarketplaceEntitlementService.Client.get_entitlements)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_entitlement/client/#get_entitlements)
        """

    def get_paginator(
        self, operation_name: Literal["get_entitlements"]
    ) -> GetEntitlementsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-entitlement.html#MarketplaceEntitlementService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_entitlement/client/#get_paginator)
        """

    async def __aenter__(self) -> "MarketplaceEntitlementServiceClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-entitlement.html#MarketplaceEntitlementService.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_entitlement/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-entitlement.html#MarketplaceEntitlementService.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_entitlement/client/)
        """
