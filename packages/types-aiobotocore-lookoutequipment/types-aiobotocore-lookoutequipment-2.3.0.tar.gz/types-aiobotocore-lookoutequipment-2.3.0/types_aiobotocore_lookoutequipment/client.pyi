"""
Type annotations for lookoutequipment service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_lookoutequipment.client import LookoutEquipmentClient

    session = get_session()
    async with session.create_client("lookoutequipment") as client:
        client: LookoutEquipmentClient
    ```
"""
from datetime import datetime
from typing import Any, Dict, Mapping, Sequence, Type, Union

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import (
    DataUploadFrequencyType,
    InferenceExecutionStatusType,
    IngestionJobStatusType,
    ModelStatusType,
)
from .type_defs import (
    CreateDatasetResponseTypeDef,
    CreateInferenceSchedulerResponseTypeDef,
    CreateModelResponseTypeDef,
    DataPreProcessingConfigurationTypeDef,
    DatasetSchemaTypeDef,
    DescribeDataIngestionJobResponseTypeDef,
    DescribeDatasetResponseTypeDef,
    DescribeInferenceSchedulerResponseTypeDef,
    DescribeModelResponseTypeDef,
    InferenceInputConfigurationTypeDef,
    InferenceOutputConfigurationTypeDef,
    IngestionInputConfigurationTypeDef,
    LabelsInputConfigurationTypeDef,
    ListDataIngestionJobsResponseTypeDef,
    ListDatasetsResponseTypeDef,
    ListInferenceExecutionsResponseTypeDef,
    ListInferenceSchedulersResponseTypeDef,
    ListModelsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    StartDataIngestionJobResponseTypeDef,
    StartInferenceSchedulerResponseTypeDef,
    StopInferenceSchedulerResponseTypeDef,
    TagTypeDef,
)

__all__ = ("LookoutEquipmentClient",)

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

class LookoutEquipmentClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment.html#LookoutEquipment.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        LookoutEquipmentClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment.html#LookoutEquipment.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#exceptions)
        """
    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment.html#LookoutEquipment.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#can_paginate)
        """
    async def create_dataset(
        self,
        *,
        DatasetName: str,
        DatasetSchema: "DatasetSchemaTypeDef",
        ClientToken: str,
        ServerSideKmsKeyId: str = ...,
        Tags: Sequence["TagTypeDef"] = ...
    ) -> CreateDatasetResponseTypeDef:
        """
        Creates a container for a collection of data being ingested for analysis.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment.html#LookoutEquipment.Client.create_dataset)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#create_dataset)
        """
    async def create_inference_scheduler(
        self,
        *,
        ModelName: str,
        InferenceSchedulerName: str,
        DataUploadFrequency: DataUploadFrequencyType,
        DataInputConfiguration: "InferenceInputConfigurationTypeDef",
        DataOutputConfiguration: "InferenceOutputConfigurationTypeDef",
        RoleArn: str,
        ClientToken: str,
        DataDelayOffsetInMinutes: int = ...,
        ServerSideKmsKeyId: str = ...,
        Tags: Sequence["TagTypeDef"] = ...
    ) -> CreateInferenceSchedulerResponseTypeDef:
        """
        Creates a scheduled inference.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment.html#LookoutEquipment.Client.create_inference_scheduler)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#create_inference_scheduler)
        """
    async def create_model(
        self,
        *,
        ModelName: str,
        DatasetName: str,
        ClientToken: str,
        DatasetSchema: "DatasetSchemaTypeDef" = ...,
        LabelsInputConfiguration: "LabelsInputConfigurationTypeDef" = ...,
        TrainingDataStartTime: Union[datetime, str] = ...,
        TrainingDataEndTime: Union[datetime, str] = ...,
        EvaluationDataStartTime: Union[datetime, str] = ...,
        EvaluationDataEndTime: Union[datetime, str] = ...,
        RoleArn: str = ...,
        DataPreProcessingConfiguration: "DataPreProcessingConfigurationTypeDef" = ...,
        ServerSideKmsKeyId: str = ...,
        Tags: Sequence["TagTypeDef"] = ...,
        OffCondition: str = ...
    ) -> CreateModelResponseTypeDef:
        """
        Creates an ML model for data inference.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment.html#LookoutEquipment.Client.create_model)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#create_model)
        """
    async def delete_dataset(self, *, DatasetName: str) -> None:
        """
        Deletes a dataset and associated artifacts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment.html#LookoutEquipment.Client.delete_dataset)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#delete_dataset)
        """
    async def delete_inference_scheduler(self, *, InferenceSchedulerName: str) -> None:
        """
        Deletes an inference scheduler that has been set up.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment.html#LookoutEquipment.Client.delete_inference_scheduler)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#delete_inference_scheduler)
        """
    async def delete_model(self, *, ModelName: str) -> None:
        """
        Deletes an ML model currently available for Amazon Lookout for Equipment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment.html#LookoutEquipment.Client.delete_model)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#delete_model)
        """
    async def describe_data_ingestion_job(
        self, *, JobId: str
    ) -> DescribeDataIngestionJobResponseTypeDef:
        """
        Provides information on a specific data ingestion job such as creation time,
        dataset ARN, status, and so on.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment.html#LookoutEquipment.Client.describe_data_ingestion_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#describe_data_ingestion_job)
        """
    async def describe_dataset(self, *, DatasetName: str) -> DescribeDatasetResponseTypeDef:
        """
        Provides a JSON description of the data that is in each time series dataset,
        including names, column names, and data types.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment.html#LookoutEquipment.Client.describe_dataset)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#describe_dataset)
        """
    async def describe_inference_scheduler(
        self, *, InferenceSchedulerName: str
    ) -> DescribeInferenceSchedulerResponseTypeDef:
        """
        Specifies information about the inference scheduler being used, including name,
        model, status, and associated metadata See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/lookoutequipment-2020-12-15/DescribeInferenceScheduler).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment.html#LookoutEquipment.Client.describe_inference_scheduler)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#describe_inference_scheduler)
        """
    async def describe_model(self, *, ModelName: str) -> DescribeModelResponseTypeDef:
        """
        Provides a JSON containing the overall information about a specific ML model,
        including model name and ARN, dataset, training and evaluation information,
        status, and so on.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment.html#LookoutEquipment.Client.describe_model)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#describe_model)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment.html#LookoutEquipment.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#generate_presigned_url)
        """
    async def list_data_ingestion_jobs(
        self,
        *,
        DatasetName: str = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
        Status: IngestionJobStatusType = ...
    ) -> ListDataIngestionJobsResponseTypeDef:
        """
        Provides a list of all data ingestion jobs, including dataset name and ARN, S3
        location of the input data, status, and so on.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment.html#LookoutEquipment.Client.list_data_ingestion_jobs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#list_data_ingestion_jobs)
        """
    async def list_datasets(
        self, *, NextToken: str = ..., MaxResults: int = ..., DatasetNameBeginsWith: str = ...
    ) -> ListDatasetsResponseTypeDef:
        """
        Lists all datasets currently available in your account, filtering on the dataset
        name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment.html#LookoutEquipment.Client.list_datasets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#list_datasets)
        """
    async def list_inference_executions(
        self,
        *,
        InferenceSchedulerName: str,
        NextToken: str = ...,
        MaxResults: int = ...,
        DataStartTimeAfter: Union[datetime, str] = ...,
        DataEndTimeBefore: Union[datetime, str] = ...,
        Status: InferenceExecutionStatusType = ...
    ) -> ListInferenceExecutionsResponseTypeDef:
        """
        Lists all inference executions that have been performed by the specified
        inference scheduler.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment.html#LookoutEquipment.Client.list_inference_executions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#list_inference_executions)
        """
    async def list_inference_schedulers(
        self,
        *,
        NextToken: str = ...,
        MaxResults: int = ...,
        InferenceSchedulerNameBeginsWith: str = ...,
        ModelName: str = ...
    ) -> ListInferenceSchedulersResponseTypeDef:
        """
        Retrieves a list of all inference schedulers currently available for your
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment.html#LookoutEquipment.Client.list_inference_schedulers)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#list_inference_schedulers)
        """
    async def list_models(
        self,
        *,
        NextToken: str = ...,
        MaxResults: int = ...,
        Status: ModelStatusType = ...,
        ModelNameBeginsWith: str = ...,
        DatasetNameBeginsWith: str = ...
    ) -> ListModelsResponseTypeDef:
        """
        Generates a list of all models in the account, including model name and ARN,
        dataset, and status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment.html#LookoutEquipment.Client.list_models)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#list_models)
        """
    async def list_tags_for_resource(
        self, *, ResourceArn: str
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists all the tags for a specified resource, including key and value.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment.html#LookoutEquipment.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#list_tags_for_resource)
        """
    async def start_data_ingestion_job(
        self,
        *,
        DatasetName: str,
        IngestionInputConfiguration: "IngestionInputConfigurationTypeDef",
        RoleArn: str,
        ClientToken: str
    ) -> StartDataIngestionJobResponseTypeDef:
        """
        Starts a data ingestion job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment.html#LookoutEquipment.Client.start_data_ingestion_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#start_data_ingestion_job)
        """
    async def start_inference_scheduler(
        self, *, InferenceSchedulerName: str
    ) -> StartInferenceSchedulerResponseTypeDef:
        """
        Starts an inference scheduler.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment.html#LookoutEquipment.Client.start_inference_scheduler)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#start_inference_scheduler)
        """
    async def stop_inference_scheduler(
        self, *, InferenceSchedulerName: str
    ) -> StopInferenceSchedulerResponseTypeDef:
        """
        Stops an inference scheduler.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment.html#LookoutEquipment.Client.stop_inference_scheduler)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#stop_inference_scheduler)
        """
    async def tag_resource(
        self, *, ResourceArn: str, Tags: Sequence["TagTypeDef"]
    ) -> Dict[str, Any]:
        """
        Associates a given tag to a resource in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment.html#LookoutEquipment.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#tag_resource)
        """
    async def untag_resource(self, *, ResourceArn: str, TagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes a specific tag from a given resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment.html#LookoutEquipment.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#untag_resource)
        """
    async def update_inference_scheduler(
        self,
        *,
        InferenceSchedulerName: str,
        DataDelayOffsetInMinutes: int = ...,
        DataUploadFrequency: DataUploadFrequencyType = ...,
        DataInputConfiguration: "InferenceInputConfigurationTypeDef" = ...,
        DataOutputConfiguration: "InferenceOutputConfigurationTypeDef" = ...,
        RoleArn: str = ...
    ) -> None:
        """
        Updates an inference scheduler.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment.html#LookoutEquipment.Client.update_inference_scheduler)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/#update_inference_scheduler)
        """
    async def __aenter__(self) -> "LookoutEquipmentClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment.html#LookoutEquipment.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/)
        """
    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lookoutequipment.html#LookoutEquipment.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lookoutequipment/client/)
        """
