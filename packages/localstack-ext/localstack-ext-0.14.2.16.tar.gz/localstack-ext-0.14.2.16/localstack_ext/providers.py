import functools
from localstack.aws.proxy import AwsApiListener
from localstack.config import is_env_true
from localstack.constants import ENV_PRO_ACTIVATED
from localstack.services.moto import MotoFallbackDispatcher
from localstack.services.plugins import Service,aws_provider
pro_aws_provider=functools.partial(aws_provider,name="pro",should_load=lambda:is_env_true(ENV_PRO_ACTIVATED))
@pro_aws_provider()
def amplify():
 from localstack.aws.proxy import AwsApiListener
 from localstack_ext.services.amplify.provider import AmplifyProvider
 provider=AmplifyProvider()
 return Service("amplify",listener=AwsApiListener("amplify",provider),lifecycle_hook=provider)
@pro_aws_provider()
def appconfig():
 from localstack.aws.proxy import AwsApiListener
 from localstack_ext.services.appconfig.provider import AppconfigProvider
 provider=AppconfigProvider()
 return Service("appconfig",listener=AwsApiListener("appconfig",provider),lifecycle_hook=provider)
@pro_aws_provider(api="application-autoscaling")
def application_autoscaling():
 from localstack_ext.services.applicationautoscaling.provider import(ApplicationAutoscalingProvider)
 provider=ApplicationAutoscalingProvider()
 return Service("application-autoscaling",listener=AwsApiListener("application-autoscaling",MotoFallbackDispatcher(provider)),lifecycle_hook=provider)
@pro_aws_provider()
def appsync():
 from localstack_ext.services.appsync import appsync_starter
 return Service("appsync",start=appsync_starter.start_appsync)
@pro_aws_provider()
def athena():
 from localstack.aws.proxy import AwsApiListener
 from localstack_ext.services.athena.provider import AthenaProvider
 provider=AthenaProvider()
 return Service("athena",listener=AwsApiListener("athena",provider),lifecycle_hook=provider)
@pro_aws_provider()
def autoscaling():
 from localstack_ext.services.autoscaling.provider import AutoscalingProvider
 provider=AutoscalingProvider()
 return Service("autoscaling",listener=AwsApiListener("autoscaling",MotoFallbackDispatcher(provider)))
@pro_aws_provider()
def azure():
 from localstack_ext.services.azure import azure_starter
 return Service("azure",start=azure_starter.start_azure)
@pro_aws_provider()
def backup():
 from localstack.aws.proxy import AwsApiListener
 from localstack_ext.services.backup.provider import BackupProvider
 provider=BackupProvider()
 return Service("backup",listener=AwsApiListener("backup",provider),lifecycle_hook=provider)
@pro_aws_provider()
def batch():
 from localstack_ext.services.batch.provider import BatchProvider
 provider=BatchProvider()
 listener=AwsApiListener("batch",MotoFallbackDispatcher(provider))
 return Service("batch",listener=listener)
@pro_aws_provider()
def ce():
 from localstack.aws.proxy import AwsApiListener
 from localstack_ext.services.costexplorer.provider import CeProvider
 provider=CeProvider()
 return Service("ce",listener=AwsApiListener("ce",provider),lifecycle_hook=provider)
@pro_aws_provider()
def cloudfront():
 from localstack.aws.proxy import AwsApiListener
 from localstack_ext.services.cloudfront.provider import CloudFrontProvider
 provider=CloudFrontProvider()
 return Service("cloudfront",listener=AwsApiListener("cloudfront",provider),lifecycle_hook=provider)
@pro_aws_provider()
def cloudtrail():
 from localstack.aws.proxy import AwsApiListener
 from localstack_ext.services.cloudtrail.provider import CloudtrailProvider
 provider=CloudtrailProvider()
 return Service("cloudtrail",listener=AwsApiListener("cloudtrail",provider),lifecycle_hook=provider)
@pro_aws_provider()
def codecommit():
 from localstack_ext.services.codecommit import codecommit_listener,codecommit_starter
 return Service("codecommit",start=codecommit_starter.start_codecommit,listener=codecommit_listener.UPDATE_CODECOMMIT)
