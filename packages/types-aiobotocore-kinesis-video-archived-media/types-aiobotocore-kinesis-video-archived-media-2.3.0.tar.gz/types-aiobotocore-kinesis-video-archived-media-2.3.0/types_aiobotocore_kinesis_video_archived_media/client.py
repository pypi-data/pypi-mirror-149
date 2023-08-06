"""
Type annotations for kinesis-video-archived-media service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis_video_archived_media/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_kinesis_video_archived_media.client import KinesisVideoArchivedMediaClient

    session = get_session()
    async with session.create_client("kinesis-video-archived-media") as client:
        client: KinesisVideoArchivedMediaClient
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import (
    ContainerFormatType,
    DASHDisplayFragmentNumberType,
    DASHDisplayFragmentTimestampType,
    DASHPlaybackModeType,
    HLSDiscontinuityModeType,
    HLSDisplayFragmentTimestampType,
    HLSPlaybackModeType,
)
from .paginator import ListFragmentsPaginator
from .type_defs import (
    ClipFragmentSelectorTypeDef,
    DASHFragmentSelectorTypeDef,
    FragmentSelectorTypeDef,
    GetClipOutputTypeDef,
    GetDASHStreamingSessionURLOutputTypeDef,
    GetHLSStreamingSessionURLOutputTypeDef,
    GetMediaForFragmentListOutputTypeDef,
    HLSFragmentSelectorTypeDef,
    ListFragmentsOutputTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("KinesisVideoArchivedMediaClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    ClientLimitExceededException: Type[BotocoreClientError]
    InvalidArgumentException: Type[BotocoreClientError]
    InvalidCodecPrivateDataException: Type[BotocoreClientError]
    InvalidMediaFrameException: Type[BotocoreClientError]
    MissingCodecPrivateDataException: Type[BotocoreClientError]
    NoDataRetentionException: Type[BotocoreClientError]
    NotAuthorizedException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    UnsupportedStreamMediaTypeException: Type[BotocoreClientError]


class KinesisVideoArchivedMediaClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-archived-media.html#KinesisVideoArchivedMedia.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis_video_archived_media/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        KinesisVideoArchivedMediaClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-archived-media.html#KinesisVideoArchivedMedia.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis_video_archived_media/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-archived-media.html#KinesisVideoArchivedMedia.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis_video_archived_media/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-archived-media.html#KinesisVideoArchivedMedia.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis_video_archived_media/client/#generate_presigned_url)
        """

    async def get_clip(
        self,
        *,
        ClipFragmentSelector: "ClipFragmentSelectorTypeDef",
        StreamName: str = ...,
        StreamARN: str = ...
    ) -> GetClipOutputTypeDef:
        """
        Downloads an MP4 file (clip) containing the archived, on-demand media from the
        specified video stream over the specified time range.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-archived-media.html#KinesisVideoArchivedMedia.Client.get_clip)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis_video_archived_media/client/#get_clip)
        """

    async def get_dash_streaming_session_url(
        self,
        *,
        StreamName: str = ...,
        StreamARN: str = ...,
        PlaybackMode: DASHPlaybackModeType = ...,
        DisplayFragmentTimestamp: DASHDisplayFragmentTimestampType = ...,
        DisplayFragmentNumber: DASHDisplayFragmentNumberType = ...,
        DASHFragmentSelector: "DASHFragmentSelectorTypeDef" = ...,
        Expires: int = ...,
        MaxManifestFragmentResults: int = ...
    ) -> GetDASHStreamingSessionURLOutputTypeDef:
        """
        Retrieves an MPEG Dynamic Adaptive Streaming over HTTP (DASH) URL for the
        stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-archived-media.html#KinesisVideoArchivedMedia.Client.get_dash_streaming_session_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis_video_archived_media/client/#get_dash_streaming_session_url)
        """

    async def get_hls_streaming_session_url(
        self,
        *,
        StreamName: str = ...,
        StreamARN: str = ...,
        PlaybackMode: HLSPlaybackModeType = ...,
        HLSFragmentSelector: "HLSFragmentSelectorTypeDef" = ...,
        ContainerFormat: ContainerFormatType = ...,
        DiscontinuityMode: HLSDiscontinuityModeType = ...,
        DisplayFragmentTimestamp: HLSDisplayFragmentTimestampType = ...,
        Expires: int = ...,
        MaxMediaPlaylistFragmentResults: int = ...
    ) -> GetHLSStreamingSessionURLOutputTypeDef:
        """
        Retrieves an HTTP Live Streaming (HLS) URL for the stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-archived-media.html#KinesisVideoArchivedMedia.Client.get_hls_streaming_session_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis_video_archived_media/client/#get_hls_streaming_session_url)
        """

    async def get_media_for_fragment_list(
        self, *, Fragments: Sequence[str], StreamName: str = ..., StreamARN: str = ...
    ) -> GetMediaForFragmentListOutputTypeDef:
        """
        Gets media for a list of fragments (specified by fragment number) from the
        archived data in an Amazon Kinesis video stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-archived-media.html#KinesisVideoArchivedMedia.Client.get_media_for_fragment_list)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis_video_archived_media/client/#get_media_for_fragment_list)
        """

    async def list_fragments(
        self,
        *,
        StreamName: str = ...,
        StreamARN: str = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
        FragmentSelector: "FragmentSelectorTypeDef" = ...
    ) -> ListFragmentsOutputTypeDef:
        """
        Returns a list of  Fragment objects from the specified stream and timestamp
        range within the archived data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-archived-media.html#KinesisVideoArchivedMedia.Client.list_fragments)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis_video_archived_media/client/#list_fragments)
        """

    def get_paginator(self, operation_name: Literal["list_fragments"]) -> ListFragmentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-archived-media.html#KinesisVideoArchivedMedia.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis_video_archived_media/client/#get_paginator)
        """

    async def __aenter__(self) -> "KinesisVideoArchivedMediaClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-archived-media.html#KinesisVideoArchivedMedia.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis_video_archived_media/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis-video-archived-media.html#KinesisVideoArchivedMedia.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis_video_archived_media/client/)
        """
