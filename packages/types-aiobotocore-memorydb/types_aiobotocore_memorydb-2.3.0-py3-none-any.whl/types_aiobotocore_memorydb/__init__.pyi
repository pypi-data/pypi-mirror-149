"""
Main interface for memorydb service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_memorydb import (
        Client,
        MemoryDBClient,
    )

    session = get_session()
    async with session.create_client("memorydb") as client:
        client: MemoryDBClient
        ...

    ```
"""
from .client import MemoryDBClient

Client = MemoryDBClient

__all__ = ("Client", "MemoryDBClient")
