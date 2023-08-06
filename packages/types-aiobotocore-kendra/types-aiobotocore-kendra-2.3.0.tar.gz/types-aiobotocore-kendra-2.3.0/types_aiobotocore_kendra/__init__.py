"""
Main interface for kendra service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_kendra import (
        Client,
        kendraClient,
    )

    session = get_session()
    async with session.create_client("kendra") as client:
        client: kendraClient
        ...

    ```
"""
from .client import kendraClient

Client = kendraClient


__all__ = ("Client", "kendraClient")
