"""
Type annotations for devops-guru service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/type_defs/)

Usage::

    ```python
    from types_aiobotocore_devops_guru.type_defs import AccountHealthTypeDef

    data: AccountHealthTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence, Union

from .literals import (
    AnomalySeverityType,
    AnomalyStatusType,
    AnomalyTypeType,
    CloudWatchMetricDataStatusCodeType,
    CloudWatchMetricsStatType,
    CostEstimationServiceResourceStateType,
    CostEstimationStatusType,
    EventClassType,
    EventDataSourceType,
    EventSourceOptInStatusType,
    InsightFeedbackOptionType,
    InsightSeverityType,
    InsightStatusType,
    InsightTypeType,
    LocaleType,
    OptInStatusType,
    OrganizationResourceCollectionTypeType,
    ResourceCollectionTypeType,
    ServiceNameType,
    UpdateResourceCollectionActionType,
)

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "AccountHealthTypeDef",
    "AccountInsightHealthTypeDef",
    "AddNotificationChannelRequestRequestTypeDef",
    "AddNotificationChannelResponseTypeDef",
    "AmazonCodeGuruProfilerIntegrationTypeDef",
    "AnomalyReportedTimeRangeTypeDef",
    "AnomalyResourceTypeDef",
    "AnomalySourceDetailsTypeDef",
    "AnomalySourceMetadataTypeDef",
    "AnomalyTimeRangeTypeDef",
    "CloudFormationCollectionFilterTypeDef",
    "CloudFormationCollectionTypeDef",
    "CloudFormationCostEstimationResourceCollectionFilterTypeDef",
    "CloudFormationHealthTypeDef",
    "CloudWatchMetricsDataSummaryTypeDef",
    "CloudWatchMetricsDetailTypeDef",
    "CloudWatchMetricsDimensionTypeDef",
    "CostEstimationResourceCollectionFilterTypeDef",
    "CostEstimationTimeRangeTypeDef",
    "DescribeAccountHealthResponseTypeDef",
    "DescribeAccountOverviewRequestRequestTypeDef",
    "DescribeAccountOverviewResponseTypeDef",
    "DescribeAnomalyRequestRequestTypeDef",
    "DescribeAnomalyResponseTypeDef",
    "DescribeEventSourcesConfigResponseTypeDef",
    "DescribeFeedbackRequestRequestTypeDef",
    "DescribeFeedbackResponseTypeDef",
    "DescribeInsightRequestRequestTypeDef",
    "DescribeInsightResponseTypeDef",
    "DescribeOrganizationHealthRequestRequestTypeDef",
    "DescribeOrganizationHealthResponseTypeDef",
    "DescribeOrganizationOverviewRequestRequestTypeDef",
    "DescribeOrganizationOverviewResponseTypeDef",
    "DescribeOrganizationResourceCollectionHealthRequestDescribeOrganizationResourceCollectionHealthPaginateTypeDef",
    "DescribeOrganizationResourceCollectionHealthRequestRequestTypeDef",
    "DescribeOrganizationResourceCollectionHealthResponseTypeDef",
    "DescribeResourceCollectionHealthRequestDescribeResourceCollectionHealthPaginateTypeDef",
    "DescribeResourceCollectionHealthRequestRequestTypeDef",
    "DescribeResourceCollectionHealthResponseTypeDef",
    "DescribeServiceIntegrationResponseTypeDef",
    "EndTimeRangeTypeDef",
    "EventResourceTypeDef",
    "EventSourcesConfigTypeDef",
    "EventTimeRangeTypeDef",
    "EventTypeDef",
    "GetCostEstimationRequestGetCostEstimationPaginateTypeDef",
    "GetCostEstimationRequestRequestTypeDef",
    "GetCostEstimationResponseTypeDef",
    "GetResourceCollectionRequestGetResourceCollectionPaginateTypeDef",
    "GetResourceCollectionRequestRequestTypeDef",
    "GetResourceCollectionResponseTypeDef",
    "InsightFeedbackTypeDef",
    "InsightHealthTypeDef",
    "InsightTimeRangeTypeDef",
    "ListAnomaliesForInsightRequestListAnomaliesForInsightPaginateTypeDef",
    "ListAnomaliesForInsightRequestRequestTypeDef",
    "ListAnomaliesForInsightResponseTypeDef",
    "ListEventsFiltersTypeDef",
    "ListEventsRequestListEventsPaginateTypeDef",
    "ListEventsRequestRequestTypeDef",
    "ListEventsResponseTypeDef",
    "ListInsightsAnyStatusFilterTypeDef",
    "ListInsightsClosedStatusFilterTypeDef",
    "ListInsightsOngoingStatusFilterTypeDef",
    "ListInsightsRequestListInsightsPaginateTypeDef",
    "ListInsightsRequestRequestTypeDef",
    "ListInsightsResponseTypeDef",
    "ListInsightsStatusFilterTypeDef",
    "ListNotificationChannelsRequestListNotificationChannelsPaginateTypeDef",
    "ListNotificationChannelsRequestRequestTypeDef",
    "ListNotificationChannelsResponseTypeDef",
    "ListOrganizationInsightsRequestListOrganizationInsightsPaginateTypeDef",
    "ListOrganizationInsightsRequestRequestTypeDef",
    "ListOrganizationInsightsResponseTypeDef",
    "ListRecommendationsRequestListRecommendationsPaginateTypeDef",
    "ListRecommendationsRequestRequestTypeDef",
    "ListRecommendationsResponseTypeDef",
    "NotificationChannelConfigTypeDef",
    "NotificationChannelTypeDef",
    "OpsCenterIntegrationConfigTypeDef",
    "OpsCenterIntegrationTypeDef",
    "PaginatorConfigTypeDef",
    "PerformanceInsightsMetricDimensionGroupTypeDef",
    "PerformanceInsightsMetricQueryTypeDef",
    "PerformanceInsightsMetricsDetailTypeDef",
    "PerformanceInsightsReferenceComparisonValuesTypeDef",
    "PerformanceInsightsReferenceDataTypeDef",
    "PerformanceInsightsReferenceMetricTypeDef",
    "PerformanceInsightsReferenceScalarTypeDef",
    "PerformanceInsightsStatTypeDef",
    "PredictionTimeRangeTypeDef",
    "ProactiveAnomalySummaryTypeDef",
    "ProactiveAnomalyTypeDef",
    "ProactiveInsightSummaryTypeDef",
    "ProactiveInsightTypeDef",
    "ProactiveOrganizationInsightSummaryTypeDef",
    "PutFeedbackRequestRequestTypeDef",
    "ReactiveAnomalySummaryTypeDef",
    "ReactiveAnomalyTypeDef",
    "ReactiveInsightSummaryTypeDef",
    "ReactiveInsightTypeDef",
    "ReactiveOrganizationInsightSummaryTypeDef",
    "RecommendationRelatedAnomalyResourceTypeDef",
    "RecommendationRelatedAnomalySourceDetailTypeDef",
    "RecommendationRelatedAnomalyTypeDef",
    "RecommendationRelatedCloudWatchMetricsSourceDetailTypeDef",
    "RecommendationRelatedEventResourceTypeDef",
    "RecommendationRelatedEventTypeDef",
    "RecommendationTypeDef",
    "RemoveNotificationChannelRequestRequestTypeDef",
    "ResourceCollectionFilterTypeDef",
    "ResourceCollectionTypeDef",
    "ResponseMetadataTypeDef",
    "SearchInsightsFiltersTypeDef",
    "SearchInsightsRequestRequestTypeDef",
    "SearchInsightsRequestSearchInsightsPaginateTypeDef",
    "SearchInsightsResponseTypeDef",
    "SearchOrganizationInsightsFiltersTypeDef",
    "SearchOrganizationInsightsRequestRequestTypeDef",
    "SearchOrganizationInsightsRequestSearchOrganizationInsightsPaginateTypeDef",
    "SearchOrganizationInsightsResponseTypeDef",
    "ServiceCollectionTypeDef",
    "ServiceHealthTypeDef",
    "ServiceInsightHealthTypeDef",
    "ServiceIntegrationConfigTypeDef",
    "ServiceResourceCostTypeDef",
    "SnsChannelConfigTypeDef",
    "StartCostEstimationRequestRequestTypeDef",
    "StartTimeRangeTypeDef",
    "TagCollectionFilterTypeDef",
    "TagCollectionTypeDef",
    "TagCostEstimationResourceCollectionFilterTypeDef",
    "TagHealthTypeDef",
    "TimestampMetricValuePairTypeDef",
    "UpdateCloudFormationCollectionFilterTypeDef",
    "UpdateEventSourcesConfigRequestRequestTypeDef",
    "UpdateResourceCollectionFilterTypeDef",
    "UpdateResourceCollectionRequestRequestTypeDef",
    "UpdateServiceIntegrationConfigTypeDef",
    "UpdateServiceIntegrationRequestRequestTypeDef",
    "UpdateTagCollectionFilterTypeDef",
)

AccountHealthTypeDef = TypedDict(
    "AccountHealthTypeDef",
    {
        "AccountId": str,
        "Insight": "AccountInsightHealthTypeDef",
    },
    total=False,
)

AccountInsightHealthTypeDef = TypedDict(
    "AccountInsightHealthTypeDef",
    {
        "OpenProactiveInsights": int,
        "OpenReactiveInsights": int,
    },
    total=False,
)

AddNotificationChannelRequestRequestTypeDef = TypedDict(
    "AddNotificationChannelRequestRequestTypeDef",
    {
        "Config": "NotificationChannelConfigTypeDef",
    },
)

AddNotificationChannelResponseTypeDef = TypedDict(
    "AddNotificationChannelResponseTypeDef",
    {
        "Id": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

AmazonCodeGuruProfilerIntegrationTypeDef = TypedDict(
    "AmazonCodeGuruProfilerIntegrationTypeDef",
    {
        "Status": EventSourceOptInStatusType,
    },
    total=False,
)

_RequiredAnomalyReportedTimeRangeTypeDef = TypedDict(
    "_RequiredAnomalyReportedTimeRangeTypeDef",
    {
        "OpenTime": datetime,
    },
)
_OptionalAnomalyReportedTimeRangeTypeDef = TypedDict(
    "_OptionalAnomalyReportedTimeRangeTypeDef",
    {
        "CloseTime": datetime,
    },
    total=False,
)


class AnomalyReportedTimeRangeTypeDef(
    _RequiredAnomalyReportedTimeRangeTypeDef, _OptionalAnomalyReportedTimeRangeTypeDef
):
    pass


AnomalyResourceTypeDef = TypedDict(
    "AnomalyResourceTypeDef",
    {
        "Name": str,
        "Type": str,
    },
    total=False,
)

AnomalySourceDetailsTypeDef = TypedDict(
    "AnomalySourceDetailsTypeDef",
    {
        "CloudWatchMetrics": List["CloudWatchMetricsDetailTypeDef"],
        "PerformanceInsightsMetrics": List["PerformanceInsightsMetricsDetailTypeDef"],
    },
    total=False,
)

AnomalySourceMetadataTypeDef = TypedDict(
    "AnomalySourceMetadataTypeDef",
    {
        "Source": str,
        "SourceResourceName": str,
        "SourceResourceType": str,
    },
    total=False,
)

_RequiredAnomalyTimeRangeTypeDef = TypedDict(
    "_RequiredAnomalyTimeRangeTypeDef",
    {
        "StartTime": datetime,
    },
)
_OptionalAnomalyTimeRangeTypeDef = TypedDict(
    "_OptionalAnomalyTimeRangeTypeDef",
    {
        "EndTime": datetime,
    },
    total=False,
)


class AnomalyTimeRangeTypeDef(_RequiredAnomalyTimeRangeTypeDef, _OptionalAnomalyTimeRangeTypeDef):
    pass


CloudFormationCollectionFilterTypeDef = TypedDict(
    "CloudFormationCollectionFilterTypeDef",
    {
        "StackNames": List[str],
    },
    total=False,
)

CloudFormationCollectionTypeDef = TypedDict(
    "CloudFormationCollectionTypeDef",
    {
        "StackNames": List[str],
    },
    total=False,
)

CloudFormationCostEstimationResourceCollectionFilterTypeDef = TypedDict(
    "CloudFormationCostEstimationResourceCollectionFilterTypeDef",
    {
        "StackNames": List[str],
    },
    total=False,
)

CloudFormationHealthTypeDef = TypedDict(
    "CloudFormationHealthTypeDef",
    {
        "StackName": str,
        "Insight": "InsightHealthTypeDef",
    },
    total=False,
)

CloudWatchMetricsDataSummaryTypeDef = TypedDict(
    "CloudWatchMetricsDataSummaryTypeDef",
    {
        "TimestampMetricValuePairList": List["TimestampMetricValuePairTypeDef"],
        "StatusCode": CloudWatchMetricDataStatusCodeType,
    },
    total=False,
)

CloudWatchMetricsDetailTypeDef = TypedDict(
    "CloudWatchMetricsDetailTypeDef",
    {
        "MetricName": str,
        "Namespace": str,
        "Dimensions": List["CloudWatchMetricsDimensionTypeDef"],
        "Stat": CloudWatchMetricsStatType,
        "Unit": str,
        "Period": int,
        "MetricDataSummary": "CloudWatchMetricsDataSummaryTypeDef",
    },
    total=False,
)

CloudWatchMetricsDimensionTypeDef = TypedDict(
    "CloudWatchMetricsDimensionTypeDef",
    {
        "Name": str,
        "Value": str,
    },
    total=False,
)

CostEstimationResourceCollectionFilterTypeDef = TypedDict(
    "CostEstimationResourceCollectionFilterTypeDef",
    {
        "CloudFormation": "CloudFormationCostEstimationResourceCollectionFilterTypeDef",
        "Tags": List["TagCostEstimationResourceCollectionFilterTypeDef"],
    },
    total=False,
)

CostEstimationTimeRangeTypeDef = TypedDict(
    "CostEstimationTimeRangeTypeDef",
    {
        "StartTime": datetime,
        "EndTime": datetime,
    },
    total=False,
)

DescribeAccountHealthResponseTypeDef = TypedDict(
    "DescribeAccountHealthResponseTypeDef",
    {
        "OpenReactiveInsights": int,
        "OpenProactiveInsights": int,
        "MetricsAnalyzed": int,
        "ResourceHours": int,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredDescribeAccountOverviewRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeAccountOverviewRequestRequestTypeDef",
    {
        "FromTime": Union[datetime, str],
    },
)
_OptionalDescribeAccountOverviewRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeAccountOverviewRequestRequestTypeDef",
    {
        "ToTime": Union[datetime, str],
    },
    total=False,
)


class DescribeAccountOverviewRequestRequestTypeDef(
    _RequiredDescribeAccountOverviewRequestRequestTypeDef,
    _OptionalDescribeAccountOverviewRequestRequestTypeDef,
):
    pass


DescribeAccountOverviewResponseTypeDef = TypedDict(
    "DescribeAccountOverviewResponseTypeDef",
    {
        "ReactiveInsights": int,
        "ProactiveInsights": int,
        "MeanTimeToRecoverInMilliseconds": int,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredDescribeAnomalyRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeAnomalyRequestRequestTypeDef",
    {
        "Id": str,
    },
)
_OptionalDescribeAnomalyRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeAnomalyRequestRequestTypeDef",
    {
        "AccountId": str,
    },
    total=False,
)


class DescribeAnomalyRequestRequestTypeDef(
    _RequiredDescribeAnomalyRequestRequestTypeDef, _OptionalDescribeAnomalyRequestRequestTypeDef
):
    pass


DescribeAnomalyResponseTypeDef = TypedDict(
    "DescribeAnomalyResponseTypeDef",
    {
        "ProactiveAnomaly": "ProactiveAnomalyTypeDef",
        "ReactiveAnomaly": "ReactiveAnomalyTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeEventSourcesConfigResponseTypeDef = TypedDict(
    "DescribeEventSourcesConfigResponseTypeDef",
    {
        "EventSources": "EventSourcesConfigTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeFeedbackRequestRequestTypeDef = TypedDict(
    "DescribeFeedbackRequestRequestTypeDef",
    {
        "InsightId": str,
    },
    total=False,
)

DescribeFeedbackResponseTypeDef = TypedDict(
    "DescribeFeedbackResponseTypeDef",
    {
        "InsightFeedback": "InsightFeedbackTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredDescribeInsightRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeInsightRequestRequestTypeDef",
    {
        "Id": str,
    },
)
_OptionalDescribeInsightRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeInsightRequestRequestTypeDef",
    {
        "AccountId": str,
    },
    total=False,
)


class DescribeInsightRequestRequestTypeDef(
    _RequiredDescribeInsightRequestRequestTypeDef, _OptionalDescribeInsightRequestRequestTypeDef
):
    pass


DescribeInsightResponseTypeDef = TypedDict(
    "DescribeInsightResponseTypeDef",
    {
        "ProactiveInsight": "ProactiveInsightTypeDef",
        "ReactiveInsight": "ReactiveInsightTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeOrganizationHealthRequestRequestTypeDef = TypedDict(
    "DescribeOrganizationHealthRequestRequestTypeDef",
    {
        "AccountIds": Sequence[str],
        "OrganizationalUnitIds": Sequence[str],
    },
    total=False,
)

DescribeOrganizationHealthResponseTypeDef = TypedDict(
    "DescribeOrganizationHealthResponseTypeDef",
    {
        "OpenReactiveInsights": int,
        "OpenProactiveInsights": int,
        "MetricsAnalyzed": int,
        "ResourceHours": int,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredDescribeOrganizationOverviewRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeOrganizationOverviewRequestRequestTypeDef",
    {
        "FromTime": Union[datetime, str],
    },
)
_OptionalDescribeOrganizationOverviewRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeOrganizationOverviewRequestRequestTypeDef",
    {
        "ToTime": Union[datetime, str],
        "AccountIds": Sequence[str],
        "OrganizationalUnitIds": Sequence[str],
    },
    total=False,
)


class DescribeOrganizationOverviewRequestRequestTypeDef(
    _RequiredDescribeOrganizationOverviewRequestRequestTypeDef,
    _OptionalDescribeOrganizationOverviewRequestRequestTypeDef,
):
    pass


DescribeOrganizationOverviewResponseTypeDef = TypedDict(
    "DescribeOrganizationOverviewResponseTypeDef",
    {
        "ReactiveInsights": int,
        "ProactiveInsights": int,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredDescribeOrganizationResourceCollectionHealthRequestDescribeOrganizationResourceCollectionHealthPaginateTypeDef = TypedDict(
    "_RequiredDescribeOrganizationResourceCollectionHealthRequestDescribeOrganizationResourceCollectionHealthPaginateTypeDef",
    {
        "OrganizationResourceCollectionType": OrganizationResourceCollectionTypeType,
    },
)
_OptionalDescribeOrganizationResourceCollectionHealthRequestDescribeOrganizationResourceCollectionHealthPaginateTypeDef = TypedDict(
    "_OptionalDescribeOrganizationResourceCollectionHealthRequestDescribeOrganizationResourceCollectionHealthPaginateTypeDef",
    {
        "AccountIds": Sequence[str],
        "OrganizationalUnitIds": Sequence[str],
        "MaxResults": int,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class DescribeOrganizationResourceCollectionHealthRequestDescribeOrganizationResourceCollectionHealthPaginateTypeDef(
    _RequiredDescribeOrganizationResourceCollectionHealthRequestDescribeOrganizationResourceCollectionHealthPaginateTypeDef,
    _OptionalDescribeOrganizationResourceCollectionHealthRequestDescribeOrganizationResourceCollectionHealthPaginateTypeDef,
):
    pass


_RequiredDescribeOrganizationResourceCollectionHealthRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeOrganizationResourceCollectionHealthRequestRequestTypeDef",
    {
        "OrganizationResourceCollectionType": OrganizationResourceCollectionTypeType,
    },
)
_OptionalDescribeOrganizationResourceCollectionHealthRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeOrganizationResourceCollectionHealthRequestRequestTypeDef",
    {
        "AccountIds": Sequence[str],
        "OrganizationalUnitIds": Sequence[str],
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class DescribeOrganizationResourceCollectionHealthRequestRequestTypeDef(
    _RequiredDescribeOrganizationResourceCollectionHealthRequestRequestTypeDef,
    _OptionalDescribeOrganizationResourceCollectionHealthRequestRequestTypeDef,
):
    pass


DescribeOrganizationResourceCollectionHealthResponseTypeDef = TypedDict(
    "DescribeOrganizationResourceCollectionHealthResponseTypeDef",
    {
        "CloudFormation": List["CloudFormationHealthTypeDef"],
        "Service": List["ServiceHealthTypeDef"],
        "Account": List["AccountHealthTypeDef"],
        "NextToken": str,
        "Tags": List["TagHealthTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredDescribeResourceCollectionHealthRequestDescribeResourceCollectionHealthPaginateTypeDef = TypedDict(
    "_RequiredDescribeResourceCollectionHealthRequestDescribeResourceCollectionHealthPaginateTypeDef",
    {
        "ResourceCollectionType": ResourceCollectionTypeType,
    },
)
_OptionalDescribeResourceCollectionHealthRequestDescribeResourceCollectionHealthPaginateTypeDef = TypedDict(
    "_OptionalDescribeResourceCollectionHealthRequestDescribeResourceCollectionHealthPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class DescribeResourceCollectionHealthRequestDescribeResourceCollectionHealthPaginateTypeDef(
    _RequiredDescribeResourceCollectionHealthRequestDescribeResourceCollectionHealthPaginateTypeDef,
    _OptionalDescribeResourceCollectionHealthRequestDescribeResourceCollectionHealthPaginateTypeDef,
):
    pass


_RequiredDescribeResourceCollectionHealthRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeResourceCollectionHealthRequestRequestTypeDef",
    {
        "ResourceCollectionType": ResourceCollectionTypeType,
    },
)
_OptionalDescribeResourceCollectionHealthRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeResourceCollectionHealthRequestRequestTypeDef",
    {
        "NextToken": str,
    },
    total=False,
)


class DescribeResourceCollectionHealthRequestRequestTypeDef(
    _RequiredDescribeResourceCollectionHealthRequestRequestTypeDef,
    _OptionalDescribeResourceCollectionHealthRequestRequestTypeDef,
):
    pass


DescribeResourceCollectionHealthResponseTypeDef = TypedDict(
    "DescribeResourceCollectionHealthResponseTypeDef",
    {
        "CloudFormation": List["CloudFormationHealthTypeDef"],
        "Service": List["ServiceHealthTypeDef"],
        "NextToken": str,
        "Tags": List["TagHealthTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeServiceIntegrationResponseTypeDef = TypedDict(
    "DescribeServiceIntegrationResponseTypeDef",
    {
        "ServiceIntegration": "ServiceIntegrationConfigTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

EndTimeRangeTypeDef = TypedDict(
    "EndTimeRangeTypeDef",
    {
        "FromTime": Union[datetime, str],
        "ToTime": Union[datetime, str],
    },
    total=False,
)

EventResourceTypeDef = TypedDict(
    "EventResourceTypeDef",
    {
        "Type": str,
        "Name": str,
        "Arn": str,
    },
    total=False,
)

EventSourcesConfigTypeDef = TypedDict(
    "EventSourcesConfigTypeDef",
    {
        "AmazonCodeGuruProfiler": "AmazonCodeGuruProfilerIntegrationTypeDef",
    },
    total=False,
)

EventTimeRangeTypeDef = TypedDict(
    "EventTimeRangeTypeDef",
    {
        "FromTime": Union[datetime, str],
        "ToTime": Union[datetime, str],
    },
)

EventTypeDef = TypedDict(
    "EventTypeDef",
    {
        "ResourceCollection": "ResourceCollectionTypeDef",
        "Id": str,
        "Time": datetime,
        "EventSource": str,
        "Name": str,
        "DataSource": EventDataSourceType,
        "EventClass": EventClassType,
        "Resources": List["EventResourceTypeDef"],
    },
    total=False,
)

GetCostEstimationRequestGetCostEstimationPaginateTypeDef = TypedDict(
    "GetCostEstimationRequestGetCostEstimationPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

GetCostEstimationRequestRequestTypeDef = TypedDict(
    "GetCostEstimationRequestRequestTypeDef",
    {
        "NextToken": str,
    },
    total=False,
)

GetCostEstimationResponseTypeDef = TypedDict(
    "GetCostEstimationResponseTypeDef",
    {
        "ResourceCollection": "CostEstimationResourceCollectionFilterTypeDef",
        "Status": CostEstimationStatusType,
        "Costs": List["ServiceResourceCostTypeDef"],
        "TimeRange": "CostEstimationTimeRangeTypeDef",
        "TotalCost": float,
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredGetResourceCollectionRequestGetResourceCollectionPaginateTypeDef = TypedDict(
    "_RequiredGetResourceCollectionRequestGetResourceCollectionPaginateTypeDef",
    {
        "ResourceCollectionType": ResourceCollectionTypeType,
    },
)
_OptionalGetResourceCollectionRequestGetResourceCollectionPaginateTypeDef = TypedDict(
    "_OptionalGetResourceCollectionRequestGetResourceCollectionPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class GetResourceCollectionRequestGetResourceCollectionPaginateTypeDef(
    _RequiredGetResourceCollectionRequestGetResourceCollectionPaginateTypeDef,
    _OptionalGetResourceCollectionRequestGetResourceCollectionPaginateTypeDef,
):
    pass


_RequiredGetResourceCollectionRequestRequestTypeDef = TypedDict(
    "_RequiredGetResourceCollectionRequestRequestTypeDef",
    {
        "ResourceCollectionType": ResourceCollectionTypeType,
    },
)
_OptionalGetResourceCollectionRequestRequestTypeDef = TypedDict(
    "_OptionalGetResourceCollectionRequestRequestTypeDef",
    {
        "NextToken": str,
    },
    total=False,
)


class GetResourceCollectionRequestRequestTypeDef(
    _RequiredGetResourceCollectionRequestRequestTypeDef,
    _OptionalGetResourceCollectionRequestRequestTypeDef,
):
    pass


GetResourceCollectionResponseTypeDef = TypedDict(
    "GetResourceCollectionResponseTypeDef",
    {
        "ResourceCollection": "ResourceCollectionFilterTypeDef",
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

InsightFeedbackTypeDef = TypedDict(
    "InsightFeedbackTypeDef",
    {
        "Id": str,
        "Feedback": InsightFeedbackOptionType,
    },
    total=False,
)

InsightHealthTypeDef = TypedDict(
    "InsightHealthTypeDef",
    {
        "OpenProactiveInsights": int,
        "OpenReactiveInsights": int,
        "MeanTimeToRecoverInMilliseconds": int,
    },
    total=False,
)

_RequiredInsightTimeRangeTypeDef = TypedDict(
    "_RequiredInsightTimeRangeTypeDef",
    {
        "StartTime": datetime,
    },
)
_OptionalInsightTimeRangeTypeDef = TypedDict(
    "_OptionalInsightTimeRangeTypeDef",
    {
        "EndTime": datetime,
    },
    total=False,
)


class InsightTimeRangeTypeDef(_RequiredInsightTimeRangeTypeDef, _OptionalInsightTimeRangeTypeDef):
    pass


_RequiredListAnomaliesForInsightRequestListAnomaliesForInsightPaginateTypeDef = TypedDict(
    "_RequiredListAnomaliesForInsightRequestListAnomaliesForInsightPaginateTypeDef",
    {
        "InsightId": str,
    },
)
_OptionalListAnomaliesForInsightRequestListAnomaliesForInsightPaginateTypeDef = TypedDict(
    "_OptionalListAnomaliesForInsightRequestListAnomaliesForInsightPaginateTypeDef",
    {
        "StartTimeRange": "StartTimeRangeTypeDef",
        "AccountId": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListAnomaliesForInsightRequestListAnomaliesForInsightPaginateTypeDef(
    _RequiredListAnomaliesForInsightRequestListAnomaliesForInsightPaginateTypeDef,
    _OptionalListAnomaliesForInsightRequestListAnomaliesForInsightPaginateTypeDef,
):
    pass


_RequiredListAnomaliesForInsightRequestRequestTypeDef = TypedDict(
    "_RequiredListAnomaliesForInsightRequestRequestTypeDef",
    {
        "InsightId": str,
    },
)
_OptionalListAnomaliesForInsightRequestRequestTypeDef = TypedDict(
    "_OptionalListAnomaliesForInsightRequestRequestTypeDef",
    {
        "StartTimeRange": "StartTimeRangeTypeDef",
        "MaxResults": int,
        "NextToken": str,
        "AccountId": str,
    },
    total=False,
)


class ListAnomaliesForInsightRequestRequestTypeDef(
    _RequiredListAnomaliesForInsightRequestRequestTypeDef,
    _OptionalListAnomaliesForInsightRequestRequestTypeDef,
):
    pass


ListAnomaliesForInsightResponseTypeDef = TypedDict(
    "ListAnomaliesForInsightResponseTypeDef",
    {
        "ProactiveAnomalies": List["ProactiveAnomalySummaryTypeDef"],
        "ReactiveAnomalies": List["ReactiveAnomalySummaryTypeDef"],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListEventsFiltersTypeDef = TypedDict(
    "ListEventsFiltersTypeDef",
    {
        "InsightId": str,
        "EventTimeRange": "EventTimeRangeTypeDef",
        "EventClass": EventClassType,
        "EventSource": str,
        "DataSource": EventDataSourceType,
        "ResourceCollection": "ResourceCollectionTypeDef",
    },
    total=False,
)

_RequiredListEventsRequestListEventsPaginateTypeDef = TypedDict(
    "_RequiredListEventsRequestListEventsPaginateTypeDef",
    {
        "Filters": "ListEventsFiltersTypeDef",
    },
)
_OptionalListEventsRequestListEventsPaginateTypeDef = TypedDict(
    "_OptionalListEventsRequestListEventsPaginateTypeDef",
    {
        "AccountId": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListEventsRequestListEventsPaginateTypeDef(
    _RequiredListEventsRequestListEventsPaginateTypeDef,
    _OptionalListEventsRequestListEventsPaginateTypeDef,
):
    pass


_RequiredListEventsRequestRequestTypeDef = TypedDict(
    "_RequiredListEventsRequestRequestTypeDef",
    {
        "Filters": "ListEventsFiltersTypeDef",
    },
)
_OptionalListEventsRequestRequestTypeDef = TypedDict(
    "_OptionalListEventsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
        "AccountId": str,
    },
    total=False,
)


class ListEventsRequestRequestTypeDef(
    _RequiredListEventsRequestRequestTypeDef, _OptionalListEventsRequestRequestTypeDef
):
    pass


ListEventsResponseTypeDef = TypedDict(
    "ListEventsResponseTypeDef",
    {
        "Events": List["EventTypeDef"],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListInsightsAnyStatusFilterTypeDef = TypedDict(
    "ListInsightsAnyStatusFilterTypeDef",
    {
        "Type": InsightTypeType,
        "StartTimeRange": "StartTimeRangeTypeDef",
    },
)

ListInsightsClosedStatusFilterTypeDef = TypedDict(
    "ListInsightsClosedStatusFilterTypeDef",
    {
        "Type": InsightTypeType,
        "EndTimeRange": "EndTimeRangeTypeDef",
    },
)

ListInsightsOngoingStatusFilterTypeDef = TypedDict(
    "ListInsightsOngoingStatusFilterTypeDef",
    {
        "Type": InsightTypeType,
    },
)

_RequiredListInsightsRequestListInsightsPaginateTypeDef = TypedDict(
    "_RequiredListInsightsRequestListInsightsPaginateTypeDef",
    {
        "StatusFilter": "ListInsightsStatusFilterTypeDef",
    },
)
_OptionalListInsightsRequestListInsightsPaginateTypeDef = TypedDict(
    "_OptionalListInsightsRequestListInsightsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListInsightsRequestListInsightsPaginateTypeDef(
    _RequiredListInsightsRequestListInsightsPaginateTypeDef,
    _OptionalListInsightsRequestListInsightsPaginateTypeDef,
):
    pass


_RequiredListInsightsRequestRequestTypeDef = TypedDict(
    "_RequiredListInsightsRequestRequestTypeDef",
    {
        "StatusFilter": "ListInsightsStatusFilterTypeDef",
    },
)
_OptionalListInsightsRequestRequestTypeDef = TypedDict(
    "_OptionalListInsightsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListInsightsRequestRequestTypeDef(
    _RequiredListInsightsRequestRequestTypeDef, _OptionalListInsightsRequestRequestTypeDef
):
    pass


ListInsightsResponseTypeDef = TypedDict(
    "ListInsightsResponseTypeDef",
    {
        "ProactiveInsights": List["ProactiveInsightSummaryTypeDef"],
        "ReactiveInsights": List["ReactiveInsightSummaryTypeDef"],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListInsightsStatusFilterTypeDef = TypedDict(
    "ListInsightsStatusFilterTypeDef",
    {
        "Ongoing": "ListInsightsOngoingStatusFilterTypeDef",
        "Closed": "ListInsightsClosedStatusFilterTypeDef",
        "Any": "ListInsightsAnyStatusFilterTypeDef",
    },
    total=False,
)

ListNotificationChannelsRequestListNotificationChannelsPaginateTypeDef = TypedDict(
    "ListNotificationChannelsRequestListNotificationChannelsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListNotificationChannelsRequestRequestTypeDef = TypedDict(
    "ListNotificationChannelsRequestRequestTypeDef",
    {
        "NextToken": str,
    },
    total=False,
)

ListNotificationChannelsResponseTypeDef = TypedDict(
    "ListNotificationChannelsResponseTypeDef",
    {
        "Channels": List["NotificationChannelTypeDef"],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredListOrganizationInsightsRequestListOrganizationInsightsPaginateTypeDef = TypedDict(
    "_RequiredListOrganizationInsightsRequestListOrganizationInsightsPaginateTypeDef",
    {
        "StatusFilter": "ListInsightsStatusFilterTypeDef",
    },
)
_OptionalListOrganizationInsightsRequestListOrganizationInsightsPaginateTypeDef = TypedDict(
    "_OptionalListOrganizationInsightsRequestListOrganizationInsightsPaginateTypeDef",
    {
        "AccountIds": Sequence[str],
        "OrganizationalUnitIds": Sequence[str],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListOrganizationInsightsRequestListOrganizationInsightsPaginateTypeDef(
    _RequiredListOrganizationInsightsRequestListOrganizationInsightsPaginateTypeDef,
    _OptionalListOrganizationInsightsRequestListOrganizationInsightsPaginateTypeDef,
):
    pass


_RequiredListOrganizationInsightsRequestRequestTypeDef = TypedDict(
    "_RequiredListOrganizationInsightsRequestRequestTypeDef",
    {
        "StatusFilter": "ListInsightsStatusFilterTypeDef",
    },
)
_OptionalListOrganizationInsightsRequestRequestTypeDef = TypedDict(
    "_OptionalListOrganizationInsightsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "AccountIds": Sequence[str],
        "OrganizationalUnitIds": Sequence[str],
        "NextToken": str,
    },
    total=False,
)


class ListOrganizationInsightsRequestRequestTypeDef(
    _RequiredListOrganizationInsightsRequestRequestTypeDef,
    _OptionalListOrganizationInsightsRequestRequestTypeDef,
):
    pass


ListOrganizationInsightsResponseTypeDef = TypedDict(
    "ListOrganizationInsightsResponseTypeDef",
    {
        "ProactiveInsights": List["ProactiveOrganizationInsightSummaryTypeDef"],
        "ReactiveInsights": List["ReactiveOrganizationInsightSummaryTypeDef"],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredListRecommendationsRequestListRecommendationsPaginateTypeDef = TypedDict(
    "_RequiredListRecommendationsRequestListRecommendationsPaginateTypeDef",
    {
        "InsightId": str,
    },
)
_OptionalListRecommendationsRequestListRecommendationsPaginateTypeDef = TypedDict(
    "_OptionalListRecommendationsRequestListRecommendationsPaginateTypeDef",
    {
        "Locale": LocaleType,
        "AccountId": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListRecommendationsRequestListRecommendationsPaginateTypeDef(
    _RequiredListRecommendationsRequestListRecommendationsPaginateTypeDef,
    _OptionalListRecommendationsRequestListRecommendationsPaginateTypeDef,
):
    pass


_RequiredListRecommendationsRequestRequestTypeDef = TypedDict(
    "_RequiredListRecommendationsRequestRequestTypeDef",
    {
        "InsightId": str,
    },
)
_OptionalListRecommendationsRequestRequestTypeDef = TypedDict(
    "_OptionalListRecommendationsRequestRequestTypeDef",
    {
        "NextToken": str,
        "Locale": LocaleType,
        "AccountId": str,
    },
    total=False,
)


class ListRecommendationsRequestRequestTypeDef(
    _RequiredListRecommendationsRequestRequestTypeDef,
    _OptionalListRecommendationsRequestRequestTypeDef,
):
    pass


ListRecommendationsResponseTypeDef = TypedDict(
    "ListRecommendationsResponseTypeDef",
    {
        "Recommendations": List["RecommendationTypeDef"],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

NotificationChannelConfigTypeDef = TypedDict(
    "NotificationChannelConfigTypeDef",
    {
        "Sns": "SnsChannelConfigTypeDef",
    },
)

NotificationChannelTypeDef = TypedDict(
    "NotificationChannelTypeDef",
    {
        "Id": str,
        "Config": "NotificationChannelConfigTypeDef",
    },
    total=False,
)

OpsCenterIntegrationConfigTypeDef = TypedDict(
    "OpsCenterIntegrationConfigTypeDef",
    {
        "OptInStatus": OptInStatusType,
    },
    total=False,
)

OpsCenterIntegrationTypeDef = TypedDict(
    "OpsCenterIntegrationTypeDef",
    {
        "OptInStatus": OptInStatusType,
    },
    total=False,
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": int,
        "PageSize": int,
        "StartingToken": str,
    },
    total=False,
)

PerformanceInsightsMetricDimensionGroupTypeDef = TypedDict(
    "PerformanceInsightsMetricDimensionGroupTypeDef",
    {
        "Group": str,
        "Dimensions": List[str],
        "Limit": int,
    },
    total=False,
)

PerformanceInsightsMetricQueryTypeDef = TypedDict(
    "PerformanceInsightsMetricQueryTypeDef",
    {
        "Metric": str,
        "GroupBy": "PerformanceInsightsMetricDimensionGroupTypeDef",
        "Filter": Dict[str, str],
    },
    total=False,
)

PerformanceInsightsMetricsDetailTypeDef = TypedDict(
    "PerformanceInsightsMetricsDetailTypeDef",
    {
        "MetricDisplayName": str,
        "Unit": str,
        "MetricQuery": "PerformanceInsightsMetricQueryTypeDef",
        "ReferenceData": List["PerformanceInsightsReferenceDataTypeDef"],
        "StatsAtAnomaly": List["PerformanceInsightsStatTypeDef"],
        "StatsAtBaseline": List["PerformanceInsightsStatTypeDef"],
    },
    total=False,
)

PerformanceInsightsReferenceComparisonValuesTypeDef = TypedDict(
    "PerformanceInsightsReferenceComparisonValuesTypeDef",
    {
        "ReferenceScalar": "PerformanceInsightsReferenceScalarTypeDef",
        "ReferenceMetric": "PerformanceInsightsReferenceMetricTypeDef",
    },
    total=False,
)

PerformanceInsightsReferenceDataTypeDef = TypedDict(
    "PerformanceInsightsReferenceDataTypeDef",
    {
        "Name": str,
        "ComparisonValues": "PerformanceInsightsReferenceComparisonValuesTypeDef",
    },
    total=False,
)

PerformanceInsightsReferenceMetricTypeDef = TypedDict(
    "PerformanceInsightsReferenceMetricTypeDef",
    {
        "MetricQuery": "PerformanceInsightsMetricQueryTypeDef",
    },
    total=False,
)

PerformanceInsightsReferenceScalarTypeDef = TypedDict(
    "PerformanceInsightsReferenceScalarTypeDef",
    {
        "Value": float,
    },
    total=False,
)

PerformanceInsightsStatTypeDef = TypedDict(
    "PerformanceInsightsStatTypeDef",
    {
        "Type": str,
        "Value": float,
    },
    total=False,
)

_RequiredPredictionTimeRangeTypeDef = TypedDict(
    "_RequiredPredictionTimeRangeTypeDef",
    {
        "StartTime": datetime,
    },
)
_OptionalPredictionTimeRangeTypeDef = TypedDict(
    "_OptionalPredictionTimeRangeTypeDef",
    {
        "EndTime": datetime,
    },
    total=False,
)


class PredictionTimeRangeTypeDef(
    _RequiredPredictionTimeRangeTypeDef, _OptionalPredictionTimeRangeTypeDef
):
    pass


ProactiveAnomalySummaryTypeDef = TypedDict(
    "ProactiveAnomalySummaryTypeDef",
    {
        "Id": str,
        "Severity": AnomalySeverityType,
        "Status": AnomalyStatusType,
        "UpdateTime": datetime,
        "AnomalyTimeRange": "AnomalyTimeRangeTypeDef",
        "AnomalyReportedTimeRange": "AnomalyReportedTimeRangeTypeDef",
        "PredictionTimeRange": "PredictionTimeRangeTypeDef",
        "SourceDetails": "AnomalySourceDetailsTypeDef",
        "AssociatedInsightId": str,
        "ResourceCollection": "ResourceCollectionTypeDef",
        "Limit": float,
        "SourceMetadata": "AnomalySourceMetadataTypeDef",
        "AnomalyResources": List["AnomalyResourceTypeDef"],
    },
    total=False,
)

ProactiveAnomalyTypeDef = TypedDict(
    "ProactiveAnomalyTypeDef",
    {
        "Id": str,
        "Severity": AnomalySeverityType,
        "Status": AnomalyStatusType,
        "UpdateTime": datetime,
        "AnomalyTimeRange": "AnomalyTimeRangeTypeDef",
        "AnomalyReportedTimeRange": "AnomalyReportedTimeRangeTypeDef",
        "PredictionTimeRange": "PredictionTimeRangeTypeDef",
        "SourceDetails": "AnomalySourceDetailsTypeDef",
        "AssociatedInsightId": str,
        "ResourceCollection": "ResourceCollectionTypeDef",
        "Limit": float,
        "SourceMetadata": "AnomalySourceMetadataTypeDef",
        "AnomalyResources": List["AnomalyResourceTypeDef"],
    },
    total=False,
)

ProactiveInsightSummaryTypeDef = TypedDict(
    "ProactiveInsightSummaryTypeDef",
    {
        "Id": str,
        "Name": str,
        "Severity": InsightSeverityType,
        "Status": InsightStatusType,
        "InsightTimeRange": "InsightTimeRangeTypeDef",
        "PredictionTimeRange": "PredictionTimeRangeTypeDef",
        "ResourceCollection": "ResourceCollectionTypeDef",
        "ServiceCollection": "ServiceCollectionTypeDef",
        "AssociatedResourceArns": List[str],
    },
    total=False,
)

ProactiveInsightTypeDef = TypedDict(
    "ProactiveInsightTypeDef",
    {
        "Id": str,
        "Name": str,
        "Severity": InsightSeverityType,
        "Status": InsightStatusType,
        "InsightTimeRange": "InsightTimeRangeTypeDef",
        "PredictionTimeRange": "PredictionTimeRangeTypeDef",
        "ResourceCollection": "ResourceCollectionTypeDef",
        "SsmOpsItemId": str,
        "Description": str,
    },
    total=False,
)

ProactiveOrganizationInsightSummaryTypeDef = TypedDict(
    "ProactiveOrganizationInsightSummaryTypeDef",
    {
        "Id": str,
        "AccountId": str,
        "OrganizationalUnitId": str,
        "Name": str,
        "Severity": InsightSeverityType,
        "Status": InsightStatusType,
        "InsightTimeRange": "InsightTimeRangeTypeDef",
        "PredictionTimeRange": "PredictionTimeRangeTypeDef",
        "ResourceCollection": "ResourceCollectionTypeDef",
        "ServiceCollection": "ServiceCollectionTypeDef",
    },
    total=False,
)

PutFeedbackRequestRequestTypeDef = TypedDict(
    "PutFeedbackRequestRequestTypeDef",
    {
        "InsightFeedback": "InsightFeedbackTypeDef",
    },
    total=False,
)

ReactiveAnomalySummaryTypeDef = TypedDict(
    "ReactiveAnomalySummaryTypeDef",
    {
        "Id": str,
        "Severity": AnomalySeverityType,
        "Status": AnomalyStatusType,
        "AnomalyTimeRange": "AnomalyTimeRangeTypeDef",
        "AnomalyReportedTimeRange": "AnomalyReportedTimeRangeTypeDef",
        "SourceDetails": "AnomalySourceDetailsTypeDef",
        "AssociatedInsightId": str,
        "ResourceCollection": "ResourceCollectionTypeDef",
        "Type": AnomalyTypeType,
        "Name": str,
        "Description": str,
        "CausalAnomalyId": str,
        "AnomalyResources": List["AnomalyResourceTypeDef"],
    },
    total=False,
)

ReactiveAnomalyTypeDef = TypedDict(
    "ReactiveAnomalyTypeDef",
    {
        "Id": str,
        "Severity": AnomalySeverityType,
        "Status": AnomalyStatusType,
        "AnomalyTimeRange": "AnomalyTimeRangeTypeDef",
        "AnomalyReportedTimeRange": "AnomalyReportedTimeRangeTypeDef",
        "SourceDetails": "AnomalySourceDetailsTypeDef",
        "AssociatedInsightId": str,
        "ResourceCollection": "ResourceCollectionTypeDef",
        "Type": AnomalyTypeType,
        "Name": str,
        "Description": str,
        "CausalAnomalyId": str,
        "AnomalyResources": List["AnomalyResourceTypeDef"],
    },
    total=False,
)

ReactiveInsightSummaryTypeDef = TypedDict(
    "ReactiveInsightSummaryTypeDef",
    {
        "Id": str,
        "Name": str,
        "Severity": InsightSeverityType,
        "Status": InsightStatusType,
        "InsightTimeRange": "InsightTimeRangeTypeDef",
        "ResourceCollection": "ResourceCollectionTypeDef",
        "ServiceCollection": "ServiceCollectionTypeDef",
        "AssociatedResourceArns": List[str],
    },
    total=False,
)

ReactiveInsightTypeDef = TypedDict(
    "ReactiveInsightTypeDef",
    {
        "Id": str,
        "Name": str,
        "Severity": InsightSeverityType,
        "Status": InsightStatusType,
        "InsightTimeRange": "InsightTimeRangeTypeDef",
        "ResourceCollection": "ResourceCollectionTypeDef",
        "SsmOpsItemId": str,
        "Description": str,
    },
    total=False,
)

ReactiveOrganizationInsightSummaryTypeDef = TypedDict(
    "ReactiveOrganizationInsightSummaryTypeDef",
    {
        "Id": str,
        "AccountId": str,
        "OrganizationalUnitId": str,
        "Name": str,
        "Severity": InsightSeverityType,
        "Status": InsightStatusType,
        "InsightTimeRange": "InsightTimeRangeTypeDef",
        "ResourceCollection": "ResourceCollectionTypeDef",
        "ServiceCollection": "ServiceCollectionTypeDef",
    },
    total=False,
)

RecommendationRelatedAnomalyResourceTypeDef = TypedDict(
    "RecommendationRelatedAnomalyResourceTypeDef",
    {
        "Name": str,
        "Type": str,
    },
    total=False,
)

RecommendationRelatedAnomalySourceDetailTypeDef = TypedDict(
    "RecommendationRelatedAnomalySourceDetailTypeDef",
    {
        "CloudWatchMetrics": List["RecommendationRelatedCloudWatchMetricsSourceDetailTypeDef"],
    },
    total=False,
)

RecommendationRelatedAnomalyTypeDef = TypedDict(
    "RecommendationRelatedAnomalyTypeDef",
    {
        "Resources": List["RecommendationRelatedAnomalyResourceTypeDef"],
        "SourceDetails": List["RecommendationRelatedAnomalySourceDetailTypeDef"],
        "AnomalyId": str,
    },
    total=False,
)

RecommendationRelatedCloudWatchMetricsSourceDetailTypeDef = TypedDict(
    "RecommendationRelatedCloudWatchMetricsSourceDetailTypeDef",
    {
        "MetricName": str,
        "Namespace": str,
    },
    total=False,
)

RecommendationRelatedEventResourceTypeDef = TypedDict(
    "RecommendationRelatedEventResourceTypeDef",
    {
        "Name": str,
        "Type": str,
    },
    total=False,
)

RecommendationRelatedEventTypeDef = TypedDict(
    "RecommendationRelatedEventTypeDef",
    {
        "Name": str,
        "Resources": List["RecommendationRelatedEventResourceTypeDef"],
    },
    total=False,
)

RecommendationTypeDef = TypedDict(
    "RecommendationTypeDef",
    {
        "Description": str,
        "Link": str,
        "Name": str,
        "Reason": str,
        "RelatedEvents": List["RecommendationRelatedEventTypeDef"],
        "RelatedAnomalies": List["RecommendationRelatedAnomalyTypeDef"],
        "Category": str,
    },
    total=False,
)

RemoveNotificationChannelRequestRequestTypeDef = TypedDict(
    "RemoveNotificationChannelRequestRequestTypeDef",
    {
        "Id": str,
    },
)

ResourceCollectionFilterTypeDef = TypedDict(
    "ResourceCollectionFilterTypeDef",
    {
        "CloudFormation": "CloudFormationCollectionFilterTypeDef",
        "Tags": List["TagCollectionFilterTypeDef"],
    },
    total=False,
)

ResourceCollectionTypeDef = TypedDict(
    "ResourceCollectionTypeDef",
    {
        "CloudFormation": "CloudFormationCollectionTypeDef",
        "Tags": List["TagCollectionTypeDef"],
    },
    total=False,
)

ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HostId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
    },
)

SearchInsightsFiltersTypeDef = TypedDict(
    "SearchInsightsFiltersTypeDef",
    {
        "Severities": Sequence[InsightSeverityType],
        "Statuses": Sequence[InsightStatusType],
        "ResourceCollection": "ResourceCollectionTypeDef",
        "ServiceCollection": "ServiceCollectionTypeDef",
    },
    total=False,
)

_RequiredSearchInsightsRequestRequestTypeDef = TypedDict(
    "_RequiredSearchInsightsRequestRequestTypeDef",
    {
        "StartTimeRange": "StartTimeRangeTypeDef",
        "Type": InsightTypeType,
    },
)
_OptionalSearchInsightsRequestRequestTypeDef = TypedDict(
    "_OptionalSearchInsightsRequestRequestTypeDef",
    {
        "Filters": "SearchInsightsFiltersTypeDef",
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class SearchInsightsRequestRequestTypeDef(
    _RequiredSearchInsightsRequestRequestTypeDef, _OptionalSearchInsightsRequestRequestTypeDef
):
    pass


_RequiredSearchInsightsRequestSearchInsightsPaginateTypeDef = TypedDict(
    "_RequiredSearchInsightsRequestSearchInsightsPaginateTypeDef",
    {
        "StartTimeRange": "StartTimeRangeTypeDef",
        "Type": InsightTypeType,
    },
)
_OptionalSearchInsightsRequestSearchInsightsPaginateTypeDef = TypedDict(
    "_OptionalSearchInsightsRequestSearchInsightsPaginateTypeDef",
    {
        "Filters": "SearchInsightsFiltersTypeDef",
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class SearchInsightsRequestSearchInsightsPaginateTypeDef(
    _RequiredSearchInsightsRequestSearchInsightsPaginateTypeDef,
    _OptionalSearchInsightsRequestSearchInsightsPaginateTypeDef,
):
    pass


SearchInsightsResponseTypeDef = TypedDict(
    "SearchInsightsResponseTypeDef",
    {
        "ProactiveInsights": List["ProactiveInsightSummaryTypeDef"],
        "ReactiveInsights": List["ReactiveInsightSummaryTypeDef"],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

SearchOrganizationInsightsFiltersTypeDef = TypedDict(
    "SearchOrganizationInsightsFiltersTypeDef",
    {
        "Severities": Sequence[InsightSeverityType],
        "Statuses": Sequence[InsightStatusType],
        "ResourceCollection": "ResourceCollectionTypeDef",
        "ServiceCollection": "ServiceCollectionTypeDef",
    },
    total=False,
)

_RequiredSearchOrganizationInsightsRequestRequestTypeDef = TypedDict(
    "_RequiredSearchOrganizationInsightsRequestRequestTypeDef",
    {
        "AccountIds": Sequence[str],
        "StartTimeRange": "StartTimeRangeTypeDef",
        "Type": InsightTypeType,
    },
)
_OptionalSearchOrganizationInsightsRequestRequestTypeDef = TypedDict(
    "_OptionalSearchOrganizationInsightsRequestRequestTypeDef",
    {
        "Filters": "SearchOrganizationInsightsFiltersTypeDef",
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class SearchOrganizationInsightsRequestRequestTypeDef(
    _RequiredSearchOrganizationInsightsRequestRequestTypeDef,
    _OptionalSearchOrganizationInsightsRequestRequestTypeDef,
):
    pass


_RequiredSearchOrganizationInsightsRequestSearchOrganizationInsightsPaginateTypeDef = TypedDict(
    "_RequiredSearchOrganizationInsightsRequestSearchOrganizationInsightsPaginateTypeDef",
    {
        "AccountIds": Sequence[str],
        "StartTimeRange": "StartTimeRangeTypeDef",
        "Type": InsightTypeType,
    },
)
_OptionalSearchOrganizationInsightsRequestSearchOrganizationInsightsPaginateTypeDef = TypedDict(
    "_OptionalSearchOrganizationInsightsRequestSearchOrganizationInsightsPaginateTypeDef",
    {
        "Filters": "SearchOrganizationInsightsFiltersTypeDef",
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class SearchOrganizationInsightsRequestSearchOrganizationInsightsPaginateTypeDef(
    _RequiredSearchOrganizationInsightsRequestSearchOrganizationInsightsPaginateTypeDef,
    _OptionalSearchOrganizationInsightsRequestSearchOrganizationInsightsPaginateTypeDef,
):
    pass


SearchOrganizationInsightsResponseTypeDef = TypedDict(
    "SearchOrganizationInsightsResponseTypeDef",
    {
        "ProactiveInsights": List["ProactiveInsightSummaryTypeDef"],
        "ReactiveInsights": List["ReactiveInsightSummaryTypeDef"],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ServiceCollectionTypeDef = TypedDict(
    "ServiceCollectionTypeDef",
    {
        "ServiceNames": List[ServiceNameType],
    },
    total=False,
)

ServiceHealthTypeDef = TypedDict(
    "ServiceHealthTypeDef",
    {
        "ServiceName": ServiceNameType,
        "Insight": "ServiceInsightHealthTypeDef",
    },
    total=False,
)

ServiceInsightHealthTypeDef = TypedDict(
    "ServiceInsightHealthTypeDef",
    {
        "OpenProactiveInsights": int,
        "OpenReactiveInsights": int,
    },
    total=False,
)

ServiceIntegrationConfigTypeDef = TypedDict(
    "ServiceIntegrationConfigTypeDef",
    {
        "OpsCenter": "OpsCenterIntegrationTypeDef",
    },
    total=False,
)

ServiceResourceCostTypeDef = TypedDict(
    "ServiceResourceCostTypeDef",
    {
        "Type": str,
        "State": CostEstimationServiceResourceStateType,
        "Count": int,
        "UnitCost": float,
        "Cost": float,
    },
    total=False,
)

SnsChannelConfigTypeDef = TypedDict(
    "SnsChannelConfigTypeDef",
    {
        "TopicArn": str,
    },
    total=False,
)

_RequiredStartCostEstimationRequestRequestTypeDef = TypedDict(
    "_RequiredStartCostEstimationRequestRequestTypeDef",
    {
        "ResourceCollection": "CostEstimationResourceCollectionFilterTypeDef",
    },
)
_OptionalStartCostEstimationRequestRequestTypeDef = TypedDict(
    "_OptionalStartCostEstimationRequestRequestTypeDef",
    {
        "ClientToken": str,
    },
    total=False,
)


class StartCostEstimationRequestRequestTypeDef(
    _RequiredStartCostEstimationRequestRequestTypeDef,
    _OptionalStartCostEstimationRequestRequestTypeDef,
):
    pass


StartTimeRangeTypeDef = TypedDict(
    "StartTimeRangeTypeDef",
    {
        "FromTime": Union[datetime, str],
        "ToTime": Union[datetime, str],
    },
    total=False,
)

TagCollectionFilterTypeDef = TypedDict(
    "TagCollectionFilterTypeDef",
    {
        "AppBoundaryKey": str,
        "TagValues": List[str],
    },
)

TagCollectionTypeDef = TypedDict(
    "TagCollectionTypeDef",
    {
        "AppBoundaryKey": str,
        "TagValues": List[str],
    },
)

TagCostEstimationResourceCollectionFilterTypeDef = TypedDict(
    "TagCostEstimationResourceCollectionFilterTypeDef",
    {
        "AppBoundaryKey": str,
        "TagValues": List[str],
    },
)

TagHealthTypeDef = TypedDict(
    "TagHealthTypeDef",
    {
        "AppBoundaryKey": str,
        "TagValue": str,
        "Insight": "InsightHealthTypeDef",
    },
    total=False,
)

TimestampMetricValuePairTypeDef = TypedDict(
    "TimestampMetricValuePairTypeDef",
    {
        "Timestamp": datetime,
        "MetricValue": float,
    },
    total=False,
)

UpdateCloudFormationCollectionFilterTypeDef = TypedDict(
    "UpdateCloudFormationCollectionFilterTypeDef",
    {
        "StackNames": Sequence[str],
    },
    total=False,
)

UpdateEventSourcesConfigRequestRequestTypeDef = TypedDict(
    "UpdateEventSourcesConfigRequestRequestTypeDef",
    {
        "EventSources": "EventSourcesConfigTypeDef",
    },
    total=False,
)

UpdateResourceCollectionFilterTypeDef = TypedDict(
    "UpdateResourceCollectionFilterTypeDef",
    {
        "CloudFormation": "UpdateCloudFormationCollectionFilterTypeDef",
        "Tags": Sequence["UpdateTagCollectionFilterTypeDef"],
    },
    total=False,
)

UpdateResourceCollectionRequestRequestTypeDef = TypedDict(
    "UpdateResourceCollectionRequestRequestTypeDef",
    {
        "Action": UpdateResourceCollectionActionType,
        "ResourceCollection": "UpdateResourceCollectionFilterTypeDef",
    },
)

UpdateServiceIntegrationConfigTypeDef = TypedDict(
    "UpdateServiceIntegrationConfigTypeDef",
    {
        "OpsCenter": "OpsCenterIntegrationConfigTypeDef",
    },
    total=False,
)

UpdateServiceIntegrationRequestRequestTypeDef = TypedDict(
    "UpdateServiceIntegrationRequestRequestTypeDef",
    {
        "ServiceIntegration": "UpdateServiceIntegrationConfigTypeDef",
    },
)

UpdateTagCollectionFilterTypeDef = TypedDict(
    "UpdateTagCollectionFilterTypeDef",
    {
        "AppBoundaryKey": str,
        "TagValues": Sequence[str],
    },
)
