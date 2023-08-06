"""
Type annotations for dax service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dax/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_dax.client import DAXClient
    from types_aiobotocore_dax.paginator import (
        DescribeClustersPaginator,
        DescribeDefaultParametersPaginator,
        DescribeEventsPaginator,
        DescribeParameterGroupsPaginator,
        DescribeParametersPaginator,
        DescribeSubnetGroupsPaginator,
        ListTagsPaginator,
    )

    session = get_session()
    with session.create_client("dax") as client:
        client: DAXClient

        describe_clusters_paginator: DescribeClustersPaginator = client.get_paginator("describe_clusters")
        describe_default_parameters_paginator: DescribeDefaultParametersPaginator = client.get_paginator("describe_default_parameters")
        describe_events_paginator: DescribeEventsPaginator = client.get_paginator("describe_events")
        describe_parameter_groups_paginator: DescribeParameterGroupsPaginator = client.get_paginator("describe_parameter_groups")
        describe_parameters_paginator: DescribeParametersPaginator = client.get_paginator("describe_parameters")
        describe_subnet_groups_paginator: DescribeSubnetGroupsPaginator = client.get_paginator("describe_subnet_groups")
        list_tags_paginator: ListTagsPaginator = client.get_paginator("list_tags")
    ```
"""
import sys
from datetime import datetime
from typing import Generic, Iterator, Sequence, TypeVar, Union

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .literals import SourceTypeType
from .type_defs import (
    DescribeClustersResponseTypeDef,
    DescribeDefaultParametersResponseTypeDef,
    DescribeEventsResponseTypeDef,
    DescribeParameterGroupsResponseTypeDef,
    DescribeParametersResponseTypeDef,
    DescribeSubnetGroupsResponseTypeDef,
    ListTagsResponseTypeDef,
    PaginatorConfigTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import AsyncIterator
else:
    from typing_extensions import AsyncIterator

__all__ = (
    "DescribeClustersPaginator",
    "DescribeDefaultParametersPaginator",
    "DescribeEventsPaginator",
    "DescribeParameterGroupsPaginator",
    "DescribeParametersPaginator",
    "DescribeSubnetGroupsPaginator",
    "ListTagsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class DescribeClustersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax.html#DAX.Paginator.DescribeClusters)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dax/paginators/#describeclusterspaginator)
    """

    def paginate(
        self, *, ClusterNames: Sequence[str] = ..., PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DescribeClustersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax.html#DAX.Paginator.DescribeClusters.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dax/paginators/#describeclusterspaginator)
        """

class DescribeDefaultParametersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax.html#DAX.Paginator.DescribeDefaultParameters)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dax/paginators/#describedefaultparameterspaginator)
    """

    def paginate(
        self, *, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DescribeDefaultParametersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax.html#DAX.Paginator.DescribeDefaultParameters.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dax/paginators/#describedefaultparameterspaginator)
        """

class DescribeEventsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax.html#DAX.Paginator.DescribeEvents)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dax/paginators/#describeeventspaginator)
    """

    def paginate(
        self,
        *,
        SourceName: str = ...,
        SourceType: SourceTypeType = ...,
        StartTime: Union[datetime, str] = ...,
        EndTime: Union[datetime, str] = ...,
        Duration: int = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DescribeEventsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax.html#DAX.Paginator.DescribeEvents.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dax/paginators/#describeeventspaginator)
        """

class DescribeParameterGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax.html#DAX.Paginator.DescribeParameterGroups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dax/paginators/#describeparametergroupspaginator)
    """

    def paginate(
        self,
        *,
        ParameterGroupNames: Sequence[str] = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DescribeParameterGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax.html#DAX.Paginator.DescribeParameterGroups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dax/paginators/#describeparametergroupspaginator)
        """

class DescribeParametersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax.html#DAX.Paginator.DescribeParameters)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dax/paginators/#describeparameterspaginator)
    """

    def paginate(
        self,
        *,
        ParameterGroupName: str,
        Source: str = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DescribeParametersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax.html#DAX.Paginator.DescribeParameters.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dax/paginators/#describeparameterspaginator)
        """

class DescribeSubnetGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax.html#DAX.Paginator.DescribeSubnetGroups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dax/paginators/#describesubnetgroupspaginator)
    """

    def paginate(
        self,
        *,
        SubnetGroupNames: Sequence[str] = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DescribeSubnetGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax.html#DAX.Paginator.DescribeSubnetGroups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dax/paginators/#describesubnetgroupspaginator)
        """

class ListTagsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax.html#DAX.Paginator.ListTags)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dax/paginators/#listtagspaginator)
    """

    def paginate(
        self, *, ResourceName: str, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListTagsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dax.html#DAX.Paginator.ListTags.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dax/paginators/#listtagspaginator)
        """
