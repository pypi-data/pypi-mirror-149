"""
Type annotations for sts service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sts/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_sts.client import STSClient

    session = get_session()
    async with session.create_client("sts") as client:
        client: STSClient
    ```
"""
from typing import Any, Dict, Mapping, Sequence, Type

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .type_defs import (
    AssumeRoleResponseTypeDef,
    AssumeRoleWithSAMLResponseTypeDef,
    AssumeRoleWithWebIdentityResponseTypeDef,
    DecodeAuthorizationMessageResponseTypeDef,
    GetAccessKeyInfoResponseTypeDef,
    GetCallerIdentityResponseTypeDef,
    GetFederationTokenResponseTypeDef,
    GetSessionTokenResponseTypeDef,
    PolicyDescriptorTypeTypeDef,
    TagTypeDef,
)

__all__ = ("STSClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    ExpiredTokenException: Type[BotocoreClientError]
    IDPCommunicationErrorException: Type[BotocoreClientError]
    IDPRejectedClaimException: Type[BotocoreClientError]
    InvalidAuthorizationMessageException: Type[BotocoreClientError]
    InvalidIdentityTokenException: Type[BotocoreClientError]
    MalformedPolicyDocumentException: Type[BotocoreClientError]
    PackedPolicyTooLargeException: Type[BotocoreClientError]
    RegionDisabledException: Type[BotocoreClientError]


class STSClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sts.html#STS.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sts/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        STSClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sts.html#STS.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sts/client/#exceptions)
        """

    async def assume_role(
        self,
        *,
        RoleArn: str,
        RoleSessionName: str,
        PolicyArns: Sequence["PolicyDescriptorTypeTypeDef"] = ...,
        Policy: str = ...,
        DurationSeconds: int = ...,
        Tags: Sequence["TagTypeDef"] = ...,
        TransitiveTagKeys: Sequence[str] = ...,
        ExternalId: str = ...,
        SerialNumber: str = ...,
        TokenCode: str = ...,
        SourceIdentity: str = ...
    ) -> AssumeRoleResponseTypeDef:
        """
        Returns a set of temporary security credentials that you can use to access
        Amazon Web Services resources that you might not normally have access to.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sts.html#STS.Client.assume_role)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sts/client/#assume_role)
        """

    async def assume_role_with_saml(
        self,
        *,
        RoleArn: str,
        PrincipalArn: str,
        SAMLAssertion: str,
        PolicyArns: Sequence["PolicyDescriptorTypeTypeDef"] = ...,
        Policy: str = ...,
        DurationSeconds: int = ...
    ) -> AssumeRoleWithSAMLResponseTypeDef:
        """
        Returns a set of temporary security credentials for users who have been
        authenticated via a SAML authentication response.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sts.html#STS.Client.assume_role_with_saml)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sts/client/#assume_role_with_saml)
        """

    async def assume_role_with_web_identity(
        self,
        *,
        RoleArn: str,
        RoleSessionName: str,
        WebIdentityToken: str,
        ProviderId: str = ...,
        PolicyArns: Sequence["PolicyDescriptorTypeTypeDef"] = ...,
        Policy: str = ...,
        DurationSeconds: int = ...
    ) -> AssumeRoleWithWebIdentityResponseTypeDef:
        """
        Returns a set of temporary security credentials for users who have been
        authenticated in a mobile or web application with a web identity provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sts.html#STS.Client.assume_role_with_web_identity)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sts/client/#assume_role_with_web_identity)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sts.html#STS.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sts/client/#can_paginate)
        """

    async def decode_authorization_message(
        self, *, EncodedMessage: str
    ) -> DecodeAuthorizationMessageResponseTypeDef:
        """
        Decodes additional information about the authorization status of a request from
        an encoded message returned in response to an Amazon Web Services request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sts.html#STS.Client.decode_authorization_message)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sts/client/#decode_authorization_message)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sts.html#STS.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sts/client/#generate_presigned_url)
        """

    async def get_access_key_info(self, *, AccessKeyId: str) -> GetAccessKeyInfoResponseTypeDef:
        """
        Returns the account identifier for the specified access key ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sts.html#STS.Client.get_access_key_info)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sts/client/#get_access_key_info)
        """

    async def get_caller_identity(self) -> GetCallerIdentityResponseTypeDef:
        """
        Returns details about the IAM user or role whose credentials are used to call
        the operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sts.html#STS.Client.get_caller_identity)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sts/client/#get_caller_identity)
        """

    async def get_federation_token(
        self,
        *,
        Name: str,
        Policy: str = ...,
        PolicyArns: Sequence["PolicyDescriptorTypeTypeDef"] = ...,
        DurationSeconds: int = ...,
        Tags: Sequence["TagTypeDef"] = ...
    ) -> GetFederationTokenResponseTypeDef:
        """
        Returns a set of temporary security credentials (consisting of an access key ID,
        a secret access key, and a security token) for a federated user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sts.html#STS.Client.get_federation_token)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sts/client/#get_federation_token)
        """

    async def get_session_token(
        self, *, DurationSeconds: int = ..., SerialNumber: str = ..., TokenCode: str = ...
    ) -> GetSessionTokenResponseTypeDef:
        """
        Returns a set of temporary credentials for an Amazon Web Services account or IAM
        user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sts.html#STS.Client.get_session_token)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sts/client/#get_session_token)
        """

    async def __aenter__(self) -> "STSClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sts.html#STS.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sts/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sts.html#STS.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sts/client/)
        """
