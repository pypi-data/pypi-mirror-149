"""
Type annotations for iam service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_iam.client import IAMClient

    session = get_session()
    async with session.create_client("iam") as client:
        client: IAMClient
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import (
    AccessAdvisorUsageGranularityTypeType,
    EntityTypeType,
    PolicyUsageTypeType,
    assignmentStatusTypeType,
    encodingTypeType,
    globalEndpointTokenVersionType,
    policyScopeTypeType,
    sortKeyTypeType,
    statusTypeType,
)
from .paginator import (
    GetAccountAuthorizationDetailsPaginator,
    GetGroupPaginator,
    ListAccessKeysPaginator,
    ListAccountAliasesPaginator,
    ListAttachedGroupPoliciesPaginator,
    ListAttachedRolePoliciesPaginator,
    ListAttachedUserPoliciesPaginator,
    ListEntitiesForPolicyPaginator,
    ListGroupPoliciesPaginator,
    ListGroupsForUserPaginator,
    ListGroupsPaginator,
    ListInstanceProfilesForRolePaginator,
    ListInstanceProfilesPaginator,
    ListMFADevicesPaginator,
    ListPoliciesPaginator,
    ListPolicyVersionsPaginator,
    ListRolePoliciesPaginator,
    ListRolesPaginator,
    ListServerCertificatesPaginator,
    ListSigningCertificatesPaginator,
    ListSSHPublicKeysPaginator,
    ListUserPoliciesPaginator,
    ListUsersPaginator,
    ListUserTagsPaginator,
    ListVirtualMFADevicesPaginator,
    SimulateCustomPolicyPaginator,
    SimulatePrincipalPolicyPaginator,
)
from .type_defs import (
    ContextEntryTypeDef,
    CreateAccessKeyResponseTypeDef,
    CreateGroupResponseTypeDef,
    CreateInstanceProfileResponseTypeDef,
    CreateLoginProfileResponseTypeDef,
    CreateOpenIDConnectProviderResponseTypeDef,
    CreatePolicyResponseTypeDef,
    CreatePolicyVersionResponseTypeDef,
    CreateRoleResponseTypeDef,
    CreateSAMLProviderResponseTypeDef,
    CreateServiceLinkedRoleResponseTypeDef,
    CreateServiceSpecificCredentialResponseTypeDef,
    CreateUserResponseTypeDef,
    CreateVirtualMFADeviceResponseTypeDef,
    DeleteServiceLinkedRoleResponseTypeDef,
    GenerateCredentialReportResponseTypeDef,
    GenerateOrganizationsAccessReportResponseTypeDef,
    GenerateServiceLastAccessedDetailsResponseTypeDef,
    GetAccessKeyLastUsedResponseTypeDef,
    GetAccountAuthorizationDetailsResponseTypeDef,
    GetAccountPasswordPolicyResponseTypeDef,
    GetAccountSummaryResponseTypeDef,
    GetContextKeysForPolicyResponseTypeDef,
    GetCredentialReportResponseTypeDef,
    GetGroupPolicyResponseTypeDef,
    GetGroupResponseTypeDef,
    GetInstanceProfileResponseTypeDef,
    GetLoginProfileResponseTypeDef,
    GetOpenIDConnectProviderResponseTypeDef,
    GetOrganizationsAccessReportResponseTypeDef,
    GetPolicyResponseTypeDef,
    GetPolicyVersionResponseTypeDef,
    GetRolePolicyResponseTypeDef,
    GetRoleResponseTypeDef,
    GetSAMLProviderResponseTypeDef,
    GetServerCertificateResponseTypeDef,
    GetServiceLastAccessedDetailsResponseTypeDef,
    GetServiceLastAccessedDetailsWithEntitiesResponseTypeDef,
    GetServiceLinkedRoleDeletionStatusResponseTypeDef,
    GetSSHPublicKeyResponseTypeDef,
    GetUserPolicyResponseTypeDef,
    GetUserResponseTypeDef,
    ListAccessKeysResponseTypeDef,
    ListAccountAliasesResponseTypeDef,
    ListAttachedGroupPoliciesResponseTypeDef,
    ListAttachedRolePoliciesResponseTypeDef,
    ListAttachedUserPoliciesResponseTypeDef,
    ListEntitiesForPolicyResponseTypeDef,
    ListGroupPoliciesResponseTypeDef,
    ListGroupsForUserResponseTypeDef,
    ListGroupsResponseTypeDef,
    ListInstanceProfilesForRoleResponseTypeDef,
    ListInstanceProfilesResponseTypeDef,
    ListInstanceProfileTagsResponseTypeDef,
    ListMFADevicesResponseTypeDef,
    ListMFADeviceTagsResponseTypeDef,
    ListOpenIDConnectProvidersResponseTypeDef,
    ListOpenIDConnectProviderTagsResponseTypeDef,
    ListPoliciesGrantingServiceAccessResponseTypeDef,
    ListPoliciesResponseTypeDef,
    ListPolicyTagsResponseTypeDef,
    ListPolicyVersionsResponseTypeDef,
    ListRolePoliciesResponseTypeDef,
    ListRolesResponseTypeDef,
    ListRoleTagsResponseTypeDef,
    ListSAMLProvidersResponseTypeDef,
    ListSAMLProviderTagsResponseTypeDef,
    ListServerCertificatesResponseTypeDef,
    ListServerCertificateTagsResponseTypeDef,
    ListServiceSpecificCredentialsResponseTypeDef,
    ListSigningCertificatesResponseTypeDef,
    ListSSHPublicKeysResponseTypeDef,
    ListUserPoliciesResponseTypeDef,
    ListUsersResponseTypeDef,
    ListUserTagsResponseTypeDef,
    ListVirtualMFADevicesResponseTypeDef,
    ResetServiceSpecificCredentialResponseTypeDef,
    SimulatePolicyResponseTypeDef,
    TagTypeDef,
    UpdateRoleDescriptionResponseTypeDef,
    UpdateSAMLProviderResponseTypeDef,
    UploadServerCertificateResponseTypeDef,
    UploadSigningCertificateResponseTypeDef,
    UploadSSHPublicKeyResponseTypeDef,
)
from .waiter import (
    InstanceProfileExistsWaiter,
    PolicyExistsWaiter,
    RoleExistsWaiter,
    UserExistsWaiter,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("IAMClient",)

class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    ClientError: Type[BotocoreClientError]
    ConcurrentModificationException: Type[BotocoreClientError]
    CredentialReportExpiredException: Type[BotocoreClientError]
    CredentialReportNotPresentException: Type[BotocoreClientError]
    CredentialReportNotReadyException: Type[BotocoreClientError]
    DeleteConflictException: Type[BotocoreClientError]
    DuplicateCertificateException: Type[BotocoreClientError]
    DuplicateSSHPublicKeyException: Type[BotocoreClientError]
    EntityAlreadyExistsException: Type[BotocoreClientError]
    EntityTemporarilyUnmodifiableException: Type[BotocoreClientError]
    InvalidAuthenticationCodeException: Type[BotocoreClientError]
    InvalidCertificateException: Type[BotocoreClientError]
    InvalidInputException: Type[BotocoreClientError]
    InvalidPublicKeyException: Type[BotocoreClientError]
    InvalidUserTypeException: Type[BotocoreClientError]
    KeyPairMismatchException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    MalformedCertificateException: Type[BotocoreClientError]
    MalformedPolicyDocumentException: Type[BotocoreClientError]
    NoSuchEntityException: Type[BotocoreClientError]
    PasswordPolicyViolationException: Type[BotocoreClientError]
    PolicyEvaluationException: Type[BotocoreClientError]
    PolicyNotAttachableException: Type[BotocoreClientError]
    ReportGenerationLimitExceededException: Type[BotocoreClientError]
    ServiceFailureException: Type[BotocoreClientError]
    ServiceNotSupportedException: Type[BotocoreClientError]
    UnmodifiableEntityException: Type[BotocoreClientError]
    UnrecognizedPublicKeyEncodingException: Type[BotocoreClientError]

class IAMClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        IAMClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#exceptions)
        """
    async def add_client_id_to_open_id_connect_provider(
        self, *, OpenIDConnectProviderArn: str, ClientID: str
    ) -> None:
        """
        Adds a new client ID (also known as audience) to the list of client IDs already
        registered for the specified IAM OpenID Connect (OIDC) provider resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.add_client_id_to_open_id_connect_provider)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#add_client_id_to_open_id_connect_provider)
        """
    async def add_role_to_instance_profile(
        self, *, InstanceProfileName: str, RoleName: str
    ) -> None:
        """
        Adds the specified IAM role to the specified instance profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.add_role_to_instance_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#add_role_to_instance_profile)
        """
    async def add_user_to_group(self, *, GroupName: str, UserName: str) -> None:
        """
        Adds the specified user to the specified group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.add_user_to_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#add_user_to_group)
        """
    async def attach_group_policy(self, *, GroupName: str, PolicyArn: str) -> None:
        """
        Attaches the specified managed policy to the specified IAM group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.attach_group_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#attach_group_policy)
        """
    async def attach_role_policy(self, *, RoleName: str, PolicyArn: str) -> None:
        """
        Attaches the specified managed policy to the specified IAM role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.attach_role_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#attach_role_policy)
        """
    async def attach_user_policy(self, *, UserName: str, PolicyArn: str) -> None:
        """
        Attaches the specified managed policy to the specified user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.attach_user_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#attach_user_policy)
        """
    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#can_paginate)
        """
    async def change_password(self, *, OldPassword: str, NewPassword: str) -> None:
        """
        Changes the password of the IAM user who is calling this operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.change_password)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#change_password)
        """
    async def create_access_key(self, *, UserName: str = ...) -> CreateAccessKeyResponseTypeDef:
        """
        Creates a new Amazon Web Services secret access key and corresponding Amazon Web
        Services access key ID for the specified user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.create_access_key)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#create_access_key)
        """
    async def create_account_alias(self, *, AccountAlias: str) -> None:
        """
        Creates an alias for your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.create_account_alias)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#create_account_alias)
        """
    async def create_group(self, *, GroupName: str, Path: str = ...) -> CreateGroupResponseTypeDef:
        """
        Creates a new group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.create_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#create_group)
        """
    async def create_instance_profile(
        self, *, InstanceProfileName: str, Path: str = ..., Tags: Sequence["TagTypeDef"] = ...
    ) -> CreateInstanceProfileResponseTypeDef:
        """
        Creates a new instance profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.create_instance_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#create_instance_profile)
        """
    async def create_login_profile(
        self, *, UserName: str, Password: str, PasswordResetRequired: bool = ...
    ) -> CreateLoginProfileResponseTypeDef:
        """
        Creates a password for the specified IAM user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.create_login_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#create_login_profile)
        """
    async def create_open_id_connect_provider(
        self,
        *,
        Url: str,
        ThumbprintList: Sequence[str],
        ClientIDList: Sequence[str] = ...,
        Tags: Sequence["TagTypeDef"] = ...
    ) -> CreateOpenIDConnectProviderResponseTypeDef:
        """
        Creates an IAM entity to describe an identity provider (IdP) that supports
        `OpenID Connect (OIDC) <http://openid.net/connect/>`__ .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.create_open_id_connect_provider)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#create_open_id_connect_provider)
        """
    async def create_policy(
        self,
        *,
        PolicyName: str,
        PolicyDocument: str,
        Path: str = ...,
        Description: str = ...,
        Tags: Sequence["TagTypeDef"] = ...
    ) -> CreatePolicyResponseTypeDef:
        """
        Creates a new managed policy for your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.create_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#create_policy)
        """
    async def create_policy_version(
        self, *, PolicyArn: str, PolicyDocument: str, SetAsDefault: bool = ...
    ) -> CreatePolicyVersionResponseTypeDef:
        """
        Creates a new version of the specified managed policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.create_policy_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#create_policy_version)
        """
    async def create_role(
        self,
        *,
        RoleName: str,
        AssumeRolePolicyDocument: str,
        Path: str = ...,
        Description: str = ...,
        MaxSessionDuration: int = ...,
        PermissionsBoundary: str = ...,
        Tags: Sequence["TagTypeDef"] = ...
    ) -> CreateRoleResponseTypeDef:
        """
        Creates a new role for your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.create_role)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#create_role)
        """
    async def create_saml_provider(
        self, *, SAMLMetadataDocument: str, Name: str, Tags: Sequence["TagTypeDef"] = ...
    ) -> CreateSAMLProviderResponseTypeDef:
        """
        Creates an IAM resource that describes an identity provider (IdP) that supports
        SAML 2.0.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.create_saml_provider)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#create_saml_provider)
        """
    async def create_service_linked_role(
        self, *, AWSServiceName: str, Description: str = ..., CustomSuffix: str = ...
    ) -> CreateServiceLinkedRoleResponseTypeDef:
        """
        Creates an IAM role that is linked to a specific Amazon Web Services service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.create_service_linked_role)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#create_service_linked_role)
        """
    async def create_service_specific_credential(
        self, *, UserName: str, ServiceName: str
    ) -> CreateServiceSpecificCredentialResponseTypeDef:
        """
        Generates a set of credentials consisting of a user name and password that can
        be used to access the service specified in the request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.create_service_specific_credential)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#create_service_specific_credential)
        """
    async def create_user(
        self,
        *,
        UserName: str,
        Path: str = ...,
        PermissionsBoundary: str = ...,
        Tags: Sequence["TagTypeDef"] = ...
    ) -> CreateUserResponseTypeDef:
        """
        Creates a new IAM user for your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.create_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#create_user)
        """
    async def create_virtual_mfa_device(
        self, *, VirtualMFADeviceName: str, Path: str = ..., Tags: Sequence["TagTypeDef"] = ...
    ) -> CreateVirtualMFADeviceResponseTypeDef:
        """
        Creates a new virtual MFA device for the Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.create_virtual_mfa_device)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#create_virtual_mfa_device)
        """
    async def deactivate_mfa_device(self, *, UserName: str, SerialNumber: str) -> None:
        """
        Deactivates the specified MFA device and removes it from association with the
        user name for which it was originally enabled.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.deactivate_mfa_device)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#deactivate_mfa_device)
        """
    async def delete_access_key(self, *, AccessKeyId: str, UserName: str = ...) -> None:
        """
        Deletes the access key pair associated with the specified IAM user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.delete_access_key)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#delete_access_key)
        """
    async def delete_account_alias(self, *, AccountAlias: str) -> None:
        """
        Deletes the specified Amazon Web Services account alias.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.delete_account_alias)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#delete_account_alias)
        """
    async def delete_account_password_policy(self) -> None:
        """
        Deletes the password policy for the Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.delete_account_password_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#delete_account_password_policy)
        """
    async def delete_group(self, *, GroupName: str) -> None:
        """
        Deletes the specified IAM group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.delete_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#delete_group)
        """
    async def delete_group_policy(self, *, GroupName: str, PolicyName: str) -> None:
        """
        Deletes the specified inline policy that is embedded in the specified IAM group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.delete_group_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#delete_group_policy)
        """
    async def delete_instance_profile(self, *, InstanceProfileName: str) -> None:
        """
        Deletes the specified instance profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.delete_instance_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#delete_instance_profile)
        """
    async def delete_login_profile(self, *, UserName: str) -> None:
        """
        Deletes the password for the specified IAM user, which terminates the user's
        ability to access Amazon Web Services services through the Amazon Web Services
        Management Console.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.delete_login_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#delete_login_profile)
        """
    async def delete_open_id_connect_provider(self, *, OpenIDConnectProviderArn: str) -> None:
        """
        Deletes an OpenID Connect identity provider (IdP) resource object in IAM.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.delete_open_id_connect_provider)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#delete_open_id_connect_provider)
        """
    async def delete_policy(self, *, PolicyArn: str) -> None:
        """
        Deletes the specified managed policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.delete_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#delete_policy)
        """
    async def delete_policy_version(self, *, PolicyArn: str, VersionId: str) -> None:
        """
        Deletes the specified version from the specified managed policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.delete_policy_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#delete_policy_version)
        """
    async def delete_role(self, *, RoleName: str) -> None:
        """
        Deletes the specified role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.delete_role)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#delete_role)
        """
    async def delete_role_permissions_boundary(self, *, RoleName: str) -> None:
        """
        Deletes the permissions boundary for the specified IAM role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.delete_role_permissions_boundary)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#delete_role_permissions_boundary)
        """
    async def delete_role_policy(self, *, RoleName: str, PolicyName: str) -> None:
        """
        Deletes the specified inline policy that is embedded in the specified IAM role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.delete_role_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#delete_role_policy)
        """
    async def delete_saml_provider(self, *, SAMLProviderArn: str) -> None:
        """
        Deletes a SAML provider resource in IAM.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.delete_saml_provider)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#delete_saml_provider)
        """
    async def delete_server_certificate(self, *, ServerCertificateName: str) -> None:
        """
        Deletes the specified server certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.delete_server_certificate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#delete_server_certificate)
        """
    async def delete_service_linked_role(
        self, *, RoleName: str
    ) -> DeleteServiceLinkedRoleResponseTypeDef:
        """
        Submits a service-linked role deletion request and returns a `DeletionTaskId` ,
        which you can use to check the status of the deletion.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.delete_service_linked_role)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#delete_service_linked_role)
        """
    async def delete_service_specific_credential(
        self, *, ServiceSpecificCredentialId: str, UserName: str = ...
    ) -> None:
        """
        Deletes the specified service-specific credential.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.delete_service_specific_credential)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#delete_service_specific_credential)
        """
    async def delete_signing_certificate(self, *, CertificateId: str, UserName: str = ...) -> None:
        """
        Deletes a signing certificate associated with the specified IAM user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.delete_signing_certificate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#delete_signing_certificate)
        """
    async def delete_ssh_public_key(self, *, UserName: str, SSHPublicKeyId: str) -> None:
        """
        Deletes the specified SSH public key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.delete_ssh_public_key)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#delete_ssh_public_key)
        """
    async def delete_user(self, *, UserName: str) -> None:
        """
        Deletes the specified IAM user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.delete_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#delete_user)
        """
    async def delete_user_permissions_boundary(self, *, UserName: str) -> None:
        """
        Deletes the permissions boundary for the specified IAM user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.delete_user_permissions_boundary)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#delete_user_permissions_boundary)
        """
    async def delete_user_policy(self, *, UserName: str, PolicyName: str) -> None:
        """
        Deletes the specified inline policy that is embedded in the specified IAM user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.delete_user_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#delete_user_policy)
        """
    async def delete_virtual_mfa_device(self, *, SerialNumber: str) -> None:
        """
        Deletes a virtual MFA device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.delete_virtual_mfa_device)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#delete_virtual_mfa_device)
        """
    async def detach_group_policy(self, *, GroupName: str, PolicyArn: str) -> None:
        """
        Removes the specified managed policy from the specified IAM group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.detach_group_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#detach_group_policy)
        """
    async def detach_role_policy(self, *, RoleName: str, PolicyArn: str) -> None:
        """
        Removes the specified managed policy from the specified role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.detach_role_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#detach_role_policy)
        """
    async def detach_user_policy(self, *, UserName: str, PolicyArn: str) -> None:
        """
        Removes the specified managed policy from the specified user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.detach_user_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#detach_user_policy)
        """
    async def enable_mfa_device(
        self,
        *,
        UserName: str,
        SerialNumber: str,
        AuthenticationCode1: str,
        AuthenticationCode2: str
    ) -> None:
        """
        Enables the specified MFA device and associates it with the specified IAM user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.enable_mfa_device)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#enable_mfa_device)
        """
    async def generate_credential_report(self) -> GenerateCredentialReportResponseTypeDef:
        """
        Generates a credential report for the Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.generate_credential_report)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#generate_credential_report)
        """
    async def generate_organizations_access_report(
        self, *, EntityPath: str, OrganizationsPolicyId: str = ...
    ) -> GenerateOrganizationsAccessReportResponseTypeDef:
        """
        Generates a report for service last accessed data for Organizations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.generate_organizations_access_report)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#generate_organizations_access_report)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#generate_presigned_url)
        """
    async def generate_service_last_accessed_details(
        self, *, Arn: str, Granularity: AccessAdvisorUsageGranularityTypeType = ...
    ) -> GenerateServiceLastAccessedDetailsResponseTypeDef:
        """
        Generates a report that includes details about when an IAM resource (user,
        group, role, or policy) was last used in an attempt to access Amazon Web
        Services services.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.generate_service_last_accessed_details)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#generate_service_last_accessed_details)
        """
    async def get_access_key_last_used(
        self, *, AccessKeyId: str
    ) -> GetAccessKeyLastUsedResponseTypeDef:
        """
        Retrieves information about when the specified access key was last used.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_access_key_last_used)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#get_access_key_last_used)
        """
    async def get_account_authorization_details(
        self, *, Filter: Sequence[EntityTypeType] = ..., MaxItems: int = ..., Marker: str = ...
    ) -> GetAccountAuthorizationDetailsResponseTypeDef:
        """
        Retrieves information about all IAM users, groups, roles, and policies in your
        Amazon Web Services account, including their relationships to one another.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_account_authorization_details)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#get_account_authorization_details)
        """
    async def get_account_password_policy(self) -> GetAccountPasswordPolicyResponseTypeDef:
        """
        Retrieves the password policy for the Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_account_password_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#get_account_password_policy)
        """
    async def get_account_summary(self) -> GetAccountSummaryResponseTypeDef:
        """
        Retrieves information about IAM entity usage and IAM quotas in the Amazon Web
        Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_account_summary)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#get_account_summary)
        """
    async def get_context_keys_for_custom_policy(
        self, *, PolicyInputList: Sequence[str]
    ) -> GetContextKeysForPolicyResponseTypeDef:
        """
        Gets a list of all of the context keys referenced in the input policies.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_context_keys_for_custom_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#get_context_keys_for_custom_policy)
        """
    async def get_context_keys_for_principal_policy(
        self, *, PolicySourceArn: str, PolicyInputList: Sequence[str] = ...
    ) -> GetContextKeysForPolicyResponseTypeDef:
        """
        Gets a list of all of the context keys referenced in all the IAM policies that
        are attached to the specified IAM entity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_context_keys_for_principal_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#get_context_keys_for_principal_policy)
        """
    async def get_credential_report(self) -> GetCredentialReportResponseTypeDef:
        """
        Retrieves a credential report for the Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_credential_report)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#get_credential_report)
        """
    async def get_group(
        self, *, GroupName: str, Marker: str = ..., MaxItems: int = ...
    ) -> GetGroupResponseTypeDef:
        """
        Returns a list of IAM users that are in the specified IAM group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#get_group)
        """
    async def get_group_policy(
        self, *, GroupName: str, PolicyName: str
    ) -> GetGroupPolicyResponseTypeDef:
        """
        Retrieves the specified inline policy document that is embedded in the specified
        IAM group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_group_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#get_group_policy)
        """
    async def get_instance_profile(
        self, *, InstanceProfileName: str
    ) -> GetInstanceProfileResponseTypeDef:
        """
        Retrieves information about the specified instance profile, including the
        instance profile's path, GUID, ARN, and role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_instance_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#get_instance_profile)
        """
    async def get_login_profile(self, *, UserName: str) -> GetLoginProfileResponseTypeDef:
        """
        Retrieves the user name for the specified IAM user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_login_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#get_login_profile)
        """
    async def get_open_id_connect_provider(
        self, *, OpenIDConnectProviderArn: str
    ) -> GetOpenIDConnectProviderResponseTypeDef:
        """
        Returns information about the specified OpenID Connect (OIDC) provider resource
        object in IAM.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_open_id_connect_provider)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#get_open_id_connect_provider)
        """
    async def get_organizations_access_report(
        self, *, JobId: str, MaxItems: int = ..., Marker: str = ..., SortKey: sortKeyTypeType = ...
    ) -> GetOrganizationsAccessReportResponseTypeDef:
        """
        Retrieves the service last accessed data report for Organizations that was
        previously generated using the `  GenerateOrganizationsAccessReport ` operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_organizations_access_report)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#get_organizations_access_report)
        """
    async def get_policy(self, *, PolicyArn: str) -> GetPolicyResponseTypeDef:
        """
        Retrieves information about the specified managed policy, including the policy's
        default version and the total number of IAM users, groups, and roles to which
        the policy is attached.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#get_policy)
        """
    async def get_policy_version(
        self, *, PolicyArn: str, VersionId: str
    ) -> GetPolicyVersionResponseTypeDef:
        """
        Retrieves information about the specified version of the specified managed
        policy, including the policy document.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_policy_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#get_policy_version)
        """
    async def get_role(self, *, RoleName: str) -> GetRoleResponseTypeDef:
        """
        Retrieves information about the specified role, including the role's path, GUID,
        ARN, and the role's trust policy that grants permission to assume the role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_role)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#get_role)
        """
    async def get_role_policy(
        self, *, RoleName: str, PolicyName: str
    ) -> GetRolePolicyResponseTypeDef:
        """
        Retrieves the specified inline policy document that is embedded with the
        specified IAM role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_role_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#get_role_policy)
        """
    async def get_saml_provider(self, *, SAMLProviderArn: str) -> GetSAMLProviderResponseTypeDef:
        """
        Returns the SAML provider metadocument that was uploaded when the IAM SAML
        provider resource object was created or updated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_saml_provider)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#get_saml_provider)
        """
    async def get_server_certificate(
        self, *, ServerCertificateName: str
    ) -> GetServerCertificateResponseTypeDef:
        """
        Retrieves information about the specified server certificate stored in IAM.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_server_certificate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#get_server_certificate)
        """
    async def get_service_last_accessed_details(
        self, *, JobId: str, MaxItems: int = ..., Marker: str = ...
    ) -> GetServiceLastAccessedDetailsResponseTypeDef:
        """
        Retrieves a service last accessed report that was created using the
        `GenerateServiceLastAccessedDetails` operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_service_last_accessed_details)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#get_service_last_accessed_details)
        """
    async def get_service_last_accessed_details_with_entities(
        self, *, JobId: str, ServiceNamespace: str, MaxItems: int = ..., Marker: str = ...
    ) -> GetServiceLastAccessedDetailsWithEntitiesResponseTypeDef:
        """
        After you generate a group or policy report using the
        `GenerateServiceLastAccessedDetails` operation, you can use the `JobId`
        parameter in `GetServiceLastAccessedDetailsWithEntities`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_service_last_accessed_details_with_entities)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#get_service_last_accessed_details_with_entities)
        """
    async def get_service_linked_role_deletion_status(
        self, *, DeletionTaskId: str
    ) -> GetServiceLinkedRoleDeletionStatusResponseTypeDef:
        """
        Retrieves the status of your service-linked role deletion.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_service_linked_role_deletion_status)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#get_service_linked_role_deletion_status)
        """
    async def get_ssh_public_key(
        self, *, UserName: str, SSHPublicKeyId: str, Encoding: encodingTypeType
    ) -> GetSSHPublicKeyResponseTypeDef:
        """
        Retrieves the specified SSH public key, including metadata about the key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_ssh_public_key)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#get_ssh_public_key)
        """
    async def get_user(self, *, UserName: str = ...) -> GetUserResponseTypeDef:
        """
        Retrieves information about the specified IAM user, including the user's
        creation date, path, unique ID, and ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#get_user)
        """
    async def get_user_policy(
        self, *, UserName: str, PolicyName: str
    ) -> GetUserPolicyResponseTypeDef:
        """
        Retrieves the specified inline policy document that is embedded in the specified
        IAM user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_user_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#get_user_policy)
        """
    async def list_access_keys(
        self, *, UserName: str = ..., Marker: str = ..., MaxItems: int = ...
    ) -> ListAccessKeysResponseTypeDef:
        """
        Returns information about the access key IDs associated with the specified IAM
        user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_access_keys)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#list_access_keys)
        """
    async def list_account_aliases(
        self, *, Marker: str = ..., MaxItems: int = ...
    ) -> ListAccountAliasesResponseTypeDef:
        """
        Lists the account alias associated with the Amazon Web Services account (Note:
        you can have only one).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_account_aliases)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#list_account_aliases)
        """
    async def list_attached_group_policies(
        self, *, GroupName: str, PathPrefix: str = ..., Marker: str = ..., MaxItems: int = ...
    ) -> ListAttachedGroupPoliciesResponseTypeDef:
        """
        Lists all managed policies that are attached to the specified IAM group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_attached_group_policies)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#list_attached_group_policies)
        """
    async def list_attached_role_policies(
        self, *, RoleName: str, PathPrefix: str = ..., Marker: str = ..., MaxItems: int = ...
    ) -> ListAttachedRolePoliciesResponseTypeDef:
        """
        Lists all managed policies that are attached to the specified IAM role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_attached_role_policies)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#list_attached_role_policies)
        """
    async def list_attached_user_policies(
        self, *, UserName: str, PathPrefix: str = ..., Marker: str = ..., MaxItems: int = ...
    ) -> ListAttachedUserPoliciesResponseTypeDef:
        """
        Lists all managed policies that are attached to the specified IAM user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_attached_user_policies)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#list_attached_user_policies)
        """
    async def list_entities_for_policy(
        self,
        *,
        PolicyArn: str,
        EntityFilter: EntityTypeType = ...,
        PathPrefix: str = ...,
        PolicyUsageFilter: PolicyUsageTypeType = ...,
        Marker: str = ...,
        MaxItems: int = ...
    ) -> ListEntitiesForPolicyResponseTypeDef:
        """
        Lists all IAM users, groups, and roles that the specified managed policy is
        attached to.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_entities_for_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#list_entities_for_policy)
        """
    async def list_group_policies(
        self, *, GroupName: str, Marker: str = ..., MaxItems: int = ...
    ) -> ListGroupPoliciesResponseTypeDef:
        """
        Lists the names of the inline policies that are embedded in the specified IAM
        group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_group_policies)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#list_group_policies)
        """
    async def list_groups(
        self, *, PathPrefix: str = ..., Marker: str = ..., MaxItems: int = ...
    ) -> ListGroupsResponseTypeDef:
        """
        Lists the IAM groups that have the specified path prefix.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#list_groups)
        """
    async def list_groups_for_user(
        self, *, UserName: str, Marker: str = ..., MaxItems: int = ...
    ) -> ListGroupsForUserResponseTypeDef:
        """
        Lists the IAM groups that the specified IAM user belongs to.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_groups_for_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#list_groups_for_user)
        """
    async def list_instance_profile_tags(
        self, *, InstanceProfileName: str, Marker: str = ..., MaxItems: int = ...
    ) -> ListInstanceProfileTagsResponseTypeDef:
        """
        Lists the tags that are attached to the specified IAM instance profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_instance_profile_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#list_instance_profile_tags)
        """
    async def list_instance_profiles(
        self, *, PathPrefix: str = ..., Marker: str = ..., MaxItems: int = ...
    ) -> ListInstanceProfilesResponseTypeDef:
        """
        Lists the instance profiles that have the specified path prefix.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_instance_profiles)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#list_instance_profiles)
        """
    async def list_instance_profiles_for_role(
        self, *, RoleName: str, Marker: str = ..., MaxItems: int = ...
    ) -> ListInstanceProfilesForRoleResponseTypeDef:
        """
        Lists the instance profiles that have the specified associated IAM role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_instance_profiles_for_role)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#list_instance_profiles_for_role)
        """
    async def list_mfa_device_tags(
        self, *, SerialNumber: str, Marker: str = ..., MaxItems: int = ...
    ) -> ListMFADeviceTagsResponseTypeDef:
        """
        Lists the tags that are attached to the specified IAM virtual multi-factor
        authentication (MFA) device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_mfa_device_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#list_mfa_device_tags)
        """
    async def list_mfa_devices(
        self, *, UserName: str = ..., Marker: str = ..., MaxItems: int = ...
    ) -> ListMFADevicesResponseTypeDef:
        """
        Lists the MFA devices for an IAM user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_mfa_devices)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#list_mfa_devices)
        """
    async def list_open_id_connect_provider_tags(
        self, *, OpenIDConnectProviderArn: str, Marker: str = ..., MaxItems: int = ...
    ) -> ListOpenIDConnectProviderTagsResponseTypeDef:
        """
        Lists the tags that are attached to the specified OpenID Connect
        (OIDC)-compatible identity provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_open_id_connect_provider_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#list_open_id_connect_provider_tags)
        """
    async def list_open_id_connect_providers(self) -> ListOpenIDConnectProvidersResponseTypeDef:
        """
        Lists information about the IAM OpenID Connect (OIDC) provider resource objects
        defined in the Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_open_id_connect_providers)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#list_open_id_connect_providers)
        """
    async def list_policies(
        self,
        *,
        Scope: policyScopeTypeType = ...,
        OnlyAttached: bool = ...,
        PathPrefix: str = ...,
        PolicyUsageFilter: PolicyUsageTypeType = ...,
        Marker: str = ...,
        MaxItems: int = ...
    ) -> ListPoliciesResponseTypeDef:
        """
        Lists all the managed policies that are available in your Amazon Web Services
        account, including your own customer-defined managed policies and all Amazon Web
        Services managed policies.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_policies)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#list_policies)
        """
    async def list_policies_granting_service_access(
        self, *, Arn: str, ServiceNamespaces: Sequence[str], Marker: str = ...
    ) -> ListPoliciesGrantingServiceAccessResponseTypeDef:
        """
        Retrieves a list of policies that the IAM identity (user, group, or role) can
        use to access each specified service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_policies_granting_service_access)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#list_policies_granting_service_access)
        """
    async def list_policy_tags(
        self, *, PolicyArn: str, Marker: str = ..., MaxItems: int = ...
    ) -> ListPolicyTagsResponseTypeDef:
        """
        Lists the tags that are attached to the specified IAM customer managed policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_policy_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#list_policy_tags)
        """
    async def list_policy_versions(
        self, *, PolicyArn: str, Marker: str = ..., MaxItems: int = ...
    ) -> ListPolicyVersionsResponseTypeDef:
        """
        Lists information about the versions of the specified managed policy, including
        the version that is currently set as the policy's default version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_policy_versions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#list_policy_versions)
        """
    async def list_role_policies(
        self, *, RoleName: str, Marker: str = ..., MaxItems: int = ...
    ) -> ListRolePoliciesResponseTypeDef:
        """
        Lists the names of the inline policies that are embedded in the specified IAM
        role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_role_policies)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#list_role_policies)
        """
    async def list_role_tags(
        self, *, RoleName: str, Marker: str = ..., MaxItems: int = ...
    ) -> ListRoleTagsResponseTypeDef:
        """
        Lists the tags that are attached to the specified role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_role_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#list_role_tags)
        """
    async def list_roles(
        self, *, PathPrefix: str = ..., Marker: str = ..., MaxItems: int = ...
    ) -> ListRolesResponseTypeDef:
        """
        Lists the IAM roles that have the specified path prefix.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_roles)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#list_roles)
        """
    async def list_saml_provider_tags(
        self, *, SAMLProviderArn: str, Marker: str = ..., MaxItems: int = ...
    ) -> ListSAMLProviderTagsResponseTypeDef:
        """
        Lists the tags that are attached to the specified Security Assertion Markup
        Language (SAML) identity provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_saml_provider_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#list_saml_provider_tags)
        """
    async def list_saml_providers(self) -> ListSAMLProvidersResponseTypeDef:
        """
        Lists the SAML provider resource objects defined in IAM in the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_saml_providers)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#list_saml_providers)
        """
    async def list_server_certificate_tags(
        self, *, ServerCertificateName: str, Marker: str = ..., MaxItems: int = ...
    ) -> ListServerCertificateTagsResponseTypeDef:
        """
        Lists the tags that are attached to the specified IAM server certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_server_certificate_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#list_server_certificate_tags)
        """
    async def list_server_certificates(
        self, *, PathPrefix: str = ..., Marker: str = ..., MaxItems: int = ...
    ) -> ListServerCertificatesResponseTypeDef:
        """
        Lists the server certificates stored in IAM that have the specified path prefix.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_server_certificates)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#list_server_certificates)
        """
    async def list_service_specific_credentials(
        self, *, UserName: str = ..., ServiceName: str = ...
    ) -> ListServiceSpecificCredentialsResponseTypeDef:
        """
        Returns information about the service-specific credentials associated with the
        specified IAM user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_service_specific_credentials)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#list_service_specific_credentials)
        """
    async def list_signing_certificates(
        self, *, UserName: str = ..., Marker: str = ..., MaxItems: int = ...
    ) -> ListSigningCertificatesResponseTypeDef:
        """
        Returns information about the signing certificates associated with the specified
        IAM user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_signing_certificates)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#list_signing_certificates)
        """
    async def list_ssh_public_keys(
        self, *, UserName: str = ..., Marker: str = ..., MaxItems: int = ...
    ) -> ListSSHPublicKeysResponseTypeDef:
        """
        Returns information about the SSH public keys associated with the specified IAM
        user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_ssh_public_keys)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#list_ssh_public_keys)
        """
    async def list_user_policies(
        self, *, UserName: str, Marker: str = ..., MaxItems: int = ...
    ) -> ListUserPoliciesResponseTypeDef:
        """
        Lists the names of the inline policies embedded in the specified IAM user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_user_policies)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#list_user_policies)
        """
    async def list_user_tags(
        self, *, UserName: str, Marker: str = ..., MaxItems: int = ...
    ) -> ListUserTagsResponseTypeDef:
        """
        Lists the tags that are attached to the specified IAM user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_user_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#list_user_tags)
        """
    async def list_users(
        self, *, PathPrefix: str = ..., Marker: str = ..., MaxItems: int = ...
    ) -> ListUsersResponseTypeDef:
        """
        Lists the IAM users that have the specified path prefix.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_users)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#list_users)
        """
    async def list_virtual_mfa_devices(
        self,
        *,
        AssignmentStatus: assignmentStatusTypeType = ...,
        Marker: str = ...,
        MaxItems: int = ...
    ) -> ListVirtualMFADevicesResponseTypeDef:
        """
        Lists the virtual MFA devices defined in the Amazon Web Services account by
        assignment status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_virtual_mfa_devices)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#list_virtual_mfa_devices)
        """
    async def put_group_policy(
        self, *, GroupName: str, PolicyName: str, PolicyDocument: str
    ) -> None:
        """
        Adds or updates an inline policy document that is embedded in the specified IAM
        group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.put_group_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#put_group_policy)
        """
    async def put_role_permissions_boundary(
        self, *, RoleName: str, PermissionsBoundary: str
    ) -> None:
        """
        Adds or updates the policy that is specified as the IAM role's permissions
        boundary.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.put_role_permissions_boundary)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#put_role_permissions_boundary)
        """
    async def put_role_policy(self, *, RoleName: str, PolicyName: str, PolicyDocument: str) -> None:
        """
        Adds or updates an inline policy document that is embedded in the specified IAM
        role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.put_role_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#put_role_policy)
        """
    async def put_user_permissions_boundary(
        self, *, UserName: str, PermissionsBoundary: str
    ) -> None:
        """
        Adds or updates the policy that is specified as the IAM user's permissions
        boundary.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.put_user_permissions_boundary)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#put_user_permissions_boundary)
        """
    async def put_user_policy(self, *, UserName: str, PolicyName: str, PolicyDocument: str) -> None:
        """
        Adds or updates an inline policy document that is embedded in the specified IAM
        user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.put_user_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#put_user_policy)
        """
    async def remove_client_id_from_open_id_connect_provider(
        self, *, OpenIDConnectProviderArn: str, ClientID: str
    ) -> None:
        """
        Removes the specified client ID (also known as audience) from the list of client
        IDs registered for the specified IAM OpenID Connect (OIDC) provider resource
        object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.remove_client_id_from_open_id_connect_provider)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#remove_client_id_from_open_id_connect_provider)
        """
    async def remove_role_from_instance_profile(
        self, *, InstanceProfileName: str, RoleName: str
    ) -> None:
        """
        Removes the specified IAM role from the specified EC2 instance profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.remove_role_from_instance_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#remove_role_from_instance_profile)
        """
    async def remove_user_from_group(self, *, GroupName: str, UserName: str) -> None:
        """
        Removes the specified user from the specified group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.remove_user_from_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#remove_user_from_group)
        """
    async def reset_service_specific_credential(
        self, *, ServiceSpecificCredentialId: str, UserName: str = ...
    ) -> ResetServiceSpecificCredentialResponseTypeDef:
        """
        Resets the password for a service-specific credential.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.reset_service_specific_credential)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#reset_service_specific_credential)
        """
    async def resync_mfa_device(
        self,
        *,
        UserName: str,
        SerialNumber: str,
        AuthenticationCode1: str,
        AuthenticationCode2: str
    ) -> None:
        """
        Synchronizes the specified MFA device with its IAM resource object on the Amazon
        Web Services servers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.resync_mfa_device)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#resync_mfa_device)
        """
    async def set_default_policy_version(self, *, PolicyArn: str, VersionId: str) -> None:
        """
        Sets the specified version of the specified policy as the policy's default
        (operative) version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.set_default_policy_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#set_default_policy_version)
        """
    async def set_security_token_service_preferences(
        self, *, GlobalEndpointTokenVersion: globalEndpointTokenVersionType
    ) -> None:
        """
        Sets the specified version of the global endpoint token as the token version
        used for the Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.set_security_token_service_preferences)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#set_security_token_service_preferences)
        """
    async def simulate_custom_policy(
        self,
        *,
        PolicyInputList: Sequence[str],
        ActionNames: Sequence[str],
        PermissionsBoundaryPolicyInputList: Sequence[str] = ...,
        ResourceArns: Sequence[str] = ...,
        ResourcePolicy: str = ...,
        ResourceOwner: str = ...,
        CallerArn: str = ...,
        ContextEntries: Sequence["ContextEntryTypeDef"] = ...,
        ResourceHandlingOption: str = ...,
        MaxItems: int = ...,
        Marker: str = ...
    ) -> SimulatePolicyResponseTypeDef:
        """
        Simulate how a set of IAM policies and optionally a resource-based policy works
        with a list of API operations and Amazon Web Services resources to determine the
        policies' effective permissions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.simulate_custom_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#simulate_custom_policy)
        """
    async def simulate_principal_policy(
        self,
        *,
        PolicySourceArn: str,
        ActionNames: Sequence[str],
        PolicyInputList: Sequence[str] = ...,
        PermissionsBoundaryPolicyInputList: Sequence[str] = ...,
        ResourceArns: Sequence[str] = ...,
        ResourcePolicy: str = ...,
        ResourceOwner: str = ...,
        CallerArn: str = ...,
        ContextEntries: Sequence["ContextEntryTypeDef"] = ...,
        ResourceHandlingOption: str = ...,
        MaxItems: int = ...,
        Marker: str = ...
    ) -> SimulatePolicyResponseTypeDef:
        """
        Simulate how a set of IAM policies attached to an IAM entity works with a list
        of API operations and Amazon Web Services resources to determine the policies'
        effective permissions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.simulate_principal_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#simulate_principal_policy)
        """
    async def tag_instance_profile(
        self, *, InstanceProfileName: str, Tags: Sequence["TagTypeDef"]
    ) -> None:
        """
        Adds one or more tags to an IAM instance profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.tag_instance_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#tag_instance_profile)
        """
    async def tag_mfa_device(self, *, SerialNumber: str, Tags: Sequence["TagTypeDef"]) -> None:
        """
        Adds one or more tags to an IAM virtual multi-factor authentication (MFA)
        device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.tag_mfa_device)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#tag_mfa_device)
        """
    async def tag_open_id_connect_provider(
        self, *, OpenIDConnectProviderArn: str, Tags: Sequence["TagTypeDef"]
    ) -> None:
        """
        Adds one or more tags to an OpenID Connect (OIDC)-compatible identity provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.tag_open_id_connect_provider)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#tag_open_id_connect_provider)
        """
    async def tag_policy(self, *, PolicyArn: str, Tags: Sequence["TagTypeDef"]) -> None:
        """
        Adds one or more tags to an IAM customer managed policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.tag_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#tag_policy)
        """
    async def tag_role(self, *, RoleName: str, Tags: Sequence["TagTypeDef"]) -> None:
        """
        Adds one or more tags to an IAM role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.tag_role)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#tag_role)
        """
    async def tag_saml_provider(
        self, *, SAMLProviderArn: str, Tags: Sequence["TagTypeDef"]
    ) -> None:
        """
        Adds one or more tags to a Security Assertion Markup Language (SAML) identity
        provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.tag_saml_provider)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#tag_saml_provider)
        """
    async def tag_server_certificate(
        self, *, ServerCertificateName: str, Tags: Sequence["TagTypeDef"]
    ) -> None:
        """
        Adds one or more tags to an IAM server certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.tag_server_certificate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#tag_server_certificate)
        """
    async def tag_user(self, *, UserName: str, Tags: Sequence["TagTypeDef"]) -> None:
        """
        Adds one or more tags to an IAM user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.tag_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#tag_user)
        """
    async def untag_instance_profile(
        self, *, InstanceProfileName: str, TagKeys: Sequence[str]
    ) -> None:
        """
        Removes the specified tags from the IAM instance profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.untag_instance_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#untag_instance_profile)
        """
    async def untag_mfa_device(self, *, SerialNumber: str, TagKeys: Sequence[str]) -> None:
        """
        Removes the specified tags from the IAM virtual multi-factor authentication
        (MFA) device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.untag_mfa_device)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#untag_mfa_device)
        """
    async def untag_open_id_connect_provider(
        self, *, OpenIDConnectProviderArn: str, TagKeys: Sequence[str]
    ) -> None:
        """
        Removes the specified tags from the specified OpenID Connect (OIDC)-compatible
        identity provider in IAM.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.untag_open_id_connect_provider)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#untag_open_id_connect_provider)
        """
    async def untag_policy(self, *, PolicyArn: str, TagKeys: Sequence[str]) -> None:
        """
        Removes the specified tags from the customer managed policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.untag_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#untag_policy)
        """
    async def untag_role(self, *, RoleName: str, TagKeys: Sequence[str]) -> None:
        """
        Removes the specified tags from the role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.untag_role)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#untag_role)
        """
    async def untag_saml_provider(self, *, SAMLProviderArn: str, TagKeys: Sequence[str]) -> None:
        """
        Removes the specified tags from the specified Security Assertion Markup Language
        (SAML) identity provider in IAM.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.untag_saml_provider)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#untag_saml_provider)
        """
    async def untag_server_certificate(
        self, *, ServerCertificateName: str, TagKeys: Sequence[str]
    ) -> None:
        """
        Removes the specified tags from the IAM server certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.untag_server_certificate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#untag_server_certificate)
        """
    async def untag_user(self, *, UserName: str, TagKeys: Sequence[str]) -> None:
        """
        Removes the specified tags from the user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.untag_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#untag_user)
        """
    async def update_access_key(
        self, *, AccessKeyId: str, Status: statusTypeType, UserName: str = ...
    ) -> None:
        """
        Changes the status of the specified access key from Active to Inactive, or vice
        versa.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.update_access_key)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#update_access_key)
        """
    async def update_account_password_policy(
        self,
        *,
        MinimumPasswordLength: int = ...,
        RequireSymbols: bool = ...,
        RequireNumbers: bool = ...,
        RequireUppercaseCharacters: bool = ...,
        RequireLowercaseCharacters: bool = ...,
        AllowUsersToChangePassword: bool = ...,
        MaxPasswordAge: int = ...,
        PasswordReusePrevention: int = ...,
        HardExpiry: bool = ...
    ) -> None:
        """
        Updates the password policy settings for the Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.update_account_password_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#update_account_password_policy)
        """
    async def update_assume_role_policy(self, *, RoleName: str, PolicyDocument: str) -> None:
        """
        Updates the policy that grants an IAM entity permission to assume a role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.update_assume_role_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#update_assume_role_policy)
        """
    async def update_group(
        self, *, GroupName: str, NewPath: str = ..., NewGroupName: str = ...
    ) -> None:
        """
        Updates the name and/or the path of the specified IAM group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.update_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#update_group)
        """
    async def update_login_profile(
        self, *, UserName: str, Password: str = ..., PasswordResetRequired: bool = ...
    ) -> None:
        """
        Changes the password for the specified IAM user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.update_login_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#update_login_profile)
        """
    async def update_open_id_connect_provider_thumbprint(
        self, *, OpenIDConnectProviderArn: str, ThumbprintList: Sequence[str]
    ) -> None:
        """
        Replaces the existing list of server certificate thumbprints associated with an
        OpenID Connect (OIDC) provider resource object with a new list of thumbprints.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.update_open_id_connect_provider_thumbprint)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#update_open_id_connect_provider_thumbprint)
        """
    async def update_role(
        self, *, RoleName: str, Description: str = ..., MaxSessionDuration: int = ...
    ) -> Dict[str, Any]:
        """
        Updates the description or maximum session duration setting of a role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.update_role)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#update_role)
        """
    async def update_role_description(
        self, *, RoleName: str, Description: str
    ) -> UpdateRoleDescriptionResponseTypeDef:
        """
        Use  UpdateRole instead.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.update_role_description)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#update_role_description)
        """
    async def update_saml_provider(
        self, *, SAMLMetadataDocument: str, SAMLProviderArn: str
    ) -> UpdateSAMLProviderResponseTypeDef:
        """
        Updates the metadata document for an existing SAML provider resource object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.update_saml_provider)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#update_saml_provider)
        """
    async def update_server_certificate(
        self, *, ServerCertificateName: str, NewPath: str = ..., NewServerCertificateName: str = ...
    ) -> None:
        """
        Updates the name and/or the path of the specified server certificate stored in
        IAM.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.update_server_certificate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#update_server_certificate)
        """
    async def update_service_specific_credential(
        self, *, ServiceSpecificCredentialId: str, Status: statusTypeType, UserName: str = ...
    ) -> None:
        """
        Sets the status of a service-specific credential to `Active` or `Inactive`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.update_service_specific_credential)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#update_service_specific_credential)
        """
    async def update_signing_certificate(
        self, *, CertificateId: str, Status: statusTypeType, UserName: str = ...
    ) -> None:
        """
        Changes the status of the specified user signing certificate from active to
        disabled, or vice versa.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.update_signing_certificate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#update_signing_certificate)
        """
    async def update_ssh_public_key(
        self, *, UserName: str, SSHPublicKeyId: str, Status: statusTypeType
    ) -> None:
        """
        Sets the status of an IAM user's SSH public key to active or inactive.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.update_ssh_public_key)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#update_ssh_public_key)
        """
    async def update_user(
        self, *, UserName: str, NewPath: str = ..., NewUserName: str = ...
    ) -> None:
        """
        Updates the name and/or the path of the specified IAM user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.update_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#update_user)
        """
    async def upload_server_certificate(
        self,
        *,
        ServerCertificateName: str,
        CertificateBody: str,
        PrivateKey: str,
        Path: str = ...,
        CertificateChain: str = ...,
        Tags: Sequence["TagTypeDef"] = ...
    ) -> UploadServerCertificateResponseTypeDef:
        """
        Uploads a server certificate entity for the Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.upload_server_certificate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#upload_server_certificate)
        """
    async def upload_signing_certificate(
        self, *, CertificateBody: str, UserName: str = ...
    ) -> UploadSigningCertificateResponseTypeDef:
        """
        Uploads an X.509 signing certificate and associates it with the specified IAM
        user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.upload_signing_certificate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#upload_signing_certificate)
        """
    async def upload_ssh_public_key(
        self, *, UserName: str, SSHPublicKeyBody: str
    ) -> UploadSSHPublicKeyResponseTypeDef:
        """
        Uploads an SSH public key and associates it with the specified IAM user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.upload_ssh_public_key)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#upload_ssh_public_key)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["get_account_authorization_details"]
    ) -> GetAccountAuthorizationDetailsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#get_paginator)
        """
    @overload
    def get_paginator(self, operation_name: Literal["get_group"]) -> GetGroupPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#get_paginator)
        """
    @overload
    def get_paginator(self, operation_name: Literal["list_access_keys"]) -> ListAccessKeysPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_account_aliases"]
    ) -> ListAccountAliasesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_attached_group_policies"]
    ) -> ListAttachedGroupPoliciesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_attached_role_policies"]
    ) -> ListAttachedRolePoliciesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_attached_user_policies"]
    ) -> ListAttachedUserPoliciesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_entities_for_policy"]
    ) -> ListEntitiesForPolicyPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_group_policies"]
    ) -> ListGroupPoliciesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#get_paginator)
        """
    @overload
    def get_paginator(self, operation_name: Literal["list_groups"]) -> ListGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_groups_for_user"]
    ) -> ListGroupsForUserPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_instance_profiles"]
    ) -> ListInstanceProfilesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_instance_profiles_for_role"]
    ) -> ListInstanceProfilesForRolePaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#get_paginator)
        """
    @overload
    def get_paginator(self, operation_name: Literal["list_mfa_devices"]) -> ListMFADevicesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#get_paginator)
        """
    @overload
    def get_paginator(self, operation_name: Literal["list_policies"]) -> ListPoliciesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_policy_versions"]
    ) -> ListPolicyVersionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_role_policies"]
    ) -> ListRolePoliciesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#get_paginator)
        """
    @overload
    def get_paginator(self, operation_name: Literal["list_roles"]) -> ListRolesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_ssh_public_keys"]
    ) -> ListSSHPublicKeysPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_server_certificates"]
    ) -> ListServerCertificatesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_signing_certificates"]
    ) -> ListSigningCertificatesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_user_policies"]
    ) -> ListUserPoliciesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#get_paginator)
        """
    @overload
    def get_paginator(self, operation_name: Literal["list_user_tags"]) -> ListUserTagsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#get_paginator)
        """
    @overload
    def get_paginator(self, operation_name: Literal["list_users"]) -> ListUsersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_virtual_mfa_devices"]
    ) -> ListVirtualMFADevicesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["simulate_custom_policy"]
    ) -> SimulateCustomPolicyPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["simulate_principal_policy"]
    ) -> SimulatePrincipalPolicyPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#get_paginator)
        """
    @overload
    def get_waiter(
        self, waiter_name: Literal["instance_profile_exists"]
    ) -> InstanceProfileExistsWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#get_waiter)
        """
    @overload
    def get_waiter(self, waiter_name: Literal["policy_exists"]) -> PolicyExistsWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#get_waiter)
        """
    @overload
    def get_waiter(self, waiter_name: Literal["role_exists"]) -> RoleExistsWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#get_waiter)
        """
    @overload
    def get_waiter(self, waiter_name: Literal["user_exists"]) -> UserExistsWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/#get_waiter)
        """
    async def __aenter__(self) -> "IAMClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/)
        """
    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/client/)
        """
