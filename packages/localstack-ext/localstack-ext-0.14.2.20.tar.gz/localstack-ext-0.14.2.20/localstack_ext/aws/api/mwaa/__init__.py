import sys
from datetime import datetime
from typing import Dict, List, Optional

if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

from localstack.aws.api import RequestContext, ServiceException, ServiceRequest, handler

AirflowVersion = str
CloudWatchLogGroupArn = str
ConfigKey = str
ConfigValue = str
Double = float
EnvironmentArn = str
EnvironmentClass = str
EnvironmentName = str
ErrorCode = str
ErrorMessage = str
Hostname = str
IamRoleArn = str
Integer = int
KmsKey = str
ListEnvironmentsInputMaxResultsInteger = int
LoggingEnabled = bool
MaxWorkers = int
MinWorkers = int
NextToken = str
RelativePath = str
S3BucketArn = str
S3ObjectVersion = str
Schedulers = int
SecurityGroupId = str
String = str
SubnetId = str
SyntheticCreateCliTokenResponseToken = str
SyntheticCreateWebLoginTokenResponseToken = str
TagKey = str
TagValue = str
UpdateSource = str
WebserverUrl = str
WeeklyMaintenanceWindowStart = str


class EnvironmentStatus(str):
    CREATING = "CREATING"
    CREATE_FAILED = "CREATE_FAILED"
    AVAILABLE = "AVAILABLE"
    UPDATING = "UPDATING"
    DELETING = "DELETING"
    DELETED = "DELETED"
    UNAVAILABLE = "UNAVAILABLE"
    UPDATE_FAILED = "UPDATE_FAILED"


class LoggingLevel(str):
    CRITICAL = "CRITICAL"
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"
    DEBUG = "DEBUG"


class Unit(str):
    Seconds = "Seconds"
    Microseconds = "Microseconds"
    Milliseconds = "Milliseconds"
    Bytes = "Bytes"
    Kilobytes = "Kilobytes"
    Megabytes = "Megabytes"
    Gigabytes = "Gigabytes"
    Terabytes = "Terabytes"
    Bits = "Bits"
    Kilobits = "Kilobits"
    Megabits = "Megabits"
    Gigabits = "Gigabits"
    Terabits = "Terabits"
    Percent = "Percent"
    Count = "Count"
    Bytes_Second = "Bytes/Second"
    Kilobytes_Second = "Kilobytes/Second"
    Megabytes_Second = "Megabytes/Second"
    Gigabytes_Second = "Gigabytes/Second"
    Terabytes_Second = "Terabytes/Second"
    Bits_Second = "Bits/Second"
    Kilobits_Second = "Kilobits/Second"
    Megabits_Second = "Megabits/Second"
    Gigabits_Second = "Gigabits/Second"
    Terabits_Second = "Terabits/Second"
    Count_Second = "Count/Second"
    None_ = "None"


class UpdateStatus(str):
    SUCCESS = "SUCCESS"
    PENDING = "PENDING"
    FAILED = "FAILED"


class WebserverAccessMode(str):
    PRIVATE_ONLY = "PRIVATE_ONLY"
    PUBLIC_ONLY = "PUBLIC_ONLY"


class AccessDeniedException(ServiceException):
    Message: Optional[String]


class InternalServerException(ServiceException):
    message: Optional[String]


class ResourceNotFoundException(ServiceException):
    message: Optional[String]


class ValidationException(ServiceException):
    message: Optional[String]


AirflowConfigurationOptions = Dict[ConfigKey, ConfigValue]


class CreateCliTokenRequest(ServiceRequest):
    Name: EnvironmentName


class CreateCliTokenResponse(TypedDict, total=False):
    CliToken: Optional[SyntheticCreateCliTokenResponseToken]
    WebServerHostname: Optional[Hostname]


TagMap = Dict[TagKey, TagValue]
SubnetList = List[SubnetId]
SecurityGroupList = List[SecurityGroupId]


class NetworkConfiguration(TypedDict, total=False):
    SecurityGroupIds: Optional[SecurityGroupList]
    SubnetIds: Optional[SubnetList]


class ModuleLoggingConfigurationInput(TypedDict, total=False):
    Enabled: LoggingEnabled
    LogLevel: LoggingLevel