@pro_aws_provider(api="cognito-identity")
def cognito_identity():
 from localstack_ext.services.cognito_identity.provider import CognitoIdentityAWSApiListener
 listener=CognitoIdentityAWSApiListener()
 return Service("cognito-identity",listener=listener,lifecycle_hook=listener.provider)
@pro_aws_provider(api="cognito-idp")
def cognito_idp():
 from localstack.aws.proxy import AwsApiListener
 from localstack_ext.services.cognito_idp.provider import CognitoIdpProvider
 provider=CognitoIdpProvider()
 return Service("cognito-idp",listener=AwsApiListener("cognito-idp",provider),lifecycle_hook=provider)
@pro_aws_provider()
def docdb():
 from localstack_ext.services.docdb import docdb_api
 return Service("docdb",start=docdb_api.start_docdb)
@pro_aws_provider()
def ec2():
 from localstack_ext.services.ec2.provider import Ec2Provider
 provider=Ec2Provider()
 listener=AwsApiListener("ec2",MotoFallbackDispatcher(provider))
 return Service("ec2",listener=listener,lifecycle_hook=provider)
@pro_aws_provider()
def ecr():
 from localstack_ext.services.ecr.provider import EcrProvider
 provider=EcrProvider()
 return Service("ecr",listener=AwsApiListener("ecr",MotoFallbackDispatcher(provider)),lifecycle_hook=provider)
@pro_aws_provider()
def ecs():
 from localstack_ext.services.ecs import ecs_listener,ecs_starter
 return Service("ecs",start=ecs_starter.start_ecs,listener=ecs_listener.UPDATE_ECS)
@pro_aws_provider()
def efs():
 from localstack.aws.proxy import AwsApiListener
 from localstack_ext.services.efs.provider import EfsProvider
 provider=EfsProvider()
 return Service("efs",listener=AwsApiListener("efs",provider),lifecycle_hook=provider)
@pro_aws_provider()
def elasticache():
 from localstack_ext.services.elasticache import elasticache_starter
 return Service("elasticache",start=elasticache_starter.start_elasticache)
@pro_aws_provider()
def elasticbeanstalk():
 from localstack.aws.proxy import AwsApiListener
 from localstack_ext.services.elasticbeanstalk.provider import ElasticBeanstalkProvider
 provider=ElasticBeanstalkProvider()
 return Service("elasticbeanstalk",listener=AwsApiListener("elasticbeanstalk",provider),lifecycle_hook=provider)
@pro_aws_provider()
def elb():
 from localstack_ext.services.elb.provider import ElbProvider
 from localstack_ext.services.elb.routing import ElbApiListener
 provider=ElbProvider()
 listener=ElbApiListener("elb",MotoFallbackDispatcher(provider))
 return Service("elb",listener=listener,lifecycle_hook=provider)
@pro_aws_provider()
def elbv2():
 from localstack_ext.services.elb.routing import ElbApiListener
 from localstack_ext.services.elbv2.provider import Elbv2Provider
 provider=Elbv2Provider()
 listener=ElbApiListener("elbv2",MotoFallbackDispatcher(provider))
 return Service("elbv2",listener=listener,lifecycle_hook=provider)
@pro_aws_provider()
def eks():
 from localstack.aws.proxy import AwsApiListener
 from localstack_ext.services.eks.provider import EksProvider
 provider=EksProvider()
 return Service("eks",listener=AwsApiListener("eks",provider),lifecycle_hook=provider)
@pro_aws_provider()
def emr():
 from localstack_ext.services.emr.provider import EmrProvider
 provider=EmrProvider()
 return Service("emr",listener=AwsApiListener("emr",MotoFallbackDispatcher(provider)),lifecycle_hook=provider)
@pro_aws_provider()
def glacier():
 from localstack_ext.services.glacier.provider import GlacierProvider
 provider=GlacierProvider()
 return Service("glacier",listener=AwsApiListener("glacier",MotoFallbackDispatcher(provider)),lifecycle_hook=provider)
@pro_aws_provider()
def glue():
 from localstack_ext.services.glue.provider import GlueProvider
 provider=GlueProvider()
 return Service("glue",listener=AwsApiListener("glue",provider),lifecycle_hook=provider)
