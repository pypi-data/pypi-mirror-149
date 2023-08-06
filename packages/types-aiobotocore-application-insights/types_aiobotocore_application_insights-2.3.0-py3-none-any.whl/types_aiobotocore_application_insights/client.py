"""
Type annotations for application-insights service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_insights/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_application_insights.client import ApplicationInsightsClient

    session = get_session()
    async with session.create_client("application-insights") as client:
        client: ApplicationInsightsClient
    ```
"""
from datetime import datetime
from typing import Any, Dict, Mapping, Sequence, Type, Union

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import ConfigurationEventStatusType, TierType
from .type_defs import (
    CreateApplicationResponseTypeDef,
    CreateLogPatternResponseTypeDef,
    DescribeApplicationResponseTypeDef,
    DescribeComponentConfigurationRecommendationResponseTypeDef,
    DescribeComponentConfigurationResponseTypeDef,
    DescribeComponentResponseTypeDef,
    DescribeLogPatternResponseTypeDef,
    DescribeObservationResponseTypeDef,
    DescribeProblemObservationsResponseTypeDef,
    DescribeProblemResponseTypeDef,
    ListApplicationsResponseTypeDef,
    ListComponentsResponseTypeDef,
    ListConfigurationHistoryResponseTypeDef,
    ListLogPatternSetsResponseTypeDef,
    ListLogPatternsResponseTypeDef,
    ListProblemsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    TagTypeDef,
    UpdateApplicationResponseTypeDef,
    UpdateLogPatternResponseTypeDef,
)

