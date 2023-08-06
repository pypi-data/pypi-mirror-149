"""
Main interface for iotsecuretunneling service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_iotsecuretunneling import (
        Client,
        IoTSecureTunnelingClient,
    )

    session = get_session()
    async with session.create_client("iotsecuretunneling") as client:
        client: IoTSecureTunnelingClient
        ...

    ```
"""
from .client import IoTSecureTunnelingClient

Client = IoTSecureTunnelingClient

__all__ = ("Client", "IoTSecureTunnelingClient")
