"""
Type annotations for glue service literal definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glue/literals/)

Usage::

    ```python
    from types_aiobotocore_glue.literals import BackfillErrorCodeType

    data: BackfillErrorCodeType = "ENCRYPTED_PARTITION_ERROR"
    ```
"""
import sys

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = (
    "BackfillErrorCodeType",
    "BlueprintRunStateType",
    "BlueprintStatusType",
    "CatalogEncryptionModeType",
    "CloudWatchEncryptionModeType",
    "ColumnStatisticsTypeType",
    "ComparatorType",
    "CompatibilityType",
    "ConnectionPropertyKeyType",
    "ConnectionTypeType",
    "CrawlStateType",
    "CrawlerLineageSettingsType",
    "CrawlerStateType",
    "CsvHeaderOptionType",
    "DataFormatType",
    "DeleteBehaviorType",
    "EnableHybridValuesType",
    "ExistConditionType",
    "GetClassifiersPaginatorName",
    "GetConnectionsPaginatorName",
    "GetCrawlerMetricsPaginatorName",
    "GetCrawlersPaginatorName",
    "GetDatabasesPaginatorName",
    "GetDevEndpointsPaginatorName",
    "GetJobRunsPaginatorName",
    "GetJobsPaginatorName",
    "GetPartitionIndexesPaginatorName",
    "GetPartitionsPaginatorName",
    "GetResourcePoliciesPaginatorName",
    "GetSecurityConfigurationsPaginatorName",
    "GetTableVersionsPaginatorName",
    "GetTablesPaginatorName",
    "GetTriggersPaginatorName",
    "GetUserDefinedFunctionsPaginatorName",
    "JobBookmarksEncryptionModeType",
    "JobRunStateType",
    "LanguageType",
    "LastCrawlStatusType",
    "ListRegistriesPaginatorName",
    "ListSchemaVersionsPaginatorName",
    "ListSchemasPaginatorName",
    "LogicalOperatorType",
    "LogicalType",
    "MLUserDataEncryptionModeStringType",
    "NodeTypeType",
    "PartitionIndexStatusType",
    "PermissionType",
    "PermissionTypeType",
    "PrincipalTypeType",
    "RecrawlBehaviorType",
    "RegistryStatusType",
    "ResourceShareTypeType",
    "ResourceTypeType",
    "S3EncryptionModeType",
    "ScheduleStateType",
    "SchemaDiffTypeType",
    "SchemaStatusType",
    "SchemaVersionStatusType",
    "SortDirectionTypeType",
    "SortType",
    "TaskRunSortColumnTypeType",
    "TaskStatusTypeType",
    "TaskTypeType",
    "TransformSortColumnTypeType",
    "TransformStatusTypeType",
    "TransformTypeType",
    "TriggerStateType",
    "TriggerTypeType",
    "UpdateBehaviorType",
    "WorkerTypeType",
    "WorkflowRunStatusType",
    "GlueServiceName",
    "ServiceName",
    "ResourceServiceName",
    "PaginatorName",
    "RegionName",
)


