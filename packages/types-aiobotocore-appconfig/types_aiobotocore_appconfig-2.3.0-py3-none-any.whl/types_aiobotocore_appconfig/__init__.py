"""
Main interface for appconfig service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_appconfig import (
        AppConfigClient,
        Client,
    )

    session = get_session()
    async with session.create_client("appconfig") as client:
        client: AppConfigClient
        ...

    ```
"""
from .client import AppConfigClient

Client = AppConfigClient


__all__ = ("AppConfigClient", "Client")
