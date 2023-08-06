"""
Type annotations for mediapackage service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_mediapackage.client import MediaPackageClient
    from types_aiobotocore_mediapackage.paginator import (
        ListChannelsPaginator,
        ListHarvestJobsPaginator,
        ListOriginEndpointsPaginator,
    )

    session = get_session()
    with session.create_client("mediapackage") as client:
        client: MediaPackageClient

        list_channels_paginator: ListChannelsPaginator = client.get_paginator("list_channels")
        list_harvest_jobs_paginator: ListHarvestJobsPaginator = client.get_paginator("list_harvest_jobs")
        list_origin_endpoints_paginator: ListOriginEndpointsPaginator = client.get_paginator("list_origin_endpoints")
    ```
"""
import sys
from typing import Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListChannelsResponseTypeDef,
    ListHarvestJobsResponseTypeDef,
    ListOriginEndpointsResponseTypeDef,
    PaginatorConfigTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import AsyncIterator
else:
    from typing_extensions import AsyncIterator


__all__ = ("ListChannelsPaginator", "ListHarvestJobsPaginator", "ListOriginEndpointsPaginator")


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListChannelsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage.html#MediaPackage.Paginator.ListChannels)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage/paginators/#listchannelspaginator)
    """

    def paginate(
        self, *, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListChannelsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage.html#MediaPackage.Paginator.ListChannels.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage/paginators/#listchannelspaginator)
        """


class ListHarvestJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage.html#MediaPackage.Paginator.ListHarvestJobs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage/paginators/#listharvestjobspaginator)
    """

    def paginate(
        self,
        *,
        IncludeChannelId: str = ...,
        IncludeStatus: str = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListHarvestJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage.html#MediaPackage.Paginator.ListHarvestJobs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage/paginators/#listharvestjobspaginator)
        """


class ListOriginEndpointsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage.html#MediaPackage.Paginator.ListOriginEndpoints)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage/paginators/#listoriginendpointspaginator)
    """

    def paginate(
        self, *, ChannelId: str = ..., PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListOriginEndpointsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackage.html#MediaPackage.Paginator.ListOriginEndpoints.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackage/paginators/#listoriginendpointspaginator)
        """
