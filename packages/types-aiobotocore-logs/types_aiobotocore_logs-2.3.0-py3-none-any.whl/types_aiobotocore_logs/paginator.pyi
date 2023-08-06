"""
Type annotations for logs service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_logs.client import CloudWatchLogsClient
    from types_aiobotocore_logs.paginator import (
        DescribeDestinationsPaginator,
        DescribeExportTasksPaginator,
        DescribeLogGroupsPaginator,
        DescribeLogStreamsPaginator,
        DescribeMetricFiltersPaginator,
        DescribeQueriesPaginator,
        DescribeResourcePoliciesPaginator,
        DescribeSubscriptionFiltersPaginator,
        FilterLogEventsPaginator,
    )

    session = get_session()
    with session.create_client("logs") as client:
        client: CloudWatchLogsClient

        describe_destinations_paginator: DescribeDestinationsPaginator = client.get_paginator("describe_destinations")
        describe_export_tasks_paginator: DescribeExportTasksPaginator = client.get_paginator("describe_export_tasks")
        describe_log_groups_paginator: DescribeLogGroupsPaginator = client.get_paginator("describe_log_groups")
        describe_log_streams_paginator: DescribeLogStreamsPaginator = client.get_paginator("describe_log_streams")
        describe_metric_filters_paginator: DescribeMetricFiltersPaginator = client.get_paginator("describe_metric_filters")
        describe_queries_paginator: DescribeQueriesPaginator = client.get_paginator("describe_queries")
        describe_resource_policies_paginator: DescribeResourcePoliciesPaginator = client.get_paginator("describe_resource_policies")
        describe_subscription_filters_paginator: DescribeSubscriptionFiltersPaginator = client.get_paginator("describe_subscription_filters")
        filter_log_events_paginator: FilterLogEventsPaginator = client.get_paginator("filter_log_events")
    ```
"""
import sys
from typing import Generic, Iterator, Sequence, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .literals import ExportTaskStatusCodeType, OrderByType, QueryStatusType
from .type_defs import (
    DescribeDestinationsResponseTypeDef,
    DescribeExportTasksResponseTypeDef,
    DescribeLogGroupsResponseTypeDef,
    DescribeLogStreamsResponseTypeDef,
    DescribeMetricFiltersResponseTypeDef,
    DescribeQueriesResponseTypeDef,
    DescribeResourcePoliciesResponseTypeDef,
    DescribeSubscriptionFiltersResponseTypeDef,
    FilterLogEventsResponseTypeDef,
    PaginatorConfigTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import AsyncIterator
else:
    from typing_extensions import AsyncIterator

__all__ = (
    "DescribeDestinationsPaginator",
    "DescribeExportTasksPaginator",
    "DescribeLogGroupsPaginator",
    "DescribeLogStreamsPaginator",
    "DescribeMetricFiltersPaginator",
    "DescribeQueriesPaginator",
    "DescribeResourcePoliciesPaginator",
    "DescribeSubscriptionFiltersPaginator",
    "FilterLogEventsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class DescribeDestinationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Paginator.DescribeDestinations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#describedestinationspaginator)
    """

    def paginate(
        self, *, DestinationNamePrefix: str = ..., PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DescribeDestinationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Paginator.DescribeDestinations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#describedestinationspaginator)
        """

class DescribeExportTasksPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Paginator.DescribeExportTasks)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#describeexporttaskspaginator)
    """

    def paginate(
        self,
        *,
        taskId: str = ...,
        statusCode: ExportTaskStatusCodeType = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DescribeExportTasksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Paginator.DescribeExportTasks.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#describeexporttaskspaginator)
        """

class DescribeLogGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Paginator.DescribeLogGroups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#describeloggroupspaginator)
    """

    def paginate(
        self, *, logGroupNamePrefix: str = ..., PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DescribeLogGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Paginator.DescribeLogGroups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#describeloggroupspaginator)
        """

class DescribeLogStreamsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Paginator.DescribeLogStreams)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#describelogstreamspaginator)
    """

    def paginate(
        self,
        *,
        logGroupName: str,
        logStreamNamePrefix: str = ...,
        orderBy: OrderByType = ...,
        descending: bool = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DescribeLogStreamsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Paginator.DescribeLogStreams.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#describelogstreamspaginator)
        """

class DescribeMetricFiltersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Paginator.DescribeMetricFilters)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#describemetricfilterspaginator)
    """

    def paginate(
        self,
        *,
        logGroupName: str = ...,
        filterNamePrefix: str = ...,
        metricName: str = ...,
        metricNamespace: str = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DescribeMetricFiltersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Paginator.DescribeMetricFilters.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#describemetricfilterspaginator)
        """

class DescribeQueriesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Paginator.DescribeQueries)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#describequeriespaginator)
    """

    def paginate(
        self,
        *,
        logGroupName: str = ...,
        status: QueryStatusType = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DescribeQueriesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Paginator.DescribeQueries.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#describequeriespaginator)
        """

class DescribeResourcePoliciesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Paginator.DescribeResourcePolicies)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#describeresourcepoliciespaginator)
    """

    def paginate(
        self, *, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DescribeResourcePoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Paginator.DescribeResourcePolicies.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#describeresourcepoliciespaginator)
        """

class DescribeSubscriptionFiltersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Paginator.DescribeSubscriptionFilters)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#describesubscriptionfilterspaginator)
    """

    def paginate(
        self,
        *,
        logGroupName: str,
        filterNamePrefix: str = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DescribeSubscriptionFiltersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Paginator.DescribeSubscriptionFilters.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#describesubscriptionfilterspaginator)
        """

class FilterLogEventsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Paginator.FilterLogEvents)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#filterlogeventspaginator)
    """

    def paginate(
        self,
        *,
        logGroupName: str,
        logStreamNames: Sequence[str] = ...,
        logStreamNamePrefix: str = ...,
        startTime: int = ...,
        endTime: int = ...,
        filterPattern: str = ...,
        interleaved: bool = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[FilterLogEventsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Paginator.FilterLogEvents.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#filterlogeventspaginator)
        """
