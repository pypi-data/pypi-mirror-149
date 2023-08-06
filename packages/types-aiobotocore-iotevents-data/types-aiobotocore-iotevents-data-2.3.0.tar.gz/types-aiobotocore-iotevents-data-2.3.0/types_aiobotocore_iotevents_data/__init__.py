"""
Main interface for iotevents-data service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_iotevents_data import (
        Client,
        IoTEventsDataClient,
    )

    session = get_session()
    async with session.create_client("iotevents-data") as client:
        client: IoTEventsDataClient
        ...

    ```
"""
from .client import IoTEventsDataClient

Client = IoTEventsDataClient


__all__ = ("Client", "IoTEventsDataClient")