BackfillErrorCodeType = Literal[
    "ENCRYPTED_PARTITION_ERROR",
    "INTERNAL_ERROR",
    "INVALID_PARTITION_TYPE_DATA_ERROR",
    "MISSING_PARTITION_VALUE_ERROR",
    "UNSUPPORTED_PARTITION_CHARACTER_ERROR",
]
BlueprintRunStateType = Literal["FAILED", "ROLLING_BACK", "RUNNING", "SUCCEEDED"]
BlueprintStatusType = Literal["ACTIVE", "CREATING", "FAILED", "UPDATING"]
CatalogEncryptionModeType = Literal["DISABLED", "SSE-KMS"]
CloudWatchEncryptionModeType = Literal["DISABLED", "SSE-KMS"]
ColumnStatisticsTypeType = Literal[
    "BINARY", "BOOLEAN", "DATE", "DECIMAL", "DOUBLE", "LONG", "STRING"
]
ComparatorType = Literal[
    "EQUALS", "GREATER_THAN", "GREATER_THAN_EQUALS", "LESS_THAN", "LESS_THAN_EQUALS"
]
CompatibilityType = Literal[
    "BACKWARD", "BACKWARD_ALL", "DISABLED", "FORWARD", "FORWARD_ALL", "FULL", "FULL_ALL", "NONE"
]
ConnectionPropertyKeyType = Literal[
    "CONFIG_FILES",
    "CONNECTION_URL",
    "CONNECTOR_CLASS_NAME",
    "CONNECTOR_TYPE",
    "CONNECTOR_URL",
    "CUSTOM_JDBC_CERT",
    "CUSTOM_JDBC_CERT_STRING",
    "ENCRYPTED_KAFKA_CLIENT_KEYSTORE_PASSWORD",
    "ENCRYPTED_KAFKA_CLIENT_KEY_PASSWORD",
    "ENCRYPTED_PASSWORD",
    "HOST",
    "INSTANCE_ID",
    "JDBC_CONNECTION_URL",
    "JDBC_DRIVER_CLASS_NAME",
    "JDBC_DRIVER_JAR_URI",
    "JDBC_ENFORCE_SSL",
    "JDBC_ENGINE",
    "JDBC_ENGINE_VERSION",
    "KAFKA_BOOTSTRAP_SERVERS",
    "KAFKA_CLIENT_KEYSTORE",
    "KAFKA_CLIENT_KEYSTORE_PASSWORD",
    "KAFKA_CLIENT_KEY_PASSWORD",
    "KAFKA_CUSTOM_CERT",
    "KAFKA_SKIP_CUSTOM_CERT_VALIDATION",
    "KAFKA_SSL_ENABLED",
    "PASSWORD",
    "PORT",
    "SECRET_ID",
    "SKIP_CUSTOM_JDBC_CERT_VALIDATION",
    "USERNAME",
]
ConnectionTypeType = Literal["CUSTOM", "JDBC", "KAFKA", "MARKETPLACE", "MONGODB", "NETWORK", "SFTP"]
CrawlStateType = Literal["CANCELLED", "CANCELLING", "FAILED", "RUNNING", "SUCCEEDED"]
CrawlerLineageSettingsType = Literal["DISABLE", "ENABLE"]
CrawlerStateType = Literal["READY", "RUNNING", "STOPPING"]
CsvHeaderOptionType = Literal["ABSENT", "PRESENT", "UNKNOWN"]
DataFormatType = Literal["AVRO", "JSON", "PROTOBUF"]
DeleteBehaviorType = Literal["DELETE_FROM_DATABASE", "DEPRECATE_IN_DATABASE", "LOG"]
EnableHybridValuesType = Literal["FALSE", "TRUE"]
ExistConditionType = Literal["MUST_EXIST", "NONE", "NOT_EXIST"]
GetClassifiersPaginatorName = Literal["get_classifiers"]
GetConnectionsPaginatorName = Literal["get_connections"]
GetCrawlerMetricsPaginatorName = Literal["get_crawler_metrics"]
GetCrawlersPaginatorName = Literal["get_crawlers"]
GetDatabasesPaginatorName = Literal["get_databases"]
GetDevEndpointsPaginatorName = Literal["get_dev_endpoints"]
GetJobRunsPaginatorName = Literal["get_job_runs"]
GetJobsPaginatorName = Literal["get_jobs"]
GetPartitionIndexesPaginatorName = Literal["get_partition_indexes"]
GetPartitionsPaginatorName = Literal["get_partitions"]
GetResourcePoliciesPaginatorName = Literal["get_resource_policies"]
GetSecurityConfigurationsPaginatorName = Literal["get_security_configurations"]
GetTableVersionsPaginatorName = Literal["get_table_versions"]
GetTablesPaginatorName = Literal["get_tables"]
GetTriggersPaginatorName = Literal["get_triggers"]
GetUserDefinedFunctionsPaginatorName = Literal["get_user_defined_functions"]
JobBookmarksEncryptionModeType = Literal["CSE-KMS", "DISABLED"]
JobRunStateType = Literal[
    "FAILED", "RUNNING", "STARTING", "STOPPED", "STOPPING", "SUCCEEDED", "TIMEOUT"
]
LanguageType = Literal["PYTHON", "SCALA"]
LastCrawlStatusType = Literal["CANCELLED", "FAILED", "SUCCEEDED"]
ListRegistriesPaginatorName = Literal["list_registries"]
ListSchemaVersionsPaginatorName = Literal["list_schema_versions"]
ListSchemasPaginatorName = Literal["list_schemas"]
LogicalOperatorType = Literal["EQUALS"]
LogicalType = Literal["AND", "ANY"]
MLUserDataEncryptionModeStringType = Literal["DISABLED", "SSE-KMS"]
NodeTypeType = Literal["CRAWLER", "JOB", "TRIGGER"]
PartitionIndexStatusType = Literal["ACTIVE", "CREATING", "DELETING", "FAILED"]
PermissionType = Literal[
    "ALL",
    "ALTER",
    "CREATE_DATABASE",
    "CREATE_TABLE",
    "DATA_LOCATION_ACCESS",
    "DELETE",
    "DROP",
    "INSERT",
    "SELECT",
]
PermissionTypeType = Literal["CELL_FILTER_PERMISSION", "COLUMN_PERMISSION"]
PrincipalTypeType = Literal["GROUP", "ROLE", "USER"]
RecrawlBehaviorType = Literal["CRAWL_EVENT_MODE", "CRAWL_EVERYTHING", "CRAWL_NEW_FOLDERS_ONLY"]
RegistryStatusType = Literal["AVAILABLE", "DELETING"]
ResourceShareTypeType = Literal["ALL", "FOREIGN"]
ResourceTypeType = Literal["ARCHIVE", "FILE", "JAR"]
S3EncryptionModeType = Literal["DISABLED", "SSE-KMS", "SSE-S3"]
ScheduleStateType = Literal["NOT_SCHEDULED", "SCHEDULED", "TRANSITIONING"]
SchemaDiffTypeType = Literal["SYNTAX_DIFF"]
SchemaStatusType = Literal["AVAILABLE", "DELETING", "PENDING"]
SchemaVersionStatusType = Literal["AVAILABLE", "DELETING", "FAILURE", "PENDING"]
SortDirectionTypeType = Literal["ASCENDING", "DESCENDING"]
SortType = Literal["ASC", "DESC"]
TaskRunSortColumnTypeType = Literal["STARTED", "STATUS", "TASK_RUN_TYPE"]
TaskStatusTypeType = Literal[
    "FAILED", "RUNNING", "STARTING", "STOPPED", "STOPPING", "SUCCEEDED", "TIMEOUT"
]
TaskTypeType = Literal[
    "EVALUATION", "EXPORT_LABELS", "FIND_MATCHES", "IMPORT_LABELS", "LABELING_SET_GENERATION"
]
TransformSortColumnTypeType = Literal[
    "CREATED", "LAST_MODIFIED", "NAME", "STATUS", "TRANSFORM_TYPE"
]
TransformStatusTypeType = Literal["DELETING", "NOT_READY", "READY"]
TransformTypeType = Literal["FIND_MATCHES"]
TriggerStateType = Literal[
    "ACTIVATED",
    "ACTIVATING",
    "CREATED",
    "CREATING",
    "DEACTIVATED",
    "DEACTIVATING",
    "DELETING",
    "UPDATING",
]
TriggerTypeType = Literal["CONDITIONAL", "EVENT", "ON_DEMAND", "SCHEDULED"]
UpdateBehaviorType = Literal["LOG", "UPDATE_IN_DATABASE"]
WorkerTypeType = Literal["G.1X", "G.2X", "Standard"]
WorkflowRunStatusType = Literal["COMPLETED", "ERROR", "RUNNING", "STOPPED", "STOPPING"]
GlueServiceName = Literal["glue"]
ServiceName = Literal[
    "accessanalyzer",
    "account",
    "acm",
    "acm-pca",
    "alexaforbusiness",
    "amp",
    "amplify",
    "amplifybackend",
    "amplifyuibuilder",
    "apigateway",
    "apigatewaymanagementapi",
    "apigatewayv2",
    "appconfig",
    "appconfigdata",
    "appflow",
    "appintegrations",
    "application-autoscaling",
    "application-insights",
    "applicationcostprofiler",
    "appmesh",
    "apprunner",
    "appstream",
    "appsync",
    "athena",
    "auditmanager",
    "autoscaling",
    "autoscaling-plans",
    "backup",
    "backup-gateway",
    "batch",
    "billingconductor",
    "braket",
    "budgets",
    "ce",
    "chime",
    "chime-sdk-identity",
    "chime-sdk-meetings",
    "chime-sdk-messaging",
    "cloud9",
    "cloudcontrol",
    "clouddirectory",
    "cloudformation",
    "cloudfront",
    "cloudhsm",
    "cloudhsmv2",
    "cloudsearch",
    "cloudsearchdomain",
    "cloudtrail",
    "cloudwatch",
    "codeartifact",
    "codebuild",
    "codecommit",
    "codedeploy",
    "codeguru-reviewer",
    "codeguruprofiler",
    "codepipeline",
    "codestar",
    "codestar-connections",
    "codestar-notifications",
    "cognito-identity",
    "cognito-idp",
    "cognito-sync",
    "comprehend",
    "comprehendmedical",
    "compute-optimizer",
    "config",
    "connect",
    "connect-contact-lens",
    "connectparticipant",
    "cur",
    "customer-profiles",
    "databrew",
    "dataexchange",
    "datapipeline",
    "datasync",
    "dax",
    "detective",
    "devicefarm",
    "devops-guru",
    "directconnect",
    "discovery",
    "dlm",
    "dms",
    "docdb",
    "drs",
    "ds",
    "dynamodb",
    "dynamodbstreams",
    "ebs",
    "ec2",
    "ec2-instance-connect",
    "ecr",
    "ecr-public",
    "ecs",
    "efs",
    "eks",
    "elastic-inference",
    "elasticache",
    "elasticbeanstalk",
    "elastictranscoder",
    "elb",
    "elbv2",
    "emr",
    "emr-containers",
    "es",
    "events",
    "evidently",
    "finspace",
    "finspace-data",
    "firehose",
    "fis",
    "fms",
    "forecast",
    "forecastquery",
    "frauddetector",
    "fsx",
    "gamelift",
    "glacier",
    "globalaccelerator",
    "glue",
    "grafana",
    "greengrass",
    "greengrassv2",
    "groundstation",
    "guardduty",
    "health",
    "healthlake",
    "honeycode",
    "iam",
    "identitystore",
    "imagebuilder",
    "importexport",
    "inspector",
    "inspector2",
    "iot",
    "iot-data",
    "iot-jobs-data",
    "iot1click-devices",
    "iot1click-projects",
    "iotanalytics",
    "iotdeviceadvisor",
    "iotevents",
    "iotevents-data",
    "iotfleethub",
    "iotsecuretunneling",
    "iotsitewise",
    "iotthingsgraph",
    "iottwinmaker",
    "iotwireless",
    "ivs",
    "kafka",
    "kafkaconnect",
    "kendra",
    "keyspaces",
    "kinesis",
    "kinesis-video-archived-media",
    "kinesis-video-media",
    "kinesis-video-signaling",
    "kinesisanalytics",
    "kinesisanalyticsv2",
    "kinesisvideo",
    "kms",
    "lakeformation",
    "lambda",
    "lex-models",
    "lex-runtime",
    "lexv2-models",
    "lexv2-runtime",
    "license-manager",
    "lightsail",
    "location",
    "logs",
    "lookoutequipment",
    "lookoutmetrics",
    "lookoutvision",
    "machinelearning",
    "macie",
    "macie2",
    "managedblockchain",
    "marketplace-catalog",
    "marketplace-entitlement",
    "marketplacecommerceanalytics",
    "mediaconnect",
    "mediaconvert",
    "medialive",
    "mediapackage",
    "mediapackage-vod",
    "mediastore",
    "mediastore-data",
    "mediatailor",
    "memorydb",
    "meteringmarketplace",
    "mgh",
    "mgn",
    "migration-hub-refactor-spaces",
    "migrationhub-config",
    "migrationhubstrategy",
    "mobile",
    "mq",
    "mturk",
    "mwaa",
    "neptune",
    "network-firewall",
    "networkmanager",
    "nimble",
    "opensearch",
    "opsworks",
    "opsworkscm",
    "organizations",
    "outposts",
    "panorama",
    "personalize",
    "personalize-events",
    "personalize-runtime",
    "pi",
    "pinpoint",
    "pinpoint-email",
    "pinpoint-sms-voice",
    "polly",
    "pricing",
    "proton",
    "qldb",
    "qldb-session",
    "quicksight",
    "ram",
    "rbin",
    "rds",
    "rds-data",
    "redshift",
    "redshift-data",
    "rekognition",
    "resiliencehub",
    "resource-groups",
    "resourcegroupstaggingapi",
    "robomaker",
    "route53",
    "route53-recovery-cluster",
    "route53-recovery-control-config",
    "route53-recovery-readiness",
    "route53domains",
    "route53resolver",
    "rum",
    "s3",
    "s3control",
    "s3outposts",
    "sagemaker",
    "sagemaker-a2i-runtime",
    "sagemaker-edge",
    "sagemaker-featurestore-runtime",
    "sagemaker-runtime",
    "savingsplans",
    "schemas",
    "sdb",
    "secretsmanager",
    "securityhub",
    "serverlessrepo",
    "service-quotas",
    "servicecatalog",
    "servicecatalog-appregistry",
    "servicediscovery",
    "ses",
    "sesv2",
    "shield",
    "signer",
    "sms",
    "sms-voice",
    "snow-device-management",
    "snowball",
    "sns",
    "sqs",
    "ssm",
    "ssm-contacts",
    "ssm-incidents",
    "sso",
    "sso-admin",
    "sso-oidc",
    "stepfunctions",
    "storagegateway",
    "sts",
    "support",
    "swf",
    "synthetics",
    "textract",
    "timestream-query",
    "timestream-write",
    "transcribe",
    "transfer",
    "translate",
    "voice-id",
    "waf",
    "waf-regional",
    "wafv2",
    "wellarchitected",
    "wisdom",
    "workdocs",
    "worklink",
    "workmail",
    "workmailmessageflow",
    "workspaces",
    "workspaces-web",
    "xray",
]
ResourceServiceName = Literal[
    "cloudformation",
    "cloudwatch",
    "dynamodb",
    "ec2",
    "glacier",
    "iam",
    "opsworks",
    "s3",
    "sns",
    "sqs",
]
PaginatorName = Literal[
    "get_classifiers",
    "get_connections",
    "get_crawler_metrics",
    "get_crawlers",
    "get_databases",
    "get_dev_endpoints",
    "get_job_runs",
    "get_jobs",
    "get_partition_indexes",
    "get_partitions",
    "get_resource_policies",
    "get_security_configurations",
    "get_table_versions",
    "get_tables",
    "get_triggers",
    "get_user_defined_functions",
    "list_registries",
    "list_schema_versions",
    "list_schemas",
]
RegionName = Literal[
    "af-south-1",
    "ap-east-1",
    "ap-northeast-1",
    "ap-northeast-2",
    "ap-northeast-3",
    "ap-south-1",
    "ap-southeast-1",
    "ap-southeast-2",
    "ca-central-1",
    "eu-central-1",
    "eu-north-1",
    "eu-south-1",
    "eu-west-1",
    "eu-west-2",
    "eu-west-3",
    "me-south-1",
    "sa-east-1",
    "us-east-1",
    "us-east-2",
    "us-west-1",
    "us-west-2",
]
