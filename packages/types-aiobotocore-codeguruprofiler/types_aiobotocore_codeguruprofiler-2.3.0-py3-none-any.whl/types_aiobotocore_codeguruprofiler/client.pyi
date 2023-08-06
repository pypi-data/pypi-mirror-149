"""
Type annotations for codeguruprofiler service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_codeguruprofiler.client import CodeGuruProfilerClient

    session = get_session()
    async with session.create_client("codeguruprofiler") as client:
        client: CodeGuruProfilerClient
    ```
"""
import sys
from datetime import datetime
from typing import IO, Any, Dict, Mapping, Sequence, Type, Union

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.response import StreamingBody

from .literals import (
    AggregationPeriodType,
    ComputePlatformType,
    FeedbackTypeType,
    MetadataFieldType,
    OrderByType,
)
from .paginator import ListProfileTimesPaginator
from .type_defs import (
    AddNotificationChannelsResponseTypeDef,
    AgentOrchestrationConfigTypeDef,
    BatchGetFrameMetricDataResponseTypeDef,
    ChannelTypeDef,
    ConfigureAgentResponseTypeDef,
    CreateProfilingGroupResponseTypeDef,
    DescribeProfilingGroupResponseTypeDef,
    FrameMetricTypeDef,
    GetFindingsReportAccountSummaryResponseTypeDef,
    GetNotificationConfigurationResponseTypeDef,
    GetPolicyResponseTypeDef,
    GetProfileResponseTypeDef,
    GetRecommendationsResponseTypeDef,
    ListFindingsReportsResponseTypeDef,
    ListProfileTimesResponseTypeDef,
    ListProfilingGroupsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    PutPermissionResponseTypeDef,
    RemoveNotificationChannelResponseTypeDef,
    RemovePermissionResponseTypeDef,
    UpdateProfilingGroupResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("CodeGuruProfilerClient",)

class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class CodeGuruProfilerClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CodeGuruProfilerClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#exceptions)
        """
    async def add_notification_channels(
        self, *, channels: Sequence["ChannelTypeDef"], profilingGroupName: str
    ) -> AddNotificationChannelsResponseTypeDef:
        """
        Add up to 2 anomaly notifications channels for a profiling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client.add_notification_channels)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#add_notification_channels)
        """
    async def batch_get_frame_metric_data(
        self,
        *,
        profilingGroupName: str,
        endTime: Union[datetime, str] = ...,
        frameMetrics: Sequence["FrameMetricTypeDef"] = ...,
        period: str = ...,
        startTime: Union[datetime, str] = ...,
        targetResolution: AggregationPeriodType = ...
    ) -> BatchGetFrameMetricDataResponseTypeDef:
        """
        Returns the time series of values for a requested list of frame metrics from a
        time period.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client.batch_get_frame_metric_data)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#batch_get_frame_metric_data)
        """
    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#can_paginate)
        """
    async def configure_agent(
        self,
        *,
        profilingGroupName: str,
        fleetInstanceId: str = ...,
        metadata: Mapping[MetadataFieldType, str] = ...
    ) -> ConfigureAgentResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client.configure_agent)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#configure_agent)
        """
    async def create_profiling_group(
        self,
        *,
        clientToken: str,
        profilingGroupName: str,
        agentOrchestrationConfig: "AgentOrchestrationConfigTypeDef" = ...,
        computePlatform: ComputePlatformType = ...,
        tags: Mapping[str, str] = ...
    ) -> CreateProfilingGroupResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client.create_profiling_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#create_profiling_group)
        """
    async def delete_profiling_group(self, *, profilingGroupName: str) -> Dict[str, Any]:
        """
        Deletes a profiling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client.delete_profiling_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#delete_profiling_group)
        """
    async def describe_profiling_group(
        self, *, profilingGroupName: str
    ) -> DescribeProfilingGroupResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client.describe_profiling_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#describe_profiling_group)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#generate_presigned_url)
        """
    async def get_findings_report_account_summary(
        self, *, dailyReportsOnly: bool = ..., maxResults: int = ..., nextToken: str = ...
    ) -> GetFindingsReportAccountSummaryResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client.get_findings_report_account_summary)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#get_findings_report_account_summary)
        """
    async def get_notification_configuration(
        self, *, profilingGroupName: str
    ) -> GetNotificationConfigurationResponseTypeDef:
        """
        Get the current configuration for anomaly notifications for a profiling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client.get_notification_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#get_notification_configuration)
        """
    async def get_policy(self, *, profilingGroupName: str) -> GetPolicyResponseTypeDef:
        """
        Returns the JSON-formatted resource-based policy on a profiling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client.get_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#get_policy)
        """
    async def get_profile(
        self,
        *,
        profilingGroupName: str,
        accept: str = ...,
        endTime: Union[datetime, str] = ...,
        maxDepth: int = ...,
        period: str = ...,
        startTime: Union[datetime, str] = ...
    ) -> GetProfileResponseTypeDef:
        """
        Gets the aggregated profile of a profiling group for a specified time range.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client.get_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#get_profile)
        """
    async def get_recommendations(
        self,
        *,
        endTime: Union[datetime, str],
        profilingGroupName: str,
        startTime: Union[datetime, str],
        locale: str = ...
    ) -> GetRecommendationsResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client.get_recommendations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#get_recommendations)
        """
    async def list_findings_reports(
        self,
        *,
        endTime: Union[datetime, str],
        profilingGroupName: str,
        startTime: Union[datetime, str],
        dailyReportsOnly: bool = ...,
        maxResults: int = ...,
        nextToken: str = ...
    ) -> ListFindingsReportsResponseTypeDef:
        """
        List the available reports for a given profiling group and time range.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client.list_findings_reports)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#list_findings_reports)
        """
    async def list_profile_times(
        self,
        *,
        endTime: Union[datetime, str],
        period: AggregationPeriodType,
        profilingGroupName: str,
        startTime: Union[datetime, str],
        maxResults: int = ...,
        nextToken: str = ...,
        orderBy: OrderByType = ...
    ) -> ListProfileTimesResponseTypeDef:
        """
        Lists the start times of the available aggregated profiles of a profiling group
        for an aggregation period within the specified time range.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client.list_profile_times)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#list_profile_times)
        """
    async def list_profiling_groups(
        self, *, includeDescription: bool = ..., maxResults: int = ..., nextToken: str = ...
    ) -> ListProfilingGroupsResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client.list_profiling_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#list_profiling_groups)
        """
    async def list_tags_for_resource(
        self, *, resourceArn: str
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Returns a list of the tags that are assigned to a specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#list_tags_for_resource)
        """
    async def post_agent_profile(
        self,
        *,
        agentProfile: Union[str, bytes, IO[Any], StreamingBody],
        contentType: str,
        profilingGroupName: str,
        profileToken: str = ...
    ) -> Dict[str, Any]:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client.post_agent_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#post_agent_profile)
        """
    async def put_permission(
        self,
        *,
        actionGroup: Literal["agentPermissions"],
        principals: Sequence[str],
        profilingGroupName: str,
        revisionId: str = ...
    ) -> PutPermissionResponseTypeDef:
        """
        Adds permissions to a profiling group's resource-based policy that are provided
        using an action group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client.put_permission)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#put_permission)
        """
    async def remove_notification_channel(
        self, *, channelId: str, profilingGroupName: str
    ) -> RemoveNotificationChannelResponseTypeDef:
        """
        Remove one anomaly notifications channel for a profiling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client.remove_notification_channel)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#remove_notification_channel)
        """
    async def remove_permission(
        self, *, actionGroup: Literal["agentPermissions"], profilingGroupName: str, revisionId: str
    ) -> RemovePermissionResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client.remove_permission)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#remove_permission)
        """
    async def submit_feedback(
        self,
        *,
        anomalyInstanceId: str,
        profilingGroupName: str,
        type: FeedbackTypeType,
        comment: str = ...
    ) -> Dict[str, Any]:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client.submit_feedback)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#submit_feedback)
        """
    async def tag_resource(self, *, resourceArn: str, tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Use to assign one or more tags to a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#tag_resource)
        """
    async def untag_resource(self, *, resourceArn: str, tagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Use to remove one or more tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#untag_resource)
        """
    async def update_profiling_group(
        self,
        *,
        agentOrchestrationConfig: "AgentOrchestrationConfigTypeDef",
        profilingGroupName: str
    ) -> UpdateProfilingGroupResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client.update_profiling_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#update_profiling_group)
        """
    def get_paginator(
        self, operation_name: Literal["list_profile_times"]
    ) -> ListProfileTimesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#get_paginator)
        """
    async def __aenter__(self) -> "CodeGuruProfilerClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/)
        """
    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/)
        """
