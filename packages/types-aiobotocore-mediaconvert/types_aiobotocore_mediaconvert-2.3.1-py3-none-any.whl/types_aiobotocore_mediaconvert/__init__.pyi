"""
Main interface for mediaconvert service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_mediaconvert import (
        Client,
        DescribeEndpointsPaginator,
        ListJobTemplatesPaginator,
        ListJobsPaginator,
        ListPresetsPaginator,
        ListQueuesPaginator,
        MediaConvertClient,
    )

    session = get_session()
    async with session.create_client("mediaconvert") as client:
        client: MediaConvertClient
        ...


    describe_endpoints_paginator: DescribeEndpointsPaginator = client.get_paginator("describe_endpoints")
    list_job_templates_paginator: ListJobTemplatesPaginator = client.get_paginator("list_job_templates")
    list_jobs_paginator: ListJobsPaginator = client.get_paginator("list_jobs")
    list_presets_paginator: ListPresetsPaginator = client.get_paginator("list_presets")
    list_queues_paginator: ListQueuesPaginator = client.get_paginator("list_queues")
    ```
"""
from .client import MediaConvertClient
from .paginator import (
    DescribeEndpointsPaginator,
    ListJobsPaginator,
    ListJobTemplatesPaginator,
    ListPresetsPaginator,
    ListQueuesPaginator,
)

Client = MediaConvertClient

__all__ = (
    "Client",
    "DescribeEndpointsPaginator",
    "ListJobTemplatesPaginator",
    "ListJobsPaginator",
    "ListPresetsPaginator",
    "ListQueuesPaginator",
    "MediaConvertClient",
)
