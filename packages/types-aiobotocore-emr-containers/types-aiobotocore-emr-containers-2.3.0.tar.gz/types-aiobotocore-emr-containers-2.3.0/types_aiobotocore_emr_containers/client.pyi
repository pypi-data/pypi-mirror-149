"""
Type annotations for emr-containers service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_containers/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_emr_containers.client import EMRContainersClient

    session = get_session()
    async with session.create_client("emr-containers") as client:
        client: EMRContainersClient
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, Mapping, Sequence, Type, Union, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import EndpointStateType, JobRunStateType, VirtualClusterStateType
from .paginator import (
    ListJobRunsPaginator,
    ListManagedEndpointsPaginator,
    ListVirtualClustersPaginator,
)
from .type_defs import (
    CancelJobRunResponseTypeDef,
    ConfigurationOverridesTypeDef,
    ContainerProviderTypeDef,
    CreateManagedEndpointResponseTypeDef,
    CreateVirtualClusterResponseTypeDef,
    DeleteManagedEndpointResponseTypeDef,
    DeleteVirtualClusterResponseTypeDef,
    DescribeJobRunResponseTypeDef,
    DescribeManagedEndpointResponseTypeDef,
    DescribeVirtualClusterResponseTypeDef,
    JobDriverTypeDef,
    ListJobRunsResponseTypeDef,
    ListManagedEndpointsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListVirtualClustersResponseTypeDef,
    StartJobRunResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("EMRContainersClient",)

class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    ClientError: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class EMRContainersClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-containers.html#EMRContainers.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_containers/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        EMRContainersClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-containers.html#EMRContainers.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_containers/client/#exceptions)
        """
    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-containers.html#EMRContainers.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_containers/client/#can_paginate)
        """
    async def cancel_job_run(
        self, *, id: str, virtualClusterId: str
    ) -> CancelJobRunResponseTypeDef:
        """
        Cancels a job run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-containers.html#EMRContainers.Client.cancel_job_run)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_containers/client/#cancel_job_run)
        """
    async def create_managed_endpoint(
        self,
        *,
        name: str,
        virtualClusterId: str,
        type: str,
        releaseLabel: str,
        executionRoleArn: str,
        clientToken: str,
        certificateArn: str = ...,
        configurationOverrides: "ConfigurationOverridesTypeDef" = ...,
        tags: Mapping[str, str] = ...
    ) -> CreateManagedEndpointResponseTypeDef:
        """
        Creates a managed endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-containers.html#EMRContainers.Client.create_managed_endpoint)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_containers/client/#create_managed_endpoint)
        """
    async def create_virtual_cluster(
        self,
        *,
        name: str,
        containerProvider: "ContainerProviderTypeDef",
        clientToken: str,
        tags: Mapping[str, str] = ...
    ) -> CreateVirtualClusterResponseTypeDef:
        """
        Creates a virtual cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-containers.html#EMRContainers.Client.create_virtual_cluster)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_containers/client/#create_virtual_cluster)
        """
    async def delete_managed_endpoint(
        self, *, id: str, virtualClusterId: str
    ) -> DeleteManagedEndpointResponseTypeDef:
        """
        Deletes a managed endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-containers.html#EMRContainers.Client.delete_managed_endpoint)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_containers/client/#delete_managed_endpoint)
        """
    async def delete_virtual_cluster(self, *, id: str) -> DeleteVirtualClusterResponseTypeDef:
        """
        Deletes a virtual cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-containers.html#EMRContainers.Client.delete_virtual_cluster)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_containers/client/#delete_virtual_cluster)
        """
    async def describe_job_run(
        self, *, id: str, virtualClusterId: str
    ) -> DescribeJobRunResponseTypeDef:
        """
        Displays detailed information about a job run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-containers.html#EMRContainers.Client.describe_job_run)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_containers/client/#describe_job_run)
        """
    async def describe_managed_endpoint(
        self, *, id: str, virtualClusterId: str
    ) -> DescribeManagedEndpointResponseTypeDef:
        """
        Displays detailed information about a managed endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-containers.html#EMRContainers.Client.describe_managed_endpoint)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_containers/client/#describe_managed_endpoint)
        """
    async def describe_virtual_cluster(self, *, id: str) -> DescribeVirtualClusterResponseTypeDef:
        """
        Displays detailed information about a specified virtual cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-containers.html#EMRContainers.Client.describe_virtual_cluster)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_containers/client/#describe_virtual_cluster)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-containers.html#EMRContainers.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_containers/client/#generate_presigned_url)
        """
    async def list_job_runs(
        self,
        *,
        virtualClusterId: str,
        createdBefore: Union[datetime, str] = ...,
        createdAfter: Union[datetime, str] = ...,
        name: str = ...,
        states: Sequence[JobRunStateType] = ...,
        maxResults: int = ...,
        nextToken: str = ...
    ) -> ListJobRunsResponseTypeDef:
        """
        Lists job runs based on a set of parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-containers.html#EMRContainers.Client.list_job_runs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_containers/client/#list_job_runs)
        """
    async def list_managed_endpoints(
        self,
        *,
        virtualClusterId: str,
        createdBefore: Union[datetime, str] = ...,
        createdAfter: Union[datetime, str] = ...,
        types: Sequence[str] = ...,
        states: Sequence[EndpointStateType] = ...,
        maxResults: int = ...,
        nextToken: str = ...
    ) -> ListManagedEndpointsResponseTypeDef:
        """
        Lists managed endpoints based on a set of parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-containers.html#EMRContainers.Client.list_managed_endpoints)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_containers/client/#list_managed_endpoints)
        """
    async def list_tags_for_resource(
        self, *, resourceArn: str
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags assigned to the resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-containers.html#EMRContainers.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_containers/client/#list_tags_for_resource)
        """
    async def list_virtual_clusters(
        self,
        *,
        containerProviderId: str = ...,
        containerProviderType: Literal["EKS"] = ...,
        createdAfter: Union[datetime, str] = ...,
        createdBefore: Union[datetime, str] = ...,
        states: Sequence[VirtualClusterStateType] = ...,
        maxResults: int = ...,
        nextToken: str = ...
    ) -> ListVirtualClustersResponseTypeDef:
        """
        Lists information about the specified virtual cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-containers.html#EMRContainers.Client.list_virtual_clusters)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_containers/client/#list_virtual_clusters)
        """
    async def start_job_run(
        self,
        *,
        virtualClusterId: str,
        clientToken: str,
        executionRoleArn: str,
        releaseLabel: str,
        jobDriver: "JobDriverTypeDef",
        name: str = ...,
        configurationOverrides: "ConfigurationOverridesTypeDef" = ...,
        tags: Mapping[str, str] = ...
    ) -> StartJobRunResponseTypeDef:
        """
        Starts a job run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-containers.html#EMRContainers.Client.start_job_run)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_containers/client/#start_job_run)
        """
    async def tag_resource(self, *, resourceArn: str, tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Assigns tags to resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-containers.html#EMRContainers.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_containers/client/#tag_resource)
        """
    async def untag_resource(self, *, resourceArn: str, tagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes tags from resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-containers.html#EMRContainers.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_containers/client/#untag_resource)
        """
    @overload
    def get_paginator(self, operation_name: Literal["list_job_runs"]) -> ListJobRunsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-containers.html#EMRContainers.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_containers/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_managed_endpoints"]
    ) -> ListManagedEndpointsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-containers.html#EMRContainers.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_containers/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_virtual_clusters"]
    ) -> ListVirtualClustersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-containers.html#EMRContainers.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_containers/client/#get_paginator)
        """
    async def __aenter__(self) -> "EMRContainersClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-containers.html#EMRContainers.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_containers/client/)
        """
    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-containers.html#EMRContainers.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_containers/client/)
        """