class LoggingConfigurationInput(TypedDict, total=False):
    DagProcessingLogs: Optional[ModuleLoggingConfigurationInput]
    SchedulerLogs: Optional[ModuleLoggingConfigurationInput]
    TaskLogs: Optional[ModuleLoggingConfigurationInput]
    WebserverLogs: Optional[ModuleLoggingConfigurationInput]
    WorkerLogs: Optional[ModuleLoggingConfigurationInput]


SyntheticCreateEnvironmentInputAirflowConfigurationOptions = Dict[ConfigKey, ConfigValue]


class CreateEnvironmentInput(ServiceRequest):
    AirflowConfigurationOptions: Optional[
        SyntheticCreateEnvironmentInputAirflowConfigurationOptions
    ]
    AirflowVersion: Optional[AirflowVersion]
    DagS3Path: RelativePath
    EnvironmentClass: Optional[EnvironmentClass]
    ExecutionRoleArn: IamRoleArn
    KmsKey: Optional[KmsKey]
    LoggingConfiguration: Optional[LoggingConfigurationInput]
    MaxWorkers: Optional[MaxWorkers]
    MinWorkers: Optional[MinWorkers]
    Name: EnvironmentName
    NetworkConfiguration: NetworkConfiguration
    PluginsS3ObjectVersion: Optional[S3ObjectVersion]
    PluginsS3Path: Optional[RelativePath]
    RequirementsS3ObjectVersion: Optional[S3ObjectVersion]
    RequirementsS3Path: Optional[RelativePath]
    Schedulers: Optional[Schedulers]
    SourceBucketArn: S3BucketArn
    Tags: Optional[TagMap]
    WebserverAccessMode: Optional[WebserverAccessMode]
    WeeklyMaintenanceWindowStart: Optional[WeeklyMaintenanceWindowStart]


class CreateEnvironmentOutput(TypedDict, total=False):
    Arn: Optional[EnvironmentArn]


class CreateWebLoginTokenRequest(ServiceRequest):
    Name: EnvironmentName


class CreateWebLoginTokenResponse(TypedDict, total=False):
    WebServerHostname: Optional[Hostname]
    WebToken: Optional[SyntheticCreateWebLoginTokenResponseToken]


CreatedAt = datetime


class DeleteEnvironmentInput(ServiceRequest):
    Name: EnvironmentName


class DeleteEnvironmentOutput(TypedDict, total=False):
    pass


class Dimension(TypedDict, total=False):
    Name: String
    Value: String


Dimensions = List[Dimension]


class ModuleLoggingConfiguration(TypedDict, total=False):
    CloudWatchLogGroupArn: Optional[CloudWatchLogGroupArn]
    Enabled: Optional[LoggingEnabled]
    LogLevel: Optional[LoggingLevel]


class LoggingConfiguration(TypedDict, total=False):
    DagProcessingLogs: Optional[ModuleLoggingConfiguration]
    SchedulerLogs: Optional[ModuleLoggingConfiguration]
    TaskLogs: Optional[ModuleLoggingConfiguration]
    WebserverLogs: Optional[ModuleLoggingConfiguration]
    WorkerLogs: Optional[ModuleLoggingConfiguration]


class UpdateError(TypedDict, total=False):
    ErrorCode: Optional[ErrorCode]
    ErrorMessage: Optional[ErrorMessage]


UpdateCreatedAt = datetime


class LastUpdate(TypedDict, total=False):
    CreatedAt: Optional[UpdateCreatedAt]
    Error: Optional[UpdateError]
    Source: Optional[UpdateSource]
    Status: Optional[UpdateStatus]


