"""
Type annotations for ivs service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_ivs.client import IVSClient

    session = get_session()
    async with session.create_client("ivs") as client:
        client: IVSClient
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import ChannelLatencyModeType, ChannelTypeType
from .paginator import (
    ListChannelsPaginator,
    ListPlaybackKeyPairsPaginator,
    ListRecordingConfigurationsPaginator,
    ListStreamKeysPaginator,
    ListStreamsPaginator,
)
from .type_defs import (
    BatchGetChannelResponseTypeDef,
    BatchGetStreamKeyResponseTypeDef,
    CreateChannelResponseTypeDef,
    CreateRecordingConfigurationResponseTypeDef,
    CreateStreamKeyResponseTypeDef,
    DestinationConfigurationTypeDef,
    GetChannelResponseTypeDef,
    GetPlaybackKeyPairResponseTypeDef,
    GetRecordingConfigurationResponseTypeDef,
    GetStreamKeyResponseTypeDef,
    GetStreamResponseTypeDef,
    GetStreamSessionResponseTypeDef,
    ImportPlaybackKeyPairResponseTypeDef,
    ListChannelsResponseTypeDef,
    ListPlaybackKeyPairsResponseTypeDef,
    ListRecordingConfigurationsResponseTypeDef,
    ListStreamKeysResponseTypeDef,
    ListStreamSessionsResponseTypeDef,
    ListStreamsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    StreamFiltersTypeDef,
    ThumbnailConfigurationTypeDef,
    UpdateChannelResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("IVSClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ChannelNotBroadcasting: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    PendingVerification: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    StreamUnavailable: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class IVSClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        IVSClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs/client/#exceptions)
        """

    async def batch_get_channel(self, *, arns: Sequence[str]) -> BatchGetChannelResponseTypeDef:
        """
        Performs  GetChannel on multiple ARNs simultaneously.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.batch_get_channel)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs/client/#batch_get_channel)
        """

    async def batch_get_stream_key(
        self, *, arns: Sequence[str]
    ) -> BatchGetStreamKeyResponseTypeDef:
        """
        Performs  GetStreamKey on multiple ARNs simultaneously.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.batch_get_stream_key)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs/client/#batch_get_stream_key)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs/client/#can_paginate)
        """

    async def create_channel(
        self,
        *,
        authorized: bool = ...,
        latencyMode: ChannelLatencyModeType = ...,
        name: str = ...,
        recordingConfigurationArn: str = ...,
        tags: Mapping[str, str] = ...,
        type: ChannelTypeType = ...
    ) -> CreateChannelResponseTypeDef:
        """
        Creates a new channel and an associated stream key to start streaming.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.create_channel)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs/client/#create_channel)
        """

    async def create_recording_configuration(
        self,
        *,
        destinationConfiguration: "DestinationConfigurationTypeDef",
        name: str = ...,
        tags: Mapping[str, str] = ...,
        thumbnailConfiguration: "ThumbnailConfigurationTypeDef" = ...
    ) -> CreateRecordingConfigurationResponseTypeDef:
        """
        Creates a new recording configuration, used to enable recording to Amazon S3.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.create_recording_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs/client/#create_recording_configuration)
        """

    async def create_stream_key(
        self, *, channelArn: str, tags: Mapping[str, str] = ...
    ) -> CreateStreamKeyResponseTypeDef:
        """
        Creates a stream key, used to initiate a stream, for the specified channel ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.create_stream_key)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs/client/#create_stream_key)
        """

    async def delete_channel(self, *, arn: str) -> None:
        """
        Deletes the specified channel and its associated stream keys.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.delete_channel)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs/client/#delete_channel)
        """

    async def delete_playback_key_pair(self, *, arn: str) -> Dict[str, Any]:
        """
        Deletes a specified authorization key pair.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.delete_playback_key_pair)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs/client/#delete_playback_key_pair)
        """

    async def delete_recording_configuration(self, *, arn: str) -> None:
        """
        Deletes the recording configuration for the specified ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.delete_recording_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs/client/#delete_recording_configuration)
        """

    async def delete_stream_key(self, *, arn: str) -> None:
        """
        Deletes the stream key for the specified ARN, so it can no longer be used to
        stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.delete_stream_key)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs/client/#delete_stream_key)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs/client/#generate_presigned_url)
        """

    async def get_channel(self, *, arn: str) -> GetChannelResponseTypeDef:
        """
        Gets the channel configuration for the specified channel ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.get_channel)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs/client/#get_channel)
        """

    async def get_playback_key_pair(self, *, arn: str) -> GetPlaybackKeyPairResponseTypeDef:
        """
        Gets a specified playback authorization key pair and returns the `arn` and
        `fingerprint`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.get_playback_key_pair)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs/client/#get_playback_key_pair)
        """

    async def get_recording_configuration(
        self, *, arn: str
    ) -> GetRecordingConfigurationResponseTypeDef:
        """
        Gets the recording configuration for the specified ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.get_recording_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs/client/#get_recording_configuration)
        """

    async def get_stream(self, *, channelArn: str) -> GetStreamResponseTypeDef:
        """
        Gets information about the active (live) stream on a specified channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.get_stream)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs/client/#get_stream)
        """

    async def get_stream_key(self, *, arn: str) -> GetStreamKeyResponseTypeDef:
        """
        Gets stream-key information for a specified ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.get_stream_key)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs/client/#get_stream_key)
        """

    async def get_stream_session(
        self, *, channelArn: str, streamId: str = ...
    ) -> GetStreamSessionResponseTypeDef:
        """
        Gets metadata on a specified stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.get_stream_session)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs/client/#get_stream_session)
        """

    async def import_playback_key_pair(
        self, *, publicKeyMaterial: str, name: str = ..., tags: Mapping[str, str] = ...
    ) -> ImportPlaybackKeyPairResponseTypeDef:
        """
        Imports the public portion of a new key pair and returns its `arn` and
        `fingerprint`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.import_playback_key_pair)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs/client/#import_playback_key_pair)
        """

    async def list_channels(
        self,
        *,
        filterByName: str = ...,
        filterByRecordingConfigurationArn: str = ...,
        maxResults: int = ...,
        nextToken: str = ...
    ) -> ListChannelsResponseTypeDef:
        """
        Gets summary information about all channels in your account, in the Amazon Web
        Services region where the API request is processed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.list_channels)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs/client/#list_channels)
        """

    async def list_playback_key_pairs(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> ListPlaybackKeyPairsResponseTypeDef:
        """
        Gets summary information about playback key pairs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.list_playback_key_pairs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs/client/#list_playback_key_pairs)
        """

    async def list_recording_configurations(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> ListRecordingConfigurationsResponseTypeDef:
        """
        Gets summary information about all recording configurations in your account, in
        the Amazon Web Services region where the API request is processed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.list_recording_configurations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs/client/#list_recording_configurations)
        """

    async def list_stream_keys(
        self, *, channelArn: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListStreamKeysResponseTypeDef:
        """
        Gets summary information about stream keys for the specified channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.list_stream_keys)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs/client/#list_stream_keys)
        """

    async def list_stream_sessions(
        self, *, channelArn: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListStreamSessionsResponseTypeDef:
        """
        Gets a summary of current and previous streams for a specified channel in your
        account, in the AWS region where the API request is processed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.list_stream_sessions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs/client/#list_stream_sessions)
        """

    async def list_streams(
        self, *, filterBy: "StreamFiltersTypeDef" = ..., maxResults: int = ..., nextToken: str = ...
    ) -> ListStreamsResponseTypeDef:
        """
        Gets summary information about live streams in your account, in the Amazon Web
        Services region where the API request is processed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.list_streams)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs/client/#list_streams)
        """

    async def list_tags_for_resource(
        self, *, resourceArn: str
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Gets information about Amazon Web Services tags for the specified ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs/client/#list_tags_for_resource)
        """

    async def put_metadata(self, *, channelArn: str, metadata: str) -> None:
        """
        Inserts metadata into the active stream of the specified channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.put_metadata)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs/client/#put_metadata)
        """

    async def stop_stream(self, *, channelArn: str) -> Dict[str, Any]:
        """
        Disconnects the incoming RTMPS stream for the specified channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.stop_stream)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs/client/#stop_stream)
        """

    async def tag_resource(self, *, resourceArn: str, tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Adds or updates tags for the Amazon Web Services resource with the specified
        ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs/client/#tag_resource)
        """

    async def untag_resource(self, *, resourceArn: str, tagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes tags from the resource with the specified ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs/client/#untag_resource)
        """

    async def update_channel(
        self,
        *,
        arn: str,
        authorized: bool = ...,
        latencyMode: ChannelLatencyModeType = ...,
        name: str = ...,
        recordingConfigurationArn: str = ...,
        type: ChannelTypeType = ...
    ) -> UpdateChannelResponseTypeDef:
        """
        Updates a channel's configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.update_channel)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs/client/#update_channel)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_channels"]) -> ListChannelsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_playback_key_pairs"]
    ) -> ListPlaybackKeyPairsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_recording_configurations"]
    ) -> ListRecordingConfigurationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_stream_keys"]) -> ListStreamKeysPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_streams"]) -> ListStreamsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs/client/#get_paginator)
        """

    async def __aenter__(self) -> "IVSClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs/client/)
        """
