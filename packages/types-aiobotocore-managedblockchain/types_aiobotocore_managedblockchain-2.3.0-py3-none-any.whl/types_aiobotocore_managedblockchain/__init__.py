"""
Main interface for managedblockchain service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_managedblockchain import (
        Client,
        ManagedBlockchainClient,
    )

    session = get_session()
    async with session.create_client("managedblockchain") as client:
        client: ManagedBlockchainClient
        ...

    ```
"""
from .client import ManagedBlockchainClient

Client = ManagedBlockchainClient


__all__ = ("Client", "ManagedBlockchainClient")
