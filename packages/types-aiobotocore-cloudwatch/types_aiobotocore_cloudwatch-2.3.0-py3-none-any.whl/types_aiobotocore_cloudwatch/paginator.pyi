"""
Type annotations for cloudwatch service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_cloudwatch.client import CloudWatchClient
    from types_aiobotocore_cloudwatch.paginator import (
        DescribeAlarmHistoryPaginator,
        DescribeAlarmsPaginator,
        GetMetricDataPaginator,
        ListDashboardsPaginator,
        ListMetricsPaginator,
    )

    session = get_session()
    with session.create_client("cloudwatch") as client:
        client: CloudWatchClient

        describe_alarm_history_paginator: DescribeAlarmHistoryPaginator = client.get_paginator("describe_alarm_history")
        describe_alarms_paginator: DescribeAlarmsPaginator = client.get_paginator("describe_alarms")
        get_metric_data_paginator: GetMetricDataPaginator = client.get_paginator("get_metric_data")
        list_dashboards_paginator: ListDashboardsPaginator = client.get_paginator("list_dashboards")
        list_metrics_paginator: ListMetricsPaginator = client.get_paginator("list_metrics")
    ```
"""
import sys
from datetime import datetime
from typing import Generic, Iterator, Sequence, TypeVar, Union

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .literals import AlarmTypeType, HistoryItemTypeType, ScanByType, StateValueType
from .type_defs import (
    DescribeAlarmHistoryOutputTypeDef,
    DescribeAlarmsOutputTypeDef,
    DimensionFilterTypeDef,
    GetMetricDataOutputTypeDef,
    LabelOptionsTypeDef,
    ListDashboardsOutputTypeDef,
    ListMetricsOutputTypeDef,
    MetricDataQueryTypeDef,
    PaginatorConfigTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import AsyncIterator
else:
    from typing_extensions import AsyncIterator
if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = (
    "DescribeAlarmHistoryPaginator",
    "DescribeAlarmsPaginator",
    "GetMetricDataPaginator",
    "ListDashboardsPaginator",
    "ListMetricsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class DescribeAlarmHistoryPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Paginator.DescribeAlarmHistory)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/paginators/#describealarmhistorypaginator)
    """

    def paginate(
        self,
        *,
        AlarmName: str = ...,
        AlarmTypes: Sequence[AlarmTypeType] = ...,
        HistoryItemType: HistoryItemTypeType = ...,
        StartDate: Union[datetime, str] = ...,
        EndDate: Union[datetime, str] = ...,
        ScanBy: ScanByType = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DescribeAlarmHistoryOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Paginator.DescribeAlarmHistory.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/paginators/#describealarmhistorypaginator)
        """

class DescribeAlarmsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Paginator.DescribeAlarms)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/paginators/#describealarmspaginator)
    """

    def paginate(
        self,
        *,
        AlarmNames: Sequence[str] = ...,
        AlarmNamePrefix: str = ...,
        AlarmTypes: Sequence[AlarmTypeType] = ...,
        ChildrenOfAlarmName: str = ...,
        ParentsOfAlarmName: str = ...,
        StateValue: StateValueType = ...,
        ActionPrefix: str = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DescribeAlarmsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Paginator.DescribeAlarms.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/paginators/#describealarmspaginator)
        """

class GetMetricDataPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Paginator.GetMetricData)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/paginators/#getmetricdatapaginator)
    """

    def paginate(
        self,
        *,
        MetricDataQueries: Sequence["MetricDataQueryTypeDef"],
        StartTime: Union[datetime, str],
        EndTime: Union[datetime, str],
        ScanBy: ScanByType = ...,
        LabelOptions: "LabelOptionsTypeDef" = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[GetMetricDataOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Paginator.GetMetricData.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/paginators/#getmetricdatapaginator)
        """

class ListDashboardsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Paginator.ListDashboards)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/paginators/#listdashboardspaginator)
    """

    def paginate(
        self, *, DashboardNamePrefix: str = ..., PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListDashboardsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Paginator.ListDashboards.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/paginators/#listdashboardspaginator)
        """

class ListMetricsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Paginator.ListMetrics)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/paginators/#listmetricspaginator)
    """

    def paginate(
        self,
        *,
        Namespace: str = ...,
        MetricName: str = ...,
        Dimensions: Sequence["DimensionFilterTypeDef"] = ...,
        RecentlyActive: Literal["PT3H"] = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListMetricsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Paginator.ListMetrics.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/paginators/#listmetricspaginator)
        """