class Environment(TypedDict, total=False):
    AirflowConfigurationOptions: Optional[AirflowConfigurationOptions]
    AirflowVersion: Optional[AirflowVersion]
    Arn: Optional[EnvironmentArn]
    CreatedAt: Optional[CreatedAt]
    DagS3Path: Optional[RelativePath]
    EnvironmentClass: Optional[EnvironmentClass]
    ExecutionRoleArn: Optional[IamRoleArn]
    KmsKey: Optional[KmsKey]
    LastUpdate: Optional[LastUpdate]
    LoggingConfiguration: Optional[LoggingConfiguration]
    MaxWorkers: Optional[MaxWorkers]
    MinWorkers: Optional[MinWorkers]
    Name: Optional[EnvironmentName]
    NetworkConfiguration: Optional[NetworkConfiguration]
    PluginsS3ObjectVersion: Optional[S3ObjectVersion]
    PluginsS3Path: Optional[RelativePath]
    RequirementsS3ObjectVersion: Optional[S3ObjectVersion]
    RequirementsS3Path: Optional[RelativePath]
    Schedulers: Optional[Schedulers]
    ServiceRoleArn: Optional[IamRoleArn]
    SourceBucketArn: Optional[S3BucketArn]
    Status: Optional[EnvironmentStatus]
    Tags: Optional[TagMap]
    WebserverAccessMode: Optional[WebserverAccessMode]
    WebserverUrl: Optional[WebserverUrl]
    WeeklyMaintenanceWindowStart: Optional[WeeklyMaintenanceWindowStart]


EnvironmentList = List[EnvironmentName]


class GetEnvironmentInput(ServiceRequest):
    Name: EnvironmentName


class GetEnvironmentOutput(TypedDict, total=False):
    Environment: Optional[Environment]


class ListEnvironmentsInput(ServiceRequest):
    MaxResults: Optional[ListEnvironmentsInputMaxResultsInteger]
    NextToken: Optional[NextToken]


class ListEnvironmentsOutput(TypedDict, total=False):
    Environments: EnvironmentList
    NextToken: Optional[NextToken]


class ListTagsForResourceInput(ServiceRequest):
    ResourceArn: EnvironmentArn


class ListTagsForResourceOutput(TypedDict, total=False):
    Tags: Optional[TagMap]


Timestamp = datetime


class StatisticSet(TypedDict, total=False):
    Maximum: Optional[Double]
    Minimum: Optional[Double]
    SampleCount: Optional[Integer]
    Sum: Optional[Double]


class MetricDatum(TypedDict, total=False):
    Dimensions: Optional[Dimensions]
    MetricName: String
    StatisticValues: Optional[StatisticSet]
    Timestamp: Timestamp
    Unit: Optional[Unit]
    Value: Optional[Double]


MetricData = List[MetricDatum]


class PublishMetricsInput(ServiceRequest):
    EnvironmentName: EnvironmentName
    MetricData: MetricData


class PublishMetricsOutput(TypedDict, total=False):
    pass


SyntheticUpdateEnvironmentInputAirflowConfigurationOptions = Dict[ConfigKey, ConfigValue]
TagKeyList = List[TagKey]


class TagResourceInput(ServiceRequest):
    ResourceArn: EnvironmentArn
    Tags: TagMap


class TagResourceOutput(TypedDict, total=False):
    pass


class UntagResourceInput(ServiceRequest):
    ResourceArn: EnvironmentArn
    tagKeys: TagKeyList


class UntagResourceOutput(TypedDict, total=False):
    pass


class UpdateNetworkConfigurationInput(TypedDict, total=False):
    SecurityGroupIds: SecurityGroupList


class UpdateEnvironmentInput(ServiceRequest):
    AirflowConfigurationOptions: Optional[
        SyntheticUpdateEnvironmentInputAirflowConfigurationOptions
    ]
    AirflowVersion: Optional[AirflowVersion]
    DagS3Path: Optional[RelativePath]
    EnvironmentClass: Optional[EnvironmentClass]
    ExecutionRoleArn: Optional[IamRoleArn]
    LoggingConfiguration: Optional[LoggingConfigurationInput]
    MaxWorkers: Optional[MaxWorkers]
    MinWorkers: Optional[MinWorkers]
    Name: EnvironmentName
    NetworkConfiguration: Optional[UpdateNetworkConfigurationInput]
    PluginsS3ObjectVersion: Optional[S3ObjectVersion]
    PluginsS3Path: Optional[RelativePath]
    RequirementsS3ObjectVersion: Optional[S3ObjectVersion]
    RequirementsS3Path: Optional[RelativePath]
    Schedulers: Optional[Schedulers]
    SourceBucketArn: Optional[S3BucketArn]
    WebserverAccessMode: Optional[WebserverAccessMode]
    WeeklyMaintenanceWindowStart: Optional[WeeklyMaintenanceWindowStart]


class UpdateEnvironmentOutput(TypedDict, total=False):
    Arn: Optional[EnvironmentArn]