@pro_aws_provider()
def iot():
 from localstack_ext.services.iot import iot_listener,iot_starter
 return Service("iot",start=iot_starter.start_iot,listener=iot_listener.UPDATE_IOT)
@pro_aws_provider(api="iot-data")
def iot_data():
 from localstack.services import plugins
 def require_iot(*args,**kwargs):
  plugins.SERVICE_PLUGINS.require("iot")
 return Service("iot-data",start=require_iot)
@pro_aws_provider(api="iotanalytics")
def iot_analytics():
 from localstack.services import plugins
 def require_iot(*args,**kwargs):
  plugins.SERVICE_PLUGINS.require("iot")
 return Service("iotanalytics",start=require_iot)
@pro_aws_provider()
def kafka():
 from localstack_ext.services.kafka import kafka_starter
 return Service("kafka",start=kafka_starter.start_kafka)
@pro_aws_provider()
def kinesisanalytics():
 from localstack_ext.services.kinesisanalytics import kinesis_analytics_api
 return Service("kinesisanalytics",start=kinesis_analytics_api.start_kinesis_analytics)
@pro_aws_provider()
def lakeformation():
 from localstack.aws.proxy import AwsApiListener
 from localstack_ext.services.lakeformation.provider import LakeFormationProvider
 provider=LakeFormationProvider()
 return Service("lakeformation",listener=AwsApiListener("lakeformation",provider),lifecycle_hook=provider)
@pro_aws_provider()
def logs():
 from localstack.services.logs.provider import LogsAwsApiListener
 from localstack_ext.services.logs import logs_extended
 listener=LogsAwsApiListener()
 provider=listener.provider
 return Service("logs",listener=listener,lifecycle_hook=provider)
@pro_aws_provider()
def mediastore():
 from localstack_ext.services.mediastore.provider import MediastoreProvider
 provider=MediastoreProvider()
 return Service("mediastore",listener=AwsApiListener("mediastore",provider),lifecycle_hook=provider)
@pro_aws_provider(api="mediastore-data")
def mediastore_data():
 from localstack_ext.services.mediastore.provider import MediaStoreDataProvider
 provider=MediaStoreDataProvider()
 return Service("mediastore-data",listener=AwsApiListener("mediastore-data",provider),lifecycle_hook=provider)
@pro_aws_provider()
def mwaa():
 from localstack_ext.services.mwaa.provider import MwaaProvider
 provider=MwaaProvider()
 return Service("mwaa",listener=AwsApiListener("mwaa",provider),lifecycle_hook=provider)
@pro_aws_provider()
def neptune():
 from localstack_ext.services.neptune import neptune_api
 return Service("neptune",start=neptune_api.start_neptune)
@pro_aws_provider()
def organizations():
 from localstack_ext.services.organizations.provider import OrganizationsProvider
 provider=OrganizationsProvider()
 listener=AwsApiListener("organizations",MotoFallbackDispatcher(provider))
 return Service("organizations",listener=listener)
@pro_aws_provider()
def qldb():
 from localstack.aws.proxy import AwsApiListener
 from localstack_ext.services.qldb.provider import QldbProvider
 provider=QldbProvider()
 return Service("qldb",listener=AwsApiListener("qldb",provider),lifecycle_hook=provider)
@pro_aws_provider(api="qldb-session")
def qldb_session():
 from localstack.aws.proxy import AwsApiListener
 from localstack_ext.services.qldb.provider import QldbSessionProvider
 provider=QldbSessionProvider()
 return Service("qldb-session",listener=AwsApiListener("qldb-session",provider),lifecycle_hook=provider)
@pro_aws_provider()
def rds():
 from localstack.aws.proxy import AsfWithFallbackListener
 from localstack_ext.services.rds import rds_listener,rds_starter
 from localstack_ext.services.rds.provider import RdsProvider
 asf_listener=AsfWithFallbackListener("rds",RdsProvider(),rds_listener.UPDATE_RDS)
 return Service("rds",start=rds_starter.start_rds,listener=asf_listener)
@pro_aws_provider(api="rds-data")
def rds_data():
 from localstack_ext.services.rds_data.provider import RdsDataProvider
 provider=RdsDataProvider()
 return Service("rds-data",listener=AwsApiListener("rds-data",provider))
