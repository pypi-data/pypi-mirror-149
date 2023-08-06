"""
Type annotations for neptune service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_neptune.client import NeptuneClient

    session = get_session()
    async with session.create_client("neptune") as client:
        client: NeptuneClient
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, Mapping, Sequence, Type, Union, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import SourceTypeType
from .paginator import (
    DescribeDBClusterEndpointsPaginator,
    DescribeDBClusterParameterGroupsPaginator,
    DescribeDBClusterParametersPaginator,
    DescribeDBClusterSnapshotsPaginator,
    DescribeDBClustersPaginator,
    DescribeDBEngineVersionsPaginator,
    DescribeDBInstancesPaginator,
    DescribeDBParameterGroupsPaginator,
    DescribeDBParametersPaginator,
    DescribeDBSubnetGroupsPaginator,
    DescribeEngineDefaultParametersPaginator,
    DescribeEventsPaginator,
    DescribeEventSubscriptionsPaginator,
    DescribeOrderableDBInstanceOptionsPaginator,
    DescribePendingMaintenanceActionsPaginator,
)
from .type_defs import (
    AddSourceIdentifierToSubscriptionResultTypeDef,
    ApplyPendingMaintenanceActionResultTypeDef,
    CloudwatchLogsExportConfigurationTypeDef,
    CopyDBClusterParameterGroupResultTypeDef,
    CopyDBClusterSnapshotResultTypeDef,
    CopyDBParameterGroupResultTypeDef,
    CreateDBClusterEndpointOutputTypeDef,
    CreateDBClusterParameterGroupResultTypeDef,
    CreateDBClusterResultTypeDef,
    CreateDBClusterSnapshotResultTypeDef,
    CreateDBInstanceResultTypeDef,
    CreateDBParameterGroupResultTypeDef,
    CreateDBSubnetGroupResultTypeDef,
    CreateEventSubscriptionResultTypeDef,
    DBClusterEndpointMessageTypeDef,
    DBClusterMessageTypeDef,
    DBClusterParameterGroupDetailsTypeDef,
    DBClusterParameterGroupNameMessageTypeDef,
    DBClusterParameterGroupsMessageTypeDef,
    DBClusterSnapshotMessageTypeDef,
    DBEngineVersionMessageTypeDef,
    DBInstanceMessageTypeDef,
    DBParameterGroupDetailsTypeDef,
    DBParameterGroupNameMessageTypeDef,
    DBParameterGroupsMessageTypeDef,
    DBSubnetGroupMessageTypeDef,
    DeleteDBClusterEndpointOutputTypeDef,
    DeleteDBClusterResultTypeDef,
    DeleteDBClusterSnapshotResultTypeDef,
    DeleteDBInstanceResultTypeDef,
    DeleteEventSubscriptionResultTypeDef,
    DescribeDBClusterSnapshotAttributesResultTypeDef,
    DescribeEngineDefaultClusterParametersResultTypeDef,
    DescribeEngineDefaultParametersResultTypeDef,
    DescribeValidDBInstanceModificationsResultTypeDef,
    EventCategoriesMessageTypeDef,
    EventsMessageTypeDef,
    EventSubscriptionsMessageTypeDef,
    FailoverDBClusterResultTypeDef,
    FilterTypeDef,
    ModifyDBClusterEndpointOutputTypeDef,
    ModifyDBClusterResultTypeDef,
    ModifyDBClusterSnapshotAttributeResultTypeDef,
    ModifyDBInstanceResultTypeDef,
    ModifyDBSubnetGroupResultTypeDef,
    ModifyEventSubscriptionResultTypeDef,
    OrderableDBInstanceOptionsMessageTypeDef,
    ParameterTypeDef,
    PendingMaintenanceActionsMessageTypeDef,
    PromoteReadReplicaDBClusterResultTypeDef,
    RebootDBInstanceResultTypeDef,
    RemoveSourceIdentifierFromSubscriptionResultTypeDef,
    RestoreDBClusterFromSnapshotResultTypeDef,
    RestoreDBClusterToPointInTimeResultTypeDef,
    StartDBClusterResultTypeDef,
    StopDBClusterResultTypeDef,
    TagListMessageTypeDef,
    TagTypeDef,
)
from .waiter import DBInstanceAvailableWaiter, DBInstanceDeletedWaiter

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("NeptuneClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AuthorizationNotFoundFault: Type[BotocoreClientError]
    CertificateNotFoundFault: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    DBClusterAlreadyExistsFault: Type[BotocoreClientError]
    DBClusterEndpointAlreadyExistsFault: Type[BotocoreClientError]
    DBClusterEndpointNotFoundFault: Type[BotocoreClientError]
    DBClusterEndpointQuotaExceededFault: Type[BotocoreClientError]
    DBClusterNotFoundFault: Type[BotocoreClientError]
    DBClusterParameterGroupNotFoundFault: Type[BotocoreClientError]
    DBClusterQuotaExceededFault: Type[BotocoreClientError]
    DBClusterRoleAlreadyExistsFault: Type[BotocoreClientError]
    DBClusterRoleNotFoundFault: Type[BotocoreClientError]
    DBClusterRoleQuotaExceededFault: Type[BotocoreClientError]
    DBClusterSnapshotAlreadyExistsFault: Type[BotocoreClientError]
    DBClusterSnapshotNotFoundFault: Type[BotocoreClientError]
    DBInstanceAlreadyExistsFault: Type[BotocoreClientError]
    DBInstanceNotFoundFault: Type[BotocoreClientError]
    DBParameterGroupAlreadyExistsFault: Type[BotocoreClientError]
    DBParameterGroupNotFoundFault: Type[BotocoreClientError]
    DBParameterGroupQuotaExceededFault: Type[BotocoreClientError]
    DBSecurityGroupNotFoundFault: Type[BotocoreClientError]
    DBSnapshotAlreadyExistsFault: Type[BotocoreClientError]
    DBSnapshotNotFoundFault: Type[BotocoreClientError]
    DBSubnetGroupAlreadyExistsFault: Type[BotocoreClientError]
    DBSubnetGroupDoesNotCoverEnoughAZs: Type[BotocoreClientError]
    DBSubnetGroupNotFoundFault: Type[BotocoreClientError]
    DBSubnetGroupQuotaExceededFault: Type[BotocoreClientError]
    DBSubnetQuotaExceededFault: Type[BotocoreClientError]
    DBUpgradeDependencyFailureFault: Type[BotocoreClientError]
    DomainNotFoundFault: Type[BotocoreClientError]
    EventSubscriptionQuotaExceededFault: Type[BotocoreClientError]
    InstanceQuotaExceededFault: Type[BotocoreClientError]
    InsufficientDBClusterCapacityFault: Type[BotocoreClientError]
    InsufficientDBInstanceCapacityFault: Type[BotocoreClientError]
    InsufficientStorageClusterCapacityFault: Type[BotocoreClientError]
    InvalidDBClusterEndpointStateFault: Type[BotocoreClientError]
    InvalidDBClusterSnapshotStateFault: Type[BotocoreClientError]
    InvalidDBClusterStateFault: Type[BotocoreClientError]
    InvalidDBInstanceStateFault: Type[BotocoreClientError]
    InvalidDBParameterGroupStateFault: Type[BotocoreClientError]
    InvalidDBSecurityGroupStateFault: Type[BotocoreClientError]
    InvalidDBSnapshotStateFault: Type[BotocoreClientError]
    InvalidDBSubnetGroupStateFault: Type[BotocoreClientError]
    InvalidDBSubnetStateFault: Type[BotocoreClientError]
    InvalidEventSubscriptionStateFault: Type[BotocoreClientError]
    InvalidRestoreFault: Type[BotocoreClientError]
    InvalidSubnet: Type[BotocoreClientError]
    InvalidVPCNetworkStateFault: Type[BotocoreClientError]
    KMSKeyNotAccessibleFault: Type[BotocoreClientError]
    OptionGroupNotFoundFault: Type[BotocoreClientError]
    ProvisionedIopsNotAvailableInAZFault: Type[BotocoreClientError]
    ResourceNotFoundFault: Type[BotocoreClientError]
    SNSInvalidTopicFault: Type[BotocoreClientError]
    SNSNoAuthorizationFault: Type[BotocoreClientError]
    SNSTopicArnNotFoundFault: Type[BotocoreClientError]
    SharedSnapshotQuotaExceededFault: Type[BotocoreClientError]
    SnapshotQuotaExceededFault: Type[BotocoreClientError]
    SourceNotFoundFault: Type[BotocoreClientError]
    StorageQuotaExceededFault: Type[BotocoreClientError]
    StorageTypeNotSupportedFault: Type[BotocoreClientError]
    SubnetAlreadyInUse: Type[BotocoreClientError]
    SubscriptionAlreadyExistFault: Type[BotocoreClientError]
    SubscriptionCategoryNotFoundFault: Type[BotocoreClientError]
    SubscriptionNotFoundFault: Type[BotocoreClientError]


class NeptuneClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        NeptuneClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#exceptions)
        """

    async def add_role_to_db_cluster(
        self, *, DBClusterIdentifier: str, RoleArn: str, FeatureName: str = ...
    ) -> None:
        """
        Associates an Identity and Access Management (IAM) role with an Neptune DB
        cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.add_role_to_db_cluster)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#add_role_to_db_cluster)
        """

    async def add_source_identifier_to_subscription(
        self, *, SubscriptionName: str, SourceIdentifier: str
    ) -> AddSourceIdentifierToSubscriptionResultTypeDef:
        """
        Adds a source identifier to an existing event notification subscription.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.add_source_identifier_to_subscription)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#add_source_identifier_to_subscription)
        """

    async def add_tags_to_resource(
        self, *, ResourceName: str, Tags: Sequence["TagTypeDef"]
    ) -> None:
        """
        Adds metadata tags to an Amazon Neptune resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.add_tags_to_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#add_tags_to_resource)
        """

    async def apply_pending_maintenance_action(
        self, *, ResourceIdentifier: str, ApplyAction: str, OptInType: str
    ) -> ApplyPendingMaintenanceActionResultTypeDef:
        """
        Applies a pending maintenance action to a resource (for example, to a DB
        instance).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.apply_pending_maintenance_action)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#apply_pending_maintenance_action)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#can_paginate)
        """

    async def copy_db_cluster_parameter_group(
        self,
        *,
        SourceDBClusterParameterGroupIdentifier: str,
        TargetDBClusterParameterGroupIdentifier: str,
        TargetDBClusterParameterGroupDescription: str,
        Tags: Sequence["TagTypeDef"] = ...
    ) -> CopyDBClusterParameterGroupResultTypeDef:
        """
        Copies the specified DB cluster parameter group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.copy_db_cluster_parameter_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#copy_db_cluster_parameter_group)
        """

    async def copy_db_cluster_snapshot(
        self,
        *,
        SourceDBClusterSnapshotIdentifier: str,
        TargetDBClusterSnapshotIdentifier: str,
        KmsKeyId: str = ...,
        PreSignedUrl: str = ...,
        CopyTags: bool = ...,
        Tags: Sequence["TagTypeDef"] = ...,
        SourceRegion: str = ...
    ) -> CopyDBClusterSnapshotResultTypeDef:
        """
        Copies a snapshot of a DB cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.copy_db_cluster_snapshot)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#copy_db_cluster_snapshot)
        """

    async def copy_db_parameter_group(
        self,
        *,
        SourceDBParameterGroupIdentifier: str,
        TargetDBParameterGroupIdentifier: str,
        TargetDBParameterGroupDescription: str,
        Tags: Sequence["TagTypeDef"] = ...
    ) -> CopyDBParameterGroupResultTypeDef:
        """
        Copies the specified DB parameter group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.copy_db_parameter_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#copy_db_parameter_group)
        """

    async def create_db_cluster(
        self,
        *,
        DBClusterIdentifier: str,
        Engine: str,
        AvailabilityZones: Sequence[str] = ...,
        BackupRetentionPeriod: int = ...,
        CharacterSetName: str = ...,
        CopyTagsToSnapshot: bool = ...,
        DatabaseName: str = ...,
        DBClusterParameterGroupName: str = ...,
        VpcSecurityGroupIds: Sequence[str] = ...,
        DBSubnetGroupName: str = ...,
        EngineVersion: str = ...,
        Port: int = ...,
        MasterUsername: str = ...,
        MasterUserPassword: str = ...,
        OptionGroupName: str = ...,
        PreferredBackupWindow: str = ...,
        PreferredMaintenanceWindow: str = ...,
        ReplicationSourceIdentifier: str = ...,
        Tags: Sequence["TagTypeDef"] = ...,
        StorageEncrypted: bool = ...,
        KmsKeyId: str = ...,
        PreSignedUrl: str = ...,
        EnableIAMDatabaseAuthentication: bool = ...,
        EnableCloudwatchLogsExports: Sequence[str] = ...,
        DeletionProtection: bool = ...,
        SourceRegion: str = ...
    ) -> CreateDBClusterResultTypeDef:
        """
        Creates a new Amazon Neptune DB cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.create_db_cluster)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#create_db_cluster)
        """

    async def create_db_cluster_endpoint(
        self,
        *,
        DBClusterIdentifier: str,
        DBClusterEndpointIdentifier: str,
        EndpointType: str,
        StaticMembers: Sequence[str] = ...,
        ExcludedMembers: Sequence[str] = ...,
        Tags: Sequence["TagTypeDef"] = ...
    ) -> CreateDBClusterEndpointOutputTypeDef:
        """
        Creates a new custom endpoint and associates it with an Amazon Neptune DB
        cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.create_db_cluster_endpoint)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#create_db_cluster_endpoint)
        """

    async def create_db_cluster_parameter_group(
        self,
        *,
        DBClusterParameterGroupName: str,
        DBParameterGroupFamily: str,
        Description: str,
        Tags: Sequence["TagTypeDef"] = ...
    ) -> CreateDBClusterParameterGroupResultTypeDef:
        """
        Creates a new DB cluster parameter group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.create_db_cluster_parameter_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#create_db_cluster_parameter_group)
        """

    async def create_db_cluster_snapshot(
        self,
        *,
        DBClusterSnapshotIdentifier: str,
        DBClusterIdentifier: str,
        Tags: Sequence["TagTypeDef"] = ...
    ) -> CreateDBClusterSnapshotResultTypeDef:
        """
        Creates a snapshot of a DB cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.create_db_cluster_snapshot)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#create_db_cluster_snapshot)
        """

    async def create_db_instance(
        self,
        *,
        DBInstanceIdentifier: str,
        DBInstanceClass: str,
        Engine: str,
        DBName: str = ...,
        AllocatedStorage: int = ...,
        MasterUsername: str = ...,
        MasterUserPassword: str = ...,
        DBSecurityGroups: Sequence[str] = ...,
        VpcSecurityGroupIds: Sequence[str] = ...,
        AvailabilityZone: str = ...,
        DBSubnetGroupName: str = ...,
        PreferredMaintenanceWindow: str = ...,
        DBParameterGroupName: str = ...,
        BackupRetentionPeriod: int = ...,
        PreferredBackupWindow: str = ...,
        Port: int = ...,
        MultiAZ: bool = ...,
        EngineVersion: str = ...,
        AutoMinorVersionUpgrade: bool = ...,
        LicenseModel: str = ...,
        Iops: int = ...,
        OptionGroupName: str = ...,
        CharacterSetName: str = ...,
        PubliclyAccessible: bool = ...,
        Tags: Sequence["TagTypeDef"] = ...,
        DBClusterIdentifier: str = ...,
        StorageType: str = ...,
        TdeCredentialArn: str = ...,
        TdeCredentialPassword: str = ...,
        StorageEncrypted: bool = ...,
        KmsKeyId: str = ...,
        Domain: str = ...,
        CopyTagsToSnapshot: bool = ...,
        MonitoringInterval: int = ...,
        MonitoringRoleArn: str = ...,
        DomainIAMRoleName: str = ...,
        PromotionTier: int = ...,
        Timezone: str = ...,
        EnableIAMDatabaseAuthentication: bool = ...,
        EnablePerformanceInsights: bool = ...,
        PerformanceInsightsKMSKeyId: str = ...,
        EnableCloudwatchLogsExports: Sequence[str] = ...,
        DeletionProtection: bool = ...
    ) -> CreateDBInstanceResultTypeDef:
        """
        Creates a new DB instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.create_db_instance)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#create_db_instance)
        """

    async def create_db_parameter_group(
        self,
        *,
        DBParameterGroupName: str,
        DBParameterGroupFamily: str,
        Description: str,
        Tags: Sequence["TagTypeDef"] = ...
    ) -> CreateDBParameterGroupResultTypeDef:
        """
        Creates a new DB parameter group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.create_db_parameter_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#create_db_parameter_group)
        """

    async def create_db_subnet_group(
        self,
        *,
        DBSubnetGroupName: str,
        DBSubnetGroupDescription: str,
        SubnetIds: Sequence[str],
        Tags: Sequence["TagTypeDef"] = ...
    ) -> CreateDBSubnetGroupResultTypeDef:
        """
        Creates a new DB subnet group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.create_db_subnet_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#create_db_subnet_group)
        """

    async def create_event_subscription(
        self,
        *,
        SubscriptionName: str,
        SnsTopicArn: str,
        SourceType: str = ...,
        EventCategories: Sequence[str] = ...,
        SourceIds: Sequence[str] = ...,
        Enabled: bool = ...,
        Tags: Sequence["TagTypeDef"] = ...
    ) -> CreateEventSubscriptionResultTypeDef:
        """
        Creates an event notification subscription.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.create_event_subscription)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#create_event_subscription)
        """

    async def delete_db_cluster(
        self,
        *,
        DBClusterIdentifier: str,
        SkipFinalSnapshot: bool = ...,
        FinalDBSnapshotIdentifier: str = ...
    ) -> DeleteDBClusterResultTypeDef:
        """
        The DeleteDBCluster action deletes a previously provisioned DB cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.delete_db_cluster)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#delete_db_cluster)
        """

    async def delete_db_cluster_endpoint(
        self, *, DBClusterEndpointIdentifier: str
    ) -> DeleteDBClusterEndpointOutputTypeDef:
        """
        Deletes a custom endpoint and removes it from an Amazon Neptune DB cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.delete_db_cluster_endpoint)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#delete_db_cluster_endpoint)
        """

    async def delete_db_cluster_parameter_group(self, *, DBClusterParameterGroupName: str) -> None:
        """
        Deletes a specified DB cluster parameter group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.delete_db_cluster_parameter_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#delete_db_cluster_parameter_group)
        """

    async def delete_db_cluster_snapshot(
        self, *, DBClusterSnapshotIdentifier: str
    ) -> DeleteDBClusterSnapshotResultTypeDef:
        """
        Deletes a DB cluster snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.delete_db_cluster_snapshot)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#delete_db_cluster_snapshot)
        """

    async def delete_db_instance(
        self,
        *,
        DBInstanceIdentifier: str,
        SkipFinalSnapshot: bool = ...,
        FinalDBSnapshotIdentifier: str = ...
    ) -> DeleteDBInstanceResultTypeDef:
        """
        The DeleteDBInstance action deletes a previously provisioned DB instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.delete_db_instance)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#delete_db_instance)
        """

    async def delete_db_parameter_group(self, *, DBParameterGroupName: str) -> None:
        """
        Deletes a specified DBParameterGroup.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.delete_db_parameter_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#delete_db_parameter_group)
        """

    async def delete_db_subnet_group(self, *, DBSubnetGroupName: str) -> None:
        """
        Deletes a DB subnet group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.delete_db_subnet_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#delete_db_subnet_group)
        """

    async def delete_event_subscription(
        self, *, SubscriptionName: str
    ) -> DeleteEventSubscriptionResultTypeDef:
        """
        Deletes an event notification subscription.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.delete_event_subscription)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#delete_event_subscription)
        """

    async def describe_db_cluster_endpoints(
        self,
        *,
        DBClusterIdentifier: str = ...,
        DBClusterEndpointIdentifier: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        MaxRecords: int = ...,
        Marker: str = ...
    ) -> DBClusterEndpointMessageTypeDef:
        """
        Returns information about endpoints for an Amazon Neptune DB cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.describe_db_cluster_endpoints)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#describe_db_cluster_endpoints)
        """

    async def describe_db_cluster_parameter_groups(
        self,
        *,
        DBClusterParameterGroupName: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        MaxRecords: int = ...,
        Marker: str = ...
    ) -> DBClusterParameterGroupsMessageTypeDef:
        """
        Returns a list of `DBClusterParameterGroup` descriptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.describe_db_cluster_parameter_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#describe_db_cluster_parameter_groups)
        """

    async def describe_db_cluster_parameters(
        self,
        *,
        DBClusterParameterGroupName: str,
        Source: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        MaxRecords: int = ...,
        Marker: str = ...
    ) -> DBClusterParameterGroupDetailsTypeDef:
        """
        Returns the detailed parameter list for a particular DB cluster parameter group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.describe_db_cluster_parameters)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#describe_db_cluster_parameters)
        """

    async def describe_db_cluster_snapshot_attributes(
        self, *, DBClusterSnapshotIdentifier: str
    ) -> DescribeDBClusterSnapshotAttributesResultTypeDef:
        """
        Returns a list of DB cluster snapshot attribute names and values for a manual DB
        cluster snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.describe_db_cluster_snapshot_attributes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#describe_db_cluster_snapshot_attributes)
        """

    async def describe_db_cluster_snapshots(
        self,
        *,
        DBClusterIdentifier: str = ...,
        DBClusterSnapshotIdentifier: str = ...,
        SnapshotType: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        MaxRecords: int = ...,
        Marker: str = ...,
        IncludeShared: bool = ...,
        IncludePublic: bool = ...
    ) -> DBClusterSnapshotMessageTypeDef:
        """
        Returns information about DB cluster snapshots.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.describe_db_cluster_snapshots)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#describe_db_cluster_snapshots)
        """

    async def describe_db_clusters(
        self,
        *,
        DBClusterIdentifier: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        MaxRecords: int = ...,
        Marker: str = ...
    ) -> DBClusterMessageTypeDef:
        """
        Returns information about provisioned DB clusters, and supports pagination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.describe_db_clusters)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#describe_db_clusters)
        """

    async def describe_db_engine_versions(
        self,
        *,
        Engine: str = ...,
        EngineVersion: str = ...,
        DBParameterGroupFamily: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        MaxRecords: int = ...,
        Marker: str = ...,
        DefaultOnly: bool = ...,
        ListSupportedCharacterSets: bool = ...,
        ListSupportedTimezones: bool = ...
    ) -> DBEngineVersionMessageTypeDef:
        """
        Returns a list of the available DB engines.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.describe_db_engine_versions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#describe_db_engine_versions)
        """

    async def describe_db_instances(
        self,
        *,
        DBInstanceIdentifier: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        MaxRecords: int = ...,
        Marker: str = ...
    ) -> DBInstanceMessageTypeDef:
        """
        Returns information about provisioned instances, and supports pagination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.describe_db_instances)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#describe_db_instances)
        """

    async def describe_db_parameter_groups(
        self,
        *,
        DBParameterGroupName: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        MaxRecords: int = ...,
        Marker: str = ...
    ) -> DBParameterGroupsMessageTypeDef:
        """
        Returns a list of `DBParameterGroup` descriptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.describe_db_parameter_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#describe_db_parameter_groups)
        """

    async def describe_db_parameters(
        self,
        *,
        DBParameterGroupName: str,
        Source: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        MaxRecords: int = ...,
        Marker: str = ...
    ) -> DBParameterGroupDetailsTypeDef:
        """
        Returns the detailed parameter list for a particular DB parameter group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.describe_db_parameters)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#describe_db_parameters)
        """

    async def describe_db_subnet_groups(
        self,
        *,
        DBSubnetGroupName: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        MaxRecords: int = ...,
        Marker: str = ...
    ) -> DBSubnetGroupMessageTypeDef:
        """
        Returns a list of DBSubnetGroup descriptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.describe_db_subnet_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#describe_db_subnet_groups)
        """

    async def describe_engine_default_cluster_parameters(
        self,
        *,
        DBParameterGroupFamily: str,
        Filters: Sequence["FilterTypeDef"] = ...,
        MaxRecords: int = ...,
        Marker: str = ...
    ) -> DescribeEngineDefaultClusterParametersResultTypeDef:
        """
        Returns the default engine and system parameter information for the cluster
        database engine.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.describe_engine_default_cluster_parameters)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#describe_engine_default_cluster_parameters)
        """

    async def describe_engine_default_parameters(
        self,
        *,
        DBParameterGroupFamily: str,
        Filters: Sequence["FilterTypeDef"] = ...,
        MaxRecords: int = ...,
        Marker: str = ...
    ) -> DescribeEngineDefaultParametersResultTypeDef:
        """
        Returns the default engine and system parameter information for the specified
        database engine.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.describe_engine_default_parameters)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#describe_engine_default_parameters)
        """

    async def describe_event_categories(
        self, *, SourceType: str = ..., Filters: Sequence["FilterTypeDef"] = ...
    ) -> EventCategoriesMessageTypeDef:
        """
        Displays a list of categories for all event source types, or, if specified, for
        a specified source type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.describe_event_categories)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#describe_event_categories)
        """

    async def describe_event_subscriptions(
        self,
        *,
        SubscriptionName: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        MaxRecords: int = ...,
        Marker: str = ...
    ) -> EventSubscriptionsMessageTypeDef:
        """
        Lists all the subscription descriptions for a customer account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.describe_event_subscriptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#describe_event_subscriptions)
        """

    async def describe_events(
        self,
        *,
        SourceIdentifier: str = ...,
        SourceType: SourceTypeType = ...,
        StartTime: Union[datetime, str] = ...,
        EndTime: Union[datetime, str] = ...,
        Duration: int = ...,
        EventCategories: Sequence[str] = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        MaxRecords: int = ...,
        Marker: str = ...
    ) -> EventsMessageTypeDef:
        """
        Returns events related to DB instances, DB security groups, DB snapshots, and DB
        parameter groups for the past 14 days.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.describe_events)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#describe_events)
        """

    async def describe_orderable_db_instance_options(
        self,
        *,
        Engine: str,
        EngineVersion: str = ...,
        DBInstanceClass: str = ...,
        LicenseModel: str = ...,
        Vpc: bool = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        MaxRecords: int = ...,
        Marker: str = ...
    ) -> OrderableDBInstanceOptionsMessageTypeDef:
        """
        Returns a list of orderable DB instance options for the specified engine.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.describe_orderable_db_instance_options)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#describe_orderable_db_instance_options)
        """

    async def describe_pending_maintenance_actions(
        self,
        *,
        ResourceIdentifier: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        Marker: str = ...,
        MaxRecords: int = ...
    ) -> PendingMaintenanceActionsMessageTypeDef:
        """
        Returns a list of resources (for example, DB instances) that have at least one
        pending maintenance action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.describe_pending_maintenance_actions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#describe_pending_maintenance_actions)
        """

    async def describe_valid_db_instance_modifications(
        self, *, DBInstanceIdentifier: str
    ) -> DescribeValidDBInstanceModificationsResultTypeDef:
        """
        You can call  DescribeValidDBInstanceModifications to learn what modifications
        you can make to your DB instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.describe_valid_db_instance_modifications)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#describe_valid_db_instance_modifications)
        """

    async def failover_db_cluster(
        self, *, DBClusterIdentifier: str = ..., TargetDBInstanceIdentifier: str = ...
    ) -> FailoverDBClusterResultTypeDef:
        """
        Forces a failover for a DB cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.failover_db_cluster)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#failover_db_cluster)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#generate_presigned_url)
        """

    async def list_tags_for_resource(
        self, *, ResourceName: str, Filters: Sequence["FilterTypeDef"] = ...
    ) -> TagListMessageTypeDef:
        """
        Lists all tags on an Amazon Neptune resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#list_tags_for_resource)
        """

    async def modify_db_cluster(
        self,
        *,
        DBClusterIdentifier: str,
        NewDBClusterIdentifier: str = ...,
        ApplyImmediately: bool = ...,
        BackupRetentionPeriod: int = ...,
        DBClusterParameterGroupName: str = ...,
        VpcSecurityGroupIds: Sequence[str] = ...,
        Port: int = ...,
        MasterUserPassword: str = ...,
        OptionGroupName: str = ...,
        PreferredBackupWindow: str = ...,
        PreferredMaintenanceWindow: str = ...,
        EnableIAMDatabaseAuthentication: bool = ...,
        CloudwatchLogsExportConfiguration: "CloudwatchLogsExportConfigurationTypeDef" = ...,
        EngineVersion: str = ...,
        AllowMajorVersionUpgrade: bool = ...,
        DBInstanceParameterGroupName: str = ...,
        DeletionProtection: bool = ...,
        CopyTagsToSnapshot: bool = ...
    ) -> ModifyDBClusterResultTypeDef:
        """
        Modify a setting for a DB cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.modify_db_cluster)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#modify_db_cluster)
        """

    async def modify_db_cluster_endpoint(
        self,
        *,
        DBClusterEndpointIdentifier: str,
        EndpointType: str = ...,
        StaticMembers: Sequence[str] = ...,
        ExcludedMembers: Sequence[str] = ...
    ) -> ModifyDBClusterEndpointOutputTypeDef:
        """
        Modifies the properties of an endpoint in an Amazon Neptune DB cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.modify_db_cluster_endpoint)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#modify_db_cluster_endpoint)
        """

    async def modify_db_cluster_parameter_group(
        self, *, DBClusterParameterGroupName: str, Parameters: Sequence["ParameterTypeDef"]
    ) -> DBClusterParameterGroupNameMessageTypeDef:
        """
        Modifies the parameters of a DB cluster parameter group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.modify_db_cluster_parameter_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#modify_db_cluster_parameter_group)
        """

    async def modify_db_cluster_snapshot_attribute(
        self,
        *,
        DBClusterSnapshotIdentifier: str,
        AttributeName: str,
        ValuesToAdd: Sequence[str] = ...,
        ValuesToRemove: Sequence[str] = ...
    ) -> ModifyDBClusterSnapshotAttributeResultTypeDef:
        """
        Adds an attribute and values to, or removes an attribute and values from, a
        manual DB cluster snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.modify_db_cluster_snapshot_attribute)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#modify_db_cluster_snapshot_attribute)
        """

    async def modify_db_instance(
        self,
        *,
        DBInstanceIdentifier: str,
        AllocatedStorage: int = ...,
        DBInstanceClass: str = ...,
        DBSubnetGroupName: str = ...,
        DBSecurityGroups: Sequence[str] = ...,
        VpcSecurityGroupIds: Sequence[str] = ...,
        ApplyImmediately: bool = ...,
        MasterUserPassword: str = ...,
        DBParameterGroupName: str = ...,
        BackupRetentionPeriod: int = ...,
        PreferredBackupWindow: str = ...,
        PreferredMaintenanceWindow: str = ...,
        MultiAZ: bool = ...,
        EngineVersion: str = ...,
        AllowMajorVersionUpgrade: bool = ...,
        AutoMinorVersionUpgrade: bool = ...,
        LicenseModel: str = ...,
        Iops: int = ...,
        OptionGroupName: str = ...,
        NewDBInstanceIdentifier: str = ...,
        StorageType: str = ...,
        TdeCredentialArn: str = ...,
        TdeCredentialPassword: str = ...,
        CACertificateIdentifier: str = ...,
        Domain: str = ...,
        CopyTagsToSnapshot: bool = ...,
        MonitoringInterval: int = ...,
        DBPortNumber: int = ...,
        PubliclyAccessible: bool = ...,
        MonitoringRoleArn: str = ...,
        DomainIAMRoleName: str = ...,
        PromotionTier: int = ...,
        EnableIAMDatabaseAuthentication: bool = ...,
        EnablePerformanceInsights: bool = ...,
        PerformanceInsightsKMSKeyId: str = ...,
        CloudwatchLogsExportConfiguration: "CloudwatchLogsExportConfigurationTypeDef" = ...,
        DeletionProtection: bool = ...
    ) -> ModifyDBInstanceResultTypeDef:
        """
        Modifies settings for a DB instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.modify_db_instance)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#modify_db_instance)
        """

    async def modify_db_parameter_group(
        self, *, DBParameterGroupName: str, Parameters: Sequence["ParameterTypeDef"]
    ) -> DBParameterGroupNameMessageTypeDef:
        """
        Modifies the parameters of a DB parameter group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.modify_db_parameter_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#modify_db_parameter_group)
        """

    async def modify_db_subnet_group(
        self,
        *,
        DBSubnetGroupName: str,
        SubnetIds: Sequence[str],
        DBSubnetGroupDescription: str = ...
    ) -> ModifyDBSubnetGroupResultTypeDef:
        """
        Modifies an existing DB subnet group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.modify_db_subnet_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#modify_db_subnet_group)
        """

    async def modify_event_subscription(
        self,
        *,
        SubscriptionName: str,
        SnsTopicArn: str = ...,
        SourceType: str = ...,
        EventCategories: Sequence[str] = ...,
        Enabled: bool = ...
    ) -> ModifyEventSubscriptionResultTypeDef:
        """
        Modifies an existing event notification subscription.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.modify_event_subscription)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#modify_event_subscription)
        """

    async def promote_read_replica_db_cluster(
        self, *, DBClusterIdentifier: str
    ) -> PromoteReadReplicaDBClusterResultTypeDef:
        """
        Not supported.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.promote_read_replica_db_cluster)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#promote_read_replica_db_cluster)
        """

    async def reboot_db_instance(
        self, *, DBInstanceIdentifier: str, ForceFailover: bool = ...
    ) -> RebootDBInstanceResultTypeDef:
        """
        You might need to reboot your DB instance, usually for maintenance reasons.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.reboot_db_instance)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#reboot_db_instance)
        """

    async def remove_role_from_db_cluster(
        self, *, DBClusterIdentifier: str, RoleArn: str, FeatureName: str = ...
    ) -> None:
        """
        Disassociates an Identity and Access Management (IAM) role from a DB cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.remove_role_from_db_cluster)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#remove_role_from_db_cluster)
        """

    async def remove_source_identifier_from_subscription(
        self, *, SubscriptionName: str, SourceIdentifier: str
    ) -> RemoveSourceIdentifierFromSubscriptionResultTypeDef:
        """
        Removes a source identifier from an existing event notification subscription.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.remove_source_identifier_from_subscription)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#remove_source_identifier_from_subscription)
        """

    async def remove_tags_from_resource(self, *, ResourceName: str, TagKeys: Sequence[str]) -> None:
        """
        Removes metadata tags from an Amazon Neptune resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.remove_tags_from_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#remove_tags_from_resource)
        """

    async def reset_db_cluster_parameter_group(
        self,
        *,
        DBClusterParameterGroupName: str,
        ResetAllParameters: bool = ...,
        Parameters: Sequence["ParameterTypeDef"] = ...
    ) -> DBClusterParameterGroupNameMessageTypeDef:
        """
        Modifies the parameters of a DB cluster parameter group to the default value.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.reset_db_cluster_parameter_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#reset_db_cluster_parameter_group)
        """

    async def reset_db_parameter_group(
        self,
        *,
        DBParameterGroupName: str,
        ResetAllParameters: bool = ...,
        Parameters: Sequence["ParameterTypeDef"] = ...
    ) -> DBParameterGroupNameMessageTypeDef:
        """
        Modifies the parameters of a DB parameter group to the engine/system default
        value.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.reset_db_parameter_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#reset_db_parameter_group)
        """

    async def restore_db_cluster_from_snapshot(
        self,
        *,
        DBClusterIdentifier: str,
        SnapshotIdentifier: str,
        Engine: str,
        AvailabilityZones: Sequence[str] = ...,
        EngineVersion: str = ...,
        Port: int = ...,
        DBSubnetGroupName: str = ...,
        DatabaseName: str = ...,
        OptionGroupName: str = ...,
        VpcSecurityGroupIds: Sequence[str] = ...,
        Tags: Sequence["TagTypeDef"] = ...,
        KmsKeyId: str = ...,
        EnableIAMDatabaseAuthentication: bool = ...,
        EnableCloudwatchLogsExports: Sequence[str] = ...,
        DBClusterParameterGroupName: str = ...,
        DeletionProtection: bool = ...,
        CopyTagsToSnapshot: bool = ...
    ) -> RestoreDBClusterFromSnapshotResultTypeDef:
        """
        Creates a new DB cluster from a DB snapshot or DB cluster snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.restore_db_cluster_from_snapshot)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#restore_db_cluster_from_snapshot)
        """

    async def restore_db_cluster_to_point_in_time(
        self,
        *,
        DBClusterIdentifier: str,
        SourceDBClusterIdentifier: str,
        RestoreType: str = ...,
        RestoreToTime: Union[datetime, str] = ...,
        UseLatestRestorableTime: bool = ...,
        Port: int = ...,
        DBSubnetGroupName: str = ...,
        OptionGroupName: str = ...,
        VpcSecurityGroupIds: Sequence[str] = ...,
        Tags: Sequence["TagTypeDef"] = ...,
        KmsKeyId: str = ...,
        EnableIAMDatabaseAuthentication: bool = ...,
        EnableCloudwatchLogsExports: Sequence[str] = ...,
        DBClusterParameterGroupName: str = ...,
        DeletionProtection: bool = ...
    ) -> RestoreDBClusterToPointInTimeResultTypeDef:
        """
        Restores a DB cluster to an arbitrary point in time.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.restore_db_cluster_to_point_in_time)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#restore_db_cluster_to_point_in_time)
        """

    async def start_db_cluster(self, *, DBClusterIdentifier: str) -> StartDBClusterResultTypeDef:
        """
        Starts an Amazon Neptune DB cluster that was stopped using the Amazon console,
        the Amazon CLI stop-db-cluster command, or the StopDBCluster API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.start_db_cluster)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#start_db_cluster)
        """

    async def stop_db_cluster(self, *, DBClusterIdentifier: str) -> StopDBClusterResultTypeDef:
        """
        Stops an Amazon Neptune DB cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.stop_db_cluster)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#stop_db_cluster)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_db_cluster_endpoints"]
    ) -> DescribeDBClusterEndpointsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_db_cluster_parameter_groups"]
    ) -> DescribeDBClusterParameterGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_db_cluster_parameters"]
    ) -> DescribeDBClusterParametersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_db_cluster_snapshots"]
    ) -> DescribeDBClusterSnapshotsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_db_clusters"]
    ) -> DescribeDBClustersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_db_engine_versions"]
    ) -> DescribeDBEngineVersionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_db_instances"]
    ) -> DescribeDBInstancesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_db_parameter_groups"]
    ) -> DescribeDBParameterGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_db_parameters"]
    ) -> DescribeDBParametersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_db_subnet_groups"]
    ) -> DescribeDBSubnetGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_engine_default_parameters"]
    ) -> DescribeEngineDefaultParametersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_event_subscriptions"]
    ) -> DescribeEventSubscriptionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["describe_events"]) -> DescribeEventsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_orderable_db_instance_options"]
    ) -> DescribeOrderableDBInstanceOptionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_pending_maintenance_actions"]
    ) -> DescribePendingMaintenanceActionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#get_paginator)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["db_instance_available"]
    ) -> DBInstanceAvailableWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["db_instance_deleted"]) -> DBInstanceDeletedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/#get_waiter)
        """

    async def __aenter__(self) -> "NeptuneClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_neptune/client/)
        """
