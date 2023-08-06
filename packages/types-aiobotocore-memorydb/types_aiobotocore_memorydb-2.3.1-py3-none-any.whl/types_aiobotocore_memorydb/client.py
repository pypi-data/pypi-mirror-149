"""
Type annotations for memorydb service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_memorydb.client import MemoryDBClient

    session = get_session()
    async with session.create_client("memorydb") as client:
        client: MemoryDBClient
    ```
"""
from datetime import datetime
from typing import Any, Dict, Mapping, Sequence, Type, Union

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import ServiceUpdateStatusType, SourceTypeType
from .type_defs import (
    AuthenticationModeTypeDef,
    BatchUpdateClusterResponseTypeDef,
    CopySnapshotResponseTypeDef,
    CreateACLResponseTypeDef,
    CreateClusterResponseTypeDef,
    CreateParameterGroupResponseTypeDef,
    CreateSnapshotResponseTypeDef,
    CreateSubnetGroupResponseTypeDef,
    CreateUserResponseTypeDef,
    DeleteACLResponseTypeDef,
    DeleteClusterResponseTypeDef,
    DeleteParameterGroupResponseTypeDef,
    DeleteSnapshotResponseTypeDef,
    DeleteSubnetGroupResponseTypeDef,
    DeleteUserResponseTypeDef,
    DescribeACLsResponseTypeDef,
    DescribeClustersResponseTypeDef,
    DescribeEngineVersionsResponseTypeDef,
    DescribeEventsResponseTypeDef,
    DescribeParameterGroupsResponseTypeDef,
    DescribeParametersResponseTypeDef,
    DescribeServiceUpdatesResponseTypeDef,
    DescribeSnapshotsResponseTypeDef,
    DescribeSubnetGroupsResponseTypeDef,
    DescribeUsersResponseTypeDef,
    FailoverShardResponseTypeDef,
    FilterTypeDef,
    ListAllowedNodeTypeUpdatesResponseTypeDef,
    ListTagsResponseTypeDef,
    ParameterNameValueTypeDef,
    ReplicaConfigurationRequestTypeDef,
    ResetParameterGroupResponseTypeDef,
    ServiceUpdateRequestTypeDef,
    ShardConfigurationRequestTypeDef,
    TagResourceResponseTypeDef,
    TagTypeDef,
    UntagResourceResponseTypeDef,
    UpdateACLResponseTypeDef,
    UpdateClusterResponseTypeDef,
    UpdateParameterGroupResponseTypeDef,
    UpdateSubnetGroupResponseTypeDef,
    UpdateUserResponseTypeDef,
)

