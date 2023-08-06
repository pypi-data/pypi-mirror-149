"""
Main interface for pi service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_pi import (
        Client,
        PIClient,
    )

    session = get_session()
    async with session.create_client("pi") as client:
        client: PIClient
        ...

    ```
"""
from .client import PIClient

Client = PIClient


__all__ = ("Client", "PIClient")
