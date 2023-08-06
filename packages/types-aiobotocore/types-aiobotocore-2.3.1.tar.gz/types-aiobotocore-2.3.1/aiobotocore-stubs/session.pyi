import sys
from typing import Any, List, Optional, Union, overload

from aiobotocore.client import AioBaseClient as AioBaseClient
from aiobotocore.client import AioClientCreator as AioClientCreator
from aiobotocore.credentials import AioCredentials as AioCredentials
from aiobotocore.credentials import create_credential_resolver as create_credential_resolver
from aiobotocore.handlers import inject_presigned_url_ec2 as inject_presigned_url_ec2
from aiobotocore.handlers import inject_presigned_url_rds as inject_presigned_url_rds
from aiobotocore.hooks import AioHierarchicalEmitter as AioHierarchicalEmitter
from aiobotocore.parsers import AioResponseParserFactory as AioResponseParserFactory
from aiobotocore.signers import add_generate_db_auth_token as add_generate_db_auth_token
from aiobotocore.signers import add_generate_presigned_post as add_generate_presigned_post
from aiobotocore.signers import add_generate_presigned_url as add_generate_presigned_url
from botocore.config import Config
from botocore.model import ServiceModel
from botocore.session import Session
from types_aiobotocore_accessanalyzer.client import AccessAnalyzerClient
from types_aiobotocore_account.client import AccountClient
from types_aiobotocore_acm.client import ACMClient
from types_aiobotocore_acm_pca.client import ACMPCAClient
from types_aiobotocore_alexaforbusiness.client import AlexaForBusinessClient
from types_aiobotocore_amp.client import PrometheusServiceClient
from types_aiobotocore_amplify.client import AmplifyClient
from types_aiobotocore_amplifybackend.client import AmplifyBackendClient
from types_aiobotocore_amplifyuibuilder.client import AmplifyUIBuilderClient
from types_aiobotocore_apigateway.client import APIGatewayClient
from types_aiobotocore_apigatewaymanagementapi.client import ApiGatewayManagementApiClient
from types_aiobotocore_apigatewayv2.client import ApiGatewayV2Client
from types_aiobotocore_appconfig.client import AppConfigClient
from types_aiobotocore_appconfigdata.client import AppConfigDataClient
from types_aiobotocore_appflow.client import AppflowClient
from types_aiobotocore_appintegrations.client import AppIntegrationsServiceClient
from types_aiobotocore_application_autoscaling.client import ApplicationAutoScalingClient
from types_aiobotocore_application_insights.client import ApplicationInsightsClient
from types_aiobotocore_applicationcostprofiler.client import ApplicationCostProfilerClient
from types_aiobotocore_appmesh.client import AppMeshClient
from types_aiobotocore_apprunner.client import AppRunnerClient
from types_aiobotocore_appstream.client import AppStreamClient
from types_aiobotocore_appsync.client import AppSyncClient
from types_aiobotocore_athena.client import AthenaClient
from types_aiobotocore_auditmanager.client import AuditManagerClient
from types_aiobotocore_autoscaling.client import AutoScalingClient
from types_aiobotocore_autoscaling_plans.client import AutoScalingPlansClient
from types_aiobotocore_backup.client import BackupClient
from types_aiobotocore_backup_gateway.client import BackupGatewayClient
from types_aiobotocore_batch.client import BatchClient
from types_aiobotocore_billingconductor.client import BillingConductorClient
from types_aiobotocore_braket.client import BraketClient
from types_aiobotocore_budgets.client import BudgetsClient
from types_aiobotocore_ce.client import CostExplorerClient
from types_aiobotocore_chime.client import ChimeClient
from types_aiobotocore_chime_sdk_identity.client import ChimeSDKIdentityClient
from types_aiobotocore_chime_sdk_meetings.client import ChimeSDKMeetingsClient
from types_aiobotocore_chime_sdk_messaging.client import ChimeSDKMessagingClient
from types_aiobotocore_cloud9.client import Cloud9Client
from types_aiobotocore_cloudcontrol.client import CloudControlApiClient
from types_aiobotocore_clouddirectory.client import CloudDirectoryClient
from types_aiobotocore_cloudformation.client import CloudFormationClient
from types_aiobotocore_cloudfront.client import CloudFrontClient
from types_aiobotocore_cloudhsm.client import CloudHSMClient
from types_aiobotocore_cloudhsmv2.client import CloudHSMV2Client
from types_aiobotocore_cloudsearch.client import CloudSearchClient
from types_aiobotocore_cloudsearchdomain.client import CloudSearchDomainClient
from types_aiobotocore_cloudtrail.client import CloudTrailClient
from types_aiobotocore_cloudwatch.client import CloudWatchClient
from types_aiobotocore_codeartifact.client import CodeArtifactClient
from types_aiobotocore_codebuild.client import CodeBuildClient
from types_aiobotocore_codecommit.client import CodeCommitClient
from types_aiobotocore_codedeploy.client import CodeDeployClient
from types_aiobotocore_codeguru_reviewer.client import CodeGuruReviewerClient
from types_aiobotocore_codeguruprofiler.client import CodeGuruProfilerClient
from types_aiobotocore_codepipeline.client import CodePipelineClient
from types_aiobotocore_codestar.client import CodeStarClient
from types_aiobotocore_codestar_connections.client import CodeStarconnectionsClient
from types_aiobotocore_codestar_notifications.client import CodeStarNotificationsClient
from types_aiobotocore_cognito_identity.client import CognitoIdentityClient
from types_aiobotocore_cognito_idp.client import CognitoIdentityProviderClient
from types_aiobotocore_cognito_sync.client import CognitoSyncClient
from types_aiobotocore_comprehend.client import ComprehendClient
from types_aiobotocore_comprehendmedical.client import ComprehendMedicalClient
from types_aiobotocore_compute_optimizer.client import ComputeOptimizerClient
from types_aiobotocore_config.client import ConfigServiceClient
from types_aiobotocore_connect.client import ConnectClient
from types_aiobotocore_connect_contact_lens.client import ConnectContactLensClient
from types_aiobotocore_connectparticipant.client import ConnectParticipantClient
from types_aiobotocore_cur.client import CostandUsageReportServiceClient
from types_aiobotocore_customer_profiles.client import CustomerProfilesClient
from types_aiobotocore_databrew.client import GlueDataBrewClient
from types_aiobotocore_dataexchange.client import DataExchangeClient
from types_aiobotocore_datapipeline.client import DataPipelineClient
from types_aiobotocore_datasync.client import DataSyncClient
from types_aiobotocore_dax.client import DAXClient
from types_aiobotocore_detective.client import DetectiveClient
from types_aiobotocore_devicefarm.client import DeviceFarmClient
from types_aiobotocore_devops_guru.client import DevOpsGuruClient
from types_aiobotocore_directconnect.client import DirectConnectClient
from types_aiobotocore_discovery.client import ApplicationDiscoveryServiceClient
from types_aiobotocore_dlm.client import DLMClient
from types_aiobotocore_dms.client import DatabaseMigrationServiceClient
from types_aiobotocore_docdb.client import DocDBClient
from types_aiobotocore_drs.client import drsClient
from types_aiobotocore_ds.client import DirectoryServiceClient
from types_aiobotocore_dynamodb.client import DynamoDBClient
from types_aiobotocore_dynamodbstreams.client import DynamoDBStreamsClient
from types_aiobotocore_ebs.client import EBSClient
from types_aiobotocore_ec2.client import EC2Client
from types_aiobotocore_ec2_instance_connect.client import EC2InstanceConnectClient
from types_aiobotocore_ecr.client import ECRClient
from types_aiobotocore_ecr_public.client import ECRPublicClient
from types_aiobotocore_ecs.client import ECSClient
from types_aiobotocore_efs.client import EFSClient
from types_aiobotocore_eks.client import EKSClient
from types_aiobotocore_elastic_inference.client import ElasticInferenceClient
from types_aiobotocore_elasticache.client import ElastiCacheClient
from types_aiobotocore_elasticbeanstalk.client import ElasticBeanstalkClient
from types_aiobotocore_elastictranscoder.client import ElasticTranscoderClient
from types_aiobotocore_elb.client import ElasticLoadBalancingClient
from types_aiobotocore_elbv2.client import ElasticLoadBalancingv2Client
from types_aiobotocore_emr.client import EMRClient
from types_aiobotocore_emr_containers.client import EMRContainersClient
from types_aiobotocore_es.client import ElasticsearchServiceClient
from types_aiobotocore_events.client import EventBridgeClient
from types_aiobotocore_evidently.client import CloudWatchEvidentlyClient
from types_aiobotocore_finspace.client import finspaceClient
from types_aiobotocore_finspace_data.client import FinSpaceDataClient
from types_aiobotocore_firehose.client import FirehoseClient
from types_aiobotocore_fis.client import FISClient
from types_aiobotocore_fms.client import FMSClient
from types_aiobotocore_forecast.client import ForecastServiceClient
from types_aiobotocore_forecastquery.client import ForecastQueryServiceClient
from types_aiobotocore_frauddetector.client import FraudDetectorClient
from types_aiobotocore_fsx.client import FSxClient
from types_aiobotocore_gamelift.client import GameLiftClient
from types_aiobotocore_glacier.client import GlacierClient
from types_aiobotocore_globalaccelerator.client import GlobalAcceleratorClient
from types_aiobotocore_glue.client import GlueClient
from types_aiobotocore_grafana.client import ManagedGrafanaClient
from types_aiobotocore_greengrass.client import GreengrassClient
from types_aiobotocore_greengrassv2.client import GreengrassV2Client
from types_aiobotocore_groundstation.client import GroundStationClient
from types_aiobotocore_guardduty.client import GuardDutyClient
from types_aiobotocore_health.client import HealthClient
from types_aiobotocore_healthlake.client import HealthLakeClient
from types_aiobotocore_honeycode.client import HoneycodeClient
from types_aiobotocore_iam.client import IAMClient
from types_aiobotocore_identitystore.client import IdentityStoreClient
from types_aiobotocore_imagebuilder.client import imagebuilderClient
from types_aiobotocore_importexport.client import ImportExportClient
from types_aiobotocore_inspector2.client import Inspector2Client
from types_aiobotocore_inspector.client import InspectorClient
from types_aiobotocore_iot1click_devices.client import IoT1ClickDevicesServiceClient
from types_aiobotocore_iot1click_projects.client import IoT1ClickProjectsClient
from types_aiobotocore_iot.client import IoTClient
from types_aiobotocore_iot_data.client import IoTDataPlaneClient
from types_aiobotocore_iot_jobs_data.client import IoTJobsDataPlaneClient
from types_aiobotocore_iotanalytics.client import IoTAnalyticsClient
from types_aiobotocore_iotdeviceadvisor.client import IoTDeviceAdvisorClient
from types_aiobotocore_iotevents.client import IoTEventsClient
from types_aiobotocore_iotevents_data.client import IoTEventsDataClient
from types_aiobotocore_iotfleethub.client import IoTFleetHubClient
from types_aiobotocore_iotsecuretunneling.client import IoTSecureTunnelingClient
from types_aiobotocore_iotsitewise.client import IoTSiteWiseClient
from types_aiobotocore_iotthingsgraph.client import IoTThingsGraphClient
from types_aiobotocore_iottwinmaker.client import IoTTwinMakerClient
from types_aiobotocore_iotwireless.client import IoTWirelessClient
from types_aiobotocore_ivs.client import IVSClient
from types_aiobotocore_kafka.client import KafkaClient
from types_aiobotocore_kafkaconnect.client import KafkaConnectClient
from types_aiobotocore_kendra.client import kendraClient
from types_aiobotocore_keyspaces.client import KeyspacesClient
from types_aiobotocore_kinesis.client import KinesisClient
from types_aiobotocore_kinesis_video_archived_media.client import KinesisVideoArchivedMediaClient
from types_aiobotocore_kinesis_video_media.client import KinesisVideoMediaClient
from types_aiobotocore_kinesis_video_signaling.client import KinesisVideoSignalingChannelsClient
from types_aiobotocore_kinesisanalytics.client import KinesisAnalyticsClient
from types_aiobotocore_kinesisanalyticsv2.client import KinesisAnalyticsV2Client
from types_aiobotocore_kinesisvideo.client import KinesisVideoClient
from types_aiobotocore_kms.client import KMSClient
from types_aiobotocore_lakeformation.client import LakeFormationClient
from types_aiobotocore_lambda.client import LambdaClient
from types_aiobotocore_lex_models.client import LexModelBuildingServiceClient
from types_aiobotocore_lex_runtime.client import LexRuntimeServiceClient
from types_aiobotocore_lexv2_models.client import LexModelsV2Client
from types_aiobotocore_lexv2_runtime.client import LexRuntimeV2Client
from types_aiobotocore_license_manager.client import LicenseManagerClient
from types_aiobotocore_lightsail.client import LightsailClient
from types_aiobotocore_location.client import LocationServiceClient
from types_aiobotocore_logs.client import CloudWatchLogsClient
from types_aiobotocore_lookoutequipment.client import LookoutEquipmentClient
from types_aiobotocore_lookoutmetrics.client import LookoutMetricsClient
from types_aiobotocore_lookoutvision.client import LookoutforVisionClient
from types_aiobotocore_machinelearning.client import MachineLearningClient
from types_aiobotocore_macie2.client import Macie2Client
from types_aiobotocore_macie.client import MacieClient
from types_aiobotocore_managedblockchain.client import ManagedBlockchainClient
from types_aiobotocore_marketplace_catalog.client import MarketplaceCatalogClient
from types_aiobotocore_marketplace_entitlement.client import MarketplaceEntitlementServiceClient
from types_aiobotocore_marketplacecommerceanalytics.client import MarketplaceCommerceAnalyticsClient
from types_aiobotocore_mediaconnect.client import MediaConnectClient
from types_aiobotocore_mediaconvert.client import MediaConvertClient
from types_aiobotocore_medialive.client import MediaLiveClient
from types_aiobotocore_mediapackage.client import MediaPackageClient
from types_aiobotocore_mediapackage_vod.client import MediaPackageVodClient
from types_aiobotocore_mediastore.client import MediaStoreClient
from types_aiobotocore_mediastore_data.client import MediaStoreDataClient
from types_aiobotocore_mediatailor.client import MediaTailorClient
from types_aiobotocore_memorydb.client import MemoryDBClient
from types_aiobotocore_meteringmarketplace.client import MarketplaceMeteringClient
from types_aiobotocore_mgh.client import MigrationHubClient
from types_aiobotocore_mgn.client import mgnClient
from types_aiobotocore_migration_hub_refactor_spaces.client import MigrationHubRefactorSpacesClient
from types_aiobotocore_migrationhub_config.client import MigrationHubConfigClient
from types_aiobotocore_migrationhubstrategy.client import MigrationHubStrategyRecommendationsClient
from types_aiobotocore_mobile.client import MobileClient
from types_aiobotocore_mq.client import MQClient
from types_aiobotocore_mturk.client import MTurkClient
from types_aiobotocore_mwaa.client import MWAAClient
from types_aiobotocore_neptune.client import NeptuneClient
from types_aiobotocore_network_firewall.client import NetworkFirewallClient
from types_aiobotocore_networkmanager.client import NetworkManagerClient
from types_aiobotocore_nimble.client import NimbleStudioClient
from types_aiobotocore_opensearch.client import OpenSearchServiceClient
from types_aiobotocore_opsworks.client import OpsWorksClient
from types_aiobotocore_opsworkscm.client import OpsWorksCMClient
from types_aiobotocore_organizations.client import OrganizationsClient
from types_aiobotocore_outposts.client import OutpostsClient
from types_aiobotocore_panorama.client import PanoramaClient
from types_aiobotocore_personalize.client import PersonalizeClient
from types_aiobotocore_personalize_events.client import PersonalizeEventsClient
from types_aiobotocore_personalize_runtime.client import PersonalizeRuntimeClient
from types_aiobotocore_pi.client import PIClient
from types_aiobotocore_pinpoint.client import PinpointClient
from types_aiobotocore_pinpoint_email.client import PinpointEmailClient
from types_aiobotocore_pinpoint_sms_voice.client import PinpointSMSVoiceClient
from types_aiobotocore_polly.client import PollyClient
from types_aiobotocore_pricing.client import PricingClient
from types_aiobotocore_proton.client import ProtonClient
from types_aiobotocore_qldb.client import QLDBClient
from types_aiobotocore_qldb_session.client import QLDBSessionClient
from types_aiobotocore_quicksight.client import QuickSightClient
from types_aiobotocore_ram.client import RAMClient
from types_aiobotocore_rbin.client import RecycleBinClient
from types_aiobotocore_rds.client import RDSClient
from types_aiobotocore_rds_data.client import RDSDataServiceClient
from types_aiobotocore_redshift.client import RedshiftClient
from types_aiobotocore_redshift_data.client import RedshiftDataAPIServiceClient
from types_aiobotocore_rekognition.client import RekognitionClient
from types_aiobotocore_resiliencehub.client import ResilienceHubClient
from types_aiobotocore_resource_groups.client import ResourceGroupsClient
from types_aiobotocore_resourcegroupstaggingapi.client import ResourceGroupsTaggingAPIClient
from types_aiobotocore_robomaker.client import RoboMakerClient
from types_aiobotocore_route53.client import Route53Client
from types_aiobotocore_route53_recovery_cluster.client import Route53RecoveryClusterClient
from types_aiobotocore_route53_recovery_control_config.client import (
    Route53RecoveryControlConfigClient,
)
from types_aiobotocore_route53_recovery_readiness.client import Route53RecoveryReadinessClient
from types_aiobotocore_route53domains.client import Route53DomainsClient
from types_aiobotocore_route53resolver.client import Route53ResolverClient
from types_aiobotocore_rum.client import CloudWatchRUMClient
from types_aiobotocore_s3.client import S3Client
from types_aiobotocore_s3control.client import S3ControlClient
from types_aiobotocore_s3outposts.client import S3OutpostsClient
from types_aiobotocore_sagemaker.client import SageMakerClient
from types_aiobotocore_sagemaker_a2i_runtime.client import AugmentedAIRuntimeClient
from types_aiobotocore_sagemaker_edge.client import SagemakerEdgeManagerClient
from types_aiobotocore_sagemaker_featurestore_runtime.client import (
    SageMakerFeatureStoreRuntimeClient,
)
from types_aiobotocore_sagemaker_runtime.client import SageMakerRuntimeClient
from types_aiobotocore_savingsplans.client import SavingsPlansClient
from types_aiobotocore_schemas.client import SchemasClient
from types_aiobotocore_sdb.client import SimpleDBClient
from types_aiobotocore_secretsmanager.client import SecretsManagerClient
from types_aiobotocore_securityhub.client import SecurityHubClient
from types_aiobotocore_serverlessrepo.client import ServerlessApplicationRepositoryClient
from types_aiobotocore_service_quotas.client import ServiceQuotasClient
from types_aiobotocore_servicecatalog.client import ServiceCatalogClient
from types_aiobotocore_servicecatalog_appregistry.client import AppRegistryClient
from types_aiobotocore_servicediscovery.client import ServiceDiscoveryClient
from types_aiobotocore_ses.client import SESClient
from types_aiobotocore_sesv2.client import SESV2Client
from types_aiobotocore_shield.client import ShieldClient
from types_aiobotocore_signer.client import signerClient
from types_aiobotocore_sms.client import SMSClient
from types_aiobotocore_snow_device_management.client import SnowDeviceManagementClient
from types_aiobotocore_snowball.client import SnowballClient
from types_aiobotocore_sns.client import SNSClient
from types_aiobotocore_sqs.client import SQSClient
from types_aiobotocore_ssm.client import SSMClient
from types_aiobotocore_ssm_contacts.client import SSMContactsClient
from types_aiobotocore_ssm_incidents.client import SSMIncidentsClient
from types_aiobotocore_sso.client import SSOClient
from types_aiobotocore_sso_admin.client import SSOAdminClient
from types_aiobotocore_sso_oidc.client import SSOOIDCClient
from types_aiobotocore_stepfunctions.client import SFNClient
from types_aiobotocore_storagegateway.client import StorageGatewayClient
from types_aiobotocore_sts.client import STSClient
from types_aiobotocore_support.client import SupportClient
from types_aiobotocore_swf.client import SWFClient
from types_aiobotocore_synthetics.client import SyntheticsClient
from types_aiobotocore_textract.client import TextractClient
from types_aiobotocore_timestream_query.client import TimestreamQueryClient
from types_aiobotocore_timestream_write.client import TimestreamWriteClient
from types_aiobotocore_transcribe.client import TranscribeServiceClient
from types_aiobotocore_transfer.client import TransferClient
from types_aiobotocore_translate.client import TranslateClient
from types_aiobotocore_voice_id.client import VoiceIDClient
from types_aiobotocore_waf.client import WAFClient
from types_aiobotocore_waf_regional.client import WAFRegionalClient
from types_aiobotocore_wafv2.client import WAFV2Client
from types_aiobotocore_wellarchitected.client import WellArchitectedClient
from types_aiobotocore_wisdom.client import ConnectWisdomServiceClient
from types_aiobotocore_workdocs.client import WorkDocsClient
from types_aiobotocore_worklink.client import WorkLinkClient
from types_aiobotocore_workmail.client import WorkMailClient
from types_aiobotocore_workmailmessageflow.client import WorkMailMessageFlowClient
from types_aiobotocore_workspaces.client import WorkSpacesClient
from types_aiobotocore_workspaces_web.client import WorkSpacesWebClient
from types_aiobotocore_xray.client import XRayClient

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal

