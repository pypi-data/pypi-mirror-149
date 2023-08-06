"""
Type annotations for migrationhubstrategy service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhubstrategy/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_migrationhubstrategy.client import MigrationHubStrategyRecommendationsClient

    session = get_session()
    async with session.create_client("migrationhubstrategy") as client:
        client: MigrationHubStrategyRecommendationsClient
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import (
    ApplicationComponentCriteriaType,
    DataSourceTypeType,
    InclusionStatusType,
    OutputFormatType,
    ServerCriteriaType,
    SortOrderType,
)
from .paginator import (
    GetServerDetailsPaginator,
    ListApplicationComponentsPaginator,
    ListCollectorsPaginator,
    ListImportFileTaskPaginator,
    ListServersPaginator,
)
from .type_defs import (
    ApplicationPreferencesTypeDef,
    DatabasePreferencesTypeDef,
    GetApplicationComponentDetailsResponseTypeDef,
    GetApplicationComponentStrategiesResponseTypeDef,
    GetAssessmentResponseTypeDef,
    GetImportFileTaskResponseTypeDef,
    GetPortfolioPreferencesResponseTypeDef,
    GetPortfolioSummaryResponseTypeDef,
    GetRecommendationReportDetailsResponseTypeDef,
    GetServerDetailsResponseTypeDef,
    GetServerStrategiesResponseTypeDef,
    GroupTypeDef,
    ListApplicationComponentsResponseTypeDef,
    ListCollectorsResponseTypeDef,
    ListImportFileTaskResponseTypeDef,
    ListServersResponseTypeDef,
    PrioritizeBusinessGoalsTypeDef,
    SourceCodeTypeDef,
    StartAssessmentResponseTypeDef,
    StartImportFileTaskResponseTypeDef,
    StartRecommendationReportGenerationResponseTypeDef,
    StrategyOptionTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("MigrationHubStrategyRecommendationsClient",)


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
    ServiceLinkedRoleLockClientException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class MigrationHubStrategyRecommendationsClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy.html#MigrationHubStrategyRecommendations.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhubstrategy/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        MigrationHubStrategyRecommendationsClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy.html#MigrationHubStrategyRecommendations.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhubstrategy/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy.html#MigrationHubStrategyRecommendations.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhubstrategy/client/#can_paginate)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy.html#MigrationHubStrategyRecommendations.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhubstrategy/client/#generate_presigned_url)
        """

    async def get_application_component_details(
        self, *, applicationComponentId: str
    ) -> GetApplicationComponentDetailsResponseTypeDef:
        """
        Retrieves details about an application component.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy.html#MigrationHubStrategyRecommendations.Client.get_application_component_details)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhubstrategy/client/#get_application_component_details)
        """

    async def get_application_component_strategies(
        self, *, applicationComponentId: str
    ) -> GetApplicationComponentStrategiesResponseTypeDef:
        """
        Retrieves a list of all the recommended strategies and tools for an application
        component running on a server.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy.html#MigrationHubStrategyRecommendations.Client.get_application_component_strategies)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhubstrategy/client/#get_application_component_strategies)
        """

    async def get_assessment(self, *, id: str) -> GetAssessmentResponseTypeDef:
        """
        Retrieves the status of an on-going assessment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy.html#MigrationHubStrategyRecommendations.Client.get_assessment)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhubstrategy/client/#get_assessment)
        """

    async def get_import_file_task(self, *, id: str) -> GetImportFileTaskResponseTypeDef:
        """
        Retrieves the details about a specific import task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy.html#MigrationHubStrategyRecommendations.Client.get_import_file_task)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhubstrategy/client/#get_import_file_task)
        """

    async def get_portfolio_preferences(self) -> GetPortfolioPreferencesResponseTypeDef:
        """
        Retrieves your migration and modernization preferences.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy.html#MigrationHubStrategyRecommendations.Client.get_portfolio_preferences)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhubstrategy/client/#get_portfolio_preferences)
        """

    async def get_portfolio_summary(self) -> GetPortfolioSummaryResponseTypeDef:
        """
        Retrieves overall summary including the number of servers to rehost and the
        overall number of anti-patterns.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy.html#MigrationHubStrategyRecommendations.Client.get_portfolio_summary)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhubstrategy/client/#get_portfolio_summary)
        """

    async def get_recommendation_report_details(
        self, *, id: str
    ) -> GetRecommendationReportDetailsResponseTypeDef:
        """
        Retrieves detailed information about the specified recommendation report.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy.html#MigrationHubStrategyRecommendations.Client.get_recommendation_report_details)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhubstrategy/client/#get_recommendation_report_details)
        """

    async def get_server_details(
        self, *, serverId: str, maxResults: int = ..., nextToken: str = ...
    ) -> GetServerDetailsResponseTypeDef:
        """
        Retrieves detailed information about a specified server.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy.html#MigrationHubStrategyRecommendations.Client.get_server_details)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhubstrategy/client/#get_server_details)
        """

    async def get_server_strategies(self, *, serverId: str) -> GetServerStrategiesResponseTypeDef:
        """
        Retrieves recommended strategies and tools for the specified server.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy.html#MigrationHubStrategyRecommendations.Client.get_server_strategies)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhubstrategy/client/#get_server_strategies)
        """

    async def list_application_components(
        self,
        *,
        applicationComponentCriteria: ApplicationComponentCriteriaType = ...,
        filterValue: str = ...,
        groupIdFilter: Sequence["GroupTypeDef"] = ...,
        maxResults: int = ...,
        nextToken: str = ...,
        sort: SortOrderType = ...
    ) -> ListApplicationComponentsResponseTypeDef:
        """
        Retrieves a list of all the application components (processes).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy.html#MigrationHubStrategyRecommendations.Client.list_application_components)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhubstrategy/client/#list_application_components)
        """

    async def list_collectors(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> ListCollectorsResponseTypeDef:
        """
        Retrieves a list of all the installed collectors.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy.html#MigrationHubStrategyRecommendations.Client.list_collectors)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhubstrategy/client/#list_collectors)
        """

    async def list_import_file_task(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> ListImportFileTaskResponseTypeDef:
        """
        Retrieves a list of all the imports performed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy.html#MigrationHubStrategyRecommendations.Client.list_import_file_task)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhubstrategy/client/#list_import_file_task)
        """

    async def list_servers(
        self,
        *,
        filterValue: str = ...,
        groupIdFilter: Sequence["GroupTypeDef"] = ...,
        maxResults: int = ...,
        nextToken: str = ...,
        serverCriteria: ServerCriteriaType = ...,
        sort: SortOrderType = ...
    ) -> ListServersResponseTypeDef:
        """
        Returns a list of all the servers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy.html#MigrationHubStrategyRecommendations.Client.list_servers)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhubstrategy/client/#list_servers)
        """

    async def put_portfolio_preferences(
        self,
        *,
        applicationPreferences: "ApplicationPreferencesTypeDef" = ...,
        databasePreferences: "DatabasePreferencesTypeDef" = ...,
        prioritizeBusinessGoals: "PrioritizeBusinessGoalsTypeDef" = ...
    ) -> Dict[str, Any]:
        """
        Saves the specified migration and modernization preferences.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy.html#MigrationHubStrategyRecommendations.Client.put_portfolio_preferences)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhubstrategy/client/#put_portfolio_preferences)
        """

    async def start_assessment(
        self, *, s3bucketForAnalysisData: str = ..., s3bucketForReportData: str = ...
    ) -> StartAssessmentResponseTypeDef:
        """
        Starts the assessment of an on-premises environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy.html#MigrationHubStrategyRecommendations.Client.start_assessment)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhubstrategy/client/#start_assessment)
        """

    async def start_import_file_task(
        self,
        *,
        S3Bucket: str,
        name: str,
        s3key: str,
        dataSourceType: DataSourceTypeType = ...,
        groupId: Sequence["GroupTypeDef"] = ...,
        s3bucketForReportData: str = ...
    ) -> StartImportFileTaskResponseTypeDef:
        """
        Starts a file import.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy.html#MigrationHubStrategyRecommendations.Client.start_import_file_task)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhubstrategy/client/#start_import_file_task)
        """

    async def start_recommendation_report_generation(
        self, *, groupIdFilter: Sequence["GroupTypeDef"] = ..., outputFormat: OutputFormatType = ...
    ) -> StartRecommendationReportGenerationResponseTypeDef:
        """
        Starts generating a recommendation report.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy.html#MigrationHubStrategyRecommendations.Client.start_recommendation_report_generation)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhubstrategy/client/#start_recommendation_report_generation)
        """

    async def stop_assessment(self, *, assessmentId: str) -> Dict[str, Any]:
        """
        Stops the assessment of an on-premises environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy.html#MigrationHubStrategyRecommendations.Client.stop_assessment)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhubstrategy/client/#stop_assessment)
        """

    async def update_application_component_config(
        self,
        *,
        applicationComponentId: str,
        inclusionStatus: InclusionStatusType = ...,
        secretsManagerKey: str = ...,
        sourceCodeList: Sequence["SourceCodeTypeDef"] = ...,
        strategyOption: "StrategyOptionTypeDef" = ...
    ) -> Dict[str, Any]:
        """
        Updates the configuration of an application component.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy.html#MigrationHubStrategyRecommendations.Client.update_application_component_config)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhubstrategy/client/#update_application_component_config)
        """

    async def update_server_config(
        self, *, serverId: str, strategyOption: "StrategyOptionTypeDef" = ...
    ) -> Dict[str, Any]:
        """
        Updates the configuration of the specified server.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy.html#MigrationHubStrategyRecommendations.Client.update_server_config)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhubstrategy/client/#update_server_config)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_server_details"]
    ) -> GetServerDetailsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy.html#MigrationHubStrategyRecommendations.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhubstrategy/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_application_components"]
    ) -> ListApplicationComponentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy.html#MigrationHubStrategyRecommendations.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhubstrategy/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_collectors"]) -> ListCollectorsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy.html#MigrationHubStrategyRecommendations.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhubstrategy/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_import_file_task"]
    ) -> ListImportFileTaskPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy.html#MigrationHubStrategyRecommendations.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhubstrategy/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_servers"]) -> ListServersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy.html#MigrationHubStrategyRecommendations.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhubstrategy/client/#get_paginator)
        """

    async def __aenter__(self) -> "MigrationHubStrategyRecommendationsClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy.html#MigrationHubStrategyRecommendations.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhubstrategy/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhubstrategy.html#MigrationHubStrategyRecommendations.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhubstrategy/client/)
        """
