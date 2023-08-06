"""
Type annotations for devops-guru service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_devops_guru.client import DevOpsGuruClient

    session = get_session()
    async with session.create_client("devops-guru") as client:
        client: DevOpsGuruClient
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, Mapping, Sequence, Type, Union, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import (
    InsightTypeType,
    LocaleType,
    OrganizationResourceCollectionTypeType,
    ResourceCollectionTypeType,
    UpdateResourceCollectionActionType,
)
from .paginator import (
    DescribeOrganizationResourceCollectionHealthPaginator,
    DescribeResourceCollectionHealthPaginator,
    GetCostEstimationPaginator,
    GetResourceCollectionPaginator,
    ListAnomaliesForInsightPaginator,
    ListEventsPaginator,
    ListInsightsPaginator,
    ListNotificationChannelsPaginator,
    ListOrganizationInsightsPaginator,
    ListRecommendationsPaginator,
    SearchInsightsPaginator,
    SearchOrganizationInsightsPaginator,
)
from .type_defs import (
    AddNotificationChannelResponseTypeDef,
    CostEstimationResourceCollectionFilterTypeDef,
    DescribeAccountHealthResponseTypeDef,
    DescribeAccountOverviewResponseTypeDef,
    DescribeAnomalyResponseTypeDef,
    DescribeEventSourcesConfigResponseTypeDef,
    DescribeFeedbackResponseTypeDef,
    DescribeInsightResponseTypeDef,
    DescribeOrganizationHealthResponseTypeDef,
    DescribeOrganizationOverviewResponseTypeDef,
    DescribeOrganizationResourceCollectionHealthResponseTypeDef,
    DescribeResourceCollectionHealthResponseTypeDef,
    DescribeServiceIntegrationResponseTypeDef,
    EventSourcesConfigTypeDef,
    GetCostEstimationResponseTypeDef,
    GetResourceCollectionResponseTypeDef,
    InsightFeedbackTypeDef,
    ListAnomaliesForInsightResponseTypeDef,
    ListEventsFiltersTypeDef,
    ListEventsResponseTypeDef,
    ListInsightsResponseTypeDef,
    ListInsightsStatusFilterTypeDef,
    ListNotificationChannelsResponseTypeDef,
    ListOrganizationInsightsResponseTypeDef,
    ListRecommendationsResponseTypeDef,
    NotificationChannelConfigTypeDef,
    SearchInsightsFiltersTypeDef,
    SearchInsightsResponseTypeDef,
    SearchOrganizationInsightsFiltersTypeDef,
    SearchOrganizationInsightsResponseTypeDef,
    StartTimeRangeTypeDef,
    UpdateResourceCollectionFilterTypeDef,
    UpdateServiceIntegrationConfigTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("DevOpsGuruClient",)

class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class DevOpsGuruClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru.html#DevOpsGuru.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        DevOpsGuruClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru.html#DevOpsGuru.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/client/#exceptions)
        """
    async def add_notification_channel(
        self, *, Config: "NotificationChannelConfigTypeDef"
    ) -> AddNotificationChannelResponseTypeDef:
        """
        Adds a notification channel to DevOps Guru.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru.html#DevOpsGuru.Client.add_notification_channel)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/client/#add_notification_channel)
        """
    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru.html#DevOpsGuru.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/client/#can_paginate)
        """
    async def describe_account_health(self) -> DescribeAccountHealthResponseTypeDef:
        """
        Returns the number of open reactive insights, the number of open proactive
        insights, and the number of metrics analyzed in your Amazon Web Services
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru.html#DevOpsGuru.Client.describe_account_health)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/client/#describe_account_health)
        """
    async def describe_account_overview(
        self, *, FromTime: Union[datetime, str], ToTime: Union[datetime, str] = ...
    ) -> DescribeAccountOverviewResponseTypeDef:
        """
        For the time range passed in, returns the number of open reactive insight that
        were created, the number of open proactive insights that were created, and the
        Mean Time to Recover (MTTR) for all closed reactive insights.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru.html#DevOpsGuru.Client.describe_account_overview)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/client/#describe_account_overview)
        """
    async def describe_anomaly(
        self, *, Id: str, AccountId: str = ...
    ) -> DescribeAnomalyResponseTypeDef:
        """
        Returns details about an anomaly that you specify using its ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru.html#DevOpsGuru.Client.describe_anomaly)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/client/#describe_anomaly)
        """
    async def describe_event_sources_config(self) -> DescribeEventSourcesConfigResponseTypeDef:
        """
        This operation lists details about a DevOps Guru event source that is shared
        with your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru.html#DevOpsGuru.Client.describe_event_sources_config)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/client/#describe_event_sources_config)
        """
    async def describe_feedback(self, *, InsightId: str = ...) -> DescribeFeedbackResponseTypeDef:
        """
        Returns the most recent feedback submitted in the current Amazon Web Services
        account and Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru.html#DevOpsGuru.Client.describe_feedback)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/client/#describe_feedback)
        """
    async def describe_insight(
        self, *, Id: str, AccountId: str = ...
    ) -> DescribeInsightResponseTypeDef:
        """
        Returns details about an insight that you specify using its ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru.html#DevOpsGuru.Client.describe_insight)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/client/#describe_insight)
        """
    async def describe_organization_health(
        self, *, AccountIds: Sequence[str] = ..., OrganizationalUnitIds: Sequence[str] = ...
    ) -> DescribeOrganizationHealthResponseTypeDef:
        """
        Returns active insights, predictive insights, and resource hours analyzed in
        last hour.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru.html#DevOpsGuru.Client.describe_organization_health)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/client/#describe_organization_health)
        """
    async def describe_organization_overview(
        self,
        *,
        FromTime: Union[datetime, str],
        ToTime: Union[datetime, str] = ...,
        AccountIds: Sequence[str] = ...,
        OrganizationalUnitIds: Sequence[str] = ...
    ) -> DescribeOrganizationOverviewResponseTypeDef:
        """
        Returns an overview of your organization's history based on the specified time
        range.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru.html#DevOpsGuru.Client.describe_organization_overview)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/client/#describe_organization_overview)
        """
    async def describe_organization_resource_collection_health(
        self,
        *,
        OrganizationResourceCollectionType: OrganizationResourceCollectionTypeType,
        AccountIds: Sequence[str] = ...,
        OrganizationalUnitIds: Sequence[str] = ...,
        NextToken: str = ...,
        MaxResults: int = ...
    ) -> DescribeOrganizationResourceCollectionHealthResponseTypeDef:
        """
        Provides an overview of your system's health.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru.html#DevOpsGuru.Client.describe_organization_resource_collection_health)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/client/#describe_organization_resource_collection_health)
        """
    async def describe_resource_collection_health(
        self, *, ResourceCollectionType: ResourceCollectionTypeType, NextToken: str = ...
    ) -> DescribeResourceCollectionHealthResponseTypeDef:
        """
        Returns the number of open proactive insights, open reactive insights, and the
        Mean Time to Recover (MTTR) for all closed insights in resource collections in
        your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru.html#DevOpsGuru.Client.describe_resource_collection_health)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/client/#describe_resource_collection_health)
        """
    async def describe_service_integration(self) -> DescribeServiceIntegrationResponseTypeDef:
        """
        Returns the integration status of services that are integrated with DevOps Guru.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru.html#DevOpsGuru.Client.describe_service_integration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/client/#describe_service_integration)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru.html#DevOpsGuru.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/client/#generate_presigned_url)
        """
    async def get_cost_estimation(
        self, *, NextToken: str = ...
    ) -> GetCostEstimationResponseTypeDef:
        """
        Returns an estimate of the monthly cost for DevOps Guru to analyze your Amazon
        Web Services resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru.html#DevOpsGuru.Client.get_cost_estimation)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/client/#get_cost_estimation)
        """
    async def get_resource_collection(
        self, *, ResourceCollectionType: ResourceCollectionTypeType, NextToken: str = ...
    ) -> GetResourceCollectionResponseTypeDef:
        """
        Returns lists Amazon Web Services resources that are of the specified resource
        collection type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru.html#DevOpsGuru.Client.get_resource_collection)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/client/#get_resource_collection)
        """
    async def list_anomalies_for_insight(
        self,
        *,
        InsightId: str,
        StartTimeRange: "StartTimeRangeTypeDef" = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
        AccountId: str = ...
    ) -> ListAnomaliesForInsightResponseTypeDef:
        """
        Returns a list of the anomalies that belong to an insight that you specify using
        its ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru.html#DevOpsGuru.Client.list_anomalies_for_insight)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/client/#list_anomalies_for_insight)
        """
    async def list_events(
        self,
        *,
        Filters: "ListEventsFiltersTypeDef",
        MaxResults: int = ...,
        NextToken: str = ...,
        AccountId: str = ...
    ) -> ListEventsResponseTypeDef:
        """
        Returns a list of the events emitted by the resources that are evaluated by
        DevOps Guru.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru.html#DevOpsGuru.Client.list_events)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/client/#list_events)
        """
    async def list_insights(
        self,
        *,
        StatusFilter: "ListInsightsStatusFilterTypeDef",
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> ListInsightsResponseTypeDef:
        """
        Returns a list of insights in your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru.html#DevOpsGuru.Client.list_insights)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/client/#list_insights)
        """
    async def list_notification_channels(
        self, *, NextToken: str = ...
    ) -> ListNotificationChannelsResponseTypeDef:
        """
        Returns a list of notification channels configured for DevOps Guru.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru.html#DevOpsGuru.Client.list_notification_channels)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/client/#list_notification_channels)
        """
    async def list_organization_insights(
        self,
        *,
        StatusFilter: "ListInsightsStatusFilterTypeDef",
        MaxResults: int = ...,
        AccountIds: Sequence[str] = ...,
        OrganizationalUnitIds: Sequence[str] = ...,
        NextToken: str = ...
    ) -> ListOrganizationInsightsResponseTypeDef:
        """
        Returns a list of insights associated with the account or OU Id.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru.html#DevOpsGuru.Client.list_organization_insights)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/client/#list_organization_insights)
        """
    async def list_recommendations(
        self,
        *,
        InsightId: str,
        NextToken: str = ...,
        Locale: LocaleType = ...,
        AccountId: str = ...
    ) -> ListRecommendationsResponseTypeDef:
        """
        Returns a list of a specified insight's recommendations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru.html#DevOpsGuru.Client.list_recommendations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/client/#list_recommendations)
        """
    async def put_feedback(
        self, *, InsightFeedback: "InsightFeedbackTypeDef" = ...
    ) -> Dict[str, Any]:
        """
        Collects customer feedback about the specified insight.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru.html#DevOpsGuru.Client.put_feedback)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/client/#put_feedback)
        """
    async def remove_notification_channel(self, *, Id: str) -> Dict[str, Any]:
        """
        Removes a notification channel from DevOps Guru.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru.html#DevOpsGuru.Client.remove_notification_channel)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/client/#remove_notification_channel)
        """
    async def search_insights(
        self,
        *,
        StartTimeRange: "StartTimeRangeTypeDef",
        Type: InsightTypeType,
        Filters: "SearchInsightsFiltersTypeDef" = ...,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> SearchInsightsResponseTypeDef:
        """
        Returns a list of insights in your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru.html#DevOpsGuru.Client.search_insights)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/client/#search_insights)
        """
    async def search_organization_insights(
        self,
        *,
        AccountIds: Sequence[str],
        StartTimeRange: "StartTimeRangeTypeDef",
        Type: InsightTypeType,
        Filters: "SearchOrganizationInsightsFiltersTypeDef" = ...,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> SearchOrganizationInsightsResponseTypeDef:
        """
        Returns a list of insights in your organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru.html#DevOpsGuru.Client.search_organization_insights)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/client/#search_organization_insights)
        """
    async def start_cost_estimation(
        self,
        *,
        ResourceCollection: "CostEstimationResourceCollectionFilterTypeDef",
        ClientToken: str = ...
    ) -> Dict[str, Any]:
        """
        Starts the creation of an estimate of the monthly cost to analyze your Amazon
        Web Services resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru.html#DevOpsGuru.Client.start_cost_estimation)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/client/#start_cost_estimation)
        """
    async def update_event_sources_config(
        self, *, EventSources: "EventSourcesConfigTypeDef" = ...
    ) -> Dict[str, Any]:
        """
        Updates the event source configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru.html#DevOpsGuru.Client.update_event_sources_config)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/client/#update_event_sources_config)
        """
    async def update_resource_collection(
        self,
        *,
        Action: UpdateResourceCollectionActionType,
        ResourceCollection: "UpdateResourceCollectionFilterTypeDef"
    ) -> Dict[str, Any]:
        """
        Updates the collection of resources that DevOps Guru analyzes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru.html#DevOpsGuru.Client.update_resource_collection)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/client/#update_resource_collection)
        """
    async def update_service_integration(
        self, *, ServiceIntegration: "UpdateServiceIntegrationConfigTypeDef"
    ) -> Dict[str, Any]:
        """
        Enables or disables integration with a service that can be integrated with
        DevOps Guru.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru.html#DevOpsGuru.Client.update_service_integration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/client/#update_service_integration)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["describe_organization_resource_collection_health"]
    ) -> DescribeOrganizationResourceCollectionHealthPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru.html#DevOpsGuru.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["describe_resource_collection_health"]
    ) -> DescribeResourceCollectionHealthPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru.html#DevOpsGuru.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["get_cost_estimation"]
    ) -> GetCostEstimationPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru.html#DevOpsGuru.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["get_resource_collection"]
    ) -> GetResourceCollectionPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru.html#DevOpsGuru.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_anomalies_for_insight"]
    ) -> ListAnomaliesForInsightPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru.html#DevOpsGuru.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/client/#get_paginator)
        """
    @overload
    def get_paginator(self, operation_name: Literal["list_events"]) -> ListEventsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru.html#DevOpsGuru.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/client/#get_paginator)
        """
    @overload
    def get_paginator(self, operation_name: Literal["list_insights"]) -> ListInsightsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru.html#DevOpsGuru.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_notification_channels"]
    ) -> ListNotificationChannelsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru.html#DevOpsGuru.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_organization_insights"]
    ) -> ListOrganizationInsightsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru.html#DevOpsGuru.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_recommendations"]
    ) -> ListRecommendationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru.html#DevOpsGuru.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/client/#get_paginator)
        """
    @overload
    def get_paginator(self, operation_name: Literal["search_insights"]) -> SearchInsightsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru.html#DevOpsGuru.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["search_organization_insights"]
    ) -> SearchOrganizationInsightsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru.html#DevOpsGuru.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/client/#get_paginator)
        """
    async def __aenter__(self) -> "DevOpsGuruClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru.html#DevOpsGuru.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/client/)
        """
    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-guru.html#DevOpsGuru.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_guru/client/)
        """
