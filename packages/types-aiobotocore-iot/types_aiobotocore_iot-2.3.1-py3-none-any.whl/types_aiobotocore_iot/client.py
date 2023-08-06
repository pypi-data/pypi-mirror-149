"""
Type annotations for iot service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_iot.client import IoTClient

    session = get_session()
    async with session.create_client("iot") as client:
        client: IoTClient
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, Mapping, Sequence, Type, Union, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import (
    AuditFrequencyType,
    AuditMitigationActionsExecutionStatusType,
    AuditMitigationActionsTaskStatusType,
    AuditTaskStatusType,
    AuditTaskTypeType,
    AuthorizerStatusType,
    AutoRegistrationStatusType,
    BehaviorCriteriaTypeType,
    CACertificateStatusType,
    CertificateStatusType,
    CustomMetricTypeType,
    DayOfWeekType,
    DomainConfigurationStatusType,
    EventTypeType,
    FleetMetricUnitType,
    JobExecutionStatusType,
    JobStatusType,
    LogLevelType,
    LogTargetTypeType,
    MitigationActionTypeType,
    OTAUpdateStatusType,
    ProtocolType,
    ReportTypeType,
    ServiceTypeType,
    StatusType,
    TargetSelectionType,
    TopicRuleDestinationStatusType,
    VerificationStateType,
)
from .paginator import (
    GetBehaviorModelTrainingSummariesPaginator,
    ListActiveViolationsPaginator,
    ListAttachedPoliciesPaginator,
    ListAuditFindingsPaginator,
    ListAuditMitigationActionsExecutionsPaginator,
    ListAuditMitigationActionsTasksPaginator,
    ListAuditSuppressionsPaginator,
    ListAuditTasksPaginator,
    ListAuthorizersPaginator,
    ListBillingGroupsPaginator,
    ListCACertificatesPaginator,
    ListCertificatesByCAPaginator,
    ListCertificatesPaginator,
    ListCustomMetricsPaginator,
    ListDetectMitigationActionsExecutionsPaginator,
    ListDetectMitigationActionsTasksPaginator,
    ListDimensionsPaginator,
    ListDomainConfigurationsPaginator,
    ListFleetMetricsPaginator,
    ListIndicesPaginator,
    ListJobExecutionsForJobPaginator,
    ListJobExecutionsForThingPaginator,
    ListJobsPaginator,
    ListJobTemplatesPaginator,
    ListMitigationActionsPaginator,
    ListOTAUpdatesPaginator,
    ListOutgoingCertificatesPaginator,
    ListPoliciesPaginator,
    ListPolicyPrincipalsPaginator,
    ListPrincipalPoliciesPaginator,
    ListPrincipalThingsPaginator,
    ListProvisioningTemplatesPaginator,
    ListProvisioningTemplateVersionsPaginator,
    ListRoleAliasesPaginator,
    ListScheduledAuditsPaginator,
    ListSecurityProfilesForTargetPaginator,
    ListSecurityProfilesPaginator,
    ListStreamsPaginator,
    ListTagsForResourcePaginator,
    ListTargetsForPolicyPaginator,
    ListTargetsForSecurityProfilePaginator,
    ListThingGroupsForThingPaginator,
    ListThingGroupsPaginator,
    ListThingPrincipalsPaginator,
    ListThingRegistrationTaskReportsPaginator,
    ListThingRegistrationTasksPaginator,
    ListThingsInBillingGroupPaginator,
    ListThingsInThingGroupPaginator,
    ListThingsPaginator,
    ListThingTypesPaginator,
    ListTopicRuleDestinationsPaginator,
    ListTopicRulesPaginator,
    ListV2LoggingLevelsPaginator,
    ListViolationEventsPaginator,
)
from .type_defs import (
    AbortConfigTypeDef,
    AggregationTypeTypeDef,
    AlertTargetTypeDef,
    AssociateTargetsWithJobResponseTypeDef,
    AttributePayloadTypeDef,
    AuditCheckConfigurationTypeDef,
    AuditMitigationActionsTaskTargetTypeDef,
    AuditNotificationTargetTypeDef,
    AuthInfoTypeDef,
    AuthorizerConfigTypeDef,
    AwsJobAbortConfigTypeDef,
    AwsJobExecutionsRolloutConfigTypeDef,
    AwsJobPresignedUrlConfigTypeDef,
    AwsJobTimeoutConfigTypeDef,
    BehaviorTypeDef,
    BillingGroupPropertiesTypeDef,
    BucketsAggregationTypeTypeDef,
    CancelJobResponseTypeDef,
    ConfigurationTypeDef,
    CreateAuthorizerResponseTypeDef,
    CreateBillingGroupResponseTypeDef,
    CreateCertificateFromCsrResponseTypeDef,
    CreateCustomMetricResponseTypeDef,
    CreateDimensionResponseTypeDef,
    CreateDomainConfigurationResponseTypeDef,
    CreateDynamicThingGroupResponseTypeDef,
    CreateFleetMetricResponseTypeDef,
    CreateJobResponseTypeDef,
    CreateJobTemplateResponseTypeDef,
    CreateKeysAndCertificateResponseTypeDef,
    CreateMitigationActionResponseTypeDef,
    CreateOTAUpdateResponseTypeDef,
    CreatePolicyResponseTypeDef,
    CreatePolicyVersionResponseTypeDef,
    CreateProvisioningClaimResponseTypeDef,
    CreateProvisioningTemplateResponseTypeDef,
    CreateProvisioningTemplateVersionResponseTypeDef,
    CreateRoleAliasResponseTypeDef,
    CreateScheduledAuditResponseTypeDef,
    CreateSecurityProfileResponseTypeDef,
    CreateStreamResponseTypeDef,
    CreateThingGroupResponseTypeDef,
    CreateThingResponseTypeDef,
    CreateThingTypeResponseTypeDef,
    CreateTopicRuleDestinationResponseTypeDef,
    DescribeAccountAuditConfigurationResponseTypeDef,
    DescribeAuditFindingResponseTypeDef,
    DescribeAuditMitigationActionsTaskResponseTypeDef,
    DescribeAuditSuppressionResponseTypeDef,
    DescribeAuditTaskResponseTypeDef,
    DescribeAuthorizerResponseTypeDef,
    DescribeBillingGroupResponseTypeDef,
    DescribeCACertificateResponseTypeDef,
    DescribeCertificateResponseTypeDef,
    DescribeCustomMetricResponseTypeDef,
    DescribeDefaultAuthorizerResponseTypeDef,
    DescribeDetectMitigationActionsTaskResponseTypeDef,
    DescribeDimensionResponseTypeDef,
    DescribeDomainConfigurationResponseTypeDef,
    DescribeEndpointResponseTypeDef,
    DescribeEventConfigurationsResponseTypeDef,
    DescribeFleetMetricResponseTypeDef,
    DescribeIndexResponseTypeDef,
    DescribeJobExecutionResponseTypeDef,
    DescribeJobResponseTypeDef,
    DescribeJobTemplateResponseTypeDef,
    DescribeManagedJobTemplateResponseTypeDef,
    DescribeMitigationActionResponseTypeDef,
    DescribeProvisioningTemplateResponseTypeDef,
    DescribeProvisioningTemplateVersionResponseTypeDef,
    DescribeRoleAliasResponseTypeDef,
    DescribeScheduledAuditResponseTypeDef,
    DescribeSecurityProfileResponseTypeDef,
    DescribeStreamResponseTypeDef,
    DescribeThingGroupResponseTypeDef,
    DescribeThingRegistrationTaskResponseTypeDef,
    DescribeThingResponseTypeDef,
    DescribeThingTypeResponseTypeDef,
    DetectMitigationActionsTaskTargetTypeDef,
    GetBehaviorModelTrainingSummariesResponseTypeDef,
    GetBucketsAggregationResponseTypeDef,
    GetCardinalityResponseTypeDef,
    GetEffectivePoliciesResponseTypeDef,
    GetIndexingConfigurationResponseTypeDef,
    GetJobDocumentResponseTypeDef,
    GetLoggingOptionsResponseTypeDef,
    GetOTAUpdateResponseTypeDef,
    GetPercentilesResponseTypeDef,
    GetPolicyResponseTypeDef,
    GetPolicyVersionResponseTypeDef,
    GetRegistrationCodeResponseTypeDef,
    GetStatisticsResponseTypeDef,
    GetTopicRuleDestinationResponseTypeDef,
    GetTopicRuleResponseTypeDef,
    GetV2LoggingOptionsResponseTypeDef,
    HttpContextTypeDef,
    JobExecutionsRetryConfigTypeDef,
    JobExecutionsRolloutConfigTypeDef,
    ListActiveViolationsResponseTypeDef,
    ListAttachedPoliciesResponseTypeDef,
    ListAuditFindingsResponseTypeDef,
    ListAuditMitigationActionsExecutionsResponseTypeDef,
    ListAuditMitigationActionsTasksResponseTypeDef,
    ListAuditSuppressionsResponseTypeDef,
    ListAuditTasksResponseTypeDef,
    ListAuthorizersResponseTypeDef,
    ListBillingGroupsResponseTypeDef,
    ListCACertificatesResponseTypeDef,
    ListCertificatesByCAResponseTypeDef,
    ListCertificatesResponseTypeDef,
    ListCustomMetricsResponseTypeDef,
    ListDetectMitigationActionsExecutionsResponseTypeDef,
    ListDetectMitigationActionsTasksResponseTypeDef,
    ListDimensionsResponseTypeDef,
    ListDomainConfigurationsResponseTypeDef,
    ListFleetMetricsResponseTypeDef,
    ListIndicesResponseTypeDef,
    ListJobExecutionsForJobResponseTypeDef,
    ListJobExecutionsForThingResponseTypeDef,
    ListJobsResponseTypeDef,
    ListJobTemplatesResponseTypeDef,
    ListManagedJobTemplatesResponseTypeDef,
    ListMitigationActionsResponseTypeDef,
    ListOTAUpdatesResponseTypeDef,
    ListOutgoingCertificatesResponseTypeDef,
    ListPoliciesResponseTypeDef,
    ListPolicyPrincipalsResponseTypeDef,
    ListPolicyVersionsResponseTypeDef,
    ListPrincipalPoliciesResponseTypeDef,
    ListPrincipalThingsResponseTypeDef,
    ListProvisioningTemplatesResponseTypeDef,
    ListProvisioningTemplateVersionsResponseTypeDef,
    ListRoleAliasesResponseTypeDef,
    ListScheduledAuditsResponseTypeDef,
    ListSecurityProfilesForTargetResponseTypeDef,
    ListSecurityProfilesResponseTypeDef,
    ListStreamsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTargetsForPolicyResponseTypeDef,
    ListTargetsForSecurityProfileResponseTypeDef,
    ListThingGroupsForThingResponseTypeDef,
    ListThingGroupsResponseTypeDef,
    ListThingPrincipalsResponseTypeDef,
    ListThingRegistrationTaskReportsResponseTypeDef,
    ListThingRegistrationTasksResponseTypeDef,
    ListThingsInBillingGroupResponseTypeDef,
    ListThingsInThingGroupResponseTypeDef,
    ListThingsResponseTypeDef,
    ListThingTypesResponseTypeDef,
    ListTopicRuleDestinationsResponseTypeDef,
    ListTopicRulesResponseTypeDef,
    ListV2LoggingLevelsResponseTypeDef,
    ListViolationEventsResponseTypeDef,
    LoggingOptionsPayloadTypeDef,
    LogTargetTypeDef,
    MetricToRetainTypeDef,
    MitigationActionParamsTypeDef,
    MqttContextTypeDef,
    OTAUpdateFileTypeDef,
    PresignedUrlConfigTypeDef,
    ProvisioningHookTypeDef,
    RegisterCACertificateResponseTypeDef,
    RegisterCertificateResponseTypeDef,
    RegisterCertificateWithoutCAResponseTypeDef,
    RegisterThingResponseTypeDef,
    RegistrationConfigTypeDef,
    ResourceIdentifierTypeDef,
    SearchIndexResponseTypeDef,
    SetDefaultAuthorizerResponseTypeDef,
    StartAuditMitigationActionsTaskResponseTypeDef,
    StartDetectMitigationActionsTaskResponseTypeDef,
    StartOnDemandAuditTaskResponseTypeDef,
    StartThingRegistrationTaskResponseTypeDef,
    StreamFileTypeDef,
    TagTypeDef,
    TestAuthorizationResponseTypeDef,
    TestInvokeAuthorizerResponseTypeDef,
    ThingGroupIndexingConfigurationTypeDef,
    ThingGroupPropertiesTypeDef,
    ThingIndexingConfigurationTypeDef,
    ThingTypePropertiesTypeDef,
    TimeoutConfigTypeDef,
    TlsContextTypeDef,
    TopicRuleDestinationConfigurationTypeDef,
    TopicRulePayloadTypeDef,
    TransferCertificateResponseTypeDef,
    UpdateAuthorizerResponseTypeDef,
    UpdateBillingGroupResponseTypeDef,
    UpdateCustomMetricResponseTypeDef,
    UpdateDimensionResponseTypeDef,
    UpdateDomainConfigurationResponseTypeDef,
    UpdateDynamicThingGroupResponseTypeDef,
    UpdateMitigationActionResponseTypeDef,
    UpdateRoleAliasResponseTypeDef,
    UpdateScheduledAuditResponseTypeDef,
    UpdateSecurityProfileResponseTypeDef,
    UpdateStreamResponseTypeDef,
    UpdateThingGroupResponseTypeDef,
    ValidateSecurityProfileBehaviorsResponseTypeDef,
    ViolationEventOccurrenceRangeTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("IoTClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    CertificateConflictException: Type[BotocoreClientError]
    CertificateStateException: Type[BotocoreClientError]
    CertificateValidationException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    ConflictingResourceUpdateException: Type[BotocoreClientError]
    DeleteConflictException: Type[BotocoreClientError]
    IndexNotReadyException: Type[BotocoreClientError]
    InternalException: Type[BotocoreClientError]
    InternalFailureException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    InvalidAggregationException: Type[BotocoreClientError]
    InvalidQueryException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    InvalidResponseException: Type[BotocoreClientError]
    InvalidStateTransitionException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    MalformedPolicyException: Type[BotocoreClientError]
    NotConfiguredException: Type[BotocoreClientError]
    RegistrationCodeValidationException: Type[BotocoreClientError]
    ResourceAlreadyExistsException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ResourceRegistrationFailureException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    SqlParseException: Type[BotocoreClientError]
    TaskAlreadyExistsException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    TransferAlreadyCompletedException: Type[BotocoreClientError]
    TransferConflictException: Type[BotocoreClientError]
    UnauthorizedException: Type[BotocoreClientError]
    VersionConflictException: Type[BotocoreClientError]
    VersionsLimitExceededException: Type[BotocoreClientError]


class IoTClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        IoTClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#exceptions)
        """

    async def accept_certificate_transfer(
        self, *, certificateId: str, setAsActive: bool = ...
    ) -> None:
        """
        Accepts a pending certificate transfer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.accept_certificate_transfer)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#accept_certificate_transfer)
        """

    async def add_thing_to_billing_group(
        self,
        *,
        billingGroupName: str = ...,
        billingGroupArn: str = ...,
        thingName: str = ...,
        thingArn: str = ...
    ) -> Dict[str, Any]:
        """
        Adds a thing to a billing group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.add_thing_to_billing_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#add_thing_to_billing_group)
        """

    async def add_thing_to_thing_group(
        self,
        *,
        thingGroupName: str = ...,
        thingGroupArn: str = ...,
        thingName: str = ...,
        thingArn: str = ...,
        overrideDynamicGroups: bool = ...
    ) -> Dict[str, Any]:
        """
        Adds a thing to a thing group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.add_thing_to_thing_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#add_thing_to_thing_group)
        """

    async def associate_targets_with_job(
        self, *, targets: Sequence[str], jobId: str, comment: str = ..., namespaceId: str = ...
    ) -> AssociateTargetsWithJobResponseTypeDef:
        """
        Associates a group with a continuous job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.associate_targets_with_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#associate_targets_with_job)
        """

    async def attach_policy(self, *, policyName: str, target: str) -> None:
        """
        Attaches the specified policy to the specified principal (certificate or other
        credential).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.attach_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#attach_policy)
        """

    async def attach_principal_policy(self, *, policyName: str, principal: str) -> None:
        """
        Attaches the specified policy to the specified principal (certificate or other
        credential).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.attach_principal_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#attach_principal_policy)
        """

    async def attach_security_profile(
        self, *, securityProfileName: str, securityProfileTargetArn: str
    ) -> Dict[str, Any]:
        """
        Associates a Device Defender security profile with a thing group or this
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.attach_security_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#attach_security_profile)
        """

    async def attach_thing_principal(self, *, thingName: str, principal: str) -> Dict[str, Any]:
        """
        Attaches the specified principal to the specified thing.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.attach_thing_principal)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#attach_thing_principal)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#can_paginate)
        """

    async def cancel_audit_mitigation_actions_task(self, *, taskId: str) -> Dict[str, Any]:
        """
        Cancels a mitigation action task that is in progress.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.cancel_audit_mitigation_actions_task)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#cancel_audit_mitigation_actions_task)
        """

    async def cancel_audit_task(self, *, taskId: str) -> Dict[str, Any]:
        """
        Cancels an audit that is in progress.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.cancel_audit_task)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#cancel_audit_task)
        """

    async def cancel_certificate_transfer(self, *, certificateId: str) -> None:
        """
        Cancels a pending transfer for the specified certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.cancel_certificate_transfer)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#cancel_certificate_transfer)
        """

    async def cancel_detect_mitigation_actions_task(self, *, taskId: str) -> Dict[str, Any]:
        """
        Cancels a Device Defender ML Detect mitigation action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.cancel_detect_mitigation_actions_task)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#cancel_detect_mitigation_actions_task)
        """

    async def cancel_job(
        self, *, jobId: str, reasonCode: str = ..., comment: str = ..., force: bool = ...
    ) -> CancelJobResponseTypeDef:
        """
        Cancels a job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.cancel_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#cancel_job)
        """

    async def cancel_job_execution(
        self,
        *,
        jobId: str,
        thingName: str,
        force: bool = ...,
        expectedVersion: int = ...,
        statusDetails: Mapping[str, str] = ...
    ) -> None:
        """
        Cancels the execution of a job for a given thing.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.cancel_job_execution)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#cancel_job_execution)
        """

    async def clear_default_authorizer(self) -> Dict[str, Any]:
        """
        Clears the default authorizer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.clear_default_authorizer)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#clear_default_authorizer)
        """

    async def confirm_topic_rule_destination(self, *, confirmationToken: str) -> Dict[str, Any]:
        """
        Confirms a topic rule destination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.confirm_topic_rule_destination)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#confirm_topic_rule_destination)
        """

    async def create_audit_suppression(
        self,
        *,
        checkName: str,
        resourceIdentifier: "ResourceIdentifierTypeDef",
        clientRequestToken: str,
        expirationDate: Union[datetime, str] = ...,
        suppressIndefinitely: bool = ...,
        description: str = ...
    ) -> Dict[str, Any]:
        """
        Creates a Device Defender audit suppression.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.create_audit_suppression)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#create_audit_suppression)
        """

    async def create_authorizer(
        self,
        *,
        authorizerName: str,
        authorizerFunctionArn: str,
        tokenKeyName: str = ...,
        tokenSigningPublicKeys: Mapping[str, str] = ...,
        status: AuthorizerStatusType = ...,
        tags: Sequence["TagTypeDef"] = ...,
        signingDisabled: bool = ...,
        enableCachingForHttp: bool = ...
    ) -> CreateAuthorizerResponseTypeDef:
        """
        Creates an authorizer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.create_authorizer)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#create_authorizer)
        """

    async def create_billing_group(
        self,
        *,
        billingGroupName: str,
        billingGroupProperties: "BillingGroupPropertiesTypeDef" = ...,
        tags: Sequence["TagTypeDef"] = ...
    ) -> CreateBillingGroupResponseTypeDef:
        """
        Creates a billing group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.create_billing_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#create_billing_group)
        """

    async def create_certificate_from_csr(
        self, *, certificateSigningRequest: str, setAsActive: bool = ...
    ) -> CreateCertificateFromCsrResponseTypeDef:
        """
        Creates an X.509 certificate using the specified certificate signing request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.create_certificate_from_csr)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#create_certificate_from_csr)
        """

    async def create_custom_metric(
        self,
        *,
        metricName: str,
        metricType: CustomMetricTypeType,
        clientRequestToken: str,
        displayName: str = ...,
        tags: Sequence["TagTypeDef"] = ...
    ) -> CreateCustomMetricResponseTypeDef:
        """
        Use this API to define a Custom Metric published by your devices to Device
        Defender.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.create_custom_metric)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#create_custom_metric)
        """

    async def create_dimension(
        self,
        *,
        name: str,
        type: Literal["TOPIC_FILTER"],
        stringValues: Sequence[str],
        clientRequestToken: str,
        tags: Sequence["TagTypeDef"] = ...
    ) -> CreateDimensionResponseTypeDef:
        """
        Create a dimension that you can use to limit the scope of a metric used in a
        security profile for IoT Device Defender.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.create_dimension)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#create_dimension)
        """

    async def create_domain_configuration(
        self,
        *,
        domainConfigurationName: str,
        domainName: str = ...,
        serverCertificateArns: Sequence[str] = ...,
        validationCertificateArn: str = ...,
        authorizerConfig: "AuthorizerConfigTypeDef" = ...,
        serviceType: ServiceTypeType = ...,
        tags: Sequence["TagTypeDef"] = ...
    ) -> CreateDomainConfigurationResponseTypeDef:
        """
        Creates a domain configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.create_domain_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#create_domain_configuration)
        """

    async def create_dynamic_thing_group(
        self,
        *,
        thingGroupName: str,
        queryString: str,
        thingGroupProperties: "ThingGroupPropertiesTypeDef" = ...,
        indexName: str = ...,
        queryVersion: str = ...,
        tags: Sequence["TagTypeDef"] = ...
    ) -> CreateDynamicThingGroupResponseTypeDef:
        """
        Creates a dynamic thing group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.create_dynamic_thing_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#create_dynamic_thing_group)
        """

    async def create_fleet_metric(
        self,
        *,
        metricName: str,
        queryString: str,
        aggregationType: "AggregationTypeTypeDef",
        period: int,
        aggregationField: str,
        description: str = ...,
        queryVersion: str = ...,
        indexName: str = ...,
        unit: FleetMetricUnitType = ...,
        tags: Sequence["TagTypeDef"] = ...
    ) -> CreateFleetMetricResponseTypeDef:
        """
        Creates a fleet metric.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.create_fleet_metric)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#create_fleet_metric)
        """

    async def create_job(
        self,
        *,
        jobId: str,
        targets: Sequence[str],
        documentSource: str = ...,
        document: str = ...,
        description: str = ...,
        presignedUrlConfig: "PresignedUrlConfigTypeDef" = ...,
        targetSelection: TargetSelectionType = ...,
        jobExecutionsRolloutConfig: "JobExecutionsRolloutConfigTypeDef" = ...,
        abortConfig: "AbortConfigTypeDef" = ...,
        timeoutConfig: "TimeoutConfigTypeDef" = ...,
        tags: Sequence["TagTypeDef"] = ...,
        namespaceId: str = ...,
        jobTemplateArn: str = ...,
        jobExecutionsRetryConfig: "JobExecutionsRetryConfigTypeDef" = ...,
        documentParameters: Mapping[str, str] = ...
    ) -> CreateJobResponseTypeDef:
        """
        Creates a job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.create_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#create_job)
        """

    async def create_job_template(
        self,
        *,
        jobTemplateId: str,
        description: str,
        jobArn: str = ...,
        documentSource: str = ...,
        document: str = ...,
        presignedUrlConfig: "PresignedUrlConfigTypeDef" = ...,
        jobExecutionsRolloutConfig: "JobExecutionsRolloutConfigTypeDef" = ...,
        abortConfig: "AbortConfigTypeDef" = ...,
        timeoutConfig: "TimeoutConfigTypeDef" = ...,
        tags: Sequence["TagTypeDef"] = ...,
        jobExecutionsRetryConfig: "JobExecutionsRetryConfigTypeDef" = ...
    ) -> CreateJobTemplateResponseTypeDef:
        """
        Creates a job template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.create_job_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#create_job_template)
        """

    async def create_keys_and_certificate(
        self, *, setAsActive: bool = ...
    ) -> CreateKeysAndCertificateResponseTypeDef:
        """
        Creates a 2048-bit RSA key pair and issues an X.509 certificate using the issued
        public key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.create_keys_and_certificate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#create_keys_and_certificate)
        """

    async def create_mitigation_action(
        self,
        *,
        actionName: str,
        roleArn: str,
        actionParams: "MitigationActionParamsTypeDef",
        tags: Sequence["TagTypeDef"] = ...
    ) -> CreateMitigationActionResponseTypeDef:
        """
        Defines an action that can be applied to audit findings by using
        StartAuditMitigationActionsTask.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.create_mitigation_action)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#create_mitigation_action)
        """

    async def create_ota_update(
        self,
        *,
        otaUpdateId: str,
        targets: Sequence[str],
        files: Sequence["OTAUpdateFileTypeDef"],
        roleArn: str,
        description: str = ...,
        protocols: Sequence[ProtocolType] = ...,
        targetSelection: TargetSelectionType = ...,
        awsJobExecutionsRolloutConfig: "AwsJobExecutionsRolloutConfigTypeDef" = ...,
        awsJobPresignedUrlConfig: "AwsJobPresignedUrlConfigTypeDef" = ...,
        awsJobAbortConfig: "AwsJobAbortConfigTypeDef" = ...,
        awsJobTimeoutConfig: "AwsJobTimeoutConfigTypeDef" = ...,
        additionalParameters: Mapping[str, str] = ...,
        tags: Sequence["TagTypeDef"] = ...
    ) -> CreateOTAUpdateResponseTypeDef:
        """
        Creates an IoT OTA update on a target group of things or groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.create_ota_update)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#create_ota_update)
        """

    async def create_policy(
        self, *, policyName: str, policyDocument: str, tags: Sequence["TagTypeDef"] = ...
    ) -> CreatePolicyResponseTypeDef:
        """
        Creates an IoT policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.create_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#create_policy)
        """

    async def create_policy_version(
        self, *, policyName: str, policyDocument: str, setAsDefault: bool = ...
    ) -> CreatePolicyVersionResponseTypeDef:
        """
        Creates a new version of the specified IoT policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.create_policy_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#create_policy_version)
        """

    async def create_provisioning_claim(
        self, *, templateName: str
    ) -> CreateProvisioningClaimResponseTypeDef:
        """
        Creates a provisioning claim.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.create_provisioning_claim)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#create_provisioning_claim)
        """

    async def create_provisioning_template(
        self,
        *,
        templateName: str,
        templateBody: str,
        provisioningRoleArn: str,
        description: str = ...,
        enabled: bool = ...,
        preProvisioningHook: "ProvisioningHookTypeDef" = ...,
        tags: Sequence["TagTypeDef"] = ...
    ) -> CreateProvisioningTemplateResponseTypeDef:
        """
        Creates a fleet provisioning template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.create_provisioning_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#create_provisioning_template)
        """

    async def create_provisioning_template_version(
        self, *, templateName: str, templateBody: str, setAsDefault: bool = ...
    ) -> CreateProvisioningTemplateVersionResponseTypeDef:
        """
        Creates a new version of a fleet provisioning template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.create_provisioning_template_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#create_provisioning_template_version)
        """

    async def create_role_alias(
        self,
        *,
        roleAlias: str,
        roleArn: str,
        credentialDurationSeconds: int = ...,
        tags: Sequence["TagTypeDef"] = ...
    ) -> CreateRoleAliasResponseTypeDef:
        """
        Creates a role alias.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.create_role_alias)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#create_role_alias)
        """

    async def create_scheduled_audit(
        self,
        *,
        frequency: AuditFrequencyType,
        targetCheckNames: Sequence[str],
        scheduledAuditName: str,
        dayOfMonth: str = ...,
        dayOfWeek: DayOfWeekType = ...,
        tags: Sequence["TagTypeDef"] = ...
    ) -> CreateScheduledAuditResponseTypeDef:
        """
        Creates a scheduled audit that is run at a specified time interval.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.create_scheduled_audit)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#create_scheduled_audit)
        """

    async def create_security_profile(
        self,
        *,
        securityProfileName: str,
        securityProfileDescription: str = ...,
        behaviors: Sequence["BehaviorTypeDef"] = ...,
        alertTargets: Mapping[Literal["SNS"], "AlertTargetTypeDef"] = ...,
        additionalMetricsToRetain: Sequence[str] = ...,
        additionalMetricsToRetainV2: Sequence["MetricToRetainTypeDef"] = ...,
        tags: Sequence["TagTypeDef"] = ...
    ) -> CreateSecurityProfileResponseTypeDef:
        """
        Creates a Device Defender security profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.create_security_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#create_security_profile)
        """

    async def create_stream(
        self,
        *,
        streamId: str,
        files: Sequence["StreamFileTypeDef"],
        roleArn: str,
        description: str = ...,
        tags: Sequence["TagTypeDef"] = ...
    ) -> CreateStreamResponseTypeDef:
        """
        Creates a stream for delivering one or more large files in chunks over MQTT.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.create_stream)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#create_stream)
        """

    async def create_thing(
        self,
        *,
        thingName: str,
        thingTypeName: str = ...,
        attributePayload: "AttributePayloadTypeDef" = ...,
        billingGroupName: str = ...
    ) -> CreateThingResponseTypeDef:
        """
        Creates a thing record in the registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.create_thing)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#create_thing)
        """

    async def create_thing_group(
        self,
        *,
        thingGroupName: str,
        parentGroupName: str = ...,
        thingGroupProperties: "ThingGroupPropertiesTypeDef" = ...,
        tags: Sequence["TagTypeDef"] = ...
    ) -> CreateThingGroupResponseTypeDef:
        """
        Create a thing group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.create_thing_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#create_thing_group)
        """

    async def create_thing_type(
        self,
        *,
        thingTypeName: str,
        thingTypeProperties: "ThingTypePropertiesTypeDef" = ...,
        tags: Sequence["TagTypeDef"] = ...
    ) -> CreateThingTypeResponseTypeDef:
        """
        Creates a new thing type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.create_thing_type)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#create_thing_type)
        """

    async def create_topic_rule(
        self, *, ruleName: str, topicRulePayload: "TopicRulePayloadTypeDef", tags: str = ...
    ) -> None:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.create_topic_rule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#create_topic_rule)
        """

    async def create_topic_rule_destination(
        self, *, destinationConfiguration: "TopicRuleDestinationConfigurationTypeDef"
    ) -> CreateTopicRuleDestinationResponseTypeDef:
        """
        Creates a topic rule destination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.create_topic_rule_destination)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#create_topic_rule_destination)
        """

    async def delete_account_audit_configuration(
        self, *, deleteScheduledAudits: bool = ...
    ) -> Dict[str, Any]:
        """
        Restores the default settings for Device Defender audits for this account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.delete_account_audit_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#delete_account_audit_configuration)
        """

    async def delete_audit_suppression(
        self, *, checkName: str, resourceIdentifier: "ResourceIdentifierTypeDef"
    ) -> Dict[str, Any]:
        """
        Deletes a Device Defender audit suppression.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.delete_audit_suppression)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#delete_audit_suppression)
        """

    async def delete_authorizer(self, *, authorizerName: str) -> Dict[str, Any]:
        """
        Deletes an authorizer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.delete_authorizer)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#delete_authorizer)
        """

    async def delete_billing_group(
        self, *, billingGroupName: str, expectedVersion: int = ...
    ) -> Dict[str, Any]:
        """
        Deletes the billing group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.delete_billing_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#delete_billing_group)
        """

    async def delete_ca_certificate(self, *, certificateId: str) -> Dict[str, Any]:
        """
        Deletes a registered CA certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.delete_ca_certificate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#delete_ca_certificate)
        """

    async def delete_certificate(self, *, certificateId: str, forceDelete: bool = ...) -> None:
        """
        Deletes the specified certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.delete_certificate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#delete_certificate)
        """

    async def delete_custom_metric(self, *, metricName: str) -> Dict[str, Any]:
        """
        Deletes a Device Defender detect custom metric.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.delete_custom_metric)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#delete_custom_metric)
        """

    async def delete_dimension(self, *, name: str) -> Dict[str, Any]:
        """
        Removes the specified dimension from your Amazon Web Services accounts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.delete_dimension)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#delete_dimension)
        """

    async def delete_domain_configuration(self, *, domainConfigurationName: str) -> Dict[str, Any]:
        """
        Deletes the specified domain configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.delete_domain_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#delete_domain_configuration)
        """

    async def delete_dynamic_thing_group(
        self, *, thingGroupName: str, expectedVersion: int = ...
    ) -> Dict[str, Any]:
        """
        Deletes a dynamic thing group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.delete_dynamic_thing_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#delete_dynamic_thing_group)
        """

    async def delete_fleet_metric(self, *, metricName: str, expectedVersion: int = ...) -> None:
        """
        Deletes the specified fleet metric.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.delete_fleet_metric)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#delete_fleet_metric)
        """

    async def delete_job(self, *, jobId: str, force: bool = ..., namespaceId: str = ...) -> None:
        """
        Deletes a job and its related job executions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.delete_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#delete_job)
        """

    async def delete_job_execution(
        self,
        *,
        jobId: str,
        thingName: str,
        executionNumber: int,
        force: bool = ...,
        namespaceId: str = ...
    ) -> None:
        """
        Deletes a job execution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.delete_job_execution)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#delete_job_execution)
        """

    async def delete_job_template(self, *, jobTemplateId: str) -> None:
        """
        Deletes the specified job template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.delete_job_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#delete_job_template)
        """

    async def delete_mitigation_action(self, *, actionName: str) -> Dict[str, Any]:
        """
        Deletes a defined mitigation action from your Amazon Web Services accounts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.delete_mitigation_action)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#delete_mitigation_action)
        """

    async def delete_ota_update(
        self, *, otaUpdateId: str, deleteStream: bool = ..., forceDeleteAWSJob: bool = ...
    ) -> Dict[str, Any]:
        """
        Delete an OTA update.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.delete_ota_update)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#delete_ota_update)
        """

    async def delete_policy(self, *, policyName: str) -> None:
        """
        Deletes the specified policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.delete_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#delete_policy)
        """

    async def delete_policy_version(self, *, policyName: str, policyVersionId: str) -> None:
        """
        Deletes the specified version of the specified policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.delete_policy_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#delete_policy_version)
        """

    async def delete_provisioning_template(self, *, templateName: str) -> Dict[str, Any]:
        """
        Deletes a fleet provisioning template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.delete_provisioning_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#delete_provisioning_template)
        """

    async def delete_provisioning_template_version(
        self, *, templateName: str, versionId: int
    ) -> Dict[str, Any]:
        """
        Deletes a fleet provisioning template version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.delete_provisioning_template_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#delete_provisioning_template_version)
        """

    async def delete_registration_code(self) -> Dict[str, Any]:
        """
        Deletes a CA certificate registration code.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.delete_registration_code)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#delete_registration_code)
        """

    async def delete_role_alias(self, *, roleAlias: str) -> Dict[str, Any]:
        """
        Deletes a role alias Requires permission to access the
        [DeleteRoleAlias](https://docs.aws.amazon.com/service-
        authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions)_
        action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.delete_role_alias)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#delete_role_alias)
        """

    async def delete_scheduled_audit(self, *, scheduledAuditName: str) -> Dict[str, Any]:
        """
        Deletes a scheduled audit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.delete_scheduled_audit)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#delete_scheduled_audit)
        """

    async def delete_security_profile(
        self, *, securityProfileName: str, expectedVersion: int = ...
    ) -> Dict[str, Any]:
        """
        Deletes a Device Defender security profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.delete_security_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#delete_security_profile)
        """

    async def delete_stream(self, *, streamId: str) -> Dict[str, Any]:
        """
        Deletes a stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.delete_stream)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#delete_stream)
        """

    async def delete_thing(self, *, thingName: str, expectedVersion: int = ...) -> Dict[str, Any]:
        """
        Deletes the specified thing.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.delete_thing)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#delete_thing)
        """

    async def delete_thing_group(
        self, *, thingGroupName: str, expectedVersion: int = ...
    ) -> Dict[str, Any]:
        """
        Deletes a thing group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.delete_thing_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#delete_thing_group)
        """

    async def delete_thing_type(self, *, thingTypeName: str) -> Dict[str, Any]:
        """
        Deletes the specified thing type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.delete_thing_type)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#delete_thing_type)
        """

    async def delete_topic_rule(self, *, ruleName: str) -> None:
        """
        Deletes the rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.delete_topic_rule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#delete_topic_rule)
        """

    async def delete_topic_rule_destination(self, *, arn: str) -> Dict[str, Any]:
        """
        Deletes a topic rule destination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.delete_topic_rule_destination)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#delete_topic_rule_destination)
        """

    async def delete_v2_logging_level(
        self, *, targetType: LogTargetTypeType, targetName: str
    ) -> None:
        """
        Deletes a logging level.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.delete_v2_logging_level)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#delete_v2_logging_level)
        """

    async def deprecate_thing_type(
        self, *, thingTypeName: str, undoDeprecate: bool = ...
    ) -> Dict[str, Any]:
        """
        Deprecates a thing type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.deprecate_thing_type)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#deprecate_thing_type)
        """

    async def describe_account_audit_configuration(
        self,
    ) -> DescribeAccountAuditConfigurationResponseTypeDef:
        """
        Gets information about the Device Defender audit settings for this account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.describe_account_audit_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#describe_account_audit_configuration)
        """

    async def describe_audit_finding(
        self, *, findingId: str
    ) -> DescribeAuditFindingResponseTypeDef:
        """
        Gets information about a single audit finding.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.describe_audit_finding)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#describe_audit_finding)
        """

    async def describe_audit_mitigation_actions_task(
        self, *, taskId: str
    ) -> DescribeAuditMitigationActionsTaskResponseTypeDef:
        """
        Gets information about an audit mitigation task that is used to apply mitigation
        actions to a set of audit findings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.describe_audit_mitigation_actions_task)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#describe_audit_mitigation_actions_task)
        """

    async def describe_audit_suppression(
        self, *, checkName: str, resourceIdentifier: "ResourceIdentifierTypeDef"
    ) -> DescribeAuditSuppressionResponseTypeDef:
        """
        Gets information about a Device Defender audit suppression.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.describe_audit_suppression)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#describe_audit_suppression)
        """

    async def describe_audit_task(self, *, taskId: str) -> DescribeAuditTaskResponseTypeDef:
        """
        Gets information about a Device Defender audit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.describe_audit_task)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#describe_audit_task)
        """

    async def describe_authorizer(
        self, *, authorizerName: str
    ) -> DescribeAuthorizerResponseTypeDef:
        """
        Describes an authorizer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.describe_authorizer)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#describe_authorizer)
        """

    async def describe_billing_group(
        self, *, billingGroupName: str
    ) -> DescribeBillingGroupResponseTypeDef:
        """
        Returns information about a billing group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.describe_billing_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#describe_billing_group)
        """

    async def describe_ca_certificate(
        self, *, certificateId: str
    ) -> DescribeCACertificateResponseTypeDef:
        """
        Describes a registered CA certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.describe_ca_certificate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#describe_ca_certificate)
        """

    async def describe_certificate(
        self, *, certificateId: str
    ) -> DescribeCertificateResponseTypeDef:
        """
        Gets information about the specified certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.describe_certificate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#describe_certificate)
        """

    async def describe_custom_metric(
        self, *, metricName: str
    ) -> DescribeCustomMetricResponseTypeDef:
        """
        Gets information about a Device Defender detect custom metric.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.describe_custom_metric)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#describe_custom_metric)
        """

    async def describe_default_authorizer(self) -> DescribeDefaultAuthorizerResponseTypeDef:
        """
        Describes the default authorizer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.describe_default_authorizer)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#describe_default_authorizer)
        """

    async def describe_detect_mitigation_actions_task(
        self, *, taskId: str
    ) -> DescribeDetectMitigationActionsTaskResponseTypeDef:
        """
        Gets information about a Device Defender ML Detect mitigation action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.describe_detect_mitigation_actions_task)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#describe_detect_mitigation_actions_task)
        """

    async def describe_dimension(self, *, name: str) -> DescribeDimensionResponseTypeDef:
        """
        Provides details about a dimension that is defined in your Amazon Web Services
        accounts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.describe_dimension)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#describe_dimension)
        """

    async def describe_domain_configuration(
        self, *, domainConfigurationName: str
    ) -> DescribeDomainConfigurationResponseTypeDef:
        """
        Gets summary information about a domain configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.describe_domain_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#describe_domain_configuration)
        """

    async def describe_endpoint(
        self, *, endpointType: str = ...
    ) -> DescribeEndpointResponseTypeDef:
        """
        Returns a unique endpoint specific to the Amazon Web Services account making the
        call.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.describe_endpoint)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#describe_endpoint)
        """

    async def describe_event_configurations(self) -> DescribeEventConfigurationsResponseTypeDef:
        """
        Describes event configurations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.describe_event_configurations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#describe_event_configurations)
        """

    async def describe_fleet_metric(self, *, metricName: str) -> DescribeFleetMetricResponseTypeDef:
        """
        Gets information about the specified fleet metric.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.describe_fleet_metric)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#describe_fleet_metric)
        """

    async def describe_index(self, *, indexName: str) -> DescribeIndexResponseTypeDef:
        """
        Describes a search index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.describe_index)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#describe_index)
        """

    async def describe_job(self, *, jobId: str) -> DescribeJobResponseTypeDef:
        """
        Describes a job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.describe_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#describe_job)
        """

    async def describe_job_execution(
        self, *, jobId: str, thingName: str, executionNumber: int = ...
    ) -> DescribeJobExecutionResponseTypeDef:
        """
        Describes a job execution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.describe_job_execution)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#describe_job_execution)
        """

    async def describe_job_template(
        self, *, jobTemplateId: str
    ) -> DescribeJobTemplateResponseTypeDef:
        """
        Returns information about a job template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.describe_job_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#describe_job_template)
        """

    async def describe_managed_job_template(
        self, *, templateName: str, templateVersion: str = ...
    ) -> DescribeManagedJobTemplateResponseTypeDef:
        """
        View details of a managed job template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.describe_managed_job_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#describe_managed_job_template)
        """

    async def describe_mitigation_action(
        self, *, actionName: str
    ) -> DescribeMitigationActionResponseTypeDef:
        """
        Gets information about a mitigation action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.describe_mitigation_action)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#describe_mitigation_action)
        """

    async def describe_provisioning_template(
        self, *, templateName: str
    ) -> DescribeProvisioningTemplateResponseTypeDef:
        """
        Returns information about a fleet provisioning template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.describe_provisioning_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#describe_provisioning_template)
        """

    async def describe_provisioning_template_version(
        self, *, templateName: str, versionId: int
    ) -> DescribeProvisioningTemplateVersionResponseTypeDef:
        """
        Returns information about a fleet provisioning template version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.describe_provisioning_template_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#describe_provisioning_template_version)
        """

    async def describe_role_alias(self, *, roleAlias: str) -> DescribeRoleAliasResponseTypeDef:
        """
        Describes a role alias.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.describe_role_alias)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#describe_role_alias)
        """

    async def describe_scheduled_audit(
        self, *, scheduledAuditName: str
    ) -> DescribeScheduledAuditResponseTypeDef:
        """
        Gets information about a scheduled audit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.describe_scheduled_audit)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#describe_scheduled_audit)
        """

    async def describe_security_profile(
        self, *, securityProfileName: str
    ) -> DescribeSecurityProfileResponseTypeDef:
        """
        Gets information about a Device Defender security profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.describe_security_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#describe_security_profile)
        """

    async def describe_stream(self, *, streamId: str) -> DescribeStreamResponseTypeDef:
        """
        Gets information about a stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.describe_stream)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#describe_stream)
        """

    async def describe_thing(self, *, thingName: str) -> DescribeThingResponseTypeDef:
        """
        Gets information about the specified thing.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.describe_thing)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#describe_thing)
        """

    async def describe_thing_group(
        self, *, thingGroupName: str
    ) -> DescribeThingGroupResponseTypeDef:
        """
        Describe a thing group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.describe_thing_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#describe_thing_group)
        """

    async def describe_thing_registration_task(
        self, *, taskId: str
    ) -> DescribeThingRegistrationTaskResponseTypeDef:
        """
        Describes a bulk thing provisioning task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.describe_thing_registration_task)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#describe_thing_registration_task)
        """

    async def describe_thing_type(self, *, thingTypeName: str) -> DescribeThingTypeResponseTypeDef:
        """
        Gets information about the specified thing type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.describe_thing_type)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#describe_thing_type)
        """

    async def detach_policy(self, *, policyName: str, target: str) -> None:
        """
        Detaches a policy from the specified target.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.detach_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#detach_policy)
        """

    async def detach_principal_policy(self, *, policyName: str, principal: str) -> None:
        """
        Removes the specified policy from the specified certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.detach_principal_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#detach_principal_policy)
        """

    async def detach_security_profile(
        self, *, securityProfileName: str, securityProfileTargetArn: str
    ) -> Dict[str, Any]:
        """
        Disassociates a Device Defender security profile from a thing group or from this
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.detach_security_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#detach_security_profile)
        """

    async def detach_thing_principal(self, *, thingName: str, principal: str) -> Dict[str, Any]:
        """
        Detaches the specified principal from the specified thing.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.detach_thing_principal)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#detach_thing_principal)
        """

    async def disable_topic_rule(self, *, ruleName: str) -> None:
        """
        Disables the rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.disable_topic_rule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#disable_topic_rule)
        """

    async def enable_topic_rule(self, *, ruleName: str) -> None:
        """
        Enables the rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.enable_topic_rule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#enable_topic_rule)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#generate_presigned_url)
        """

    async def get_behavior_model_training_summaries(
        self, *, securityProfileName: str = ..., maxResults: int = ..., nextToken: str = ...
    ) -> GetBehaviorModelTrainingSummariesResponseTypeDef:
        """
        Returns a Device Defender's ML Detect Security Profile training model's status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.get_behavior_model_training_summaries)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#get_behavior_model_training_summaries)
        """

    async def get_buckets_aggregation(
        self,
        *,
        queryString: str,
        aggregationField: str,
        bucketsAggregationType: "BucketsAggregationTypeTypeDef",
        indexName: str = ...,
        queryVersion: str = ...
    ) -> GetBucketsAggregationResponseTypeDef:
        """
        Aggregates on indexed data with search queries pertaining to particular fields.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.get_buckets_aggregation)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#get_buckets_aggregation)
        """

    async def get_cardinality(
        self,
        *,
        queryString: str,
        indexName: str = ...,
        aggregationField: str = ...,
        queryVersion: str = ...
    ) -> GetCardinalityResponseTypeDef:
        """
        Returns the approximate count of unique values that match the query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.get_cardinality)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#get_cardinality)
        """

    async def get_effective_policies(
        self, *, principal: str = ..., cognitoIdentityPoolId: str = ..., thingName: str = ...
    ) -> GetEffectivePoliciesResponseTypeDef:
        """
        Gets a list of the policies that have an effect on the authorization behavior of
        the specified device when it connects to the IoT device gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.get_effective_policies)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#get_effective_policies)
        """

    async def get_indexing_configuration(self) -> GetIndexingConfigurationResponseTypeDef:
        """
        Gets the indexing configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.get_indexing_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#get_indexing_configuration)
        """

    async def get_job_document(self, *, jobId: str) -> GetJobDocumentResponseTypeDef:
        """
        Gets a job document.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.get_job_document)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#get_job_document)
        """

    async def get_logging_options(self) -> GetLoggingOptionsResponseTypeDef:
        """
        Gets the logging options.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.get_logging_options)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#get_logging_options)
        """

    async def get_ota_update(self, *, otaUpdateId: str) -> GetOTAUpdateResponseTypeDef:
        """
        Gets an OTA update.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.get_ota_update)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#get_ota_update)
        """

    async def get_percentiles(
        self,
        *,
        queryString: str,
        indexName: str = ...,
        aggregationField: str = ...,
        queryVersion: str = ...,
        percents: Sequence[float] = ...
    ) -> GetPercentilesResponseTypeDef:
        """
        Groups the aggregated values that match the query into percentile groupings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.get_percentiles)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#get_percentiles)
        """

    async def get_policy(self, *, policyName: str) -> GetPolicyResponseTypeDef:
        """
        Gets information about the specified policy with the policy document of the
        default version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.get_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#get_policy)
        """

    async def get_policy_version(
        self, *, policyName: str, policyVersionId: str
    ) -> GetPolicyVersionResponseTypeDef:
        """
        Gets information about the specified policy version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.get_policy_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#get_policy_version)
        """

    async def get_registration_code(self) -> GetRegistrationCodeResponseTypeDef:
        """
        Gets a registration code used to register a CA certificate with IoT.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.get_registration_code)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#get_registration_code)
        """

    async def get_statistics(
        self,
        *,
        queryString: str,
        indexName: str = ...,
        aggregationField: str = ...,
        queryVersion: str = ...
    ) -> GetStatisticsResponseTypeDef:
        """
        Returns the count, average, sum, minimum, maximum, sum of squares, variance, and
        standard deviation for the specified aggregated field.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.get_statistics)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#get_statistics)
        """

    async def get_topic_rule(self, *, ruleName: str) -> GetTopicRuleResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.get_topic_rule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#get_topic_rule)
        """

    async def get_topic_rule_destination(
        self, *, arn: str
    ) -> GetTopicRuleDestinationResponseTypeDef:
        """
        Gets information about a topic rule destination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.get_topic_rule_destination)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#get_topic_rule_destination)
        """

    async def get_v2_logging_options(self) -> GetV2LoggingOptionsResponseTypeDef:
        """
        Gets the fine grained logging options.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.get_v2_logging_options)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#get_v2_logging_options)
        """

    async def list_active_violations(
        self,
        *,
        thingName: str = ...,
        securityProfileName: str = ...,
        behaviorCriteriaType: BehaviorCriteriaTypeType = ...,
        listSuppressedAlerts: bool = ...,
        verificationState: VerificationStateType = ...,
        nextToken: str = ...,
        maxResults: int = ...
    ) -> ListActiveViolationsResponseTypeDef:
        """
        Lists the active violations for a given Device Defender security profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.list_active_violations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#list_active_violations)
        """

    async def list_attached_policies(
        self, *, target: str, recursive: bool = ..., marker: str = ..., pageSize: int = ...
    ) -> ListAttachedPoliciesResponseTypeDef:
        """
        Lists the policies attached to the specified thing group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.list_attached_policies)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#list_attached_policies)
        """

    async def list_audit_findings(
        self,
        *,
        taskId: str = ...,
        checkName: str = ...,
        resourceIdentifier: "ResourceIdentifierTypeDef" = ...,
        maxResults: int = ...,
        nextToken: str = ...,
        startTime: Union[datetime, str] = ...,
        endTime: Union[datetime, str] = ...,
        listSuppressedFindings: bool = ...
    ) -> ListAuditFindingsResponseTypeDef:
        """
        Lists the findings (results) of a Device Defender audit or of the audits
        performed during a specified time period.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.list_audit_findings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#list_audit_findings)
        """

    async def list_audit_mitigation_actions_executions(
        self,
        *,
        taskId: str,
        findingId: str,
        actionStatus: AuditMitigationActionsExecutionStatusType = ...,
        maxResults: int = ...,
        nextToken: str = ...
    ) -> ListAuditMitigationActionsExecutionsResponseTypeDef:
        """
        Gets the status of audit mitigation action tasks that were executed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.list_audit_mitigation_actions_executions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#list_audit_mitigation_actions_executions)
        """

    async def list_audit_mitigation_actions_tasks(
        self,
        *,
        startTime: Union[datetime, str],
        endTime: Union[datetime, str],
        auditTaskId: str = ...,
        findingId: str = ...,
        taskStatus: AuditMitigationActionsTaskStatusType = ...,
        maxResults: int = ...,
        nextToken: str = ...
    ) -> ListAuditMitigationActionsTasksResponseTypeDef:
        """
        Gets a list of audit mitigation action tasks that match the specified filters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.list_audit_mitigation_actions_tasks)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#list_audit_mitigation_actions_tasks)
        """

    async def list_audit_suppressions(
        self,
        *,
        checkName: str = ...,
        resourceIdentifier: "ResourceIdentifierTypeDef" = ...,
        ascendingOrder: bool = ...,
        nextToken: str = ...,
        maxResults: int = ...
    ) -> ListAuditSuppressionsResponseTypeDef:
        """
        Lists your Device Defender audit listings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.list_audit_suppressions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#list_audit_suppressions)
        """

    async def list_audit_tasks(
        self,
        *,
        startTime: Union[datetime, str],
        endTime: Union[datetime, str],
        taskType: AuditTaskTypeType = ...,
        taskStatus: AuditTaskStatusType = ...,
        nextToken: str = ...,
        maxResults: int = ...
    ) -> ListAuditTasksResponseTypeDef:
        """
        Lists the Device Defender audits that have been performed during a given time
        period.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.list_audit_tasks)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#list_audit_tasks)
        """

    async def list_authorizers(
        self,
        *,
        pageSize: int = ...,
        marker: str = ...,
        ascendingOrder: bool = ...,
        status: AuthorizerStatusType = ...
    ) -> ListAuthorizersResponseTypeDef:
        """
        Lists the authorizers registered in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.list_authorizers)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#list_authorizers)
        """

    async def list_billing_groups(
        self, *, nextToken: str = ..., maxResults: int = ..., namePrefixFilter: str = ...
    ) -> ListBillingGroupsResponseTypeDef:
        """
        Lists the billing groups you have created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.list_billing_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#list_billing_groups)
        """

    async def list_ca_certificates(
        self, *, pageSize: int = ..., marker: str = ..., ascendingOrder: bool = ...
    ) -> ListCACertificatesResponseTypeDef:
        """
        Lists the CA certificates registered for your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.list_ca_certificates)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#list_ca_certificates)
        """

    async def list_certificates(
        self, *, pageSize: int = ..., marker: str = ..., ascendingOrder: bool = ...
    ) -> ListCertificatesResponseTypeDef:
        """
        Lists the certificates registered in your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.list_certificates)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#list_certificates)
        """

    async def list_certificates_by_ca(
        self,
        *,
        caCertificateId: str,
        pageSize: int = ...,
        marker: str = ...,
        ascendingOrder: bool = ...
    ) -> ListCertificatesByCAResponseTypeDef:
        """
        List the device certificates signed by the specified CA certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.list_certificates_by_ca)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#list_certificates_by_ca)
        """

    async def list_custom_metrics(
        self, *, nextToken: str = ..., maxResults: int = ...
    ) -> ListCustomMetricsResponseTypeDef:
        """
        Lists your Device Defender detect custom metrics.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.list_custom_metrics)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#list_custom_metrics)
        """

    async def list_detect_mitigation_actions_executions(
        self,
        *,
        taskId: str = ...,
        violationId: str = ...,
        thingName: str = ...,
        startTime: Union[datetime, str] = ...,
        endTime: Union[datetime, str] = ...,
        maxResults: int = ...,
        nextToken: str = ...
    ) -> ListDetectMitigationActionsExecutionsResponseTypeDef:
        """
        Lists mitigation actions executions for a Device Defender ML Detect Security
        Profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.list_detect_mitigation_actions_executions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#list_detect_mitigation_actions_executions)
        """

    async def list_detect_mitigation_actions_tasks(
        self,
        *,
        startTime: Union[datetime, str],
        endTime: Union[datetime, str],
        maxResults: int = ...,
        nextToken: str = ...
    ) -> ListDetectMitigationActionsTasksResponseTypeDef:
        """
        List of Device Defender ML Detect mitigation actions tasks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.list_detect_mitigation_actions_tasks)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#list_detect_mitigation_actions_tasks)
        """

    async def list_dimensions(
        self, *, nextToken: str = ..., maxResults: int = ...
    ) -> ListDimensionsResponseTypeDef:
        """
        List the set of dimensions that are defined for your Amazon Web Services
        accounts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.list_dimensions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#list_dimensions)
        """

    async def list_domain_configurations(
        self, *, marker: str = ..., pageSize: int = ..., serviceType: ServiceTypeType = ...
    ) -> ListDomainConfigurationsResponseTypeDef:
        """
        Gets a list of domain configurations for the user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.list_domain_configurations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#list_domain_configurations)
        """

    async def list_fleet_metrics(
        self, *, nextToken: str = ..., maxResults: int = ...
    ) -> ListFleetMetricsResponseTypeDef:
        """
        Lists all your fleet metrics.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.list_fleet_metrics)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#list_fleet_metrics)
        """

    async def list_indices(
        self, *, nextToken: str = ..., maxResults: int = ...
    ) -> ListIndicesResponseTypeDef:
        """
        Lists the search indices.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.list_indices)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#list_indices)
        """

    async def list_job_executions_for_job(
        self,
        *,
        jobId: str,
        status: JobExecutionStatusType = ...,
        maxResults: int = ...,
        nextToken: str = ...
    ) -> ListJobExecutionsForJobResponseTypeDef:
        """
        Lists the job executions for a job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.list_job_executions_for_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#list_job_executions_for_job)
        """

    async def list_job_executions_for_thing(
        self,
        *,
        thingName: str,
        status: JobExecutionStatusType = ...,
        namespaceId: str = ...,
        maxResults: int = ...,
        nextToken: str = ...,
        jobId: str = ...
    ) -> ListJobExecutionsForThingResponseTypeDef:
        """
        Lists the job executions for the specified thing.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.list_job_executions_for_thing)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#list_job_executions_for_thing)
        """

    async def list_job_templates(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> ListJobTemplatesResponseTypeDef:
        """
        Returns a list of job templates.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.list_job_templates)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#list_job_templates)
        """

    async def list_jobs(
        self,
        *,
        status: JobStatusType = ...,
        targetSelection: TargetSelectionType = ...,
        maxResults: int = ...,
        nextToken: str = ...,
        thingGroupName: str = ...,
        thingGroupId: str = ...,
        namespaceId: str = ...
    ) -> ListJobsResponseTypeDef:
        """
        Lists jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.list_jobs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#list_jobs)
        """

    async def list_managed_job_templates(
        self, *, templateName: str = ..., maxResults: int = ..., nextToken: str = ...
    ) -> ListManagedJobTemplatesResponseTypeDef:
        """
        Returns a list of managed job templates.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.list_managed_job_templates)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#list_managed_job_templates)
        """

    async def list_mitigation_actions(
        self,
        *,
        actionType: MitigationActionTypeType = ...,
        maxResults: int = ...,
        nextToken: str = ...
    ) -> ListMitigationActionsResponseTypeDef:
        """
        Gets a list of all mitigation actions that match the specified filter criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.list_mitigation_actions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#list_mitigation_actions)
        """

    async def list_ota_updates(
        self,
        *,
        maxResults: int = ...,
        nextToken: str = ...,
        otaUpdateStatus: OTAUpdateStatusType = ...
    ) -> ListOTAUpdatesResponseTypeDef:
        """
        Lists OTA updates.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.list_ota_updates)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#list_ota_updates)
        """

    async def list_outgoing_certificates(
        self, *, pageSize: int = ..., marker: str = ..., ascendingOrder: bool = ...
    ) -> ListOutgoingCertificatesResponseTypeDef:
        """
        Lists certificates that are being transferred but not yet accepted.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.list_outgoing_certificates)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#list_outgoing_certificates)
        """

    async def list_policies(
        self, *, marker: str = ..., pageSize: int = ..., ascendingOrder: bool = ...
    ) -> ListPoliciesResponseTypeDef:
        """
        Lists your policies.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.list_policies)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#list_policies)
        """

    async def list_policy_principals(
        self, *, policyName: str, marker: str = ..., pageSize: int = ..., ascendingOrder: bool = ...
    ) -> ListPolicyPrincipalsResponseTypeDef:
        """
        Lists the principals associated with the specified policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.list_policy_principals)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#list_policy_principals)
        """

    async def list_policy_versions(self, *, policyName: str) -> ListPolicyVersionsResponseTypeDef:
        """
        Lists the versions of the specified policy and identifies the default version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.list_policy_versions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#list_policy_versions)
        """

    async def list_principal_policies(
        self, *, principal: str, marker: str = ..., pageSize: int = ..., ascendingOrder: bool = ...
    ) -> ListPrincipalPoliciesResponseTypeDef:
        """
        Lists the policies attached to the specified principal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.list_principal_policies)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#list_principal_policies)
        """

    async def list_principal_things(
        self, *, principal: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListPrincipalThingsResponseTypeDef:
        """
        Lists the things associated with the specified principal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.list_principal_things)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#list_principal_things)
        """

    async def list_provisioning_template_versions(
        self, *, templateName: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListProvisioningTemplateVersionsResponseTypeDef:
        """
        A list of fleet provisioning template versions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.list_provisioning_template_versions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#list_provisioning_template_versions)
        """

    async def list_provisioning_templates(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> ListProvisioningTemplatesResponseTypeDef:
        """
        Lists the fleet provisioning templates in your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.list_provisioning_templates)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#list_provisioning_templates)
        """

    async def list_role_aliases(
        self, *, pageSize: int = ..., marker: str = ..., ascendingOrder: bool = ...
    ) -> ListRoleAliasesResponseTypeDef:
        """
        Lists the role aliases registered in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.list_role_aliases)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#list_role_aliases)
        """

    async def list_scheduled_audits(
        self, *, nextToken: str = ..., maxResults: int = ...
    ) -> ListScheduledAuditsResponseTypeDef:
        """
        Lists all of your scheduled audits.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.list_scheduled_audits)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#list_scheduled_audits)
        """

    async def list_security_profiles(
        self,
        *,
        nextToken: str = ...,
        maxResults: int = ...,
        dimensionName: str = ...,
        metricName: str = ...
    ) -> ListSecurityProfilesResponseTypeDef:
        """
        Lists the Device Defender security profiles you've created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.list_security_profiles)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#list_security_profiles)
        """

    async def list_security_profiles_for_target(
        self,
        *,
        securityProfileTargetArn: str,
        nextToken: str = ...,
        maxResults: int = ...,
        recursive: bool = ...
    ) -> ListSecurityProfilesForTargetResponseTypeDef:
        """
        Lists the Device Defender security profiles attached to a target (thing group).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.list_security_profiles_for_target)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#list_security_profiles_for_target)
        """

    async def list_streams(
        self, *, maxResults: int = ..., nextToken: str = ..., ascendingOrder: bool = ...
    ) -> ListStreamsResponseTypeDef:
        """
        Lists all of the streams in your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.list_streams)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#list_streams)
        """

    async def list_tags_for_resource(
        self, *, resourceArn: str, nextToken: str = ...
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags (metadata) you have assigned to the resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#list_tags_for_resource)
        """

    async def list_targets_for_policy(
        self, *, policyName: str, marker: str = ..., pageSize: int = ...
    ) -> ListTargetsForPolicyResponseTypeDef:
        """
        List targets for the specified policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.list_targets_for_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#list_targets_for_policy)
        """

    async def list_targets_for_security_profile(
        self, *, securityProfileName: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListTargetsForSecurityProfileResponseTypeDef:
        """
        Lists the targets (thing groups) associated with a given Device Defender
        security profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.list_targets_for_security_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#list_targets_for_security_profile)
        """

    async def list_thing_groups(
        self,
        *,
        nextToken: str = ...,
        maxResults: int = ...,
        parentGroup: str = ...,
        namePrefixFilter: str = ...,
        recursive: bool = ...
    ) -> ListThingGroupsResponseTypeDef:
        """
        List the thing groups in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.list_thing_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#list_thing_groups)
        """

    async def list_thing_groups_for_thing(
        self, *, thingName: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListThingGroupsForThingResponseTypeDef:
        """
        List the thing groups to which the specified thing belongs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.list_thing_groups_for_thing)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#list_thing_groups_for_thing)
        """

    async def list_thing_principals(
        self, *, thingName: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListThingPrincipalsResponseTypeDef:
        """
        Lists the principals associated with the specified thing.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.list_thing_principals)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#list_thing_principals)
        """

    async def list_thing_registration_task_reports(
        self,
        *,
        taskId: str,
        reportType: ReportTypeType,
        nextToken: str = ...,
        maxResults: int = ...
    ) -> ListThingRegistrationTaskReportsResponseTypeDef:
        """
        Information about the thing registration tasks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.list_thing_registration_task_reports)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#list_thing_registration_task_reports)
        """

    async def list_thing_registration_tasks(
        self, *, nextToken: str = ..., maxResults: int = ..., status: StatusType = ...
    ) -> ListThingRegistrationTasksResponseTypeDef:
        """
        List bulk thing provisioning tasks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.list_thing_registration_tasks)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#list_thing_registration_tasks)
        """

    async def list_thing_types(
        self, *, nextToken: str = ..., maxResults: int = ..., thingTypeName: str = ...
    ) -> ListThingTypesResponseTypeDef:
        """
        Lists the existing thing types.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.list_thing_types)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#list_thing_types)
        """

    async def list_things(
        self,
        *,
        nextToken: str = ...,
        maxResults: int = ...,
        attributeName: str = ...,
        attributeValue: str = ...,
        thingTypeName: str = ...,
        usePrefixAttributeValue: bool = ...
    ) -> ListThingsResponseTypeDef:
        """
        Lists your things.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.list_things)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#list_things)
        """

    async def list_things_in_billing_group(
        self, *, billingGroupName: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListThingsInBillingGroupResponseTypeDef:
        """
        Lists the things you have added to the given billing group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.list_things_in_billing_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#list_things_in_billing_group)
        """

    async def list_things_in_thing_group(
        self,
        *,
        thingGroupName: str,
        recursive: bool = ...,
        nextToken: str = ...,
        maxResults: int = ...
    ) -> ListThingsInThingGroupResponseTypeDef:
        """
        Lists the things in the specified group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.list_things_in_thing_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#list_things_in_thing_group)
        """

    async def list_topic_rule_destinations(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> ListTopicRuleDestinationsResponseTypeDef:
        """
        Lists all the topic rule destinations in your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.list_topic_rule_destinations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#list_topic_rule_destinations)
        """

    async def list_topic_rules(
        self,
        *,
        topic: str = ...,
        maxResults: int = ...,
        nextToken: str = ...,
        ruleDisabled: bool = ...
    ) -> ListTopicRulesResponseTypeDef:
        """
        Lists the rules for the specific topic.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.list_topic_rules)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#list_topic_rules)
        """

    async def list_v2_logging_levels(
        self, *, targetType: LogTargetTypeType = ..., nextToken: str = ..., maxResults: int = ...
    ) -> ListV2LoggingLevelsResponseTypeDef:
        """
        Lists logging levels.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.list_v2_logging_levels)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#list_v2_logging_levels)
        """

    async def list_violation_events(
        self,
        *,
        startTime: Union[datetime, str],
        endTime: Union[datetime, str],
        thingName: str = ...,
        securityProfileName: str = ...,
        behaviorCriteriaType: BehaviorCriteriaTypeType = ...,
        listSuppressedAlerts: bool = ...,
        verificationState: VerificationStateType = ...,
        nextToken: str = ...,
        maxResults: int = ...
    ) -> ListViolationEventsResponseTypeDef:
        """
        Lists the Device Defender security profile violations discovered during the
        given time period.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.list_violation_events)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#list_violation_events)
        """

    async def put_verification_state_on_violation(
        self,
        *,
        violationId: str,
        verificationState: VerificationStateType,
        verificationStateDescription: str = ...
    ) -> Dict[str, Any]:
        """
        Set a verification state and provide a description of that verification state on
        a violation (detect alarm).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.put_verification_state_on_violation)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#put_verification_state_on_violation)
        """

    async def register_ca_certificate(
        self,
        *,
        caCertificate: str,
        verificationCertificate: str,
        setAsActive: bool = ...,
        allowAutoRegistration: bool = ...,
        registrationConfig: "RegistrationConfigTypeDef" = ...,
        tags: Sequence["TagTypeDef"] = ...
    ) -> RegisterCACertificateResponseTypeDef:
        """
        Registers a CA certificate with IoT.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.register_ca_certificate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#register_ca_certificate)
        """

    async def register_certificate(
        self,
        *,
        certificatePem: str,
        caCertificatePem: str = ...,
        setAsActive: bool = ...,
        status: CertificateStatusType = ...
    ) -> RegisterCertificateResponseTypeDef:
        """
        Registers a device certificate with IoT.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.register_certificate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#register_certificate)
        """

    async def register_certificate_without_ca(
        self, *, certificatePem: str, status: CertificateStatusType = ...
    ) -> RegisterCertificateWithoutCAResponseTypeDef:
        """
        Register a certificate that does not have a certificate authority (CA).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.register_certificate_without_ca)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#register_certificate_without_ca)
        """

    async def register_thing(
        self, *, templateBody: str, parameters: Mapping[str, str] = ...
    ) -> RegisterThingResponseTypeDef:
        """
        Provisions a thing in the device registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.register_thing)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#register_thing)
        """

    async def reject_certificate_transfer(
        self, *, certificateId: str, rejectReason: str = ...
    ) -> None:
        """
        Rejects a pending certificate transfer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.reject_certificate_transfer)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#reject_certificate_transfer)
        """

    async def remove_thing_from_billing_group(
        self,
        *,
        billingGroupName: str = ...,
        billingGroupArn: str = ...,
        thingName: str = ...,
        thingArn: str = ...
    ) -> Dict[str, Any]:
        """
        Removes the given thing from the billing group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.remove_thing_from_billing_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#remove_thing_from_billing_group)
        """

    async def remove_thing_from_thing_group(
        self,
        *,
        thingGroupName: str = ...,
        thingGroupArn: str = ...,
        thingName: str = ...,
        thingArn: str = ...
    ) -> Dict[str, Any]:
        """
        Remove the specified thing from the specified group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.remove_thing_from_thing_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#remove_thing_from_thing_group)
        """

    async def replace_topic_rule(
        self, *, ruleName: str, topicRulePayload: "TopicRulePayloadTypeDef"
    ) -> None:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.replace_topic_rule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#replace_topic_rule)
        """

    async def search_index(
        self,
        *,
        queryString: str,
        indexName: str = ...,
        nextToken: str = ...,
        maxResults: int = ...,
        queryVersion: str = ...
    ) -> SearchIndexResponseTypeDef:
        """
        The query search index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.search_index)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#search_index)
        """

    async def set_default_authorizer(
        self, *, authorizerName: str
    ) -> SetDefaultAuthorizerResponseTypeDef:
        """
        Sets the default authorizer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.set_default_authorizer)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#set_default_authorizer)
        """

    async def set_default_policy_version(self, *, policyName: str, policyVersionId: str) -> None:
        """
        Sets the specified version of the specified policy as the policy's default
        (operative) version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.set_default_policy_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#set_default_policy_version)
        """

    async def set_logging_options(
        self, *, loggingOptionsPayload: "LoggingOptionsPayloadTypeDef"
    ) -> None:
        """
        Sets the logging options.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.set_logging_options)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#set_logging_options)
        """

    async def set_v2_logging_level(
        self, *, logTarget: "LogTargetTypeDef", logLevel: LogLevelType
    ) -> None:
        """
        Sets the logging level.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.set_v2_logging_level)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#set_v2_logging_level)
        """

    async def set_v2_logging_options(
        self, *, roleArn: str = ..., defaultLogLevel: LogLevelType = ..., disableAllLogs: bool = ...
    ) -> None:
        """
        Sets the logging options for the V2 logging service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.set_v2_logging_options)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#set_v2_logging_options)
        """

    async def start_audit_mitigation_actions_task(
        self,
        *,
        taskId: str,
        target: "AuditMitigationActionsTaskTargetTypeDef",
        auditCheckToActionsMapping: Mapping[str, Sequence[str]],
        clientRequestToken: str
    ) -> StartAuditMitigationActionsTaskResponseTypeDef:
        """
        Starts a task that applies a set of mitigation actions to the specified target.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.start_audit_mitigation_actions_task)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#start_audit_mitigation_actions_task)
        """

    async def start_detect_mitigation_actions_task(
        self,
        *,
        taskId: str,
        target: "DetectMitigationActionsTaskTargetTypeDef",
        actions: Sequence[str],
        clientRequestToken: str,
        violationEventOccurrenceRange: "ViolationEventOccurrenceRangeTypeDef" = ...,
        includeOnlyActiveViolations: bool = ...,
        includeSuppressedAlerts: bool = ...
    ) -> StartDetectMitigationActionsTaskResponseTypeDef:
        """
        Starts a Device Defender ML Detect mitigation actions task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.start_detect_mitigation_actions_task)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#start_detect_mitigation_actions_task)
        """

    async def start_on_demand_audit_task(
        self, *, targetCheckNames: Sequence[str]
    ) -> StartOnDemandAuditTaskResponseTypeDef:
        """
        Starts an on-demand Device Defender audit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.start_on_demand_audit_task)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#start_on_demand_audit_task)
        """

    async def start_thing_registration_task(
        self, *, templateBody: str, inputFileBucket: str, inputFileKey: str, roleArn: str
    ) -> StartThingRegistrationTaskResponseTypeDef:
        """
        Creates a bulk thing provisioning task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.start_thing_registration_task)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#start_thing_registration_task)
        """

    async def stop_thing_registration_task(self, *, taskId: str) -> Dict[str, Any]:
        """
        Cancels a bulk thing provisioning task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.stop_thing_registration_task)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#stop_thing_registration_task)
        """

    async def tag_resource(
        self, *, resourceArn: str, tags: Sequence["TagTypeDef"]
    ) -> Dict[str, Any]:
        """
        Adds to or modifies the tags of the given resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#tag_resource)
        """

    async def test_authorization(
        self,
        *,
        authInfos: Sequence["AuthInfoTypeDef"],
        principal: str = ...,
        cognitoIdentityPoolId: str = ...,
        clientId: str = ...,
        policyNamesToAdd: Sequence[str] = ...,
        policyNamesToSkip: Sequence[str] = ...
    ) -> TestAuthorizationResponseTypeDef:
        """
        Tests if a specified principal is authorized to perform an IoT action on a
        specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.test_authorization)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#test_authorization)
        """

    async def test_invoke_authorizer(
        self,
        *,
        authorizerName: str,
        token: str = ...,
        tokenSignature: str = ...,
        httpContext: "HttpContextTypeDef" = ...,
        mqttContext: "MqttContextTypeDef" = ...,
        tlsContext: "TlsContextTypeDef" = ...
    ) -> TestInvokeAuthorizerResponseTypeDef:
        """
        Tests a custom authorization behavior by invoking a specified custom authorizer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.test_invoke_authorizer)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#test_invoke_authorizer)
        """

    async def transfer_certificate(
        self, *, certificateId: str, targetAwsAccount: str, transferMessage: str = ...
    ) -> TransferCertificateResponseTypeDef:
        """
        Transfers the specified certificate to the specified Amazon Web Services
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.transfer_certificate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#transfer_certificate)
        """

    async def untag_resource(self, *, resourceArn: str, tagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes the given tags (metadata) from the resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#untag_resource)
        """

    async def update_account_audit_configuration(
        self,
        *,
        roleArn: str = ...,
        auditNotificationTargetConfigurations: Mapping[
            Literal["SNS"], "AuditNotificationTargetTypeDef"
        ] = ...,
        auditCheckConfigurations: Mapping[str, "AuditCheckConfigurationTypeDef"] = ...
    ) -> Dict[str, Any]:
        """
        Configures or reconfigures the Device Defender audit settings for this account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.update_account_audit_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#update_account_audit_configuration)
        """

    async def update_audit_suppression(
        self,
        *,
        checkName: str,
        resourceIdentifier: "ResourceIdentifierTypeDef",
        expirationDate: Union[datetime, str] = ...,
        suppressIndefinitely: bool = ...,
        description: str = ...
    ) -> Dict[str, Any]:
        """
        Updates a Device Defender audit suppression.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.update_audit_suppression)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#update_audit_suppression)
        """

    async def update_authorizer(
        self,
        *,
        authorizerName: str,
        authorizerFunctionArn: str = ...,
        tokenKeyName: str = ...,
        tokenSigningPublicKeys: Mapping[str, str] = ...,
        status: AuthorizerStatusType = ...,
        enableCachingForHttp: bool = ...
    ) -> UpdateAuthorizerResponseTypeDef:
        """
        Updates an authorizer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.update_authorizer)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#update_authorizer)
        """

    async def update_billing_group(
        self,
        *,
        billingGroupName: str,
        billingGroupProperties: "BillingGroupPropertiesTypeDef",
        expectedVersion: int = ...
    ) -> UpdateBillingGroupResponseTypeDef:
        """
        Updates information about the billing group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.update_billing_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#update_billing_group)
        """

    async def update_ca_certificate(
        self,
        *,
        certificateId: str,
        newStatus: CACertificateStatusType = ...,
        newAutoRegistrationStatus: AutoRegistrationStatusType = ...,
        registrationConfig: "RegistrationConfigTypeDef" = ...,
        removeAutoRegistration: bool = ...
    ) -> None:
        """
        Updates a registered CA certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.update_ca_certificate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#update_ca_certificate)
        """

    async def update_certificate(
        self, *, certificateId: str, newStatus: CertificateStatusType
    ) -> None:
        """
        Updates the status of the specified certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.update_certificate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#update_certificate)
        """

    async def update_custom_metric(
        self, *, metricName: str, displayName: str
    ) -> UpdateCustomMetricResponseTypeDef:
        """
        Updates a Device Defender detect custom metric.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.update_custom_metric)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#update_custom_metric)
        """

    async def update_dimension(
        self, *, name: str, stringValues: Sequence[str]
    ) -> UpdateDimensionResponseTypeDef:
        """
        Updates the definition for a dimension.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.update_dimension)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#update_dimension)
        """

    async def update_domain_configuration(
        self,
        *,
        domainConfigurationName: str,
        authorizerConfig: "AuthorizerConfigTypeDef" = ...,
        domainConfigurationStatus: DomainConfigurationStatusType = ...,
        removeAuthorizerConfig: bool = ...
    ) -> UpdateDomainConfigurationResponseTypeDef:
        """
        Updates values stored in the domain configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.update_domain_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#update_domain_configuration)
        """

    async def update_dynamic_thing_group(
        self,
        *,
        thingGroupName: str,
        thingGroupProperties: "ThingGroupPropertiesTypeDef",
        expectedVersion: int = ...,
        indexName: str = ...,
        queryString: str = ...,
        queryVersion: str = ...
    ) -> UpdateDynamicThingGroupResponseTypeDef:
        """
        Updates a dynamic thing group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.update_dynamic_thing_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#update_dynamic_thing_group)
        """

    async def update_event_configurations(
        self, *, eventConfigurations: Mapping[EventTypeType, "ConfigurationTypeDef"] = ...
    ) -> Dict[str, Any]:
        """
        Updates the event configurations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.update_event_configurations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#update_event_configurations)
        """

    async def update_fleet_metric(
        self,
        *,
        metricName: str,
        indexName: str,
        queryString: str = ...,
        aggregationType: "AggregationTypeTypeDef" = ...,
        period: int = ...,
        aggregationField: str = ...,
        description: str = ...,
        queryVersion: str = ...,
        unit: FleetMetricUnitType = ...,
        expectedVersion: int = ...
    ) -> None:
        """
        Updates the data for a fleet metric.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.update_fleet_metric)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#update_fleet_metric)
        """

    async def update_indexing_configuration(
        self,
        *,
        thingIndexingConfiguration: "ThingIndexingConfigurationTypeDef" = ...,
        thingGroupIndexingConfiguration: "ThingGroupIndexingConfigurationTypeDef" = ...
    ) -> Dict[str, Any]:
        """
        Updates the search configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.update_indexing_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#update_indexing_configuration)
        """

    async def update_job(
        self,
        *,
        jobId: str,
        description: str = ...,
        presignedUrlConfig: "PresignedUrlConfigTypeDef" = ...,
        jobExecutionsRolloutConfig: "JobExecutionsRolloutConfigTypeDef" = ...,
        abortConfig: "AbortConfigTypeDef" = ...,
        timeoutConfig: "TimeoutConfigTypeDef" = ...,
        namespaceId: str = ...,
        jobExecutionsRetryConfig: "JobExecutionsRetryConfigTypeDef" = ...
    ) -> None:
        """
        Updates supported fields of the specified job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.update_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#update_job)
        """

    async def update_mitigation_action(
        self,
        *,
        actionName: str,
        roleArn: str = ...,
        actionParams: "MitigationActionParamsTypeDef" = ...
    ) -> UpdateMitigationActionResponseTypeDef:
        """
        Updates the definition for the specified mitigation action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.update_mitigation_action)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#update_mitigation_action)
        """

    async def update_provisioning_template(
        self,
        *,
        templateName: str,
        description: str = ...,
        enabled: bool = ...,
        defaultVersionId: int = ...,
        provisioningRoleArn: str = ...,
        preProvisioningHook: "ProvisioningHookTypeDef" = ...,
        removePreProvisioningHook: bool = ...
    ) -> Dict[str, Any]:
        """
        Updates a fleet provisioning template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.update_provisioning_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#update_provisioning_template)
        """

    async def update_role_alias(
        self, *, roleAlias: str, roleArn: str = ..., credentialDurationSeconds: int = ...
    ) -> UpdateRoleAliasResponseTypeDef:
        """
        Updates a role alias.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.update_role_alias)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#update_role_alias)
        """

    async def update_scheduled_audit(
        self,
        *,
        scheduledAuditName: str,
        frequency: AuditFrequencyType = ...,
        dayOfMonth: str = ...,
        dayOfWeek: DayOfWeekType = ...,
        targetCheckNames: Sequence[str] = ...
    ) -> UpdateScheduledAuditResponseTypeDef:
        """
        Updates a scheduled audit, including which checks are performed and how often
        the audit takes place.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.update_scheduled_audit)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#update_scheduled_audit)
        """

    async def update_security_profile(
        self,
        *,
        securityProfileName: str,
        securityProfileDescription: str = ...,
        behaviors: Sequence["BehaviorTypeDef"] = ...,
        alertTargets: Mapping[Literal["SNS"], "AlertTargetTypeDef"] = ...,
        additionalMetricsToRetain: Sequence[str] = ...,
        additionalMetricsToRetainV2: Sequence["MetricToRetainTypeDef"] = ...,
        deleteBehaviors: bool = ...,
        deleteAlertTargets: bool = ...,
        deleteAdditionalMetricsToRetain: bool = ...,
        expectedVersion: int = ...
    ) -> UpdateSecurityProfileResponseTypeDef:
        """
        Updates a Device Defender security profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.update_security_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#update_security_profile)
        """

    async def update_stream(
        self,
        *,
        streamId: str,
        description: str = ...,
        files: Sequence["StreamFileTypeDef"] = ...,
        roleArn: str = ...
    ) -> UpdateStreamResponseTypeDef:
        """
        Updates an existing stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.update_stream)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#update_stream)
        """

    async def update_thing(
        self,
        *,
        thingName: str,
        thingTypeName: str = ...,
        attributePayload: "AttributePayloadTypeDef" = ...,
        expectedVersion: int = ...,
        removeThingType: bool = ...
    ) -> Dict[str, Any]:
        """
        Updates the data for a thing.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.update_thing)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#update_thing)
        """

    async def update_thing_group(
        self,
        *,
        thingGroupName: str,
        thingGroupProperties: "ThingGroupPropertiesTypeDef",
        expectedVersion: int = ...
    ) -> UpdateThingGroupResponseTypeDef:
        """
        Update a thing group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.update_thing_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#update_thing_group)
        """

    async def update_thing_groups_for_thing(
        self,
        *,
        thingName: str = ...,
        thingGroupsToAdd: Sequence[str] = ...,
        thingGroupsToRemove: Sequence[str] = ...,
        overrideDynamicGroups: bool = ...
    ) -> Dict[str, Any]:
        """
        Updates the groups to which the thing belongs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.update_thing_groups_for_thing)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#update_thing_groups_for_thing)
        """

    async def update_topic_rule_destination(
        self, *, arn: str, status: TopicRuleDestinationStatusType
    ) -> Dict[str, Any]:
        """
        Updates a topic rule destination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.update_topic_rule_destination)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#update_topic_rule_destination)
        """

    async def validate_security_profile_behaviors(
        self, *, behaviors: Sequence["BehaviorTypeDef"]
    ) -> ValidateSecurityProfileBehaviorsResponseTypeDef:
        """
        Validates a Device Defender security profile behaviors specification.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.validate_security_profile_behaviors)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#validate_security_profile_behaviors)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_behavior_model_training_summaries"]
    ) -> GetBehaviorModelTrainingSummariesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_active_violations"]
    ) -> ListActiveViolationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_attached_policies"]
    ) -> ListAttachedPoliciesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_audit_findings"]
    ) -> ListAuditFindingsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_audit_mitigation_actions_executions"]
    ) -> ListAuditMitigationActionsExecutionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_audit_mitigation_actions_tasks"]
    ) -> ListAuditMitigationActionsTasksPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_audit_suppressions"]
    ) -> ListAuditSuppressionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_audit_tasks"]) -> ListAuditTasksPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_authorizers"]
    ) -> ListAuthorizersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_billing_groups"]
    ) -> ListBillingGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_ca_certificates"]
    ) -> ListCACertificatesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_certificates"]
    ) -> ListCertificatesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_certificates_by_ca"]
    ) -> ListCertificatesByCAPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_custom_metrics"]
    ) -> ListCustomMetricsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_detect_mitigation_actions_executions"]
    ) -> ListDetectMitigationActionsExecutionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_detect_mitigation_actions_tasks"]
    ) -> ListDetectMitigationActionsTasksPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_dimensions"]) -> ListDimensionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_domain_configurations"]
    ) -> ListDomainConfigurationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_fleet_metrics"]
    ) -> ListFleetMetricsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_indices"]) -> ListIndicesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_job_executions_for_job"]
    ) -> ListJobExecutionsForJobPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_job_executions_for_thing"]
    ) -> ListJobExecutionsForThingPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_job_templates"]
    ) -> ListJobTemplatesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_jobs"]) -> ListJobsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_mitigation_actions"]
    ) -> ListMitigationActionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_ota_updates"]) -> ListOTAUpdatesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_outgoing_certificates"]
    ) -> ListOutgoingCertificatesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_policies"]) -> ListPoliciesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_policy_principals"]
    ) -> ListPolicyPrincipalsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_principal_policies"]
    ) -> ListPrincipalPoliciesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_principal_things"]
    ) -> ListPrincipalThingsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_provisioning_template_versions"]
    ) -> ListProvisioningTemplateVersionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_provisioning_templates"]
    ) -> ListProvisioningTemplatesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_role_aliases"]
    ) -> ListRoleAliasesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_scheduled_audits"]
    ) -> ListScheduledAuditsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_security_profiles"]
    ) -> ListSecurityProfilesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_security_profiles_for_target"]
    ) -> ListSecurityProfilesForTargetPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_streams"]) -> ListStreamsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_tags_for_resource"]
    ) -> ListTagsForResourcePaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_targets_for_policy"]
    ) -> ListTargetsForPolicyPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_targets_for_security_profile"]
    ) -> ListTargetsForSecurityProfilePaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_thing_groups"]
    ) -> ListThingGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_thing_groups_for_thing"]
    ) -> ListThingGroupsForThingPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_thing_principals"]
    ) -> ListThingPrincipalsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_thing_registration_task_reports"]
    ) -> ListThingRegistrationTaskReportsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_thing_registration_tasks"]
    ) -> ListThingRegistrationTasksPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_thing_types"]) -> ListThingTypesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_things"]) -> ListThingsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_things_in_billing_group"]
    ) -> ListThingsInBillingGroupPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_things_in_thing_group"]
    ) -> ListThingsInThingGroupPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_topic_rule_destinations"]
    ) -> ListTopicRuleDestinationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_topic_rules"]) -> ListTopicRulesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_v2_logging_levels"]
    ) -> ListV2LoggingLevelsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_violation_events"]
    ) -> ListViolationEventsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/#get_paginator)
        """

    async def __aenter__(self) -> "IoTClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/client/)
        """