@pro_aws_provider()
def redshift():
 from localstack_ext.services.redshift.provider import RedshiftProvider
 provider=RedshiftProvider()
 listener=AwsApiListener("redshift",MotoFallbackDispatcher(provider))
 return Service("redshift",listener=listener,lifecycle_hook=provider)
@pro_aws_provider(api="redshift-data")
def redshift_data():
 from localstack_ext.services.redshift.provider import RedshiftDataProvider
 provider=RedshiftDataProvider()
 listener=AwsApiListener("redshift-data",provider)
 return Service("redshift-data",listener=listener)
@pro_aws_provider()
def sagemaker():
 from localstack_ext.services.sagemaker import sagemaker_starter
 return Service("sagemaker",start=sagemaker_starter.start_sagemaker)
@pro_aws_provider()
def serverlessrepo():
 from localstack_ext.services.serverlessrepo.provider import ServerlessrepoProvider
 provider=ServerlessrepoProvider()
 return Service("serverlessrepo",listener=AwsApiListener("serverlessrepo",provider),lifecycle_hook=provider)
@pro_aws_provider()
def servicediscovery():
 from localstack.aws.proxy import AwsApiListener
 from localstack_ext.services.servicediscovery.provider import ServicediscoveryProvider
 provider=ServicediscoveryProvider()
 return Service("servicediscovery",listener=AwsApiListener("servicediscovery",provider),lifecycle_hook=provider)
@pro_aws_provider()
def ssm():
 from localstack_ext.services.ssm.provider import SsmProvider
 provider=SsmProvider()
 listener=AwsApiListener("ssm",MotoFallbackDispatcher(provider))
 return Service("ssm",listener=listener,lifecycle_hook=provider)
@pro_aws_provider(api="timestream-write")
def timestream_write():
 from localstack_ext.services.timestream.provider import TimestreamWriteProvider
 return Service("timestream-write",listener=AwsApiListener("timestream-write",TimestreamWriteProvider()))
@pro_aws_provider(api="timestream-query")
def timestream_query():
 from localstack_ext.services.timestream.provider import TimestreamQueryProvider
 return Service("timestream-query",listener=AwsApiListener("timestream-query",TimestreamQueryProvider()))
@pro_aws_provider()
def transfer():
 from localstack_ext.services.transfer.provider import TransferProvider
 provider=TransferProvider()
 return Service("transfer",listener=AwsApiListener("transfer",provider),lifecycle_hook=provider)
@pro_aws_provider()
def xray():
 from localstack_ext.services.xray.provider import XrayProvider
 provider=XrayProvider()
 listener=AwsApiListener("xray",MotoFallbackDispatcher(provider))
 return Service("xray",listener=listener)
@pro_aws_provider()
def apigateway():
 from localstack.services.apigateway import apigateway_listener,apigateway_starter
 from localstack_ext.services.apigateway import apigateway_extended
 apigateway_extended.patch_apigateway()
 return Service("apigateway",listener=apigateway_listener.UPDATE_APIGATEWAY,start=apigateway_starter.start_apigateway)
@pro_aws_provider(api="lambda")
def awslambda():
 from localstack.services.awslambda import lambda_starter
 from localstack_ext.services.awslambda.lambda_extended import patch_lambda
 patch_lambda()
 return Service("lambda",start=lambda_starter.start_lambda,stop=lambda_starter.stop_lambda,check=lambda_starter.check_lambda)
@pro_aws_provider()
def cloudformation():
 from localstack.services.cloudformation.provider import CloudformationProvider
 from localstack_ext.services.cloudformation import cloudformation_extended
 cloudformation_extended.patch_cloudformation()
 provider=CloudformationProvider()
 return Service("cloudformation",listener=AwsApiListener("cloudformation",provider))
@pro_aws_provider()
def dynamodb():
 from localstack.services.dynamodb.provider import DynamoDBApiListener
 from localstack_ext.services.dynamodb.provider import DynamoDBProviderExt
 provider=DynamoDBProviderExt()
 listener=DynamoDBApiListener(provider=provider)
 return Service("dynamodb",listener=listener,lifecycle_hook=provider)