__all__ = ("ApplicationInsightsClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceInUseException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    TagsAlreadyExistException: Type[BotocoreClientError]
    TooManyTagsException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class ApplicationInsightsClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-insights.html#ApplicationInsights.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_insights/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ApplicationInsightsClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-insights.html#ApplicationInsights.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_insights/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-insights.html#ApplicationInsights.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_insights/client/#can_paginate)
        """

    async def create_application(
        self,
        *,
        ResourceGroupName: str = ...,
        OpsCenterEnabled: bool = ...,
        CWEMonitorEnabled: bool = ...,
        OpsItemSNSTopicArn: str = ...,
        Tags: Sequence["TagTypeDef"] = ...,
        AutoConfigEnabled: bool = ...,
        AutoCreate: bool = ...
    ) -> CreateApplicationResponseTypeDef:
        """
        Adds an application that is created from a resource group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-insights.html#ApplicationInsights.Client.create_application)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_insights/client/#create_application)
        """

    async def create_component(
        self, *, ResourceGroupName: str, ComponentName: str, ResourceList: Sequence[str]
    ) -> Dict[str, Any]:
        """
        Creates a custom component by grouping similar standalone instances to monitor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-insights.html#ApplicationInsights.Client.create_component)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_insights/client/#create_component)
        """

    async def create_log_pattern(
        self,
        *,
        ResourceGroupName: str,
        PatternSetName: str,
        PatternName: str,
        Pattern: str,
        Rank: int
    ) -> CreateLogPatternResponseTypeDef:
        """
        Adds an log pattern to a `LogPatternSet` .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-insights.html#ApplicationInsights.Client.create_log_pattern)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_insights/client/#create_log_pattern)
        """

    async def delete_application(self, *, ResourceGroupName: str) -> Dict[str, Any]:
        """
        Removes the specified application from monitoring.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-insights.html#ApplicationInsights.Client.delete_application)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_insights/client/#delete_application)
        """

    async def delete_component(
        self, *, ResourceGroupName: str, ComponentName: str
    ) -> Dict[str, Any]:
        """
        Ungroups a custom component.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-insights.html#ApplicationInsights.Client.delete_component)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_insights/client/#delete_component)
        """

    async def delete_log_pattern(
        self, *, ResourceGroupName: str, PatternSetName: str, PatternName: str
    ) -> Dict[str, Any]:
        """
        Removes the specified log pattern from a `LogPatternSet` .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-insights.html#ApplicationInsights.Client.delete_log_pattern)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_insights/client/#delete_log_pattern)
        """

    async def describe_application(
        self, *, ResourceGroupName: str
    ) -> DescribeApplicationResponseTypeDef:
        """
        Describes the application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-insights.html#ApplicationInsights.Client.describe_application)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_insights/client/#describe_application)
        """

    async def describe_component(
        self, *, ResourceGroupName: str, ComponentName: str
    ) -> DescribeComponentResponseTypeDef:
        """
        Describes a component and lists the resources that are grouped together in a
        component.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-insights.html#ApplicationInsights.Client.describe_component)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_insights/client/#describe_component)
        """

    async def describe_component_configuration(
        self, *, ResourceGroupName: str, ComponentName: str
    ) -> DescribeComponentConfigurationResponseTypeDef:
        """
        Describes the monitoring configuration of the component.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-insights.html#ApplicationInsights.Client.describe_component_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_insights/client/#describe_component_configuration)
        """

    async def describe_component_configuration_recommendation(
        self, *, ResourceGroupName: str, ComponentName: str, Tier: TierType
    ) -> DescribeComponentConfigurationRecommendationResponseTypeDef:
        """
        Describes the recommended monitoring configuration of the component.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-insights.html#ApplicationInsights.Client.describe_component_configuration_recommendation)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_insights/client/#describe_component_configuration_recommendation)
        """

    async def describe_log_pattern(
        self, *, ResourceGroupName: str, PatternSetName: str, PatternName: str
    ) -> DescribeLogPatternResponseTypeDef:
        """
        Describe a specific log pattern from a `LogPatternSet` .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-insights.html#ApplicationInsights.Client.describe_log_pattern)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_insights/client/#describe_log_pattern)
        """

    async def describe_observation(
        self, *, ObservationId: str
    ) -> DescribeObservationResponseTypeDef:
        """
        Describes an anomaly or error with the application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-insights.html#ApplicationInsights.Client.describe_observation)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_insights/client/#describe_observation)
        """

    async def describe_problem(self, *, ProblemId: str) -> DescribeProblemResponseTypeDef:
        """
        Describes an application problem.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-insights.html#ApplicationInsights.Client.describe_problem)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_insights/client/#describe_problem)
        """

    async def describe_problem_observations(
        self, *, ProblemId: str
    ) -> DescribeProblemObservationsResponseTypeDef:
        """
        Describes the anomalies or errors associated with the problem.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-insights.html#ApplicationInsights.Client.describe_problem_observations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_insights/client/#describe_problem_observations)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-insights.html#ApplicationInsights.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_insights/client/#generate_presigned_url)
        """

    async def list_applications(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListApplicationsResponseTypeDef:
        """
        Lists the IDs of the applications that you are monitoring.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-insights.html#ApplicationInsights.Client.list_applications)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_insights/client/#list_applications)
        """

    async def list_components(
        self, *, ResourceGroupName: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListComponentsResponseTypeDef:
        """
        Lists the auto-grouped, standalone, and custom components of the application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-insights.html#ApplicationInsights.Client.list_components)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_insights/client/#list_components)
        """

    async def list_configuration_history(
        self,
        *,
        ResourceGroupName: str = ...,
        StartTime: Union[datetime, str] = ...,
        EndTime: Union[datetime, str] = ...,
        EventStatus: ConfigurationEventStatusType = ...,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> ListConfigurationHistoryResponseTypeDef:
        """
        Lists the INFO, WARN, and ERROR events for periodic configuration updates
        performed by Application Insights.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-insights.html#ApplicationInsights.Client.list_configuration_history)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_insights/client/#list_configuration_history)
        """

    async def list_log_pattern_sets(
        self, *, ResourceGroupName: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListLogPatternSetsResponseTypeDef:
        """
        Lists the log pattern sets in the specific application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-insights.html#ApplicationInsights.Client.list_log_pattern_sets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_insights/client/#list_log_pattern_sets)
        """

    async def list_log_patterns(
        self,
        *,
        ResourceGroupName: str,
        PatternSetName: str = ...,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> ListLogPatternsResponseTypeDef:
        """
        Lists the log patterns in the specific log `LogPatternSet` .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-insights.html#ApplicationInsights.Client.list_log_patterns)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_insights/client/#list_log_patterns)
        """

    async def list_problems(
        self,
        *,
        ResourceGroupName: str = ...,
        StartTime: Union[datetime, str] = ...,
        EndTime: Union[datetime, str] = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
        ComponentName: str = ...
    ) -> ListProblemsResponseTypeDef:
        """
        Lists the problems with your application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-insights.html#ApplicationInsights.Client.list_problems)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_insights/client/#list_problems)
        """

    async def list_tags_for_resource(
        self, *, ResourceARN: str
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Retrieve a list of the tags (keys and values) that are associated with a
        specified application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-insights.html#ApplicationInsights.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_insights/client/#list_tags_for_resource)
        """

    async def tag_resource(
        self, *, ResourceARN: str, Tags: Sequence["TagTypeDef"]
    ) -> Dict[str, Any]:
        """
        Add one or more tags (keys and values) to a specified application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-insights.html#ApplicationInsights.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_insights/client/#tag_resource)
        """

    async def untag_resource(self, *, ResourceARN: str, TagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Remove one or more tags (keys and values) from a specified application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-insights.html#ApplicationInsights.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_insights/client/#untag_resource)
        """

    async def update_application(
        self,
        *,
        ResourceGroupName: str,
        OpsCenterEnabled: bool = ...,
        CWEMonitorEnabled: bool = ...,
        OpsItemSNSTopicArn: str = ...,
        RemoveSNSTopic: bool = ...,
        AutoConfigEnabled: bool = ...
    ) -> UpdateApplicationResponseTypeDef:
        """
        Updates the application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-insights.html#ApplicationInsights.Client.update_application)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_insights/client/#update_application)
        """

    async def update_component(
        self,
        *,
        ResourceGroupName: str,
        ComponentName: str,
        NewComponentName: str = ...,
        ResourceList: Sequence[str] = ...
    ) -> Dict[str, Any]:
        """
        Updates the custom component name and/or the list of resources that make up the
        component.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-insights.html#ApplicationInsights.Client.update_component)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_insights/client/#update_component)
        """

    async def update_component_configuration(
        self,
        *,
        ResourceGroupName: str,
        ComponentName: str,
        Monitor: bool = ...,
        Tier: TierType = ...,
        ComponentConfiguration: str = ...,
        AutoConfigEnabled: bool = ...
    ) -> Dict[str, Any]:
        """
        Updates the monitoring configurations for the component.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-insights.html#ApplicationInsights.Client.update_component_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_insights/client/#update_component_configuration)
        """

    async def update_log_pattern(
        self,
        *,
        ResourceGroupName: str,
        PatternSetName: str,
        PatternName: str,
        Pattern: str = ...,
        Rank: int = ...
    ) -> UpdateLogPatternResponseTypeDef:
        """
        Adds a log pattern to a `LogPatternSet` .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-insights.html#ApplicationInsights.Client.update_log_pattern)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_insights/client/#update_log_pattern)
        """

    async def __aenter__(self) -> "ApplicationInsightsClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-insights.html#ApplicationInsights.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_insights/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-insights.html#ApplicationInsights.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_insights/client/)
        """
