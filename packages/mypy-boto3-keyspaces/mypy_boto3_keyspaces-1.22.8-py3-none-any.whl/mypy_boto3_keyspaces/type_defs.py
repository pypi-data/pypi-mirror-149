"""
Type annotations for keyspaces service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_keyspaces/type_defs/)

Usage::

    ```python
    from mypy_boto3_keyspaces.type_defs import CapacitySpecificationSummaryTypeDef

    data: CapacitySpecificationSummaryTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence, Union

from .literals import (
    EncryptionTypeType,
    PointInTimeRecoveryStatusType,
    SortOrderType,
    TableStatusType,
    ThroughputModeType,
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
    "CapacitySpecificationSummaryTypeDef",
    "CapacitySpecificationTypeDef",
    "ClusteringKeyTypeDef",
    "ColumnDefinitionTypeDef",
    "CommentTypeDef",
    "CreateKeyspaceRequestRequestTypeDef",
    "CreateKeyspaceResponseTypeDef",
    "CreateTableRequestRequestTypeDef",
    "CreateTableResponseTypeDef",
    "DeleteKeyspaceRequestRequestTypeDef",
    "DeleteTableRequestRequestTypeDef",
    "EncryptionSpecificationTypeDef",
    "GetKeyspaceRequestRequestTypeDef",
    "GetKeyspaceResponseTypeDef",
    "GetTableRequestRequestTypeDef",
    "GetTableResponseTypeDef",
    "KeyspaceSummaryTypeDef",
    "ListKeyspacesRequestListKeyspacesPaginateTypeDef",
    "ListKeyspacesRequestRequestTypeDef",
    "ListKeyspacesResponseTypeDef",
    "ListTablesRequestListTablesPaginateTypeDef",
    "ListTablesRequestRequestTypeDef",
    "ListTablesResponseTypeDef",
    "ListTagsForResourceRequestListTagsForResourcePaginateTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PaginatorConfigTypeDef",
    "PartitionKeyTypeDef",
    "PointInTimeRecoverySummaryTypeDef",
    "PointInTimeRecoveryTypeDef",
    "ResponseMetadataTypeDef",
    "RestoreTableRequestRequestTypeDef",
    "RestoreTableResponseTypeDef",
    "SchemaDefinitionTypeDef",
    "StaticColumnTypeDef",
    "TableSummaryTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagTypeDef",
    "TimeToLiveTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateTableRequestRequestTypeDef",
    "UpdateTableResponseTypeDef",
)

_RequiredCapacitySpecificationSummaryTypeDef = TypedDict(
    "_RequiredCapacitySpecificationSummaryTypeDef",
    {
        "throughputMode": ThroughputModeType,
    },
)
_OptionalCapacitySpecificationSummaryTypeDef = TypedDict(
    "_OptionalCapacitySpecificationSummaryTypeDef",
    {
        "readCapacityUnits": int,
        "writeCapacityUnits": int,
        "lastUpdateToPayPerRequestTimestamp": datetime,
    },
    total=False,
)


class CapacitySpecificationSummaryTypeDef(
    _RequiredCapacitySpecificationSummaryTypeDef, _OptionalCapacitySpecificationSummaryTypeDef
):
    pass


_RequiredCapacitySpecificationTypeDef = TypedDict(
    "_RequiredCapacitySpecificationTypeDef",
    {
        "throughputMode": ThroughputModeType,
    },
)
_OptionalCapacitySpecificationTypeDef = TypedDict(
    "_OptionalCapacitySpecificationTypeDef",
    {
        "readCapacityUnits": int,
        "writeCapacityUnits": int,
    },
    total=False,
)


class CapacitySpecificationTypeDef(
    _RequiredCapacitySpecificationTypeDef, _OptionalCapacitySpecificationTypeDef
):
    pass


ClusteringKeyTypeDef = TypedDict(
    "ClusteringKeyTypeDef",
    {
        "name": str,
        "orderBy": SortOrderType,
    },
)

ColumnDefinitionTypeDef = TypedDict(
    "ColumnDefinitionTypeDef",
    {
        "name": str,
        "type": str,
    },
)

CommentTypeDef = TypedDict(
    "CommentTypeDef",
    {
        "message": str,
    },
)

_RequiredCreateKeyspaceRequestRequestTypeDef = TypedDict(
    "_RequiredCreateKeyspaceRequestRequestTypeDef",
    {
        "keyspaceName": str,
    },
)
_OptionalCreateKeyspaceRequestRequestTypeDef = TypedDict(
    "_OptionalCreateKeyspaceRequestRequestTypeDef",
    {
        "tags": Sequence["TagTypeDef"],
    },
    total=False,
)


class CreateKeyspaceRequestRequestTypeDef(
    _RequiredCreateKeyspaceRequestRequestTypeDef, _OptionalCreateKeyspaceRequestRequestTypeDef
):
    pass


CreateKeyspaceResponseTypeDef = TypedDict(
    "CreateKeyspaceResponseTypeDef",
    {
        "resourceArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateTableRequestRequestTypeDef = TypedDict(
    "_RequiredCreateTableRequestRequestTypeDef",
    {
        "keyspaceName": str,
        "tableName": str,
        "schemaDefinition": "SchemaDefinitionTypeDef",
    },
)
_OptionalCreateTableRequestRequestTypeDef = TypedDict(
    "_OptionalCreateTableRequestRequestTypeDef",
    {
        "comment": "CommentTypeDef",
        "capacitySpecification": "CapacitySpecificationTypeDef",
        "encryptionSpecification": "EncryptionSpecificationTypeDef",
        "pointInTimeRecovery": "PointInTimeRecoveryTypeDef",
        "ttl": "TimeToLiveTypeDef",
        "defaultTimeToLive": int,
        "tags": Sequence["TagTypeDef"],
    },
    total=False,
)


class CreateTableRequestRequestTypeDef(
    _RequiredCreateTableRequestRequestTypeDef, _OptionalCreateTableRequestRequestTypeDef
):
    pass


CreateTableResponseTypeDef = TypedDict(
    "CreateTableResponseTypeDef",
    {
        "resourceArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteKeyspaceRequestRequestTypeDef = TypedDict(
    "DeleteKeyspaceRequestRequestTypeDef",
    {
        "keyspaceName": str,
    },
)

DeleteTableRequestRequestTypeDef = TypedDict(
    "DeleteTableRequestRequestTypeDef",
    {
        "keyspaceName": str,
        "tableName": str,
    },
)

_RequiredEncryptionSpecificationTypeDef = TypedDict(
    "_RequiredEncryptionSpecificationTypeDef",
    {
        "type": EncryptionTypeType,
    },
)
_OptionalEncryptionSpecificationTypeDef = TypedDict(
    "_OptionalEncryptionSpecificationTypeDef",
    {
        "kmsKeyIdentifier": str,
    },
    total=False,
)


class EncryptionSpecificationTypeDef(
    _RequiredEncryptionSpecificationTypeDef, _OptionalEncryptionSpecificationTypeDef
):
    pass


GetKeyspaceRequestRequestTypeDef = TypedDict(
    "GetKeyspaceRequestRequestTypeDef",
    {
        "keyspaceName": str,
    },
)

GetKeyspaceResponseTypeDef = TypedDict(
    "GetKeyspaceResponseTypeDef",
    {
        "keyspaceName": str,
        "resourceArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetTableRequestRequestTypeDef = TypedDict(
    "GetTableRequestRequestTypeDef",
    {
        "keyspaceName": str,
        "tableName": str,
    },
)

GetTableResponseTypeDef = TypedDict(
    "GetTableResponseTypeDef",
    {
        "keyspaceName": str,
        "tableName": str,
        "resourceArn": str,
        "creationTimestamp": datetime,
        "status": TableStatusType,
        "schemaDefinition": "SchemaDefinitionTypeDef",
        "capacitySpecification": "CapacitySpecificationSummaryTypeDef",
        "encryptionSpecification": "EncryptionSpecificationTypeDef",
        "pointInTimeRecovery": "PointInTimeRecoverySummaryTypeDef",
        "ttl": "TimeToLiveTypeDef",
        "defaultTimeToLive": int,
        "comment": "CommentTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

KeyspaceSummaryTypeDef = TypedDict(
    "KeyspaceSummaryTypeDef",
    {
        "keyspaceName": str,
        "resourceArn": str,
    },
)

ListKeyspacesRequestListKeyspacesPaginateTypeDef = TypedDict(
    "ListKeyspacesRequestListKeyspacesPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListKeyspacesRequestRequestTypeDef = TypedDict(
    "ListKeyspacesRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

ListKeyspacesResponseTypeDef = TypedDict(
    "ListKeyspacesResponseTypeDef",
    {
        "nextToken": str,
        "keyspaces": List["KeyspaceSummaryTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredListTablesRequestListTablesPaginateTypeDef = TypedDict(
    "_RequiredListTablesRequestListTablesPaginateTypeDef",
    {
        "keyspaceName": str,
    },
)
_OptionalListTablesRequestListTablesPaginateTypeDef = TypedDict(
    "_OptionalListTablesRequestListTablesPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListTablesRequestListTablesPaginateTypeDef(
    _RequiredListTablesRequestListTablesPaginateTypeDef,
    _OptionalListTablesRequestListTablesPaginateTypeDef,
):
    pass


_RequiredListTablesRequestRequestTypeDef = TypedDict(
    "_RequiredListTablesRequestRequestTypeDef",
    {
        "keyspaceName": str,
    },
)
_OptionalListTablesRequestRequestTypeDef = TypedDict(
    "_OptionalListTablesRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class ListTablesRequestRequestTypeDef(
    _RequiredListTablesRequestRequestTypeDef, _OptionalListTablesRequestRequestTypeDef
):
    pass


ListTablesResponseTypeDef = TypedDict(
    "ListTablesResponseTypeDef",
    {
        "nextToken": str,
        "tables": List["TableSummaryTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredListTagsForResourceRequestListTagsForResourcePaginateTypeDef = TypedDict(
    "_RequiredListTagsForResourceRequestListTagsForResourcePaginateTypeDef",
    {
        "resourceArn": str,
    },
)
_OptionalListTagsForResourceRequestListTagsForResourcePaginateTypeDef = TypedDict(
    "_OptionalListTagsForResourceRequestListTagsForResourcePaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListTagsForResourceRequestListTagsForResourcePaginateTypeDef(
    _RequiredListTagsForResourceRequestListTagsForResourcePaginateTypeDef,
    _OptionalListTagsForResourceRequestListTagsForResourcePaginateTypeDef,
):
    pass


_RequiredListTagsForResourceRequestRequestTypeDef = TypedDict(
    "_RequiredListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)
_OptionalListTagsForResourceRequestRequestTypeDef = TypedDict(
    "_OptionalListTagsForResourceRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class ListTagsForResourceRequestRequestTypeDef(
    _RequiredListTagsForResourceRequestRequestTypeDef,
    _OptionalListTagsForResourceRequestRequestTypeDef,
):
    pass


ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "nextToken": str,
        "tags": List["TagTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
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

PartitionKeyTypeDef = TypedDict(
    "PartitionKeyTypeDef",
    {
        "name": str,
    },
)

_RequiredPointInTimeRecoverySummaryTypeDef = TypedDict(
    "_RequiredPointInTimeRecoverySummaryTypeDef",
    {
        "status": PointInTimeRecoveryStatusType,
    },
)
_OptionalPointInTimeRecoverySummaryTypeDef = TypedDict(
    "_OptionalPointInTimeRecoverySummaryTypeDef",
    {
        "earliestRestorableTimestamp": datetime,
    },
    total=False,
)


class PointInTimeRecoverySummaryTypeDef(
    _RequiredPointInTimeRecoverySummaryTypeDef, _OptionalPointInTimeRecoverySummaryTypeDef
):
    pass


PointInTimeRecoveryTypeDef = TypedDict(
    "PointInTimeRecoveryTypeDef",
    {
        "status": PointInTimeRecoveryStatusType,
    },
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

_RequiredRestoreTableRequestRequestTypeDef = TypedDict(
    "_RequiredRestoreTableRequestRequestTypeDef",
    {
        "sourceKeyspaceName": str,
        "sourceTableName": str,
        "targetKeyspaceName": str,
        "targetTableName": str,
    },
)
_OptionalRestoreTableRequestRequestTypeDef = TypedDict(
    "_OptionalRestoreTableRequestRequestTypeDef",
    {
        "restoreTimestamp": Union[datetime, str],
        "capacitySpecificationOverride": "CapacitySpecificationTypeDef",
        "encryptionSpecificationOverride": "EncryptionSpecificationTypeDef",
        "pointInTimeRecoveryOverride": "PointInTimeRecoveryTypeDef",
        "tagsOverride": Sequence["TagTypeDef"],
    },
    total=False,
)


class RestoreTableRequestRequestTypeDef(
    _RequiredRestoreTableRequestRequestTypeDef, _OptionalRestoreTableRequestRequestTypeDef
):
    pass


RestoreTableResponseTypeDef = TypedDict(
    "RestoreTableResponseTypeDef",
    {
        "restoredTableARN": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredSchemaDefinitionTypeDef = TypedDict(
    "_RequiredSchemaDefinitionTypeDef",
    {
        "allColumns": Sequence["ColumnDefinitionTypeDef"],
        "partitionKeys": Sequence["PartitionKeyTypeDef"],
    },
)
_OptionalSchemaDefinitionTypeDef = TypedDict(
    "_OptionalSchemaDefinitionTypeDef",
    {
        "clusteringKeys": Sequence["ClusteringKeyTypeDef"],
        "staticColumns": Sequence["StaticColumnTypeDef"],
    },
    total=False,
)


class SchemaDefinitionTypeDef(_RequiredSchemaDefinitionTypeDef, _OptionalSchemaDefinitionTypeDef):
    pass


StaticColumnTypeDef = TypedDict(
    "StaticColumnTypeDef",
    {
        "name": str,
    },
)

TableSummaryTypeDef = TypedDict(
    "TableSummaryTypeDef",
    {
        "keyspaceName": str,
        "tableName": str,
        "resourceArn": str,
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Sequence["TagTypeDef"],
    },
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "key": str,
        "value": str,
    },
)

TimeToLiveTypeDef = TypedDict(
    "TimeToLiveTypeDef",
    {
        "status": Literal["ENABLED"],
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Sequence["TagTypeDef"],
    },
)

_RequiredUpdateTableRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateTableRequestRequestTypeDef",
    {
        "keyspaceName": str,
        "tableName": str,
    },
)
_OptionalUpdateTableRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateTableRequestRequestTypeDef",
    {
        "addColumns": Sequence["ColumnDefinitionTypeDef"],
        "capacitySpecification": "CapacitySpecificationTypeDef",
        "encryptionSpecification": "EncryptionSpecificationTypeDef",
        "pointInTimeRecovery": "PointInTimeRecoveryTypeDef",
        "ttl": "TimeToLiveTypeDef",
        "defaultTimeToLive": int,
    },
    total=False,
)


class UpdateTableRequestRequestTypeDef(
    _RequiredUpdateTableRequestRequestTypeDef, _OptionalUpdateTableRequestRequestTypeDef
):
    pass


UpdateTableResponseTypeDef = TypedDict(
    "UpdateTableResponseTypeDef",
    {
        "resourceArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)