class ClientCreatorContext:
    def __init__(self, coro: Any) -> None: ...
    async def __aenter__(self) -> AioBaseClient: ...
    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None: ...

class AioSession(Session):
    def __init__(
        self,
        session_vars: Optional[Any] = ...,
        event_hooks: Optional[Any] = ...,
        include_builtin_handlers: bool = ...,
        profile: Optional[Any] = ...,
    ) -> None: ...
    def register(
        self,
        event_name: str,
        handler: Any,
        unique_id: Optional[Any] = ...,
        unique_id_uses_count: bool = ...,
    ) -> None: ...
    async def get_credentials(self) -> AioCredentials: ...
    def set_credentials(
        self, access_key: str, secret_key: str, token: Optional[Any] = ...
    ) -> None: ...
    async def get_service_model(
        self, service_name: str, api_version: Optional[Any] = ...
    ) -> ServiceModel: ...
    async def get_service_data(
        self, service_name: str, api_version: Optional[Any] = ...
    ) -> Any: ...
    async def get_available_regions(
        self, service_name: str, partition_name: str = ..., allow_non_regional: bool = ...
    ) -> List[str]: ...
    @overload
    def create_client(
        self,
        service_name: Literal["accessanalyzer"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> AccessAnalyzerClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["account"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> AccountClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["acm"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> ACMClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["acm-pca"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> ACMPCAClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["alexaforbusiness"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> AlexaForBusinessClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["amp"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> PrometheusServiceClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["amplify"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> AmplifyClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["amplifybackend"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> AmplifyBackendClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["amplifyuibuilder"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> AmplifyUIBuilderClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["apigateway"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> APIGatewayClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["apigatewaymanagementapi"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> ApiGatewayManagementApiClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["apigatewayv2"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> ApiGatewayV2Client: ...
    @overload
    def create_client(
        self,
        service_name: Literal["appconfig"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> AppConfigClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["appconfigdata"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> AppConfigDataClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["appflow"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> AppflowClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["appintegrations"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> AppIntegrationsServiceClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["application-autoscaling"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> ApplicationAutoScalingClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["application-insights"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> ApplicationInsightsClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["applicationcostprofiler"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> ApplicationCostProfilerClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["appmesh"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> AppMeshClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["apprunner"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> AppRunnerClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["appstream"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> AppStreamClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["appsync"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> AppSyncClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["athena"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> AthenaClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["auditmanager"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> AuditManagerClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["autoscaling"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> AutoScalingClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["autoscaling-plans"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> AutoScalingPlansClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["backup"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> BackupClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["backup-gateway"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> BackupGatewayClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["batch"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> BatchClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["billingconductor"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> BillingConductorClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["braket"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> BraketClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["budgets"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> BudgetsClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["ce"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> CostExplorerClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["chime"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> ChimeClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["chime-sdk-identity"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> ChimeSDKIdentityClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["chime-sdk-meetings"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> ChimeSDKMeetingsClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["chime-sdk-messaging"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> ChimeSDKMessagingClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["cloud9"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> Cloud9Client: ...
    @overload
    def create_client(
        self,
        service_name: Literal["cloudcontrol"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> CloudControlApiClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["clouddirectory"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> CloudDirectoryClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["cloudformation"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> CloudFormationClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["cloudfront"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> CloudFrontClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["cloudhsm"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> CloudHSMClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["cloudhsmv2"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> CloudHSMV2Client: ...
    @overload
    def create_client(
        self,
        service_name: Literal["cloudsearch"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> CloudSearchClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["cloudsearchdomain"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> CloudSearchDomainClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["cloudtrail"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> CloudTrailClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["cloudwatch"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> CloudWatchClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["codeartifact"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> CodeArtifactClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["codebuild"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> CodeBuildClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["codecommit"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> CodeCommitClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["codedeploy"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> CodeDeployClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["codeguru-reviewer"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> CodeGuruReviewerClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["codeguruprofiler"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> CodeGuruProfilerClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["codepipeline"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> CodePipelineClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["codestar"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> CodeStarClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["codestar-connections"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> CodeStarconnectionsClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["codestar-notifications"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> CodeStarNotificationsClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["cognito-identity"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> CognitoIdentityClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["cognito-idp"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> CognitoIdentityProviderClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["cognito-sync"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> CognitoSyncClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["comprehend"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> ComprehendClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["comprehendmedical"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> ComprehendMedicalClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["compute-optimizer"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> ComputeOptimizerClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["config"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> ConfigServiceClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["connect"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> ConnectClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["connect-contact-lens"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> ConnectContactLensClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["connectparticipant"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> ConnectParticipantClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["cur"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> CostandUsageReportServiceClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["customer-profiles"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> CustomerProfilesClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["databrew"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> GlueDataBrewClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["dataexchange"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> DataExchangeClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["datapipeline"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> DataPipelineClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["datasync"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> DataSyncClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["dax"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> DAXClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["detective"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> DetectiveClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["devicefarm"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> DeviceFarmClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["devops-guru"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> DevOpsGuruClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["directconnect"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> DirectConnectClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["discovery"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> ApplicationDiscoveryServiceClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["dlm"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> DLMClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["dms"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> DatabaseMigrationServiceClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["docdb"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> DocDBClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["drs"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> drsClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["ds"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> DirectoryServiceClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["dynamodb"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> DynamoDBClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["dynamodbstreams"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> DynamoDBStreamsClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["ebs"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> EBSClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["ec2"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> EC2Client: ...
    @overload
    def create_client(
        self,
        service_name: Literal["ec2-instance-connect"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> EC2InstanceConnectClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["ecr"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> ECRClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["ecr-public"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> ECRPublicClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["ecs"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> ECSClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["efs"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> EFSClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["eks"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> EKSClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["elastic-inference"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> ElasticInferenceClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["elasticache"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> ElastiCacheClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["elasticbeanstalk"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> ElasticBeanstalkClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["elastictranscoder"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> ElasticTranscoderClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["elb"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> ElasticLoadBalancingClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["elbv2"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> ElasticLoadBalancingv2Client: ...
    @overload
    def create_client(
        self,
        service_name: Literal["emr"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> EMRClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["emr-containers"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> EMRContainersClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["es"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> ElasticsearchServiceClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["events"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> EventBridgeClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["evidently"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> CloudWatchEvidentlyClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["finspace"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> finspaceClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["finspace-data"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> FinSpaceDataClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["firehose"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> FirehoseClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["fis"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> FISClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["fms"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> FMSClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["forecast"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> ForecastServiceClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["forecastquery"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> ForecastQueryServiceClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["frauddetector"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> FraudDetectorClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["fsx"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> FSxClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["gamelift"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> GameLiftClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["glacier"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> GlacierClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["globalaccelerator"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> GlobalAcceleratorClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["glue"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> GlueClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["grafana"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> ManagedGrafanaClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["greengrass"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> GreengrassClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["greengrassv2"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> GreengrassV2Client: ...
    @overload
    def create_client(
        self,
        service_name: Literal["groundstation"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> GroundStationClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["guardduty"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> GuardDutyClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["health"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> HealthClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["healthlake"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> HealthLakeClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["honeycode"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> HoneycodeClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["iam"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> IAMClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["identitystore"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> IdentityStoreClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["imagebuilder"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> imagebuilderClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["importexport"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> ImportExportClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["inspector"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> InspectorClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["inspector2"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> Inspector2Client: ...
    @overload
    def create_client(
        self,
        service_name: Literal["iot"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> IoTClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["iot-data"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> IoTDataPlaneClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["iot-jobs-data"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> IoTJobsDataPlaneClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["iot1click-devices"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> IoT1ClickDevicesServiceClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["iot1click-projects"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> IoT1ClickProjectsClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["iotanalytics"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> IoTAnalyticsClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["iotdeviceadvisor"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> IoTDeviceAdvisorClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["iotevents"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> IoTEventsClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["iotevents-data"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> IoTEventsDataClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["iotfleethub"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> IoTFleetHubClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["iotsecuretunneling"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> IoTSecureTunnelingClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["iotsitewise"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> IoTSiteWiseClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["iotthingsgraph"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> IoTThingsGraphClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["iottwinmaker"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> IoTTwinMakerClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["iotwireless"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> IoTWirelessClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["ivs"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> IVSClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["kafka"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> KafkaClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["kafkaconnect"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> KafkaConnectClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["kendra"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> kendraClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["keyspaces"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> KeyspacesClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["kinesis"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> KinesisClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["kinesis-video-archived-media"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> KinesisVideoArchivedMediaClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["kinesis-video-media"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> KinesisVideoMediaClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["kinesis-video-signaling"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> KinesisVideoSignalingChannelsClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["kinesisanalytics"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> KinesisAnalyticsClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["kinesisanalyticsv2"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> KinesisAnalyticsV2Client: ...
    @overload
    def create_client(
        self,
        service_name: Literal["kinesisvideo"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> KinesisVideoClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["kms"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> KMSClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["lakeformation"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> LakeFormationClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["lambda"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> LambdaClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["lex-models"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> LexModelBuildingServiceClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["lex-runtime"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> LexRuntimeServiceClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["lexv2-models"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> LexModelsV2Client: ...
    @overload
    def create_client(
        self,
        service_name: Literal["lexv2-runtime"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> LexRuntimeV2Client: ...
    @overload
    def create_client(
        self,
        service_name: Literal["license-manager"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> LicenseManagerClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["lightsail"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> LightsailClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["location"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> LocationServiceClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["logs"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> CloudWatchLogsClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["lookoutequipment"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> LookoutEquipmentClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["lookoutmetrics"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> LookoutMetricsClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["lookoutvision"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> LookoutforVisionClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["machinelearning"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> MachineLearningClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["macie"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> MacieClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["macie2"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> Macie2Client: ...
    @overload
    def create_client(
        self,
        service_name: Literal["managedblockchain"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> ManagedBlockchainClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["marketplace-catalog"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> MarketplaceCatalogClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["marketplace-entitlement"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> MarketplaceEntitlementServiceClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["marketplacecommerceanalytics"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> MarketplaceCommerceAnalyticsClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["mediaconnect"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> MediaConnectClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["mediaconvert"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> MediaConvertClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["medialive"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> MediaLiveClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["mediapackage"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> MediaPackageClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["mediapackage-vod"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> MediaPackageVodClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["mediastore"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> MediaStoreClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["mediastore-data"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> MediaStoreDataClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["mediatailor"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> MediaTailorClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["memorydb"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> MemoryDBClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["meteringmarketplace"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> MarketplaceMeteringClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["mgh"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> MigrationHubClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["mgn"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> mgnClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["migration-hub-refactor-spaces"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> MigrationHubRefactorSpacesClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["migrationhub-config"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> MigrationHubConfigClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["migrationhubstrategy"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> MigrationHubStrategyRecommendationsClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["mobile"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> MobileClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["mq"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> MQClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["mturk"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> MTurkClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["mwaa"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> MWAAClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["neptune"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> NeptuneClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["network-firewall"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> NetworkFirewallClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["networkmanager"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> NetworkManagerClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["nimble"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> NimbleStudioClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["opensearch"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> OpenSearchServiceClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["opsworks"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> OpsWorksClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["opsworkscm"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> OpsWorksCMClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["organizations"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> OrganizationsClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["outposts"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> OutpostsClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["panorama"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> PanoramaClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["personalize"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> PersonalizeClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["personalize-events"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> PersonalizeEventsClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["personalize-runtime"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> PersonalizeRuntimeClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["pi"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> PIClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["pinpoint"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> PinpointClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["pinpoint-email"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> PinpointEmailClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["pinpoint-sms-voice"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> PinpointSMSVoiceClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["polly"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> PollyClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["pricing"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> PricingClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["proton"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> ProtonClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["qldb"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> QLDBClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["qldb-session"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> QLDBSessionClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["quicksight"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> QuickSightClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["ram"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> RAMClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["rbin"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> RecycleBinClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["rds"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> RDSClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["rds-data"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> RDSDataServiceClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["redshift"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> RedshiftClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["redshift-data"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> RedshiftDataAPIServiceClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["rekognition"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> RekognitionClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["resiliencehub"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> ResilienceHubClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["resource-groups"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> ResourceGroupsClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["resourcegroupstaggingapi"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> ResourceGroupsTaggingAPIClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["robomaker"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> RoboMakerClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["route53"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> Route53Client: ...
    @overload
    def create_client(
        self,
        service_name: Literal["route53-recovery-cluster"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> Route53RecoveryClusterClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["route53-recovery-control-config"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> Route53RecoveryControlConfigClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["route53-recovery-readiness"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> Route53RecoveryReadinessClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["route53domains"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> Route53DomainsClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["route53resolver"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> Route53ResolverClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["rum"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> CloudWatchRUMClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["s3"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> S3Client: ...
    @overload
    def create_client(
        self,
        service_name: Literal["s3control"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> S3ControlClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["s3outposts"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> S3OutpostsClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["sagemaker"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> SageMakerClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["sagemaker-a2i-runtime"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> AugmentedAIRuntimeClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["sagemaker-edge"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> SagemakerEdgeManagerClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["sagemaker-featurestore-runtime"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> SageMakerFeatureStoreRuntimeClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["sagemaker-runtime"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> SageMakerRuntimeClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["savingsplans"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> SavingsPlansClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["schemas"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> SchemasClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["sdb"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> SimpleDBClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["secretsmanager"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> SecretsManagerClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["securityhub"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> SecurityHubClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["serverlessrepo"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> ServerlessApplicationRepositoryClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["service-quotas"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> ServiceQuotasClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["servicecatalog"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> ServiceCatalogClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["servicecatalog-appregistry"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> AppRegistryClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["servicediscovery"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> ServiceDiscoveryClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["ses"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> SESClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["sesv2"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> SESV2Client: ...
    @overload
    def create_client(
        self,
        service_name: Literal["shield"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> ShieldClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["signer"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> signerClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["sms"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> SMSClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["sms-voice"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> PinpointSMSVoiceClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["snow-device-management"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> SnowDeviceManagementClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["snowball"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> SnowballClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["sns"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> SNSClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["sqs"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> SQSClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["ssm"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> SSMClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["ssm-contacts"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> SSMContactsClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["ssm-incidents"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> SSMIncidentsClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["sso"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> SSOClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["sso-admin"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> SSOAdminClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["sso-oidc"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> SSOOIDCClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["stepfunctions"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> SFNClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["storagegateway"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> StorageGatewayClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["sts"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> STSClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["support"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> SupportClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["swf"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> SWFClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["synthetics"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> SyntheticsClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["textract"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> TextractClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["timestream-query"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> TimestreamQueryClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["timestream-write"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> TimestreamWriteClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["transcribe"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> TranscribeServiceClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["transfer"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> TransferClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["translate"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> TranslateClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["voice-id"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> VoiceIDClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["waf"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> WAFClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["waf-regional"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> WAFRegionalClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["wafv2"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> WAFV2Client: ...
    @overload
    def create_client(
        self,
        service_name: Literal["wellarchitected"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> WellArchitectedClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["wisdom"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> ConnectWisdomServiceClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["workdocs"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> WorkDocsClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["worklink"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> WorkLinkClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["workmail"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> WorkMailClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["workmailmessageflow"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> WorkMailMessageFlowClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["workspaces"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> WorkSpacesClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["workspaces-web"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> WorkSpacesWebClient: ...
    @overload
    def create_client(
        self,
        service_name: Literal["xray"],
        region_name: Optional[str] = ...,
        api_version: Optional[str] = ...,
        use_ssl: Optional[bool] = ...,
        verify: Union[bool, str, None] = ...,
        endpoint_url: Optional[str] = ...,
        aws_access_key_id: Optional[str] = ...,
        aws_secret_access_key: Optional[str] = ...,
        aws_session_token: Optional[str] = ...,
        config: Optional[Config] = ...,
    ) -> XRayClient: ...

def get_session(env_vars: Optional[Any] = ...) -> AioSession: ...
