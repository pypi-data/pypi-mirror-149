"""
Main interface for qldb service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_qldb import (
        Client,
        QLDBClient,
    )

    session = get_session()
    async with session.create_client("qldb") as client:
        client: QLDBClient
        ...

    ```
"""
from .client import QLDBClient

Client = QLDBClient


__all__ = ("Client", "QLDBClient")