@pro_aws_provider()
def events():
 from localstack.services.events import events_listener,events_starter
 from localstack_ext.services.events import events_extended
 events_extended.patch_events()
 return Service("events",listener=events_listener.UPDATE_EVENTS,start=events_starter.start_events)
@pro_aws_provider()
def iam():
 from localstack.services.iam import iam_listener,iam_starter
 from localstack_ext.services.iam import iam_extended
 iam_extended.patch_iam()
 return Service("iam",listener=iam_listener.UPDATE_IAM,start=iam_starter.start_iam)
@pro_aws_provider()
def kms():
 from localstack.services.providers import kms as default_kms
 from localstack_ext.services.kms import kms_extended
 kms_extended.patch_kms()
 return default_kms.factory.__wrapped__()
@pro_aws_provider()
def opensearch():
 from localstack.aws.proxy import AwsApiListener
 from localstack_ext.services.opensearch.provider import OpensearchProvider
 provider=OpensearchProvider()
 return Service("opensearch",listener=AwsApiListener("opensearch",provider),lifecycle_hook=provider)
@pro_aws_provider()
def route53():
 from localstack.services.route53.provider import Route53Provider
 from localstack_ext.services.route53 import route53_extended
 route53_extended.patch_route53()
 provider=Route53Provider()
 return Service("route53",listener=AwsApiListener("route53",MotoFallbackDispatcher(provider)))
@pro_aws_provider()
def s3():
 from localstack.services.s3 import s3_listener,s3_starter
 from localstack_ext.services.s3 import s3_extended
 s3_extended.patch_s3()
 return Service("s3",listener=s3_listener.UPDATE_S3,start=s3_starter.start_s3,check=s3_starter.check_s3)
@pro_aws_provider()
def secretsmanager():
 from localstack.services.secretsmanager.provider import SecretsmanagerProvider
 from localstack_ext.services.secretsmanager.secretsmanager_extended import patch_secretsmanager
 patch_secretsmanager()
 provider=SecretsmanagerProvider()
 return Service("secretsmanager",listener=AwsApiListener("secretsmanager",MotoFallbackDispatcher(provider)))
@pro_aws_provider()
def ses():
 from localstack_ext.services.ses.provider import SesProvider
 provider=SesProvider()
 listener=AwsApiListener("ses",MotoFallbackDispatcher(provider))
 return Service("ses",listener=listener,lifecycle_hook=provider)
@pro_aws_provider()
def sesv2():
 from localstack_ext.services.sesv2.provider import Sesv2Provider
 provider=Sesv2Provider()
 listener=AwsApiListener("sesv2",provider)
 return Service("sesv2",listener=listener,lifecycle_hook=provider)
@pro_aws_provider()
def sns():
 from localstack.services.sns import sns_listener,sns_starter
 from localstack_ext.services.sns import sns_extended
 sns_extended.patch_sns()
 return Service("sns",listener=sns_listener.UPDATE_SNS,start=sns_starter.start_sns)
@pro_aws_provider()
def sqs():
 from localstack.services.sqs import sqs_listener,sqs_starter
 from localstack_ext.services.sqs.sqs_extended import patch_sqs
 patch_sqs()
 return Service("sqs",listener=sqs_listener.UPDATE_SQS,start=sqs_starter.start_sqs,check=sqs_starter.check_sqs)
@pro_aws_provider()
def stepfunctions():
 from localstack.services.providers import stepfunctions as default_stepfunctions
 from localstack_ext.services.stepfunctions.stepfunctions_extended import patch_stepfunctions
 patch_stepfunctions()
 return default_stepfunctions.factory.__wrapped__()
@pro_aws_provider()
def sts():
 from localstack.services.providers import sts as default_sts
 from localstack_ext.services.sts import sts_extended
 sts_extended.patch_sts()
 return default_sts.factory.__wrapped__()
@pro_aws_provider(name="mock",api="eks")
def eks_mock():
 from localstack.aws.proxy import AwsApiListener
 from localstack_ext.services.eks.provider import EksMockProvider
 provider=EksMockProvider()
 return Service("eks",listener=AwsApiListener("eks",provider),lifecycle_hook=provider)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
