"""
Main interface for appintegrations service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_appintegrations import (
        AppIntegrationsServiceClient,
        Client,
    )

    session = get_session()
    async with session.create_client("appintegrations") as client:
        client: AppIntegrationsServiceClient
        ...

    ```
"""
from .client import AppIntegrationsServiceClient

Client = AppIntegrationsServiceClient

__all__ = ("AppIntegrationsServiceClient", "Client")