class MwaaApi:

    service = "mwaa"
    version = "2020-07-01"

    @handler("CreateCliToken")
    def create_cli_token(
        self, context: RequestContext, name: EnvironmentName
    ) -> CreateCliTokenResponse:
        raise NotImplementedError

    @handler("CreateEnvironment")
    def create_environment(
        self,
        context: RequestContext,
        dag_s3_path: RelativePath,
        execution_role_arn: IamRoleArn,
        name: EnvironmentName,
        network_configuration: NetworkConfiguration,
        source_bucket_arn: S3BucketArn,
        airflow_configuration_options: SyntheticCreateEnvironmentInputAirflowConfigurationOptions = None,
        airflow_version: AirflowVersion = None,
        environment_class: EnvironmentClass = None,
        kms_key: KmsKey = None,
        logging_configuration: LoggingConfigurationInput = None,
        max_workers: MaxWorkers = None,
        min_workers: MinWorkers = None,
        plugins_s3_object_version: S3ObjectVersion = None,
        plugins_s3_path: RelativePath = None,
        requirements_s3_object_version: S3ObjectVersion = None,
        requirements_s3_path: RelativePath = None,
        schedulers: Schedulers = None,
        tags: TagMap = None,
        webserver_access_mode: WebserverAccessMode = None,
        weekly_maintenance_window_start: WeeklyMaintenanceWindowStart = None,
    ) -> CreateEnvironmentOutput:
        raise NotImplementedError

    @handler("CreateWebLoginToken")
    def create_web_login_token(
        self, context: RequestContext, name: EnvironmentName
    ) -> CreateWebLoginTokenResponse:
        raise NotImplementedError

    @handler("DeleteEnvironment")
    def delete_environment(
        self, context: RequestContext, name: EnvironmentName
    ) -> DeleteEnvironmentOutput:
        raise NotImplementedError

    @handler("GetEnvironment")
    def get_environment(
        self, context: RequestContext, name: EnvironmentName
    ) -> GetEnvironmentOutput:
        raise NotImplementedError

    @handler("ListEnvironments")
    def list_environments(
        self,
        context: RequestContext,
        max_results: ListEnvironmentsInputMaxResultsInteger = None,
        next_token: NextToken = None,
    ) -> ListEnvironmentsOutput:
        raise NotImplementedError

    @handler("ListTagsForResource")
    def list_tags_for_resource(
        self, context: RequestContext, resource_arn: EnvironmentArn
    ) -> ListTagsForResourceOutput:
        raise NotImplementedError

    @handler("PublishMetrics")
    def publish_metrics(
        self, context: RequestContext, environment_name: EnvironmentName, metric_data: MetricData
    ) -> PublishMetricsOutput:
        raise NotImplementedError

    @handler("TagResource")
    def tag_resource(
        self, context: RequestContext, resource_arn: EnvironmentArn, tags: TagMap
    ) -> TagResourceOutput:
        raise NotImplementedError

    @handler("UntagResource")
    def untag_resource(
        self, context: RequestContext, resource_arn: EnvironmentArn, tag_keys: TagKeyList
    ) -> UntagResourceOutput:
        raise NotImplementedError

    @handler("UpdateEnvironment")
    def update_environment(
        self,
        context: RequestContext,
        name: EnvironmentName,
        airflow_configuration_options: SyntheticUpdateEnvironmentInputAirflowConfigurationOptions = None,
        airflow_version: AirflowVersion = None,
        dag_s3_path: RelativePath = None,
        environment_class: EnvironmentClass = None,
        execution_role_arn: IamRoleArn = None,
        logging_configuration: LoggingConfigurationInput = None,
        max_workers: MaxWorkers = None,
        min_workers: MinWorkers = None,
        network_configuration: UpdateNetworkConfigurationInput = None,
        plugins_s3_object_version: S3ObjectVersion = None,
        plugins_s3_path: RelativePath = None,
        requirements_s3_object_version: S3ObjectVersion = None,
        requirements_s3_path: RelativePath = None,
        schedulers: Schedulers = None,
        source_bucket_arn: S3BucketArn = None,
        webserver_access_mode: WebserverAccessMode = None,
        weekly_maintenance_window_start: WeeklyMaintenanceWindowStart = None,
    ) -> UpdateEnvironmentOutput:
        raise NotImplementedError
