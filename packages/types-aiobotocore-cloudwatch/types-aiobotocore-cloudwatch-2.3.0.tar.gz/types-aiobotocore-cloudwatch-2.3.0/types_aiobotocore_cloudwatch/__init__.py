"""
Main interface for cloudwatch service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_cloudwatch import (
        AlarmExistsWaiter,
        Client,
        CloudWatchClient,
        CloudWatchServiceResource,
        CompositeAlarmExistsWaiter,
        DescribeAlarmHistoryPaginator,
        DescribeAlarmsPaginator,
        GetMetricDataPaginator,
        ListDashboardsPaginator,
        ListMetricsPaginator,
        ServiceResource,
    )

    session = get_session()
    async with session.create_client("cloudwatch") as client:
        client: CloudWatchClient
        ...


    alarm_exists_waiter: AlarmExistsWaiter = client.get_waiter("alarm_exists")
    composite_alarm_exists_waiter: CompositeAlarmExistsWaiter = client.get_waiter("composite_alarm_exists")

    describe_alarm_history_paginator: DescribeAlarmHistoryPaginator = client.get_paginator("describe_alarm_history")
    describe_alarms_paginator: DescribeAlarmsPaginator = client.get_paginator("describe_alarms")
    get_metric_data_paginator: GetMetricDataPaginator = client.get_paginator("get_metric_data")
    list_dashboards_paginator: ListDashboardsPaginator = client.get_paginator("list_dashboards")
    list_metrics_paginator: ListMetricsPaginator = client.get_paginator("list_metrics")
    ```
"""
from .client import CloudWatchClient
from .paginator import (
    DescribeAlarmHistoryPaginator,
    DescribeAlarmsPaginator,
    GetMetricDataPaginator,
    ListDashboardsPaginator,
    ListMetricsPaginator,
)
from .service_resource import CloudWatchServiceResource
from .waiter import AlarmExistsWaiter, CompositeAlarmExistsWaiter

Client = CloudWatchClient


__all__ = (
    "AlarmExistsWaiter",
    "Client",
    "CloudWatchClient",
    "CloudWatchServiceResource",
    "CompositeAlarmExistsWaiter",
    "DescribeAlarmHistoryPaginator",
    "DescribeAlarmsPaginator",
    "GetMetricDataPaginator",
    "ListDashboardsPaginator",
    "ListMetricsPaginator",
    "ServiceResource",
)
