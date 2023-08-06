"""
Main interface for marketplace-catalog service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_marketplace_catalog import (
        Client,
        MarketplaceCatalogClient,
    )

    session = get_session()
    async with session.create_client("marketplace-catalog") as client:
        client: MarketplaceCatalogClient
        ...

    ```
"""
from .client import MarketplaceCatalogClient

Client = MarketplaceCatalogClient

__all__ = ("Client", "MarketplaceCatalogClient")
