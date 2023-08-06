"""
Main interface for lookoutequipment service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_lookoutequipment import (
        Client,
        LookoutEquipmentClient,
    )

    session = get_session()
    async with session.create_client("lookoutequipment") as client:
        client: LookoutEquipmentClient
        ...

    ```
"""
from .client import LookoutEquipmentClient

Client = LookoutEquipmentClient


__all__ = ("Client", "LookoutEquipmentClient")
