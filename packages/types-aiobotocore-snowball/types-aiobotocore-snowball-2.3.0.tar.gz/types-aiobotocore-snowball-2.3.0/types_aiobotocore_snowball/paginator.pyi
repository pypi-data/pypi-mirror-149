"""
Type annotations for snowball service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_snowball.client import SnowballClient
    from types_aiobotocore_snowball.paginator import (
        DescribeAddressesPaginator,
        ListClusterJobsPaginator,
        ListClustersPaginator,
        ListCompatibleImagesPaginator,
        ListJobsPaginator,
    )

    session = get_session()
    with session.create_client("snowball") as client:
        client: SnowballClient

        describe_addresses_paginator: DescribeAddressesPaginator = client.get_paginator("describe_addresses")
        list_cluster_jobs_paginator: ListClusterJobsPaginator = client.get_paginator("list_cluster_jobs")
        list_clusters_paginator: ListClustersPaginator = client.get_paginator("list_clusters")
        list_compatible_images_paginator: ListCompatibleImagesPaginator = client.get_paginator("list_compatible_images")
        list_jobs_paginator: ListJobsPaginator = client.get_paginator("list_jobs")
    ```
"""
import sys
from typing import Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    DescribeAddressesResultTypeDef,
    ListClusterJobsResultTypeDef,
    ListClustersResultTypeDef,
    ListCompatibleImagesResultTypeDef,
    ListJobsResultTypeDef,
    PaginatorConfigTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import AsyncIterator
else:
    from typing_extensions import AsyncIterator

__all__ = (
    "DescribeAddressesPaginator",
    "ListClusterJobsPaginator",
    "ListClustersPaginator",
    "ListCompatibleImagesPaginator",
    "ListJobsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class DescribeAddressesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball.html#Snowball.Paginator.DescribeAddresses)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/paginators/#describeaddressespaginator)
    """

    def paginate(
        self, *, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DescribeAddressesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball.html#Snowball.Paginator.DescribeAddresses.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/paginators/#describeaddressespaginator)
        """

class ListClusterJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball.html#Snowball.Paginator.ListClusterJobs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/paginators/#listclusterjobspaginator)
    """

    def paginate(
        self, *, ClusterId: str, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListClusterJobsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball.html#Snowball.Paginator.ListClusterJobs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/paginators/#listclusterjobspaginator)
        """

class ListClustersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball.html#Snowball.Paginator.ListClusters)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/paginators/#listclusterspaginator)
    """

    def paginate(
        self, *, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListClustersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball.html#Snowball.Paginator.ListClusters.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/paginators/#listclusterspaginator)
        """

class ListCompatibleImagesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball.html#Snowball.Paginator.ListCompatibleImages)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/paginators/#listcompatibleimagespaginator)
    """

    def paginate(
        self, *, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListCompatibleImagesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball.html#Snowball.Paginator.ListCompatibleImages.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/paginators/#listcompatibleimagespaginator)
        """

class ListJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball.html#Snowball.Paginator.ListJobs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/paginators/#listjobspaginator)
    """

    def paginate(
        self, *, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListJobsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball.html#Snowball.Paginator.ListJobs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_snowball/paginators/#listjobspaginator)
        """
