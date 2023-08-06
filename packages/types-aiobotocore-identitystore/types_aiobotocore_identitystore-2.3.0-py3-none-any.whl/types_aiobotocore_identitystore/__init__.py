"""
Main interface for identitystore service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_identitystore import (
        Client,
        IdentityStoreClient,
    )

    session = get_session()
    async with session.create_client("identitystore") as client:
        client: IdentityStoreClient
        ...

    ```
"""
from .client import IdentityStoreClient

Client = IdentityStoreClient


__all__ = ("Client", "IdentityStoreClient")
