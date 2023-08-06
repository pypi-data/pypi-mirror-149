"""
Type annotations for glue service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_glue.client import GlueClient

    session = get_session()
    async with session.create_client("glue") as client:
        client: GlueClient
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, Mapping, Sequence, Type, Union, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import (
    CompatibilityType,
    DataFormatType,
    EnableHybridValuesType,
    ExistConditionType,
    LanguageType,
    PermissionTypeType,
    ResourceShareTypeType,
    TriggerTypeType,
    WorkerTypeType,
)
from .paginator import (
    GetClassifiersPaginator,
    GetConnectionsPaginator,
    GetCrawlerMetricsPaginator,
    GetCrawlersPaginator,
    GetDatabasesPaginator,
    GetDevEndpointsPaginator,
    GetJobRunsPaginator,
    GetJobsPaginator,
    GetPartitionIndexesPaginator,
    GetPartitionsPaginator,
    GetResourcePoliciesPaginator,
    GetSecurityConfigurationsPaginator,
    GetTablesPaginator,
    GetTableVersionsPaginator,
    GetTriggersPaginator,
    GetUserDefinedFunctionsPaginator,
    ListRegistriesPaginator,
    ListSchemasPaginator,
    ListSchemaVersionsPaginator,
)
from .type_defs import (
    ActionTypeDef,
    AuditContextTypeDef,
    BatchCreatePartitionResponseTypeDef,
    BatchDeleteConnectionResponseTypeDef,
    BatchDeletePartitionResponseTypeDef,
    BatchDeleteTableResponseTypeDef,
    BatchDeleteTableVersionResponseTypeDef,
    BatchGetBlueprintsResponseTypeDef,
    BatchGetCrawlersResponseTypeDef,
    BatchGetDevEndpointsResponseTypeDef,
    BatchGetJobsResponseTypeDef,
    BatchGetPartitionResponseTypeDef,
    BatchGetTriggersResponseTypeDef,
    BatchGetWorkflowsResponseTypeDef,
    BatchStopJobRunResponseTypeDef,
    BatchUpdatePartitionRequestEntryTypeDef,
    BatchUpdatePartitionResponseTypeDef,
    CancelMLTaskRunResponseTypeDef,
    CatalogEntryTypeDef,
    CheckSchemaVersionValidityResponseTypeDef,
    CodeGenEdgeTypeDef,
    CodeGenNodeTypeDef,
    ColumnStatisticsTypeDef,
    ConnectionInputTypeDef,
    ConnectionsListTypeDef,
    CrawlerTargetsTypeDef,
    CreateBlueprintResponseTypeDef,
    CreateCsvClassifierRequestTypeDef,
    CreateDevEndpointResponseTypeDef,
    CreateGrokClassifierRequestTypeDef,
    CreateJobResponseTypeDef,
    CreateJsonClassifierRequestTypeDef,
    CreateMLTransformResponseTypeDef,
    CreateRegistryResponseTypeDef,
    CreateSchemaResponseTypeDef,
    CreateScriptResponseTypeDef,
    CreateSecurityConfigurationResponseTypeDef,
    CreateTriggerResponseTypeDef,
    CreateWorkflowResponseTypeDef,
    CreateXMLClassifierRequestTypeDef,
    DatabaseInputTypeDef,
    DataCatalogEncryptionSettingsTypeDef,
    DeleteBlueprintResponseTypeDef,
    DeleteJobResponseTypeDef,
    DeleteMLTransformResponseTypeDef,
    DeleteRegistryResponseTypeDef,
    DeleteSchemaResponseTypeDef,
    DeleteSchemaVersionsResponseTypeDef,
    DeleteTriggerResponseTypeDef,
    DeleteWorkflowResponseTypeDef,
    DevEndpointCustomLibrariesTypeDef,
    EncryptionConfigurationTypeDef,
    EventBatchingConditionTypeDef,
    ExecutionPropertyTypeDef,
    GetBlueprintResponseTypeDef,
    GetBlueprintRunResponseTypeDef,
    GetBlueprintRunsResponseTypeDef,
    GetCatalogImportStatusResponseTypeDef,
    GetClassifierResponseTypeDef,
    GetClassifiersResponseTypeDef,
    GetColumnStatisticsForPartitionResponseTypeDef,
    GetColumnStatisticsForTableResponseTypeDef,
    GetConnectionResponseTypeDef,
    GetConnectionsFilterTypeDef,
    GetConnectionsResponseTypeDef,
    GetCrawlerMetricsResponseTypeDef,
    GetCrawlerResponseTypeDef,
    GetCrawlersResponseTypeDef,
    GetDatabaseResponseTypeDef,
    GetDatabasesResponseTypeDef,
    GetDataCatalogEncryptionSettingsResponseTypeDef,
    GetDataflowGraphResponseTypeDef,
    GetDevEndpointResponseTypeDef,
    GetDevEndpointsResponseTypeDef,
    GetJobBookmarkResponseTypeDef,
    GetJobResponseTypeDef,
    GetJobRunResponseTypeDef,
    GetJobRunsResponseTypeDef,
    GetJobsResponseTypeDef,
    GetMappingResponseTypeDef,
    GetMLTaskRunResponseTypeDef,
    GetMLTaskRunsResponseTypeDef,
    GetMLTransformResponseTypeDef,
    GetMLTransformsResponseTypeDef,
    GetPartitionIndexesResponseTypeDef,
    GetPartitionResponseTypeDef,
    GetPartitionsResponseTypeDef,
    GetPlanResponseTypeDef,
    GetRegistryResponseTypeDef,
    GetResourcePoliciesResponseTypeDef,
    GetResourcePolicyResponseTypeDef,
    GetSchemaByDefinitionResponseTypeDef,
    GetSchemaResponseTypeDef,
    GetSchemaVersionResponseTypeDef,
    GetSchemaVersionsDiffResponseTypeDef,
    GetSecurityConfigurationResponseTypeDef,
    GetSecurityConfigurationsResponseTypeDef,
    GetTableResponseTypeDef,
    GetTablesResponseTypeDef,
    GetTableVersionResponseTypeDef,
    GetTableVersionsResponseTypeDef,
    GetTagsResponseTypeDef,
    GetTriggerResponseTypeDef,
    GetTriggersResponseTypeDef,
    GetUnfilteredPartitionMetadataResponseTypeDef,
    GetUnfilteredPartitionsMetadataResponseTypeDef,
    GetUnfilteredTableMetadataResponseTypeDef,
    GetUserDefinedFunctionResponseTypeDef,
    GetUserDefinedFunctionsResponseTypeDef,
    GetWorkflowResponseTypeDef,
    GetWorkflowRunPropertiesResponseTypeDef,
    GetWorkflowRunResponseTypeDef,
    GetWorkflowRunsResponseTypeDef,
    GlueTableTypeDef,
    JobCommandTypeDef,
    JobUpdateTypeDef,
    LakeFormationConfigurationTypeDef,
    LineageConfigurationTypeDef,
    ListBlueprintsResponseTypeDef,
    ListCrawlersResponseTypeDef,
    ListDevEndpointsResponseTypeDef,
    ListJobsResponseTypeDef,
    ListMLTransformsResponseTypeDef,
    ListRegistriesResponseTypeDef,
    ListSchemasResponseTypeDef,
    ListSchemaVersionsResponseTypeDef,
    ListTriggersResponseTypeDef,
    ListWorkflowsResponseTypeDef,
    LocationTypeDef,
    MappingEntryTypeDef,
    MetadataKeyValuePairTypeDef,
    NotificationPropertyTypeDef,
    PartitionIndexTypeDef,
    PartitionInputTypeDef,
    PartitionValueListTypeDef,
    PredicateTypeDef,
    PropertyPredicateTypeDef,
    PutResourcePolicyResponseTypeDef,
    PutSchemaVersionMetadataResponseTypeDef,
    QuerySchemaVersionMetadataResponseTypeDef,
    RecrawlPolicyTypeDef,
    RegisterSchemaVersionResponseTypeDef,
    RegistryIdTypeDef,
    RemoveSchemaVersionMetadataResponseTypeDef,
    ResetJobBookmarkResponseTypeDef,
    ResumeWorkflowRunResponseTypeDef,
    SchemaChangePolicyTypeDef,
    SchemaIdTypeDef,
    SchemaVersionNumberTypeDef,
    SearchTablesResponseTypeDef,
    SegmentTypeDef,
    SortCriterionTypeDef,
    StartBlueprintRunResponseTypeDef,
    StartExportLabelsTaskRunResponseTypeDef,
    StartImportLabelsTaskRunResponseTypeDef,
    StartJobRunResponseTypeDef,
    StartMLEvaluationTaskRunResponseTypeDef,
    StartMLLabelingSetGenerationTaskRunResponseTypeDef,
    StartTriggerResponseTypeDef,
    StartWorkflowRunResponseTypeDef,
    StopTriggerResponseTypeDef,
    TableInputTypeDef,
    TaskRunFilterCriteriaTypeDef,
    TaskRunSortCriteriaTypeDef,
    TransformEncryptionTypeDef,
    TransformFilterCriteriaTypeDef,
    TransformParametersTypeDef,
    TransformSortCriteriaTypeDef,
    TriggerUpdateTypeDef,
    UpdateBlueprintResponseTypeDef,
    UpdateColumnStatisticsForPartitionResponseTypeDef,
    UpdateColumnStatisticsForTableResponseTypeDef,
    UpdateCsvClassifierRequestTypeDef,
    UpdateGrokClassifierRequestTypeDef,
    UpdateJobResponseTypeDef,
    UpdateJsonClassifierRequestTypeDef,
    UpdateMLTransformResponseTypeDef,
    UpdateRegistryResponseTypeDef,
    UpdateSchemaResponseTypeDef,
    UpdateTriggerResponseTypeDef,
    UpdateWorkflowResponseTypeDef,
    UpdateXMLClassifierRequestTypeDef,
    UserDefinedFunctionInputTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("GlueClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    AlreadyExistsException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConcurrentModificationException: Type[BotocoreClientError]
    ConcurrentRunsExceededException: Type[BotocoreClientError]
    ConditionCheckFailureException: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    CrawlerNotRunningException: Type[BotocoreClientError]
    CrawlerRunningException: Type[BotocoreClientError]
    CrawlerStoppingException: Type[BotocoreClientError]
    EntityNotFoundException: Type[BotocoreClientError]
    GlueEncryptionException: Type[BotocoreClientError]
    IdempotentParameterMismatchException: Type[BotocoreClientError]
    IllegalBlueprintStateException: Type[BotocoreClientError]
    IllegalWorkflowStateException: Type[BotocoreClientError]
    InternalServiceException: Type[BotocoreClientError]
    InvalidInputException: Type[BotocoreClientError]
    InvalidStateException: Type[BotocoreClientError]
    MLTransformNotReadyException: Type[BotocoreClientError]
    NoScheduleException: Type[BotocoreClientError]
    OperationTimeoutException: Type[BotocoreClientError]
    PermissionTypeMismatchException: Type[BotocoreClientError]
    ResourceNotReadyException: Type[BotocoreClientError]
    ResourceNumberLimitExceededException: Type[BotocoreClientError]
    SchedulerNotRunningException: Type[BotocoreClientError]
    SchedulerRunningException: Type[BotocoreClientError]
    SchedulerTransitioningException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]
    VersionMismatchException: Type[BotocoreClientError]


class GlueClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        GlueClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#exceptions)
        """

    async def batch_create_partition(
        self,
        *,
        DatabaseName: str,
        TableName: str,
        PartitionInputList: Sequence["PartitionInputTypeDef"],
        CatalogId: str = ...
    ) -> BatchCreatePartitionResponseTypeDef:
        """
        Creates one or more partitions in a batch operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.batch_create_partition)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#batch_create_partition)
        """

    async def batch_delete_connection(
        self, *, ConnectionNameList: Sequence[str], CatalogId: str = ...
    ) -> BatchDeleteConnectionResponseTypeDef:
        """
        Deletes a list of connection definitions from the Data Catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.batch_delete_connection)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#batch_delete_connection)
        """

    async def batch_delete_partition(
        self,
        *,
        DatabaseName: str,
        TableName: str,
        PartitionsToDelete: Sequence["PartitionValueListTypeDef"],
        CatalogId: str = ...
    ) -> BatchDeletePartitionResponseTypeDef:
        """
        Deletes one or more partitions in a batch operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.batch_delete_partition)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#batch_delete_partition)
        """

    async def batch_delete_table(
        self,
        *,
        DatabaseName: str,
        TablesToDelete: Sequence[str],
        CatalogId: str = ...,
        TransactionId: str = ...
    ) -> BatchDeleteTableResponseTypeDef:
        """
        Deletes multiple tables at once.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.batch_delete_table)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#batch_delete_table)
        """

    async def batch_delete_table_version(
        self, *, DatabaseName: str, TableName: str, VersionIds: Sequence[str], CatalogId: str = ...
    ) -> BatchDeleteTableVersionResponseTypeDef:
        """
        Deletes a specified batch of versions of a table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.batch_delete_table_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#batch_delete_table_version)
        """

    async def batch_get_blueprints(
        self,
        *,
        Names: Sequence[str],
        IncludeBlueprint: bool = ...,
        IncludeParameterSpec: bool = ...
    ) -> BatchGetBlueprintsResponseTypeDef:
        """
        Retrieves information about a list of blueprints.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.batch_get_blueprints)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#batch_get_blueprints)
        """

    async def batch_get_crawlers(
        self, *, CrawlerNames: Sequence[str]
    ) -> BatchGetCrawlersResponseTypeDef:
        """
        Returns a list of resource metadata for a given list of crawler names.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.batch_get_crawlers)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#batch_get_crawlers)
        """

    async def batch_get_dev_endpoints(
        self, *, DevEndpointNames: Sequence[str]
    ) -> BatchGetDevEndpointsResponseTypeDef:
        """
        Returns a list of resource metadata for a given list of development endpoint
        names.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.batch_get_dev_endpoints)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#batch_get_dev_endpoints)
        """

    async def batch_get_jobs(self, *, JobNames: Sequence[str]) -> BatchGetJobsResponseTypeDef:
        """
        Returns a list of resource metadata for a given list of job names.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.batch_get_jobs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#batch_get_jobs)
        """

    async def batch_get_partition(
        self,
        *,
        DatabaseName: str,
        TableName: str,
        PartitionsToGet: Sequence["PartitionValueListTypeDef"],
        CatalogId: str = ...
    ) -> BatchGetPartitionResponseTypeDef:
        """
        Retrieves partitions in a batch request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.batch_get_partition)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#batch_get_partition)
        """

    async def batch_get_triggers(
        self, *, TriggerNames: Sequence[str]
    ) -> BatchGetTriggersResponseTypeDef:
        """
        Returns a list of resource metadata for a given list of trigger names.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.batch_get_triggers)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#batch_get_triggers)
        """

    async def batch_get_workflows(
        self, *, Names: Sequence[str], IncludeGraph: bool = ...
    ) -> BatchGetWorkflowsResponseTypeDef:
        """
        Returns a list of resource metadata for a given list of workflow names.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.batch_get_workflows)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#batch_get_workflows)
        """

    async def batch_stop_job_run(
        self, *, JobName: str, JobRunIds: Sequence[str]
    ) -> BatchStopJobRunResponseTypeDef:
        """
        Stops one or more job runs for a specified job definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.batch_stop_job_run)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#batch_stop_job_run)
        """

    async def batch_update_partition(
        self,
        *,
        DatabaseName: str,
        TableName: str,
        Entries: Sequence["BatchUpdatePartitionRequestEntryTypeDef"],
        CatalogId: str = ...
    ) -> BatchUpdatePartitionResponseTypeDef:
        """
        Updates one or more partitions in a batch operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.batch_update_partition)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#batch_update_partition)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#can_paginate)
        """

    async def cancel_ml_task_run(
        self, *, TransformId: str, TaskRunId: str
    ) -> CancelMLTaskRunResponseTypeDef:
        """
        Cancels (stops) a task run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.cancel_ml_task_run)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#cancel_ml_task_run)
        """

    async def check_schema_version_validity(
        self, *, DataFormat: DataFormatType, SchemaDefinition: str
    ) -> CheckSchemaVersionValidityResponseTypeDef:
        """
        Validates the supplied schema.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.check_schema_version_validity)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#check_schema_version_validity)
        """

    async def create_blueprint(
        self,
        *,
        Name: str,
        BlueprintLocation: str,
        Description: str = ...,
        Tags: Mapping[str, str] = ...
    ) -> CreateBlueprintResponseTypeDef:
        """
        Registers a blueprint with Glue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.create_blueprint)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#create_blueprint)
        """

    async def create_classifier(
        self,
        *,
        GrokClassifier: "CreateGrokClassifierRequestTypeDef" = ...,
        XMLClassifier: "CreateXMLClassifierRequestTypeDef" = ...,
        JsonClassifier: "CreateJsonClassifierRequestTypeDef" = ...,
        CsvClassifier: "CreateCsvClassifierRequestTypeDef" = ...
    ) -> Dict[str, Any]:
        """
        Creates a classifier in the user's account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.create_classifier)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#create_classifier)
        """

    async def create_connection(
        self,
        *,
        ConnectionInput: "ConnectionInputTypeDef",
        CatalogId: str = ...,
        Tags: Mapping[str, str] = ...
    ) -> Dict[str, Any]:
        """
        Creates a connection definition in the Data Catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.create_connection)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#create_connection)
        """

    async def create_crawler(
        self,
        *,
        Name: str,
        Role: str,
        Targets: "CrawlerTargetsTypeDef",
        DatabaseName: str = ...,
        Description: str = ...,
        Schedule: str = ...,
        Classifiers: Sequence[str] = ...,
        TablePrefix: str = ...,
        SchemaChangePolicy: "SchemaChangePolicyTypeDef" = ...,
        RecrawlPolicy: "RecrawlPolicyTypeDef" = ...,
        LineageConfiguration: "LineageConfigurationTypeDef" = ...,
        LakeFormationConfiguration: "LakeFormationConfigurationTypeDef" = ...,
        Configuration: str = ...,
        CrawlerSecurityConfiguration: str = ...,
        Tags: Mapping[str, str] = ...
    ) -> Dict[str, Any]:
        """
        Creates a new crawler with specified targets, role, configuration, and optional
        schedule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.create_crawler)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#create_crawler)
        """

    async def create_database(
        self, *, DatabaseInput: "DatabaseInputTypeDef", CatalogId: str = ...
    ) -> Dict[str, Any]:
        """
        Creates a new database in a Data Catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.create_database)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#create_database)
        """

    async def create_dev_endpoint(
        self,
        *,
        EndpointName: str,
        RoleArn: str,
        SecurityGroupIds: Sequence[str] = ...,
        SubnetId: str = ...,
        PublicKey: str = ...,
        PublicKeys: Sequence[str] = ...,
        NumberOfNodes: int = ...,
        WorkerType: WorkerTypeType = ...,
        GlueVersion: str = ...,
        NumberOfWorkers: int = ...,
        ExtraPythonLibsS3Path: str = ...,
        ExtraJarsS3Path: str = ...,
        SecurityConfiguration: str = ...,
        Tags: Mapping[str, str] = ...,
        Arguments: Mapping[str, str] = ...
    ) -> CreateDevEndpointResponseTypeDef:
        """
        Creates a new development endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.create_dev_endpoint)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#create_dev_endpoint)
        """

    async def create_job(
        self,
        *,
        Name: str,
        Role: str,
        Command: "JobCommandTypeDef",
        Description: str = ...,
        LogUri: str = ...,
        ExecutionProperty: "ExecutionPropertyTypeDef" = ...,
        DefaultArguments: Mapping[str, str] = ...,
        NonOverridableArguments: Mapping[str, str] = ...,
        Connections: "ConnectionsListTypeDef" = ...,
        MaxRetries: int = ...,
        AllocatedCapacity: int = ...,
        Timeout: int = ...,
        MaxCapacity: float = ...,
        SecurityConfiguration: str = ...,
        Tags: Mapping[str, str] = ...,
        NotificationProperty: "NotificationPropertyTypeDef" = ...,
        GlueVersion: str = ...,
        NumberOfWorkers: int = ...,
        WorkerType: WorkerTypeType = ...
    ) -> CreateJobResponseTypeDef:
        """
        Creates a new job definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.create_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#create_job)
        """

    async def create_ml_transform(
        self,
        *,
        Name: str,
        InputRecordTables: Sequence["GlueTableTypeDef"],
        Parameters: "TransformParametersTypeDef",
        Role: str,
        Description: str = ...,
        GlueVersion: str = ...,
        MaxCapacity: float = ...,
        WorkerType: WorkerTypeType = ...,
        NumberOfWorkers: int = ...,
        Timeout: int = ...,
        MaxRetries: int = ...,
        Tags: Mapping[str, str] = ...,
        TransformEncryption: "TransformEncryptionTypeDef" = ...
    ) -> CreateMLTransformResponseTypeDef:
        """
        Creates an Glue machine learning transform.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.create_ml_transform)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#create_ml_transform)
        """

    async def create_partition(
        self,
        *,
        DatabaseName: str,
        TableName: str,
        PartitionInput: "PartitionInputTypeDef",
        CatalogId: str = ...
    ) -> Dict[str, Any]:
        """
        Creates a new partition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.create_partition)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#create_partition)
        """

    async def create_partition_index(
        self,
        *,
        DatabaseName: str,
        TableName: str,
        PartitionIndex: "PartitionIndexTypeDef",
        CatalogId: str = ...
    ) -> Dict[str, Any]:
        """
        Creates a specified partition index in an existing table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.create_partition_index)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#create_partition_index)
        """

    async def create_registry(
        self, *, RegistryName: str, Description: str = ..., Tags: Mapping[str, str] = ...
    ) -> CreateRegistryResponseTypeDef:
        """
        Creates a new registry which may be used to hold a collection of schemas.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.create_registry)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#create_registry)
        """

    async def create_schema(
        self,
        *,
        SchemaName: str,
        DataFormat: DataFormatType,
        RegistryId: "RegistryIdTypeDef" = ...,
        Compatibility: CompatibilityType = ...,
        Description: str = ...,
        Tags: Mapping[str, str] = ...,
        SchemaDefinition: str = ...
    ) -> CreateSchemaResponseTypeDef:
        """
        Creates a new schema set and registers the schema definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.create_schema)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#create_schema)
        """

    async def create_script(
        self,
        *,
        DagNodes: Sequence["CodeGenNodeTypeDef"] = ...,
        DagEdges: Sequence["CodeGenEdgeTypeDef"] = ...,
        Language: LanguageType = ...
    ) -> CreateScriptResponseTypeDef:
        """
        Transforms a directed acyclic graph (DAG) into code.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.create_script)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#create_script)
        """

    async def create_security_configuration(
        self, *, Name: str, EncryptionConfiguration: "EncryptionConfigurationTypeDef"
    ) -> CreateSecurityConfigurationResponseTypeDef:
        """
        Creates a new security configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.create_security_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#create_security_configuration)
        """

    async def create_table(
        self,
        *,
        DatabaseName: str,
        TableInput: "TableInputTypeDef",
        CatalogId: str = ...,
        PartitionIndexes: Sequence["PartitionIndexTypeDef"] = ...,
        TransactionId: str = ...
    ) -> Dict[str, Any]:
        """
        Creates a new table definition in the Data Catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.create_table)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#create_table)
        """

    async def create_trigger(
        self,
        *,
        Name: str,
        Type: TriggerTypeType,
        Actions: Sequence["ActionTypeDef"],
        WorkflowName: str = ...,
        Schedule: str = ...,
        Predicate: "PredicateTypeDef" = ...,
        Description: str = ...,
        StartOnCreation: bool = ...,
        Tags: Mapping[str, str] = ...,
        EventBatchingCondition: "EventBatchingConditionTypeDef" = ...
    ) -> CreateTriggerResponseTypeDef:
        """
        Creates a new trigger.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.create_trigger)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#create_trigger)
        """

    async def create_user_defined_function(
        self,
        *,
        DatabaseName: str,
        FunctionInput: "UserDefinedFunctionInputTypeDef",
        CatalogId: str = ...
    ) -> Dict[str, Any]:
        """
        Creates a new function definition in the Data Catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.create_user_defined_function)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#create_user_defined_function)
        """

    async def create_workflow(
        self,
        *,
        Name: str,
        Description: str = ...,
        DefaultRunProperties: Mapping[str, str] = ...,
        Tags: Mapping[str, str] = ...,
        MaxConcurrentRuns: int = ...
    ) -> CreateWorkflowResponseTypeDef:
        """
        Creates a new workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.create_workflow)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#create_workflow)
        """

    async def delete_blueprint(self, *, Name: str) -> DeleteBlueprintResponseTypeDef:
        """
        Deletes an existing blueprint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.delete_blueprint)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#delete_blueprint)
        """

    async def delete_classifier(self, *, Name: str) -> Dict[str, Any]:
        """
        Removes a classifier from the Data Catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.delete_classifier)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#delete_classifier)
        """

    async def delete_column_statistics_for_partition(
        self,
        *,
        DatabaseName: str,
        TableName: str,
        PartitionValues: Sequence[str],
        ColumnName: str,
        CatalogId: str = ...
    ) -> Dict[str, Any]:
        """
        Delete the partition column statistics of a column.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.delete_column_statistics_for_partition)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#delete_column_statistics_for_partition)
        """

    async def delete_column_statistics_for_table(
        self, *, DatabaseName: str, TableName: str, ColumnName: str, CatalogId: str = ...
    ) -> Dict[str, Any]:
        """
        Retrieves table statistics of columns.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.delete_column_statistics_for_table)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#delete_column_statistics_for_table)
        """

    async def delete_connection(
        self, *, ConnectionName: str, CatalogId: str = ...
    ) -> Dict[str, Any]:
        """
        Deletes a connection from the Data Catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.delete_connection)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#delete_connection)
        """

    async def delete_crawler(self, *, Name: str) -> Dict[str, Any]:
        """
        Removes a specified crawler from the Glue Data Catalog, unless the crawler state
        is `RUNNING` .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.delete_crawler)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#delete_crawler)
        """

    async def delete_database(self, *, Name: str, CatalogId: str = ...) -> Dict[str, Any]:
        """
        Removes a specified database from a Data Catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.delete_database)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#delete_database)
        """

    async def delete_dev_endpoint(self, *, EndpointName: str) -> Dict[str, Any]:
        """
        Deletes a specified development endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.delete_dev_endpoint)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#delete_dev_endpoint)
        """

    async def delete_job(self, *, JobName: str) -> DeleteJobResponseTypeDef:
        """
        Deletes a specified job definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.delete_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#delete_job)
        """

    async def delete_ml_transform(self, *, TransformId: str) -> DeleteMLTransformResponseTypeDef:
        """
        Deletes an Glue machine learning transform.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.delete_ml_transform)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#delete_ml_transform)
        """

    async def delete_partition(
        self,
        *,
        DatabaseName: str,
        TableName: str,
        PartitionValues: Sequence[str],
        CatalogId: str = ...
    ) -> Dict[str, Any]:
        """
        Deletes a specified partition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.delete_partition)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#delete_partition)
        """

    async def delete_partition_index(
        self, *, DatabaseName: str, TableName: str, IndexName: str, CatalogId: str = ...
    ) -> Dict[str, Any]:
        """
        Deletes a specified partition index from an existing table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.delete_partition_index)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#delete_partition_index)
        """

    async def delete_registry(
        self, *, RegistryId: "RegistryIdTypeDef"
    ) -> DeleteRegistryResponseTypeDef:
        """
        Delete the entire registry including schema and all of its versions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.delete_registry)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#delete_registry)
        """

    async def delete_resource_policy(
        self, *, PolicyHashCondition: str = ..., ResourceArn: str = ...
    ) -> Dict[str, Any]:
        """
        Deletes a specified policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.delete_resource_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#delete_resource_policy)
        """

    async def delete_schema(self, *, SchemaId: "SchemaIdTypeDef") -> DeleteSchemaResponseTypeDef:
        """
        Deletes the entire schema set, including the schema set and all of its versions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.delete_schema)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#delete_schema)
        """

    async def delete_schema_versions(
        self, *, SchemaId: "SchemaIdTypeDef", Versions: str
    ) -> DeleteSchemaVersionsResponseTypeDef:
        """
        Remove versions from the specified schema.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.delete_schema_versions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#delete_schema_versions)
        """

    async def delete_security_configuration(self, *, Name: str) -> Dict[str, Any]:
        """
        Deletes a specified security configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.delete_security_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#delete_security_configuration)
        """

    async def delete_table(
        self, *, DatabaseName: str, Name: str, CatalogId: str = ..., TransactionId: str = ...
    ) -> Dict[str, Any]:
        """
        Removes a table definition from the Data Catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.delete_table)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#delete_table)
        """

    async def delete_table_version(
        self, *, DatabaseName: str, TableName: str, VersionId: str, CatalogId: str = ...
    ) -> Dict[str, Any]:
        """
        Deletes a specified version of a table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.delete_table_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#delete_table_version)
        """

    async def delete_trigger(self, *, Name: str) -> DeleteTriggerResponseTypeDef:
        """
        Deletes a specified trigger.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.delete_trigger)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#delete_trigger)
        """

    async def delete_user_defined_function(
        self, *, DatabaseName: str, FunctionName: str, CatalogId: str = ...
    ) -> Dict[str, Any]:
        """
        Deletes an existing function definition from the Data Catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.delete_user_defined_function)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#delete_user_defined_function)
        """

    async def delete_workflow(self, *, Name: str) -> DeleteWorkflowResponseTypeDef:
        """
        Deletes a workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.delete_workflow)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#delete_workflow)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#generate_presigned_url)
        """

    async def get_blueprint(
        self, *, Name: str, IncludeBlueprint: bool = ..., IncludeParameterSpec: bool = ...
    ) -> GetBlueprintResponseTypeDef:
        """
        Retrieves the details of a blueprint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_blueprint)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_blueprint)
        """

    async def get_blueprint_run(
        self, *, BlueprintName: str, RunId: str
    ) -> GetBlueprintRunResponseTypeDef:
        """
        Retrieves the details of a blueprint run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_blueprint_run)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_blueprint_run)
        """

    async def get_blueprint_runs(
        self, *, BlueprintName: str, NextToken: str = ..., MaxResults: int = ...
    ) -> GetBlueprintRunsResponseTypeDef:
        """
        Retrieves the details of blueprint runs for a specified blueprint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_blueprint_runs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_blueprint_runs)
        """

    async def get_catalog_import_status(
        self, *, CatalogId: str = ...
    ) -> GetCatalogImportStatusResponseTypeDef:
        """
        Retrieves the status of a migration operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_catalog_import_status)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_catalog_import_status)
        """

    async def get_classifier(self, *, Name: str) -> GetClassifierResponseTypeDef:
        """
        Retrieve a classifier by name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_classifier)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_classifier)
        """

    async def get_classifiers(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> GetClassifiersResponseTypeDef:
        """
        Lists all classifier objects in the Data Catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_classifiers)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_classifiers)
        """

    async def get_column_statistics_for_partition(
        self,
        *,
        DatabaseName: str,
        TableName: str,
        PartitionValues: Sequence[str],
        ColumnNames: Sequence[str],
        CatalogId: str = ...
    ) -> GetColumnStatisticsForPartitionResponseTypeDef:
        """
        Retrieves partition statistics of columns.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_column_statistics_for_partition)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_column_statistics_for_partition)
        """

    async def get_column_statistics_for_table(
        self, *, DatabaseName: str, TableName: str, ColumnNames: Sequence[str], CatalogId: str = ...
    ) -> GetColumnStatisticsForTableResponseTypeDef:
        """
        Retrieves table statistics of columns.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_column_statistics_for_table)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_column_statistics_for_table)
        """

    async def get_connection(
        self, *, Name: str, CatalogId: str = ..., HidePassword: bool = ...
    ) -> GetConnectionResponseTypeDef:
        """
        Retrieves a connection definition from the Data Catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_connection)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_connection)
        """

    async def get_connections(
        self,
        *,
        CatalogId: str = ...,
        Filter: "GetConnectionsFilterTypeDef" = ...,
        HidePassword: bool = ...,
        NextToken: str = ...,
        MaxResults: int = ...
    ) -> GetConnectionsResponseTypeDef:
        """
        Retrieves a list of connection definitions from the Data Catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_connections)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_connections)
        """

    async def get_crawler(self, *, Name: str) -> GetCrawlerResponseTypeDef:
        """
        Retrieves metadata for a specified crawler.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_crawler)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_crawler)
        """

    async def get_crawler_metrics(
        self, *, CrawlerNameList: Sequence[str] = ..., MaxResults: int = ..., NextToken: str = ...
    ) -> GetCrawlerMetricsResponseTypeDef:
        """
        Retrieves metrics about specified crawlers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_crawler_metrics)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_crawler_metrics)
        """

    async def get_crawlers(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> GetCrawlersResponseTypeDef:
        """
        Retrieves metadata for all crawlers defined in the customer account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_crawlers)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_crawlers)
        """

    async def get_data_catalog_encryption_settings(
        self, *, CatalogId: str = ...
    ) -> GetDataCatalogEncryptionSettingsResponseTypeDef:
        """
        Retrieves the security configuration for a specified catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_data_catalog_encryption_settings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_data_catalog_encryption_settings)
        """

    async def get_database(self, *, Name: str, CatalogId: str = ...) -> GetDatabaseResponseTypeDef:
        """
        Retrieves the definition of a specified database.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_database)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_database)
        """

    async def get_databases(
        self,
        *,
        CatalogId: str = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
        ResourceShareType: ResourceShareTypeType = ...
    ) -> GetDatabasesResponseTypeDef:
        """
        Retrieves all databases defined in a given Data Catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_databases)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_databases)
        """

    async def get_dataflow_graph(
        self, *, PythonScript: str = ...
    ) -> GetDataflowGraphResponseTypeDef:
        """
        Transforms a Python script into a directed acyclic graph (DAG).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_dataflow_graph)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_dataflow_graph)
        """

    async def get_dev_endpoint(self, *, EndpointName: str) -> GetDevEndpointResponseTypeDef:
        """
        Retrieves information about a specified development endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_dev_endpoint)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_dev_endpoint)
        """

    async def get_dev_endpoints(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> GetDevEndpointsResponseTypeDef:
        """
        Retrieves all the development endpoints in this AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_dev_endpoints)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_dev_endpoints)
        """

    async def get_job(self, *, JobName: str) -> GetJobResponseTypeDef:
        """
        Retrieves an existing job definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_job)
        """

    async def get_job_bookmark(
        self, *, JobName: str, RunId: str = ...
    ) -> GetJobBookmarkResponseTypeDef:
        """
        Returns information on a job bookmark entry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_job_bookmark)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_job_bookmark)
        """

    async def get_job_run(
        self, *, JobName: str, RunId: str, PredecessorsIncluded: bool = ...
    ) -> GetJobRunResponseTypeDef:
        """
        Retrieves the metadata for a given job run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_job_run)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_job_run)
        """

    async def get_job_runs(
        self, *, JobName: str, NextToken: str = ..., MaxResults: int = ...
    ) -> GetJobRunsResponseTypeDef:
        """
        Retrieves metadata for all runs of a given job definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_job_runs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_job_runs)
        """

    async def get_jobs(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> GetJobsResponseTypeDef:
        """
        Retrieves all current job definitions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_jobs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_jobs)
        """

    async def get_mapping(
        self,
        *,
        Source: "CatalogEntryTypeDef",
        Sinks: Sequence["CatalogEntryTypeDef"] = ...,
        Location: "LocationTypeDef" = ...
    ) -> GetMappingResponseTypeDef:
        """
        Creates mappings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_mapping)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_mapping)
        """

    async def get_ml_task_run(
        self, *, TransformId: str, TaskRunId: str
    ) -> GetMLTaskRunResponseTypeDef:
        """
        Gets details for a specific task run on a machine learning transform.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_ml_task_run)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_ml_task_run)
        """

    async def get_ml_task_runs(
        self,
        *,
        TransformId: str,
        NextToken: str = ...,
        MaxResults: int = ...,
        Filter: "TaskRunFilterCriteriaTypeDef" = ...,
        Sort: "TaskRunSortCriteriaTypeDef" = ...
    ) -> GetMLTaskRunsResponseTypeDef:
        """
        Gets a list of runs for a machine learning transform.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_ml_task_runs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_ml_task_runs)
        """

    async def get_ml_transform(self, *, TransformId: str) -> GetMLTransformResponseTypeDef:
        """
        Gets an Glue machine learning transform artifact and all its corresponding
        metadata.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_ml_transform)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_ml_transform)
        """

    async def get_ml_transforms(
        self,
        *,
        NextToken: str = ...,
        MaxResults: int = ...,
        Filter: "TransformFilterCriteriaTypeDef" = ...,
        Sort: "TransformSortCriteriaTypeDef" = ...
    ) -> GetMLTransformsResponseTypeDef:
        """
        Gets a sortable, filterable list of existing Glue machine learning transforms.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_ml_transforms)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_ml_transforms)
        """

    async def get_partition(
        self,
        *,
        DatabaseName: str,
        TableName: str,
        PartitionValues: Sequence[str],
        CatalogId: str = ...
    ) -> GetPartitionResponseTypeDef:
        """
        Retrieves information about a specified partition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_partition)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_partition)
        """

    async def get_partition_indexes(
        self, *, DatabaseName: str, TableName: str, CatalogId: str = ..., NextToken: str = ...
    ) -> GetPartitionIndexesResponseTypeDef:
        """
        Retrieves the partition indexes associated with a table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_partition_indexes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_partition_indexes)
        """

    async def get_partitions(
        self,
        *,
        DatabaseName: str,
        TableName: str,
        CatalogId: str = ...,
        Expression: str = ...,
        NextToken: str = ...,
        Segment: "SegmentTypeDef" = ...,
        MaxResults: int = ...,
        ExcludeColumnSchema: bool = ...,
        TransactionId: str = ...,
        QueryAsOfTime: Union[datetime, str] = ...
    ) -> GetPartitionsResponseTypeDef:
        """
        Retrieves information about the partitions in a table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_partitions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_partitions)
        """

    async def get_plan(
        self,
        *,
        Mapping: Sequence["MappingEntryTypeDef"],
        Source: "CatalogEntryTypeDef",
        Sinks: Sequence["CatalogEntryTypeDef"] = ...,
        Location: "LocationTypeDef" = ...,
        Language: LanguageType = ...,
        AdditionalPlanOptionsMap: Mapping[str, str] = ...
    ) -> GetPlanResponseTypeDef:
        """
        Gets code to perform a specified mapping.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_plan)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_plan)
        """

    async def get_registry(self, *, RegistryId: "RegistryIdTypeDef") -> GetRegistryResponseTypeDef:
        """
        Describes the specified registry in detail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_registry)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_registry)
        """

    async def get_resource_policies(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> GetResourcePoliciesResponseTypeDef:
        """
        Retrieves the resource policies set on individual resources by Resource Access
        Manager during cross-account permission grants.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_resource_policies)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_resource_policies)
        """

    async def get_resource_policy(
        self, *, ResourceArn: str = ...
    ) -> GetResourcePolicyResponseTypeDef:
        """
        Retrieves a specified resource policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_resource_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_resource_policy)
        """

    async def get_schema(self, *, SchemaId: "SchemaIdTypeDef") -> GetSchemaResponseTypeDef:
        """
        Describes the specified schema in detail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_schema)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_schema)
        """

    async def get_schema_by_definition(
        self, *, SchemaId: "SchemaIdTypeDef", SchemaDefinition: str
    ) -> GetSchemaByDefinitionResponseTypeDef:
        """
        Retrieves a schema by the `SchemaDefinition`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_schema_by_definition)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_schema_by_definition)
        """

    async def get_schema_version(
        self,
        *,
        SchemaId: "SchemaIdTypeDef" = ...,
        SchemaVersionId: str = ...,
        SchemaVersionNumber: "SchemaVersionNumberTypeDef" = ...
    ) -> GetSchemaVersionResponseTypeDef:
        """
        Get the specified schema by its unique ID assigned when a version of the schema
        is created or registered.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_schema_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_schema_version)
        """

    async def get_schema_versions_diff(
        self,
        *,
        SchemaId: "SchemaIdTypeDef",
        FirstSchemaVersionNumber: "SchemaVersionNumberTypeDef",
        SecondSchemaVersionNumber: "SchemaVersionNumberTypeDef",
        SchemaDiffType: Literal["SYNTAX_DIFF"]
    ) -> GetSchemaVersionsDiffResponseTypeDef:
        """
        Fetches the schema version difference in the specified difference type between
        two stored schema versions in the Schema Registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_schema_versions_diff)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_schema_versions_diff)
        """

    async def get_security_configuration(
        self, *, Name: str
    ) -> GetSecurityConfigurationResponseTypeDef:
        """
        Retrieves a specified security configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_security_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_security_configuration)
        """

    async def get_security_configurations(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> GetSecurityConfigurationsResponseTypeDef:
        """
        Retrieves a list of all security configurations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_security_configurations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_security_configurations)
        """

    async def get_table(
        self,
        *,
        DatabaseName: str,
        Name: str,
        CatalogId: str = ...,
        TransactionId: str = ...,
        QueryAsOfTime: Union[datetime, str] = ...
    ) -> GetTableResponseTypeDef:
        """
        Retrieves the `Table` definition in a Data Catalog for a specified table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_table)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_table)
        """

    async def get_table_version(
        self, *, DatabaseName: str, TableName: str, CatalogId: str = ..., VersionId: str = ...
    ) -> GetTableVersionResponseTypeDef:
        """
        Retrieves a specified version of a table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_table_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_table_version)
        """

    async def get_table_versions(
        self,
        *,
        DatabaseName: str,
        TableName: str,
        CatalogId: str = ...,
        NextToken: str = ...,
        MaxResults: int = ...
    ) -> GetTableVersionsResponseTypeDef:
        """
        Retrieves a list of strings that identify available versions of a specified
        table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_table_versions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_table_versions)
        """

    async def get_tables(
        self,
        *,
        DatabaseName: str,
        CatalogId: str = ...,
        Expression: str = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
        TransactionId: str = ...,
        QueryAsOfTime: Union[datetime, str] = ...
    ) -> GetTablesResponseTypeDef:
        """
        Retrieves the definitions of some or all of the tables in a given `Database` .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_tables)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_tables)
        """

    async def get_tags(self, *, ResourceArn: str) -> GetTagsResponseTypeDef:
        """
        Retrieves a list of tags associated with a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_tags)
        """

    async def get_trigger(self, *, Name: str) -> GetTriggerResponseTypeDef:
        """
        Retrieves the definition of a trigger.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_trigger)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_trigger)
        """

    async def get_triggers(
        self, *, NextToken: str = ..., DependentJobName: str = ..., MaxResults: int = ...
    ) -> GetTriggersResponseTypeDef:
        """
        Gets all the triggers associated with a job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_triggers)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_triggers)
        """

    async def get_unfiltered_partition_metadata(
        self,
        *,
        CatalogId: str,
        DatabaseName: str,
        TableName: str,
        PartitionValues: Sequence[str],
        SupportedPermissionTypes: Sequence[PermissionTypeType],
        AuditContext: "AuditContextTypeDef" = ...
    ) -> GetUnfilteredPartitionMetadataResponseTypeDef:
        """
        See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/glue-2017-03-31/GetUnfilteredPartitionMetadata).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_unfiltered_partition_metadata)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_unfiltered_partition_metadata)
        """

    async def get_unfiltered_partitions_metadata(
        self,
        *,
        CatalogId: str,
        DatabaseName: str,
        TableName: str,
        SupportedPermissionTypes: Sequence[PermissionTypeType],
        Expression: str = ...,
        AuditContext: "AuditContextTypeDef" = ...,
        NextToken: str = ...,
        Segment: "SegmentTypeDef" = ...,
        MaxResults: int = ...
    ) -> GetUnfilteredPartitionsMetadataResponseTypeDef:
        """
        See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/glue-2017-03-31/GetUnfilteredPartitionsMetadata).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_unfiltered_partitions_metadata)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_unfiltered_partitions_metadata)
        """

    async def get_unfiltered_table_metadata(
        self,
        *,
        CatalogId: str,
        DatabaseName: str,
        Name: str,
        SupportedPermissionTypes: Sequence[PermissionTypeType],
        AuditContext: "AuditContextTypeDef" = ...
    ) -> GetUnfilteredTableMetadataResponseTypeDef:
        """
        See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/glue-2017-03-31/GetUnfilteredTableMetadata).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_unfiltered_table_metadata)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_unfiltered_table_metadata)
        """

    async def get_user_defined_function(
        self, *, DatabaseName: str, FunctionName: str, CatalogId: str = ...
    ) -> GetUserDefinedFunctionResponseTypeDef:
        """
        Retrieves a specified function definition from the Data Catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_user_defined_function)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_user_defined_function)
        """

    async def get_user_defined_functions(
        self,
        *,
        Pattern: str,
        CatalogId: str = ...,
        DatabaseName: str = ...,
        NextToken: str = ...,
        MaxResults: int = ...
    ) -> GetUserDefinedFunctionsResponseTypeDef:
        """
        Retrieves multiple function definitions from the Data Catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_user_defined_functions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_user_defined_functions)
        """

    async def get_workflow(
        self, *, Name: str, IncludeGraph: bool = ...
    ) -> GetWorkflowResponseTypeDef:
        """
        Retrieves resource metadata for a workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_workflow)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_workflow)
        """

    async def get_workflow_run(
        self, *, Name: str, RunId: str, IncludeGraph: bool = ...
    ) -> GetWorkflowRunResponseTypeDef:
        """
        Retrieves the metadata for a given workflow run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_workflow_run)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_workflow_run)
        """

    async def get_workflow_run_properties(
        self, *, Name: str, RunId: str
    ) -> GetWorkflowRunPropertiesResponseTypeDef:
        """
        Retrieves the workflow run properties which were set during the run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_workflow_run_properties)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_workflow_run_properties)
        """

    async def get_workflow_runs(
        self, *, Name: str, IncludeGraph: bool = ..., NextToken: str = ..., MaxResults: int = ...
    ) -> GetWorkflowRunsResponseTypeDef:
        """
        Retrieves metadata for all runs of a given workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_workflow_runs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_workflow_runs)
        """

    async def import_catalog_to_glue(self, *, CatalogId: str = ...) -> Dict[str, Any]:
        """
        Imports an existing Amazon Athena Data Catalog to Glue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.import_catalog_to_glue)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#import_catalog_to_glue)
        """

    async def list_blueprints(
        self, *, NextToken: str = ..., MaxResults: int = ..., Tags: Mapping[str, str] = ...
    ) -> ListBlueprintsResponseTypeDef:
        """
        Lists all the blueprint names in an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.list_blueprints)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#list_blueprints)
        """

    async def list_crawlers(
        self, *, MaxResults: int = ..., NextToken: str = ..., Tags: Mapping[str, str] = ...
    ) -> ListCrawlersResponseTypeDef:
        """
        Retrieves the names of all crawler resources in this Amazon Web Services
        account, or the resources with the specified tag.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.list_crawlers)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#list_crawlers)
        """

    async def list_dev_endpoints(
        self, *, NextToken: str = ..., MaxResults: int = ..., Tags: Mapping[str, str] = ...
    ) -> ListDevEndpointsResponseTypeDef:
        """
        Retrieves the names of all `DevEndpoint` resources in this Amazon Web Services
        account, or the resources with the specified tag.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.list_dev_endpoints)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#list_dev_endpoints)
        """

    async def list_jobs(
        self, *, NextToken: str = ..., MaxResults: int = ..., Tags: Mapping[str, str] = ...
    ) -> ListJobsResponseTypeDef:
        """
        Retrieves the names of all job resources in this Amazon Web Services account, or
        the resources with the specified tag.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.list_jobs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#list_jobs)
        """

    async def list_ml_transforms(
        self,
        *,
        NextToken: str = ...,
        MaxResults: int = ...,
        Filter: "TransformFilterCriteriaTypeDef" = ...,
        Sort: "TransformSortCriteriaTypeDef" = ...,
        Tags: Mapping[str, str] = ...
    ) -> ListMLTransformsResponseTypeDef:
        """
        Retrieves a sortable, filterable list of existing Glue machine learning
        transforms in this Amazon Web Services account, or the resources with the
        specified tag.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.list_ml_transforms)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#list_ml_transforms)
        """

    async def list_registries(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListRegistriesResponseTypeDef:
        """
        Returns a list of registries that you have created, with minimal registry
        information.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.list_registries)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#list_registries)
        """

    async def list_schema_versions(
        self, *, SchemaId: "SchemaIdTypeDef", MaxResults: int = ..., NextToken: str = ...
    ) -> ListSchemaVersionsResponseTypeDef:
        """
        Returns a list of schema versions that you have created, with minimal
        information.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.list_schema_versions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#list_schema_versions)
        """

    async def list_schemas(
        self, *, RegistryId: "RegistryIdTypeDef" = ..., MaxResults: int = ..., NextToken: str = ...
    ) -> ListSchemasResponseTypeDef:
        """
        Returns a list of schemas with minimal details.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.list_schemas)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#list_schemas)
        """

    async def list_triggers(
        self,
        *,
        NextToken: str = ...,
        DependentJobName: str = ...,
        MaxResults: int = ...,
        Tags: Mapping[str, str] = ...
    ) -> ListTriggersResponseTypeDef:
        """
        Retrieves the names of all trigger resources in this Amazon Web Services
        account, or the resources with the specified tag.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.list_triggers)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#list_triggers)
        """

    async def list_workflows(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> ListWorkflowsResponseTypeDef:
        """
        Lists names of workflows created in the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.list_workflows)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#list_workflows)
        """

    async def put_data_catalog_encryption_settings(
        self,
        *,
        DataCatalogEncryptionSettings: "DataCatalogEncryptionSettingsTypeDef",
        CatalogId: str = ...
    ) -> Dict[str, Any]:
        """
        Sets the security configuration for a specified catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.put_data_catalog_encryption_settings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#put_data_catalog_encryption_settings)
        """

    async def put_resource_policy(
        self,
        *,
        PolicyInJson: str,
        ResourceArn: str = ...,
        PolicyHashCondition: str = ...,
        PolicyExistsCondition: ExistConditionType = ...,
        EnableHybrid: EnableHybridValuesType = ...
    ) -> PutResourcePolicyResponseTypeDef:
        """
        Sets the Data Catalog resource policy for access control.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.put_resource_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#put_resource_policy)
        """

    async def put_schema_version_metadata(
        self,
        *,
        MetadataKeyValue: "MetadataKeyValuePairTypeDef",
        SchemaId: "SchemaIdTypeDef" = ...,
        SchemaVersionNumber: "SchemaVersionNumberTypeDef" = ...,
        SchemaVersionId: str = ...
    ) -> PutSchemaVersionMetadataResponseTypeDef:
        """
        Puts the metadata key value pair for a specified schema version ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.put_schema_version_metadata)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#put_schema_version_metadata)
        """

    async def put_workflow_run_properties(
        self, *, Name: str, RunId: str, RunProperties: Mapping[str, str]
    ) -> Dict[str, Any]:
        """
        Puts the specified workflow run properties for the given workflow run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.put_workflow_run_properties)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#put_workflow_run_properties)
        """

    async def query_schema_version_metadata(
        self,
        *,
        SchemaId: "SchemaIdTypeDef" = ...,
        SchemaVersionNumber: "SchemaVersionNumberTypeDef" = ...,
        SchemaVersionId: str = ...,
        MetadataList: Sequence["MetadataKeyValuePairTypeDef"] = ...,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> QuerySchemaVersionMetadataResponseTypeDef:
        """
        Queries for the schema version metadata information.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.query_schema_version_metadata)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#query_schema_version_metadata)
        """

    async def register_schema_version(
        self, *, SchemaId: "SchemaIdTypeDef", SchemaDefinition: str
    ) -> RegisterSchemaVersionResponseTypeDef:
        """
        Adds a new version to the existing schema.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.register_schema_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#register_schema_version)
        """

    async def remove_schema_version_metadata(
        self,
        *,
        MetadataKeyValue: "MetadataKeyValuePairTypeDef",
        SchemaId: "SchemaIdTypeDef" = ...,
        SchemaVersionNumber: "SchemaVersionNumberTypeDef" = ...,
        SchemaVersionId: str = ...
    ) -> RemoveSchemaVersionMetadataResponseTypeDef:
        """
        Removes a key value pair from the schema version metadata for the specified
        schema version ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.remove_schema_version_metadata)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#remove_schema_version_metadata)
        """

    async def reset_job_bookmark(
        self, *, JobName: str, RunId: str = ...
    ) -> ResetJobBookmarkResponseTypeDef:
        """
        Resets a bookmark entry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.reset_job_bookmark)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#reset_job_bookmark)
        """

    async def resume_workflow_run(
        self, *, Name: str, RunId: str, NodeIds: Sequence[str]
    ) -> ResumeWorkflowRunResponseTypeDef:
        """
        Restarts selected nodes of a previous partially completed workflow run and
        resumes the workflow run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.resume_workflow_run)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#resume_workflow_run)
        """

    async def search_tables(
        self,
        *,
        CatalogId: str = ...,
        NextToken: str = ...,
        Filters: Sequence["PropertyPredicateTypeDef"] = ...,
        SearchText: str = ...,
        SortCriteria: Sequence["SortCriterionTypeDef"] = ...,
        MaxResults: int = ...,
        ResourceShareType: ResourceShareTypeType = ...
    ) -> SearchTablesResponseTypeDef:
        """
        Searches a set of tables based on properties in the table metadata as well as on
        the parent database.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.search_tables)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#search_tables)
        """

    async def start_blueprint_run(
        self, *, BlueprintName: str, RoleArn: str, Parameters: str = ...
    ) -> StartBlueprintRunResponseTypeDef:
        """
        Starts a new run of the specified blueprint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.start_blueprint_run)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#start_blueprint_run)
        """

    async def start_crawler(self, *, Name: str) -> Dict[str, Any]:
        """
        Starts a crawl using the specified crawler, regardless of what is scheduled.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.start_crawler)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#start_crawler)
        """

    async def start_crawler_schedule(self, *, CrawlerName: str) -> Dict[str, Any]:
        """
        Changes the schedule state of the specified crawler to `SCHEDULED` , unless the
        crawler is already running or the schedule state is already `SCHEDULED` .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.start_crawler_schedule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#start_crawler_schedule)
        """

    async def start_export_labels_task_run(
        self, *, TransformId: str, OutputS3Path: str
    ) -> StartExportLabelsTaskRunResponseTypeDef:
        """
        Begins an asynchronous task to export all labeled data for a particular
        transform.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.start_export_labels_task_run)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#start_export_labels_task_run)
        """

    async def start_import_labels_task_run(
        self, *, TransformId: str, InputS3Path: str, ReplaceAllLabels: bool = ...
    ) -> StartImportLabelsTaskRunResponseTypeDef:
        """
        Enables you to provide additional labels (examples of truth) to be used to teach
        the machine learning transform and improve its quality.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.start_import_labels_task_run)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#start_import_labels_task_run)
        """

    async def start_job_run(
        self,
        *,
        JobName: str,
        JobRunId: str = ...,
        Arguments: Mapping[str, str] = ...,
        AllocatedCapacity: int = ...,
        Timeout: int = ...,
        MaxCapacity: float = ...,
        SecurityConfiguration: str = ...,
        NotificationProperty: "NotificationPropertyTypeDef" = ...,
        WorkerType: WorkerTypeType = ...,
        NumberOfWorkers: int = ...
    ) -> StartJobRunResponseTypeDef:
        """
        Starts a job run using a job definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.start_job_run)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#start_job_run)
        """

    async def start_ml_evaluation_task_run(
        self, *, TransformId: str
    ) -> StartMLEvaluationTaskRunResponseTypeDef:
        """
        Starts a task to estimate the quality of the transform.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.start_ml_evaluation_task_run)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#start_ml_evaluation_task_run)
        """

    async def start_ml_labeling_set_generation_task_run(
        self, *, TransformId: str, OutputS3Path: str
    ) -> StartMLLabelingSetGenerationTaskRunResponseTypeDef:
        """
        Starts the active learning workflow for your machine learning transform to
        improve the transform's quality by generating label sets and adding labels.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.start_ml_labeling_set_generation_task_run)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#start_ml_labeling_set_generation_task_run)
        """

    async def start_trigger(self, *, Name: str) -> StartTriggerResponseTypeDef:
        """
        Starts an existing trigger.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.start_trigger)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#start_trigger)
        """

    async def start_workflow_run(
        self, *, Name: str, RunProperties: Mapping[str, str] = ...
    ) -> StartWorkflowRunResponseTypeDef:
        """
        Starts a new run of the specified workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.start_workflow_run)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#start_workflow_run)
        """

    async def stop_crawler(self, *, Name: str) -> Dict[str, Any]:
        """
        If the specified crawler is running, stops the crawl.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.stop_crawler)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#stop_crawler)
        """

    async def stop_crawler_schedule(self, *, CrawlerName: str) -> Dict[str, Any]:
        """
        Sets the schedule state of the specified crawler to `NOT_SCHEDULED` , but does
        not stop the crawler if it is already running.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.stop_crawler_schedule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#stop_crawler_schedule)
        """

    async def stop_trigger(self, *, Name: str) -> StopTriggerResponseTypeDef:
        """
        Stops a specified trigger.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.stop_trigger)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#stop_trigger)
        """

    async def stop_workflow_run(self, *, Name: str, RunId: str) -> Dict[str, Any]:
        """
        Stops the execution of the specified workflow run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.stop_workflow_run)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#stop_workflow_run)
        """

    async def tag_resource(
        self, *, ResourceArn: str, TagsToAdd: Mapping[str, str]
    ) -> Dict[str, Any]:
        """
        Adds tags to a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#tag_resource)
        """

    async def untag_resource(
        self, *, ResourceArn: str, TagsToRemove: Sequence[str]
    ) -> Dict[str, Any]:
        """
        Removes tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#untag_resource)
        """

    async def update_blueprint(
        self, *, Name: str, BlueprintLocation: str, Description: str = ...
    ) -> UpdateBlueprintResponseTypeDef:
        """
        Updates a registered blueprint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.update_blueprint)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#update_blueprint)
        """

    async def update_classifier(
        self,
        *,
        GrokClassifier: "UpdateGrokClassifierRequestTypeDef" = ...,
        XMLClassifier: "UpdateXMLClassifierRequestTypeDef" = ...,
        JsonClassifier: "UpdateJsonClassifierRequestTypeDef" = ...,
        CsvClassifier: "UpdateCsvClassifierRequestTypeDef" = ...
    ) -> Dict[str, Any]:
        """
        Modifies an existing classifier (a `GrokClassifier` , an `XMLClassifier` , a
        `JsonClassifier` , or a `CsvClassifier` , depending on which field is present).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.update_classifier)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#update_classifier)
        """

    async def update_column_statistics_for_partition(
        self,
        *,
        DatabaseName: str,
        TableName: str,
        PartitionValues: Sequence[str],
        ColumnStatisticsList: Sequence["ColumnStatisticsTypeDef"],
        CatalogId: str = ...
    ) -> UpdateColumnStatisticsForPartitionResponseTypeDef:
        """
        Creates or updates partition statistics of columns.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.update_column_statistics_for_partition)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#update_column_statistics_for_partition)
        """

    async def update_column_statistics_for_table(
        self,
        *,
        DatabaseName: str,
        TableName: str,
        ColumnStatisticsList: Sequence["ColumnStatisticsTypeDef"],
        CatalogId: str = ...
    ) -> UpdateColumnStatisticsForTableResponseTypeDef:
        """
        Creates or updates table statistics of columns.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.update_column_statistics_for_table)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#update_column_statistics_for_table)
        """

    async def update_connection(
        self, *, Name: str, ConnectionInput: "ConnectionInputTypeDef", CatalogId: str = ...
    ) -> Dict[str, Any]:
        """
        Updates a connection definition in the Data Catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.update_connection)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#update_connection)
        """

    async def update_crawler(
        self,
        *,
        Name: str,
        Role: str = ...,
        DatabaseName: str = ...,
        Description: str = ...,
        Targets: "CrawlerTargetsTypeDef" = ...,
        Schedule: str = ...,
        Classifiers: Sequence[str] = ...,
        TablePrefix: str = ...,
        SchemaChangePolicy: "SchemaChangePolicyTypeDef" = ...,
        RecrawlPolicy: "RecrawlPolicyTypeDef" = ...,
        LineageConfiguration: "LineageConfigurationTypeDef" = ...,
        LakeFormationConfiguration: "LakeFormationConfigurationTypeDef" = ...,
        Configuration: str = ...,
        CrawlerSecurityConfiguration: str = ...
    ) -> Dict[str, Any]:
        """
        Updates a crawler.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.update_crawler)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#update_crawler)
        """

    async def update_crawler_schedule(
        self, *, CrawlerName: str, Schedule: str = ...
    ) -> Dict[str, Any]:
        """
        Updates the schedule of a crawler using a `cron` expression.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.update_crawler_schedule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#update_crawler_schedule)
        """

    async def update_database(
        self, *, Name: str, DatabaseInput: "DatabaseInputTypeDef", CatalogId: str = ...
    ) -> Dict[str, Any]:
        """
        Updates an existing database definition in a Data Catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.update_database)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#update_database)
        """

    async def update_dev_endpoint(
        self,
        *,
        EndpointName: str,
        PublicKey: str = ...,
        AddPublicKeys: Sequence[str] = ...,
        DeletePublicKeys: Sequence[str] = ...,
        CustomLibraries: "DevEndpointCustomLibrariesTypeDef" = ...,
        UpdateEtlLibraries: bool = ...,
        DeleteArguments: Sequence[str] = ...,
        AddArguments: Mapping[str, str] = ...
    ) -> Dict[str, Any]:
        """
        Updates a specified development endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.update_dev_endpoint)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#update_dev_endpoint)
        """

    async def update_job(
        self, *, JobName: str, JobUpdate: "JobUpdateTypeDef"
    ) -> UpdateJobResponseTypeDef:
        """
        Updates an existing job definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.update_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#update_job)
        """

    async def update_ml_transform(
        self,
        *,
        TransformId: str,
        Name: str = ...,
        Description: str = ...,
        Parameters: "TransformParametersTypeDef" = ...,
        Role: str = ...,
        GlueVersion: str = ...,
        MaxCapacity: float = ...,
        WorkerType: WorkerTypeType = ...,
        NumberOfWorkers: int = ...,
        Timeout: int = ...,
        MaxRetries: int = ...
    ) -> UpdateMLTransformResponseTypeDef:
        """
        Updates an existing machine learning transform.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.update_ml_transform)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#update_ml_transform)
        """

    async def update_partition(
        self,
        *,
        DatabaseName: str,
        TableName: str,
        PartitionValueList: Sequence[str],
        PartitionInput: "PartitionInputTypeDef",
        CatalogId: str = ...
    ) -> Dict[str, Any]:
        """
        Updates a partition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.update_partition)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#update_partition)
        """

    async def update_registry(
        self, *, RegistryId: "RegistryIdTypeDef", Description: str
    ) -> UpdateRegistryResponseTypeDef:
        """
        Updates an existing registry which is used to hold a collection of schemas.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.update_registry)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#update_registry)
        """

    async def update_schema(
        self,
        *,
        SchemaId: "SchemaIdTypeDef",
        SchemaVersionNumber: "SchemaVersionNumberTypeDef" = ...,
        Compatibility: CompatibilityType = ...,
        Description: str = ...
    ) -> UpdateSchemaResponseTypeDef:
        """
        Updates the description, compatibility setting, or version checkpoint for a
        schema set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.update_schema)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#update_schema)
        """

    async def update_table(
        self,
        *,
        DatabaseName: str,
        TableInput: "TableInputTypeDef",
        CatalogId: str = ...,
        SkipArchive: bool = ...,
        TransactionId: str = ...,
        VersionId: str = ...
    ) -> Dict[str, Any]:
        """
        Updates a metadata table in the Data Catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.update_table)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#update_table)
        """

    async def update_trigger(
        self, *, Name: str, TriggerUpdate: "TriggerUpdateTypeDef"
    ) -> UpdateTriggerResponseTypeDef:
        """
        Updates a trigger definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.update_trigger)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#update_trigger)
        """

    async def update_user_defined_function(
        self,
        *,
        DatabaseName: str,
        FunctionName: str,
        FunctionInput: "UserDefinedFunctionInputTypeDef",
        CatalogId: str = ...
    ) -> Dict[str, Any]:
        """
        Updates an existing function definition in the Data Catalog.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.update_user_defined_function)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#update_user_defined_function)
        """

    async def update_workflow(
        self,
        *,
        Name: str,
        Description: str = ...,
        DefaultRunProperties: Mapping[str, str] = ...,
        MaxConcurrentRuns: int = ...
    ) -> UpdateWorkflowResponseTypeDef:
        """
        Updates an existing workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.update_workflow)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#update_workflow)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_classifiers"]) -> GetClassifiersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_connections"]) -> GetConnectionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_crawler_metrics"]
    ) -> GetCrawlerMetricsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_crawlers"]) -> GetCrawlersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_databases"]) -> GetDatabasesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_dev_endpoints"]
    ) -> GetDevEndpointsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_job_runs"]) -> GetJobRunsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_jobs"]) -> GetJobsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_partition_indexes"]
    ) -> GetPartitionIndexesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_partitions"]) -> GetPartitionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_resource_policies"]
    ) -> GetResourcePoliciesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_security_configurations"]
    ) -> GetSecurityConfigurationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_table_versions"]
    ) -> GetTableVersionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_tables"]) -> GetTablesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_triggers"]) -> GetTriggersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_user_defined_functions"]
    ) -> GetUserDefinedFunctionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_registries"]) -> ListRegistriesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_schema_versions"]
    ) -> ListSchemaVersionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_schemas"]) -> ListSchemasPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/#get_paginator)
        """

    async def __aenter__(self) -> "GlueClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/client/)
        """
