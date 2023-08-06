"""
Type annotations for organizations service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_organizations.client import OrganizationsClient
    from types_aiobotocore_organizations.paginator import (
        ListAWSServiceAccessForOrganizationPaginator,
        ListAccountsPaginator,
        ListAccountsForParentPaginator,
        ListChildrenPaginator,
        ListCreateAccountStatusPaginator,
        ListDelegatedAdministratorsPaginator,
        ListDelegatedServicesForAccountPaginator,
        ListHandshakesForAccountPaginator,
        ListHandshakesForOrganizationPaginator,
        ListOrganizationalUnitsForParentPaginator,
        ListParentsPaginator,
        ListPoliciesPaginator,
        ListPoliciesForTargetPaginator,
        ListRootsPaginator,
        ListTagsForResourcePaginator,
        ListTargetsForPolicyPaginator,
    )

    session = get_session()
    with session.create_client("organizations") as client:
        client: OrganizationsClient

        list_aws_service_access_for_organization_paginator: ListAWSServiceAccessForOrganizationPaginator = client.get_paginator("list_aws_service_access_for_organization")
        list_accounts_paginator: ListAccountsPaginator = client.get_paginator("list_accounts")
        list_accounts_for_parent_paginator: ListAccountsForParentPaginator = client.get_paginator("list_accounts_for_parent")
        list_children_paginator: ListChildrenPaginator = client.get_paginator("list_children")
        list_create_account_status_paginator: ListCreateAccountStatusPaginator = client.get_paginator("list_create_account_status")
        list_delegated_administrators_paginator: ListDelegatedAdministratorsPaginator = client.get_paginator("list_delegated_administrators")
        list_delegated_services_for_account_paginator: ListDelegatedServicesForAccountPaginator = client.get_paginator("list_delegated_services_for_account")
        list_handshakes_for_account_paginator: ListHandshakesForAccountPaginator = client.get_paginator("list_handshakes_for_account")
        list_handshakes_for_organization_paginator: ListHandshakesForOrganizationPaginator = client.get_paginator("list_handshakes_for_organization")
        list_organizational_units_for_parent_paginator: ListOrganizationalUnitsForParentPaginator = client.get_paginator("list_organizational_units_for_parent")
        list_parents_paginator: ListParentsPaginator = client.get_paginator("list_parents")
        list_policies_paginator: ListPoliciesPaginator = client.get_paginator("list_policies")
        list_policies_for_target_paginator: ListPoliciesForTargetPaginator = client.get_paginator("list_policies_for_target")
        list_roots_paginator: ListRootsPaginator = client.get_paginator("list_roots")
        list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
        list_targets_for_policy_paginator: ListTargetsForPolicyPaginator = client.get_paginator("list_targets_for_policy")
    ```
"""
import sys
from typing import Generic, Iterator, Sequence, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .literals import ChildTypeType, CreateAccountStateType, PolicyTypeType
from .type_defs import (
    HandshakeFilterTypeDef,
    ListAccountsForParentResponseTypeDef,
    ListAccountsResponseTypeDef,
    ListAWSServiceAccessForOrganizationResponseTypeDef,
    ListChildrenResponseTypeDef,
    ListCreateAccountStatusResponseTypeDef,
    ListDelegatedAdministratorsResponseTypeDef,
    ListDelegatedServicesForAccountResponseTypeDef,
    ListHandshakesForAccountResponseTypeDef,
    ListHandshakesForOrganizationResponseTypeDef,
    ListOrganizationalUnitsForParentResponseTypeDef,
    ListParentsResponseTypeDef,
    ListPoliciesForTargetResponseTypeDef,
    ListPoliciesResponseTypeDef,
    ListRootsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTargetsForPolicyResponseTypeDef,
    PaginatorConfigTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import AsyncIterator
else:
    from typing_extensions import AsyncIterator

__all__ = (
    "ListAWSServiceAccessForOrganizationPaginator",
    "ListAccountsPaginator",
    "ListAccountsForParentPaginator",
    "ListChildrenPaginator",
    "ListCreateAccountStatusPaginator",
    "ListDelegatedAdministratorsPaginator",
    "ListDelegatedServicesForAccountPaginator",
    "ListHandshakesForAccountPaginator",
    "ListHandshakesForOrganizationPaginator",
    "ListOrganizationalUnitsForParentPaginator",
    "ListParentsPaginator",
    "ListPoliciesPaginator",
    "ListPoliciesForTargetPaginator",
    "ListRootsPaginator",
    "ListTagsForResourcePaginator",
    "ListTargetsForPolicyPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListAWSServiceAccessForOrganizationPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Paginator.ListAWSServiceAccessForOrganization)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/paginators/#listawsserviceaccessfororganizationpaginator)
    """

    def paginate(
        self, *, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListAWSServiceAccessForOrganizationResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Paginator.ListAWSServiceAccessForOrganization.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/paginators/#listawsserviceaccessfororganizationpaginator)
        """

class ListAccountsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Paginator.ListAccounts)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/paginators/#listaccountspaginator)
    """

    def paginate(
        self, *, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListAccountsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Paginator.ListAccounts.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/paginators/#listaccountspaginator)
        """

class ListAccountsForParentPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Paginator.ListAccountsForParent)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/paginators/#listaccountsforparentpaginator)
    """

    def paginate(
        self, *, ParentId: str, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListAccountsForParentResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Paginator.ListAccountsForParent.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/paginators/#listaccountsforparentpaginator)
        """

class ListChildrenPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Paginator.ListChildren)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/paginators/#listchildrenpaginator)
    """

    def paginate(
        self,
        *,
        ParentId: str,
        ChildType: ChildTypeType,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListChildrenResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Paginator.ListChildren.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/paginators/#listchildrenpaginator)
        """

class ListCreateAccountStatusPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Paginator.ListCreateAccountStatus)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/paginators/#listcreateaccountstatuspaginator)
    """

    def paginate(
        self,
        *,
        States: Sequence[CreateAccountStateType] = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListCreateAccountStatusResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Paginator.ListCreateAccountStatus.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/paginators/#listcreateaccountstatuspaginator)
        """

class ListDelegatedAdministratorsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Paginator.ListDelegatedAdministrators)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/paginators/#listdelegatedadministratorspaginator)
    """

    def paginate(
        self, *, ServicePrincipal: str = ..., PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListDelegatedAdministratorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Paginator.ListDelegatedAdministrators.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/paginators/#listdelegatedadministratorspaginator)
        """

class ListDelegatedServicesForAccountPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Paginator.ListDelegatedServicesForAccount)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/paginators/#listdelegatedservicesforaccountpaginator)
    """

    def paginate(
        self, *, AccountId: str, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListDelegatedServicesForAccountResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Paginator.ListDelegatedServicesForAccount.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/paginators/#listdelegatedservicesforaccountpaginator)
        """

class ListHandshakesForAccountPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Paginator.ListHandshakesForAccount)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/paginators/#listhandshakesforaccountpaginator)
    """

    def paginate(
        self,
        *,
        Filter: "HandshakeFilterTypeDef" = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListHandshakesForAccountResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Paginator.ListHandshakesForAccount.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/paginators/#listhandshakesforaccountpaginator)
        """

class ListHandshakesForOrganizationPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Paginator.ListHandshakesForOrganization)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/paginators/#listhandshakesfororganizationpaginator)
    """

    def paginate(
        self,
        *,
        Filter: "HandshakeFilterTypeDef" = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListHandshakesForOrganizationResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Paginator.ListHandshakesForOrganization.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/paginators/#listhandshakesfororganizationpaginator)
        """

class ListOrganizationalUnitsForParentPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Paginator.ListOrganizationalUnitsForParent)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/paginators/#listorganizationalunitsforparentpaginator)
    """

    def paginate(
        self, *, ParentId: str, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListOrganizationalUnitsForParentResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Paginator.ListOrganizationalUnitsForParent.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/paginators/#listorganizationalunitsforparentpaginator)
        """

class ListParentsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Paginator.ListParents)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/paginators/#listparentspaginator)
    """

    def paginate(
        self, *, ChildId: str, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListParentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Paginator.ListParents.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/paginators/#listparentspaginator)
        """

class ListPoliciesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Paginator.ListPolicies)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/paginators/#listpoliciespaginator)
    """

    def paginate(
        self, *, Filter: PolicyTypeType, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Paginator.ListPolicies.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/paginators/#listpoliciespaginator)
        """

class ListPoliciesForTargetPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Paginator.ListPoliciesForTarget)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/paginators/#listpoliciesfortargetpaginator)
    """

    def paginate(
        self,
        *,
        TargetId: str,
        Filter: PolicyTypeType,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListPoliciesForTargetResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Paginator.ListPoliciesForTarget.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/paginators/#listpoliciesfortargetpaginator)
        """

class ListRootsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Paginator.ListRoots)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/paginators/#listrootspaginator)
    """

    def paginate(
        self, *, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListRootsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Paginator.ListRoots.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/paginators/#listrootspaginator)
        """

class ListTagsForResourcePaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Paginator.ListTagsForResource)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/paginators/#listtagsforresourcepaginator)
    """

    def paginate(
        self, *, ResourceId: str, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListTagsForResourceResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Paginator.ListTagsForResource.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/paginators/#listtagsforresourcepaginator)
        """

class ListTargetsForPolicyPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Paginator.ListTargetsForPolicy)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/paginators/#listtargetsforpolicypaginator)
    """

    def paginate(
        self, *, PolicyId: str, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListTargetsForPolicyResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Paginator.ListTargetsForPolicy.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/paginators/#listtargetsforpolicypaginator)
        """
