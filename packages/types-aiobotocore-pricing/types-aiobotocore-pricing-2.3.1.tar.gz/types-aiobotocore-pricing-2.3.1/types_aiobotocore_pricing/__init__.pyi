"""
Main interface for pricing service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_pricing import (
        Client,
        DescribeServicesPaginator,
        GetAttributeValuesPaginator,
        GetProductsPaginator,
        PricingClient,
    )

    session = get_session()
    async with session.create_client("pricing") as client:
        client: PricingClient
        ...


    describe_services_paginator: DescribeServicesPaginator = client.get_paginator("describe_services")
    get_attribute_values_paginator: GetAttributeValuesPaginator = client.get_paginator("get_attribute_values")
    get_products_paginator: GetProductsPaginator = client.get_paginator("get_products")
    ```
"""
from .client import PricingClient
from .paginator import DescribeServicesPaginator, GetAttributeValuesPaginator, GetProductsPaginator

Client = PricingClient

__all__ = (
    "Client",
    "DescribeServicesPaginator",
    "GetAttributeValuesPaginator",
    "GetProductsPaginator",
    "PricingClient",
)