__all__ = ("MemoryDBClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ACLAlreadyExistsFault: Type[BotocoreClientError]
    ACLNotFoundFault: Type[BotocoreClientError]
    ACLQuotaExceededFault: Type[BotocoreClientError]
    APICallRateForCustomerExceededFault: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ClusterAlreadyExistsFault: Type[BotocoreClientError]
    ClusterNotFoundFault: Type[BotocoreClientError]
    ClusterQuotaForCustomerExceededFault: Type[BotocoreClientError]
    DefaultUserRequired: Type[BotocoreClientError]
    DuplicateUserNameFault: Type[BotocoreClientError]
    InsufficientClusterCapacityFault: Type[BotocoreClientError]
    InvalidACLStateFault: Type[BotocoreClientError]
    InvalidARNFault: Type[BotocoreClientError]
    InvalidClusterStateFault: Type[BotocoreClientError]
    InvalidCredentialsException: Type[BotocoreClientError]
    InvalidKMSKeyFault: Type[BotocoreClientError]
    InvalidNodeStateFault: Type[BotocoreClientError]
    InvalidParameterCombinationException: Type[BotocoreClientError]
    InvalidParameterGroupStateFault: Type[BotocoreClientError]
    InvalidParameterValueException: Type[BotocoreClientError]
    InvalidSnapshotStateFault: Type[BotocoreClientError]
    InvalidSubnet: Type[BotocoreClientError]
    InvalidUserStateFault: Type[BotocoreClientError]
    InvalidVPCNetworkStateFault: Type[BotocoreClientError]
    NoOperationFault: Type[BotocoreClientError]
    NodeQuotaForClusterExceededFault: Type[BotocoreClientError]
    NodeQuotaForCustomerExceededFault: Type[BotocoreClientError]
    ParameterGroupAlreadyExistsFault: Type[BotocoreClientError]
    ParameterGroupNotFoundFault: Type[BotocoreClientError]
    ParameterGroupQuotaExceededFault: Type[BotocoreClientError]
    ServiceLinkedRoleNotFoundFault: Type[BotocoreClientError]
    ServiceUpdateNotFoundFault: Type[BotocoreClientError]
    ShardNotFoundFault: Type[BotocoreClientError]
    ShardsPerClusterQuotaExceededFault: Type[BotocoreClientError]
    SnapshotAlreadyExistsFault: Type[BotocoreClientError]
    SnapshotNotFoundFault: Type[BotocoreClientError]
    SnapshotQuotaExceededFault: Type[BotocoreClientError]
    SubnetGroupAlreadyExistsFault: Type[BotocoreClientError]
    SubnetGroupInUseFault: Type[BotocoreClientError]
    SubnetGroupNotFoundFault: Type[BotocoreClientError]
    SubnetGroupQuotaExceededFault: Type[BotocoreClientError]
    SubnetInUse: Type[BotocoreClientError]
    SubnetNotAllowedFault: Type[BotocoreClientError]
    SubnetQuotaExceededFault: Type[BotocoreClientError]
    TagNotFoundFault: Type[BotocoreClientError]
    TagQuotaPerResourceExceeded: Type[BotocoreClientError]
    TestFailoverNotAvailableFault: Type[BotocoreClientError]
    UserAlreadyExistsFault: Type[BotocoreClientError]
    UserNotFoundFault: Type[BotocoreClientError]
    UserQuotaExceededFault: Type[BotocoreClientError]


class MemoryDBClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        MemoryDBClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#exceptions)
        """

    async def batch_update_cluster(
        self, *, ClusterNames: Sequence[str], ServiceUpdate: "ServiceUpdateRequestTypeDef" = ...
    ) -> BatchUpdateClusterResponseTypeDef:
        """
        Apply the service update to a list of clusters supplied.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.batch_update_cluster)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#batch_update_cluster)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#can_paginate)
        """

    async def copy_snapshot(
        self,
        *,
        SourceSnapshotName: str,
        TargetSnapshotName: str,
        TargetBucket: str = ...,
        KmsKeyId: str = ...,
        Tags: Sequence["TagTypeDef"] = ...
    ) -> CopySnapshotResponseTypeDef:
        """
        Makes a copy of an existing snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.copy_snapshot)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#copy_snapshot)
        """

    async def create_acl(
        self, *, ACLName: str, UserNames: Sequence[str] = ..., Tags: Sequence["TagTypeDef"] = ...
    ) -> CreateACLResponseTypeDef:
        """
        Creates an Access Control List.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.create_acl)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#create_acl)
        """

    async def create_cluster(
        self,
        *,
        ClusterName: str,
        NodeType: str,
        ACLName: str,
        ParameterGroupName: str = ...,
        Description: str = ...,
        NumShards: int = ...,
        NumReplicasPerShard: int = ...,
        SubnetGroupName: str = ...,
        SecurityGroupIds: Sequence[str] = ...,
        MaintenanceWindow: str = ...,
        Port: int = ...,
        SnsTopicArn: str = ...,
        TLSEnabled: bool = ...,
        KmsKeyId: str = ...,
        SnapshotArns: Sequence[str] = ...,
        SnapshotName: str = ...,
        SnapshotRetentionLimit: int = ...,
        Tags: Sequence["TagTypeDef"] = ...,
        SnapshotWindow: str = ...,
        EngineVersion: str = ...,
        AutoMinorVersionUpgrade: bool = ...
    ) -> CreateClusterResponseTypeDef:
        """
        Creates a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.create_cluster)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#create_cluster)
        """

    async def create_parameter_group(
        self,
        *,
        ParameterGroupName: str,
        Family: str,
        Description: str = ...,
        Tags: Sequence["TagTypeDef"] = ...
    ) -> CreateParameterGroupResponseTypeDef:
        """
        Creates a new MemoryDB parameter group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.create_parameter_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#create_parameter_group)
        """

    async def create_snapshot(
        self,
        *,
        ClusterName: str,
        SnapshotName: str,
        KmsKeyId: str = ...,
        Tags: Sequence["TagTypeDef"] = ...
    ) -> CreateSnapshotResponseTypeDef:
        """
        Creates a copy of an entire cluster at a specific moment in time.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.create_snapshot)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#create_snapshot)
        """

    async def create_subnet_group(
        self,
        *,
        SubnetGroupName: str,
        SubnetIds: Sequence[str],
        Description: str = ...,
        Tags: Sequence["TagTypeDef"] = ...
    ) -> CreateSubnetGroupResponseTypeDef:
        """
        Creates a subnet group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.create_subnet_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#create_subnet_group)
        """

    async def create_user(
        self,
        *,
        UserName: str,
        AuthenticationMode: "AuthenticationModeTypeDef",
        AccessString: str,
        Tags: Sequence["TagTypeDef"] = ...
    ) -> CreateUserResponseTypeDef:
        """
        Creates a MemoryDB user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.create_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#create_user)
        """

    async def delete_acl(self, *, ACLName: str) -> DeleteACLResponseTypeDef:
        """
        Deletes an Access Control List.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.delete_acl)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#delete_acl)
        """

    async def delete_cluster(
        self, *, ClusterName: str, FinalSnapshotName: str = ...
    ) -> DeleteClusterResponseTypeDef:
        """
        Deletes a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.delete_cluster)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#delete_cluster)
        """

    async def delete_parameter_group(
        self, *, ParameterGroupName: str
    ) -> DeleteParameterGroupResponseTypeDef:
        """
        Deletes the specified parameter group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.delete_parameter_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#delete_parameter_group)
        """

    async def delete_snapshot(self, *, SnapshotName: str) -> DeleteSnapshotResponseTypeDef:
        """
        Deletes an existing snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.delete_snapshot)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#delete_snapshot)
        """

    async def delete_subnet_group(
        self, *, SubnetGroupName: str
    ) -> DeleteSubnetGroupResponseTypeDef:
        """
        Deletes a subnet group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.delete_subnet_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#delete_subnet_group)
        """

    async def delete_user(self, *, UserName: str) -> DeleteUserResponseTypeDef:
        """
        Deletes a user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.delete_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#delete_user)
        """

    async def describe_acls(
        self, *, ACLName: str = ..., MaxResults: int = ..., NextToken: str = ...
    ) -> DescribeACLsResponseTypeDef:
        """
        Returns a list of ACLs See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/memorydb-2021-01-01/DescribeACLs).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.describe_acls)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#describe_acls)
        """

    async def describe_clusters(
        self,
        *,
        ClusterName: str = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
        ShowShardDetails: bool = ...
    ) -> DescribeClustersResponseTypeDef:
        """
        Returns information about all provisioned clusters if no cluster identifier is
        specified, or about a specific cluster if a cluster name is supplied.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.describe_clusters)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#describe_clusters)
        """

    async def describe_engine_versions(
        self,
        *,
        EngineVersion: str = ...,
        ParameterGroupFamily: str = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
        DefaultOnly: bool = ...
    ) -> DescribeEngineVersionsResponseTypeDef:
        """
        Returns a list of the available Redis engine versions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.describe_engine_versions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#describe_engine_versions)
        """

    async def describe_events(
        self,
        *,
        SourceName: str = ...,
        SourceType: SourceTypeType = ...,
        StartTime: Union[datetime, str] = ...,
        EndTime: Union[datetime, str] = ...,
        Duration: int = ...,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> DescribeEventsResponseTypeDef:
        """
        Returns events related to clusters, security groups, and parameter groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.describe_events)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#describe_events)
        """

    async def describe_parameter_groups(
        self, *, ParameterGroupName: str = ..., MaxResults: int = ..., NextToken: str = ...
    ) -> DescribeParameterGroupsResponseTypeDef:
        """
        Returns a list of parameter group descriptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.describe_parameter_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#describe_parameter_groups)
        """

    async def describe_parameters(
        self, *, ParameterGroupName: str, MaxResults: int = ..., NextToken: str = ...
    ) -> DescribeParametersResponseTypeDef:
        """
        Returns the detailed parameter list for a particular parameter group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.describe_parameters)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#describe_parameters)
        """

    async def describe_service_updates(
        self,
        *,
        ServiceUpdateName: str = ...,
        ClusterNames: Sequence[str] = ...,
        Status: Sequence[ServiceUpdateStatusType] = ...,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> DescribeServiceUpdatesResponseTypeDef:
        """
        Returns details of the service updates See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/memorydb-2021-01-01/DescribeServiceUpdates).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.describe_service_updates)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#describe_service_updates)
        """

    async def describe_snapshots(
        self,
        *,
        ClusterName: str = ...,
        SnapshotName: str = ...,
        Source: str = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
        ShowDetail: bool = ...
    ) -> DescribeSnapshotsResponseTypeDef:
        """
        Returns information about cluster snapshots.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.describe_snapshots)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#describe_snapshots)
        """

    async def describe_subnet_groups(
        self, *, SubnetGroupName: str = ..., MaxResults: int = ..., NextToken: str = ...
    ) -> DescribeSubnetGroupsResponseTypeDef:
        """
        Returns a list of subnet group descriptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.describe_subnet_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#describe_subnet_groups)
        """

    async def describe_users(
        self,
        *,
        UserName: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> DescribeUsersResponseTypeDef:
        """
        Returns a list of users.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.describe_users)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#describe_users)
        """

    async def failover_shard(
        self, *, ClusterName: str, ShardName: str
    ) -> FailoverShardResponseTypeDef:
        """
        Used to failover a shard See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/memorydb-2021-01-01/FailoverShard).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.failover_shard)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#failover_shard)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#generate_presigned_url)
        """

    async def list_allowed_node_type_updates(
        self, *, ClusterName: str
    ) -> ListAllowedNodeTypeUpdatesResponseTypeDef:
        """
        Lists all available node types that you can scale to from your cluster's current
        node type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.list_allowed_node_type_updates)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#list_allowed_node_type_updates)
        """

    async def list_tags(self, *, ResourceArn: str) -> ListTagsResponseTypeDef:
        """
        Lists all tags currently on a named resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.list_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#list_tags)
        """

    async def reset_parameter_group(
        self,
        *,
        ParameterGroupName: str,
        AllParameters: bool = ...,
        ParameterNames: Sequence[str] = ...
    ) -> ResetParameterGroupResponseTypeDef:
        """
        Modifies the parameters of a parameter group to the engine or system default
        value.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.reset_parameter_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#reset_parameter_group)
        """

    async def tag_resource(
        self, *, ResourceArn: str, Tags: Sequence["TagTypeDef"]
    ) -> TagResourceResponseTypeDef:
        """
        A tag is a key-value pair where the key and value are case-sensitive.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#tag_resource)
        """

    async def untag_resource(
        self, *, ResourceArn: str, TagKeys: Sequence[str]
    ) -> UntagResourceResponseTypeDef:
        """
        Use this operation to remove tags on a resource See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/memorydb-2021-01-01/UntagResource).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#untag_resource)
        """

    async def update_acl(
        self,
        *,
        ACLName: str,
        UserNamesToAdd: Sequence[str] = ...,
        UserNamesToRemove: Sequence[str] = ...
    ) -> UpdateACLResponseTypeDef:
        """
        Changes the list of users that belong to the Access Control List.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.update_acl)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#update_acl)
        """

    async def update_cluster(
        self,
        *,
        ClusterName: str,
        Description: str = ...,
        SecurityGroupIds: Sequence[str] = ...,
        MaintenanceWindow: str = ...,
        SnsTopicArn: str = ...,
        SnsTopicStatus: str = ...,
        ParameterGroupName: str = ...,
        SnapshotWindow: str = ...,
        SnapshotRetentionLimit: int = ...,
        NodeType: str = ...,
        EngineVersion: str = ...,
        ReplicaConfiguration: "ReplicaConfigurationRequestTypeDef" = ...,
        ShardConfiguration: "ShardConfigurationRequestTypeDef" = ...,
        ACLName: str = ...
    ) -> UpdateClusterResponseTypeDef:
        """
        Modifies the settings for a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.update_cluster)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#update_cluster)
        """

    async def update_parameter_group(
        self, *, ParameterGroupName: str, ParameterNameValues: Sequence["ParameterNameValueTypeDef"]
    ) -> UpdateParameterGroupResponseTypeDef:
        """
        Updates the parameters of a parameter group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.update_parameter_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#update_parameter_group)
        """

    async def update_subnet_group(
        self, *, SubnetGroupName: str, Description: str = ..., SubnetIds: Sequence[str] = ...
    ) -> UpdateSubnetGroupResponseTypeDef:
        """
        Updates a subnet group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.update_subnet_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#update_subnet_group)
        """

    async def update_user(
        self,
        *,
        UserName: str,
        AuthenticationMode: "AuthenticationModeTypeDef" = ...,
        AccessString: str = ...
    ) -> UpdateUserResponseTypeDef:
        """
        Changes user password(s) and/or access string.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client.update_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/#update_user)
        """

    async def __aenter__(self) -> "MemoryDBClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/memorydb.html#MemoryDB.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_memorydb/client/)
        """
