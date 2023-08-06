"""
Type annotations for iotsitewise service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotsitewise/type_defs/)

Usage::

    ```python
    from mypy_boto3_iotsitewise.type_defs import AccessPolicySummaryTypeDef

    data: AccessPolicySummaryTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    AggregateTypeType,
    AssetModelStateType,
    AssetStateType,
    AuthModeType,
    BatchEntryCompletionStatusType,
    BatchGetAssetPropertyAggregatesErrorCodeType,
    BatchGetAssetPropertyValueErrorCodeType,
    BatchGetAssetPropertyValueHistoryErrorCodeType,
    BatchPutAssetPropertyValueErrorCodeType,
    CapabilitySyncStatusType,
    ComputeLocationType,
    ConfigurationStateType,
    DetailedErrorCodeType,
    DisassociatedDataStorageStateType,
    EncryptionTypeType,
    ErrorCodeType,
    ForwardingConfigStateType,
    IdentityTypeType,
    ListAssetsFilterType,
    ListTimeSeriesTypeType,
    LoggingLevelType,
    MonitorErrorCodeType,
    PermissionType,
    PortalStateType,
    PropertyDataTypeType,
    PropertyNotificationStateType,
    QualityType,
    ResourceTypeType,
    StorageTypeType,
    TimeOrderingType,
    TraversalDirectionType,
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
    "AccessPolicySummaryTypeDef",
    "AggregatedValueTypeDef",
    "AggregatesTypeDef",
    "AlarmsTypeDef",
    "AssetCompositeModelTypeDef",
    "AssetErrorDetailsTypeDef",
    "AssetHierarchyInfoTypeDef",
    "AssetHierarchyTypeDef",
    "AssetModelCompositeModelDefinitionTypeDef",
    "AssetModelCompositeModelTypeDef",
    "AssetModelHierarchyDefinitionTypeDef",
    "AssetModelHierarchyTypeDef",
    "AssetModelPropertyDefinitionTypeDef",
    "AssetModelPropertyTypeDef",
    "AssetModelStatusTypeDef",
    "AssetModelSummaryTypeDef",
    "AssetPropertyTypeDef",
    "AssetPropertyValueTypeDef",
    "AssetRelationshipSummaryTypeDef",
    "AssetStatusTypeDef",
    "AssetSummaryTypeDef",
    "AssociateAssetsRequestRequestTypeDef",
    "AssociateTimeSeriesToAssetPropertyRequestRequestTypeDef",
    "AssociatedAssetsSummaryTypeDef",
    "AttributeTypeDef",
    "BatchAssociateProjectAssetsRequestRequestTypeDef",
    "BatchAssociateProjectAssetsResponseTypeDef",
    "BatchDisassociateProjectAssetsRequestRequestTypeDef",
    "BatchDisassociateProjectAssetsResponseTypeDef",
    "BatchGetAssetPropertyAggregatesEntryTypeDef",
    "BatchGetAssetPropertyAggregatesErrorEntryTypeDef",
    "BatchGetAssetPropertyAggregatesErrorInfoTypeDef",
    "BatchGetAssetPropertyAggregatesRequestRequestTypeDef",
    "BatchGetAssetPropertyAggregatesResponseTypeDef",
    "BatchGetAssetPropertyAggregatesSkippedEntryTypeDef",
    "BatchGetAssetPropertyAggregatesSuccessEntryTypeDef",
    "BatchGetAssetPropertyValueEntryTypeDef",
    "BatchGetAssetPropertyValueErrorEntryTypeDef",
    "BatchGetAssetPropertyValueErrorInfoTypeDef",
    "BatchGetAssetPropertyValueHistoryEntryTypeDef",
    "BatchGetAssetPropertyValueHistoryErrorEntryTypeDef",
    "BatchGetAssetPropertyValueHistoryErrorInfoTypeDef",
    "BatchGetAssetPropertyValueHistoryRequestRequestTypeDef",
    "BatchGetAssetPropertyValueHistoryResponseTypeDef",
    "BatchGetAssetPropertyValueHistorySkippedEntryTypeDef",
    "BatchGetAssetPropertyValueHistorySuccessEntryTypeDef",
    "BatchGetAssetPropertyValueRequestRequestTypeDef",
    "BatchGetAssetPropertyValueResponseTypeDef",
    "BatchGetAssetPropertyValueSkippedEntryTypeDef",
    "BatchGetAssetPropertyValueSuccessEntryTypeDef",
    "BatchPutAssetPropertyErrorEntryTypeDef",
    "BatchPutAssetPropertyErrorTypeDef",
    "BatchPutAssetPropertyValueRequestRequestTypeDef",
    "BatchPutAssetPropertyValueResponseTypeDef",
    "CompositeModelPropertyTypeDef",
    "ConfigurationErrorDetailsTypeDef",
    "ConfigurationStatusTypeDef",
    "CreateAccessPolicyRequestRequestTypeDef",
    "CreateAccessPolicyResponseTypeDef",
    "CreateAssetModelRequestRequestTypeDef",
    "CreateAssetModelResponseTypeDef",
    "CreateAssetRequestRequestTypeDef",
    "CreateAssetResponseTypeDef",
    "CreateDashboardRequestRequestTypeDef",
    "CreateDashboardResponseTypeDef",
    "CreateGatewayRequestRequestTypeDef",
    "CreateGatewayResponseTypeDef",
    "CreatePortalRequestRequestTypeDef",
    "CreatePortalResponseTypeDef",
    "CreateProjectRequestRequestTypeDef",
    "CreateProjectResponseTypeDef",
    "CustomerManagedS3StorageTypeDef",
    "DashboardSummaryTypeDef",
    "DeleteAccessPolicyRequestRequestTypeDef",
    "DeleteAssetModelRequestRequestTypeDef",
    "DeleteAssetModelResponseTypeDef",
    "DeleteAssetRequestRequestTypeDef",
    "DeleteAssetResponseTypeDef",
    "DeleteDashboardRequestRequestTypeDef",
    "DeleteGatewayRequestRequestTypeDef",
    "DeletePortalRequestRequestTypeDef",
    "DeletePortalResponseTypeDef",
    "DeleteProjectRequestRequestTypeDef",
    "DeleteTimeSeriesRequestRequestTypeDef",
    "DescribeAccessPolicyRequestRequestTypeDef",
    "DescribeAccessPolicyResponseTypeDef",
    "DescribeAssetModelRequestAssetModelActiveWaitTypeDef",
    "DescribeAssetModelRequestAssetModelNotExistsWaitTypeDef",
    "DescribeAssetModelRequestRequestTypeDef",
    "DescribeAssetModelResponseTypeDef",
    "DescribeAssetPropertyRequestRequestTypeDef",
    "DescribeAssetPropertyResponseTypeDef",
    "DescribeAssetRequestAssetActiveWaitTypeDef",
    "DescribeAssetRequestAssetNotExistsWaitTypeDef",
    "DescribeAssetRequestRequestTypeDef",
    "DescribeAssetResponseTypeDef",
    "DescribeDashboardRequestRequestTypeDef",
    "DescribeDashboardResponseTypeDef",
    "DescribeDefaultEncryptionConfigurationResponseTypeDef",
    "DescribeGatewayCapabilityConfigurationRequestRequestTypeDef",
    "DescribeGatewayCapabilityConfigurationResponseTypeDef",
    "DescribeGatewayRequestRequestTypeDef",
    "DescribeGatewayResponseTypeDef",
    "DescribeLoggingOptionsResponseTypeDef",
    "DescribePortalRequestPortalActiveWaitTypeDef",
    "DescribePortalRequestPortalNotExistsWaitTypeDef",
    "DescribePortalRequestRequestTypeDef",
    "DescribePortalResponseTypeDef",
    "DescribeProjectRequestRequestTypeDef",
    "DescribeProjectResponseTypeDef",
    "DescribeStorageConfigurationResponseTypeDef",
    "DescribeTimeSeriesRequestRequestTypeDef",
    "DescribeTimeSeriesResponseTypeDef",
    "DetailedErrorTypeDef",
    "DisassociateAssetsRequestRequestTypeDef",
    "DisassociateTimeSeriesFromAssetPropertyRequestRequestTypeDef",
    "ErrorDetailsTypeDef",
    "ExpressionVariableTypeDef",
    "ForwardingConfigTypeDef",
    "GatewayCapabilitySummaryTypeDef",
    "GatewayPlatformTypeDef",
    "GatewaySummaryTypeDef",
    "GetAssetPropertyAggregatesRequestGetAssetPropertyAggregatesPaginateTypeDef",
    "GetAssetPropertyAggregatesRequestRequestTypeDef",
    "GetAssetPropertyAggregatesResponseTypeDef",
    "GetAssetPropertyValueHistoryRequestGetAssetPropertyValueHistoryPaginateTypeDef",
    "GetAssetPropertyValueHistoryRequestRequestTypeDef",
    "GetAssetPropertyValueHistoryResponseTypeDef",
    "GetAssetPropertyValueRequestRequestTypeDef",
    "GetAssetPropertyValueResponseTypeDef",
    "GetInterpolatedAssetPropertyValuesRequestGetInterpolatedAssetPropertyValuesPaginateTypeDef",
    "GetInterpolatedAssetPropertyValuesRequestRequestTypeDef",
    "GetInterpolatedAssetPropertyValuesResponseTypeDef",
    "GreengrassTypeDef",
    "GreengrassV2TypeDef",
    "GroupIdentityTypeDef",
    "IAMRoleIdentityTypeDef",
    "IAMUserIdentityTypeDef",
    "IdentityTypeDef",
    "ImageFileTypeDef",
    "ImageLocationTypeDef",
    "ImageTypeDef",
    "InterpolatedAssetPropertyValueTypeDef",
    "ListAccessPoliciesRequestListAccessPoliciesPaginateTypeDef",
    "ListAccessPoliciesRequestRequestTypeDef",
    "ListAccessPoliciesResponseTypeDef",
    "ListAssetModelsRequestListAssetModelsPaginateTypeDef",
    "ListAssetModelsRequestRequestTypeDef",
    "ListAssetModelsResponseTypeDef",
    "ListAssetRelationshipsRequestListAssetRelationshipsPaginateTypeDef",
    "ListAssetRelationshipsRequestRequestTypeDef",
    "ListAssetRelationshipsResponseTypeDef",
    "ListAssetsRequestListAssetsPaginateTypeDef",
    "ListAssetsRequestRequestTypeDef",
    "ListAssetsResponseTypeDef",
    "ListAssociatedAssetsRequestListAssociatedAssetsPaginateTypeDef",
    "ListAssociatedAssetsRequestRequestTypeDef",
    "ListAssociatedAssetsResponseTypeDef",
    "ListDashboardsRequestListDashboardsPaginateTypeDef",
    "ListDashboardsRequestRequestTypeDef",
    "ListDashboardsResponseTypeDef",
    "ListGatewaysRequestListGatewaysPaginateTypeDef",
    "ListGatewaysRequestRequestTypeDef",
    "ListGatewaysResponseTypeDef",
    "ListPortalsRequestListPortalsPaginateTypeDef",
    "ListPortalsRequestRequestTypeDef",
    "ListPortalsResponseTypeDef",
    "ListProjectAssetsRequestListProjectAssetsPaginateTypeDef",
    "ListProjectAssetsRequestRequestTypeDef",
    "ListProjectAssetsResponseTypeDef",
    "ListProjectsRequestListProjectsPaginateTypeDef",
    "ListProjectsRequestRequestTypeDef",
    "ListProjectsResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListTimeSeriesRequestListTimeSeriesPaginateTypeDef",
    "ListTimeSeriesRequestRequestTypeDef",
    "ListTimeSeriesResponseTypeDef",
    "LoggingOptionsTypeDef",
    "MeasurementProcessingConfigTypeDef",
    "MeasurementTypeDef",
    "MetricProcessingConfigTypeDef",
    "MetricTypeDef",
    "MetricWindowTypeDef",
    "MonitorErrorDetailsTypeDef",
    "MultiLayerStorageTypeDef",
    "PaginatorConfigTypeDef",
    "PortalResourceTypeDef",
    "PortalStatusTypeDef",
    "PortalSummaryTypeDef",
    "ProjectResourceTypeDef",
    "ProjectSummaryTypeDef",
    "PropertyNotificationTypeDef",
    "PropertyTypeDef",
    "PropertyTypeTypeDef",
    "PutAssetPropertyValueEntryTypeDef",
    "PutDefaultEncryptionConfigurationRequestRequestTypeDef",
    "PutDefaultEncryptionConfigurationResponseTypeDef",
    "PutLoggingOptionsRequestRequestTypeDef",
    "PutStorageConfigurationRequestRequestTypeDef",
    "PutStorageConfigurationResponseTypeDef",
    "ResourceTypeDef",
    "ResponseMetadataTypeDef",
    "RetentionPeriodTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TimeInNanosTypeDef",
    "TimeSeriesSummaryTypeDef",
    "TransformProcessingConfigTypeDef",
    "TransformTypeDef",
    "TumblingWindowTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateAccessPolicyRequestRequestTypeDef",
    "UpdateAssetModelRequestRequestTypeDef",
    "UpdateAssetModelResponseTypeDef",
    "UpdateAssetPropertyRequestRequestTypeDef",
    "UpdateAssetRequestRequestTypeDef",
    "UpdateAssetResponseTypeDef",
    "UpdateDashboardRequestRequestTypeDef",
    "UpdateGatewayCapabilityConfigurationRequestRequestTypeDef",
    "UpdateGatewayCapabilityConfigurationResponseTypeDef",
    "UpdateGatewayRequestRequestTypeDef",
    "UpdatePortalRequestRequestTypeDef",
    "UpdatePortalResponseTypeDef",
    "UpdateProjectRequestRequestTypeDef",
    "UserIdentityTypeDef",
    "VariableValueTypeDef",
    "VariantTypeDef",
    "WaiterConfigTypeDef",
)

_RequiredAccessPolicySummaryTypeDef = TypedDict(
    "_RequiredAccessPolicySummaryTypeDef",
    {
        "id": str,
        "identity": "IdentityTypeDef",
        "resource": "ResourceTypeDef",
        "permission": PermissionType,
    },
)
_OptionalAccessPolicySummaryTypeDef = TypedDict(
    "_OptionalAccessPolicySummaryTypeDef",
    {
        "creationDate": datetime,
        "lastUpdateDate": datetime,
    },
    total=False,
)


class AccessPolicySummaryTypeDef(
    _RequiredAccessPolicySummaryTypeDef, _OptionalAccessPolicySummaryTypeDef
):
    pass


_RequiredAggregatedValueTypeDef = TypedDict(
    "_RequiredAggregatedValueTypeDef",
    {
        "timestamp": datetime,
        "value": "AggregatesTypeDef",
    },
)
_OptionalAggregatedValueTypeDef = TypedDict(
    "_OptionalAggregatedValueTypeDef",
    {
        "quality": QualityType,
    },
    total=False,
)


class AggregatedValueTypeDef(_RequiredAggregatedValueTypeDef, _OptionalAggregatedValueTypeDef):
    pass


AggregatesTypeDef = TypedDict(
    "AggregatesTypeDef",
    {
        "average": float,
        "count": float,
        "maximum": float,
        "minimum": float,
        "sum": float,
        "standardDeviation": float,
    },
    total=False,
)

_RequiredAlarmsTypeDef = TypedDict(
    "_RequiredAlarmsTypeDef",
    {
        "alarmRoleArn": str,
    },
)
_OptionalAlarmsTypeDef = TypedDict(
    "_OptionalAlarmsTypeDef",
    {
        "notificationLambdaArn": str,
    },
    total=False,
)


class AlarmsTypeDef(_RequiredAlarmsTypeDef, _OptionalAlarmsTypeDef):
    pass


_RequiredAssetCompositeModelTypeDef = TypedDict(
    "_RequiredAssetCompositeModelTypeDef",
    {
        "name": str,
        "type": str,
        "properties": List["AssetPropertyTypeDef"],
    },
)
_OptionalAssetCompositeModelTypeDef = TypedDict(
    "_OptionalAssetCompositeModelTypeDef",
    {
        "description": str,
    },
    total=False,
)


class AssetCompositeModelTypeDef(
    _RequiredAssetCompositeModelTypeDef, _OptionalAssetCompositeModelTypeDef
):
    pass


AssetErrorDetailsTypeDef = TypedDict(
    "AssetErrorDetailsTypeDef",
    {
        "assetId": str,
        "code": Literal["INTERNAL_FAILURE"],
        "message": str,
    },
)

AssetHierarchyInfoTypeDef = TypedDict(
    "AssetHierarchyInfoTypeDef",
    {
        "parentAssetId": str,
        "childAssetId": str,
    },
    total=False,
)

_RequiredAssetHierarchyTypeDef = TypedDict(
    "_RequiredAssetHierarchyTypeDef",
    {
        "name": str,
    },
)
_OptionalAssetHierarchyTypeDef = TypedDict(
    "_OptionalAssetHierarchyTypeDef",
    {
        "id": str,
    },
    total=False,
)


class AssetHierarchyTypeDef(_RequiredAssetHierarchyTypeDef, _OptionalAssetHierarchyTypeDef):
    pass


_RequiredAssetModelCompositeModelDefinitionTypeDef = TypedDict(
    "_RequiredAssetModelCompositeModelDefinitionTypeDef",
    {
        "name": str,
        "type": str,
    },
)
_OptionalAssetModelCompositeModelDefinitionTypeDef = TypedDict(
    "_OptionalAssetModelCompositeModelDefinitionTypeDef",
    {
        "description": str,
        "properties": Sequence["AssetModelPropertyDefinitionTypeDef"],
    },
    total=False,
)


class AssetModelCompositeModelDefinitionTypeDef(
    _RequiredAssetModelCompositeModelDefinitionTypeDef,
    _OptionalAssetModelCompositeModelDefinitionTypeDef,
):
    pass


_RequiredAssetModelCompositeModelTypeDef = TypedDict(
    "_RequiredAssetModelCompositeModelTypeDef",
    {
        "name": str,
        "type": str,
    },
)
_OptionalAssetModelCompositeModelTypeDef = TypedDict(
    "_OptionalAssetModelCompositeModelTypeDef",
    {
        "description": str,
        "properties": List["AssetModelPropertyTypeDef"],
    },
    total=False,
)


class AssetModelCompositeModelTypeDef(
    _RequiredAssetModelCompositeModelTypeDef, _OptionalAssetModelCompositeModelTypeDef
):
    pass


AssetModelHierarchyDefinitionTypeDef = TypedDict(
    "AssetModelHierarchyDefinitionTypeDef",
    {
        "name": str,
        "childAssetModelId": str,
    },
)

_RequiredAssetModelHierarchyTypeDef = TypedDict(
    "_RequiredAssetModelHierarchyTypeDef",
    {
        "name": str,
        "childAssetModelId": str,
    },
)
_OptionalAssetModelHierarchyTypeDef = TypedDict(
    "_OptionalAssetModelHierarchyTypeDef",
    {
        "id": str,
    },
    total=False,
)


class AssetModelHierarchyTypeDef(
    _RequiredAssetModelHierarchyTypeDef, _OptionalAssetModelHierarchyTypeDef
):
    pass


_RequiredAssetModelPropertyDefinitionTypeDef = TypedDict(
    "_RequiredAssetModelPropertyDefinitionTypeDef",
    {
        "name": str,
        "dataType": PropertyDataTypeType,
        "type": "PropertyTypeTypeDef",
    },
)
_OptionalAssetModelPropertyDefinitionTypeDef = TypedDict(
    "_OptionalAssetModelPropertyDefinitionTypeDef",
    {
        "dataTypeSpec": str,
        "unit": str,
    },
    total=False,
)


class AssetModelPropertyDefinitionTypeDef(
    _RequiredAssetModelPropertyDefinitionTypeDef, _OptionalAssetModelPropertyDefinitionTypeDef
):
    pass


_RequiredAssetModelPropertyTypeDef = TypedDict(
    "_RequiredAssetModelPropertyTypeDef",
    {
        "name": str,
        "dataType": PropertyDataTypeType,
        "type": "PropertyTypeTypeDef",
    },
)
_OptionalAssetModelPropertyTypeDef = TypedDict(
    "_OptionalAssetModelPropertyTypeDef",
    {
        "id": str,
        "dataTypeSpec": str,
        "unit": str,
    },
    total=False,
)


class AssetModelPropertyTypeDef(
    _RequiredAssetModelPropertyTypeDef, _OptionalAssetModelPropertyTypeDef
):
    pass


_RequiredAssetModelStatusTypeDef = TypedDict(
    "_RequiredAssetModelStatusTypeDef",
    {
        "state": AssetModelStateType,
    },
)
_OptionalAssetModelStatusTypeDef = TypedDict(
    "_OptionalAssetModelStatusTypeDef",
    {
        "error": "ErrorDetailsTypeDef",
    },
    total=False,
)


class AssetModelStatusTypeDef(_RequiredAssetModelStatusTypeDef, _OptionalAssetModelStatusTypeDef):
    pass


AssetModelSummaryTypeDef = TypedDict(
    "AssetModelSummaryTypeDef",
    {
        "id": str,
        "arn": str,
        "name": str,
        "description": str,
        "creationDate": datetime,
        "lastUpdateDate": datetime,
        "status": "AssetModelStatusTypeDef",
    },
)

_RequiredAssetPropertyTypeDef = TypedDict(
    "_RequiredAssetPropertyTypeDef",
    {
        "id": str,
        "name": str,
        "dataType": PropertyDataTypeType,
    },
)
_OptionalAssetPropertyTypeDef = TypedDict(
    "_OptionalAssetPropertyTypeDef",
    {
        "alias": str,
        "notification": "PropertyNotificationTypeDef",
        "dataTypeSpec": str,
        "unit": str,
    },
    total=False,
)


class AssetPropertyTypeDef(_RequiredAssetPropertyTypeDef, _OptionalAssetPropertyTypeDef):
    pass


_RequiredAssetPropertyValueTypeDef = TypedDict(
    "_RequiredAssetPropertyValueTypeDef",
    {
        "value": "VariantTypeDef",
        "timestamp": "TimeInNanosTypeDef",
    },
)
_OptionalAssetPropertyValueTypeDef = TypedDict(
    "_OptionalAssetPropertyValueTypeDef",
    {
        "quality": QualityType,
    },
    total=False,
)


class AssetPropertyValueTypeDef(
    _RequiredAssetPropertyValueTypeDef, _OptionalAssetPropertyValueTypeDef
):
    pass


_RequiredAssetRelationshipSummaryTypeDef = TypedDict(
    "_RequiredAssetRelationshipSummaryTypeDef",
    {
        "relationshipType": Literal["HIERARCHY"],
    },
)
_OptionalAssetRelationshipSummaryTypeDef = TypedDict(
    "_OptionalAssetRelationshipSummaryTypeDef",
    {
        "hierarchyInfo": "AssetHierarchyInfoTypeDef",
    },
    total=False,
)


class AssetRelationshipSummaryTypeDef(
    _RequiredAssetRelationshipSummaryTypeDef, _OptionalAssetRelationshipSummaryTypeDef
):
    pass


_RequiredAssetStatusTypeDef = TypedDict(
    "_RequiredAssetStatusTypeDef",
    {
        "state": AssetStateType,
    },
)
_OptionalAssetStatusTypeDef = TypedDict(
    "_OptionalAssetStatusTypeDef",
    {
        "error": "ErrorDetailsTypeDef",
    },
    total=False,
)


class AssetStatusTypeDef(_RequiredAssetStatusTypeDef, _OptionalAssetStatusTypeDef):
    pass


AssetSummaryTypeDef = TypedDict(
    "AssetSummaryTypeDef",
    {
        "id": str,
        "arn": str,
        "name": str,
        "assetModelId": str,
        "creationDate": datetime,
        "lastUpdateDate": datetime,
        "status": "AssetStatusTypeDef",
        "hierarchies": List["AssetHierarchyTypeDef"],
    },
)

_RequiredAssociateAssetsRequestRequestTypeDef = TypedDict(
    "_RequiredAssociateAssetsRequestRequestTypeDef",
    {
        "assetId": str,
        "hierarchyId": str,
        "childAssetId": str,
    },
)
_OptionalAssociateAssetsRequestRequestTypeDef = TypedDict(
    "_OptionalAssociateAssetsRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class AssociateAssetsRequestRequestTypeDef(
    _RequiredAssociateAssetsRequestRequestTypeDef, _OptionalAssociateAssetsRequestRequestTypeDef
):
    pass


_RequiredAssociateTimeSeriesToAssetPropertyRequestRequestTypeDef = TypedDict(
    "_RequiredAssociateTimeSeriesToAssetPropertyRequestRequestTypeDef",
    {
        "alias": str,
        "assetId": str,
        "propertyId": str,
    },
)
_OptionalAssociateTimeSeriesToAssetPropertyRequestRequestTypeDef = TypedDict(
    "_OptionalAssociateTimeSeriesToAssetPropertyRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class AssociateTimeSeriesToAssetPropertyRequestRequestTypeDef(
    _RequiredAssociateTimeSeriesToAssetPropertyRequestRequestTypeDef,
    _OptionalAssociateTimeSeriesToAssetPropertyRequestRequestTypeDef,
):
    pass


AssociatedAssetsSummaryTypeDef = TypedDict(
    "AssociatedAssetsSummaryTypeDef",
    {
        "id": str,
        "arn": str,
        "name": str,
        "assetModelId": str,
        "creationDate": datetime,
        "lastUpdateDate": datetime,
        "status": "AssetStatusTypeDef",
        "hierarchies": List["AssetHierarchyTypeDef"],
    },
)

AttributeTypeDef = TypedDict(
    "AttributeTypeDef",
    {
        "defaultValue": str,
    },
    total=False,
)

_RequiredBatchAssociateProjectAssetsRequestRequestTypeDef = TypedDict(
    "_RequiredBatchAssociateProjectAssetsRequestRequestTypeDef",
    {
        "projectId": str,
        "assetIds": Sequence[str],
    },
)
_OptionalBatchAssociateProjectAssetsRequestRequestTypeDef = TypedDict(
    "_OptionalBatchAssociateProjectAssetsRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class BatchAssociateProjectAssetsRequestRequestTypeDef(
    _RequiredBatchAssociateProjectAssetsRequestRequestTypeDef,
    _OptionalBatchAssociateProjectAssetsRequestRequestTypeDef,
):
    pass


BatchAssociateProjectAssetsResponseTypeDef = TypedDict(
    "BatchAssociateProjectAssetsResponseTypeDef",
    {
        "errors": List["AssetErrorDetailsTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredBatchDisassociateProjectAssetsRequestRequestTypeDef = TypedDict(
    "_RequiredBatchDisassociateProjectAssetsRequestRequestTypeDef",
    {
        "projectId": str,
        "assetIds": Sequence[str],
    },
)
_OptionalBatchDisassociateProjectAssetsRequestRequestTypeDef = TypedDict(
    "_OptionalBatchDisassociateProjectAssetsRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class BatchDisassociateProjectAssetsRequestRequestTypeDef(
    _RequiredBatchDisassociateProjectAssetsRequestRequestTypeDef,
    _OptionalBatchDisassociateProjectAssetsRequestRequestTypeDef,
):
    pass


BatchDisassociateProjectAssetsResponseTypeDef = TypedDict(
    "BatchDisassociateProjectAssetsResponseTypeDef",
    {
        "errors": List["AssetErrorDetailsTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredBatchGetAssetPropertyAggregatesEntryTypeDef = TypedDict(
    "_RequiredBatchGetAssetPropertyAggregatesEntryTypeDef",
    {
        "entryId": str,
        "aggregateTypes": Sequence[AggregateTypeType],
        "resolution": str,
        "startDate": Union[datetime, str],
        "endDate": Union[datetime, str],
    },
)
_OptionalBatchGetAssetPropertyAggregatesEntryTypeDef = TypedDict(
    "_OptionalBatchGetAssetPropertyAggregatesEntryTypeDef",
    {
        "assetId": str,
        "propertyId": str,
        "propertyAlias": str,
        "qualities": Sequence[QualityType],
        "timeOrdering": TimeOrderingType,
    },
    total=False,
)


class BatchGetAssetPropertyAggregatesEntryTypeDef(
    _RequiredBatchGetAssetPropertyAggregatesEntryTypeDef,
    _OptionalBatchGetAssetPropertyAggregatesEntryTypeDef,
):
    pass


BatchGetAssetPropertyAggregatesErrorEntryTypeDef = TypedDict(
    "BatchGetAssetPropertyAggregatesErrorEntryTypeDef",
    {
        "errorCode": BatchGetAssetPropertyAggregatesErrorCodeType,
        "errorMessage": str,
        "entryId": str,
    },
)

BatchGetAssetPropertyAggregatesErrorInfoTypeDef = TypedDict(
    "BatchGetAssetPropertyAggregatesErrorInfoTypeDef",
    {
        "errorCode": BatchGetAssetPropertyAggregatesErrorCodeType,
        "errorTimestamp": datetime,
    },
)

_RequiredBatchGetAssetPropertyAggregatesRequestRequestTypeDef = TypedDict(
    "_RequiredBatchGetAssetPropertyAggregatesRequestRequestTypeDef",
    {
        "entries": Sequence["BatchGetAssetPropertyAggregatesEntryTypeDef"],
    },
)
_OptionalBatchGetAssetPropertyAggregatesRequestRequestTypeDef = TypedDict(
    "_OptionalBatchGetAssetPropertyAggregatesRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class BatchGetAssetPropertyAggregatesRequestRequestTypeDef(
    _RequiredBatchGetAssetPropertyAggregatesRequestRequestTypeDef,
    _OptionalBatchGetAssetPropertyAggregatesRequestRequestTypeDef,
):
    pass


BatchGetAssetPropertyAggregatesResponseTypeDef = TypedDict(
    "BatchGetAssetPropertyAggregatesResponseTypeDef",
    {
        "errorEntries": List["BatchGetAssetPropertyAggregatesErrorEntryTypeDef"],
        "successEntries": List["BatchGetAssetPropertyAggregatesSuccessEntryTypeDef"],
        "skippedEntries": List["BatchGetAssetPropertyAggregatesSkippedEntryTypeDef"],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredBatchGetAssetPropertyAggregatesSkippedEntryTypeDef = TypedDict(
    "_RequiredBatchGetAssetPropertyAggregatesSkippedEntryTypeDef",
    {
        "entryId": str,
        "completionStatus": BatchEntryCompletionStatusType,
    },
)
_OptionalBatchGetAssetPropertyAggregatesSkippedEntryTypeDef = TypedDict(
    "_OptionalBatchGetAssetPropertyAggregatesSkippedEntryTypeDef",
    {
        "errorInfo": "BatchGetAssetPropertyAggregatesErrorInfoTypeDef",
    },
    total=False,
)


class BatchGetAssetPropertyAggregatesSkippedEntryTypeDef(
    _RequiredBatchGetAssetPropertyAggregatesSkippedEntryTypeDef,
    _OptionalBatchGetAssetPropertyAggregatesSkippedEntryTypeDef,
):
    pass


BatchGetAssetPropertyAggregatesSuccessEntryTypeDef = TypedDict(
    "BatchGetAssetPropertyAggregatesSuccessEntryTypeDef",
    {
        "entryId": str,
        "aggregatedValues": List["AggregatedValueTypeDef"],
    },
)

_RequiredBatchGetAssetPropertyValueEntryTypeDef = TypedDict(
    "_RequiredBatchGetAssetPropertyValueEntryTypeDef",
    {
        "entryId": str,
    },
)
_OptionalBatchGetAssetPropertyValueEntryTypeDef = TypedDict(
    "_OptionalBatchGetAssetPropertyValueEntryTypeDef",
    {
        "assetId": str,
        "propertyId": str,
        "propertyAlias": str,
    },
    total=False,
)


class BatchGetAssetPropertyValueEntryTypeDef(
    _RequiredBatchGetAssetPropertyValueEntryTypeDef, _OptionalBatchGetAssetPropertyValueEntryTypeDef
):
    pass


BatchGetAssetPropertyValueErrorEntryTypeDef = TypedDict(
    "BatchGetAssetPropertyValueErrorEntryTypeDef",
    {
        "errorCode": BatchGetAssetPropertyValueErrorCodeType,
        "errorMessage": str,
        "entryId": str,
    },
)

BatchGetAssetPropertyValueErrorInfoTypeDef = TypedDict(
    "BatchGetAssetPropertyValueErrorInfoTypeDef",
    {
        "errorCode": BatchGetAssetPropertyValueErrorCodeType,
        "errorTimestamp": datetime,
    },
)

_RequiredBatchGetAssetPropertyValueHistoryEntryTypeDef = TypedDict(
    "_RequiredBatchGetAssetPropertyValueHistoryEntryTypeDef",
    {
        "entryId": str,
    },
)
_OptionalBatchGetAssetPropertyValueHistoryEntryTypeDef = TypedDict(
    "_OptionalBatchGetAssetPropertyValueHistoryEntryTypeDef",
    {
        "assetId": str,
        "propertyId": str,
        "propertyAlias": str,
        "startDate": Union[datetime, str],
        "endDate": Union[datetime, str],
        "qualities": Sequence[QualityType],
        "timeOrdering": TimeOrderingType,
    },
    total=False,
)


class BatchGetAssetPropertyValueHistoryEntryTypeDef(
    _RequiredBatchGetAssetPropertyValueHistoryEntryTypeDef,
    _OptionalBatchGetAssetPropertyValueHistoryEntryTypeDef,
):
    pass


BatchGetAssetPropertyValueHistoryErrorEntryTypeDef = TypedDict(
    "BatchGetAssetPropertyValueHistoryErrorEntryTypeDef",
    {
        "errorCode": BatchGetAssetPropertyValueHistoryErrorCodeType,
        "errorMessage": str,
        "entryId": str,
    },
)

BatchGetAssetPropertyValueHistoryErrorInfoTypeDef = TypedDict(
    "BatchGetAssetPropertyValueHistoryErrorInfoTypeDef",
    {
        "errorCode": BatchGetAssetPropertyValueHistoryErrorCodeType,
        "errorTimestamp": datetime,
    },
)

_RequiredBatchGetAssetPropertyValueHistoryRequestRequestTypeDef = TypedDict(
    "_RequiredBatchGetAssetPropertyValueHistoryRequestRequestTypeDef",
    {
        "entries": Sequence["BatchGetAssetPropertyValueHistoryEntryTypeDef"],
    },
)
_OptionalBatchGetAssetPropertyValueHistoryRequestRequestTypeDef = TypedDict(
    "_OptionalBatchGetAssetPropertyValueHistoryRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class BatchGetAssetPropertyValueHistoryRequestRequestTypeDef(
    _RequiredBatchGetAssetPropertyValueHistoryRequestRequestTypeDef,
    _OptionalBatchGetAssetPropertyValueHistoryRequestRequestTypeDef,
):
    pass


BatchGetAssetPropertyValueHistoryResponseTypeDef = TypedDict(
    "BatchGetAssetPropertyValueHistoryResponseTypeDef",
    {
        "errorEntries": List["BatchGetAssetPropertyValueHistoryErrorEntryTypeDef"],
        "successEntries": List["BatchGetAssetPropertyValueHistorySuccessEntryTypeDef"],
        "skippedEntries": List["BatchGetAssetPropertyValueHistorySkippedEntryTypeDef"],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredBatchGetAssetPropertyValueHistorySkippedEntryTypeDef = TypedDict(
    "_RequiredBatchGetAssetPropertyValueHistorySkippedEntryTypeDef",
    {
        "entryId": str,
        "completionStatus": BatchEntryCompletionStatusType,
    },
)
_OptionalBatchGetAssetPropertyValueHistorySkippedEntryTypeDef = TypedDict(
    "_OptionalBatchGetAssetPropertyValueHistorySkippedEntryTypeDef",
    {
        "errorInfo": "BatchGetAssetPropertyValueHistoryErrorInfoTypeDef",
    },
    total=False,
)


class BatchGetAssetPropertyValueHistorySkippedEntryTypeDef(
    _RequiredBatchGetAssetPropertyValueHistorySkippedEntryTypeDef,
    _OptionalBatchGetAssetPropertyValueHistorySkippedEntryTypeDef,
):
    pass


BatchGetAssetPropertyValueHistorySuccessEntryTypeDef = TypedDict(
    "BatchGetAssetPropertyValueHistorySuccessEntryTypeDef",
    {
        "entryId": str,
        "assetPropertyValueHistory": List["AssetPropertyValueTypeDef"],
    },
)

_RequiredBatchGetAssetPropertyValueRequestRequestTypeDef = TypedDict(
    "_RequiredBatchGetAssetPropertyValueRequestRequestTypeDef",
    {
        "entries": Sequence["BatchGetAssetPropertyValueEntryTypeDef"],
    },
)
_OptionalBatchGetAssetPropertyValueRequestRequestTypeDef = TypedDict(
    "_OptionalBatchGetAssetPropertyValueRequestRequestTypeDef",
    {
        "nextToken": str,
    },
    total=False,
)


class BatchGetAssetPropertyValueRequestRequestTypeDef(
    _RequiredBatchGetAssetPropertyValueRequestRequestTypeDef,
    _OptionalBatchGetAssetPropertyValueRequestRequestTypeDef,
):
    pass


BatchGetAssetPropertyValueResponseTypeDef = TypedDict(
    "BatchGetAssetPropertyValueResponseTypeDef",
    {
        "errorEntries": List["BatchGetAssetPropertyValueErrorEntryTypeDef"],
        "successEntries": List["BatchGetAssetPropertyValueSuccessEntryTypeDef"],
        "skippedEntries": List["BatchGetAssetPropertyValueSkippedEntryTypeDef"],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredBatchGetAssetPropertyValueSkippedEntryTypeDef = TypedDict(
    "_RequiredBatchGetAssetPropertyValueSkippedEntryTypeDef",
    {
        "entryId": str,
        "completionStatus": BatchEntryCompletionStatusType,
    },
)
_OptionalBatchGetAssetPropertyValueSkippedEntryTypeDef = TypedDict(
    "_OptionalBatchGetAssetPropertyValueSkippedEntryTypeDef",
    {
        "errorInfo": "BatchGetAssetPropertyValueErrorInfoTypeDef",
    },
    total=False,
)


class BatchGetAssetPropertyValueSkippedEntryTypeDef(
    _RequiredBatchGetAssetPropertyValueSkippedEntryTypeDef,
    _OptionalBatchGetAssetPropertyValueSkippedEntryTypeDef,
):
    pass


_RequiredBatchGetAssetPropertyValueSuccessEntryTypeDef = TypedDict(
    "_RequiredBatchGetAssetPropertyValueSuccessEntryTypeDef",
    {
        "entryId": str,
    },
)
_OptionalBatchGetAssetPropertyValueSuccessEntryTypeDef = TypedDict(
    "_OptionalBatchGetAssetPropertyValueSuccessEntryTypeDef",
    {
        "assetPropertyValue": "AssetPropertyValueTypeDef",
    },
    total=False,
)


class BatchGetAssetPropertyValueSuccessEntryTypeDef(
    _RequiredBatchGetAssetPropertyValueSuccessEntryTypeDef,
    _OptionalBatchGetAssetPropertyValueSuccessEntryTypeDef,
):
    pass


BatchPutAssetPropertyErrorEntryTypeDef = TypedDict(
    "BatchPutAssetPropertyErrorEntryTypeDef",
    {
        "entryId": str,
        "errors": List["BatchPutAssetPropertyErrorTypeDef"],
    },
)

BatchPutAssetPropertyErrorTypeDef = TypedDict(
    "BatchPutAssetPropertyErrorTypeDef",
    {
        "errorCode": BatchPutAssetPropertyValueErrorCodeType,
        "errorMessage": str,
        "timestamps": List["TimeInNanosTypeDef"],
    },
)

BatchPutAssetPropertyValueRequestRequestTypeDef = TypedDict(
    "BatchPutAssetPropertyValueRequestRequestTypeDef",
    {
        "entries": Sequence["PutAssetPropertyValueEntryTypeDef"],
    },
)

BatchPutAssetPropertyValueResponseTypeDef = TypedDict(
    "BatchPutAssetPropertyValueResponseTypeDef",
    {
        "errorEntries": List["BatchPutAssetPropertyErrorEntryTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CompositeModelPropertyTypeDef = TypedDict(
    "CompositeModelPropertyTypeDef",
    {
        "name": str,
        "type": str,
        "assetProperty": "PropertyTypeDef",
    },
)

ConfigurationErrorDetailsTypeDef = TypedDict(
    "ConfigurationErrorDetailsTypeDef",
    {
        "code": ErrorCodeType,
        "message": str,
    },
)

_RequiredConfigurationStatusTypeDef = TypedDict(
    "_RequiredConfigurationStatusTypeDef",
    {
        "state": ConfigurationStateType,
    },
)
_OptionalConfigurationStatusTypeDef = TypedDict(
    "_OptionalConfigurationStatusTypeDef",
    {
        "error": "ConfigurationErrorDetailsTypeDef",
    },
    total=False,
)


class ConfigurationStatusTypeDef(
    _RequiredConfigurationStatusTypeDef, _OptionalConfigurationStatusTypeDef
):
    pass


_RequiredCreateAccessPolicyRequestRequestTypeDef = TypedDict(
    "_RequiredCreateAccessPolicyRequestRequestTypeDef",
    {
        "accessPolicyIdentity": "IdentityTypeDef",
        "accessPolicyResource": "ResourceTypeDef",
        "accessPolicyPermission": PermissionType,
    },
)
_OptionalCreateAccessPolicyRequestRequestTypeDef = TypedDict(
    "_OptionalCreateAccessPolicyRequestRequestTypeDef",
    {
        "clientToken": str,
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateAccessPolicyRequestRequestTypeDef(
    _RequiredCreateAccessPolicyRequestRequestTypeDef,
    _OptionalCreateAccessPolicyRequestRequestTypeDef,
):
    pass


CreateAccessPolicyResponseTypeDef = TypedDict(
    "CreateAccessPolicyResponseTypeDef",
    {
        "accessPolicyId": str,
        "accessPolicyArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateAssetModelRequestRequestTypeDef = TypedDict(
    "_RequiredCreateAssetModelRequestRequestTypeDef",
    {
        "assetModelName": str,
    },
)
_OptionalCreateAssetModelRequestRequestTypeDef = TypedDict(
    "_OptionalCreateAssetModelRequestRequestTypeDef",
    {
        "assetModelDescription": str,
        "assetModelProperties": Sequence["AssetModelPropertyDefinitionTypeDef"],
        "assetModelHierarchies": Sequence["AssetModelHierarchyDefinitionTypeDef"],
        "assetModelCompositeModels": Sequence["AssetModelCompositeModelDefinitionTypeDef"],
        "clientToken": str,
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateAssetModelRequestRequestTypeDef(
    _RequiredCreateAssetModelRequestRequestTypeDef, _OptionalCreateAssetModelRequestRequestTypeDef
):
    pass


CreateAssetModelResponseTypeDef = TypedDict(
    "CreateAssetModelResponseTypeDef",
    {
        "assetModelId": str,
        "assetModelArn": str,
        "assetModelStatus": "AssetModelStatusTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateAssetRequestRequestTypeDef = TypedDict(
    "_RequiredCreateAssetRequestRequestTypeDef",
    {
        "assetName": str,
        "assetModelId": str,
    },
)
_OptionalCreateAssetRequestRequestTypeDef = TypedDict(
    "_OptionalCreateAssetRequestRequestTypeDef",
    {
        "clientToken": str,
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateAssetRequestRequestTypeDef(
    _RequiredCreateAssetRequestRequestTypeDef, _OptionalCreateAssetRequestRequestTypeDef
):
    pass


CreateAssetResponseTypeDef = TypedDict(
    "CreateAssetResponseTypeDef",
    {
        "assetId": str,
        "assetArn": str,
        "assetStatus": "AssetStatusTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateDashboardRequestRequestTypeDef = TypedDict(
    "_RequiredCreateDashboardRequestRequestTypeDef",
    {
        "projectId": str,
        "dashboardName": str,
        "dashboardDefinition": str,
    },
)
_OptionalCreateDashboardRequestRequestTypeDef = TypedDict(
    "_OptionalCreateDashboardRequestRequestTypeDef",
    {
        "dashboardDescription": str,
        "clientToken": str,
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateDashboardRequestRequestTypeDef(
    _RequiredCreateDashboardRequestRequestTypeDef, _OptionalCreateDashboardRequestRequestTypeDef
):
    pass


CreateDashboardResponseTypeDef = TypedDict(
    "CreateDashboardResponseTypeDef",
    {
        "dashboardId": str,
        "dashboardArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateGatewayRequestRequestTypeDef = TypedDict(
    "_RequiredCreateGatewayRequestRequestTypeDef",
    {
        "gatewayName": str,
        "gatewayPlatform": "GatewayPlatformTypeDef",
    },
)
_OptionalCreateGatewayRequestRequestTypeDef = TypedDict(
    "_OptionalCreateGatewayRequestRequestTypeDef",
    {
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateGatewayRequestRequestTypeDef(
    _RequiredCreateGatewayRequestRequestTypeDef, _OptionalCreateGatewayRequestRequestTypeDef
):
    pass


CreateGatewayResponseTypeDef = TypedDict(
    "CreateGatewayResponseTypeDef",
    {
        "gatewayId": str,
        "gatewayArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreatePortalRequestRequestTypeDef = TypedDict(
    "_RequiredCreatePortalRequestRequestTypeDef",
    {
        "portalName": str,
        "portalContactEmail": str,
        "roleArn": str,
    },
)
_OptionalCreatePortalRequestRequestTypeDef = TypedDict(
    "_OptionalCreatePortalRequestRequestTypeDef",
    {
        "portalDescription": str,
        "clientToken": str,
        "portalLogoImageFile": "ImageFileTypeDef",
        "tags": Mapping[str, str],
        "portalAuthMode": AuthModeType,
        "notificationSenderEmail": str,
        "alarms": "AlarmsTypeDef",
    },
    total=False,
)


class CreatePortalRequestRequestTypeDef(
    _RequiredCreatePortalRequestRequestTypeDef, _OptionalCreatePortalRequestRequestTypeDef
):
    pass


CreatePortalResponseTypeDef = TypedDict(
    "CreatePortalResponseTypeDef",
    {
        "portalId": str,
        "portalArn": str,
        "portalStartUrl": str,
        "portalStatus": "PortalStatusTypeDef",
        "ssoApplicationId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateProjectRequestRequestTypeDef = TypedDict(
    "_RequiredCreateProjectRequestRequestTypeDef",
    {
        "portalId": str,
        "projectName": str,
    },
)
_OptionalCreateProjectRequestRequestTypeDef = TypedDict(
    "_OptionalCreateProjectRequestRequestTypeDef",
    {
        "projectDescription": str,
        "clientToken": str,
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateProjectRequestRequestTypeDef(
    _RequiredCreateProjectRequestRequestTypeDef, _OptionalCreateProjectRequestRequestTypeDef
):
    pass


CreateProjectResponseTypeDef = TypedDict(
    "CreateProjectResponseTypeDef",
    {
        "projectId": str,
        "projectArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CustomerManagedS3StorageTypeDef = TypedDict(
    "CustomerManagedS3StorageTypeDef",
    {
        "s3ResourceArn": str,
        "roleArn": str,
    },
)

_RequiredDashboardSummaryTypeDef = TypedDict(
    "_RequiredDashboardSummaryTypeDef",
    {
        "id": str,
        "name": str,
    },
)
_OptionalDashboardSummaryTypeDef = TypedDict(
    "_OptionalDashboardSummaryTypeDef",
    {
        "description": str,
        "creationDate": datetime,
        "lastUpdateDate": datetime,
    },
    total=False,
)


class DashboardSummaryTypeDef(_RequiredDashboardSummaryTypeDef, _OptionalDashboardSummaryTypeDef):
    pass


_RequiredDeleteAccessPolicyRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteAccessPolicyRequestRequestTypeDef",
    {
        "accessPolicyId": str,
    },
)
_OptionalDeleteAccessPolicyRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteAccessPolicyRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class DeleteAccessPolicyRequestRequestTypeDef(
    _RequiredDeleteAccessPolicyRequestRequestTypeDef,
    _OptionalDeleteAccessPolicyRequestRequestTypeDef,
):
    pass


_RequiredDeleteAssetModelRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteAssetModelRequestRequestTypeDef",
    {
        "assetModelId": str,
    },
)
_OptionalDeleteAssetModelRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteAssetModelRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class DeleteAssetModelRequestRequestTypeDef(
    _RequiredDeleteAssetModelRequestRequestTypeDef, _OptionalDeleteAssetModelRequestRequestTypeDef
):
    pass


DeleteAssetModelResponseTypeDef = TypedDict(
    "DeleteAssetModelResponseTypeDef",
    {
        "assetModelStatus": "AssetModelStatusTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredDeleteAssetRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteAssetRequestRequestTypeDef",
    {
        "assetId": str,
    },
)
_OptionalDeleteAssetRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteAssetRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class DeleteAssetRequestRequestTypeDef(
    _RequiredDeleteAssetRequestRequestTypeDef, _OptionalDeleteAssetRequestRequestTypeDef
):
    pass


DeleteAssetResponseTypeDef = TypedDict(
    "DeleteAssetResponseTypeDef",
    {
        "assetStatus": "AssetStatusTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredDeleteDashboardRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteDashboardRequestRequestTypeDef",
    {
        "dashboardId": str,
    },
)
_OptionalDeleteDashboardRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteDashboardRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class DeleteDashboardRequestRequestTypeDef(
    _RequiredDeleteDashboardRequestRequestTypeDef, _OptionalDeleteDashboardRequestRequestTypeDef
):
    pass


DeleteGatewayRequestRequestTypeDef = TypedDict(
    "DeleteGatewayRequestRequestTypeDef",
    {
        "gatewayId": str,
    },
)

_RequiredDeletePortalRequestRequestTypeDef = TypedDict(
    "_RequiredDeletePortalRequestRequestTypeDef",
    {
        "portalId": str,
    },
)
_OptionalDeletePortalRequestRequestTypeDef = TypedDict(
    "_OptionalDeletePortalRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class DeletePortalRequestRequestTypeDef(
    _RequiredDeletePortalRequestRequestTypeDef, _OptionalDeletePortalRequestRequestTypeDef
):
    pass


DeletePortalResponseTypeDef = TypedDict(
    "DeletePortalResponseTypeDef",
    {
        "portalStatus": "PortalStatusTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredDeleteProjectRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteProjectRequestRequestTypeDef",
    {
        "projectId": str,
    },
)
_OptionalDeleteProjectRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteProjectRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class DeleteProjectRequestRequestTypeDef(
    _RequiredDeleteProjectRequestRequestTypeDef, _OptionalDeleteProjectRequestRequestTypeDef
):
    pass


DeleteTimeSeriesRequestRequestTypeDef = TypedDict(
    "DeleteTimeSeriesRequestRequestTypeDef",
    {
        "alias": str,
        "assetId": str,
        "propertyId": str,
        "clientToken": str,
    },
    total=False,
)

DescribeAccessPolicyRequestRequestTypeDef = TypedDict(
    "DescribeAccessPolicyRequestRequestTypeDef",
    {
        "accessPolicyId": str,
    },
)

DescribeAccessPolicyResponseTypeDef = TypedDict(
    "DescribeAccessPolicyResponseTypeDef",
    {
        "accessPolicyId": str,
        "accessPolicyArn": str,
        "accessPolicyIdentity": "IdentityTypeDef",
        "accessPolicyResource": "ResourceTypeDef",
        "accessPolicyPermission": PermissionType,
        "accessPolicyCreationDate": datetime,
        "accessPolicyLastUpdateDate": datetime,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredDescribeAssetModelRequestAssetModelActiveWaitTypeDef = TypedDict(
    "_RequiredDescribeAssetModelRequestAssetModelActiveWaitTypeDef",
    {
        "assetModelId": str,
    },
)
_OptionalDescribeAssetModelRequestAssetModelActiveWaitTypeDef = TypedDict(
    "_OptionalDescribeAssetModelRequestAssetModelActiveWaitTypeDef",
    {
        "WaiterConfig": "WaiterConfigTypeDef",
    },
    total=False,
)


class DescribeAssetModelRequestAssetModelActiveWaitTypeDef(
    _RequiredDescribeAssetModelRequestAssetModelActiveWaitTypeDef,
    _OptionalDescribeAssetModelRequestAssetModelActiveWaitTypeDef,
):
    pass


_RequiredDescribeAssetModelRequestAssetModelNotExistsWaitTypeDef = TypedDict(
    "_RequiredDescribeAssetModelRequestAssetModelNotExistsWaitTypeDef",
    {
        "assetModelId": str,
    },
)
_OptionalDescribeAssetModelRequestAssetModelNotExistsWaitTypeDef = TypedDict(
    "_OptionalDescribeAssetModelRequestAssetModelNotExistsWaitTypeDef",
    {
        "WaiterConfig": "WaiterConfigTypeDef",
    },
    total=False,
)


class DescribeAssetModelRequestAssetModelNotExistsWaitTypeDef(
    _RequiredDescribeAssetModelRequestAssetModelNotExistsWaitTypeDef,
    _OptionalDescribeAssetModelRequestAssetModelNotExistsWaitTypeDef,
):
    pass


DescribeAssetModelRequestRequestTypeDef = TypedDict(
    "DescribeAssetModelRequestRequestTypeDef",
    {
        "assetModelId": str,
    },
)

DescribeAssetModelResponseTypeDef = TypedDict(
    "DescribeAssetModelResponseTypeDef",
    {
        "assetModelId": str,
        "assetModelArn": str,
        "assetModelName": str,
        "assetModelDescription": str,
        "assetModelProperties": List["AssetModelPropertyTypeDef"],
        "assetModelHierarchies": List["AssetModelHierarchyTypeDef"],
        "assetModelCompositeModels": List["AssetModelCompositeModelTypeDef"],
        "assetModelCreationDate": datetime,
        "assetModelLastUpdateDate": datetime,
        "assetModelStatus": "AssetModelStatusTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeAssetPropertyRequestRequestTypeDef = TypedDict(
    "DescribeAssetPropertyRequestRequestTypeDef",
    {
        "assetId": str,
        "propertyId": str,
    },
)

DescribeAssetPropertyResponseTypeDef = TypedDict(
    "DescribeAssetPropertyResponseTypeDef",
    {
        "assetId": str,
        "assetName": str,
        "assetModelId": str,
        "assetProperty": "PropertyTypeDef",
        "compositeModel": "CompositeModelPropertyTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredDescribeAssetRequestAssetActiveWaitTypeDef = TypedDict(
    "_RequiredDescribeAssetRequestAssetActiveWaitTypeDef",
    {
        "assetId": str,
    },
)
_OptionalDescribeAssetRequestAssetActiveWaitTypeDef = TypedDict(
    "_OptionalDescribeAssetRequestAssetActiveWaitTypeDef",
    {
        "WaiterConfig": "WaiterConfigTypeDef",
    },
    total=False,
)


class DescribeAssetRequestAssetActiveWaitTypeDef(
    _RequiredDescribeAssetRequestAssetActiveWaitTypeDef,
    _OptionalDescribeAssetRequestAssetActiveWaitTypeDef,
):
    pass


_RequiredDescribeAssetRequestAssetNotExistsWaitTypeDef = TypedDict(
    "_RequiredDescribeAssetRequestAssetNotExistsWaitTypeDef",
    {
        "assetId": str,
    },
)
_OptionalDescribeAssetRequestAssetNotExistsWaitTypeDef = TypedDict(
    "_OptionalDescribeAssetRequestAssetNotExistsWaitTypeDef",
    {
        "WaiterConfig": "WaiterConfigTypeDef",
    },
    total=False,
)


class DescribeAssetRequestAssetNotExistsWaitTypeDef(
    _RequiredDescribeAssetRequestAssetNotExistsWaitTypeDef,
    _OptionalDescribeAssetRequestAssetNotExistsWaitTypeDef,
):
    pass


DescribeAssetRequestRequestTypeDef = TypedDict(
    "DescribeAssetRequestRequestTypeDef",
    {
        "assetId": str,
    },
)

DescribeAssetResponseTypeDef = TypedDict(
    "DescribeAssetResponseTypeDef",
    {
        "assetId": str,
        "assetArn": str,
        "assetName": str,
        "assetModelId": str,
        "assetProperties": List["AssetPropertyTypeDef"],
        "assetHierarchies": List["AssetHierarchyTypeDef"],
        "assetCompositeModels": List["AssetCompositeModelTypeDef"],
        "assetCreationDate": datetime,
        "assetLastUpdateDate": datetime,
        "assetStatus": "AssetStatusTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeDashboardRequestRequestTypeDef = TypedDict(
    "DescribeDashboardRequestRequestTypeDef",
    {
        "dashboardId": str,
    },
)

DescribeDashboardResponseTypeDef = TypedDict(
    "DescribeDashboardResponseTypeDef",
    {
        "dashboardId": str,
        "dashboardArn": str,
        "dashboardName": str,
        "projectId": str,
        "dashboardDescription": str,
        "dashboardDefinition": str,
        "dashboardCreationDate": datetime,
        "dashboardLastUpdateDate": datetime,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeDefaultEncryptionConfigurationResponseTypeDef = TypedDict(
    "DescribeDefaultEncryptionConfigurationResponseTypeDef",
    {
        "encryptionType": EncryptionTypeType,
        "kmsKeyArn": str,
        "configurationStatus": "ConfigurationStatusTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeGatewayCapabilityConfigurationRequestRequestTypeDef = TypedDict(
    "DescribeGatewayCapabilityConfigurationRequestRequestTypeDef",
    {
        "gatewayId": str,
        "capabilityNamespace": str,
    },
)

DescribeGatewayCapabilityConfigurationResponseTypeDef = TypedDict(
    "DescribeGatewayCapabilityConfigurationResponseTypeDef",
    {
        "gatewayId": str,
        "capabilityNamespace": str,
        "capabilityConfiguration": str,
        "capabilitySyncStatus": CapabilitySyncStatusType,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeGatewayRequestRequestTypeDef = TypedDict(
    "DescribeGatewayRequestRequestTypeDef",
    {
        "gatewayId": str,
    },
)

DescribeGatewayResponseTypeDef = TypedDict(
    "DescribeGatewayResponseTypeDef",
    {
        "gatewayId": str,
        "gatewayName": str,
        "gatewayArn": str,
        "gatewayPlatform": "GatewayPlatformTypeDef",
        "gatewayCapabilitySummaries": List["GatewayCapabilitySummaryTypeDef"],
        "creationDate": datetime,
        "lastUpdateDate": datetime,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeLoggingOptionsResponseTypeDef = TypedDict(
    "DescribeLoggingOptionsResponseTypeDef",
    {
        "loggingOptions": "LoggingOptionsTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredDescribePortalRequestPortalActiveWaitTypeDef = TypedDict(
    "_RequiredDescribePortalRequestPortalActiveWaitTypeDef",
    {
        "portalId": str,
    },
)
_OptionalDescribePortalRequestPortalActiveWaitTypeDef = TypedDict(
    "_OptionalDescribePortalRequestPortalActiveWaitTypeDef",
    {
        "WaiterConfig": "WaiterConfigTypeDef",
    },
    total=False,
)


class DescribePortalRequestPortalActiveWaitTypeDef(
    _RequiredDescribePortalRequestPortalActiveWaitTypeDef,
    _OptionalDescribePortalRequestPortalActiveWaitTypeDef,
):
    pass


_RequiredDescribePortalRequestPortalNotExistsWaitTypeDef = TypedDict(
    "_RequiredDescribePortalRequestPortalNotExistsWaitTypeDef",
    {
        "portalId": str,
    },
)
_OptionalDescribePortalRequestPortalNotExistsWaitTypeDef = TypedDict(
    "_OptionalDescribePortalRequestPortalNotExistsWaitTypeDef",
    {
        "WaiterConfig": "WaiterConfigTypeDef",
    },
    total=False,
)


class DescribePortalRequestPortalNotExistsWaitTypeDef(
    _RequiredDescribePortalRequestPortalNotExistsWaitTypeDef,
    _OptionalDescribePortalRequestPortalNotExistsWaitTypeDef,
):
    pass


DescribePortalRequestRequestTypeDef = TypedDict(
    "DescribePortalRequestRequestTypeDef",
    {
        "portalId": str,
    },
)

DescribePortalResponseTypeDef = TypedDict(
    "DescribePortalResponseTypeDef",
    {
        "portalId": str,
        "portalArn": str,
        "portalName": str,
        "portalDescription": str,
        "portalClientId": str,
        "portalStartUrl": str,
        "portalContactEmail": str,
        "portalStatus": "PortalStatusTypeDef",
        "portalCreationDate": datetime,
        "portalLastUpdateDate": datetime,
        "portalLogoImageLocation": "ImageLocationTypeDef",
        "roleArn": str,
        "portalAuthMode": AuthModeType,
        "notificationSenderEmail": str,
        "alarms": "AlarmsTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeProjectRequestRequestTypeDef = TypedDict(
    "DescribeProjectRequestRequestTypeDef",
    {
        "projectId": str,
    },
)

DescribeProjectResponseTypeDef = TypedDict(
    "DescribeProjectResponseTypeDef",
    {
        "projectId": str,
        "projectArn": str,
        "projectName": str,
        "portalId": str,
        "projectDescription": str,
        "projectCreationDate": datetime,
        "projectLastUpdateDate": datetime,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeStorageConfigurationResponseTypeDef = TypedDict(
    "DescribeStorageConfigurationResponseTypeDef",
    {
        "storageType": StorageTypeType,
        "multiLayerStorage": "MultiLayerStorageTypeDef",
        "disassociatedDataStorage": DisassociatedDataStorageStateType,
        "retentionPeriod": "RetentionPeriodTypeDef",
        "configurationStatus": "ConfigurationStatusTypeDef",
        "lastUpdateDate": datetime,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeTimeSeriesRequestRequestTypeDef = TypedDict(
    "DescribeTimeSeriesRequestRequestTypeDef",
    {
        "alias": str,
        "assetId": str,
        "propertyId": str,
    },
    total=False,
)

DescribeTimeSeriesResponseTypeDef = TypedDict(
    "DescribeTimeSeriesResponseTypeDef",
    {
        "assetId": str,
        "propertyId": str,
        "alias": str,
        "timeSeriesId": str,
        "dataType": PropertyDataTypeType,
        "dataTypeSpec": str,
        "timeSeriesCreationDate": datetime,
        "timeSeriesLastUpdateDate": datetime,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DetailedErrorTypeDef = TypedDict(
    "DetailedErrorTypeDef",
    {
        "code": DetailedErrorCodeType,
        "message": str,
    },
)

_RequiredDisassociateAssetsRequestRequestTypeDef = TypedDict(
    "_RequiredDisassociateAssetsRequestRequestTypeDef",
    {
        "assetId": str,
        "hierarchyId": str,
        "childAssetId": str,
    },
)
_OptionalDisassociateAssetsRequestRequestTypeDef = TypedDict(
    "_OptionalDisassociateAssetsRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class DisassociateAssetsRequestRequestTypeDef(
    _RequiredDisassociateAssetsRequestRequestTypeDef,
    _OptionalDisassociateAssetsRequestRequestTypeDef,
):
    pass


_RequiredDisassociateTimeSeriesFromAssetPropertyRequestRequestTypeDef = TypedDict(
    "_RequiredDisassociateTimeSeriesFromAssetPropertyRequestRequestTypeDef",
    {
        "alias": str,
        "assetId": str,
        "propertyId": str,
    },
)
_OptionalDisassociateTimeSeriesFromAssetPropertyRequestRequestTypeDef = TypedDict(
    "_OptionalDisassociateTimeSeriesFromAssetPropertyRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class DisassociateTimeSeriesFromAssetPropertyRequestRequestTypeDef(
    _RequiredDisassociateTimeSeriesFromAssetPropertyRequestRequestTypeDef,
    _OptionalDisassociateTimeSeriesFromAssetPropertyRequestRequestTypeDef,
):
    pass


_RequiredErrorDetailsTypeDef = TypedDict(
    "_RequiredErrorDetailsTypeDef",
    {
        "code": ErrorCodeType,
        "message": str,
    },
)
_OptionalErrorDetailsTypeDef = TypedDict(
    "_OptionalErrorDetailsTypeDef",
    {
        "details": List["DetailedErrorTypeDef"],
    },
    total=False,
)


class ErrorDetailsTypeDef(_RequiredErrorDetailsTypeDef, _OptionalErrorDetailsTypeDef):
    pass


ExpressionVariableTypeDef = TypedDict(
    "ExpressionVariableTypeDef",
    {
        "name": str,
        "value": "VariableValueTypeDef",
    },
)

ForwardingConfigTypeDef = TypedDict(
    "ForwardingConfigTypeDef",
    {
        "state": ForwardingConfigStateType,
    },
)

GatewayCapabilitySummaryTypeDef = TypedDict(
    "GatewayCapabilitySummaryTypeDef",
    {
        "capabilityNamespace": str,
        "capabilitySyncStatus": CapabilitySyncStatusType,
    },
)

GatewayPlatformTypeDef = TypedDict(
    "GatewayPlatformTypeDef",
    {
        "greengrass": "GreengrassTypeDef",
        "greengrassV2": "GreengrassV2TypeDef",
    },
    total=False,
)

_RequiredGatewaySummaryTypeDef = TypedDict(
    "_RequiredGatewaySummaryTypeDef",
    {
        "gatewayId": str,
        "gatewayName": str,
        "creationDate": datetime,
        "lastUpdateDate": datetime,
    },
)
_OptionalGatewaySummaryTypeDef = TypedDict(
    "_OptionalGatewaySummaryTypeDef",
    {
        "gatewayPlatform": "GatewayPlatformTypeDef",
        "gatewayCapabilitySummaries": List["GatewayCapabilitySummaryTypeDef"],
    },
    total=False,
)


class GatewaySummaryTypeDef(_RequiredGatewaySummaryTypeDef, _OptionalGatewaySummaryTypeDef):
    pass


_RequiredGetAssetPropertyAggregatesRequestGetAssetPropertyAggregatesPaginateTypeDef = TypedDict(
    "_RequiredGetAssetPropertyAggregatesRequestGetAssetPropertyAggregatesPaginateTypeDef",
    {
        "aggregateTypes": Sequence[AggregateTypeType],
        "resolution": str,
        "startDate": Union[datetime, str],
        "endDate": Union[datetime, str],
    },
)
_OptionalGetAssetPropertyAggregatesRequestGetAssetPropertyAggregatesPaginateTypeDef = TypedDict(
    "_OptionalGetAssetPropertyAggregatesRequestGetAssetPropertyAggregatesPaginateTypeDef",
    {
        "assetId": str,
        "propertyId": str,
        "propertyAlias": str,
        "qualities": Sequence[QualityType],
        "timeOrdering": TimeOrderingType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class GetAssetPropertyAggregatesRequestGetAssetPropertyAggregatesPaginateTypeDef(
    _RequiredGetAssetPropertyAggregatesRequestGetAssetPropertyAggregatesPaginateTypeDef,
    _OptionalGetAssetPropertyAggregatesRequestGetAssetPropertyAggregatesPaginateTypeDef,
):
    pass


_RequiredGetAssetPropertyAggregatesRequestRequestTypeDef = TypedDict(
    "_RequiredGetAssetPropertyAggregatesRequestRequestTypeDef",
    {
        "aggregateTypes": Sequence[AggregateTypeType],
        "resolution": str,
        "startDate": Union[datetime, str],
        "endDate": Union[datetime, str],
    },
)
_OptionalGetAssetPropertyAggregatesRequestRequestTypeDef = TypedDict(
    "_OptionalGetAssetPropertyAggregatesRequestRequestTypeDef",
    {
        "assetId": str,
        "propertyId": str,
        "propertyAlias": str,
        "qualities": Sequence[QualityType],
        "timeOrdering": TimeOrderingType,
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class GetAssetPropertyAggregatesRequestRequestTypeDef(
    _RequiredGetAssetPropertyAggregatesRequestRequestTypeDef,
    _OptionalGetAssetPropertyAggregatesRequestRequestTypeDef,
):
    pass


GetAssetPropertyAggregatesResponseTypeDef = TypedDict(
    "GetAssetPropertyAggregatesResponseTypeDef",
    {
        "aggregatedValues": List["AggregatedValueTypeDef"],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetAssetPropertyValueHistoryRequestGetAssetPropertyValueHistoryPaginateTypeDef = TypedDict(
    "GetAssetPropertyValueHistoryRequestGetAssetPropertyValueHistoryPaginateTypeDef",
    {
        "assetId": str,
        "propertyId": str,
        "propertyAlias": str,
        "startDate": Union[datetime, str],
        "endDate": Union[datetime, str],
        "qualities": Sequence[QualityType],
        "timeOrdering": TimeOrderingType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

GetAssetPropertyValueHistoryRequestRequestTypeDef = TypedDict(
    "GetAssetPropertyValueHistoryRequestRequestTypeDef",
    {
        "assetId": str,
        "propertyId": str,
        "propertyAlias": str,
        "startDate": Union[datetime, str],
        "endDate": Union[datetime, str],
        "qualities": Sequence[QualityType],
        "timeOrdering": TimeOrderingType,
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

GetAssetPropertyValueHistoryResponseTypeDef = TypedDict(
    "GetAssetPropertyValueHistoryResponseTypeDef",
    {
        "assetPropertyValueHistory": List["AssetPropertyValueTypeDef"],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetAssetPropertyValueRequestRequestTypeDef = TypedDict(
    "GetAssetPropertyValueRequestRequestTypeDef",
    {
        "assetId": str,
        "propertyId": str,
        "propertyAlias": str,
    },
    total=False,
)

GetAssetPropertyValueResponseTypeDef = TypedDict(
    "GetAssetPropertyValueResponseTypeDef",
    {
        "propertyValue": "AssetPropertyValueTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredGetInterpolatedAssetPropertyValuesRequestGetInterpolatedAssetPropertyValuesPaginateTypeDef = TypedDict(
    "_RequiredGetInterpolatedAssetPropertyValuesRequestGetInterpolatedAssetPropertyValuesPaginateTypeDef",
    {
        "startTimeInSeconds": int,
        "endTimeInSeconds": int,
        "quality": QualityType,
        "intervalInSeconds": int,
        "type": str,
    },
)
_OptionalGetInterpolatedAssetPropertyValuesRequestGetInterpolatedAssetPropertyValuesPaginateTypeDef = TypedDict(
    "_OptionalGetInterpolatedAssetPropertyValuesRequestGetInterpolatedAssetPropertyValuesPaginateTypeDef",
    {
        "assetId": str,
        "propertyId": str,
        "propertyAlias": str,
        "startTimeOffsetInNanos": int,
        "endTimeOffsetInNanos": int,
        "intervalWindowInSeconds": int,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class GetInterpolatedAssetPropertyValuesRequestGetInterpolatedAssetPropertyValuesPaginateTypeDef(
    _RequiredGetInterpolatedAssetPropertyValuesRequestGetInterpolatedAssetPropertyValuesPaginateTypeDef,
    _OptionalGetInterpolatedAssetPropertyValuesRequestGetInterpolatedAssetPropertyValuesPaginateTypeDef,
):
    pass


_RequiredGetInterpolatedAssetPropertyValuesRequestRequestTypeDef = TypedDict(
    "_RequiredGetInterpolatedAssetPropertyValuesRequestRequestTypeDef",
    {
        "startTimeInSeconds": int,
        "endTimeInSeconds": int,
        "quality": QualityType,
        "intervalInSeconds": int,
        "type": str,
    },
)
_OptionalGetInterpolatedAssetPropertyValuesRequestRequestTypeDef = TypedDict(
    "_OptionalGetInterpolatedAssetPropertyValuesRequestRequestTypeDef",
    {
        "assetId": str,
        "propertyId": str,
        "propertyAlias": str,
        "startTimeOffsetInNanos": int,
        "endTimeOffsetInNanos": int,
        "nextToken": str,
        "maxResults": int,
        "intervalWindowInSeconds": int,
    },
    total=False,
)


class GetInterpolatedAssetPropertyValuesRequestRequestTypeDef(
    _RequiredGetInterpolatedAssetPropertyValuesRequestRequestTypeDef,
    _OptionalGetInterpolatedAssetPropertyValuesRequestRequestTypeDef,
):
    pass


GetInterpolatedAssetPropertyValuesResponseTypeDef = TypedDict(
    "GetInterpolatedAssetPropertyValuesResponseTypeDef",
    {
        "interpolatedAssetPropertyValues": List["InterpolatedAssetPropertyValueTypeDef"],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GreengrassTypeDef = TypedDict(
    "GreengrassTypeDef",
    {
        "groupArn": str,
    },
)

GreengrassV2TypeDef = TypedDict(
    "GreengrassV2TypeDef",
    {
        "coreDeviceThingName": str,
    },
)

GroupIdentityTypeDef = TypedDict(
    "GroupIdentityTypeDef",
    {
        "id": str,
    },
)

IAMRoleIdentityTypeDef = TypedDict(
    "IAMRoleIdentityTypeDef",
    {
        "arn": str,
    },
)

IAMUserIdentityTypeDef = TypedDict(
    "IAMUserIdentityTypeDef",
    {
        "arn": str,
    },
)

IdentityTypeDef = TypedDict(
    "IdentityTypeDef",
    {
        "user": "UserIdentityTypeDef",
        "group": "GroupIdentityTypeDef",
        "iamUser": "IAMUserIdentityTypeDef",
        "iamRole": "IAMRoleIdentityTypeDef",
    },
    total=False,
)

ImageFileTypeDef = TypedDict(
    "ImageFileTypeDef",
    {
        "data": Union[str, bytes, IO[Any], StreamingBody],
        "type": Literal["PNG"],
    },
)

ImageLocationTypeDef = TypedDict(
    "ImageLocationTypeDef",
    {
        "id": str,
        "url": str,
    },
)

ImageTypeDef = TypedDict(
    "ImageTypeDef",
    {
        "id": str,
        "file": "ImageFileTypeDef",
    },
    total=False,
)

InterpolatedAssetPropertyValueTypeDef = TypedDict(
    "InterpolatedAssetPropertyValueTypeDef",
    {
        "timestamp": "TimeInNanosTypeDef",
        "value": "VariantTypeDef",
    },
)

ListAccessPoliciesRequestListAccessPoliciesPaginateTypeDef = TypedDict(
    "ListAccessPoliciesRequestListAccessPoliciesPaginateTypeDef",
    {
        "identityType": IdentityTypeType,
        "identityId": str,
        "resourceType": ResourceTypeType,
        "resourceId": str,
        "iamArn": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListAccessPoliciesRequestRequestTypeDef = TypedDict(
    "ListAccessPoliciesRequestRequestTypeDef",
    {
        "identityType": IdentityTypeType,
        "identityId": str,
        "resourceType": ResourceTypeType,
        "resourceId": str,
        "iamArn": str,
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

ListAccessPoliciesResponseTypeDef = TypedDict(
    "ListAccessPoliciesResponseTypeDef",
    {
        "accessPolicySummaries": List["AccessPolicySummaryTypeDef"],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListAssetModelsRequestListAssetModelsPaginateTypeDef = TypedDict(
    "ListAssetModelsRequestListAssetModelsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListAssetModelsRequestRequestTypeDef = TypedDict(
    "ListAssetModelsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

ListAssetModelsResponseTypeDef = TypedDict(
    "ListAssetModelsResponseTypeDef",
    {
        "assetModelSummaries": List["AssetModelSummaryTypeDef"],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredListAssetRelationshipsRequestListAssetRelationshipsPaginateTypeDef = TypedDict(
    "_RequiredListAssetRelationshipsRequestListAssetRelationshipsPaginateTypeDef",
    {
        "assetId": str,
        "traversalType": Literal["PATH_TO_ROOT"],
    },
)
_OptionalListAssetRelationshipsRequestListAssetRelationshipsPaginateTypeDef = TypedDict(
    "_OptionalListAssetRelationshipsRequestListAssetRelationshipsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListAssetRelationshipsRequestListAssetRelationshipsPaginateTypeDef(
    _RequiredListAssetRelationshipsRequestListAssetRelationshipsPaginateTypeDef,
    _OptionalListAssetRelationshipsRequestListAssetRelationshipsPaginateTypeDef,
):
    pass


_RequiredListAssetRelationshipsRequestRequestTypeDef = TypedDict(
    "_RequiredListAssetRelationshipsRequestRequestTypeDef",
    {
        "assetId": str,
        "traversalType": Literal["PATH_TO_ROOT"],
    },
)
_OptionalListAssetRelationshipsRequestRequestTypeDef = TypedDict(
    "_OptionalListAssetRelationshipsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class ListAssetRelationshipsRequestRequestTypeDef(
    _RequiredListAssetRelationshipsRequestRequestTypeDef,
    _OptionalListAssetRelationshipsRequestRequestTypeDef,
):
    pass


ListAssetRelationshipsResponseTypeDef = TypedDict(
    "ListAssetRelationshipsResponseTypeDef",
    {
        "assetRelationshipSummaries": List["AssetRelationshipSummaryTypeDef"],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListAssetsRequestListAssetsPaginateTypeDef = TypedDict(
    "ListAssetsRequestListAssetsPaginateTypeDef",
    {
        "assetModelId": str,
        "filter": ListAssetsFilterType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListAssetsRequestRequestTypeDef = TypedDict(
    "ListAssetsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
        "assetModelId": str,
        "filter": ListAssetsFilterType,
    },
    total=False,
)

ListAssetsResponseTypeDef = TypedDict(
    "ListAssetsResponseTypeDef",
    {
        "assetSummaries": List["AssetSummaryTypeDef"],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredListAssociatedAssetsRequestListAssociatedAssetsPaginateTypeDef = TypedDict(
    "_RequiredListAssociatedAssetsRequestListAssociatedAssetsPaginateTypeDef",
    {
        "assetId": str,
    },
)
_OptionalListAssociatedAssetsRequestListAssociatedAssetsPaginateTypeDef = TypedDict(
    "_OptionalListAssociatedAssetsRequestListAssociatedAssetsPaginateTypeDef",
    {
        "hierarchyId": str,
        "traversalDirection": TraversalDirectionType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListAssociatedAssetsRequestListAssociatedAssetsPaginateTypeDef(
    _RequiredListAssociatedAssetsRequestListAssociatedAssetsPaginateTypeDef,
    _OptionalListAssociatedAssetsRequestListAssociatedAssetsPaginateTypeDef,
):
    pass


_RequiredListAssociatedAssetsRequestRequestTypeDef = TypedDict(
    "_RequiredListAssociatedAssetsRequestRequestTypeDef",
    {
        "assetId": str,
    },
)
_OptionalListAssociatedAssetsRequestRequestTypeDef = TypedDict(
    "_OptionalListAssociatedAssetsRequestRequestTypeDef",
    {
        "hierarchyId": str,
        "traversalDirection": TraversalDirectionType,
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class ListAssociatedAssetsRequestRequestTypeDef(
    _RequiredListAssociatedAssetsRequestRequestTypeDef,
    _OptionalListAssociatedAssetsRequestRequestTypeDef,
):
    pass


ListAssociatedAssetsResponseTypeDef = TypedDict(
    "ListAssociatedAssetsResponseTypeDef",
    {
        "assetSummaries": List["AssociatedAssetsSummaryTypeDef"],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredListDashboardsRequestListDashboardsPaginateTypeDef = TypedDict(
    "_RequiredListDashboardsRequestListDashboardsPaginateTypeDef",
    {
        "projectId": str,
    },
)
_OptionalListDashboardsRequestListDashboardsPaginateTypeDef = TypedDict(
    "_OptionalListDashboardsRequestListDashboardsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListDashboardsRequestListDashboardsPaginateTypeDef(
    _RequiredListDashboardsRequestListDashboardsPaginateTypeDef,
    _OptionalListDashboardsRequestListDashboardsPaginateTypeDef,
):
    pass


_RequiredListDashboardsRequestRequestTypeDef = TypedDict(
    "_RequiredListDashboardsRequestRequestTypeDef",
    {
        "projectId": str,
    },
)
_OptionalListDashboardsRequestRequestTypeDef = TypedDict(
    "_OptionalListDashboardsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class ListDashboardsRequestRequestTypeDef(
    _RequiredListDashboardsRequestRequestTypeDef, _OptionalListDashboardsRequestRequestTypeDef
):
    pass


ListDashboardsResponseTypeDef = TypedDict(
    "ListDashboardsResponseTypeDef",
    {
        "dashboardSummaries": List["DashboardSummaryTypeDef"],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListGatewaysRequestListGatewaysPaginateTypeDef = TypedDict(
    "ListGatewaysRequestListGatewaysPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListGatewaysRequestRequestTypeDef = TypedDict(
    "ListGatewaysRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

ListGatewaysResponseTypeDef = TypedDict(
    "ListGatewaysResponseTypeDef",
    {
        "gatewaySummaries": List["GatewaySummaryTypeDef"],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListPortalsRequestListPortalsPaginateTypeDef = TypedDict(
    "ListPortalsRequestListPortalsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListPortalsRequestRequestTypeDef = TypedDict(
    "ListPortalsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

ListPortalsResponseTypeDef = TypedDict(
    "ListPortalsResponseTypeDef",
    {
        "portalSummaries": List["PortalSummaryTypeDef"],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredListProjectAssetsRequestListProjectAssetsPaginateTypeDef = TypedDict(
    "_RequiredListProjectAssetsRequestListProjectAssetsPaginateTypeDef",
    {
        "projectId": str,
    },
)
_OptionalListProjectAssetsRequestListProjectAssetsPaginateTypeDef = TypedDict(
    "_OptionalListProjectAssetsRequestListProjectAssetsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListProjectAssetsRequestListProjectAssetsPaginateTypeDef(
    _RequiredListProjectAssetsRequestListProjectAssetsPaginateTypeDef,
    _OptionalListProjectAssetsRequestListProjectAssetsPaginateTypeDef,
):
    pass


_RequiredListProjectAssetsRequestRequestTypeDef = TypedDict(
    "_RequiredListProjectAssetsRequestRequestTypeDef",
    {
        "projectId": str,
    },
)
_OptionalListProjectAssetsRequestRequestTypeDef = TypedDict(
    "_OptionalListProjectAssetsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class ListProjectAssetsRequestRequestTypeDef(
    _RequiredListProjectAssetsRequestRequestTypeDef, _OptionalListProjectAssetsRequestRequestTypeDef
):
    pass


ListProjectAssetsResponseTypeDef = TypedDict(
    "ListProjectAssetsResponseTypeDef",
    {
        "assetIds": List[str],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredListProjectsRequestListProjectsPaginateTypeDef = TypedDict(
    "_RequiredListProjectsRequestListProjectsPaginateTypeDef",
    {
        "portalId": str,
    },
)
_OptionalListProjectsRequestListProjectsPaginateTypeDef = TypedDict(
    "_OptionalListProjectsRequestListProjectsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListProjectsRequestListProjectsPaginateTypeDef(
    _RequiredListProjectsRequestListProjectsPaginateTypeDef,
    _OptionalListProjectsRequestListProjectsPaginateTypeDef,
):
    pass


_RequiredListProjectsRequestRequestTypeDef = TypedDict(
    "_RequiredListProjectsRequestRequestTypeDef",
    {
        "portalId": str,
    },
)
_OptionalListProjectsRequestRequestTypeDef = TypedDict(
    "_OptionalListProjectsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class ListProjectsRequestRequestTypeDef(
    _RequiredListProjectsRequestRequestTypeDef, _OptionalListProjectsRequestRequestTypeDef
):
    pass


ListProjectsResponseTypeDef = TypedDict(
    "ListProjectsResponseTypeDef",
    {
        "projectSummaries": List["ProjectSummaryTypeDef"],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "tags": Dict[str, str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListTimeSeriesRequestListTimeSeriesPaginateTypeDef = TypedDict(
    "ListTimeSeriesRequestListTimeSeriesPaginateTypeDef",
    {
        "assetId": str,
        "aliasPrefix": str,
        "timeSeriesType": ListTimeSeriesTypeType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListTimeSeriesRequestRequestTypeDef = TypedDict(
    "ListTimeSeriesRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
        "assetId": str,
        "aliasPrefix": str,
        "timeSeriesType": ListTimeSeriesTypeType,
    },
    total=False,
)

ListTimeSeriesResponseTypeDef = TypedDict(
    "ListTimeSeriesResponseTypeDef",
    {
        "TimeSeriesSummaries": List["TimeSeriesSummaryTypeDef"],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

LoggingOptionsTypeDef = TypedDict(
    "LoggingOptionsTypeDef",
    {
        "level": LoggingLevelType,
    },
)

MeasurementProcessingConfigTypeDef = TypedDict(
    "MeasurementProcessingConfigTypeDef",
    {
        "forwardingConfig": "ForwardingConfigTypeDef",
    },
)

MeasurementTypeDef = TypedDict(
    "MeasurementTypeDef",
    {
        "processingConfig": "MeasurementProcessingConfigTypeDef",
    },
    total=False,
)

MetricProcessingConfigTypeDef = TypedDict(
    "MetricProcessingConfigTypeDef",
    {
        "computeLocation": ComputeLocationType,
    },
)

_RequiredMetricTypeDef = TypedDict(
    "_RequiredMetricTypeDef",
    {
        "expression": str,
        "variables": Sequence["ExpressionVariableTypeDef"],
        "window": "MetricWindowTypeDef",
    },
)
_OptionalMetricTypeDef = TypedDict(
    "_OptionalMetricTypeDef",
    {
        "processingConfig": "MetricProcessingConfigTypeDef",
    },
    total=False,
)


class MetricTypeDef(_RequiredMetricTypeDef, _OptionalMetricTypeDef):
    pass


MetricWindowTypeDef = TypedDict(
    "MetricWindowTypeDef",
    {
        "tumbling": "TumblingWindowTypeDef",
    },
    total=False,
)

MonitorErrorDetailsTypeDef = TypedDict(
    "MonitorErrorDetailsTypeDef",
    {
        "code": MonitorErrorCodeType,
        "message": str,
    },
    total=False,
)

MultiLayerStorageTypeDef = TypedDict(
    "MultiLayerStorageTypeDef",
    {
        "customerManagedS3Storage": "CustomerManagedS3StorageTypeDef",
    },
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

PortalResourceTypeDef = TypedDict(
    "PortalResourceTypeDef",
    {
        "id": str,
    },
)

_RequiredPortalStatusTypeDef = TypedDict(
    "_RequiredPortalStatusTypeDef",
    {
        "state": PortalStateType,
    },
)
_OptionalPortalStatusTypeDef = TypedDict(
    "_OptionalPortalStatusTypeDef",
    {
        "error": "MonitorErrorDetailsTypeDef",
    },
    total=False,
)


class PortalStatusTypeDef(_RequiredPortalStatusTypeDef, _OptionalPortalStatusTypeDef):
    pass


_RequiredPortalSummaryTypeDef = TypedDict(
    "_RequiredPortalSummaryTypeDef",
    {
        "id": str,
        "name": str,
        "startUrl": str,
        "status": "PortalStatusTypeDef",
    },
)
_OptionalPortalSummaryTypeDef = TypedDict(
    "_OptionalPortalSummaryTypeDef",
    {
        "description": str,
        "creationDate": datetime,
        "lastUpdateDate": datetime,
        "roleArn": str,
    },
    total=False,
)


class PortalSummaryTypeDef(_RequiredPortalSummaryTypeDef, _OptionalPortalSummaryTypeDef):
    pass


ProjectResourceTypeDef = TypedDict(
    "ProjectResourceTypeDef",
    {
        "id": str,
    },
)

_RequiredProjectSummaryTypeDef = TypedDict(
    "_RequiredProjectSummaryTypeDef",
    {
        "id": str,
        "name": str,
    },
)
_OptionalProjectSummaryTypeDef = TypedDict(
    "_OptionalProjectSummaryTypeDef",
    {
        "description": str,
        "creationDate": datetime,
        "lastUpdateDate": datetime,
    },
    total=False,
)


class ProjectSummaryTypeDef(_RequiredProjectSummaryTypeDef, _OptionalProjectSummaryTypeDef):
    pass


PropertyNotificationTypeDef = TypedDict(
    "PropertyNotificationTypeDef",
    {
        "topic": str,
        "state": PropertyNotificationStateType,
    },
)

_RequiredPropertyTypeDef = TypedDict(
    "_RequiredPropertyTypeDef",
    {
        "id": str,
        "name": str,
        "dataType": PropertyDataTypeType,
    },
)
_OptionalPropertyTypeDef = TypedDict(
    "_OptionalPropertyTypeDef",
    {
        "alias": str,
        "notification": "PropertyNotificationTypeDef",
        "unit": str,
        "type": "PropertyTypeTypeDef",
    },
    total=False,
)


class PropertyTypeDef(_RequiredPropertyTypeDef, _OptionalPropertyTypeDef):
    pass


PropertyTypeTypeDef = TypedDict(
    "PropertyTypeTypeDef",
    {
        "attribute": "AttributeTypeDef",
        "measurement": "MeasurementTypeDef",
        "transform": "TransformTypeDef",
        "metric": "MetricTypeDef",
    },
    total=False,
)

_RequiredPutAssetPropertyValueEntryTypeDef = TypedDict(
    "_RequiredPutAssetPropertyValueEntryTypeDef",
    {
        "entryId": str,
        "propertyValues": Sequence["AssetPropertyValueTypeDef"],
    },
)
_OptionalPutAssetPropertyValueEntryTypeDef = TypedDict(
    "_OptionalPutAssetPropertyValueEntryTypeDef",
    {
        "assetId": str,
        "propertyId": str,
        "propertyAlias": str,
    },
    total=False,
)


class PutAssetPropertyValueEntryTypeDef(
    _RequiredPutAssetPropertyValueEntryTypeDef, _OptionalPutAssetPropertyValueEntryTypeDef
):
    pass


_RequiredPutDefaultEncryptionConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredPutDefaultEncryptionConfigurationRequestRequestTypeDef",
    {
        "encryptionType": EncryptionTypeType,
    },
)
_OptionalPutDefaultEncryptionConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalPutDefaultEncryptionConfigurationRequestRequestTypeDef",
    {
        "kmsKeyId": str,
    },
    total=False,
)


class PutDefaultEncryptionConfigurationRequestRequestTypeDef(
    _RequiredPutDefaultEncryptionConfigurationRequestRequestTypeDef,
    _OptionalPutDefaultEncryptionConfigurationRequestRequestTypeDef,
):
    pass


PutDefaultEncryptionConfigurationResponseTypeDef = TypedDict(
    "PutDefaultEncryptionConfigurationResponseTypeDef",
    {
        "encryptionType": EncryptionTypeType,
        "kmsKeyArn": str,
        "configurationStatus": "ConfigurationStatusTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

PutLoggingOptionsRequestRequestTypeDef = TypedDict(
    "PutLoggingOptionsRequestRequestTypeDef",
    {
        "loggingOptions": "LoggingOptionsTypeDef",
    },
)

_RequiredPutStorageConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredPutStorageConfigurationRequestRequestTypeDef",
    {
        "storageType": StorageTypeType,
    },
)
_OptionalPutStorageConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalPutStorageConfigurationRequestRequestTypeDef",
    {
        "multiLayerStorage": "MultiLayerStorageTypeDef",
        "disassociatedDataStorage": DisassociatedDataStorageStateType,
        "retentionPeriod": "RetentionPeriodTypeDef",
    },
    total=False,
)


class PutStorageConfigurationRequestRequestTypeDef(
    _RequiredPutStorageConfigurationRequestRequestTypeDef,
    _OptionalPutStorageConfigurationRequestRequestTypeDef,
):
    pass


PutStorageConfigurationResponseTypeDef = TypedDict(
    "PutStorageConfigurationResponseTypeDef",
    {
        "storageType": StorageTypeType,
        "multiLayerStorage": "MultiLayerStorageTypeDef",
        "disassociatedDataStorage": DisassociatedDataStorageStateType,
        "retentionPeriod": "RetentionPeriodTypeDef",
        "configurationStatus": "ConfigurationStatusTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ResourceTypeDef = TypedDict(
    "ResourceTypeDef",
    {
        "portal": "PortalResourceTypeDef",
        "project": "ProjectResourceTypeDef",
    },
    total=False,
)

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

RetentionPeriodTypeDef = TypedDict(
    "RetentionPeriodTypeDef",
    {
        "numberOfDays": int,
        "unlimited": bool,
    },
    total=False,
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Mapping[str, str],
    },
)

_RequiredTimeInNanosTypeDef = TypedDict(
    "_RequiredTimeInNanosTypeDef",
    {
        "timeInSeconds": int,
    },
)
_OptionalTimeInNanosTypeDef = TypedDict(
    "_OptionalTimeInNanosTypeDef",
    {
        "offsetInNanos": int,
    },
    total=False,
)


class TimeInNanosTypeDef(_RequiredTimeInNanosTypeDef, _OptionalTimeInNanosTypeDef):
    pass


_RequiredTimeSeriesSummaryTypeDef = TypedDict(
    "_RequiredTimeSeriesSummaryTypeDef",
    {
        "timeSeriesId": str,
        "dataType": PropertyDataTypeType,
        "timeSeriesCreationDate": datetime,
        "timeSeriesLastUpdateDate": datetime,
    },
)
_OptionalTimeSeriesSummaryTypeDef = TypedDict(
    "_OptionalTimeSeriesSummaryTypeDef",
    {
        "assetId": str,
        "propertyId": str,
        "alias": str,
        "dataTypeSpec": str,
    },
    total=False,
)


class TimeSeriesSummaryTypeDef(
    _RequiredTimeSeriesSummaryTypeDef, _OptionalTimeSeriesSummaryTypeDef
):
    pass


_RequiredTransformProcessingConfigTypeDef = TypedDict(
    "_RequiredTransformProcessingConfigTypeDef",
    {
        "computeLocation": ComputeLocationType,
    },
)
_OptionalTransformProcessingConfigTypeDef = TypedDict(
    "_OptionalTransformProcessingConfigTypeDef",
    {
        "forwardingConfig": "ForwardingConfigTypeDef",
    },
    total=False,
)


class TransformProcessingConfigTypeDef(
    _RequiredTransformProcessingConfigTypeDef, _OptionalTransformProcessingConfigTypeDef
):
    pass


_RequiredTransformTypeDef = TypedDict(
    "_RequiredTransformTypeDef",
    {
        "expression": str,
        "variables": Sequence["ExpressionVariableTypeDef"],
    },
)
_OptionalTransformTypeDef = TypedDict(
    "_OptionalTransformTypeDef",
    {
        "processingConfig": "TransformProcessingConfigTypeDef",
    },
    total=False,
)


class TransformTypeDef(_RequiredTransformTypeDef, _OptionalTransformTypeDef):
    pass


_RequiredTumblingWindowTypeDef = TypedDict(
    "_RequiredTumblingWindowTypeDef",
    {
        "interval": str,
    },
)
_OptionalTumblingWindowTypeDef = TypedDict(
    "_OptionalTumblingWindowTypeDef",
    {
        "offset": str,
    },
    total=False,
)


class TumblingWindowTypeDef(_RequiredTumblingWindowTypeDef, _OptionalTumblingWindowTypeDef):
    pass


UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": Sequence[str],
    },
)

_RequiredUpdateAccessPolicyRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateAccessPolicyRequestRequestTypeDef",
    {
        "accessPolicyId": str,
        "accessPolicyIdentity": "IdentityTypeDef",
        "accessPolicyResource": "ResourceTypeDef",
        "accessPolicyPermission": PermissionType,
    },
)
_OptionalUpdateAccessPolicyRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateAccessPolicyRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class UpdateAccessPolicyRequestRequestTypeDef(
    _RequiredUpdateAccessPolicyRequestRequestTypeDef,
    _OptionalUpdateAccessPolicyRequestRequestTypeDef,
):
    pass


_RequiredUpdateAssetModelRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateAssetModelRequestRequestTypeDef",
    {
        "assetModelId": str,
        "assetModelName": str,
    },
)
_OptionalUpdateAssetModelRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateAssetModelRequestRequestTypeDef",
    {
        "assetModelDescription": str,
        "assetModelProperties": Sequence["AssetModelPropertyTypeDef"],
        "assetModelHierarchies": Sequence["AssetModelHierarchyTypeDef"],
        "assetModelCompositeModels": Sequence["AssetModelCompositeModelTypeDef"],
        "clientToken": str,
    },
    total=False,
)


class UpdateAssetModelRequestRequestTypeDef(
    _RequiredUpdateAssetModelRequestRequestTypeDef, _OptionalUpdateAssetModelRequestRequestTypeDef
):
    pass


UpdateAssetModelResponseTypeDef = TypedDict(
    "UpdateAssetModelResponseTypeDef",
    {
        "assetModelStatus": "AssetModelStatusTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredUpdateAssetPropertyRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateAssetPropertyRequestRequestTypeDef",
    {
        "assetId": str,
        "propertyId": str,
    },
)
_OptionalUpdateAssetPropertyRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateAssetPropertyRequestRequestTypeDef",
    {
        "propertyAlias": str,
        "propertyNotificationState": PropertyNotificationStateType,
        "clientToken": str,
    },
    total=False,
)


class UpdateAssetPropertyRequestRequestTypeDef(
    _RequiredUpdateAssetPropertyRequestRequestTypeDef,
    _OptionalUpdateAssetPropertyRequestRequestTypeDef,
):
    pass


_RequiredUpdateAssetRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateAssetRequestRequestTypeDef",
    {
        "assetId": str,
        "assetName": str,
    },
)
_OptionalUpdateAssetRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateAssetRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class UpdateAssetRequestRequestTypeDef(
    _RequiredUpdateAssetRequestRequestTypeDef, _OptionalUpdateAssetRequestRequestTypeDef
):
    pass


UpdateAssetResponseTypeDef = TypedDict(
    "UpdateAssetResponseTypeDef",
    {
        "assetStatus": "AssetStatusTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredUpdateDashboardRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateDashboardRequestRequestTypeDef",
    {
        "dashboardId": str,
        "dashboardName": str,
        "dashboardDefinition": str,
    },
)
_OptionalUpdateDashboardRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateDashboardRequestRequestTypeDef",
    {
        "dashboardDescription": str,
        "clientToken": str,
    },
    total=False,
)


class UpdateDashboardRequestRequestTypeDef(
    _RequiredUpdateDashboardRequestRequestTypeDef, _OptionalUpdateDashboardRequestRequestTypeDef
):
    pass


UpdateGatewayCapabilityConfigurationRequestRequestTypeDef = TypedDict(
    "UpdateGatewayCapabilityConfigurationRequestRequestTypeDef",
    {
        "gatewayId": str,
        "capabilityNamespace": str,
        "capabilityConfiguration": str,
    },
)

UpdateGatewayCapabilityConfigurationResponseTypeDef = TypedDict(
    "UpdateGatewayCapabilityConfigurationResponseTypeDef",
    {
        "capabilityNamespace": str,
        "capabilitySyncStatus": CapabilitySyncStatusType,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateGatewayRequestRequestTypeDef = TypedDict(
    "UpdateGatewayRequestRequestTypeDef",
    {
        "gatewayId": str,
        "gatewayName": str,
    },
)

_RequiredUpdatePortalRequestRequestTypeDef = TypedDict(
    "_RequiredUpdatePortalRequestRequestTypeDef",
    {
        "portalId": str,
        "portalName": str,
        "portalContactEmail": str,
        "roleArn": str,
    },
)
_OptionalUpdatePortalRequestRequestTypeDef = TypedDict(
    "_OptionalUpdatePortalRequestRequestTypeDef",
    {
        "portalDescription": str,
        "portalLogoImage": "ImageTypeDef",
        "clientToken": str,
        "notificationSenderEmail": str,
        "alarms": "AlarmsTypeDef",
    },
    total=False,
)


class UpdatePortalRequestRequestTypeDef(
    _RequiredUpdatePortalRequestRequestTypeDef, _OptionalUpdatePortalRequestRequestTypeDef
):
    pass


UpdatePortalResponseTypeDef = TypedDict(
    "UpdatePortalResponseTypeDef",
    {
        "portalStatus": "PortalStatusTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredUpdateProjectRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateProjectRequestRequestTypeDef",
    {
        "projectId": str,
        "projectName": str,
    },
)
_OptionalUpdateProjectRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateProjectRequestRequestTypeDef",
    {
        "projectDescription": str,
        "clientToken": str,
    },
    total=False,
)


class UpdateProjectRequestRequestTypeDef(
    _RequiredUpdateProjectRequestRequestTypeDef, _OptionalUpdateProjectRequestRequestTypeDef
):
    pass


UserIdentityTypeDef = TypedDict(
    "UserIdentityTypeDef",
    {
        "id": str,
    },
)

_RequiredVariableValueTypeDef = TypedDict(
    "_RequiredVariableValueTypeDef",
    {
        "propertyId": str,
    },
)
_OptionalVariableValueTypeDef = TypedDict(
    "_OptionalVariableValueTypeDef",
    {
        "hierarchyId": str,
    },
    total=False,
)


class VariableValueTypeDef(_RequiredVariableValueTypeDef, _OptionalVariableValueTypeDef):
    pass


VariantTypeDef = TypedDict(
    "VariantTypeDef",
    {
        "stringValue": str,
        "integerValue": int,
        "doubleValue": float,
        "booleanValue": bool,
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
