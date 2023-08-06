"""
Type annotations for cloudwatch service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_cloudwatch.client import CloudWatchClient

    session = get_session()
    async with session.create_client("cloudwatch") as client:
        client: CloudWatchClient
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, Mapping, Sequence, Type, Union, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import (
    AlarmTypeType,
    AnomalyDetectorTypeType,
    ComparisonOperatorType,
    HistoryItemTypeType,
    MetricStreamOutputFormatType,
    ScanByType,
    StandardUnitType,
    StateValueType,
    StatisticType,
)
from .paginator import (
    DescribeAlarmHistoryPaginator,
    DescribeAlarmsPaginator,
    GetMetricDataPaginator,
    ListDashboardsPaginator,
    ListMetricsPaginator,
)
from .type_defs import (
    AnomalyDetectorConfigurationTypeDef,
    DeleteInsightRulesOutputTypeDef,
    DescribeAlarmHistoryOutputTypeDef,
    DescribeAlarmsForMetricOutputTypeDef,
    DescribeAlarmsOutputTypeDef,
    DescribeAnomalyDetectorsOutputTypeDef,
    DescribeInsightRulesOutputTypeDef,
    DimensionFilterTypeDef,
    DimensionTypeDef,
    DisableInsightRulesOutputTypeDef,
    EnableInsightRulesOutputTypeDef,
    GetDashboardOutputTypeDef,
    GetInsightRuleReportOutputTypeDef,
    GetMetricDataOutputTypeDef,
    GetMetricStatisticsOutputTypeDef,
    GetMetricStreamOutputTypeDef,
    GetMetricWidgetImageOutputTypeDef,
    LabelOptionsTypeDef,
    ListDashboardsOutputTypeDef,
    ListMetricsOutputTypeDef,
    ListMetricStreamsOutputTypeDef,
    ListTagsForResourceOutputTypeDef,
    MetricDataQueryTypeDef,
    MetricDatumTypeDef,
    MetricMathAnomalyDetectorTypeDef,
    MetricStreamFilterTypeDef,
    PutDashboardOutputTypeDef,
    PutMetricStreamOutputTypeDef,
    SingleMetricAnomalyDetectorTypeDef,
    TagTypeDef,
)
from .waiter import AlarmExistsWaiter, CompositeAlarmExistsWaiter

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("CloudWatchClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    ConcurrentModificationException: Type[BotocoreClientError]
    DashboardInvalidInputError: Type[BotocoreClientError]
    DashboardNotFoundError: Type[BotocoreClientError]
    InternalServiceFault: Type[BotocoreClientError]
    InvalidFormatFault: Type[BotocoreClientError]
    InvalidNextToken: Type[BotocoreClientError]
    InvalidParameterCombinationException: Type[BotocoreClientError]
    InvalidParameterValueException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    LimitExceededFault: Type[BotocoreClientError]
    MissingRequiredParameterException: Type[BotocoreClientError]
    ResourceNotFound: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]


class CloudWatchClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CloudWatchClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/client/#can_paginate)
        """

    async def delete_alarms(self, *, AlarmNames: Sequence[str]) -> None:
        """
        Deletes the specified alarms.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.delete_alarms)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/client/#delete_alarms)
        """

    async def delete_anomaly_detector(
        self,
        *,
        Namespace: str = ...,
        MetricName: str = ...,
        Dimensions: Sequence["DimensionTypeDef"] = ...,
        Stat: str = ...,
        SingleMetricAnomalyDetector: "SingleMetricAnomalyDetectorTypeDef" = ...,
        MetricMathAnomalyDetector: "MetricMathAnomalyDetectorTypeDef" = ...
    ) -> Dict[str, Any]:
        """
        Deletes the specified anomaly detection model from your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.delete_anomaly_detector)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/client/#delete_anomaly_detector)
        """

    async def delete_dashboards(self, *, DashboardNames: Sequence[str]) -> Dict[str, Any]:
        """
        Deletes all dashboards that you specify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.delete_dashboards)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/client/#delete_dashboards)
        """

    async def delete_insight_rules(
        self, *, RuleNames: Sequence[str]
    ) -> DeleteInsightRulesOutputTypeDef:
        """
        Permanently deletes the specified Contributor Insights rules.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.delete_insight_rules)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/client/#delete_insight_rules)
        """

    async def delete_metric_stream(self, *, Name: str) -> Dict[str, Any]:
        """
        Permanently deletes the metric stream that you specify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.delete_metric_stream)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/client/#delete_metric_stream)
        """

    async def describe_alarm_history(
        self,
        *,
        AlarmName: str = ...,
        AlarmTypes: Sequence[AlarmTypeType] = ...,
        HistoryItemType: HistoryItemTypeType = ...,
        StartDate: Union[datetime, str] = ...,
        EndDate: Union[datetime, str] = ...,
        MaxRecords: int = ...,
        NextToken: str = ...,
        ScanBy: ScanByType = ...
    ) -> DescribeAlarmHistoryOutputTypeDef:
        """
        Retrieves the history for the specified alarm.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.describe_alarm_history)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/client/#describe_alarm_history)
        """

    async def describe_alarms(
        self,
        *,
        AlarmNames: Sequence[str] = ...,
        AlarmNamePrefix: str = ...,
        AlarmTypes: Sequence[AlarmTypeType] = ...,
        ChildrenOfAlarmName: str = ...,
        ParentsOfAlarmName: str = ...,
        StateValue: StateValueType = ...,
        ActionPrefix: str = ...,
        MaxRecords: int = ...,
        NextToken: str = ...
    ) -> DescribeAlarmsOutputTypeDef:
        """
        Retrieves the specified alarms.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.describe_alarms)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/client/#describe_alarms)
        """

    async def describe_alarms_for_metric(
        self,
        *,
        MetricName: str,
        Namespace: str,
        Statistic: StatisticType = ...,
        ExtendedStatistic: str = ...,
        Dimensions: Sequence["DimensionTypeDef"] = ...,
        Period: int = ...,
        Unit: StandardUnitType = ...
    ) -> DescribeAlarmsForMetricOutputTypeDef:
        """
        Retrieves the alarms for the specified metric.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.describe_alarms_for_metric)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/client/#describe_alarms_for_metric)
        """

    async def describe_anomaly_detectors(
        self,
        *,
        NextToken: str = ...,
        MaxResults: int = ...,
        Namespace: str = ...,
        MetricName: str = ...,
        Dimensions: Sequence["DimensionTypeDef"] = ...,
        AnomalyDetectorTypes: Sequence[AnomalyDetectorTypeType] = ...
    ) -> DescribeAnomalyDetectorsOutputTypeDef:
        """
        Lists the anomaly detection models that you have created in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.describe_anomaly_detectors)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/client/#describe_anomaly_detectors)
        """

    async def describe_insight_rules(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> DescribeInsightRulesOutputTypeDef:
        """
        Returns a list of all the Contributor Insights rules in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.describe_insight_rules)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/client/#describe_insight_rules)
        """

    async def disable_alarm_actions(self, *, AlarmNames: Sequence[str]) -> None:
        """
        Disables the actions for the specified alarms.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.disable_alarm_actions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/client/#disable_alarm_actions)
        """

    async def disable_insight_rules(
        self, *, RuleNames: Sequence[str]
    ) -> DisableInsightRulesOutputTypeDef:
        """
        Disables the specified Contributor Insights rules.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.disable_insight_rules)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/client/#disable_insight_rules)
        """

    async def enable_alarm_actions(self, *, AlarmNames: Sequence[str]) -> None:
        """
        Enables the actions for the specified alarms.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.enable_alarm_actions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/client/#enable_alarm_actions)
        """

    async def enable_insight_rules(
        self, *, RuleNames: Sequence[str]
    ) -> EnableInsightRulesOutputTypeDef:
        """
        Enables the specified Contributor Insights rules.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.enable_insight_rules)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/client/#enable_insight_rules)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/client/#generate_presigned_url)
        """

    async def get_dashboard(self, *, DashboardName: str) -> GetDashboardOutputTypeDef:
        """
        Displays the details of the dashboard that you specify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.get_dashboard)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/client/#get_dashboard)
        """

    async def get_insight_rule_report(
        self,
        *,
        RuleName: str,
        StartTime: Union[datetime, str],
        EndTime: Union[datetime, str],
        Period: int,
        MaxContributorCount: int = ...,
        Metrics: Sequence[str] = ...,
        OrderBy: str = ...
    ) -> GetInsightRuleReportOutputTypeDef:
        """
        This operation returns the time series data collected by a Contributor Insights
        rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.get_insight_rule_report)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/client/#get_insight_rule_report)
        """

    async def get_metric_data(
        self,
        *,
        MetricDataQueries: Sequence["MetricDataQueryTypeDef"],
        StartTime: Union[datetime, str],
        EndTime: Union[datetime, str],
        NextToken: str = ...,
        ScanBy: ScanByType = ...,
        MaxDatapoints: int = ...,
        LabelOptions: "LabelOptionsTypeDef" = ...
    ) -> GetMetricDataOutputTypeDef:
        """
        You can use the `GetMetricData` API to retrieve as many as 500 different metrics
        in a single request, with a total of as many as 100,800 data points.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.get_metric_data)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/client/#get_metric_data)
        """

    async def get_metric_statistics(
        self,
        *,
        Namespace: str,
        MetricName: str,
        StartTime: Union[datetime, str],
        EndTime: Union[datetime, str],
        Period: int,
        Dimensions: Sequence["DimensionTypeDef"] = ...,
        Statistics: Sequence[StatisticType] = ...,
        ExtendedStatistics: Sequence[str] = ...,
        Unit: StandardUnitType = ...
    ) -> GetMetricStatisticsOutputTypeDef:
        """
        Gets statistics for the specified metric.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.get_metric_statistics)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/client/#get_metric_statistics)
        """

    async def get_metric_stream(self, *, Name: str) -> GetMetricStreamOutputTypeDef:
        """
        Returns information about the metric stream that you specify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.get_metric_stream)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/client/#get_metric_stream)
        """

    async def get_metric_widget_image(
        self, *, MetricWidget: str, OutputFormat: str = ...
    ) -> GetMetricWidgetImageOutputTypeDef:
        """
        You can use the `GetMetricWidgetImage` API to retrieve a snapshot graph of one
        or more Amazon CloudWatch metrics as a bitmap image.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.get_metric_widget_image)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/client/#get_metric_widget_image)
        """

    async def list_dashboards(
        self, *, DashboardNamePrefix: str = ..., NextToken: str = ...
    ) -> ListDashboardsOutputTypeDef:
        """
        Returns a list of the dashboards for your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.list_dashboards)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/client/#list_dashboards)
        """

    async def list_metric_streams(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> ListMetricStreamsOutputTypeDef:
        """
        Returns a list of metric streams in this account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.list_metric_streams)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/client/#list_metric_streams)
        """

    async def list_metrics(
        self,
        *,
        Namespace: str = ...,
        MetricName: str = ...,
        Dimensions: Sequence["DimensionFilterTypeDef"] = ...,
        NextToken: str = ...,
        RecentlyActive: Literal["PT3H"] = ...
    ) -> ListMetricsOutputTypeDef:
        """
        List the specified metrics.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.list_metrics)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/client/#list_metrics)
        """

    async def list_tags_for_resource(self, *, ResourceARN: str) -> ListTagsForResourceOutputTypeDef:
        """
        Displays the tags associated with a CloudWatch resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/client/#list_tags_for_resource)
        """

    async def put_anomaly_detector(
        self,
        *,
        Namespace: str = ...,
        MetricName: str = ...,
        Dimensions: Sequence["DimensionTypeDef"] = ...,
        Stat: str = ...,
        Configuration: "AnomalyDetectorConfigurationTypeDef" = ...,
        SingleMetricAnomalyDetector: "SingleMetricAnomalyDetectorTypeDef" = ...,
        MetricMathAnomalyDetector: "MetricMathAnomalyDetectorTypeDef" = ...
    ) -> Dict[str, Any]:
        """
        Creates an anomaly detection model for a CloudWatch metric.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.put_anomaly_detector)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/client/#put_anomaly_detector)
        """

    async def put_composite_alarm(
        self,
        *,
        AlarmName: str,
        AlarmRule: str,
        ActionsEnabled: bool = ...,
        AlarmActions: Sequence[str] = ...,
        AlarmDescription: str = ...,
        InsufficientDataActions: Sequence[str] = ...,
        OKActions: Sequence[str] = ...,
        Tags: Sequence["TagTypeDef"] = ...
    ) -> None:
        """
        Creates or updates a *composite alarm*.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.put_composite_alarm)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/client/#put_composite_alarm)
        """

    async def put_dashboard(
        self, *, DashboardName: str, DashboardBody: str
    ) -> PutDashboardOutputTypeDef:
        """
        Creates a dashboard if it does not already exist, or updates an existing
        dashboard.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.put_dashboard)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/client/#put_dashboard)
        """

    async def put_insight_rule(
        self,
        *,
        RuleName: str,
        RuleDefinition: str,
        RuleState: str = ...,
        Tags: Sequence["TagTypeDef"] = ...
    ) -> Dict[str, Any]:
        """
        Creates a Contributor Insights rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.put_insight_rule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/client/#put_insight_rule)
        """

    async def put_metric_alarm(
        self,
        *,
        AlarmName: str,
        EvaluationPeriods: int,
        ComparisonOperator: ComparisonOperatorType,
        AlarmDescription: str = ...,
        ActionsEnabled: bool = ...,
        OKActions: Sequence[str] = ...,
        AlarmActions: Sequence[str] = ...,
        InsufficientDataActions: Sequence[str] = ...,
        MetricName: str = ...,
        Namespace: str = ...,
        Statistic: StatisticType = ...,
        ExtendedStatistic: str = ...,
        Dimensions: Sequence["DimensionTypeDef"] = ...,
        Period: int = ...,
        Unit: StandardUnitType = ...,
        DatapointsToAlarm: int = ...,
        Threshold: float = ...,
        TreatMissingData: str = ...,
        EvaluateLowSampleCountPercentile: str = ...,
        Metrics: Sequence["MetricDataQueryTypeDef"] = ...,
        Tags: Sequence["TagTypeDef"] = ...,
        ThresholdMetricId: str = ...
    ) -> None:
        """
        Creates or updates an alarm and associates it with the specified metric, metric
        math expression, or anomaly detection model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.put_metric_alarm)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/client/#put_metric_alarm)
        """

    async def put_metric_data(
        self, *, Namespace: str, MetricData: Sequence["MetricDatumTypeDef"]
    ) -> None:
        """
        Publishes metric data points to Amazon CloudWatch.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.put_metric_data)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/client/#put_metric_data)
        """

    async def put_metric_stream(
        self,
        *,
        Name: str,
        FirehoseArn: str,
        RoleArn: str,
        OutputFormat: MetricStreamOutputFormatType,
        IncludeFilters: Sequence["MetricStreamFilterTypeDef"] = ...,
        ExcludeFilters: Sequence["MetricStreamFilterTypeDef"] = ...,
        Tags: Sequence["TagTypeDef"] = ...
    ) -> PutMetricStreamOutputTypeDef:
        """
        Creates or updates a metric stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.put_metric_stream)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/client/#put_metric_stream)
        """

    async def set_alarm_state(
        self,
        *,
        AlarmName: str,
        StateValue: StateValueType,
        StateReason: str,
        StateReasonData: str = ...
    ) -> None:
        """
        Temporarily sets the state of an alarm for testing purposes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.set_alarm_state)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/client/#set_alarm_state)
        """

    async def start_metric_streams(self, *, Names: Sequence[str]) -> Dict[str, Any]:
        """
        Starts the streaming of metrics for one or more of your metric streams.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.start_metric_streams)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/client/#start_metric_streams)
        """

    async def stop_metric_streams(self, *, Names: Sequence[str]) -> Dict[str, Any]:
        """
        Stops the streaming of metrics for one or more of your metric streams.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.stop_metric_streams)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/client/#stop_metric_streams)
        """

    async def tag_resource(
        self, *, ResourceARN: str, Tags: Sequence["TagTypeDef"]
    ) -> Dict[str, Any]:
        """
        Assigns one or more tags (key-value pairs) to the specified CloudWatch resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/client/#tag_resource)
        """

    async def untag_resource(self, *, ResourceARN: str, TagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes one or more tags from the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/client/#untag_resource)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_alarm_history"]
    ) -> DescribeAlarmHistoryPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["describe_alarms"]) -> DescribeAlarmsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_metric_data"]) -> GetMetricDataPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_dashboards"]) -> ListDashboardsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_metrics"]) -> ListMetricsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/client/#get_paginator)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["alarm_exists"]) -> AlarmExistsWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["composite_alarm_exists"]
    ) -> CompositeAlarmExistsWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/client/#get_waiter)
        """

    async def __aenter__(self) -> "CloudWatchClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/client/)
        """
