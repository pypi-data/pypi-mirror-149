"""
Main interface for kinesis-video-archived-media service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_kinesis_video_archived_media import (
        Client,
        KinesisVideoArchivedMediaClient,
        ListFragmentsPaginator,
    )

    session = get_session()
    async with session.create_client("kinesis-video-archived-media") as client:
        client: KinesisVideoArchivedMediaClient
        ...


    list_fragments_paginator: ListFragmentsPaginator = client.get_paginator("list_fragments")
    ```
"""
from .client import KinesisVideoArchivedMediaClient
from .paginator import ListFragmentsPaginator

Client = KinesisVideoArchivedMediaClient

__all__ = ("Client", "KinesisVideoArchivedMediaClient", "ListFragmentsPaginator")
