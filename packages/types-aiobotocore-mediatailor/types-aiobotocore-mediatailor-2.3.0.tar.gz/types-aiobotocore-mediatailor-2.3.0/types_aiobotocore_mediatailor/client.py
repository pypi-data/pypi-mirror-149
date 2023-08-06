"""
Type annotations for mediatailor service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_mediatailor.client import MediaTailorClient

    session = get_session()
    async with session.create_client("mediatailor") as client:
        client: MediaTailorClient
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import PlaybackModeType
from .paginator import (
    GetChannelSchedulePaginator,
    ListAlertsPaginator,
    ListChannelsPaginator,
    ListPlaybackConfigurationsPaginator,
    ListPrefetchSchedulesPaginator,
    ListSourceLocationsPaginator,
    ListVodSourcesPaginator,
)
from .type_defs import (
    AccessConfigurationTypeDef,
    AdBreakTypeDef,
    AvailSuppressionTypeDef,
    BumperTypeDef,
    CdnConfigurationTypeDef,
    ConfigureLogsForPlaybackConfigurationResponseTypeDef,
    CreateChannelResponseTypeDef,
    CreatePrefetchScheduleResponseTypeDef,
    CreateProgramResponseTypeDef,
    CreateSourceLocationResponseTypeDef,
    CreateVodSourceResponseTypeDef,
    DashConfigurationForPutTypeDef,
    DefaultSegmentDeliveryConfigurationTypeDef,
    DescribeChannelResponseTypeDef,
    DescribeProgramResponseTypeDef,
    DescribeSourceLocationResponseTypeDef,
    DescribeVodSourceResponseTypeDef,
    GetChannelPolicyResponseTypeDef,
    GetChannelScheduleResponseTypeDef,
    GetPlaybackConfigurationResponseTypeDef,
    GetPrefetchScheduleResponseTypeDef,
    HttpConfigurationTypeDef,
    HttpPackageConfigurationTypeDef,
    ListAlertsResponseTypeDef,
    ListChannelsResponseTypeDef,
    ListPlaybackConfigurationsResponseTypeDef,
    ListPrefetchSchedulesResponseTypeDef,
    ListSourceLocationsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListVodSourcesResponseTypeDef,
    LivePreRollConfigurationTypeDef,
    ManifestProcessingRulesTypeDef,
    PrefetchConsumptionTypeDef,
    PrefetchRetrievalTypeDef,
    PutPlaybackConfigurationResponseTypeDef,
    RequestOutputItemTypeDef,
    ScheduleConfigurationTypeDef,
    SegmentDeliveryConfigurationTypeDef,
    SlateSourceTypeDef,
    UpdateChannelResponseTypeDef,
    UpdateSourceLocationResponseTypeDef,
    UpdateVodSourceResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("MediaTailorClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]


class MediaTailorClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        MediaTailorClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/client/#can_paginate)
        """

    async def configure_logs_for_playback_configuration(
        self, *, PercentEnabled: int, PlaybackConfigurationName: str
    ) -> ConfigureLogsForPlaybackConfigurationResponseTypeDef:
        """
        Configures Amazon CloudWatch log settings for a playback configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.configure_logs_for_playback_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/client/#configure_logs_for_playback_configuration)
        """

    async def create_channel(
        self,
        *,
        ChannelName: str,
        Outputs: Sequence["RequestOutputItemTypeDef"],
        PlaybackMode: PlaybackModeType,
        FillerSlate: "SlateSourceTypeDef" = ...,
        Tags: Mapping[str, str] = ...
    ) -> CreateChannelResponseTypeDef:
        """
        Creates a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.create_channel)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/client/#create_channel)
        """

    async def create_prefetch_schedule(
        self,
        *,
        Consumption: "PrefetchConsumptionTypeDef",
        Name: str,
        PlaybackConfigurationName: str,
        Retrieval: "PrefetchRetrievalTypeDef",
        StreamId: str = ...
    ) -> CreatePrefetchScheduleResponseTypeDef:
        """
        Creates a new prefetch schedule for the specified playback configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.create_prefetch_schedule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/client/#create_prefetch_schedule)
        """

    async def create_program(
        self,
        *,
        ChannelName: str,
        ProgramName: str,
        ScheduleConfiguration: "ScheduleConfigurationTypeDef",
        SourceLocationName: str,
        VodSourceName: str,
        AdBreaks: Sequence["AdBreakTypeDef"] = ...
    ) -> CreateProgramResponseTypeDef:
        """
        Creates a program.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.create_program)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/client/#create_program)
        """

    async def create_source_location(
        self,
        *,
        HttpConfiguration: "HttpConfigurationTypeDef",
        SourceLocationName: str,
        AccessConfiguration: "AccessConfigurationTypeDef" = ...,
        DefaultSegmentDeliveryConfiguration: "DefaultSegmentDeliveryConfigurationTypeDef" = ...,
        SegmentDeliveryConfigurations: Sequence["SegmentDeliveryConfigurationTypeDef"] = ...,
        Tags: Mapping[str, str] = ...
    ) -> CreateSourceLocationResponseTypeDef:
        """
        Creates a source location on a specific channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.create_source_location)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/client/#create_source_location)
        """

    async def create_vod_source(
        self,
        *,
        HttpPackageConfigurations: Sequence["HttpPackageConfigurationTypeDef"],
        SourceLocationName: str,
        VodSourceName: str,
        Tags: Mapping[str, str] = ...
    ) -> CreateVodSourceResponseTypeDef:
        """
        Creates name for a specific VOD source in a source location.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.create_vod_source)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/client/#create_vod_source)
        """

    async def delete_channel(self, *, ChannelName: str) -> Dict[str, Any]:
        """
        Deletes a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.delete_channel)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/client/#delete_channel)
        """

    async def delete_channel_policy(self, *, ChannelName: str) -> Dict[str, Any]:
        """
        Deletes a channel's IAM policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.delete_channel_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/client/#delete_channel_policy)
        """

    async def delete_playback_configuration(self, *, Name: str) -> Dict[str, Any]:
        """
        Deletes the playback configuration for the specified name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.delete_playback_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/client/#delete_playback_configuration)
        """

    async def delete_prefetch_schedule(
        self, *, Name: str, PlaybackConfigurationName: str
    ) -> Dict[str, Any]:
        """
        Deletes a prefetch schedule for a specific playback configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.delete_prefetch_schedule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/client/#delete_prefetch_schedule)
        """

    async def delete_program(self, *, ChannelName: str, ProgramName: str) -> Dict[str, Any]:
        """
        Deletes a specific program on a specific channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.delete_program)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/client/#delete_program)
        """

    async def delete_source_location(self, *, SourceLocationName: str) -> Dict[str, Any]:
        """
        Deletes a source location on a specific channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.delete_source_location)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/client/#delete_source_location)
        """

    async def delete_vod_source(
        self, *, SourceLocationName: str, VodSourceName: str
    ) -> Dict[str, Any]:
        """
        Deletes a specific VOD source in a specific source location.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.delete_vod_source)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/client/#delete_vod_source)
        """

    async def describe_channel(self, *, ChannelName: str) -> DescribeChannelResponseTypeDef:
        """
        Describes the properties of a specific channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.describe_channel)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/client/#describe_channel)
        """

    async def describe_program(
        self, *, ChannelName: str, ProgramName: str
    ) -> DescribeProgramResponseTypeDef:
        """
        Retrieves the properties of the requested program.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.describe_program)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/client/#describe_program)
        """

    async def describe_source_location(
        self, *, SourceLocationName: str
    ) -> DescribeSourceLocationResponseTypeDef:
        """
        Retrieves the properties of the requested source location.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.describe_source_location)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/client/#describe_source_location)
        """

    async def describe_vod_source(
        self, *, SourceLocationName: str, VodSourceName: str
    ) -> DescribeVodSourceResponseTypeDef:
        """
        Provides details about a specific VOD source in a specific source location.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.describe_vod_source)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/client/#describe_vod_source)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/client/#generate_presigned_url)
        """

    async def get_channel_policy(self, *, ChannelName: str) -> GetChannelPolicyResponseTypeDef:
        """
        Retrieves information about a channel's IAM policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.get_channel_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/client/#get_channel_policy)
        """

    async def get_channel_schedule(
        self,
        *,
        ChannelName: str,
        DurationMinutes: str = ...,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> GetChannelScheduleResponseTypeDef:
        """
        Retrieves information about your channel's schedule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.get_channel_schedule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/client/#get_channel_schedule)
        """

    async def get_playback_configuration(
        self, *, Name: str
    ) -> GetPlaybackConfigurationResponseTypeDef:
        """
        Returns the playback configuration for the specified name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.get_playback_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/client/#get_playback_configuration)
        """

    async def get_prefetch_schedule(
        self, *, Name: str, PlaybackConfigurationName: str
    ) -> GetPrefetchScheduleResponseTypeDef:
        """
        Returns information about the prefetch schedule for a specific playback
        configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.get_prefetch_schedule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/client/#get_prefetch_schedule)
        """

    async def list_alerts(
        self, *, ResourceArn: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListAlertsResponseTypeDef:
        """
        Returns a list of alerts for the given resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.list_alerts)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/client/#list_alerts)
        """

    async def list_channels(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListChannelsResponseTypeDef:
        """
        Retrieves a list of channels that are associated with this account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.list_channels)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/client/#list_channels)
        """

    async def list_playback_configurations(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListPlaybackConfigurationsResponseTypeDef:
        """
        Returns a list of the playback configurations defined in AWS Elemental
        MediaTailor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.list_playback_configurations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/client/#list_playback_configurations)
        """

    async def list_prefetch_schedules(
        self,
        *,
        PlaybackConfigurationName: str,
        MaxResults: int = ...,
        NextToken: str = ...,
        StreamId: str = ...
    ) -> ListPrefetchSchedulesResponseTypeDef:
        """
        Creates a new prefetch schedule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.list_prefetch_schedules)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/client/#list_prefetch_schedules)
        """

    async def list_source_locations(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListSourceLocationsResponseTypeDef:
        """
        Retrieves a list of source locations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.list_source_locations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/client/#list_source_locations)
        """

    async def list_tags_for_resource(
        self, *, ResourceArn: str
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Returns a list of the tags assigned to the specified playback configuration
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/client/#list_tags_for_resource)
        """

    async def list_vod_sources(
        self, *, SourceLocationName: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListVodSourcesResponseTypeDef:
        """
        Lists all the VOD sources in a source location.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.list_vod_sources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/client/#list_vod_sources)
        """

    async def put_channel_policy(self, *, ChannelName: str, Policy: str) -> Dict[str, Any]:
        """
        Creates an IAM policy for the channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.put_channel_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/client/#put_channel_policy)
        """

    async def put_playback_configuration(
        self,
        *,
        AdDecisionServerUrl: str = ...,
        AvailSuppression: "AvailSuppressionTypeDef" = ...,
        Bumper: "BumperTypeDef" = ...,
        CdnConfiguration: "CdnConfigurationTypeDef" = ...,
        ConfigurationAliases: Mapping[str, Mapping[str, str]] = ...,
        DashConfiguration: "DashConfigurationForPutTypeDef" = ...,
        LivePreRollConfiguration: "LivePreRollConfigurationTypeDef" = ...,
        ManifestProcessingRules: "ManifestProcessingRulesTypeDef" = ...,
        Name: str = ...,
        PersonalizationThresholdSeconds: int = ...,
        SlateAdUrl: str = ...,
        Tags: Mapping[str, str] = ...,
        TranscodeProfileName: str = ...,
        VideoContentSourceUrl: str = ...
    ) -> PutPlaybackConfigurationResponseTypeDef:
        """
        Adds a new playback configuration to AWS Elemental MediaTailor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.put_playback_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/client/#put_playback_configuration)
        """

    async def start_channel(self, *, ChannelName: str) -> Dict[str, Any]:
        """
        Starts a specific channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.start_channel)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/client/#start_channel)
        """

    async def stop_channel(self, *, ChannelName: str) -> Dict[str, Any]:
        """
        Stops a specific channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.stop_channel)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/client/#stop_channel)
        """

    async def tag_resource(self, *, ResourceArn: str, Tags: Mapping[str, str]) -> None:
        """
        Adds tags to the specified playback configuration resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/client/#tag_resource)
        """

    async def untag_resource(self, *, ResourceArn: str, TagKeys: Sequence[str]) -> None:
        """
        Removes tags from the specified playback configuration resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/client/#untag_resource)
        """

    async def update_channel(
        self,
        *,
        ChannelName: str,
        Outputs: Sequence["RequestOutputItemTypeDef"],
        FillerSlate: "SlateSourceTypeDef" = ...
    ) -> UpdateChannelResponseTypeDef:
        """
        Updates an existing channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.update_channel)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/client/#update_channel)
        """

    async def update_source_location(
        self,
        *,
        HttpConfiguration: "HttpConfigurationTypeDef",
        SourceLocationName: str,
        AccessConfiguration: "AccessConfigurationTypeDef" = ...,
        DefaultSegmentDeliveryConfiguration: "DefaultSegmentDeliveryConfigurationTypeDef" = ...,
        SegmentDeliveryConfigurations: Sequence["SegmentDeliveryConfigurationTypeDef"] = ...
    ) -> UpdateSourceLocationResponseTypeDef:
        """
        Updates a source location on a specific channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.update_source_location)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/client/#update_source_location)
        """

    async def update_vod_source(
        self,
        *,
        HttpPackageConfigurations: Sequence["HttpPackageConfigurationTypeDef"],
        SourceLocationName: str,
        VodSourceName: str
    ) -> UpdateVodSourceResponseTypeDef:
        """
        Updates a specific VOD source in a specific source location.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.update_vod_source)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/client/#update_vod_source)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_channel_schedule"]
    ) -> GetChannelSchedulePaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_alerts"]) -> ListAlertsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_channels"]) -> ListChannelsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_playback_configurations"]
    ) -> ListPlaybackConfigurationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_prefetch_schedules"]
    ) -> ListPrefetchSchedulesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_source_locations"]
    ) -> ListSourceLocationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_vod_sources"]) -> ListVodSourcesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/client/#get_paginator)
        """

    async def __aenter__(self) -> "MediaTailorClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/client/)
        """
