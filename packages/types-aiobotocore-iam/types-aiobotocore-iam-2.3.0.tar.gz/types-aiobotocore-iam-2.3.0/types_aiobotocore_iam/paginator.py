"""
Type annotations for iam service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_iam.client import IAMClient
    from types_aiobotocore_iam.paginator import (
        GetAccountAuthorizationDetailsPaginator,
        GetGroupPaginator,
        ListAccessKeysPaginator,
        ListAccountAliasesPaginator,
        ListAttachedGroupPoliciesPaginator,
        ListAttachedRolePoliciesPaginator,
        ListAttachedUserPoliciesPaginator,
        ListEntitiesForPolicyPaginator,
        ListGroupPoliciesPaginator,
        ListGroupsPaginator,
        ListGroupsForUserPaginator,
        ListInstanceProfilesPaginator,
        ListInstanceProfilesForRolePaginator,
        ListMFADevicesPaginator,
        ListPoliciesPaginator,
        ListPolicyVersionsPaginator,
        ListRolePoliciesPaginator,
        ListRolesPaginator,
        ListSSHPublicKeysPaginator,
        ListServerCertificatesPaginator,
        ListSigningCertificatesPaginator,
        ListUserPoliciesPaginator,
        ListUserTagsPaginator,
        ListUsersPaginator,
        ListVirtualMFADevicesPaginator,
        SimulateCustomPolicyPaginator,
        SimulatePrincipalPolicyPaginator,
    )

    session = get_session()
    with session.create_client("iam") as client:
        client: IAMClient

        get_account_authorization_details_paginator: GetAccountAuthorizationDetailsPaginator = client.get_paginator("get_account_authorization_details")
        get_group_paginator: GetGroupPaginator = client.get_paginator("get_group")
        list_access_keys_paginator: ListAccessKeysPaginator = client.get_paginator("list_access_keys")
        list_account_aliases_paginator: ListAccountAliasesPaginator = client.get_paginator("list_account_aliases")
        list_attached_group_policies_paginator: ListAttachedGroupPoliciesPaginator = client.get_paginator("list_attached_group_policies")
        list_attached_role_policies_paginator: ListAttachedRolePoliciesPaginator = client.get_paginator("list_attached_role_policies")
        list_attached_user_policies_paginator: ListAttachedUserPoliciesPaginator = client.get_paginator("list_attached_user_policies")
        list_entities_for_policy_paginator: ListEntitiesForPolicyPaginator = client.get_paginator("list_entities_for_policy")
        list_group_policies_paginator: ListGroupPoliciesPaginator = client.get_paginator("list_group_policies")
        list_groups_paginator: ListGroupsPaginator = client.get_paginator("list_groups")
        list_groups_for_user_paginator: ListGroupsForUserPaginator = client.get_paginator("list_groups_for_user")
        list_instance_profiles_paginator: ListInstanceProfilesPaginator = client.get_paginator("list_instance_profiles")
        list_instance_profiles_for_role_paginator: ListInstanceProfilesForRolePaginator = client.get_paginator("list_instance_profiles_for_role")
        list_mfa_devices_paginator: ListMFADevicesPaginator = client.get_paginator("list_mfa_devices")
        list_policies_paginator: ListPoliciesPaginator = client.get_paginator("list_policies")
        list_policy_versions_paginator: ListPolicyVersionsPaginator = client.get_paginator("list_policy_versions")
        list_role_policies_paginator: ListRolePoliciesPaginator = client.get_paginator("list_role_policies")
        list_roles_paginator: ListRolesPaginator = client.get_paginator("list_roles")
        list_ssh_public_keys_paginator: ListSSHPublicKeysPaginator = client.get_paginator("list_ssh_public_keys")
        list_server_certificates_paginator: ListServerCertificatesPaginator = client.get_paginator("list_server_certificates")
        list_signing_certificates_paginator: ListSigningCertificatesPaginator = client.get_paginator("list_signing_certificates")
        list_user_policies_paginator: ListUserPoliciesPaginator = client.get_paginator("list_user_policies")
        list_user_tags_paginator: ListUserTagsPaginator = client.get_paginator("list_user_tags")
        list_users_paginator: ListUsersPaginator = client.get_paginator("list_users")
        list_virtual_mfa_devices_paginator: ListVirtualMFADevicesPaginator = client.get_paginator("list_virtual_mfa_devices")
        simulate_custom_policy_paginator: SimulateCustomPolicyPaginator = client.get_paginator("simulate_custom_policy")
        simulate_principal_policy_paginator: SimulatePrincipalPolicyPaginator = client.get_paginator("simulate_principal_policy")
    ```
"""
import sys
from typing import Generic, Iterator, Sequence, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .literals import (
    EntityTypeType,
    PolicyUsageTypeType,
    assignmentStatusTypeType,
    policyScopeTypeType,
)
from .type_defs import (
    ContextEntryTypeDef,
    GetAccountAuthorizationDetailsResponseTypeDef,
    GetGroupResponseTypeDef,
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
    ListMFADevicesResponseTypeDef,
    ListPoliciesResponseTypeDef,
    ListPolicyVersionsResponseTypeDef,
    ListRolePoliciesResponseTypeDef,
    ListRolesResponseTypeDef,
    ListServerCertificatesResponseTypeDef,
    ListSigningCertificatesResponseTypeDef,
    ListSSHPublicKeysResponseTypeDef,
    ListUserPoliciesResponseTypeDef,
    ListUsersResponseTypeDef,
    ListUserTagsResponseTypeDef,
    ListVirtualMFADevicesResponseTypeDef,
    PaginatorConfigTypeDef,
    SimulatePolicyResponseTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import AsyncIterator
else:
    from typing_extensions import AsyncIterator


__all__ = (
    "GetAccountAuthorizationDetailsPaginator",
    "GetGroupPaginator",
    "ListAccessKeysPaginator",
    "ListAccountAliasesPaginator",
    "ListAttachedGroupPoliciesPaginator",
    "ListAttachedRolePoliciesPaginator",
    "ListAttachedUserPoliciesPaginator",
    "ListEntitiesForPolicyPaginator",
    "ListGroupPoliciesPaginator",
    "ListGroupsPaginator",
    "ListGroupsForUserPaginator",
    "ListInstanceProfilesPaginator",
    "ListInstanceProfilesForRolePaginator",
    "ListMFADevicesPaginator",
    "ListPoliciesPaginator",
    "ListPolicyVersionsPaginator",
    "ListRolePoliciesPaginator",
    "ListRolesPaginator",
    "ListSSHPublicKeysPaginator",
    "ListServerCertificatesPaginator",
    "ListSigningCertificatesPaginator",
    "ListUserPoliciesPaginator",
    "ListUserTagsPaginator",
    "ListUsersPaginator",
    "ListVirtualMFADevicesPaginator",
    "SimulateCustomPolicyPaginator",
    "SimulatePrincipalPolicyPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class GetAccountAuthorizationDetailsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Paginator.GetAccountAuthorizationDetails)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#getaccountauthorizationdetailspaginator)
    """

    def paginate(
        self,
        *,
        Filter: Sequence[EntityTypeType] = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[GetAccountAuthorizationDetailsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Paginator.GetAccountAuthorizationDetails.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#getaccountauthorizationdetailspaginator)
        """


class GetGroupPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Paginator.GetGroup)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#getgrouppaginator)
    """

    def paginate(
        self, *, GroupName: str, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[GetGroupResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Paginator.GetGroup.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#getgrouppaginator)
        """


class ListAccessKeysPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Paginator.ListAccessKeys)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listaccesskeyspaginator)
    """

    def paginate(
        self, *, UserName: str = ..., PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListAccessKeysResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Paginator.ListAccessKeys.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listaccesskeyspaginator)
        """


class ListAccountAliasesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Paginator.ListAccountAliases)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listaccountaliasespaginator)
    """

    def paginate(
        self, *, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListAccountAliasesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Paginator.ListAccountAliases.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listaccountaliasespaginator)
        """


class ListAttachedGroupPoliciesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Paginator.ListAttachedGroupPolicies)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listattachedgrouppoliciespaginator)
    """

    def paginate(
        self,
        *,
        GroupName: str,
        PathPrefix: str = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListAttachedGroupPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Paginator.ListAttachedGroupPolicies.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listattachedgrouppoliciespaginator)
        """


class ListAttachedRolePoliciesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Paginator.ListAttachedRolePolicies)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listattachedrolepoliciespaginator)
    """

    def paginate(
        self,
        *,
        RoleName: str,
        PathPrefix: str = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListAttachedRolePoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Paginator.ListAttachedRolePolicies.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listattachedrolepoliciespaginator)
        """


class ListAttachedUserPoliciesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Paginator.ListAttachedUserPolicies)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listattacheduserpoliciespaginator)
    """

    def paginate(
        self,
        *,
        UserName: str,
        PathPrefix: str = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListAttachedUserPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Paginator.ListAttachedUserPolicies.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listattacheduserpoliciespaginator)
        """


class ListEntitiesForPolicyPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Paginator.ListEntitiesForPolicy)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listentitiesforpolicypaginator)
    """

    def paginate(
        self,
        *,
        PolicyArn: str,
        EntityFilter: EntityTypeType = ...,
        PathPrefix: str = ...,
        PolicyUsageFilter: PolicyUsageTypeType = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListEntitiesForPolicyResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Paginator.ListEntitiesForPolicy.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listentitiesforpolicypaginator)
        """


class ListGroupPoliciesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Paginator.ListGroupPolicies)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listgrouppoliciespaginator)
    """

    def paginate(
        self, *, GroupName: str, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListGroupPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Paginator.ListGroupPolicies.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listgrouppoliciespaginator)
        """


class ListGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Paginator.ListGroups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listgroupspaginator)
    """

    def paginate(
        self, *, PathPrefix: str = ..., PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Paginator.ListGroups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listgroupspaginator)
        """


class ListGroupsForUserPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Paginator.ListGroupsForUser)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listgroupsforuserpaginator)
    """

    def paginate(
        self, *, UserName: str, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListGroupsForUserResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Paginator.ListGroupsForUser.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listgroupsforuserpaginator)
        """


class ListInstanceProfilesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Paginator.ListInstanceProfiles)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listinstanceprofilespaginator)
    """

    def paginate(
        self, *, PathPrefix: str = ..., PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListInstanceProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Paginator.ListInstanceProfiles.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listinstanceprofilespaginator)
        """


class ListInstanceProfilesForRolePaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Paginator.ListInstanceProfilesForRole)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listinstanceprofilesforrolepaginator)
    """

    def paginate(
        self, *, RoleName: str, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListInstanceProfilesForRoleResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Paginator.ListInstanceProfilesForRole.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listinstanceprofilesforrolepaginator)
        """


class ListMFADevicesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Paginator.ListMFADevices)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listmfadevicespaginator)
    """

    def paginate(
        self, *, UserName: str = ..., PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListMFADevicesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Paginator.ListMFADevices.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listmfadevicespaginator)
        """


class ListPoliciesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Paginator.ListPolicies)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listpoliciespaginator)
    """

    def paginate(
        self,
        *,
        Scope: policyScopeTypeType = ...,
        OnlyAttached: bool = ...,
        PathPrefix: str = ...,
        PolicyUsageFilter: PolicyUsageTypeType = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Paginator.ListPolicies.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listpoliciespaginator)
        """


class ListPolicyVersionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Paginator.ListPolicyVersions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listpolicyversionspaginator)
    """

    def paginate(
        self, *, PolicyArn: str, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListPolicyVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Paginator.ListPolicyVersions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listpolicyversionspaginator)
        """


class ListRolePoliciesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Paginator.ListRolePolicies)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listrolepoliciespaginator)
    """

    def paginate(
        self, *, RoleName: str, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListRolePoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Paginator.ListRolePolicies.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listrolepoliciespaginator)
        """


class ListRolesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Paginator.ListRoles)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listrolespaginator)
    """

    def paginate(
        self, *, PathPrefix: str = ..., PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListRolesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Paginator.ListRoles.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listrolespaginator)
        """


class ListSSHPublicKeysPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Paginator.ListSSHPublicKeys)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listsshpublickeyspaginator)
    """

    def paginate(
        self, *, UserName: str = ..., PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListSSHPublicKeysResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Paginator.ListSSHPublicKeys.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listsshpublickeyspaginator)
        """


class ListServerCertificatesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Paginator.ListServerCertificates)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listservercertificatespaginator)
    """

    def paginate(
        self, *, PathPrefix: str = ..., PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListServerCertificatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Paginator.ListServerCertificates.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listservercertificatespaginator)
        """


class ListSigningCertificatesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Paginator.ListSigningCertificates)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listsigningcertificatespaginator)
    """

    def paginate(
        self, *, UserName: str = ..., PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListSigningCertificatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Paginator.ListSigningCertificates.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listsigningcertificatespaginator)
        """


class ListUserPoliciesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Paginator.ListUserPolicies)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listuserpoliciespaginator)
    """

    def paginate(
        self, *, UserName: str, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListUserPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Paginator.ListUserPolicies.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listuserpoliciespaginator)
        """


class ListUserTagsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Paginator.ListUserTags)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listusertagspaginator)
    """

    def paginate(
        self, *, UserName: str, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListUserTagsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Paginator.ListUserTags.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listusertagspaginator)
        """


class ListUsersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Paginator.ListUsers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listuserspaginator)
    """

    def paginate(
        self, *, PathPrefix: str = ..., PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListUsersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Paginator.ListUsers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listuserspaginator)
        """


class ListVirtualMFADevicesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Paginator.ListVirtualMFADevices)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listvirtualmfadevicespaginator)
    """

    def paginate(
        self,
        *,
        AssignmentStatus: assignmentStatusTypeType = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListVirtualMFADevicesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Paginator.ListVirtualMFADevices.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#listvirtualmfadevicespaginator)
        """


class SimulateCustomPolicyPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Paginator.SimulateCustomPolicy)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#simulatecustompolicypaginator)
    """

    def paginate(
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
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[SimulatePolicyResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Paginator.SimulateCustomPolicy.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#simulatecustompolicypaginator)
        """


class SimulatePrincipalPolicyPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Paginator.SimulatePrincipalPolicy)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#simulateprincipalpolicypaginator)
    """

    def paginate(
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
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[SimulatePolicyResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Paginator.SimulatePrincipalPolicy.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/paginators/#simulateprincipalpolicypaginator)
        """
