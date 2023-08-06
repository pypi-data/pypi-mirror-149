"""
Main interface for finspace service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_finspace import (
        Client,
        finspaceClient,
    )

    session = get_session()
    async with session.create_client("finspace") as client:
        client: finspaceClient
        ...

    ```
"""
from .client import finspaceClient

Client = finspaceClient


__all__ = ("Client", "finspaceClient")
