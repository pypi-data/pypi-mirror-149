"""
Main interface for kinesisvideo service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_kinesisvideo import (
        Client,
        KinesisVideoClient,
        ListSignalingChannelsPaginator,
        ListStreamsPaginator,
    )

    session = get_session()
    async with session.create_client("kinesisvideo") as client:
        client: KinesisVideoClient
        ...


    list_signaling_channels_paginator: ListSignalingChannelsPaginator = client.get_paginator("list_signaling_channels")
    list_streams_paginator: ListStreamsPaginator = client.get_paginator("list_streams")
    ```
"""
from .client import KinesisVideoClient
from .paginator import ListSignalingChannelsPaginator, ListStreamsPaginator

Client = KinesisVideoClient

__all__ = ("Client", "KinesisVideoClient", "ListSignalingChannelsPaginator", "ListStreamsPaginator")
