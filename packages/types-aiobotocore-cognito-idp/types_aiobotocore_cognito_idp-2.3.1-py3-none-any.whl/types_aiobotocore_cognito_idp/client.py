"""
Type annotations for cognito-idp service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_cognito_idp.client import CognitoIdentityProviderClient

    session = get_session()
    async with session.create_client("cognito-idp") as client:
        client: CognitoIdentityProviderClient
    ```
"""
import sys
from typing import IO, Any, Dict, Mapping, Sequence, Type, Union, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.response import StreamingBody

from .literals import (
    AliasAttributeTypeType,
    AuthFlowTypeType,
    ChallengeNameTypeType,
    DeliveryMediumTypeType,
    DeviceRememberedStatusTypeType,
    ExplicitAuthFlowsTypeType,
    FeedbackValueTypeType,
    IdentityProviderTypeTypeType,
    MessageActionTypeType,
    OAuthFlowTypeType,
    PreventUserExistenceErrorTypesType,
    UsernameAttributeTypeType,
    UserPoolMfaTypeType,
    VerifiedAttributeTypeType,
)
from .paginator import (
    AdminListGroupsForUserPaginator,
    AdminListUserAuthEventsPaginator,
    ListGroupsPaginator,
    ListIdentityProvidersPaginator,
    ListResourceServersPaginator,
    ListUserPoolClientsPaginator,
    ListUserPoolsPaginator,
    ListUsersInGroupPaginator,
    ListUsersPaginator,
)
from .type_defs import (
    AccountRecoverySettingTypeTypeDef,
    AccountTakeoverRiskConfigurationTypeTypeDef,
    AdminCreateUserConfigTypeTypeDef,
    AdminCreateUserResponseTypeDef,
    AdminGetDeviceResponseTypeDef,
    AdminGetUserResponseTypeDef,
    AdminInitiateAuthResponseTypeDef,
    AdminListDevicesResponseTypeDef,
    AdminListGroupsForUserResponseTypeDef,
    AdminListUserAuthEventsResponseTypeDef,
    AdminRespondToAuthChallengeResponseTypeDef,
    AnalyticsConfigurationTypeTypeDef,
    AnalyticsMetadataTypeTypeDef,
    AssociateSoftwareTokenResponseTypeDef,
    AttributeTypeTypeDef,
    CompromisedCredentialsRiskConfigurationTypeTypeDef,
    ConfirmDeviceResponseTypeDef,
    ContextDataTypeTypeDef,
    CreateGroupResponseTypeDef,
    CreateIdentityProviderResponseTypeDef,
    CreateResourceServerResponseTypeDef,
    CreateUserImportJobResponseTypeDef,
    CreateUserPoolClientResponseTypeDef,
    CreateUserPoolDomainResponseTypeDef,
    CreateUserPoolResponseTypeDef,
    CustomDomainConfigTypeTypeDef,
    DescribeIdentityProviderResponseTypeDef,
    DescribeResourceServerResponseTypeDef,
    DescribeRiskConfigurationResponseTypeDef,
    DescribeUserImportJobResponseTypeDef,
    DescribeUserPoolClientResponseTypeDef,
    DescribeUserPoolDomainResponseTypeDef,
    DescribeUserPoolResponseTypeDef,
    DeviceConfigurationTypeTypeDef,
    DeviceSecretVerifierConfigTypeTypeDef,
    EmailConfigurationTypeTypeDef,
    ForgotPasswordResponseTypeDef,
    GetCSVHeaderResponseTypeDef,
    GetDeviceResponseTypeDef,
    GetGroupResponseTypeDef,
    GetIdentityProviderByIdentifierResponseTypeDef,
    GetSigningCertificateResponseTypeDef,
    GetUICustomizationResponseTypeDef,
    GetUserAttributeVerificationCodeResponseTypeDef,
    GetUserPoolMfaConfigResponseTypeDef,
    GetUserResponseTypeDef,
    InitiateAuthResponseTypeDef,
    LambdaConfigTypeTypeDef,
    ListDevicesResponseTypeDef,
    ListGroupsResponseTypeDef,
    ListIdentityProvidersResponseTypeDef,
    ListResourceServersResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListUserImportJobsResponseTypeDef,
    ListUserPoolClientsResponseTypeDef,
    ListUserPoolsResponseTypeDef,
    ListUsersInGroupResponseTypeDef,
    ListUsersResponseTypeDef,
    MFAOptionTypeTypeDef,
    ProviderUserIdentifierTypeTypeDef,
    ResendConfirmationCodeResponseTypeDef,
    ResourceServerScopeTypeTypeDef,
    RespondToAuthChallengeResponseTypeDef,
    RiskExceptionConfigurationTypeTypeDef,
    SchemaAttributeTypeTypeDef,
    SetRiskConfigurationResponseTypeDef,
    SetUICustomizationResponseTypeDef,
    SetUserPoolMfaConfigResponseTypeDef,
    SignUpResponseTypeDef,
    SmsConfigurationTypeTypeDef,
    SmsMfaConfigTypeTypeDef,
    SMSMfaSettingsTypeTypeDef,
    SoftwareTokenMfaConfigTypeTypeDef,
    SoftwareTokenMfaSettingsTypeTypeDef,
    StartUserImportJobResponseTypeDef,
    StopUserImportJobResponseTypeDef,
    TokenValidityUnitsTypeTypeDef,
    UpdateGroupResponseTypeDef,
    UpdateIdentityProviderResponseTypeDef,
    UpdateResourceServerResponseTypeDef,
    UpdateUserAttributesResponseTypeDef,
    UpdateUserPoolClientResponseTypeDef,
    UpdateUserPoolDomainResponseTypeDef,
    UserContextDataTypeTypeDef,
    UsernameConfigurationTypeTypeDef,
    UserPoolAddOnsTypeTypeDef,
    UserPoolPolicyTypeTypeDef,
    VerificationMessageTemplateTypeTypeDef,
    VerifySoftwareTokenResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("CognitoIdentityProviderClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AliasExistsException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    CodeDeliveryFailureException: Type[BotocoreClientError]
    CodeMismatchException: Type[BotocoreClientError]
    ConcurrentModificationException: Type[BotocoreClientError]
    DuplicateProviderException: Type[BotocoreClientError]
    EnableSoftwareTokenMFAException: Type[BotocoreClientError]
    ExpiredCodeException: Type[BotocoreClientError]
    GroupExistsException: Type[BotocoreClientError]
    InternalErrorException: Type[BotocoreClientError]
    InvalidEmailRoleAccessPolicyException: Type[BotocoreClientError]
    InvalidLambdaResponseException: Type[BotocoreClientError]
    InvalidOAuthFlowException: Type[BotocoreClientError]
    InvalidParameterException: Type[BotocoreClientError]
    InvalidPasswordException: Type[BotocoreClientError]
    InvalidSmsRoleAccessPolicyException: Type[BotocoreClientError]
    InvalidSmsRoleTrustRelationshipException: Type[BotocoreClientError]
    InvalidUserPoolConfigurationException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    MFAMethodNotFoundException: Type[BotocoreClientError]
    NotAuthorizedException: Type[BotocoreClientError]
    PasswordResetRequiredException: Type[BotocoreClientError]
    PreconditionNotMetException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ScopeDoesNotExistException: Type[BotocoreClientError]
    SoftwareTokenMFANotFoundException: Type[BotocoreClientError]
    TooManyFailedAttemptsException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]
    UnauthorizedException: Type[BotocoreClientError]
    UnexpectedLambdaException: Type[BotocoreClientError]
    UnsupportedIdentityProviderException: Type[BotocoreClientError]
    UnsupportedOperationException: Type[BotocoreClientError]
    UnsupportedTokenTypeException: Type[BotocoreClientError]
    UnsupportedUserStateException: Type[BotocoreClientError]
    UserImportInProgressException: Type[BotocoreClientError]
    UserLambdaValidationException: Type[BotocoreClientError]
    UserNotConfirmedException: Type[BotocoreClientError]
    UserNotFoundException: Type[BotocoreClientError]
    UserPoolAddOnNotEnabledException: Type[BotocoreClientError]
    UserPoolTaggingException: Type[BotocoreClientError]
    UsernameExistsException: Type[BotocoreClientError]


class CognitoIdentityProviderClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CognitoIdentityProviderClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#exceptions)
        """

    async def add_custom_attributes(
        self, *, UserPoolId: str, CustomAttributes: Sequence["SchemaAttributeTypeTypeDef"]
    ) -> Dict[str, Any]:
        """
        Adds additional user attributes to the user pool schema.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.add_custom_attributes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#add_custom_attributes)
        """

    async def admin_add_user_to_group(
        self, *, UserPoolId: str, Username: str, GroupName: str
    ) -> None:
        """
        Adds the specified user to the specified group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.admin_add_user_to_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#admin_add_user_to_group)
        """

    async def admin_confirm_sign_up(
        self, *, UserPoolId: str, Username: str, ClientMetadata: Mapping[str, str] = ...
    ) -> Dict[str, Any]:
        """
        Confirms user registration as an admin without using a confirmation code.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.admin_confirm_sign_up)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#admin_confirm_sign_up)
        """

    async def admin_create_user(
        self,
        *,
        UserPoolId: str,
        Username: str,
        UserAttributes: Sequence["AttributeTypeTypeDef"] = ...,
        ValidationData: Sequence["AttributeTypeTypeDef"] = ...,
        TemporaryPassword: str = ...,
        ForceAliasCreation: bool = ...,
        MessageAction: MessageActionTypeType = ...,
        DesiredDeliveryMediums: Sequence[DeliveryMediumTypeType] = ...,
        ClientMetadata: Mapping[str, str] = ...
    ) -> AdminCreateUserResponseTypeDef:
        """
        Creates a new user in the specified user pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.admin_create_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#admin_create_user)
        """

    async def admin_delete_user(self, *, UserPoolId: str, Username: str) -> None:
        """
        Deletes a user as an administrator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.admin_delete_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#admin_delete_user)
        """

    async def admin_delete_user_attributes(
        self, *, UserPoolId: str, Username: str, UserAttributeNames: Sequence[str]
    ) -> Dict[str, Any]:
        """
        Deletes the user attributes in a user pool as an administrator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.admin_delete_user_attributes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#admin_delete_user_attributes)
        """

    async def admin_disable_provider_for_user(
        self, *, UserPoolId: str, User: "ProviderUserIdentifierTypeTypeDef"
    ) -> Dict[str, Any]:
        """
        Prevents the user from signing in with the specified external (SAML or social)
        identity provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.admin_disable_provider_for_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#admin_disable_provider_for_user)
        """

    async def admin_disable_user(self, *, UserPoolId: str, Username: str) -> Dict[str, Any]:
        """
        Disables the specified user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.admin_disable_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#admin_disable_user)
        """

    async def admin_enable_user(self, *, UserPoolId: str, Username: str) -> Dict[str, Any]:
        """
        Enables the specified user as an administrator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.admin_enable_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#admin_enable_user)
        """

    async def admin_forget_device(self, *, UserPoolId: str, Username: str, DeviceKey: str) -> None:
        """
        Forgets the device, as an administrator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.admin_forget_device)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#admin_forget_device)
        """

    async def admin_get_device(
        self, *, DeviceKey: str, UserPoolId: str, Username: str
    ) -> AdminGetDeviceResponseTypeDef:
        """
        Gets the device, as an administrator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.admin_get_device)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#admin_get_device)
        """

    async def admin_get_user(
        self, *, UserPoolId: str, Username: str
    ) -> AdminGetUserResponseTypeDef:
        """
        Gets the specified user by user name in a user pool as an administrator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.admin_get_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#admin_get_user)
        """

    async def admin_initiate_auth(
        self,
        *,
        UserPoolId: str,
        ClientId: str,
        AuthFlow: AuthFlowTypeType,
        AuthParameters: Mapping[str, str] = ...,
        ClientMetadata: Mapping[str, str] = ...,
        AnalyticsMetadata: "AnalyticsMetadataTypeTypeDef" = ...,
        ContextData: "ContextDataTypeTypeDef" = ...
    ) -> AdminInitiateAuthResponseTypeDef:
        """
        Initiates the authentication flow, as an administrator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.admin_initiate_auth)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#admin_initiate_auth)
        """

    async def admin_link_provider_for_user(
        self,
        *,
        UserPoolId: str,
        DestinationUser: "ProviderUserIdentifierTypeTypeDef",
        SourceUser: "ProviderUserIdentifierTypeTypeDef"
    ) -> Dict[str, Any]:
        """
        Links an existing user account in a user pool (`DestinationUser` ) to an
        identity from an external identity provider (`SourceUser` ) based on a specified
        attribute name and value from the external identity provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.admin_link_provider_for_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#admin_link_provider_for_user)
        """

    async def admin_list_devices(
        self, *, UserPoolId: str, Username: str, Limit: int = ..., PaginationToken: str = ...
    ) -> AdminListDevicesResponseTypeDef:
        """
        Lists devices, as an administrator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.admin_list_devices)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#admin_list_devices)
        """

    async def admin_list_groups_for_user(
        self, *, Username: str, UserPoolId: str, Limit: int = ..., NextToken: str = ...
    ) -> AdminListGroupsForUserResponseTypeDef:
        """
        Lists the groups that the user belongs to.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.admin_list_groups_for_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#admin_list_groups_for_user)
        """

    async def admin_list_user_auth_events(
        self, *, UserPoolId: str, Username: str, MaxResults: int = ..., NextToken: str = ...
    ) -> AdminListUserAuthEventsResponseTypeDef:
        """
        A history of user activity and any risks detected as part of Amazon Cognito
        advanced security.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.admin_list_user_auth_events)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#admin_list_user_auth_events)
        """

    async def admin_remove_user_from_group(
        self, *, UserPoolId: str, Username: str, GroupName: str
    ) -> None:
        """
        Removes the specified user from the specified group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.admin_remove_user_from_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#admin_remove_user_from_group)
        """

    async def admin_reset_user_password(
        self, *, UserPoolId: str, Username: str, ClientMetadata: Mapping[str, str] = ...
    ) -> Dict[str, Any]:
        """
        Resets the specified user's password in a user pool as an administrator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.admin_reset_user_password)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#admin_reset_user_password)
        """

    async def admin_respond_to_auth_challenge(
        self,
        *,
        UserPoolId: str,
        ClientId: str,
        ChallengeName: ChallengeNameTypeType,
        ChallengeResponses: Mapping[str, str] = ...,
        Session: str = ...,
        AnalyticsMetadata: "AnalyticsMetadataTypeTypeDef" = ...,
        ContextData: "ContextDataTypeTypeDef" = ...,
        ClientMetadata: Mapping[str, str] = ...
    ) -> AdminRespondToAuthChallengeResponseTypeDef:
        """
        Responds to an authentication challenge, as an administrator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.admin_respond_to_auth_challenge)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#admin_respond_to_auth_challenge)
        """

    async def admin_set_user_mfa_preference(
        self,
        *,
        Username: str,
        UserPoolId: str,
        SMSMfaSettings: "SMSMfaSettingsTypeTypeDef" = ...,
        SoftwareTokenMfaSettings: "SoftwareTokenMfaSettingsTypeTypeDef" = ...
    ) -> Dict[str, Any]:
        """
        The user's multi-factor authentication (MFA) preference, including which MFA
        options are activated, and if any are preferred.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.admin_set_user_mfa_preference)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#admin_set_user_mfa_preference)
        """

    async def admin_set_user_password(
        self, *, UserPoolId: str, Username: str, Password: str, Permanent: bool = ...
    ) -> Dict[str, Any]:
        """
        Sets the specified user's password in a user pool as an administrator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.admin_set_user_password)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#admin_set_user_password)
        """

    async def admin_set_user_settings(
        self, *, UserPoolId: str, Username: str, MFAOptions: Sequence["MFAOptionTypeTypeDef"]
    ) -> Dict[str, Any]:
        """
        *This action is no longer supported.* You can use it to configure only SMS MFA.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.admin_set_user_settings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#admin_set_user_settings)
        """

    async def admin_update_auth_event_feedback(
        self, *, UserPoolId: str, Username: str, EventId: str, FeedbackValue: FeedbackValueTypeType
    ) -> Dict[str, Any]:
        """
        Provides feedback for an authentication event indicating if it was from a valid
        user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.admin_update_auth_event_feedback)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#admin_update_auth_event_feedback)
        """

    async def admin_update_device_status(
        self,
        *,
        UserPoolId: str,
        Username: str,
        DeviceKey: str,
        DeviceRememberedStatus: DeviceRememberedStatusTypeType = ...
    ) -> Dict[str, Any]:
        """
        Updates the device status as an administrator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.admin_update_device_status)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#admin_update_device_status)
        """

    async def admin_update_user_attributes(
        self,
        *,
        UserPoolId: str,
        Username: str,
        UserAttributes: Sequence["AttributeTypeTypeDef"],
        ClientMetadata: Mapping[str, str] = ...
    ) -> Dict[str, Any]:
        """
        Updates the specified user's attributes, including developer attributes, as an
        administrator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.admin_update_user_attributes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#admin_update_user_attributes)
        """

    async def admin_user_global_sign_out(self, *, UserPoolId: str, Username: str) -> Dict[str, Any]:
        """
        Signs out users from all devices, as an administrator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.admin_user_global_sign_out)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#admin_user_global_sign_out)
        """

    async def associate_software_token(
        self, *, AccessToken: str = ..., Session: str = ...
    ) -> AssociateSoftwareTokenResponseTypeDef:
        """
        Returns a unique generated shared secret key code for the user account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.associate_software_token)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#associate_software_token)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#can_paginate)
        """

    async def change_password(
        self, *, PreviousPassword: str, ProposedPassword: str, AccessToken: str
    ) -> Dict[str, Any]:
        """
        Changes the password for a specified user in a user pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.change_password)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#change_password)
        """

    async def confirm_device(
        self,
        *,
        AccessToken: str,
        DeviceKey: str,
        DeviceSecretVerifierConfig: "DeviceSecretVerifierConfigTypeTypeDef" = ...,
        DeviceName: str = ...
    ) -> ConfirmDeviceResponseTypeDef:
        """
        Confirms tracking of the device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.confirm_device)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#confirm_device)
        """

    async def confirm_forgot_password(
        self,
        *,
        ClientId: str,
        Username: str,
        ConfirmationCode: str,
        Password: str,
        SecretHash: str = ...,
        AnalyticsMetadata: "AnalyticsMetadataTypeTypeDef" = ...,
        UserContextData: "UserContextDataTypeTypeDef" = ...,
        ClientMetadata: Mapping[str, str] = ...
    ) -> Dict[str, Any]:
        """
        Allows a user to enter a confirmation code to reset a forgotten password.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.confirm_forgot_password)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#confirm_forgot_password)
        """

    async def confirm_sign_up(
        self,
        *,
        ClientId: str,
        Username: str,
        ConfirmationCode: str,
        SecretHash: str = ...,
        ForceAliasCreation: bool = ...,
        AnalyticsMetadata: "AnalyticsMetadataTypeTypeDef" = ...,
        UserContextData: "UserContextDataTypeTypeDef" = ...,
        ClientMetadata: Mapping[str, str] = ...
    ) -> Dict[str, Any]:
        """
        Confirms registration of a user and handles the existing alias from a previous
        user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.confirm_sign_up)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#confirm_sign_up)
        """

    async def create_group(
        self,
        *,
        GroupName: str,
        UserPoolId: str,
        Description: str = ...,
        RoleArn: str = ...,
        Precedence: int = ...
    ) -> CreateGroupResponseTypeDef:
        """
        Creates a new group in the specified user pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.create_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#create_group)
        """

    async def create_identity_provider(
        self,
        *,
        UserPoolId: str,
        ProviderName: str,
        ProviderType: IdentityProviderTypeTypeType,
        ProviderDetails: Mapping[str, str],
        AttributeMapping: Mapping[str, str] = ...,
        IdpIdentifiers: Sequence[str] = ...
    ) -> CreateIdentityProviderResponseTypeDef:
        """
        Creates an identity provider for a user pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.create_identity_provider)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#create_identity_provider)
        """

    async def create_resource_server(
        self,
        *,
        UserPoolId: str,
        Identifier: str,
        Name: str,
        Scopes: Sequence["ResourceServerScopeTypeTypeDef"] = ...
    ) -> CreateResourceServerResponseTypeDef:
        """
        Creates a new OAuth2.0 resource server and defines custom scopes within it.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.create_resource_server)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#create_resource_server)
        """

    async def create_user_import_job(
        self, *, JobName: str, UserPoolId: str, CloudWatchLogsRoleArn: str
    ) -> CreateUserImportJobResponseTypeDef:
        """
        Creates the user import job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.create_user_import_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#create_user_import_job)
        """

    async def create_user_pool(
        self,
        *,
        PoolName: str,
        Policies: "UserPoolPolicyTypeTypeDef" = ...,
        LambdaConfig: "LambdaConfigTypeTypeDef" = ...,
        AutoVerifiedAttributes: Sequence[VerifiedAttributeTypeType] = ...,
        AliasAttributes: Sequence[AliasAttributeTypeType] = ...,
        UsernameAttributes: Sequence[UsernameAttributeTypeType] = ...,
        SmsVerificationMessage: str = ...,
        EmailVerificationMessage: str = ...,
        EmailVerificationSubject: str = ...,
        VerificationMessageTemplate: "VerificationMessageTemplateTypeTypeDef" = ...,
        SmsAuthenticationMessage: str = ...,
        MfaConfiguration: UserPoolMfaTypeType = ...,
        DeviceConfiguration: "DeviceConfigurationTypeTypeDef" = ...,
        EmailConfiguration: "EmailConfigurationTypeTypeDef" = ...,
        SmsConfiguration: "SmsConfigurationTypeTypeDef" = ...,
        UserPoolTags: Mapping[str, str] = ...,
        AdminCreateUserConfig: "AdminCreateUserConfigTypeTypeDef" = ...,
        Schema: Sequence["SchemaAttributeTypeTypeDef"] = ...,
        UserPoolAddOns: "UserPoolAddOnsTypeTypeDef" = ...,
        UsernameConfiguration: "UsernameConfigurationTypeTypeDef" = ...,
        AccountRecoverySetting: "AccountRecoverySettingTypeTypeDef" = ...
    ) -> CreateUserPoolResponseTypeDef:
        """
        Creates a new Amazon Cognito user pool and sets the password policy for the
        pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.create_user_pool)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#create_user_pool)
        """

    async def create_user_pool_client(
        self,
        *,
        UserPoolId: str,
        ClientName: str,
        GenerateSecret: bool = ...,
        RefreshTokenValidity: int = ...,
        AccessTokenValidity: int = ...,
        IdTokenValidity: int = ...,
        TokenValidityUnits: "TokenValidityUnitsTypeTypeDef" = ...,
        ReadAttributes: Sequence[str] = ...,
        WriteAttributes: Sequence[str] = ...,
        ExplicitAuthFlows: Sequence[ExplicitAuthFlowsTypeType] = ...,
        SupportedIdentityProviders: Sequence[str] = ...,
        CallbackURLs: Sequence[str] = ...,
        LogoutURLs: Sequence[str] = ...,
        DefaultRedirectURI: str = ...,
        AllowedOAuthFlows: Sequence[OAuthFlowTypeType] = ...,
        AllowedOAuthScopes: Sequence[str] = ...,
        AllowedOAuthFlowsUserPoolClient: bool = ...,
        AnalyticsConfiguration: "AnalyticsConfigurationTypeTypeDef" = ...,
        PreventUserExistenceErrors: PreventUserExistenceErrorTypesType = ...,
        EnableTokenRevocation: bool = ...
    ) -> CreateUserPoolClientResponseTypeDef:
        """
        Creates the user pool client.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.create_user_pool_client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#create_user_pool_client)
        """

    async def create_user_pool_domain(
        self,
        *,
        Domain: str,
        UserPoolId: str,
        CustomDomainConfig: "CustomDomainConfigTypeTypeDef" = ...
    ) -> CreateUserPoolDomainResponseTypeDef:
        """
        Creates a new domain for a user pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.create_user_pool_domain)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#create_user_pool_domain)
        """

    async def delete_group(self, *, GroupName: str, UserPoolId: str) -> None:
        """
        Deletes a group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.delete_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#delete_group)
        """

    async def delete_identity_provider(self, *, UserPoolId: str, ProviderName: str) -> None:
        """
        Deletes an identity provider for a user pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.delete_identity_provider)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#delete_identity_provider)
        """

    async def delete_resource_server(self, *, UserPoolId: str, Identifier: str) -> None:
        """
        Deletes a resource server.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.delete_resource_server)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#delete_resource_server)
        """

    async def delete_user(self, *, AccessToken: str) -> None:
        """
        Allows a user to delete himself or herself.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.delete_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#delete_user)
        """

    async def delete_user_attributes(
        self, *, UserAttributeNames: Sequence[str], AccessToken: str
    ) -> Dict[str, Any]:
        """
        Deletes the attributes for a user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.delete_user_attributes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#delete_user_attributes)
        """

    async def delete_user_pool(self, *, UserPoolId: str) -> None:
        """
        Deletes the specified Amazon Cognito user pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.delete_user_pool)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#delete_user_pool)
        """

    async def delete_user_pool_client(self, *, UserPoolId: str, ClientId: str) -> None:
        """
        Allows the developer to delete the user pool client.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.delete_user_pool_client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#delete_user_pool_client)
        """

    async def delete_user_pool_domain(self, *, Domain: str, UserPoolId: str) -> Dict[str, Any]:
        """
        Deletes a domain for a user pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.delete_user_pool_domain)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#delete_user_pool_domain)
        """

    async def describe_identity_provider(
        self, *, UserPoolId: str, ProviderName: str
    ) -> DescribeIdentityProviderResponseTypeDef:
        """
        Gets information about a specific identity provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.describe_identity_provider)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#describe_identity_provider)
        """

    async def describe_resource_server(
        self, *, UserPoolId: str, Identifier: str
    ) -> DescribeResourceServerResponseTypeDef:
        """
        Describes a resource server.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.describe_resource_server)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#describe_resource_server)
        """

    async def describe_risk_configuration(
        self, *, UserPoolId: str, ClientId: str = ...
    ) -> DescribeRiskConfigurationResponseTypeDef:
        """
        Describes the risk configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.describe_risk_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#describe_risk_configuration)
        """

    async def describe_user_import_job(
        self, *, UserPoolId: str, JobId: str
    ) -> DescribeUserImportJobResponseTypeDef:
        """
        Describes the user import job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.describe_user_import_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#describe_user_import_job)
        """

    async def describe_user_pool(self, *, UserPoolId: str) -> DescribeUserPoolResponseTypeDef:
        """
        Returns the configuration information and metadata of the specified user pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.describe_user_pool)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#describe_user_pool)
        """

    async def describe_user_pool_client(
        self, *, UserPoolId: str, ClientId: str
    ) -> DescribeUserPoolClientResponseTypeDef:
        """
        Client method for returning the configuration information and metadata of the
        specified user pool app client.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.describe_user_pool_client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#describe_user_pool_client)
        """

    async def describe_user_pool_domain(
        self, *, Domain: str
    ) -> DescribeUserPoolDomainResponseTypeDef:
        """
        Gets information about a domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.describe_user_pool_domain)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#describe_user_pool_domain)
        """

    async def forget_device(self, *, DeviceKey: str, AccessToken: str = ...) -> None:
        """
        Forgets the specified device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.forget_device)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#forget_device)
        """

    async def forgot_password(
        self,
        *,
        ClientId: str,
        Username: str,
        SecretHash: str = ...,
        UserContextData: "UserContextDataTypeTypeDef" = ...,
        AnalyticsMetadata: "AnalyticsMetadataTypeTypeDef" = ...,
        ClientMetadata: Mapping[str, str] = ...
    ) -> ForgotPasswordResponseTypeDef:
        """
        Calling this API causes a message to be sent to the end user with a confirmation
        code that is required to change the user's password.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.forgot_password)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#forgot_password)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#generate_presigned_url)
        """

    async def get_csv_header(self, *, UserPoolId: str) -> GetCSVHeaderResponseTypeDef:
        """
        Gets the header information for the comma-separated value (CSV) file to be used
        as input for the user import job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.get_csv_header)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#get_csv_header)
        """

    async def get_device(
        self, *, DeviceKey: str, AccessToken: str = ...
    ) -> GetDeviceResponseTypeDef:
        """
        Gets the device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.get_device)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#get_device)
        """

    async def get_group(self, *, GroupName: str, UserPoolId: str) -> GetGroupResponseTypeDef:
        """
        Gets a group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.get_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#get_group)
        """

    async def get_identity_provider_by_identifier(
        self, *, UserPoolId: str, IdpIdentifier: str
    ) -> GetIdentityProviderByIdentifierResponseTypeDef:
        """
        Gets the specified identity provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.get_identity_provider_by_identifier)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#get_identity_provider_by_identifier)
        """

    async def get_signing_certificate(
        self, *, UserPoolId: str
    ) -> GetSigningCertificateResponseTypeDef:
        """
        This method takes a user pool ID, and returns the signing certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.get_signing_certificate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#get_signing_certificate)
        """

    async def get_ui_customization(
        self, *, UserPoolId: str, ClientId: str = ...
    ) -> GetUICustomizationResponseTypeDef:
        """
        Gets the user interface (UI) Customization information for a particular app
        client's app UI, if any such information exists for the client.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.get_ui_customization)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#get_ui_customization)
        """

    async def get_user(self, *, AccessToken: str) -> GetUserResponseTypeDef:
        """
        Gets the user attributes and metadata for a user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.get_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#get_user)
        """

    async def get_user_attribute_verification_code(
        self, *, AccessToken: str, AttributeName: str, ClientMetadata: Mapping[str, str] = ...
    ) -> GetUserAttributeVerificationCodeResponseTypeDef:
        """
        Gets the user attribute verification code for the specified attribute name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.get_user_attribute_verification_code)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#get_user_attribute_verification_code)
        """

    async def get_user_pool_mfa_config(
        self, *, UserPoolId: str
    ) -> GetUserPoolMfaConfigResponseTypeDef:
        """
        Gets the user pool multi-factor authentication (MFA) configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.get_user_pool_mfa_config)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#get_user_pool_mfa_config)
        """

    async def global_sign_out(self, *, AccessToken: str) -> Dict[str, Any]:
        """
        Signs out users from all devices.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.global_sign_out)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#global_sign_out)
        """

    async def initiate_auth(
        self,
        *,
        AuthFlow: AuthFlowTypeType,
        ClientId: str,
        AuthParameters: Mapping[str, str] = ...,
        ClientMetadata: Mapping[str, str] = ...,
        AnalyticsMetadata: "AnalyticsMetadataTypeTypeDef" = ...,
        UserContextData: "UserContextDataTypeTypeDef" = ...
    ) -> InitiateAuthResponseTypeDef:
        """
        Initiates the authentication flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.initiate_auth)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#initiate_auth)
        """

    async def list_devices(
        self, *, AccessToken: str, Limit: int = ..., PaginationToken: str = ...
    ) -> ListDevicesResponseTypeDef:
        """
        Lists the devices.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.list_devices)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#list_devices)
        """

    async def list_groups(
        self, *, UserPoolId: str, Limit: int = ..., NextToken: str = ...
    ) -> ListGroupsResponseTypeDef:
        """
        Lists the groups associated with a user pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.list_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#list_groups)
        """

    async def list_identity_providers(
        self, *, UserPoolId: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListIdentityProvidersResponseTypeDef:
        """
        Lists information about all identity providers for a user pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.list_identity_providers)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#list_identity_providers)
        """

    async def list_resource_servers(
        self, *, UserPoolId: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListResourceServersResponseTypeDef:
        """
        Lists the resource servers for a user pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.list_resource_servers)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#list_resource_servers)
        """

    async def list_tags_for_resource(
        self, *, ResourceArn: str
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags that are assigned to an Amazon Cognito user pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#list_tags_for_resource)
        """

    async def list_user_import_jobs(
        self, *, UserPoolId: str, MaxResults: int, PaginationToken: str = ...
    ) -> ListUserImportJobsResponseTypeDef:
        """
        Lists the user import jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.list_user_import_jobs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#list_user_import_jobs)
        """

    async def list_user_pool_clients(
        self, *, UserPoolId: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListUserPoolClientsResponseTypeDef:
        """
        Lists the clients that have been created for the specified user pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.list_user_pool_clients)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#list_user_pool_clients)
        """

    async def list_user_pools(
        self, *, MaxResults: int, NextToken: str = ...
    ) -> ListUserPoolsResponseTypeDef:
        """
        Lists the user pools associated with an Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.list_user_pools)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#list_user_pools)
        """

    async def list_users(
        self,
        *,
        UserPoolId: str,
        AttributesToGet: Sequence[str] = ...,
        Limit: int = ...,
        PaginationToken: str = ...,
        Filter: str = ...
    ) -> ListUsersResponseTypeDef:
        """
        Lists the users in the Amazon Cognito user pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.list_users)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#list_users)
        """

    async def list_users_in_group(
        self, *, UserPoolId: str, GroupName: str, Limit: int = ..., NextToken: str = ...
    ) -> ListUsersInGroupResponseTypeDef:
        """
        Lists the users in the specified group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.list_users_in_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#list_users_in_group)
        """

    async def resend_confirmation_code(
        self,
        *,
        ClientId: str,
        Username: str,
        SecretHash: str = ...,
        UserContextData: "UserContextDataTypeTypeDef" = ...,
        AnalyticsMetadata: "AnalyticsMetadataTypeTypeDef" = ...,
        ClientMetadata: Mapping[str, str] = ...
    ) -> ResendConfirmationCodeResponseTypeDef:
        """
        Resends the confirmation (for confirmation of registration) to a specific user
        in the user pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.resend_confirmation_code)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#resend_confirmation_code)
        """

    async def respond_to_auth_challenge(
        self,
        *,
        ClientId: str,
        ChallengeName: ChallengeNameTypeType,
        Session: str = ...,
        ChallengeResponses: Mapping[str, str] = ...,
        AnalyticsMetadata: "AnalyticsMetadataTypeTypeDef" = ...,
        UserContextData: "UserContextDataTypeTypeDef" = ...,
        ClientMetadata: Mapping[str, str] = ...
    ) -> RespondToAuthChallengeResponseTypeDef:
        """
        Responds to the authentication challenge.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.respond_to_auth_challenge)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#respond_to_auth_challenge)
        """

    async def revoke_token(
        self, *, Token: str, ClientId: str, ClientSecret: str = ...
    ) -> Dict[str, Any]:
        """
        Revokes all of the access tokens generated by the specified refresh token.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.revoke_token)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#revoke_token)
        """

    async def set_risk_configuration(
        self,
        *,
        UserPoolId: str,
        ClientId: str = ...,
        CompromisedCredentialsRiskConfiguration: "CompromisedCredentialsRiskConfigurationTypeTypeDef" = ...,
        AccountTakeoverRiskConfiguration: "AccountTakeoverRiskConfigurationTypeTypeDef" = ...,
        RiskExceptionConfiguration: "RiskExceptionConfigurationTypeTypeDef" = ...
    ) -> SetRiskConfigurationResponseTypeDef:
        """
        Configures actions on detected risks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.set_risk_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#set_risk_configuration)
        """

    async def set_ui_customization(
        self,
        *,
        UserPoolId: str,
        ClientId: str = ...,
        CSS: str = ...,
        ImageFile: Union[str, bytes, IO[Any], StreamingBody] = ...
    ) -> SetUICustomizationResponseTypeDef:
        """
        Sets the user interface (UI) customization information for a user pool's built-
        in app UI.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.set_ui_customization)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#set_ui_customization)
        """

    async def set_user_mfa_preference(
        self,
        *,
        AccessToken: str,
        SMSMfaSettings: "SMSMfaSettingsTypeTypeDef" = ...,
        SoftwareTokenMfaSettings: "SoftwareTokenMfaSettingsTypeTypeDef" = ...
    ) -> Dict[str, Any]:
        """
        Set the user's multi-factor authentication (MFA) method preference, including
        which MFA factors are activated and if any are preferred.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.set_user_mfa_preference)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#set_user_mfa_preference)
        """

    async def set_user_pool_mfa_config(
        self,
        *,
        UserPoolId: str,
        SmsMfaConfiguration: "SmsMfaConfigTypeTypeDef" = ...,
        SoftwareTokenMfaConfiguration: "SoftwareTokenMfaConfigTypeTypeDef" = ...,
        MfaConfiguration: UserPoolMfaTypeType = ...
    ) -> SetUserPoolMfaConfigResponseTypeDef:
        """
        Sets the user pool multi-factor authentication (MFA) configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.set_user_pool_mfa_config)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#set_user_pool_mfa_config)
        """

    async def set_user_settings(
        self, *, AccessToken: str, MFAOptions: Sequence["MFAOptionTypeTypeDef"]
    ) -> Dict[str, Any]:
        """
        *This action is no longer supported.* You can use it to configure only SMS MFA.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.set_user_settings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#set_user_settings)
        """

    async def sign_up(
        self,
        *,
        ClientId: str,
        Username: str,
        Password: str,
        SecretHash: str = ...,
        UserAttributes: Sequence["AttributeTypeTypeDef"] = ...,
        ValidationData: Sequence["AttributeTypeTypeDef"] = ...,
        AnalyticsMetadata: "AnalyticsMetadataTypeTypeDef" = ...,
        UserContextData: "UserContextDataTypeTypeDef" = ...,
        ClientMetadata: Mapping[str, str] = ...
    ) -> SignUpResponseTypeDef:
        """
        Registers the user in the specified user pool and creates a user name, password,
        and user attributes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.sign_up)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#sign_up)
        """

    async def start_user_import_job(
        self, *, UserPoolId: str, JobId: str
    ) -> StartUserImportJobResponseTypeDef:
        """
        Starts the user import.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.start_user_import_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#start_user_import_job)
        """

    async def stop_user_import_job(
        self, *, UserPoolId: str, JobId: str
    ) -> StopUserImportJobResponseTypeDef:
        """
        Stops the user import job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.stop_user_import_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#stop_user_import_job)
        """

    async def tag_resource(self, *, ResourceArn: str, Tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Assigns a set of tags to an Amazon Cognito user pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#tag_resource)
        """

    async def untag_resource(self, *, ResourceArn: str, TagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes the specified tags from an Amazon Cognito user pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#untag_resource)
        """

    async def update_auth_event_feedback(
        self,
        *,
        UserPoolId: str,
        Username: str,
        EventId: str,
        FeedbackToken: str,
        FeedbackValue: FeedbackValueTypeType
    ) -> Dict[str, Any]:
        """
        Provides the feedback for an authentication event, whether it was from a valid
        user or not.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.update_auth_event_feedback)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#update_auth_event_feedback)
        """

    async def update_device_status(
        self,
        *,
        AccessToken: str,
        DeviceKey: str,
        DeviceRememberedStatus: DeviceRememberedStatusTypeType = ...
    ) -> Dict[str, Any]:
        """
        Updates the device status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.update_device_status)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#update_device_status)
        """

    async def update_group(
        self,
        *,
        GroupName: str,
        UserPoolId: str,
        Description: str = ...,
        RoleArn: str = ...,
        Precedence: int = ...
    ) -> UpdateGroupResponseTypeDef:
        """
        Updates the specified group with the specified attributes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.update_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#update_group)
        """

    async def update_identity_provider(
        self,
        *,
        UserPoolId: str,
        ProviderName: str,
        ProviderDetails: Mapping[str, str] = ...,
        AttributeMapping: Mapping[str, str] = ...,
        IdpIdentifiers: Sequence[str] = ...
    ) -> UpdateIdentityProviderResponseTypeDef:
        """
        Updates identity provider information for a user pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.update_identity_provider)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#update_identity_provider)
        """

    async def update_resource_server(
        self,
        *,
        UserPoolId: str,
        Identifier: str,
        Name: str,
        Scopes: Sequence["ResourceServerScopeTypeTypeDef"] = ...
    ) -> UpdateResourceServerResponseTypeDef:
        """
        Updates the name and scopes of resource server.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.update_resource_server)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#update_resource_server)
        """

    async def update_user_attributes(
        self,
        *,
        UserAttributes: Sequence["AttributeTypeTypeDef"],
        AccessToken: str,
        ClientMetadata: Mapping[str, str] = ...
    ) -> UpdateUserAttributesResponseTypeDef:
        """
        Allows a user to update a specific attribute (one at a time).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.update_user_attributes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#update_user_attributes)
        """

    async def update_user_pool(
        self,
        *,
        UserPoolId: str,
        Policies: "UserPoolPolicyTypeTypeDef" = ...,
        LambdaConfig: "LambdaConfigTypeTypeDef" = ...,
        AutoVerifiedAttributes: Sequence[VerifiedAttributeTypeType] = ...,
        SmsVerificationMessage: str = ...,
        EmailVerificationMessage: str = ...,
        EmailVerificationSubject: str = ...,
        VerificationMessageTemplate: "VerificationMessageTemplateTypeTypeDef" = ...,
        SmsAuthenticationMessage: str = ...,
        MfaConfiguration: UserPoolMfaTypeType = ...,
        DeviceConfiguration: "DeviceConfigurationTypeTypeDef" = ...,
        EmailConfiguration: "EmailConfigurationTypeTypeDef" = ...,
        SmsConfiguration: "SmsConfigurationTypeTypeDef" = ...,
        UserPoolTags: Mapping[str, str] = ...,
        AdminCreateUserConfig: "AdminCreateUserConfigTypeTypeDef" = ...,
        UserPoolAddOns: "UserPoolAddOnsTypeTypeDef" = ...,
        AccountRecoverySetting: "AccountRecoverySettingTypeTypeDef" = ...
    ) -> Dict[str, Any]:
        """
        Updates the specified user pool with the specified attributes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.update_user_pool)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#update_user_pool)
        """

    async def update_user_pool_client(
        self,
        *,
        UserPoolId: str,
        ClientId: str,
        ClientName: str = ...,
        RefreshTokenValidity: int = ...,
        AccessTokenValidity: int = ...,
        IdTokenValidity: int = ...,
        TokenValidityUnits: "TokenValidityUnitsTypeTypeDef" = ...,
        ReadAttributes: Sequence[str] = ...,
        WriteAttributes: Sequence[str] = ...,
        ExplicitAuthFlows: Sequence[ExplicitAuthFlowsTypeType] = ...,
        SupportedIdentityProviders: Sequence[str] = ...,
        CallbackURLs: Sequence[str] = ...,
        LogoutURLs: Sequence[str] = ...,
        DefaultRedirectURI: str = ...,
        AllowedOAuthFlows: Sequence[OAuthFlowTypeType] = ...,
        AllowedOAuthScopes: Sequence[str] = ...,
        AllowedOAuthFlowsUserPoolClient: bool = ...,
        AnalyticsConfiguration: "AnalyticsConfigurationTypeTypeDef" = ...,
        PreventUserExistenceErrors: PreventUserExistenceErrorTypesType = ...,
        EnableTokenRevocation: bool = ...
    ) -> UpdateUserPoolClientResponseTypeDef:
        """
        Updates the specified user pool app client with the specified attributes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.update_user_pool_client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#update_user_pool_client)
        """

    async def update_user_pool_domain(
        self, *, Domain: str, UserPoolId: str, CustomDomainConfig: "CustomDomainConfigTypeTypeDef"
    ) -> UpdateUserPoolDomainResponseTypeDef:
        """
        Updates the Secure Sockets Layer (SSL) certificate for the custom domain for
        your user pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.update_user_pool_domain)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#update_user_pool_domain)
        """

    async def verify_software_token(
        self,
        *,
        UserCode: str,
        AccessToken: str = ...,
        Session: str = ...,
        FriendlyDeviceName: str = ...
    ) -> VerifySoftwareTokenResponseTypeDef:
        """
        Use this API to register a user's entered time-based one-time password (TOTP)
        code and mark the user's software token MFA status as "verified" if successful.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.verify_software_token)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#verify_software_token)
        """

    async def verify_user_attribute(
        self, *, AccessToken: str, AttributeName: str, Code: str
    ) -> Dict[str, Any]:
        """
        Verifies the specified user attributes in the user pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.verify_user_attribute)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#verify_user_attribute)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["admin_list_groups_for_user"]
    ) -> AdminListGroupsForUserPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["admin_list_user_auth_events"]
    ) -> AdminListUserAuthEventsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_groups"]) -> ListGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_identity_providers"]
    ) -> ListIdentityProvidersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_resource_servers"]
    ) -> ListResourceServersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_user_pool_clients"]
    ) -> ListUserPoolClientsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_user_pools"]) -> ListUserPoolsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_users"]) -> ListUsersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_users_in_group"]
    ) -> ListUsersInGroupPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/#get_paginator)
        """

    async def __aenter__(self) -> "CognitoIdentityProviderClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp.html#CognitoIdentityProvider.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_idp/client/)
        """
