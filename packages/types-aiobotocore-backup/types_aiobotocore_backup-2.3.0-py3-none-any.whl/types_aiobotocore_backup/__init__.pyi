"""
Main interface for backup service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_backup import (
        BackupClient,
        Client,
    )

    session = get_session()
    async with session.create_client("backup") as client:
        client: BackupClient
        ...

    ```
"""
from .client import BackupClient

Client = BackupClient

__all__ = ("BackupClient", "Client")
