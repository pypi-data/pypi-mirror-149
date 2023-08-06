"""
Type annotations for cognito-sync service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_sync/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_cognito_sync.client import CognitoSyncClient

    session = get_session()
    async with session.create_client("cognito-sync") as client:
        client: CognitoSyncClient
    ```
"""
from typing import Any, Dict, Mapping, Sequence, Type

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import PlatformType
from .type_defs import (
    BulkPublishResponseTypeDef,
    CognitoStreamsTypeDef,
    DeleteDatasetResponseTypeDef,
    DescribeDatasetResponseTypeDef,
    DescribeIdentityPoolUsageResponseTypeDef,
    DescribeIdentityUsageResponseTypeDef,
    GetBulkPublishDetailsResponseTypeDef,
    GetCognitoEventsResponseTypeDef,
    GetIdentityPoolConfigurationResponseTypeDef,
    ListDatasetsResponseTypeDef,
    ListIdentityPoolUsageResponseTypeDef,
    ListRecordsResponseTypeDef,
    PushSyncTypeDef,
    RecordPatchTypeDef,
    RegisterDeviceResponseTypeDef,
    SetIdentityPoolConfigurationResponseTypeDef,
    UpdateRecordsResponseTypeDef,
)

__all__ = ("CognitoSyncClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AlreadyStreamedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConcurrentModificationException: Type[BotocoreClientError]
    DuplicateRequestException: Type[BotocoreClientError]
    InternalErrorException: Type[BotocoreClientError]
    InvalidConfigurationException: Type[BotocoreClientError]
    InvalidLambdaFunctionOutputException: Type[BotocoreClientError]
    InvalidParameterException: Type[BotocoreClientError]
    LambdaThrottledException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    NotAuthorizedException: Type[BotocoreClientError]
    ResourceConflictException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]


class CognitoSyncClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-sync.html#CognitoSync.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_sync/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CognitoSyncClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-sync.html#CognitoSync.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_sync/client/#exceptions)
        """

    async def bulk_publish(self, *, IdentityPoolId: str) -> BulkPublishResponseTypeDef:
        """
        Initiates a bulk publish of all existing datasets for an Identity Pool to the
        configured stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-sync.html#CognitoSync.Client.bulk_publish)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_sync/client/#bulk_publish)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-sync.html#CognitoSync.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_sync/client/#can_paginate)
        """

    async def delete_dataset(
        self, *, IdentityPoolId: str, IdentityId: str, DatasetName: str
    ) -> DeleteDatasetResponseTypeDef:
        """
        Deletes the specific dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-sync.html#CognitoSync.Client.delete_dataset)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_sync/client/#delete_dataset)
        """

    async def describe_dataset(
        self, *, IdentityPoolId: str, IdentityId: str, DatasetName: str
    ) -> DescribeDatasetResponseTypeDef:
        """
        Gets meta data about a dataset by identity and dataset name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-sync.html#CognitoSync.Client.describe_dataset)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_sync/client/#describe_dataset)
        """

    async def describe_identity_pool_usage(
        self, *, IdentityPoolId: str
    ) -> DescribeIdentityPoolUsageResponseTypeDef:
        """
        Gets usage details (for example, data storage) about a particular identity pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-sync.html#CognitoSync.Client.describe_identity_pool_usage)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_sync/client/#describe_identity_pool_usage)
        """

    async def describe_identity_usage(
        self, *, IdentityPoolId: str, IdentityId: str
    ) -> DescribeIdentityUsageResponseTypeDef:
        """
        Gets usage information for an identity, including number of datasets and data
        usage.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-sync.html#CognitoSync.Client.describe_identity_usage)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_sync/client/#describe_identity_usage)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-sync.html#CognitoSync.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_sync/client/#generate_presigned_url)
        """

    async def get_bulk_publish_details(
        self, *, IdentityPoolId: str
    ) -> GetBulkPublishDetailsResponseTypeDef:
        """
        Get the status of the last BulkPublish operation for an identity pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-sync.html#CognitoSync.Client.get_bulk_publish_details)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_sync/client/#get_bulk_publish_details)
        """

    async def get_cognito_events(self, *, IdentityPoolId: str) -> GetCognitoEventsResponseTypeDef:
        """
        Gets the events and the corresponding Lambda functions associated with an
        identity pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-sync.html#CognitoSync.Client.get_cognito_events)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_sync/client/#get_cognito_events)
        """

    async def get_identity_pool_configuration(
        self, *, IdentityPoolId: str
    ) -> GetIdentityPoolConfigurationResponseTypeDef:
        """
        Gets the configuration settings of an identity pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-sync.html#CognitoSync.Client.get_identity_pool_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_sync/client/#get_identity_pool_configuration)
        """

    async def list_datasets(
        self, *, IdentityPoolId: str, IdentityId: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListDatasetsResponseTypeDef:
        """
        Lists datasets for an identity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-sync.html#CognitoSync.Client.list_datasets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_sync/client/#list_datasets)
        """

    async def list_identity_pool_usage(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> ListIdentityPoolUsageResponseTypeDef:
        """
        Gets a list of identity pools registered with Cognito.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-sync.html#CognitoSync.Client.list_identity_pool_usage)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_sync/client/#list_identity_pool_usage)
        """

    async def list_records(
        self,
        *,
        IdentityPoolId: str,
        IdentityId: str,
        DatasetName: str,
        LastSyncCount: int = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
        SyncSessionToken: str = ...
    ) -> ListRecordsResponseTypeDef:
        """
        Gets paginated records, optionally changed after a particular sync count for a
        dataset and identity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-sync.html#CognitoSync.Client.list_records)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_sync/client/#list_records)
        """

    async def register_device(
        self, *, IdentityPoolId: str, IdentityId: str, Platform: PlatformType, Token: str
    ) -> RegisterDeviceResponseTypeDef:
        """
        Registers a device to receive push sync notifications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-sync.html#CognitoSync.Client.register_device)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_sync/client/#register_device)
        """

    async def set_cognito_events(self, *, IdentityPoolId: str, Events: Mapping[str, str]) -> None:
        """
        Sets the AWS Lambda function for a given event type for an identity pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-sync.html#CognitoSync.Client.set_cognito_events)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_sync/client/#set_cognito_events)
        """

    async def set_identity_pool_configuration(
        self,
        *,
        IdentityPoolId: str,
        PushSync: "PushSyncTypeDef" = ...,
        CognitoStreams: "CognitoStreamsTypeDef" = ...
    ) -> SetIdentityPoolConfigurationResponseTypeDef:
        """
        Sets the necessary configuration for push sync.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-sync.html#CognitoSync.Client.set_identity_pool_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_sync/client/#set_identity_pool_configuration)
        """

    async def subscribe_to_dataset(
        self, *, IdentityPoolId: str, IdentityId: str, DatasetName: str, DeviceId: str
    ) -> Dict[str, Any]:
        """
        Subscribes to receive notifications when a dataset is modified by another
        device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-sync.html#CognitoSync.Client.subscribe_to_dataset)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_sync/client/#subscribe_to_dataset)
        """

    async def unsubscribe_from_dataset(
        self, *, IdentityPoolId: str, IdentityId: str, DatasetName: str, DeviceId: str
    ) -> Dict[str, Any]:
        """
        Unsubscribes from receiving notifications when a dataset is modified by another
        device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-sync.html#CognitoSync.Client.unsubscribe_from_dataset)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_sync/client/#unsubscribe_from_dataset)
        """

    async def update_records(
        self,
        *,
        IdentityPoolId: str,
        IdentityId: str,
        DatasetName: str,
        SyncSessionToken: str,
        DeviceId: str = ...,
        RecordPatches: Sequence["RecordPatchTypeDef"] = ...,
        ClientContext: str = ...
    ) -> UpdateRecordsResponseTypeDef:
        """
        Posts updates to records and adds and deletes records for a dataset and user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-sync.html#CognitoSync.Client.update_records)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_sync/client/#update_records)
        """

    async def __aenter__(self) -> "CognitoSyncClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-sync.html#CognitoSync.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_sync/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-sync.html#CognitoSync.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_sync/client/)
        """
