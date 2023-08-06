"""
Type annotations for pricing service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pricing/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_pricing.client import PricingClient
    from types_aiobotocore_pricing.paginator import (
        DescribeServicesPaginator,
        GetAttributeValuesPaginator,
        GetProductsPaginator,
    )

    session = get_session()
    with session.create_client("pricing") as client:
        client: PricingClient

        describe_services_paginator: DescribeServicesPaginator = client.get_paginator("describe_services")
        get_attribute_values_paginator: GetAttributeValuesPaginator = client.get_paginator("get_attribute_values")
        get_products_paginator: GetProductsPaginator = client.get_paginator("get_products")
    ```
"""
import sys
from typing import Generic, Iterator, Sequence, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    DescribeServicesResponseTypeDef,
    FilterTypeDef,
    GetAttributeValuesResponseTypeDef,
    GetProductsResponseTypeDef,
    PaginatorConfigTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import AsyncIterator
else:
    from typing_extensions import AsyncIterator


__all__ = ("DescribeServicesPaginator", "GetAttributeValuesPaginator", "GetProductsPaginator")


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeServicesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pricing.html#Pricing.Paginator.DescribeServices)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pricing/paginators/#describeservicespaginator)
    """

    def paginate(
        self,
        *,
        ServiceCode: str = ...,
        FormatVersion: str = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DescribeServicesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pricing.html#Pricing.Paginator.DescribeServices.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pricing/paginators/#describeservicespaginator)
        """


class GetAttributeValuesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pricing.html#Pricing.Paginator.GetAttributeValues)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pricing/paginators/#getattributevaluespaginator)
    """

    def paginate(
        self,
        *,
        ServiceCode: str,
        AttributeName: str,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[GetAttributeValuesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pricing.html#Pricing.Paginator.GetAttributeValues.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pricing/paginators/#getattributevaluespaginator)
        """


class GetProductsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pricing.html#Pricing.Paginator.GetProducts)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pricing/paginators/#getproductspaginator)
    """

    def paginate(
        self,
        *,
        ServiceCode: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        FormatVersion: str = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[GetProductsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pricing.html#Pricing.Paginator.GetProducts.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pricing/paginators/#getproductspaginator)
        """
