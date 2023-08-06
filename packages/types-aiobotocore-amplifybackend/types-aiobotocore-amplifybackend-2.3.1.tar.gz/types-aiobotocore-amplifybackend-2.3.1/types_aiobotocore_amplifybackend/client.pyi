"""
Type annotations for amplifybackend service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_amplifybackend.client import AmplifyBackendClient

    session = get_session()
    async with session.create_client("amplifybackend") as client:
        client: AmplifyBackendClient
    ```
"""
import sys
from typing import Any, Dict, Mapping, Type

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import ListBackendJobsPaginator
from .type_defs import (
    BackendAPIResourceConfigTypeDef,
    CloneBackendResponseTypeDef,
    CreateBackendAPIResponseTypeDef,
    CreateBackendAuthResourceConfigTypeDef,
    CreateBackendAuthResponseTypeDef,
    CreateBackendConfigResponseTypeDef,
    CreateBackendResponseTypeDef,
    CreateBackendStorageResourceConfigTypeDef,
    CreateBackendStorageResponseTypeDef,
    CreateTokenResponseTypeDef,
    DeleteBackendAPIResponseTypeDef,
    DeleteBackendAuthResponseTypeDef,
    DeleteBackendResponseTypeDef,
    DeleteBackendStorageResponseTypeDef,
    DeleteTokenResponseTypeDef,
    GenerateBackendAPIModelsResponseTypeDef,
    GetBackendAPIModelsResponseTypeDef,
    GetBackendAPIResponseTypeDef,
    GetBackendAuthResponseTypeDef,
    GetBackendJobResponseTypeDef,
    GetBackendResponseTypeDef,
    GetBackendStorageResponseTypeDef,
    GetTokenResponseTypeDef,
    ImportBackendAuthResponseTypeDef,
    ImportBackendStorageResponseTypeDef,
    ListBackendJobsResponseTypeDef,
    ListS3BucketsResponseTypeDef,
    LoginAuthConfigReqObjTypeDef,
    RemoveAllBackendsResponseTypeDef,
    RemoveBackendConfigResponseTypeDef,
    UpdateBackendAPIResponseTypeDef,
    UpdateBackendAuthResourceConfigTypeDef,
    UpdateBackendAuthResponseTypeDef,
    UpdateBackendConfigResponseTypeDef,
    UpdateBackendJobResponseTypeDef,
    UpdateBackendStorageResourceConfigTypeDef,
    UpdateBackendStorageResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("AmplifyBackendClient",)

class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    GatewayTimeoutException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]

class AmplifyBackendClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend.html#AmplifyBackend.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        AmplifyBackendClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend.html#AmplifyBackend.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/#exceptions)
        """
    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend.html#AmplifyBackend.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/#can_paginate)
        """
    async def clone_backend(
        self, *, AppId: str, BackendEnvironmentName: str, TargetEnvironmentName: str
    ) -> CloneBackendResponseTypeDef:
        """
        This operation clones an existing backend.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend.html#AmplifyBackend.Client.clone_backend)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/#clone_backend)
        """
    async def create_backend(
        self,
        *,
        AppId: str,
        AppName: str,
        BackendEnvironmentName: str,
        ResourceConfig: Mapping[str, Any] = ...,
        ResourceName: str = ...
    ) -> CreateBackendResponseTypeDef:
        """
        This operation creates a backend for an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend.html#AmplifyBackend.Client.create_backend)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/#create_backend)
        """
    async def create_backend_api(
        self,
        *,
        AppId: str,
        BackendEnvironmentName: str,
        ResourceConfig: "BackendAPIResourceConfigTypeDef",
        ResourceName: str
    ) -> CreateBackendAPIResponseTypeDef:
        """
        Creates a new backend API resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend.html#AmplifyBackend.Client.create_backend_api)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/#create_backend_api)
        """
    async def create_backend_auth(
        self,
        *,
        AppId: str,
        BackendEnvironmentName: str,
        ResourceConfig: "CreateBackendAuthResourceConfigTypeDef",
        ResourceName: str
    ) -> CreateBackendAuthResponseTypeDef:
        """
        Creates a new backend authentication resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend.html#AmplifyBackend.Client.create_backend_auth)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/#create_backend_auth)
        """
    async def create_backend_config(
        self, *, AppId: str, BackendManagerAppId: str = ...
    ) -> CreateBackendConfigResponseTypeDef:
        """
        Creates a config object for a backend.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend.html#AmplifyBackend.Client.create_backend_config)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/#create_backend_config)
        """
    async def create_backend_storage(
        self,
        *,
        AppId: str,
        BackendEnvironmentName: str,
        ResourceConfig: "CreateBackendStorageResourceConfigTypeDef",
        ResourceName: str
    ) -> CreateBackendStorageResponseTypeDef:
        """
        Creates a backend storage resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend.html#AmplifyBackend.Client.create_backend_storage)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/#create_backend_storage)
        """
    async def create_token(self, *, AppId: str) -> CreateTokenResponseTypeDef:
        """
        Generates a one-time challenge code to authenticate a user into your Amplify
        Admin UI.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend.html#AmplifyBackend.Client.create_token)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/#create_token)
        """
    async def delete_backend(
        self, *, AppId: str, BackendEnvironmentName: str
    ) -> DeleteBackendResponseTypeDef:
        """
        Removes an existing environment from your Amplify project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend.html#AmplifyBackend.Client.delete_backend)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/#delete_backend)
        """
    async def delete_backend_api(
        self,
        *,
        AppId: str,
        BackendEnvironmentName: str,
        ResourceName: str,
        ResourceConfig: "BackendAPIResourceConfigTypeDef" = ...
    ) -> DeleteBackendAPIResponseTypeDef:
        """
        Deletes an existing backend API resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend.html#AmplifyBackend.Client.delete_backend_api)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/#delete_backend_api)
        """
    async def delete_backend_auth(
        self, *, AppId: str, BackendEnvironmentName: str, ResourceName: str
    ) -> DeleteBackendAuthResponseTypeDef:
        """
        Deletes an existing backend authentication resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend.html#AmplifyBackend.Client.delete_backend_auth)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/#delete_backend_auth)
        """
    async def delete_backend_storage(
        self,
        *,
        AppId: str,
        BackendEnvironmentName: str,
        ResourceName: str,
        ServiceName: Literal["S3"]
    ) -> DeleteBackendStorageResponseTypeDef:
        """
        Removes the specified backend storage resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend.html#AmplifyBackend.Client.delete_backend_storage)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/#delete_backend_storage)
        """
    async def delete_token(self, *, AppId: str, SessionId: str) -> DeleteTokenResponseTypeDef:
        """
        Deletes the challenge token based on the given appId and sessionId.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend.html#AmplifyBackend.Client.delete_token)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/#delete_token)
        """
    async def generate_backend_api_models(
        self, *, AppId: str, BackendEnvironmentName: str, ResourceName: str
    ) -> GenerateBackendAPIModelsResponseTypeDef:
        """
        Generates a model schema for an existing backend API resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend.html#AmplifyBackend.Client.generate_backend_api_models)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/#generate_backend_api_models)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend.html#AmplifyBackend.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/#generate_presigned_url)
        """
    async def get_backend(
        self, *, AppId: str, BackendEnvironmentName: str = ...
    ) -> GetBackendResponseTypeDef:
        """
        Provides project-level details for your Amplify UI project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend.html#AmplifyBackend.Client.get_backend)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/#get_backend)
        """
    async def get_backend_api(
        self,
        *,
        AppId: str,
        BackendEnvironmentName: str,
        ResourceName: str,
        ResourceConfig: "BackendAPIResourceConfigTypeDef" = ...
    ) -> GetBackendAPIResponseTypeDef:
        """
        Gets the details for a backend API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend.html#AmplifyBackend.Client.get_backend_api)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/#get_backend_api)
        """
    async def get_backend_api_models(
        self, *, AppId: str, BackendEnvironmentName: str, ResourceName: str
    ) -> GetBackendAPIModelsResponseTypeDef:
        """
        Generates a model schema for existing backend API resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend.html#AmplifyBackend.Client.get_backend_api_models)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/#get_backend_api_models)
        """
    async def get_backend_auth(
        self, *, AppId: str, BackendEnvironmentName: str, ResourceName: str
    ) -> GetBackendAuthResponseTypeDef:
        """
        Gets a backend auth details.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend.html#AmplifyBackend.Client.get_backend_auth)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/#get_backend_auth)
        """
    async def get_backend_job(
        self, *, AppId: str, BackendEnvironmentName: str, JobId: str
    ) -> GetBackendJobResponseTypeDef:
        """
        Returns information about a specific job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend.html#AmplifyBackend.Client.get_backend_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/#get_backend_job)
        """
    async def get_backend_storage(
        self, *, AppId: str, BackendEnvironmentName: str, ResourceName: str
    ) -> GetBackendStorageResponseTypeDef:
        """
        Gets details for a backend storage resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend.html#AmplifyBackend.Client.get_backend_storage)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/#get_backend_storage)
        """
    async def get_token(self, *, AppId: str, SessionId: str) -> GetTokenResponseTypeDef:
        """
        Gets the challenge token based on the given appId and sessionId.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend.html#AmplifyBackend.Client.get_token)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/#get_token)
        """
    async def import_backend_auth(
        self,
        *,
        AppId: str,
        BackendEnvironmentName: str,
        NativeClientId: str,
        UserPoolId: str,
        WebClientId: str,
        IdentityPoolId: str = ...
    ) -> ImportBackendAuthResponseTypeDef:
        """
        Imports an existing backend authentication resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend.html#AmplifyBackend.Client.import_backend_auth)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/#import_backend_auth)
        """
    async def import_backend_storage(
        self,
        *,
        AppId: str,
        BackendEnvironmentName: str,
        ServiceName: Literal["S3"],
        BucketName: str = ...
    ) -> ImportBackendStorageResponseTypeDef:
        """
        Imports an existing backend storage resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend.html#AmplifyBackend.Client.import_backend_storage)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/#import_backend_storage)
        """
    async def list_backend_jobs(
        self,
        *,
        AppId: str,
        BackendEnvironmentName: str,
        JobId: str = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
        Operation: str = ...,
        Status: str = ...
    ) -> ListBackendJobsResponseTypeDef:
        """
        Lists the jobs for the backend of an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend.html#AmplifyBackend.Client.list_backend_jobs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/#list_backend_jobs)
        """
    async def list_s3_buckets(self, *, NextToken: str = ...) -> ListS3BucketsResponseTypeDef:
        """
        The list of S3 buckets in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend.html#AmplifyBackend.Client.list_s3_buckets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/#list_s3_buckets)
        """
    async def remove_all_backends(
        self, *, AppId: str, CleanAmplifyApp: bool = ...
    ) -> RemoveAllBackendsResponseTypeDef:
        """
        Removes all backend environments from your Amplify project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend.html#AmplifyBackend.Client.remove_all_backends)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/#remove_all_backends)
        """
    async def remove_backend_config(self, *, AppId: str) -> RemoveBackendConfigResponseTypeDef:
        """
        Removes the AWS resources required to access the Amplify Admin UI.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend.html#AmplifyBackend.Client.remove_backend_config)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/#remove_backend_config)
        """
    async def update_backend_api(
        self,
        *,
        AppId: str,
        BackendEnvironmentName: str,
        ResourceName: str,
        ResourceConfig: "BackendAPIResourceConfigTypeDef" = ...
    ) -> UpdateBackendAPIResponseTypeDef:
        """
        Updates an existing backend API resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend.html#AmplifyBackend.Client.update_backend_api)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/#update_backend_api)
        """
    async def update_backend_auth(
        self,
        *,
        AppId: str,
        BackendEnvironmentName: str,
        ResourceConfig: "UpdateBackendAuthResourceConfigTypeDef",
        ResourceName: str
    ) -> UpdateBackendAuthResponseTypeDef:
        """
        Updates an existing backend authentication resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend.html#AmplifyBackend.Client.update_backend_auth)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/#update_backend_auth)
        """
    async def update_backend_config(
        self, *, AppId: str, LoginAuthConfig: "LoginAuthConfigReqObjTypeDef" = ...
    ) -> UpdateBackendConfigResponseTypeDef:
        """
        Updates the AWS resources required to access the Amplify Admin UI.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend.html#AmplifyBackend.Client.update_backend_config)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/#update_backend_config)
        """
    async def update_backend_job(
        self,
        *,
        AppId: str,
        BackendEnvironmentName: str,
        JobId: str,
        Operation: str = ...,
        Status: str = ...
    ) -> UpdateBackendJobResponseTypeDef:
        """
        Updates a specific job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend.html#AmplifyBackend.Client.update_backend_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/#update_backend_job)
        """
    async def update_backend_storage(
        self,
        *,
        AppId: str,
        BackendEnvironmentName: str,
        ResourceConfig: "UpdateBackendStorageResourceConfigTypeDef",
        ResourceName: str
    ) -> UpdateBackendStorageResponseTypeDef:
        """
        Updates an existing backend storage resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend.html#AmplifyBackend.Client.update_backend_storage)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/#update_backend_storage)
        """
    def get_paginator(
        self, operation_name: Literal["list_backend_jobs"]
    ) -> ListBackendJobsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend.html#AmplifyBackend.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/#get_paginator)
        """
    async def __aenter__(self) -> "AmplifyBackendClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend.html#AmplifyBackend.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/)
        """
    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend.html#AmplifyBackend.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/)
        """
