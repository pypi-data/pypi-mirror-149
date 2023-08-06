"""
Type annotations for lookoutvision service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutvision/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_lookoutvision.client import LookoutforVisionClient

    session = get_session()
    async with session.create_client("lookoutvision") as client:
        client: LookoutforVisionClient
    ```
"""
import sys
from datetime import datetime
from typing import IO, Any, Dict, Mapping, Sequence, Type, Union, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.response import StreamingBody

from .paginator import (
    ListDatasetEntriesPaginator,
    ListModelPackagingJobsPaginator,
    ListModelsPaginator,
    ListProjectsPaginator,
)
from .type_defs import (
    CreateDatasetResponseTypeDef,
    CreateModelResponseTypeDef,
    CreateProjectResponseTypeDef,
    DatasetSourceTypeDef,
    DeleteModelResponseTypeDef,
    DeleteProjectResponseTypeDef,
    DescribeDatasetResponseTypeDef,
    DescribeModelPackagingJobResponseTypeDef,
    DescribeModelResponseTypeDef,
    DescribeProjectResponseTypeDef,
    DetectAnomaliesResponseTypeDef,
    ListDatasetEntriesResponseTypeDef,
    ListModelPackagingJobsResponseTypeDef,
    ListModelsResponseTypeDef,
    ListProjectsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    ModelPackagingConfigurationTypeDef,
    OutputConfigTypeDef,
    StartModelPackagingJobResponseTypeDef,
    StartModelResponseTypeDef,
    StopModelResponseTypeDef,
    TagTypeDef,
    UpdateDatasetEntriesResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("LookoutforVisionClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class LookoutforVisionClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision.html#LookoutforVision.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutvision/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        LookoutforVisionClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision.html#LookoutforVision.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutvision/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision.html#LookoutforVision.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutvision/client/#can_paginate)
        """

    async def create_dataset(
        self,
        *,
        ProjectName: str,
        DatasetType: str,
        DatasetSource: "DatasetSourceTypeDef" = ...,
        ClientToken: str = ...
    ) -> CreateDatasetResponseTypeDef:
        """
        Creates a new dataset in an Amazon Lookout for Vision project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision.html#LookoutforVision.Client.create_dataset)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutvision/client/#create_dataset)
        """

    async def create_model(
        self,
        *,
        ProjectName: str,
        OutputConfig: "OutputConfigTypeDef",
        Description: str = ...,
        ClientToken: str = ...,
        KmsKeyId: str = ...,
        Tags: Sequence["TagTypeDef"] = ...
    ) -> CreateModelResponseTypeDef:
        """
        Creates a new version of a model within an an Amazon Lookout for Vision project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision.html#LookoutforVision.Client.create_model)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutvision/client/#create_model)
        """

    async def create_project(
        self, *, ProjectName: str, ClientToken: str = ...
    ) -> CreateProjectResponseTypeDef:
        """
        Creates an empty Amazon Lookout for Vision project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision.html#LookoutforVision.Client.create_project)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutvision/client/#create_project)
        """

    async def delete_dataset(
        self, *, ProjectName: str, DatasetType: str, ClientToken: str = ...
    ) -> Dict[str, Any]:
        """
        Deletes an existing Amazon Lookout for Vision `dataset` .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision.html#LookoutforVision.Client.delete_dataset)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutvision/client/#delete_dataset)
        """

    async def delete_model(
        self, *, ProjectName: str, ModelVersion: str, ClientToken: str = ...
    ) -> DeleteModelResponseTypeDef:
        """
        Deletes an Amazon Lookout for Vision model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision.html#LookoutforVision.Client.delete_model)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutvision/client/#delete_model)
        """

    async def delete_project(
        self, *, ProjectName: str, ClientToken: str = ...
    ) -> DeleteProjectResponseTypeDef:
        """
        Deletes an Amazon Lookout for Vision project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision.html#LookoutforVision.Client.delete_project)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutvision/client/#delete_project)
        """

    async def describe_dataset(
        self, *, ProjectName: str, DatasetType: str
    ) -> DescribeDatasetResponseTypeDef:
        """
        Describe an Amazon Lookout for Vision dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision.html#LookoutforVision.Client.describe_dataset)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutvision/client/#describe_dataset)
        """

    async def describe_model(
        self, *, ProjectName: str, ModelVersion: str
    ) -> DescribeModelResponseTypeDef:
        """
        Describes a version of an Amazon Lookout for Vision model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision.html#LookoutforVision.Client.describe_model)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutvision/client/#describe_model)
        """

    async def describe_model_packaging_job(
        self, *, ProjectName: str, JobName: str
    ) -> DescribeModelPackagingJobResponseTypeDef:
        """
        Describes an Amazon Lookout for Vision model packaging job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision.html#LookoutforVision.Client.describe_model_packaging_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutvision/client/#describe_model_packaging_job)
        """

    async def describe_project(self, *, ProjectName: str) -> DescribeProjectResponseTypeDef:
        """
        Describes an Amazon Lookout for Vision project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision.html#LookoutforVision.Client.describe_project)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutvision/client/#describe_project)
        """

    async def detect_anomalies(
        self,
        *,
        ProjectName: str,
        ModelVersion: str,
        Body: Union[str, bytes, IO[Any], StreamingBody],
        ContentType: str
    ) -> DetectAnomaliesResponseTypeDef:
        """
        Detects anomalies in an image that you supply.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision.html#LookoutforVision.Client.detect_anomalies)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutvision/client/#detect_anomalies)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision.html#LookoutforVision.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutvision/client/#generate_presigned_url)
        """

    async def list_dataset_entries(
        self,
        *,
        ProjectName: str,
        DatasetType: str,
        Labeled: bool = ...,
        AnomalyClass: str = ...,
        BeforeCreationDate: Union[datetime, str] = ...,
        AfterCreationDate: Union[datetime, str] = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
        SourceRefContains: str = ...
    ) -> ListDatasetEntriesResponseTypeDef:
        """
        Lists the JSON Lines within a dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision.html#LookoutforVision.Client.list_dataset_entries)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutvision/client/#list_dataset_entries)
        """

    async def list_model_packaging_jobs(
        self, *, ProjectName: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListModelPackagingJobsResponseTypeDef:
        """
        Lists the model packaging jobs created for an Amazon Lookout for Vision project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision.html#LookoutforVision.Client.list_model_packaging_jobs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutvision/client/#list_model_packaging_jobs)
        """

    async def list_models(
        self, *, ProjectName: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListModelsResponseTypeDef:
        """
        Lists the versions of a model in an Amazon Lookout for Vision project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision.html#LookoutforVision.Client.list_models)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutvision/client/#list_models)
        """

    async def list_projects(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> ListProjectsResponseTypeDef:
        """
        Lists the Amazon Lookout for Vision projects in your AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision.html#LookoutforVision.Client.list_projects)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutvision/client/#list_projects)
        """

    async def list_tags_for_resource(
        self, *, ResourceArn: str
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Returns a list of tags attached to the specified Amazon Lookout for Vision
        model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision.html#LookoutforVision.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutvision/client/#list_tags_for_resource)
        """

    async def start_model(
        self, *, ProjectName: str, ModelVersion: str, MinInferenceUnits: int, ClientToken: str = ...
    ) -> StartModelResponseTypeDef:
        """
        Starts the running of the version of an Amazon Lookout for Vision model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision.html#LookoutforVision.Client.start_model)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutvision/client/#start_model)
        """

    async def start_model_packaging_job(
        self,
        *,
        ProjectName: str,
        ModelVersion: str,
        Configuration: "ModelPackagingConfigurationTypeDef",
        JobName: str = ...,
        Description: str = ...,
        ClientToken: str = ...
    ) -> StartModelPackagingJobResponseTypeDef:
        """
        Starts an Amazon Lookout for Vision model packaging job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision.html#LookoutforVision.Client.start_model_packaging_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutvision/client/#start_model_packaging_job)
        """

    async def stop_model(
        self, *, ProjectName: str, ModelVersion: str, ClientToken: str = ...
    ) -> StopModelResponseTypeDef:
        """
        Stops the hosting of a running model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision.html#LookoutforVision.Client.stop_model)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutvision/client/#stop_model)
        """

    async def tag_resource(
        self, *, ResourceArn: str, Tags: Sequence["TagTypeDef"]
    ) -> Dict[str, Any]:
        """
        Adds one or more key-value tags to an Amazon Lookout for Vision model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision.html#LookoutforVision.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutvision/client/#tag_resource)
        """

    async def untag_resource(self, *, ResourceArn: str, TagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes one or more tags from an Amazon Lookout for Vision model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision.html#LookoutforVision.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutvision/client/#untag_resource)
        """

    async def update_dataset_entries(
        self,
        *,
        ProjectName: str,
        DatasetType: str,
        Changes: Union[str, bytes, IO[Any], StreamingBody],
        ClientToken: str = ...
    ) -> UpdateDatasetEntriesResponseTypeDef:
        """
        Adds or updates one or more JSON Line entries in a dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision.html#LookoutforVision.Client.update_dataset_entries)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutvision/client/#update_dataset_entries)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_dataset_entries"]
    ) -> ListDatasetEntriesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision.html#LookoutforVision.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutvision/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_model_packaging_jobs"]
    ) -> ListModelPackagingJobsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision.html#LookoutforVision.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutvision/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_models"]) -> ListModelsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision.html#LookoutforVision.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutvision/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_projects"]) -> ListProjectsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision.html#LookoutforVision.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutvision/client/#get_paginator)
        """

    async def __aenter__(self) -> "LookoutforVisionClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision.html#LookoutforVision.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutvision/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutvision.html#LookoutforVision.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutvision/client/)
        """
