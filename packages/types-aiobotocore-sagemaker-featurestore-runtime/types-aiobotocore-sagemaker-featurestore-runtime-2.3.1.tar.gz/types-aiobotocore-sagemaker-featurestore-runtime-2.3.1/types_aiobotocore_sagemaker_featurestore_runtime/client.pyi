"""
Type annotations for sagemaker-featurestore-runtime service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_featurestore_runtime/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_sagemaker_featurestore_runtime.client import SageMakerFeatureStoreRuntimeClient

    session = get_session()
    async with session.create_client("sagemaker-featurestore-runtime") as client:
        client: SageMakerFeatureStoreRuntimeClient
    ```
"""
from typing import Any, Dict, Mapping, Sequence, Type

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .type_defs import (
    BatchGetRecordIdentifierTypeDef,
    BatchGetRecordResponseTypeDef,
    FeatureValueTypeDef,
    GetRecordResponseTypeDef,
)

__all__ = ("SageMakerFeatureStoreRuntimeClient",)

class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessForbidden: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    InternalFailure: Type[BotocoreClientError]
    ResourceNotFound: Type[BotocoreClientError]
    ServiceUnavailable: Type[BotocoreClientError]
    ValidationError: Type[BotocoreClientError]

class SageMakerFeatureStoreRuntimeClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-featurestore-runtime.html#SageMakerFeatureStoreRuntime.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_featurestore_runtime/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SageMakerFeatureStoreRuntimeClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-featurestore-runtime.html#SageMakerFeatureStoreRuntime.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_featurestore_runtime/client/#exceptions)
        """
    async def batch_get_record(
        self, *, Identifiers: Sequence["BatchGetRecordIdentifierTypeDef"]
    ) -> BatchGetRecordResponseTypeDef:
        """
        Retrieves a batch of `Records` from a `FeatureGroup` .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-featurestore-runtime.html#SageMakerFeatureStoreRuntime.Client.batch_get_record)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_featurestore_runtime/client/#batch_get_record)
        """
    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-featurestore-runtime.html#SageMakerFeatureStoreRuntime.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_featurestore_runtime/client/#can_paginate)
        """
    async def delete_record(
        self, *, FeatureGroupName: str, RecordIdentifierValueAsString: str, EventTime: str
    ) -> None:
        """
        Deletes a `Record` from a `FeatureGroup`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-featurestore-runtime.html#SageMakerFeatureStoreRuntime.Client.delete_record)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_featurestore_runtime/client/#delete_record)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-featurestore-runtime.html#SageMakerFeatureStoreRuntime.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_featurestore_runtime/client/#generate_presigned_url)
        """
    async def get_record(
        self,
        *,
        FeatureGroupName: str,
        RecordIdentifierValueAsString: str,
        FeatureNames: Sequence[str] = ...
    ) -> GetRecordResponseTypeDef:
        """
        Use for `OnlineStore` serving from a `FeatureStore`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-featurestore-runtime.html#SageMakerFeatureStoreRuntime.Client.get_record)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_featurestore_runtime/client/#get_record)
        """
    async def put_record(
        self, *, FeatureGroupName: str, Record: Sequence["FeatureValueTypeDef"]
    ) -> None:
        """
        Used for data ingestion into the `FeatureStore`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-featurestore-runtime.html#SageMakerFeatureStoreRuntime.Client.put_record)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_featurestore_runtime/client/#put_record)
        """
    async def __aenter__(self) -> "SageMakerFeatureStoreRuntimeClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-featurestore-runtime.html#SageMakerFeatureStoreRuntime.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_featurestore_runtime/client/)
        """
    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-featurestore-runtime.html#SageMakerFeatureStoreRuntime.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_featurestore_runtime/client/)
        """
