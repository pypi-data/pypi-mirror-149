"""
Main interface for appconfigdata service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_appconfigdata import (
        AppConfigDataClient,
        Client,
    )

    session = get_session()
    async with session.create_client("appconfigdata") as client:
        client: AppConfigDataClient
        ...

    ```
"""
from .client import AppConfigDataClient

Client = AppConfigDataClient


__all__ = ("AppConfigDataClient", "Client")
