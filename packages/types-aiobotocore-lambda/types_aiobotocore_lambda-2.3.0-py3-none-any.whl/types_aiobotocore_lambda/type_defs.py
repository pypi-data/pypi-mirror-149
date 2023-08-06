"""
Type annotations for lambda service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/type_defs/)

Usage::

    ```python
    from types_aiobotocore_lambda.type_defs import AccountLimitTypeDef

    data: AccountLimitTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    ArchitectureType,
    CodeSigningPolicyType,
    EventSourcePositionType,
    InvocationTypeType,
    LastUpdateStatusReasonCodeType,
    LastUpdateStatusType,
    LogTypeType,
    PackageTypeType,
    ProvisionedConcurrencyStatusEnumType,
    RuntimeType,
    SourceAccessTypeType,
    StateReasonCodeType,
    StateType,
    TracingModeType,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "AccountLimitTypeDef",
    "AccountUsageTypeDef",
    "AddLayerVersionPermissionRequestRequestTypeDef",
    "AddLayerVersionPermissionResponseTypeDef",
    "AddPermissionRequestRequestTypeDef",
    "AddPermissionResponseTypeDef",
    "AliasConfigurationResponseMetadataTypeDef",
    "AliasConfigurationTypeDef",
    "AliasRoutingConfigurationTypeDef",
    "AllowedPublishersTypeDef",
    "CodeSigningConfigTypeDef",
    "CodeSigningPoliciesTypeDef",
    "ConcurrencyResponseMetadataTypeDef",
    "ConcurrencyTypeDef",
    "CreateAliasRequestRequestTypeDef",
    "CreateCodeSigningConfigRequestRequestTypeDef",
    "CreateCodeSigningConfigResponseTypeDef",
    "CreateEventSourceMappingRequestRequestTypeDef",
    "CreateFunctionRequestRequestTypeDef",
    "DeadLetterConfigTypeDef",
    "DeleteAliasRequestRequestTypeDef",
    "DeleteCodeSigningConfigRequestRequestTypeDef",
    "DeleteEventSourceMappingRequestRequestTypeDef",
    "DeleteFunctionCodeSigningConfigRequestRequestTypeDef",
    "DeleteFunctionConcurrencyRequestRequestTypeDef",
    "DeleteFunctionEventInvokeConfigRequestRequestTypeDef",
    "DeleteFunctionRequestRequestTypeDef",
    "DeleteLayerVersionRequestRequestTypeDef",
    "DeleteProvisionedConcurrencyConfigRequestRequestTypeDef",
    "DestinationConfigTypeDef",
    "EnvironmentErrorTypeDef",
    "EnvironmentResponseTypeDef",
    "EnvironmentTypeDef",
    "EventSourceMappingConfigurationResponseMetadataTypeDef",
    "EventSourceMappingConfigurationTypeDef",
    "FileSystemConfigTypeDef",
    "FilterCriteriaTypeDef",
    "FilterTypeDef",
    "FunctionCodeLocationTypeDef",
    "FunctionCodeTypeDef",
    "FunctionConfigurationResponseMetadataTypeDef",
    "FunctionConfigurationTypeDef",
    "FunctionEventInvokeConfigResponseMetadataTypeDef",
    "FunctionEventInvokeConfigTypeDef",
    "GetAccountSettingsResponseTypeDef",
    "GetAliasRequestRequestTypeDef",
    "GetCodeSigningConfigRequestRequestTypeDef",
    "GetCodeSigningConfigResponseTypeDef",
    "GetEventSourceMappingRequestRequestTypeDef",
    "GetFunctionCodeSigningConfigRequestRequestTypeDef",
    "GetFunctionCodeSigningConfigResponseTypeDef",
    "GetFunctionConcurrencyRequestRequestTypeDef",
    "GetFunctionConcurrencyResponseTypeDef",
    "GetFunctionConfigurationRequestFunctionActiveWaitTypeDef",
    "GetFunctionConfigurationRequestFunctionUpdatedWaitTypeDef",
    "GetFunctionConfigurationRequestRequestTypeDef",
    "GetFunctionEventInvokeConfigRequestRequestTypeDef",
    "GetFunctionRequestFunctionActiveV2WaitTypeDef",
    "GetFunctionRequestFunctionExistsWaitTypeDef",
    "GetFunctionRequestFunctionUpdatedV2WaitTypeDef",
    "GetFunctionRequestRequestTypeDef",
    "GetFunctionResponseTypeDef",
    "GetLayerVersionByArnRequestRequestTypeDef",
    "GetLayerVersionPolicyRequestRequestTypeDef",
    "GetLayerVersionPolicyResponseTypeDef",
    "GetLayerVersionRequestRequestTypeDef",
    "GetLayerVersionResponseTypeDef",
    "GetPolicyRequestRequestTypeDef",
    "GetPolicyResponseTypeDef",
    "GetProvisionedConcurrencyConfigRequestRequestTypeDef",
    "GetProvisionedConcurrencyConfigResponseTypeDef",
    "ImageConfigErrorTypeDef",
    "ImageConfigResponseTypeDef",
    "ImageConfigTypeDef",
    "InvocationRequestRequestTypeDef",
    "InvocationResponseTypeDef",
    "InvokeAsyncRequestRequestTypeDef",
    "InvokeAsyncResponseTypeDef",
    "LayerTypeDef",
    "LayerVersionContentInputTypeDef",
    "LayerVersionContentOutputTypeDef",
    "LayerVersionsListItemTypeDef",
    "LayersListItemTypeDef",
    "ListAliasesRequestListAliasesPaginateTypeDef",
    "ListAliasesRequestRequestTypeDef",
    "ListAliasesResponseTypeDef",
    "ListCodeSigningConfigsRequestListCodeSigningConfigsPaginateTypeDef",
    "ListCodeSigningConfigsRequestRequestTypeDef",
    "ListCodeSigningConfigsResponseTypeDef",
    "ListEventSourceMappingsRequestListEventSourceMappingsPaginateTypeDef",
    "ListEventSourceMappingsRequestRequestTypeDef",
    "ListEventSourceMappingsResponseTypeDef",
    "ListFunctionEventInvokeConfigsRequestListFunctionEventInvokeConfigsPaginateTypeDef",
    "ListFunctionEventInvokeConfigsRequestRequestTypeDef",
    "ListFunctionEventInvokeConfigsResponseTypeDef",
    "ListFunctionsByCodeSigningConfigRequestListFunctionsByCodeSigningConfigPaginateTypeDef",
    "ListFunctionsByCodeSigningConfigRequestRequestTypeDef",
    "ListFunctionsByCodeSigningConfigResponseTypeDef",
    "ListFunctionsRequestListFunctionsPaginateTypeDef",
    "ListFunctionsRequestRequestTypeDef",
    "ListFunctionsResponseTypeDef",
    "ListLayerVersionsRequestListLayerVersionsPaginateTypeDef",
    "ListLayerVersionsRequestRequestTypeDef",
    "ListLayerVersionsResponseTypeDef",
    "ListLayersRequestListLayersPaginateTypeDef",
    "ListLayersRequestRequestTypeDef",
    "ListLayersResponseTypeDef",
    "ListProvisionedConcurrencyConfigsRequestListProvisionedConcurrencyConfigsPaginateTypeDef",
    "ListProvisionedConcurrencyConfigsRequestRequestTypeDef",
    "ListProvisionedConcurrencyConfigsResponseTypeDef",
    "ListTagsRequestRequestTypeDef",
    "ListTagsResponseTypeDef",
    "ListVersionsByFunctionRequestListVersionsByFunctionPaginateTypeDef",
    "ListVersionsByFunctionRequestRequestTypeDef",
    "ListVersionsByFunctionResponseTypeDef",
    "OnFailureTypeDef",
    "OnSuccessTypeDef",
    "PaginatorConfigTypeDef",
    "ProvisionedConcurrencyConfigListItemTypeDef",
    "PublishLayerVersionRequestRequestTypeDef",
    "PublishLayerVersionResponseTypeDef",
    "PublishVersionRequestRequestTypeDef",
    "PutFunctionCodeSigningConfigRequestRequestTypeDef",
    "PutFunctionCodeSigningConfigResponseTypeDef",
    "PutFunctionConcurrencyRequestRequestTypeDef",
    "PutFunctionEventInvokeConfigRequestRequestTypeDef",
    "PutProvisionedConcurrencyConfigRequestRequestTypeDef",
    "PutProvisionedConcurrencyConfigResponseTypeDef",
    "RemoveLayerVersionPermissionRequestRequestTypeDef",
    "RemovePermissionRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "SelfManagedEventSourceTypeDef",
    "SourceAccessConfigurationTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TracingConfigResponseTypeDef",
    "TracingConfigTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateAliasRequestRequestTypeDef",
    "UpdateCodeSigningConfigRequestRequestTypeDef",
    "UpdateCodeSigningConfigResponseTypeDef",
    "UpdateEventSourceMappingRequestRequestTypeDef",
    "UpdateFunctionCodeRequestRequestTypeDef",
    "UpdateFunctionConfigurationRequestRequestTypeDef",
    "UpdateFunctionEventInvokeConfigRequestRequestTypeDef",
    "VpcConfigResponseTypeDef",
    "VpcConfigTypeDef",
    "WaiterConfigTypeDef",
)

AccountLimitTypeDef = TypedDict(
    "AccountLimitTypeDef",
    {
        "TotalCodeSize": int,
        "CodeSizeUnzipped": int,
        "CodeSizeZipped": int,
        "ConcurrentExecutions": int,
        "UnreservedConcurrentExecutions": int,
    },
    total=False,
)

AccountUsageTypeDef = TypedDict(
    "AccountUsageTypeDef",
    {
        "TotalCodeSize": int,
        "FunctionCount": int,
    },
    total=False,
)

_RequiredAddLayerVersionPermissionRequestRequestTypeDef = TypedDict(
    "_RequiredAddLayerVersionPermissionRequestRequestTypeDef",
    {
        "LayerName": str,
        "VersionNumber": int,
        "StatementId": str,
        "Action": str,
        "Principal": str,
    },
)
_OptionalAddLayerVersionPermissionRequestRequestTypeDef = TypedDict(
    "_OptionalAddLayerVersionPermissionRequestRequestTypeDef",
    {
        "OrganizationId": str,
        "RevisionId": str,
    },
    total=False,
)


class AddLayerVersionPermissionRequestRequestTypeDef(
    _RequiredAddLayerVersionPermissionRequestRequestTypeDef,
    _OptionalAddLayerVersionPermissionRequestRequestTypeDef,
):
    pass


AddLayerVersionPermissionResponseTypeDef = TypedDict(
    "AddLayerVersionPermissionResponseTypeDef",
    {
        "Statement": str,
        "RevisionId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredAddPermissionRequestRequestTypeDef = TypedDict(
    "_RequiredAddPermissionRequestRequestTypeDef",
    {
        "FunctionName": str,
        "StatementId": str,
        "Action": str,
        "Principal": str,
    },
)
_OptionalAddPermissionRequestRequestTypeDef = TypedDict(
    "_OptionalAddPermissionRequestRequestTypeDef",
    {
        "SourceArn": str,
        "SourceAccount": str,
        "EventSourceToken": str,
        "Qualifier": str,
        "RevisionId": str,
        "PrincipalOrgID": str,
    },
    total=False,
)


class AddPermissionRequestRequestTypeDef(
    _RequiredAddPermissionRequestRequestTypeDef, _OptionalAddPermissionRequestRequestTypeDef
):
    pass


AddPermissionResponseTypeDef = TypedDict(
    "AddPermissionResponseTypeDef",
    {
        "Statement": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

AliasConfigurationResponseMetadataTypeDef = TypedDict(
    "AliasConfigurationResponseMetadataTypeDef",
    {
        "AliasArn": str,
        "Name": str,
        "FunctionVersion": str,
        "Description": str,
        "RoutingConfig": "AliasRoutingConfigurationTypeDef",
        "RevisionId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

AliasConfigurationTypeDef = TypedDict(
    "AliasConfigurationTypeDef",
    {
        "AliasArn": str,
        "Name": str,
        "FunctionVersion": str,
        "Description": str,
        "RoutingConfig": "AliasRoutingConfigurationTypeDef",
        "RevisionId": str,
    },
    total=False,
)

AliasRoutingConfigurationTypeDef = TypedDict(
    "AliasRoutingConfigurationTypeDef",
    {
        "AdditionalVersionWeights": Mapping[str, float],
    },
    total=False,
)

AllowedPublishersTypeDef = TypedDict(
    "AllowedPublishersTypeDef",
    {
        "SigningProfileVersionArns": Sequence[str],
    },
)

_RequiredCodeSigningConfigTypeDef = TypedDict(
    "_RequiredCodeSigningConfigTypeDef",
    {
        "CodeSigningConfigId": str,
        "CodeSigningConfigArn": str,
        "AllowedPublishers": "AllowedPublishersTypeDef",
        "CodeSigningPolicies": "CodeSigningPoliciesTypeDef",
        "LastModified": str,
    },
)
_OptionalCodeSigningConfigTypeDef = TypedDict(
    "_OptionalCodeSigningConfigTypeDef",
    {
        "Description": str,
    },
    total=False,
)


class CodeSigningConfigTypeDef(
    _RequiredCodeSigningConfigTypeDef, _OptionalCodeSigningConfigTypeDef
):
    pass


CodeSigningPoliciesTypeDef = TypedDict(
    "CodeSigningPoliciesTypeDef",
    {
        "UntrustedArtifactOnDeployment": CodeSigningPolicyType,
    },
    total=False,
)

ConcurrencyResponseMetadataTypeDef = TypedDict(
    "ConcurrencyResponseMetadataTypeDef",
    {
        "ReservedConcurrentExecutions": int,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ConcurrencyTypeDef = TypedDict(
    "ConcurrencyTypeDef",
    {
        "ReservedConcurrentExecutions": int,
    },
    total=False,
)

_RequiredCreateAliasRequestRequestTypeDef = TypedDict(
    "_RequiredCreateAliasRequestRequestTypeDef",
    {
        "FunctionName": str,
        "Name": str,
        "FunctionVersion": str,
    },
)
_OptionalCreateAliasRequestRequestTypeDef = TypedDict(
    "_OptionalCreateAliasRequestRequestTypeDef",
    {
        "Description": str,
        "RoutingConfig": "AliasRoutingConfigurationTypeDef",
    },
    total=False,
)


class CreateAliasRequestRequestTypeDef(
    _RequiredCreateAliasRequestRequestTypeDef, _OptionalCreateAliasRequestRequestTypeDef
):
    pass


_RequiredCreateCodeSigningConfigRequestRequestTypeDef = TypedDict(
    "_RequiredCreateCodeSigningConfigRequestRequestTypeDef",
    {
        "AllowedPublishers": "AllowedPublishersTypeDef",
    },
)
_OptionalCreateCodeSigningConfigRequestRequestTypeDef = TypedDict(
    "_OptionalCreateCodeSigningConfigRequestRequestTypeDef",
    {
        "Description": str,
        "CodeSigningPolicies": "CodeSigningPoliciesTypeDef",
    },
    total=False,
)


class CreateCodeSigningConfigRequestRequestTypeDef(
    _RequiredCreateCodeSigningConfigRequestRequestTypeDef,
    _OptionalCreateCodeSigningConfigRequestRequestTypeDef,
):
    pass


CreateCodeSigningConfigResponseTypeDef = TypedDict(
    "CreateCodeSigningConfigResponseTypeDef",
    {
        "CodeSigningConfig": "CodeSigningConfigTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateEventSourceMappingRequestRequestTypeDef = TypedDict(
    "_RequiredCreateEventSourceMappingRequestRequestTypeDef",
    {
        "FunctionName": str,
    },
)
_OptionalCreateEventSourceMappingRequestRequestTypeDef = TypedDict(
    "_OptionalCreateEventSourceMappingRequestRequestTypeDef",
    {
        "EventSourceArn": str,
        "Enabled": bool,
        "BatchSize": int,
        "FilterCriteria": "FilterCriteriaTypeDef",
        "MaximumBatchingWindowInSeconds": int,
        "ParallelizationFactor": int,
        "StartingPosition": EventSourcePositionType,
        "StartingPositionTimestamp": Union[datetime, str],
        "DestinationConfig": "DestinationConfigTypeDef",
        "MaximumRecordAgeInSeconds": int,
        "BisectBatchOnFunctionError": bool,
        "MaximumRetryAttempts": int,
        "TumblingWindowInSeconds": int,
        "Topics": Sequence[str],
        "Queues": Sequence[str],
        "SourceAccessConfigurations": Sequence["SourceAccessConfigurationTypeDef"],
        "SelfManagedEventSource": "SelfManagedEventSourceTypeDef",
        "FunctionResponseTypes": Sequence[Literal["ReportBatchItemFailures"]],
    },
    total=False,
)


class CreateEventSourceMappingRequestRequestTypeDef(
    _RequiredCreateEventSourceMappingRequestRequestTypeDef,
    _OptionalCreateEventSourceMappingRequestRequestTypeDef,
):
    pass


_RequiredCreateFunctionRequestRequestTypeDef = TypedDict(
    "_RequiredCreateFunctionRequestRequestTypeDef",
    {
        "FunctionName": str,
        "Role": str,
        "Code": "FunctionCodeTypeDef",
    },
)
_OptionalCreateFunctionRequestRequestTypeDef = TypedDict(
    "_OptionalCreateFunctionRequestRequestTypeDef",
    {
        "Runtime": RuntimeType,
        "Handler": str,
        "Description": str,
        "Timeout": int,
        "MemorySize": int,
        "Publish": bool,
        "VpcConfig": "VpcConfigTypeDef",
        "PackageType": PackageTypeType,
        "DeadLetterConfig": "DeadLetterConfigTypeDef",
        "Environment": "EnvironmentTypeDef",
        "KMSKeyArn": str,
        "TracingConfig": "TracingConfigTypeDef",
        "Tags": Mapping[str, str],
        "Layers": Sequence[str],
        "FileSystemConfigs": Sequence["FileSystemConfigTypeDef"],
        "ImageConfig": "ImageConfigTypeDef",
        "CodeSigningConfigArn": str,
        "Architectures": Sequence[ArchitectureType],
    },
    total=False,
)


class CreateFunctionRequestRequestTypeDef(
    _RequiredCreateFunctionRequestRequestTypeDef, _OptionalCreateFunctionRequestRequestTypeDef
):
    pass


DeadLetterConfigTypeDef = TypedDict(
    "DeadLetterConfigTypeDef",
    {
        "TargetArn": str,
    },
    total=False,
)

DeleteAliasRequestRequestTypeDef = TypedDict(
    "DeleteAliasRequestRequestTypeDef",
    {
        "FunctionName": str,
        "Name": str,
    },
)

DeleteCodeSigningConfigRequestRequestTypeDef = TypedDict(
    "DeleteCodeSigningConfigRequestRequestTypeDef",
    {
        "CodeSigningConfigArn": str,
    },
)

DeleteEventSourceMappingRequestRequestTypeDef = TypedDict(
    "DeleteEventSourceMappingRequestRequestTypeDef",
    {
        "UUID": str,
    },
)

DeleteFunctionCodeSigningConfigRequestRequestTypeDef = TypedDict(
    "DeleteFunctionCodeSigningConfigRequestRequestTypeDef",
    {
        "FunctionName": str,
    },
)

DeleteFunctionConcurrencyRequestRequestTypeDef = TypedDict(
    "DeleteFunctionConcurrencyRequestRequestTypeDef",
    {
        "FunctionName": str,
    },
)

_RequiredDeleteFunctionEventInvokeConfigRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteFunctionEventInvokeConfigRequestRequestTypeDef",
    {
        "FunctionName": str,
    },
)
_OptionalDeleteFunctionEventInvokeConfigRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteFunctionEventInvokeConfigRequestRequestTypeDef",
    {
        "Qualifier": str,
    },
    total=False,
)


class DeleteFunctionEventInvokeConfigRequestRequestTypeDef(
    _RequiredDeleteFunctionEventInvokeConfigRequestRequestTypeDef,
    _OptionalDeleteFunctionEventInvokeConfigRequestRequestTypeDef,
):
    pass


_RequiredDeleteFunctionRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteFunctionRequestRequestTypeDef",
    {
        "FunctionName": str,
    },
)
_OptionalDeleteFunctionRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteFunctionRequestRequestTypeDef",
    {
        "Qualifier": str,
    },
    total=False,
)


class DeleteFunctionRequestRequestTypeDef(
    _RequiredDeleteFunctionRequestRequestTypeDef, _OptionalDeleteFunctionRequestRequestTypeDef
):
    pass


DeleteLayerVersionRequestRequestTypeDef = TypedDict(
    "DeleteLayerVersionRequestRequestTypeDef",
    {
        "LayerName": str,
        "VersionNumber": int,
    },
)

DeleteProvisionedConcurrencyConfigRequestRequestTypeDef = TypedDict(
    "DeleteProvisionedConcurrencyConfigRequestRequestTypeDef",
    {
        "FunctionName": str,
        "Qualifier": str,
    },
)

DestinationConfigTypeDef = TypedDict(
    "DestinationConfigTypeDef",
    {
        "OnSuccess": "OnSuccessTypeDef",
        "OnFailure": "OnFailureTypeDef",
    },
    total=False,
)

EnvironmentErrorTypeDef = TypedDict(
    "EnvironmentErrorTypeDef",
    {
        "ErrorCode": str,
        "Message": str,
    },
    total=False,
)

EnvironmentResponseTypeDef = TypedDict(
    "EnvironmentResponseTypeDef",
    {
        "Variables": Dict[str, str],
        "Error": "EnvironmentErrorTypeDef",
    },
    total=False,
)

EnvironmentTypeDef = TypedDict(
    "EnvironmentTypeDef",
    {
        "Variables": Mapping[str, str],
    },
    total=False,
)

EventSourceMappingConfigurationResponseMetadataTypeDef = TypedDict(
    "EventSourceMappingConfigurationResponseMetadataTypeDef",
    {
        "UUID": str,
        "StartingPosition": EventSourcePositionType,
        "StartingPositionTimestamp": datetime,
        "BatchSize": int,
        "MaximumBatchingWindowInSeconds": int,
        "ParallelizationFactor": int,
        "EventSourceArn": str,
        "FilterCriteria": "FilterCriteriaTypeDef",
        "FunctionArn": str,
        "LastModified": datetime,
        "LastProcessingResult": str,
        "State": str,
        "StateTransitionReason": str,
        "DestinationConfig": "DestinationConfigTypeDef",
        "Topics": List[str],
        "Queues": List[str],
        "SourceAccessConfigurations": List["SourceAccessConfigurationTypeDef"],
        "SelfManagedEventSource": "SelfManagedEventSourceTypeDef",
        "MaximumRecordAgeInSeconds": int,
        "BisectBatchOnFunctionError": bool,
        "MaximumRetryAttempts": int,
        "TumblingWindowInSeconds": int,
        "FunctionResponseTypes": List[Literal["ReportBatchItemFailures"]],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

EventSourceMappingConfigurationTypeDef = TypedDict(
    "EventSourceMappingConfigurationTypeDef",
    {
        "UUID": str,
        "StartingPosition": EventSourcePositionType,
        "StartingPositionTimestamp": datetime,
        "BatchSize": int,
        "MaximumBatchingWindowInSeconds": int,
        "ParallelizationFactor": int,
        "EventSourceArn": str,
        "FilterCriteria": "FilterCriteriaTypeDef",
        "FunctionArn": str,
        "LastModified": datetime,
        "LastProcessingResult": str,
        "State": str,
        "StateTransitionReason": str,
        "DestinationConfig": "DestinationConfigTypeDef",
        "Topics": List[str],
        "Queues": List[str],
        "SourceAccessConfigurations": List["SourceAccessConfigurationTypeDef"],
        "SelfManagedEventSource": "SelfManagedEventSourceTypeDef",
        "MaximumRecordAgeInSeconds": int,
        "BisectBatchOnFunctionError": bool,
        "MaximumRetryAttempts": int,
        "TumblingWindowInSeconds": int,
        "FunctionResponseTypes": List[Literal["ReportBatchItemFailures"]],
    },
    total=False,
)

FileSystemConfigTypeDef = TypedDict(
    "FileSystemConfigTypeDef",
    {
        "Arn": str,
        "LocalMountPath": str,
    },
)

FilterCriteriaTypeDef = TypedDict(
    "FilterCriteriaTypeDef",
    {
        "Filters": Sequence["FilterTypeDef"],
    },
    total=False,
)

FilterTypeDef = TypedDict(
    "FilterTypeDef",
    {
        "Pattern": str,
    },
    total=False,
)

FunctionCodeLocationTypeDef = TypedDict(
    "FunctionCodeLocationTypeDef",
    {
        "RepositoryType": str,
        "Location": str,
        "ImageUri": str,
        "ResolvedImageUri": str,
    },
    total=False,
)

FunctionCodeTypeDef = TypedDict(
    "FunctionCodeTypeDef",
    {
        "ZipFile": Union[str, bytes, IO[Any], StreamingBody],
        "S3Bucket": str,
        "S3Key": str,
        "S3ObjectVersion": str,
        "ImageUri": str,
    },
    total=False,
)

FunctionConfigurationResponseMetadataTypeDef = TypedDict(
    "FunctionConfigurationResponseMetadataTypeDef",
    {
        "FunctionName": str,
        "FunctionArn": str,
        "Runtime": RuntimeType,
        "Role": str,
        "Handler": str,
        "CodeSize": int,
        "Description": str,
        "Timeout": int,
        "MemorySize": int,
        "LastModified": str,
        "CodeSha256": str,
        "Version": str,
        "VpcConfig": "VpcConfigResponseTypeDef",
        "DeadLetterConfig": "DeadLetterConfigTypeDef",
        "Environment": "EnvironmentResponseTypeDef",
        "KMSKeyArn": str,
        "TracingConfig": "TracingConfigResponseTypeDef",
        "MasterArn": str,
        "RevisionId": str,
        "Layers": List["LayerTypeDef"],
        "State": StateType,
        "StateReason": str,
        "StateReasonCode": StateReasonCodeType,
        "LastUpdateStatus": LastUpdateStatusType,
        "LastUpdateStatusReason": str,
        "LastUpdateStatusReasonCode": LastUpdateStatusReasonCodeType,
        "FileSystemConfigs": List["FileSystemConfigTypeDef"],
        "PackageType": PackageTypeType,
        "ImageConfigResponse": "ImageConfigResponseTypeDef",
        "SigningProfileVersionArn": str,
        "SigningJobArn": str,
        "Architectures": List[ArchitectureType],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

FunctionConfigurationTypeDef = TypedDict(
    "FunctionConfigurationTypeDef",
    {
        "FunctionName": str,
        "FunctionArn": str,
        "Runtime": RuntimeType,
        "Role": str,
        "Handler": str,
        "CodeSize": int,
        "Description": str,
        "Timeout": int,
        "MemorySize": int,
        "LastModified": str,
        "CodeSha256": str,
        "Version": str,
        "VpcConfig": "VpcConfigResponseTypeDef",
        "DeadLetterConfig": "DeadLetterConfigTypeDef",
        "Environment": "EnvironmentResponseTypeDef",
        "KMSKeyArn": str,
        "TracingConfig": "TracingConfigResponseTypeDef",
        "MasterArn": str,
        "RevisionId": str,
        "Layers": List["LayerTypeDef"],
        "State": StateType,
        "StateReason": str,
        "StateReasonCode": StateReasonCodeType,
        "LastUpdateStatus": LastUpdateStatusType,
        "LastUpdateStatusReason": str,
        "LastUpdateStatusReasonCode": LastUpdateStatusReasonCodeType,
        "FileSystemConfigs": List["FileSystemConfigTypeDef"],
        "PackageType": PackageTypeType,
        "ImageConfigResponse": "ImageConfigResponseTypeDef",
        "SigningProfileVersionArn": str,
        "SigningJobArn": str,
        "Architectures": List[ArchitectureType],
    },
    total=False,
)

FunctionEventInvokeConfigResponseMetadataTypeDef = TypedDict(
    "FunctionEventInvokeConfigResponseMetadataTypeDef",
    {
        "LastModified": datetime,
        "FunctionArn": str,
        "MaximumRetryAttempts": int,
        "MaximumEventAgeInSeconds": int,
        "DestinationConfig": "DestinationConfigTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

FunctionEventInvokeConfigTypeDef = TypedDict(
    "FunctionEventInvokeConfigTypeDef",
    {
        "LastModified": datetime,
        "FunctionArn": str,
        "MaximumRetryAttempts": int,
        "MaximumEventAgeInSeconds": int,
        "DestinationConfig": "DestinationConfigTypeDef",
    },
    total=False,
)

GetAccountSettingsResponseTypeDef = TypedDict(
    "GetAccountSettingsResponseTypeDef",
    {
        "AccountLimit": "AccountLimitTypeDef",
        "AccountUsage": "AccountUsageTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetAliasRequestRequestTypeDef = TypedDict(
    "GetAliasRequestRequestTypeDef",
    {
        "FunctionName": str,
        "Name": str,
    },
)

GetCodeSigningConfigRequestRequestTypeDef = TypedDict(
    "GetCodeSigningConfigRequestRequestTypeDef",
    {
        "CodeSigningConfigArn": str,
    },
)

GetCodeSigningConfigResponseTypeDef = TypedDict(
    "GetCodeSigningConfigResponseTypeDef",
    {
        "CodeSigningConfig": "CodeSigningConfigTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetEventSourceMappingRequestRequestTypeDef = TypedDict(
    "GetEventSourceMappingRequestRequestTypeDef",
    {
        "UUID": str,
    },
)

GetFunctionCodeSigningConfigRequestRequestTypeDef = TypedDict(
    "GetFunctionCodeSigningConfigRequestRequestTypeDef",
    {
        "FunctionName": str,
    },
)

GetFunctionCodeSigningConfigResponseTypeDef = TypedDict(
    "GetFunctionCodeSigningConfigResponseTypeDef",
    {
        "CodeSigningConfigArn": str,
        "FunctionName": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetFunctionConcurrencyRequestRequestTypeDef = TypedDict(
    "GetFunctionConcurrencyRequestRequestTypeDef",
    {
        "FunctionName": str,
    },
)

GetFunctionConcurrencyResponseTypeDef = TypedDict(
    "GetFunctionConcurrencyResponseTypeDef",
    {
        "ReservedConcurrentExecutions": int,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredGetFunctionConfigurationRequestFunctionActiveWaitTypeDef = TypedDict(
    "_RequiredGetFunctionConfigurationRequestFunctionActiveWaitTypeDef",
    {
        "FunctionName": str,
    },
)
_OptionalGetFunctionConfigurationRequestFunctionActiveWaitTypeDef = TypedDict(
    "_OptionalGetFunctionConfigurationRequestFunctionActiveWaitTypeDef",
    {
        "Qualifier": str,
        "WaiterConfig": "WaiterConfigTypeDef",
    },
    total=False,
)


class GetFunctionConfigurationRequestFunctionActiveWaitTypeDef(
    _RequiredGetFunctionConfigurationRequestFunctionActiveWaitTypeDef,
    _OptionalGetFunctionConfigurationRequestFunctionActiveWaitTypeDef,
):
    pass


_RequiredGetFunctionConfigurationRequestFunctionUpdatedWaitTypeDef = TypedDict(
    "_RequiredGetFunctionConfigurationRequestFunctionUpdatedWaitTypeDef",
    {
        "FunctionName": str,
    },
)
_OptionalGetFunctionConfigurationRequestFunctionUpdatedWaitTypeDef = TypedDict(
    "_OptionalGetFunctionConfigurationRequestFunctionUpdatedWaitTypeDef",
    {
        "Qualifier": str,
        "WaiterConfig": "WaiterConfigTypeDef",
    },
    total=False,
)


class GetFunctionConfigurationRequestFunctionUpdatedWaitTypeDef(
    _RequiredGetFunctionConfigurationRequestFunctionUpdatedWaitTypeDef,
    _OptionalGetFunctionConfigurationRequestFunctionUpdatedWaitTypeDef,
):
    pass


_RequiredGetFunctionConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredGetFunctionConfigurationRequestRequestTypeDef",
    {
        "FunctionName": str,
    },
)
_OptionalGetFunctionConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalGetFunctionConfigurationRequestRequestTypeDef",
    {
        "Qualifier": str,
    },
    total=False,
)


class GetFunctionConfigurationRequestRequestTypeDef(
    _RequiredGetFunctionConfigurationRequestRequestTypeDef,
    _OptionalGetFunctionConfigurationRequestRequestTypeDef,
):
    pass


_RequiredGetFunctionEventInvokeConfigRequestRequestTypeDef = TypedDict(
    "_RequiredGetFunctionEventInvokeConfigRequestRequestTypeDef",
    {
        "FunctionName": str,
    },
)
_OptionalGetFunctionEventInvokeConfigRequestRequestTypeDef = TypedDict(
    "_OptionalGetFunctionEventInvokeConfigRequestRequestTypeDef",
    {
        "Qualifier": str,
    },
    total=False,
)


class GetFunctionEventInvokeConfigRequestRequestTypeDef(
    _RequiredGetFunctionEventInvokeConfigRequestRequestTypeDef,
    _OptionalGetFunctionEventInvokeConfigRequestRequestTypeDef,
):
    pass


_RequiredGetFunctionRequestFunctionActiveV2WaitTypeDef = TypedDict(
    "_RequiredGetFunctionRequestFunctionActiveV2WaitTypeDef",
    {
        "FunctionName": str,
    },
)
_OptionalGetFunctionRequestFunctionActiveV2WaitTypeDef = TypedDict(
    "_OptionalGetFunctionRequestFunctionActiveV2WaitTypeDef",
    {
        "Qualifier": str,
        "WaiterConfig": "WaiterConfigTypeDef",
    },
    total=False,
)


class GetFunctionRequestFunctionActiveV2WaitTypeDef(
    _RequiredGetFunctionRequestFunctionActiveV2WaitTypeDef,
    _OptionalGetFunctionRequestFunctionActiveV2WaitTypeDef,
):
    pass


_RequiredGetFunctionRequestFunctionExistsWaitTypeDef = TypedDict(
    "_RequiredGetFunctionRequestFunctionExistsWaitTypeDef",
    {
        "FunctionName": str,
    },
)
_OptionalGetFunctionRequestFunctionExistsWaitTypeDef = TypedDict(
    "_OptionalGetFunctionRequestFunctionExistsWaitTypeDef",
    {
        "Qualifier": str,
        "WaiterConfig": "WaiterConfigTypeDef",
    },
    total=False,
)


class GetFunctionRequestFunctionExistsWaitTypeDef(
    _RequiredGetFunctionRequestFunctionExistsWaitTypeDef,
    _OptionalGetFunctionRequestFunctionExistsWaitTypeDef,
):
    pass


_RequiredGetFunctionRequestFunctionUpdatedV2WaitTypeDef = TypedDict(
    "_RequiredGetFunctionRequestFunctionUpdatedV2WaitTypeDef",
    {
        "FunctionName": str,
    },
)
_OptionalGetFunctionRequestFunctionUpdatedV2WaitTypeDef = TypedDict(
    "_OptionalGetFunctionRequestFunctionUpdatedV2WaitTypeDef",
    {
        "Qualifier": str,
        "WaiterConfig": "WaiterConfigTypeDef",
    },
    total=False,
)


class GetFunctionRequestFunctionUpdatedV2WaitTypeDef(
    _RequiredGetFunctionRequestFunctionUpdatedV2WaitTypeDef,
    _OptionalGetFunctionRequestFunctionUpdatedV2WaitTypeDef,
):
    pass


_RequiredGetFunctionRequestRequestTypeDef = TypedDict(
    "_RequiredGetFunctionRequestRequestTypeDef",
    {
        "FunctionName": str,
    },
)
_OptionalGetFunctionRequestRequestTypeDef = TypedDict(
    "_OptionalGetFunctionRequestRequestTypeDef",
    {
        "Qualifier": str,
    },
    total=False,
)


class GetFunctionRequestRequestTypeDef(
    _RequiredGetFunctionRequestRequestTypeDef, _OptionalGetFunctionRequestRequestTypeDef
):
    pass


GetFunctionResponseTypeDef = TypedDict(
    "GetFunctionResponseTypeDef",
    {
        "Configuration": "FunctionConfigurationTypeDef",
        "Code": "FunctionCodeLocationTypeDef",
        "Tags": Dict[str, str],
        "Concurrency": "ConcurrencyTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetLayerVersionByArnRequestRequestTypeDef = TypedDict(
    "GetLayerVersionByArnRequestRequestTypeDef",
    {
        "Arn": str,
    },
)

GetLayerVersionPolicyRequestRequestTypeDef = TypedDict(
    "GetLayerVersionPolicyRequestRequestTypeDef",
    {
        "LayerName": str,
        "VersionNumber": int,
    },
)

GetLayerVersionPolicyResponseTypeDef = TypedDict(
    "GetLayerVersionPolicyResponseTypeDef",
    {
        "Policy": str,
        "RevisionId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetLayerVersionRequestRequestTypeDef = TypedDict(
    "GetLayerVersionRequestRequestTypeDef",
    {
        "LayerName": str,
        "VersionNumber": int,
    },
)

GetLayerVersionResponseTypeDef = TypedDict(
    "GetLayerVersionResponseTypeDef",
    {
        "Content": "LayerVersionContentOutputTypeDef",
        "LayerArn": str,
        "LayerVersionArn": str,
        "Description": str,
        "CreatedDate": str,
        "Version": int,
        "CompatibleRuntimes": List[RuntimeType],
        "LicenseInfo": str,
        "CompatibleArchitectures": List[ArchitectureType],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredGetPolicyRequestRequestTypeDef = TypedDict(
    "_RequiredGetPolicyRequestRequestTypeDef",
    {
        "FunctionName": str,
    },
)
_OptionalGetPolicyRequestRequestTypeDef = TypedDict(
    "_OptionalGetPolicyRequestRequestTypeDef",
    {
        "Qualifier": str,
    },
    total=False,
)


class GetPolicyRequestRequestTypeDef(
    _RequiredGetPolicyRequestRequestTypeDef, _OptionalGetPolicyRequestRequestTypeDef
):
    pass


GetPolicyResponseTypeDef = TypedDict(
    "GetPolicyResponseTypeDef",
    {
        "Policy": str,
        "RevisionId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetProvisionedConcurrencyConfigRequestRequestTypeDef = TypedDict(
    "GetProvisionedConcurrencyConfigRequestRequestTypeDef",
    {
        "FunctionName": str,
        "Qualifier": str,
    },
)

GetProvisionedConcurrencyConfigResponseTypeDef = TypedDict(
    "GetProvisionedConcurrencyConfigResponseTypeDef",
    {
        "RequestedProvisionedConcurrentExecutions": int,
        "AvailableProvisionedConcurrentExecutions": int,
        "AllocatedProvisionedConcurrentExecutions": int,
        "Status": ProvisionedConcurrencyStatusEnumType,
        "StatusReason": str,
        "LastModified": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ImageConfigErrorTypeDef = TypedDict(
    "ImageConfigErrorTypeDef",
    {
        "ErrorCode": str,
        "Message": str,
    },
    total=False,
)

ImageConfigResponseTypeDef = TypedDict(
    "ImageConfigResponseTypeDef",
    {
        "ImageConfig": "ImageConfigTypeDef",
        "Error": "ImageConfigErrorTypeDef",
    },
    total=False,
)

ImageConfigTypeDef = TypedDict(
    "ImageConfigTypeDef",
    {
        "EntryPoint": Sequence[str],
        "Command": Sequence[str],
        "WorkingDirectory": str,
    },
    total=False,
)

_RequiredInvocationRequestRequestTypeDef = TypedDict(
    "_RequiredInvocationRequestRequestTypeDef",
    {
        "FunctionName": str,
    },
)
_OptionalInvocationRequestRequestTypeDef = TypedDict(
    "_OptionalInvocationRequestRequestTypeDef",
    {
        "InvocationType": InvocationTypeType,
        "LogType": LogTypeType,
        "ClientContext": str,
        "Payload": Union[str, bytes, IO[Any], StreamingBody],
        "Qualifier": str,
    },
    total=False,
)


class InvocationRequestRequestTypeDef(
    _RequiredInvocationRequestRequestTypeDef, _OptionalInvocationRequestRequestTypeDef
):
    pass


InvocationResponseTypeDef = TypedDict(
    "InvocationResponseTypeDef",
    {
        "StatusCode": int,
        "FunctionError": str,
        "LogResult": str,
        "Payload": IO[bytes],
        "ExecutedVersion": str,
    },
    total=False,
)

InvokeAsyncRequestRequestTypeDef = TypedDict(
    "InvokeAsyncRequestRequestTypeDef",
    {
        "FunctionName": str,
        "InvokeArgs": Union[str, bytes, IO[Any], StreamingBody],
    },
)

InvokeAsyncResponseTypeDef = TypedDict(
    "InvokeAsyncResponseTypeDef",
    {
        "Status": int,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

LayerTypeDef = TypedDict(
    "LayerTypeDef",
    {
        "Arn": str,
        "CodeSize": int,
        "SigningProfileVersionArn": str,
        "SigningJobArn": str,
    },
    total=False,
)

LayerVersionContentInputTypeDef = TypedDict(
    "LayerVersionContentInputTypeDef",
    {
        "S3Bucket": str,
        "S3Key": str,
        "S3ObjectVersion": str,
        "ZipFile": Union[str, bytes, IO[Any], StreamingBody],
    },
    total=False,
)

LayerVersionContentOutputTypeDef = TypedDict(
    "LayerVersionContentOutputTypeDef",
    {
        "Location": str,
        "CodeSha256": str,
        "CodeSize": int,
        "SigningProfileVersionArn": str,
        "SigningJobArn": str,
    },
    total=False,
)

LayerVersionsListItemTypeDef = TypedDict(
    "LayerVersionsListItemTypeDef",
    {
        "LayerVersionArn": str,
        "Version": int,
        "Description": str,
        "CreatedDate": str,
        "CompatibleRuntimes": List[RuntimeType],
        "LicenseInfo": str,
        "CompatibleArchitectures": List[ArchitectureType],
    },
    total=False,
)

LayersListItemTypeDef = TypedDict(
    "LayersListItemTypeDef",
    {
        "LayerName": str,
        "LayerArn": str,
        "LatestMatchingVersion": "LayerVersionsListItemTypeDef",
    },
    total=False,
)

_RequiredListAliasesRequestListAliasesPaginateTypeDef = TypedDict(
    "_RequiredListAliasesRequestListAliasesPaginateTypeDef",
    {
        "FunctionName": str,
    },
)
_OptionalListAliasesRequestListAliasesPaginateTypeDef = TypedDict(
    "_OptionalListAliasesRequestListAliasesPaginateTypeDef",
    {
        "FunctionVersion": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListAliasesRequestListAliasesPaginateTypeDef(
    _RequiredListAliasesRequestListAliasesPaginateTypeDef,
    _OptionalListAliasesRequestListAliasesPaginateTypeDef,
):
    pass


_RequiredListAliasesRequestRequestTypeDef = TypedDict(
    "_RequiredListAliasesRequestRequestTypeDef",
    {
        "FunctionName": str,
    },
)
_OptionalListAliasesRequestRequestTypeDef = TypedDict(
    "_OptionalListAliasesRequestRequestTypeDef",
    {
        "FunctionVersion": str,
        "Marker": str,
        "MaxItems": int,
    },
    total=False,
)


class ListAliasesRequestRequestTypeDef(
    _RequiredListAliasesRequestRequestTypeDef, _OptionalListAliasesRequestRequestTypeDef
):
    pass


ListAliasesResponseTypeDef = TypedDict(
    "ListAliasesResponseTypeDef",
    {
        "NextMarker": str,
        "Aliases": List["AliasConfigurationTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListCodeSigningConfigsRequestListCodeSigningConfigsPaginateTypeDef = TypedDict(
    "ListCodeSigningConfigsRequestListCodeSigningConfigsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListCodeSigningConfigsRequestRequestTypeDef = TypedDict(
    "ListCodeSigningConfigsRequestRequestTypeDef",
    {
        "Marker": str,
        "MaxItems": int,
    },
    total=False,
)

ListCodeSigningConfigsResponseTypeDef = TypedDict(
    "ListCodeSigningConfigsResponseTypeDef",
    {
        "NextMarker": str,
        "CodeSigningConfigs": List["CodeSigningConfigTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListEventSourceMappingsRequestListEventSourceMappingsPaginateTypeDef = TypedDict(
    "ListEventSourceMappingsRequestListEventSourceMappingsPaginateTypeDef",
    {
        "EventSourceArn": str,
        "FunctionName": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListEventSourceMappingsRequestRequestTypeDef = TypedDict(
    "ListEventSourceMappingsRequestRequestTypeDef",
    {
        "EventSourceArn": str,
        "FunctionName": str,
        "Marker": str,
        "MaxItems": int,
    },
    total=False,
)

ListEventSourceMappingsResponseTypeDef = TypedDict(
    "ListEventSourceMappingsResponseTypeDef",
    {
        "NextMarker": str,
        "EventSourceMappings": List["EventSourceMappingConfigurationTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredListFunctionEventInvokeConfigsRequestListFunctionEventInvokeConfigsPaginateTypeDef = TypedDict(
    "_RequiredListFunctionEventInvokeConfigsRequestListFunctionEventInvokeConfigsPaginateTypeDef",
    {
        "FunctionName": str,
    },
)
_OptionalListFunctionEventInvokeConfigsRequestListFunctionEventInvokeConfigsPaginateTypeDef = TypedDict(
    "_OptionalListFunctionEventInvokeConfigsRequestListFunctionEventInvokeConfigsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListFunctionEventInvokeConfigsRequestListFunctionEventInvokeConfigsPaginateTypeDef(
    _RequiredListFunctionEventInvokeConfigsRequestListFunctionEventInvokeConfigsPaginateTypeDef,
    _OptionalListFunctionEventInvokeConfigsRequestListFunctionEventInvokeConfigsPaginateTypeDef,
):
    pass


_RequiredListFunctionEventInvokeConfigsRequestRequestTypeDef = TypedDict(
    "_RequiredListFunctionEventInvokeConfigsRequestRequestTypeDef",
    {
        "FunctionName": str,
    },
)
_OptionalListFunctionEventInvokeConfigsRequestRequestTypeDef = TypedDict(
    "_OptionalListFunctionEventInvokeConfigsRequestRequestTypeDef",
    {
        "Marker": str,
        "MaxItems": int,
    },
    total=False,
)


class ListFunctionEventInvokeConfigsRequestRequestTypeDef(
    _RequiredListFunctionEventInvokeConfigsRequestRequestTypeDef,
    _OptionalListFunctionEventInvokeConfigsRequestRequestTypeDef,
):
    pass


ListFunctionEventInvokeConfigsResponseTypeDef = TypedDict(
    "ListFunctionEventInvokeConfigsResponseTypeDef",
    {
        "FunctionEventInvokeConfigs": List["FunctionEventInvokeConfigTypeDef"],
        "NextMarker": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredListFunctionsByCodeSigningConfigRequestListFunctionsByCodeSigningConfigPaginateTypeDef = TypedDict(
    "_RequiredListFunctionsByCodeSigningConfigRequestListFunctionsByCodeSigningConfigPaginateTypeDef",
    {
        "CodeSigningConfigArn": str,
    },
)
_OptionalListFunctionsByCodeSigningConfigRequestListFunctionsByCodeSigningConfigPaginateTypeDef = TypedDict(
    "_OptionalListFunctionsByCodeSigningConfigRequestListFunctionsByCodeSigningConfigPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListFunctionsByCodeSigningConfigRequestListFunctionsByCodeSigningConfigPaginateTypeDef(
    _RequiredListFunctionsByCodeSigningConfigRequestListFunctionsByCodeSigningConfigPaginateTypeDef,
    _OptionalListFunctionsByCodeSigningConfigRequestListFunctionsByCodeSigningConfigPaginateTypeDef,
):
    pass


_RequiredListFunctionsByCodeSigningConfigRequestRequestTypeDef = TypedDict(
    "_RequiredListFunctionsByCodeSigningConfigRequestRequestTypeDef",
    {
        "CodeSigningConfigArn": str,
    },
)
_OptionalListFunctionsByCodeSigningConfigRequestRequestTypeDef = TypedDict(
    "_OptionalListFunctionsByCodeSigningConfigRequestRequestTypeDef",
    {
        "Marker": str,
        "MaxItems": int,
    },
    total=False,
)


class ListFunctionsByCodeSigningConfigRequestRequestTypeDef(
    _RequiredListFunctionsByCodeSigningConfigRequestRequestTypeDef,
    _OptionalListFunctionsByCodeSigningConfigRequestRequestTypeDef,
):
    pass


ListFunctionsByCodeSigningConfigResponseTypeDef = TypedDict(
    "ListFunctionsByCodeSigningConfigResponseTypeDef",
    {
        "NextMarker": str,
        "FunctionArns": List[str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListFunctionsRequestListFunctionsPaginateTypeDef = TypedDict(
    "ListFunctionsRequestListFunctionsPaginateTypeDef",
    {
        "MasterRegion": str,
        "FunctionVersion": Literal["ALL"],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListFunctionsRequestRequestTypeDef = TypedDict(
    "ListFunctionsRequestRequestTypeDef",
    {
        "MasterRegion": str,
        "FunctionVersion": Literal["ALL"],
        "Marker": str,
        "MaxItems": int,
    },
    total=False,
)

ListFunctionsResponseTypeDef = TypedDict(
    "ListFunctionsResponseTypeDef",
    {
        "NextMarker": str,
        "Functions": List["FunctionConfigurationTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredListLayerVersionsRequestListLayerVersionsPaginateTypeDef = TypedDict(
    "_RequiredListLayerVersionsRequestListLayerVersionsPaginateTypeDef",
    {
        "LayerName": str,
    },
)
_OptionalListLayerVersionsRequestListLayerVersionsPaginateTypeDef = TypedDict(
    "_OptionalListLayerVersionsRequestListLayerVersionsPaginateTypeDef",
    {
        "CompatibleRuntime": RuntimeType,
        "CompatibleArchitecture": ArchitectureType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListLayerVersionsRequestListLayerVersionsPaginateTypeDef(
    _RequiredListLayerVersionsRequestListLayerVersionsPaginateTypeDef,
    _OptionalListLayerVersionsRequestListLayerVersionsPaginateTypeDef,
):
    pass


_RequiredListLayerVersionsRequestRequestTypeDef = TypedDict(
    "_RequiredListLayerVersionsRequestRequestTypeDef",
    {
        "LayerName": str,
    },
)
_OptionalListLayerVersionsRequestRequestTypeDef = TypedDict(
    "_OptionalListLayerVersionsRequestRequestTypeDef",
    {
        "CompatibleRuntime": RuntimeType,
        "Marker": str,
        "MaxItems": int,
        "CompatibleArchitecture": ArchitectureType,
    },
    total=False,
)


class ListLayerVersionsRequestRequestTypeDef(
    _RequiredListLayerVersionsRequestRequestTypeDef, _OptionalListLayerVersionsRequestRequestTypeDef
):
    pass


ListLayerVersionsResponseTypeDef = TypedDict(
    "ListLayerVersionsResponseTypeDef",
    {
        "NextMarker": str,
        "LayerVersions": List["LayerVersionsListItemTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListLayersRequestListLayersPaginateTypeDef = TypedDict(
    "ListLayersRequestListLayersPaginateTypeDef",
    {
        "CompatibleRuntime": RuntimeType,
        "CompatibleArchitecture": ArchitectureType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListLayersRequestRequestTypeDef = TypedDict(
    "ListLayersRequestRequestTypeDef",
    {
        "CompatibleRuntime": RuntimeType,
        "Marker": str,
        "MaxItems": int,
        "CompatibleArchitecture": ArchitectureType,
    },
    total=False,
)

ListLayersResponseTypeDef = TypedDict(
    "ListLayersResponseTypeDef",
    {
        "NextMarker": str,
        "Layers": List["LayersListItemTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredListProvisionedConcurrencyConfigsRequestListProvisionedConcurrencyConfigsPaginateTypeDef = TypedDict(
    "_RequiredListProvisionedConcurrencyConfigsRequestListProvisionedConcurrencyConfigsPaginateTypeDef",
    {
        "FunctionName": str,
    },
)
_OptionalListProvisionedConcurrencyConfigsRequestListProvisionedConcurrencyConfigsPaginateTypeDef = TypedDict(
    "_OptionalListProvisionedConcurrencyConfigsRequestListProvisionedConcurrencyConfigsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListProvisionedConcurrencyConfigsRequestListProvisionedConcurrencyConfigsPaginateTypeDef(
    _RequiredListProvisionedConcurrencyConfigsRequestListProvisionedConcurrencyConfigsPaginateTypeDef,
    _OptionalListProvisionedConcurrencyConfigsRequestListProvisionedConcurrencyConfigsPaginateTypeDef,
):
    pass


_RequiredListProvisionedConcurrencyConfigsRequestRequestTypeDef = TypedDict(
    "_RequiredListProvisionedConcurrencyConfigsRequestRequestTypeDef",
    {
        "FunctionName": str,
    },
)
_OptionalListProvisionedConcurrencyConfigsRequestRequestTypeDef = TypedDict(
    "_OptionalListProvisionedConcurrencyConfigsRequestRequestTypeDef",
    {
        "Marker": str,
        "MaxItems": int,
    },
    total=False,
)


class ListProvisionedConcurrencyConfigsRequestRequestTypeDef(
    _RequiredListProvisionedConcurrencyConfigsRequestRequestTypeDef,
    _OptionalListProvisionedConcurrencyConfigsRequestRequestTypeDef,
):
    pass


ListProvisionedConcurrencyConfigsResponseTypeDef = TypedDict(
    "ListProvisionedConcurrencyConfigsResponseTypeDef",
    {
        "ProvisionedConcurrencyConfigs": List["ProvisionedConcurrencyConfigListItemTypeDef"],
        "NextMarker": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListTagsRequestRequestTypeDef = TypedDict(
    "ListTagsRequestRequestTypeDef",
    {
        "Resource": str,
    },
)

ListTagsResponseTypeDef = TypedDict(
    "ListTagsResponseTypeDef",
    {
        "Tags": Dict[str, str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredListVersionsByFunctionRequestListVersionsByFunctionPaginateTypeDef = TypedDict(
    "_RequiredListVersionsByFunctionRequestListVersionsByFunctionPaginateTypeDef",
    {
        "FunctionName": str,
    },
)
_OptionalListVersionsByFunctionRequestListVersionsByFunctionPaginateTypeDef = TypedDict(
    "_OptionalListVersionsByFunctionRequestListVersionsByFunctionPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListVersionsByFunctionRequestListVersionsByFunctionPaginateTypeDef(
    _RequiredListVersionsByFunctionRequestListVersionsByFunctionPaginateTypeDef,
    _OptionalListVersionsByFunctionRequestListVersionsByFunctionPaginateTypeDef,
):
    pass


_RequiredListVersionsByFunctionRequestRequestTypeDef = TypedDict(
    "_RequiredListVersionsByFunctionRequestRequestTypeDef",
    {
        "FunctionName": str,
    },
)
_OptionalListVersionsByFunctionRequestRequestTypeDef = TypedDict(
    "_OptionalListVersionsByFunctionRequestRequestTypeDef",
    {
        "Marker": str,
        "MaxItems": int,
    },
    total=False,
)


class ListVersionsByFunctionRequestRequestTypeDef(
    _RequiredListVersionsByFunctionRequestRequestTypeDef,
    _OptionalListVersionsByFunctionRequestRequestTypeDef,
):
    pass


ListVersionsByFunctionResponseTypeDef = TypedDict(
    "ListVersionsByFunctionResponseTypeDef",
    {
        "NextMarker": str,
        "Versions": List["FunctionConfigurationTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

OnFailureTypeDef = TypedDict(
    "OnFailureTypeDef",
    {
        "Destination": str,
    },
    total=False,
)

OnSuccessTypeDef = TypedDict(
    "OnSuccessTypeDef",
    {
        "Destination": str,
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

ProvisionedConcurrencyConfigListItemTypeDef = TypedDict(
    "ProvisionedConcurrencyConfigListItemTypeDef",
    {
        "FunctionArn": str,
        "RequestedProvisionedConcurrentExecutions": int,
        "AvailableProvisionedConcurrentExecutions": int,
        "AllocatedProvisionedConcurrentExecutions": int,
        "Status": ProvisionedConcurrencyStatusEnumType,
        "StatusReason": str,
        "LastModified": str,
    },
    total=False,
)

_RequiredPublishLayerVersionRequestRequestTypeDef = TypedDict(
    "_RequiredPublishLayerVersionRequestRequestTypeDef",
    {
        "LayerName": str,
        "Content": "LayerVersionContentInputTypeDef",
    },
)
_OptionalPublishLayerVersionRequestRequestTypeDef = TypedDict(
    "_OptionalPublishLayerVersionRequestRequestTypeDef",
    {
        "Description": str,
        "CompatibleRuntimes": Sequence[RuntimeType],
        "LicenseInfo": str,
        "CompatibleArchitectures": Sequence[ArchitectureType],
    },
    total=False,
)


class PublishLayerVersionRequestRequestTypeDef(
    _RequiredPublishLayerVersionRequestRequestTypeDef,
    _OptionalPublishLayerVersionRequestRequestTypeDef,
):
    pass


PublishLayerVersionResponseTypeDef = TypedDict(
    "PublishLayerVersionResponseTypeDef",
    {
        "Content": "LayerVersionContentOutputTypeDef",
        "LayerArn": str,
        "LayerVersionArn": str,
        "Description": str,
        "CreatedDate": str,
        "Version": int,
        "CompatibleRuntimes": List[RuntimeType],
        "LicenseInfo": str,
        "CompatibleArchitectures": List[ArchitectureType],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredPublishVersionRequestRequestTypeDef = TypedDict(
    "_RequiredPublishVersionRequestRequestTypeDef",
    {
        "FunctionName": str,
    },
)
_OptionalPublishVersionRequestRequestTypeDef = TypedDict(
    "_OptionalPublishVersionRequestRequestTypeDef",
    {
        "CodeSha256": str,
        "Description": str,
        "RevisionId": str,
    },
    total=False,
)


class PublishVersionRequestRequestTypeDef(
    _RequiredPublishVersionRequestRequestTypeDef, _OptionalPublishVersionRequestRequestTypeDef
):
    pass


PutFunctionCodeSigningConfigRequestRequestTypeDef = TypedDict(
    "PutFunctionCodeSigningConfigRequestRequestTypeDef",
    {
        "CodeSigningConfigArn": str,
        "FunctionName": str,
    },
)

PutFunctionCodeSigningConfigResponseTypeDef = TypedDict(
    "PutFunctionCodeSigningConfigResponseTypeDef",
    {
        "CodeSigningConfigArn": str,
        "FunctionName": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

PutFunctionConcurrencyRequestRequestTypeDef = TypedDict(
    "PutFunctionConcurrencyRequestRequestTypeDef",
    {
        "FunctionName": str,
        "ReservedConcurrentExecutions": int,
    },
)

_RequiredPutFunctionEventInvokeConfigRequestRequestTypeDef = TypedDict(
    "_RequiredPutFunctionEventInvokeConfigRequestRequestTypeDef",
    {
        "FunctionName": str,
    },
)
_OptionalPutFunctionEventInvokeConfigRequestRequestTypeDef = TypedDict(
    "_OptionalPutFunctionEventInvokeConfigRequestRequestTypeDef",
    {
        "Qualifier": str,
        "MaximumRetryAttempts": int,
        "MaximumEventAgeInSeconds": int,
        "DestinationConfig": "DestinationConfigTypeDef",
    },
    total=False,
)


class PutFunctionEventInvokeConfigRequestRequestTypeDef(
    _RequiredPutFunctionEventInvokeConfigRequestRequestTypeDef,
    _OptionalPutFunctionEventInvokeConfigRequestRequestTypeDef,
):
    pass


PutProvisionedConcurrencyConfigRequestRequestTypeDef = TypedDict(
    "PutProvisionedConcurrencyConfigRequestRequestTypeDef",
    {
        "FunctionName": str,
        "Qualifier": str,
        "ProvisionedConcurrentExecutions": int,
    },
)

PutProvisionedConcurrencyConfigResponseTypeDef = TypedDict(
    "PutProvisionedConcurrencyConfigResponseTypeDef",
    {
        "RequestedProvisionedConcurrentExecutions": int,
        "AvailableProvisionedConcurrentExecutions": int,
        "AllocatedProvisionedConcurrentExecutions": int,
        "Status": ProvisionedConcurrencyStatusEnumType,
        "StatusReason": str,
        "LastModified": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredRemoveLayerVersionPermissionRequestRequestTypeDef = TypedDict(
    "_RequiredRemoveLayerVersionPermissionRequestRequestTypeDef",
    {
        "LayerName": str,
        "VersionNumber": int,
        "StatementId": str,
    },
)
_OptionalRemoveLayerVersionPermissionRequestRequestTypeDef = TypedDict(
    "_OptionalRemoveLayerVersionPermissionRequestRequestTypeDef",
    {
        "RevisionId": str,
    },
    total=False,
)


class RemoveLayerVersionPermissionRequestRequestTypeDef(
    _RequiredRemoveLayerVersionPermissionRequestRequestTypeDef,
    _OptionalRemoveLayerVersionPermissionRequestRequestTypeDef,
):
    pass


_RequiredRemovePermissionRequestRequestTypeDef = TypedDict(
    "_RequiredRemovePermissionRequestRequestTypeDef",
    {
        "FunctionName": str,
        "StatementId": str,
    },
)
_OptionalRemovePermissionRequestRequestTypeDef = TypedDict(
    "_OptionalRemovePermissionRequestRequestTypeDef",
    {
        "Qualifier": str,
        "RevisionId": str,
    },
    total=False,
)


class RemovePermissionRequestRequestTypeDef(
    _RequiredRemovePermissionRequestRequestTypeDef, _OptionalRemovePermissionRequestRequestTypeDef
):
    pass


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

SelfManagedEventSourceTypeDef = TypedDict(
    "SelfManagedEventSourceTypeDef",
    {
        "Endpoints": Mapping[Literal["KAFKA_BOOTSTRAP_SERVERS"], Sequence[str]],
    },
    total=False,
)

SourceAccessConfigurationTypeDef = TypedDict(
    "SourceAccessConfigurationTypeDef",
    {
        "Type": SourceAccessTypeType,
        "URI": str,
    },
    total=False,
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "Resource": str,
        "Tags": Mapping[str, str],
    },
)

TracingConfigResponseTypeDef = TypedDict(
    "TracingConfigResponseTypeDef",
    {
        "Mode": TracingModeType,
    },
    total=False,
)

TracingConfigTypeDef = TypedDict(
    "TracingConfigTypeDef",
    {
        "Mode": TracingModeType,
    },
    total=False,
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "Resource": str,
        "TagKeys": Sequence[str],
    },
)

_RequiredUpdateAliasRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateAliasRequestRequestTypeDef",
    {
        "FunctionName": str,
        "Name": str,
    },
)
_OptionalUpdateAliasRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateAliasRequestRequestTypeDef",
    {
        "FunctionVersion": str,
        "Description": str,
        "RoutingConfig": "AliasRoutingConfigurationTypeDef",
        "RevisionId": str,
    },
    total=False,
)


class UpdateAliasRequestRequestTypeDef(
    _RequiredUpdateAliasRequestRequestTypeDef, _OptionalUpdateAliasRequestRequestTypeDef
):
    pass


_RequiredUpdateCodeSigningConfigRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateCodeSigningConfigRequestRequestTypeDef",
    {
        "CodeSigningConfigArn": str,
    },
)
_OptionalUpdateCodeSigningConfigRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateCodeSigningConfigRequestRequestTypeDef",
    {
        "Description": str,
        "AllowedPublishers": "AllowedPublishersTypeDef",
        "CodeSigningPolicies": "CodeSigningPoliciesTypeDef",
    },
    total=False,
)


class UpdateCodeSigningConfigRequestRequestTypeDef(
    _RequiredUpdateCodeSigningConfigRequestRequestTypeDef,
    _OptionalUpdateCodeSigningConfigRequestRequestTypeDef,
):
    pass


UpdateCodeSigningConfigResponseTypeDef = TypedDict(
    "UpdateCodeSigningConfigResponseTypeDef",
    {
        "CodeSigningConfig": "CodeSigningConfigTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredUpdateEventSourceMappingRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateEventSourceMappingRequestRequestTypeDef",
    {
        "UUID": str,
    },
)
_OptionalUpdateEventSourceMappingRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateEventSourceMappingRequestRequestTypeDef",
    {
        "FunctionName": str,
        "Enabled": bool,
        "BatchSize": int,
        "FilterCriteria": "FilterCriteriaTypeDef",
        "MaximumBatchingWindowInSeconds": int,
        "DestinationConfig": "DestinationConfigTypeDef",
        "MaximumRecordAgeInSeconds": int,
        "BisectBatchOnFunctionError": bool,
        "MaximumRetryAttempts": int,
        "ParallelizationFactor": int,
        "SourceAccessConfigurations": Sequence["SourceAccessConfigurationTypeDef"],
        "TumblingWindowInSeconds": int,
        "FunctionResponseTypes": Sequence[Literal["ReportBatchItemFailures"]],
    },
    total=False,
)


class UpdateEventSourceMappingRequestRequestTypeDef(
    _RequiredUpdateEventSourceMappingRequestRequestTypeDef,
    _OptionalUpdateEventSourceMappingRequestRequestTypeDef,
):
    pass


_RequiredUpdateFunctionCodeRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateFunctionCodeRequestRequestTypeDef",
    {
        "FunctionName": str,
    },
)
_OptionalUpdateFunctionCodeRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateFunctionCodeRequestRequestTypeDef",
    {
        "ZipFile": Union[str, bytes, IO[Any], StreamingBody],
        "S3Bucket": str,
        "S3Key": str,
        "S3ObjectVersion": str,
        "ImageUri": str,
        "Publish": bool,
        "DryRun": bool,
        "RevisionId": str,
        "Architectures": Sequence[ArchitectureType],
    },
    total=False,
)


class UpdateFunctionCodeRequestRequestTypeDef(
    _RequiredUpdateFunctionCodeRequestRequestTypeDef,
    _OptionalUpdateFunctionCodeRequestRequestTypeDef,
):
    pass


_RequiredUpdateFunctionConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateFunctionConfigurationRequestRequestTypeDef",
    {
        "FunctionName": str,
    },
)
_OptionalUpdateFunctionConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateFunctionConfigurationRequestRequestTypeDef",
    {
        "Role": str,
        "Handler": str,
        "Description": str,
        "Timeout": int,
        "MemorySize": int,
        "VpcConfig": "VpcConfigTypeDef",
        "Environment": "EnvironmentTypeDef",
        "Runtime": RuntimeType,
        "DeadLetterConfig": "DeadLetterConfigTypeDef",
        "KMSKeyArn": str,
        "TracingConfig": "TracingConfigTypeDef",
        "RevisionId": str,
        "Layers": Sequence[str],
        "FileSystemConfigs": Sequence["FileSystemConfigTypeDef"],
        "ImageConfig": "ImageConfigTypeDef",
    },
    total=False,
)


class UpdateFunctionConfigurationRequestRequestTypeDef(
    _RequiredUpdateFunctionConfigurationRequestRequestTypeDef,
    _OptionalUpdateFunctionConfigurationRequestRequestTypeDef,
):
    pass


_RequiredUpdateFunctionEventInvokeConfigRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateFunctionEventInvokeConfigRequestRequestTypeDef",
    {
        "FunctionName": str,
    },
)
_OptionalUpdateFunctionEventInvokeConfigRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateFunctionEventInvokeConfigRequestRequestTypeDef",
    {
        "Qualifier": str,
        "MaximumRetryAttempts": int,
        "MaximumEventAgeInSeconds": int,
        "DestinationConfig": "DestinationConfigTypeDef",
    },
    total=False,
)


class UpdateFunctionEventInvokeConfigRequestRequestTypeDef(
    _RequiredUpdateFunctionEventInvokeConfigRequestRequestTypeDef,
    _OptionalUpdateFunctionEventInvokeConfigRequestRequestTypeDef,
):
    pass


VpcConfigResponseTypeDef = TypedDict(
    "VpcConfigResponseTypeDef",
    {
        "SubnetIds": List[str],
        "SecurityGroupIds": List[str],
        "VpcId": str,
    },
    total=False,
)

VpcConfigTypeDef = TypedDict(
    "VpcConfigTypeDef",
    {
        "SubnetIds": Sequence[str],
        "SecurityGroupIds": Sequence[str],
    },
    total=False,
)

WaiterConfigTypeDef = TypedDict(
    "WaiterConfigTypeDef",
    {
        "Delay": int,
        "MaxAttempts": int,
    },
    total=False,
)
