"""
Type annotations for cognito-identity service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_identity/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_cognito_identity.client import CognitoIdentityClient

    session = get_session()
    async with session.create_client("cognito-identity") as client:
        client: CognitoIdentityClient
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import ListIdentityPoolsPaginator
from .type_defs import (
    CognitoIdentityProviderTypeDef,
    DeleteIdentitiesResponseTypeDef,
    GetCredentialsForIdentityResponseTypeDef,
    GetIdentityPoolRolesResponseTypeDef,
    GetIdResponseTypeDef,
    GetOpenIdTokenForDeveloperIdentityResponseTypeDef,
    GetOpenIdTokenResponseTypeDef,
    GetPrincipalTagAttributeMapResponseTypeDef,
    IdentityDescriptionResponseMetadataTypeDef,
    IdentityPoolTypeDef,
    ListIdentitiesResponseTypeDef,
    ListIdentityPoolsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    LookupDeveloperIdentityResponseTypeDef,
    MergeDeveloperIdentitiesResponseTypeDef,
    RoleMappingTypeDef,
    SetPrincipalTagAttributeMapResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("CognitoIdentityClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    ConcurrentModificationException: Type[BotocoreClientError]
    DeveloperUserAlreadyRegisteredException: Type[BotocoreClientError]
    ExternalServiceException: Type[BotocoreClientError]
    InternalErrorException: Type[BotocoreClientError]
    InvalidIdentityPoolConfigurationException: Type[BotocoreClientError]
    InvalidParameterException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    NotAuthorizedException: Type[BotocoreClientError]
    ResourceConflictException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]


class CognitoIdentityClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-identity.html#CognitoIdentity.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_identity/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CognitoIdentityClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-identity.html#CognitoIdentity.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_identity/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-identity.html#CognitoIdentity.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_identity/client/#can_paginate)
        """

    async def create_identity_pool(
        self,
        *,
        IdentityPoolName: str,
        AllowUnauthenticatedIdentities: bool,
        AllowClassicFlow: bool = ...,
        SupportedLoginProviders: Mapping[str, str] = ...,
        DeveloperProviderName: str = ...,
        OpenIdConnectProviderARNs: Sequence[str] = ...,
        CognitoIdentityProviders: Sequence["CognitoIdentityProviderTypeDef"] = ...,
        SamlProviderARNs: Sequence[str] = ...,
        IdentityPoolTags: Mapping[str, str] = ...
    ) -> IdentityPoolTypeDef:
        """
        Creates a new identity pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-identity.html#CognitoIdentity.Client.create_identity_pool)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_identity/client/#create_identity_pool)
        """

    async def delete_identities(
        self, *, IdentityIdsToDelete: Sequence[str]
    ) -> DeleteIdentitiesResponseTypeDef:
        """
        Deletes identities from an identity pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-identity.html#CognitoIdentity.Client.delete_identities)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_identity/client/#delete_identities)
        """

    async def delete_identity_pool(self, *, IdentityPoolId: str) -> None:
        """
        Deletes an identity pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-identity.html#CognitoIdentity.Client.delete_identity_pool)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_identity/client/#delete_identity_pool)
        """

    async def describe_identity(
        self, *, IdentityId: str
    ) -> IdentityDescriptionResponseMetadataTypeDef:
        """
        Returns metadata related to the given identity, including when the identity was
        created and any associated linked logins.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-identity.html#CognitoIdentity.Client.describe_identity)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_identity/client/#describe_identity)
        """

    async def describe_identity_pool(self, *, IdentityPoolId: str) -> IdentityPoolTypeDef:
        """
        Gets details about a particular identity pool, including the pool name, ID
        description, creation date, and current number of users.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-identity.html#CognitoIdentity.Client.describe_identity_pool)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_identity/client/#describe_identity_pool)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-identity.html#CognitoIdentity.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_identity/client/#generate_presigned_url)
        """

    async def get_credentials_for_identity(
        self, *, IdentityId: str, Logins: Mapping[str, str] = ..., CustomRoleArn: str = ...
    ) -> GetCredentialsForIdentityResponseTypeDef:
        """
        Returns credentials for the provided identity ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-identity.html#CognitoIdentity.Client.get_credentials_for_identity)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_identity/client/#get_credentials_for_identity)
        """

    async def get_id(
        self, *, IdentityPoolId: str, AccountId: str = ..., Logins: Mapping[str, str] = ...
    ) -> GetIdResponseTypeDef:
        """
        Generates (or retrieves) a Cognito ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-identity.html#CognitoIdentity.Client.get_id)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_identity/client/#get_id)
        """

    async def get_identity_pool_roles(
        self, *, IdentityPoolId: str
    ) -> GetIdentityPoolRolesResponseTypeDef:
        """
        Gets the roles for an identity pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-identity.html#CognitoIdentity.Client.get_identity_pool_roles)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_identity/client/#get_identity_pool_roles)
        """

    async def get_open_id_token(
        self, *, IdentityId: str, Logins: Mapping[str, str] = ...
    ) -> GetOpenIdTokenResponseTypeDef:
        """
        Gets an OpenID token, using a known Cognito ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-identity.html#CognitoIdentity.Client.get_open_id_token)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_identity/client/#get_open_id_token)
        """

    async def get_open_id_token_for_developer_identity(
        self,
        *,
        IdentityPoolId: str,
        Logins: Mapping[str, str],
        IdentityId: str = ...,
        PrincipalTags: Mapping[str, str] = ...,
        TokenDuration: int = ...
    ) -> GetOpenIdTokenForDeveloperIdentityResponseTypeDef:
        """
        Registers (or retrieves) a Cognito `IdentityId` and an OpenID Connect token for
        a user authenticated by your backend authentication process.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-identity.html#CognitoIdentity.Client.get_open_id_token_for_developer_identity)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_identity/client/#get_open_id_token_for_developer_identity)
        """

    async def get_principal_tag_attribute_map(
        self, *, IdentityPoolId: str, IdentityProviderName: str
    ) -> GetPrincipalTagAttributeMapResponseTypeDef:
        """
        Use `GetPrincipalTagAttributeMap` to list all mappings between `PrincipalTags`
        and user attributes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-identity.html#CognitoIdentity.Client.get_principal_tag_attribute_map)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_identity/client/#get_principal_tag_attribute_map)
        """

    async def list_identities(
        self,
        *,
        IdentityPoolId: str,
        MaxResults: int,
        NextToken: str = ...,
        HideDisabled: bool = ...
    ) -> ListIdentitiesResponseTypeDef:
        """
        Lists the identities in an identity pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-identity.html#CognitoIdentity.Client.list_identities)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_identity/client/#list_identities)
        """

    async def list_identity_pools(
        self, *, MaxResults: int, NextToken: str = ...
    ) -> ListIdentityPoolsResponseTypeDef:
        """
        Lists all of the Cognito identity pools registered for your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-identity.html#CognitoIdentity.Client.list_identity_pools)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_identity/client/#list_identity_pools)
        """

    async def list_tags_for_resource(
        self, *, ResourceArn: str
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags that are assigned to an Amazon Cognito identity pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-identity.html#CognitoIdentity.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_identity/client/#list_tags_for_resource)
        """

    async def lookup_developer_identity(
        self,
        *,
        IdentityPoolId: str,
        IdentityId: str = ...,
        DeveloperUserIdentifier: str = ...,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> LookupDeveloperIdentityResponseTypeDef:
        """
        Retrieves the `IdentityID` associated with a `DeveloperUserIdentifier` or the
        list of `DeveloperUserIdentifier` values associated with an `IdentityId` for an
        existing identity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-identity.html#CognitoIdentity.Client.lookup_developer_identity)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_identity/client/#lookup_developer_identity)
        """

    async def merge_developer_identities(
        self,
        *,
        SourceUserIdentifier: str,
        DestinationUserIdentifier: str,
        DeveloperProviderName: str,
        IdentityPoolId: str
    ) -> MergeDeveloperIdentitiesResponseTypeDef:
        """
        Merges two users having different `IdentityId` s, existing in the same identity
        pool, and identified by the same developer provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-identity.html#CognitoIdentity.Client.merge_developer_identities)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_identity/client/#merge_developer_identities)
        """

    async def set_identity_pool_roles(
        self,
        *,
        IdentityPoolId: str,
        Roles: Mapping[str, str],
        RoleMappings: Mapping[str, "RoleMappingTypeDef"] = ...
    ) -> None:
        """
        Sets the roles for an identity pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-identity.html#CognitoIdentity.Client.set_identity_pool_roles)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_identity/client/#set_identity_pool_roles)
        """

    async def set_principal_tag_attribute_map(
        self,
        *,
        IdentityPoolId: str,
        IdentityProviderName: str,
        UseDefaults: bool = ...,
        PrincipalTags: Mapping[str, str] = ...
    ) -> SetPrincipalTagAttributeMapResponseTypeDef:
        """
        You can use this operation to use default (username and clientID) attribute or
        custom attribute mappings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-identity.html#CognitoIdentity.Client.set_principal_tag_attribute_map)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_identity/client/#set_principal_tag_attribute_map)
        """

    async def tag_resource(self, *, ResourceArn: str, Tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Assigns a set of tags to the specified Amazon Cognito identity pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-identity.html#CognitoIdentity.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_identity/client/#tag_resource)
        """

    async def unlink_developer_identity(
        self,
        *,
        IdentityId: str,
        IdentityPoolId: str,
        DeveloperProviderName: str,
        DeveloperUserIdentifier: str
    ) -> None:
        """
        Unlinks a `DeveloperUserIdentifier` from an existing identity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-identity.html#CognitoIdentity.Client.unlink_developer_identity)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_identity/client/#unlink_developer_identity)
        """

    async def unlink_identity(
        self, *, IdentityId: str, Logins: Mapping[str, str], LoginsToRemove: Sequence[str]
    ) -> None:
        """
        Unlinks a federated identity from an existing account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-identity.html#CognitoIdentity.Client.unlink_identity)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_identity/client/#unlink_identity)
        """

    async def untag_resource(self, *, ResourceArn: str, TagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes the specified tags from the specified Amazon Cognito identity pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-identity.html#CognitoIdentity.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_identity/client/#untag_resource)
        """

    async def update_identity_pool(
        self,
        *,
        IdentityPoolId: str,
        IdentityPoolName: str,
        AllowUnauthenticatedIdentities: bool,
        AllowClassicFlow: bool = ...,
        SupportedLoginProviders: Mapping[str, str] = ...,
        DeveloperProviderName: str = ...,
        OpenIdConnectProviderARNs: Sequence[str] = ...,
        CognitoIdentityProviders: Sequence["CognitoIdentityProviderTypeDef"] = ...,
        SamlProviderARNs: Sequence[str] = ...,
        IdentityPoolTags: Mapping[str, str] = ...
    ) -> IdentityPoolTypeDef:
        """
        Updates an identity pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-identity.html#CognitoIdentity.Client.update_identity_pool)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_identity/client/#update_identity_pool)
        """

    def get_paginator(
        self, operation_name: Literal["list_identity_pools"]
    ) -> ListIdentityPoolsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-identity.html#CognitoIdentity.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_identity/client/#get_paginator)
        """

    async def __aenter__(self) -> "CognitoIdentityClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-identity.html#CognitoIdentity.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_identity/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-identity.html#CognitoIdentity.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_identity/client/)
        """
