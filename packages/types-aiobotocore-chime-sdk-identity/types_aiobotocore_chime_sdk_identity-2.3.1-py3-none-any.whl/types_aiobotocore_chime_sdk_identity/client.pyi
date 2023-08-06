"""
Type annotations for chime-sdk-identity service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_identity/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_chime_sdk_identity.client import ChimeSDKIdentityClient

    session = get_session()
    async with session.create_client("chime-sdk-identity") as client:
        client: ChimeSDKIdentityClient
    ```
"""
from typing import Any, Dict, Mapping, Sequence, Type

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import AllowMessagesType, AppInstanceUserEndpointTypeType
from .type_defs import (
    AppInstanceRetentionSettingsTypeDef,
    CreateAppInstanceAdminResponseTypeDef,
    CreateAppInstanceResponseTypeDef,
    CreateAppInstanceUserResponseTypeDef,
    DescribeAppInstanceAdminResponseTypeDef,
    DescribeAppInstanceResponseTypeDef,
    DescribeAppInstanceUserEndpointResponseTypeDef,
    DescribeAppInstanceUserResponseTypeDef,
    EndpointAttributesTypeDef,
    GetAppInstanceRetentionSettingsResponseTypeDef,
    ListAppInstanceAdminsResponseTypeDef,
    ListAppInstancesResponseTypeDef,
    ListAppInstanceUserEndpointsResponseTypeDef,
    ListAppInstanceUsersResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    PutAppInstanceRetentionSettingsResponseTypeDef,
    RegisterAppInstanceUserEndpointResponseTypeDef,
    TagTypeDef,
    UpdateAppInstanceResponseTypeDef,
    UpdateAppInstanceUserEndpointResponseTypeDef,
    UpdateAppInstanceUserResponseTypeDef,
)

__all__ = ("ChimeSDKIdentityClient",)

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
    ResourceLimitExceededException: Type[BotocoreClientError]
    ServiceFailureException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    ThrottledClientException: Type[BotocoreClientError]
    UnauthorizedClientException: Type[BotocoreClientError]

class ChimeSDKIdentityClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-identity.html#ChimeSDKIdentity.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_identity/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ChimeSDKIdentityClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-identity.html#ChimeSDKIdentity.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_identity/client/#exceptions)
        """
    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-identity.html#ChimeSDKIdentity.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_identity/client/#can_paginate)
        """
    async def create_app_instance(
        self,
        *,
        Name: str,
        ClientRequestToken: str,
        Metadata: str = ...,
        Tags: Sequence["TagTypeDef"] = ...
    ) -> CreateAppInstanceResponseTypeDef:
        """
        Creates an Amazon Chime SDK messaging `AppInstance` under an AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-identity.html#ChimeSDKIdentity.Client.create_app_instance)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_identity/client/#create_app_instance)
        """
    async def create_app_instance_admin(
        self, *, AppInstanceAdminArn: str, AppInstanceArn: str
    ) -> CreateAppInstanceAdminResponseTypeDef:
        """
        Promotes an `AppInstanceUser` to an `AppInstanceAdmin`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-identity.html#ChimeSDKIdentity.Client.create_app_instance_admin)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_identity/client/#create_app_instance_admin)
        """
    async def create_app_instance_user(
        self,
        *,
        AppInstanceArn: str,
        AppInstanceUserId: str,
        Name: str,
        ClientRequestToken: str,
        Metadata: str = ...,
        Tags: Sequence["TagTypeDef"] = ...
    ) -> CreateAppInstanceUserResponseTypeDef:
        """
        Creates a user under an Amazon Chime `AppInstance`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-identity.html#ChimeSDKIdentity.Client.create_app_instance_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_identity/client/#create_app_instance_user)
        """
    async def delete_app_instance(self, *, AppInstanceArn: str) -> None:
        """
        Deletes an `AppInstance` and all associated data asynchronously.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-identity.html#ChimeSDKIdentity.Client.delete_app_instance)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_identity/client/#delete_app_instance)
        """
    async def delete_app_instance_admin(
        self, *, AppInstanceAdminArn: str, AppInstanceArn: str
    ) -> None:
        """
        Demotes an `AppInstanceAdmin` to an `AppInstanceUser`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-identity.html#ChimeSDKIdentity.Client.delete_app_instance_admin)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_identity/client/#delete_app_instance_admin)
        """
    async def delete_app_instance_user(self, *, AppInstanceUserArn: str) -> None:
        """
        Deletes an `AppInstanceUser` .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-identity.html#ChimeSDKIdentity.Client.delete_app_instance_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_identity/client/#delete_app_instance_user)
        """
    async def deregister_app_instance_user_endpoint(
        self, *, AppInstanceUserArn: str, EndpointId: str
    ) -> None:
        """
        Deregisters an `AppInstanceUserEndpoint` .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-identity.html#ChimeSDKIdentity.Client.deregister_app_instance_user_endpoint)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_identity/client/#deregister_app_instance_user_endpoint)
        """
    async def describe_app_instance(
        self, *, AppInstanceArn: str
    ) -> DescribeAppInstanceResponseTypeDef:
        """
        Returns the full details of an `AppInstance` .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-identity.html#ChimeSDKIdentity.Client.describe_app_instance)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_identity/client/#describe_app_instance)
        """
    async def describe_app_instance_admin(
        self, *, AppInstanceAdminArn: str, AppInstanceArn: str
    ) -> DescribeAppInstanceAdminResponseTypeDef:
        """
        Returns the full details of an `AppInstanceAdmin` .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-identity.html#ChimeSDKIdentity.Client.describe_app_instance_admin)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_identity/client/#describe_app_instance_admin)
        """
    async def describe_app_instance_user(
        self, *, AppInstanceUserArn: str
    ) -> DescribeAppInstanceUserResponseTypeDef:
        """
        Returns the full details of an `AppInstanceUser` .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-identity.html#ChimeSDKIdentity.Client.describe_app_instance_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_identity/client/#describe_app_instance_user)
        """
    async def describe_app_instance_user_endpoint(
        self, *, AppInstanceUserArn: str, EndpointId: str
    ) -> DescribeAppInstanceUserEndpointResponseTypeDef:
        """
        Returns the full details of an `AppInstanceUserEndpoint` .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-identity.html#ChimeSDKIdentity.Client.describe_app_instance_user_endpoint)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_identity/client/#describe_app_instance_user_endpoint)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-identity.html#ChimeSDKIdentity.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_identity/client/#generate_presigned_url)
        """
    async def get_app_instance_retention_settings(
        self, *, AppInstanceArn: str
    ) -> GetAppInstanceRetentionSettingsResponseTypeDef:
        """
        Gets the retention settings for an `AppInstance` .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-identity.html#ChimeSDKIdentity.Client.get_app_instance_retention_settings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_identity/client/#get_app_instance_retention_settings)
        """
    async def list_app_instance_admins(
        self, *, AppInstanceArn: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListAppInstanceAdminsResponseTypeDef:
        """
        Returns a list of the administrators in the `AppInstance` .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-identity.html#ChimeSDKIdentity.Client.list_app_instance_admins)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_identity/client/#list_app_instance_admins)
        """
    async def list_app_instance_user_endpoints(
        self, *, AppInstanceUserArn: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListAppInstanceUserEndpointsResponseTypeDef:
        """
        Lists all the `AppInstanceUserEndpoints` created under a single
        `AppInstanceUser` .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-identity.html#ChimeSDKIdentity.Client.list_app_instance_user_endpoints)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_identity/client/#list_app_instance_user_endpoints)
        """
    async def list_app_instance_users(
        self, *, AppInstanceArn: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListAppInstanceUsersResponseTypeDef:
        """
        List all `AppInstanceUsers` created under a single `AppInstance` .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-identity.html#ChimeSDKIdentity.Client.list_app_instance_users)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_identity/client/#list_app_instance_users)
        """
    async def list_app_instances(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListAppInstancesResponseTypeDef:
        """
        Lists all Amazon Chime `AppInstance` s created under a single AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-identity.html#ChimeSDKIdentity.Client.list_app_instances)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_identity/client/#list_app_instances)
        """
    async def list_tags_for_resource(
        self, *, ResourceARN: str
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags applied to an Amazon Chime SDK identity resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-identity.html#ChimeSDKIdentity.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_identity/client/#list_tags_for_resource)
        """
    async def put_app_instance_retention_settings(
        self,
        *,
        AppInstanceArn: str,
        AppInstanceRetentionSettings: "AppInstanceRetentionSettingsTypeDef"
    ) -> PutAppInstanceRetentionSettingsResponseTypeDef:
        """
        Sets the amount of time in days that a given `AppInstance` retains data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-identity.html#ChimeSDKIdentity.Client.put_app_instance_retention_settings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_identity/client/#put_app_instance_retention_settings)
        """
    async def register_app_instance_user_endpoint(
        self,
        *,
        AppInstanceUserArn: str,
        Type: AppInstanceUserEndpointTypeType,
        ResourceArn: str,
        EndpointAttributes: "EndpointAttributesTypeDef",
        ClientRequestToken: str,
        Name: str = ...,
        AllowMessages: AllowMessagesType = ...
    ) -> RegisterAppInstanceUserEndpointResponseTypeDef:
        """
        Registers an endpoint under an Amazon Chime `AppInstanceUser`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-identity.html#ChimeSDKIdentity.Client.register_app_instance_user_endpoint)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_identity/client/#register_app_instance_user_endpoint)
        """
    async def tag_resource(self, *, ResourceARN: str, Tags: Sequence["TagTypeDef"]) -> None:
        """
        Applies the specified tags to the specified Amazon Chime SDK identity resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-identity.html#ChimeSDKIdentity.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_identity/client/#tag_resource)
        """
    async def untag_resource(self, *, ResourceARN: str, TagKeys: Sequence[str]) -> None:
        """
        Removes the specified tags from the specified Amazon Chime SDK identity
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-identity.html#ChimeSDKIdentity.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_identity/client/#untag_resource)
        """
    async def update_app_instance(
        self, *, AppInstanceArn: str, Name: str, Metadata: str
    ) -> UpdateAppInstanceResponseTypeDef:
        """
        Updates `AppInstance` metadata.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-identity.html#ChimeSDKIdentity.Client.update_app_instance)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_identity/client/#update_app_instance)
        """
    async def update_app_instance_user(
        self, *, AppInstanceUserArn: str, Name: str, Metadata: str
    ) -> UpdateAppInstanceUserResponseTypeDef:
        """
        Updates the details of an `AppInstanceUser`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-identity.html#ChimeSDKIdentity.Client.update_app_instance_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_identity/client/#update_app_instance_user)
        """
    async def update_app_instance_user_endpoint(
        self,
        *,
        AppInstanceUserArn: str,
        EndpointId: str,
        Name: str = ...,
        AllowMessages: AllowMessagesType = ...
    ) -> UpdateAppInstanceUserEndpointResponseTypeDef:
        """
        Updates the details of an `AppInstanceUserEndpoint`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-identity.html#ChimeSDKIdentity.Client.update_app_instance_user_endpoint)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_identity/client/#update_app_instance_user_endpoint)
        """
    async def __aenter__(self) -> "ChimeSDKIdentityClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-identity.html#ChimeSDKIdentity.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_identity/client/)
        """
    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-identity.html#ChimeSDKIdentity.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_identity/client/)
        """
