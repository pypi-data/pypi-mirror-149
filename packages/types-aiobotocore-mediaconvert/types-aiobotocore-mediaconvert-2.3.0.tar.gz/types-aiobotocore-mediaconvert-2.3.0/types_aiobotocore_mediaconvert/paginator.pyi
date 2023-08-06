"""
Type annotations for mediaconvert service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_mediaconvert.client import MediaConvertClient
    from types_aiobotocore_mediaconvert.paginator import (
        DescribeEndpointsPaginator,
        ListJobTemplatesPaginator,
        ListJobsPaginator,
        ListPresetsPaginator,
        ListQueuesPaginator,
    )

    session = get_session()
    with session.create_client("mediaconvert") as client:
        client: MediaConvertClient

        describe_endpoints_paginator: DescribeEndpointsPaginator = client.get_paginator("describe_endpoints")
        list_job_templates_paginator: ListJobTemplatesPaginator = client.get_paginator("list_job_templates")
        list_jobs_paginator: ListJobsPaginator = client.get_paginator("list_jobs")
        list_presets_paginator: ListPresetsPaginator = client.get_paginator("list_presets")
        list_queues_paginator: ListQueuesPaginator = client.get_paginator("list_queues")
    ```
"""
import sys
from typing import Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .literals import (
    DescribeEndpointsModeType,
    JobStatusType,
    JobTemplateListByType,
    OrderType,
    PresetListByType,
    QueueListByType,
)
from .type_defs import (
    DescribeEndpointsResponseTypeDef,
    ListJobsResponseTypeDef,
    ListJobTemplatesResponseTypeDef,
    ListPresetsResponseTypeDef,
    ListQueuesResponseTypeDef,
    PaginatorConfigTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import AsyncIterator
else:
    from typing_extensions import AsyncIterator

__all__ = (
    "DescribeEndpointsPaginator",
    "ListJobTemplatesPaginator",
    "ListJobsPaginator",
    "ListPresetsPaginator",
    "ListQueuesPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class DescribeEndpointsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert.html#MediaConvert.Paginator.DescribeEndpoints)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/paginators/#describeendpointspaginator)
    """

    def paginate(
        self,
        *,
        Mode: DescribeEndpointsModeType = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DescribeEndpointsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert.html#MediaConvert.Paginator.DescribeEndpoints.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/paginators/#describeendpointspaginator)
        """

class ListJobTemplatesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert.html#MediaConvert.Paginator.ListJobTemplates)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/paginators/#listjobtemplatespaginator)
    """

    def paginate(
        self,
        *,
        Category: str = ...,
        ListBy: JobTemplateListByType = ...,
        Order: OrderType = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListJobTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert.html#MediaConvert.Paginator.ListJobTemplates.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/paginators/#listjobtemplatespaginator)
        """

class ListJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert.html#MediaConvert.Paginator.ListJobs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/paginators/#listjobspaginator)
    """

    def paginate(
        self,
        *,
        Order: OrderType = ...,
        Queue: str = ...,
        Status: JobStatusType = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert.html#MediaConvert.Paginator.ListJobs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/paginators/#listjobspaginator)
        """

class ListPresetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert.html#MediaConvert.Paginator.ListPresets)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/paginators/#listpresetspaginator)
    """

    def paginate(
        self,
        *,
        Category: str = ...,
        ListBy: PresetListByType = ...,
        Order: OrderType = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListPresetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert.html#MediaConvert.Paginator.ListPresets.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/paginators/#listpresetspaginator)
        """

class ListQueuesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert.html#MediaConvert.Paginator.ListQueues)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/paginators/#listqueuespaginator)
    """

    def paginate(
        self,
        *,
        ListBy: QueueListByType = ...,
        Order: OrderType = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListQueuesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert.html#MediaConvert.Paginator.ListQueues.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/paginators/#listqueuespaginator)
        """
