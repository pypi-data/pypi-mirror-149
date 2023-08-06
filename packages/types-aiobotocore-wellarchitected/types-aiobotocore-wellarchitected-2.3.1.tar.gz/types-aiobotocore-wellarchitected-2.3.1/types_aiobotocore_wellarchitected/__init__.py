"""
Main interface for wellarchitected service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_wellarchitected import (
        Client,
        WellArchitectedClient,
    )

    session = get_session()
    async with session.create_client("wellarchitected") as client:
        client: WellArchitectedClient
        ...

    ```
"""
from .client import WellArchitectedClient

Client = WellArchitectedClient


__all__ = ("Client", "WellArchitectedClient")
