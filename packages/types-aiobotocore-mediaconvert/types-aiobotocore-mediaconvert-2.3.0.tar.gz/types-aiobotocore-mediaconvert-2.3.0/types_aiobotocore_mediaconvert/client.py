"""
Type annotations for mediaconvert service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_mediaconvert.client import MediaConvertClient

    session = get_session()
    async with session.create_client("mediaconvert") as client:
        client: MediaConvertClient
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import (
    BillingTagsSourceType,
    DescribeEndpointsModeType,
    JobStatusType,
    JobTemplateListByType,
    OrderType,
    PresetListByType,
    PricingPlanType,
    QueueListByType,
    QueueStatusType,
    SimulateReservedQueueType,
    StatusUpdateIntervalType,
)
from .paginator import (
    DescribeEndpointsPaginator,
    ListJobsPaginator,
    ListJobTemplatesPaginator,
    ListPresetsPaginator,
    ListQueuesPaginator,
)
from .type_defs import (
    AccelerationSettingsTypeDef,
    CreateJobResponseTypeDef,
    CreateJobTemplateResponseTypeDef,
    CreatePresetResponseTypeDef,
    CreateQueueResponseTypeDef,
    DescribeEndpointsResponseTypeDef,
    GetJobResponseTypeDef,
    GetJobTemplateResponseTypeDef,
    GetPolicyResponseTypeDef,
    GetPresetResponseTypeDef,
    GetQueueResponseTypeDef,
    HopDestinationTypeDef,
    JobSettingsTypeDef,
    JobTemplateSettingsTypeDef,
    ListJobsResponseTypeDef,
    ListJobTemplatesResponseTypeDef,
    ListPresetsResponseTypeDef,
    ListQueuesResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    PolicyTypeDef,
    PresetSettingsTypeDef,
    PutPolicyResponseTypeDef,
    ReservationPlanSettingsTypeDef,
    UpdateJobTemplateResponseTypeDef,
    UpdatePresetResponseTypeDef,
    UpdateQueueResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("MediaConvertClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    ForbiddenException: Type[BotocoreClientError]
    InternalServerErrorException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]


class MediaConvertClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert.html#MediaConvert.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        MediaConvertClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert.html#MediaConvert.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/client/#exceptions)
        """

    async def associate_certificate(self, *, Arn: str) -> Dict[str, Any]:
        """
        Associates an AWS Certificate Manager (ACM) Amazon Resource Name (ARN) with AWS
        Elemental MediaConvert.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert.html#MediaConvert.Client.associate_certificate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/client/#associate_certificate)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert.html#MediaConvert.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/client/#can_paginate)
        """

    async def cancel_job(self, *, Id: str) -> Dict[str, Any]:
        """
        Permanently cancel a job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert.html#MediaConvert.Client.cancel_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/client/#cancel_job)
        """

    async def create_job(
        self,
        *,
        Role: str,
        Settings: "JobSettingsTypeDef",
        AccelerationSettings: "AccelerationSettingsTypeDef" = ...,
        BillingTagsSource: BillingTagsSourceType = ...,
        ClientRequestToken: str = ...,
        HopDestinations: Sequence["HopDestinationTypeDef"] = ...,
        JobTemplate: str = ...,
        Priority: int = ...,
        Queue: str = ...,
        SimulateReservedQueue: SimulateReservedQueueType = ...,
        StatusUpdateInterval: StatusUpdateIntervalType = ...,
        Tags: Mapping[str, str] = ...,
        UserMetadata: Mapping[str, str] = ...
    ) -> CreateJobResponseTypeDef:
        """
        Create a new transcoding job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert.html#MediaConvert.Client.create_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/client/#create_job)
        """

    async def create_job_template(
        self,
        *,
        Name: str,
        Settings: "JobTemplateSettingsTypeDef",
        AccelerationSettings: "AccelerationSettingsTypeDef" = ...,
        Category: str = ...,
        Description: str = ...,
        HopDestinations: Sequence["HopDestinationTypeDef"] = ...,
        Priority: int = ...,
        Queue: str = ...,
        StatusUpdateInterval: StatusUpdateIntervalType = ...,
        Tags: Mapping[str, str] = ...
    ) -> CreateJobTemplateResponseTypeDef:
        """
        Create a new job template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert.html#MediaConvert.Client.create_job_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/client/#create_job_template)
        """

    async def create_preset(
        self,
        *,
        Name: str,
        Settings: "PresetSettingsTypeDef",
        Category: str = ...,
        Description: str = ...,
        Tags: Mapping[str, str] = ...
    ) -> CreatePresetResponseTypeDef:
        """
        Create a new preset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert.html#MediaConvert.Client.create_preset)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/client/#create_preset)
        """

    async def create_queue(
        self,
        *,
        Name: str,
        Description: str = ...,
        PricingPlan: PricingPlanType = ...,
        ReservationPlanSettings: "ReservationPlanSettingsTypeDef" = ...,
        Status: QueueStatusType = ...,
        Tags: Mapping[str, str] = ...
    ) -> CreateQueueResponseTypeDef:
        """
        Create a new transcoding queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert.html#MediaConvert.Client.create_queue)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/client/#create_queue)
        """

    async def delete_job_template(self, *, Name: str) -> Dict[str, Any]:
        """
        Permanently delete a job template you have created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert.html#MediaConvert.Client.delete_job_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/client/#delete_job_template)
        """

    async def delete_policy(self) -> Dict[str, Any]:
        """
        Permanently delete a policy that you created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert.html#MediaConvert.Client.delete_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/client/#delete_policy)
        """

    async def delete_preset(self, *, Name: str) -> Dict[str, Any]:
        """
        Permanently delete a preset you have created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert.html#MediaConvert.Client.delete_preset)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/client/#delete_preset)
        """

    async def delete_queue(self, *, Name: str) -> Dict[str, Any]:
        """
        Permanently delete a queue you have created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert.html#MediaConvert.Client.delete_queue)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/client/#delete_queue)
        """

    async def describe_endpoints(
        self, *, MaxResults: int = ..., Mode: DescribeEndpointsModeType = ..., NextToken: str = ...
    ) -> DescribeEndpointsResponseTypeDef:
        """
        Send an request with an empty body to the regional API endpoint to get your
        account API endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert.html#MediaConvert.Client.describe_endpoints)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/client/#describe_endpoints)
        """

    async def disassociate_certificate(self, *, Arn: str) -> Dict[str, Any]:
        """
        Removes an association between the Amazon Resource Name (ARN) of an AWS
        Certificate Manager (ACM) certificate and an AWS Elemental MediaConvert
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert.html#MediaConvert.Client.disassociate_certificate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/client/#disassociate_certificate)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert.html#MediaConvert.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/client/#generate_presigned_url)
        """

    async def get_job(self, *, Id: str) -> GetJobResponseTypeDef:
        """
        Retrieve the JSON for a specific completed transcoding job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert.html#MediaConvert.Client.get_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/client/#get_job)
        """

    async def get_job_template(self, *, Name: str) -> GetJobTemplateResponseTypeDef:
        """
        Retrieve the JSON for a specific job template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert.html#MediaConvert.Client.get_job_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/client/#get_job_template)
        """

    async def get_policy(self) -> GetPolicyResponseTypeDef:
        """
        Retrieve the JSON for your policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert.html#MediaConvert.Client.get_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/client/#get_policy)
        """

    async def get_preset(self, *, Name: str) -> GetPresetResponseTypeDef:
        """
        Retrieve the JSON for a specific preset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert.html#MediaConvert.Client.get_preset)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/client/#get_preset)
        """

    async def get_queue(self, *, Name: str) -> GetQueueResponseTypeDef:
        """
        Retrieve the JSON for a specific queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert.html#MediaConvert.Client.get_queue)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/client/#get_queue)
        """

    async def list_job_templates(
        self,
        *,
        Category: str = ...,
        ListBy: JobTemplateListByType = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
        Order: OrderType = ...
    ) -> ListJobTemplatesResponseTypeDef:
        """
        Retrieve a JSON array of up to twenty of your job templates.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert.html#MediaConvert.Client.list_job_templates)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/client/#list_job_templates)
        """

    async def list_jobs(
        self,
        *,
        MaxResults: int = ...,
        NextToken: str = ...,
        Order: OrderType = ...,
        Queue: str = ...,
        Status: JobStatusType = ...
    ) -> ListJobsResponseTypeDef:
        """
        Retrieve a JSON array of up to twenty of your most recently created jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert.html#MediaConvert.Client.list_jobs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/client/#list_jobs)
        """

    async def list_presets(
        self,
        *,
        Category: str = ...,
        ListBy: PresetListByType = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
        Order: OrderType = ...
    ) -> ListPresetsResponseTypeDef:
        """
        Retrieve a JSON array of up to twenty of your presets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert.html#MediaConvert.Client.list_presets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/client/#list_presets)
        """

    async def list_queues(
        self,
        *,
        ListBy: QueueListByType = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
        Order: OrderType = ...
    ) -> ListQueuesResponseTypeDef:
        """
        Retrieve a JSON array of up to twenty of your queues.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert.html#MediaConvert.Client.list_queues)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/client/#list_queues)
        """

    async def list_tags_for_resource(self, *, Arn: str) -> ListTagsForResourceResponseTypeDef:
        """
        Retrieve the tags for a MediaConvert resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert.html#MediaConvert.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/client/#list_tags_for_resource)
        """

    async def put_policy(self, *, Policy: "PolicyTypeDef") -> PutPolicyResponseTypeDef:
        """
        Create or change your policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert.html#MediaConvert.Client.put_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/client/#put_policy)
        """

    async def tag_resource(self, *, Arn: str, Tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Add tags to a MediaConvert queue, preset, or job template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert.html#MediaConvert.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/client/#tag_resource)
        """

    async def untag_resource(self, *, Arn: str, TagKeys: Sequence[str] = ...) -> Dict[str, Any]:
        """
        Remove tags from a MediaConvert queue, preset, or job template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert.html#MediaConvert.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/client/#untag_resource)
        """

    async def update_job_template(
        self,
        *,
        Name: str,
        AccelerationSettings: "AccelerationSettingsTypeDef" = ...,
        Category: str = ...,
        Description: str = ...,
        HopDestinations: Sequence["HopDestinationTypeDef"] = ...,
        Priority: int = ...,
        Queue: str = ...,
        Settings: "JobTemplateSettingsTypeDef" = ...,
        StatusUpdateInterval: StatusUpdateIntervalType = ...
    ) -> UpdateJobTemplateResponseTypeDef:
        """
        Modify one of your existing job templates.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert.html#MediaConvert.Client.update_job_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/client/#update_job_template)
        """

    async def update_preset(
        self,
        *,
        Name: str,
        Category: str = ...,
        Description: str = ...,
        Settings: "PresetSettingsTypeDef" = ...
    ) -> UpdatePresetResponseTypeDef:
        """
        Modify one of your existing presets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert.html#MediaConvert.Client.update_preset)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/client/#update_preset)
        """

    async def update_queue(
        self,
        *,
        Name: str,
        Description: str = ...,
        ReservationPlanSettings: "ReservationPlanSettingsTypeDef" = ...,
        Status: QueueStatusType = ...
    ) -> UpdateQueueResponseTypeDef:
        """
        Modify one of your existing queues.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert.html#MediaConvert.Client.update_queue)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/client/#update_queue)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_endpoints"]
    ) -> DescribeEndpointsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert.html#MediaConvert.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_job_templates"]
    ) -> ListJobTemplatesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert.html#MediaConvert.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_jobs"]) -> ListJobsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert.html#MediaConvert.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_presets"]) -> ListPresetsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert.html#MediaConvert.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_queues"]) -> ListQueuesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert.html#MediaConvert.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/client/#get_paginator)
        """

    async def __aenter__(self) -> "MediaConvertClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert.html#MediaConvert.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert.html#MediaConvert.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/client/)
        """
