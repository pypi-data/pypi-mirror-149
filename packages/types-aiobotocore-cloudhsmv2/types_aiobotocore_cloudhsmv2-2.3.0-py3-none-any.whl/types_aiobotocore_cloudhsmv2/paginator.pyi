"""
Type annotations for cloudhsmv2 service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsmv2/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_cloudhsmv2.client import CloudHSMV2Client
    from types_aiobotocore_cloudhsmv2.paginator import (
        DescribeBackupsPaginator,
        DescribeClustersPaginator,
        ListTagsPaginator,
    )

    session = get_session()
    with session.create_client("cloudhsmv2") as client:
        client: CloudHSMV2Client

        describe_backups_paginator: DescribeBackupsPaginator = client.get_paginator("describe_backups")
        describe_clusters_paginator: DescribeClustersPaginator = client.get_paginator("describe_clusters")
        list_tags_paginator: ListTagsPaginator = client.get_paginator("list_tags")
    ```
"""
import sys
from typing import Generic, Iterator, Mapping, Sequence, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    DescribeBackupsResponseTypeDef,
    DescribeClustersResponseTypeDef,
    ListTagsResponseTypeDef,
    PaginatorConfigTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import AsyncIterator
else:
    from typing_extensions import AsyncIterator

__all__ = ("DescribeBackupsPaginator", "DescribeClustersPaginator", "ListTagsPaginator")

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class DescribeBackupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsmv2.html#CloudHSMV2.Paginator.DescribeBackups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsmv2/paginators/#describebackupspaginator)
    """

    def paginate(
        self,
        *,
        Filters: Mapping[str, Sequence[str]] = ...,
        SortAscending: bool = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DescribeBackupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsmv2.html#CloudHSMV2.Paginator.DescribeBackups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsmv2/paginators/#describebackupspaginator)
        """

class DescribeClustersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsmv2.html#CloudHSMV2.Paginator.DescribeClusters)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsmv2/paginators/#describeclusterspaginator)
    """

    def paginate(
        self,
        *,
        Filters: Mapping[str, Sequence[str]] = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DescribeClustersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsmv2.html#CloudHSMV2.Paginator.DescribeClusters.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsmv2/paginators/#describeclusterspaginator)
        """

class ListTagsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsmv2.html#CloudHSMV2.Paginator.ListTags)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsmv2/paginators/#listtagspaginator)
    """

    def paginate(
        self, *, ResourceId: str, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListTagsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudhsmv2.html#CloudHSMV2.Paginator.ListTags.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudhsmv2/paginators/#listtagspaginator)
        """
