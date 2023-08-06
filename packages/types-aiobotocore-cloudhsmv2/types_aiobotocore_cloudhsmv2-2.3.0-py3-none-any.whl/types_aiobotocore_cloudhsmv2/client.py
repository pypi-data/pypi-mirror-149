"""
Type annotations for cloudhsmv2 service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsmv2/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_cloudhsmv2.client import CloudHSMV2Client

    session = get_session()
    async with session.create_client("cloudhsmv2") as client:
        client: CloudHSMV2Client
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import DescribeBackupsPaginator, DescribeClustersPaginator, ListTagsPaginator
from .type_defs import (
    BackupRetentionPolicyTypeDef,
    CopyBackupToRegionResponseTypeDef,
    CreateClusterResponseTypeDef,
    CreateHsmResponseTypeDef,
    DeleteBackupResponseTypeDef,
    DeleteClusterResponseTypeDef,
    DeleteHsmResponseTypeDef,
    DescribeBackupsResponseTypeDef,
    DescribeClustersResponseTypeDef,
    InitializeClusterResponseTypeDef,
    ListTagsResponseTypeDef,
    ModifyBackupAttributesResponseTypeDef,
    ModifyClusterResponseTypeDef,
    RestoreBackupResponseTypeDef,
    TagTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("CloudHSMV2Client",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    CloudHsmAccessDeniedException: Type[BotocoreClientError]
    CloudHsmInternalFailureException: Type[BotocoreClientError]
    CloudHsmInvalidRequestException: Type[BotocoreClientError]
    CloudHsmResourceNotFoundException: Type[BotocoreClientError]
    CloudHsmServiceException: Type[BotocoreClientError]
    CloudHsmTagException: Type[BotocoreClientError]


class CloudHSMV2Client(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsmv2.html#CloudHSMV2.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsmv2/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CloudHSMV2Client exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsmv2.html#CloudHSMV2.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsmv2/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsmv2.html#CloudHSMV2.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsmv2/client/#can_paginate)
        """

    async def copy_backup_to_region(
        self, *, DestinationRegion: str, BackupId: str, TagList: Sequence["TagTypeDef"] = ...
    ) -> CopyBackupToRegionResponseTypeDef:
        """
        Copy an AWS CloudHSM cluster backup to a different region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsmv2.html#CloudHSMV2.Client.copy_backup_to_region)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsmv2/client/#copy_backup_to_region)
        """

    async def create_cluster(
        self,
        *,
        HsmType: str,
        SubnetIds: Sequence[str],
        BackupRetentionPolicy: "BackupRetentionPolicyTypeDef" = ...,
        SourceBackupId: str = ...,
        TagList: Sequence["TagTypeDef"] = ...
    ) -> CreateClusterResponseTypeDef:
        """
        Creates a new AWS CloudHSM cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsmv2.html#CloudHSMV2.Client.create_cluster)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsmv2/client/#create_cluster)
        """

    async def create_hsm(
        self, *, ClusterId: str, AvailabilityZone: str, IpAddress: str = ...
    ) -> CreateHsmResponseTypeDef:
        """
        Creates a new hardware security module (HSM) in the specified AWS CloudHSM
        cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsmv2.html#CloudHSMV2.Client.create_hsm)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsmv2/client/#create_hsm)
        """

    async def delete_backup(self, *, BackupId: str) -> DeleteBackupResponseTypeDef:
        """
        Deletes a specified AWS CloudHSM backup.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsmv2.html#CloudHSMV2.Client.delete_backup)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsmv2/client/#delete_backup)
        """

    async def delete_cluster(self, *, ClusterId: str) -> DeleteClusterResponseTypeDef:
        """
        Deletes the specified AWS CloudHSM cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsmv2.html#CloudHSMV2.Client.delete_cluster)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsmv2/client/#delete_cluster)
        """

    async def delete_hsm(
        self, *, ClusterId: str, HsmId: str = ..., EniId: str = ..., EniIp: str = ...
    ) -> DeleteHsmResponseTypeDef:
        """
        Deletes the specified HSM.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsmv2.html#CloudHSMV2.Client.delete_hsm)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsmv2/client/#delete_hsm)
        """

    async def describe_backups(
        self,
        *,
        NextToken: str = ...,
        MaxResults: int = ...,
        Filters: Mapping[str, Sequence[str]] = ...,
        SortAscending: bool = ...
    ) -> DescribeBackupsResponseTypeDef:
        """
        Gets information about backups of AWS CloudHSM clusters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsmv2.html#CloudHSMV2.Client.describe_backups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsmv2/client/#describe_backups)
        """

    async def describe_clusters(
        self,
        *,
        Filters: Mapping[str, Sequence[str]] = ...,
        NextToken: str = ...,
        MaxResults: int = ...
    ) -> DescribeClustersResponseTypeDef:
        """
        Gets information about AWS CloudHSM clusters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsmv2.html#CloudHSMV2.Client.describe_clusters)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsmv2/client/#describe_clusters)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsmv2.html#CloudHSMV2.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsmv2/client/#generate_presigned_url)
        """

    async def initialize_cluster(
        self, *, ClusterId: str, SignedCert: str, TrustAnchor: str
    ) -> InitializeClusterResponseTypeDef:
        """
        Claims an AWS CloudHSM cluster by submitting the cluster certificate issued by
        your issuing certificate authority (CA) and the CA's root certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsmv2.html#CloudHSMV2.Client.initialize_cluster)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsmv2/client/#initialize_cluster)
        """

    async def list_tags(
        self, *, ResourceId: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListTagsResponseTypeDef:
        """
        Gets a list of tags for the specified AWS CloudHSM cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsmv2.html#CloudHSMV2.Client.list_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsmv2/client/#list_tags)
        """

    async def modify_backup_attributes(
        self, *, BackupId: str, NeverExpires: bool
    ) -> ModifyBackupAttributesResponseTypeDef:
        """
        Modifies attributes for AWS CloudHSM backup.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsmv2.html#CloudHSMV2.Client.modify_backup_attributes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsmv2/client/#modify_backup_attributes)
        """

    async def modify_cluster(
        self, *, BackupRetentionPolicy: "BackupRetentionPolicyTypeDef", ClusterId: str
    ) -> ModifyClusterResponseTypeDef:
        """
        Modifies AWS CloudHSM cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsmv2.html#CloudHSMV2.Client.modify_cluster)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsmv2/client/#modify_cluster)
        """

    async def restore_backup(self, *, BackupId: str) -> RestoreBackupResponseTypeDef:
        """
        Restores a specified AWS CloudHSM backup that is in the `PENDING_DELETION`
        state.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsmv2.html#CloudHSMV2.Client.restore_backup)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsmv2/client/#restore_backup)
        """

    async def tag_resource(
        self, *, ResourceId: str, TagList: Sequence["TagTypeDef"]
    ) -> Dict[str, Any]:
        """
        Adds or overwrites one or more tags for the specified AWS CloudHSM cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsmv2.html#CloudHSMV2.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsmv2/client/#tag_resource)
        """

    async def untag_resource(self, *, ResourceId: str, TagKeyList: Sequence[str]) -> Dict[str, Any]:
        """
        Removes the specified tag or tags from the specified AWS CloudHSM cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsmv2.html#CloudHSMV2.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsmv2/client/#untag_resource)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_backups"]
    ) -> DescribeBackupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsmv2.html#CloudHSMV2.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsmv2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_clusters"]
    ) -> DescribeClustersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsmv2.html#CloudHSMV2.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsmv2/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_tags"]) -> ListTagsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsmv2.html#CloudHSMV2.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsmv2/client/#get_paginator)
        """

    async def __aenter__(self) -> "CloudHSMV2Client":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsmv2.html#CloudHSMV2.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsmv2/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsmv2.html#CloudHSMV2.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsmv2/client/)
        """
