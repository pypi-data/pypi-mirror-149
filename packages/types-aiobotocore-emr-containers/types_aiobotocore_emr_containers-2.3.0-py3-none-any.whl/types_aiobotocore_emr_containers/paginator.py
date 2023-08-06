"""
Type annotations for emr-containers service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_containers/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_emr_containers.client import EMRContainersClient
    from types_aiobotocore_emr_containers.paginator import (
        ListJobRunsPaginator,
        ListManagedEndpointsPaginator,
        ListVirtualClustersPaginator,
    )

    session = get_session()
    with session.create_client("emr-containers") as client:
        client: EMRContainersClient

        list_job_runs_paginator: ListJobRunsPaginator = client.get_paginator("list_job_runs")
        list_managed_endpoints_paginator: ListManagedEndpointsPaginator = client.get_paginator("list_managed_endpoints")
        list_virtual_clusters_paginator: ListVirtualClustersPaginator = client.get_paginator("list_virtual_clusters")
    ```
"""
import sys
from datetime import datetime
from typing import Generic, Iterator, Sequence, TypeVar, Union

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .literals import EndpointStateType, JobRunStateType, VirtualClusterStateType
from .type_defs import (
    ListJobRunsResponseTypeDef,
    ListManagedEndpointsResponseTypeDef,
    ListVirtualClustersResponseTypeDef,
    PaginatorConfigTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import AsyncIterator
else:
    from typing_extensions import AsyncIterator
if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("ListJobRunsPaginator", "ListManagedEndpointsPaginator", "ListVirtualClustersPaginator")


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListJobRunsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-containers.html#EMRContainers.Paginator.ListJobRuns)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_containers/paginators/#listjobrunspaginator)
    """

    def paginate(
        self,
        *,
        virtualClusterId: str,
        createdBefore: Union[datetime, str] = ...,
        createdAfter: Union[datetime, str] = ...,
        name: str = ...,
        states: Sequence[JobRunStateType] = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListJobRunsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-containers.html#EMRContainers.Paginator.ListJobRuns.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_containers/paginators/#listjobrunspaginator)
        """


class ListManagedEndpointsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-containers.html#EMRContainers.Paginator.ListManagedEndpoints)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_containers/paginators/#listmanagedendpointspaginator)
    """

    def paginate(
        self,
        *,
        virtualClusterId: str,
        createdBefore: Union[datetime, str] = ...,
        createdAfter: Union[datetime, str] = ...,
        types: Sequence[str] = ...,
        states: Sequence[EndpointStateType] = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListManagedEndpointsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-containers.html#EMRContainers.Paginator.ListManagedEndpoints.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_containers/paginators/#listmanagedendpointspaginator)
        """


class ListVirtualClustersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-containers.html#EMRContainers.Paginator.ListVirtualClusters)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_containers/paginators/#listvirtualclusterspaginator)
    """

    def paginate(
        self,
        *,
        containerProviderId: str = ...,
        containerProviderType: Literal["EKS"] = ...,
        createdAfter: Union[datetime, str] = ...,
        createdBefore: Union[datetime, str] = ...,
        states: Sequence[VirtualClusterStateType] = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListVirtualClustersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-containers.html#EMRContainers.Paginator.ListVirtualClusters.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_containers/paginators/#listvirtualclusterspaginator)
        """
