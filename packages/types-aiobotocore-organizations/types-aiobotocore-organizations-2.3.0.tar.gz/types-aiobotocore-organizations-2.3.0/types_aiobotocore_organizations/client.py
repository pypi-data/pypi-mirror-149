"""
Type annotations for organizations service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_organizations.client import OrganizationsClient

    session = get_session()
    async with session.create_client("organizations") as client:
        client: OrganizationsClient
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import (
    ChildTypeType,
    CreateAccountStateType,
    EffectivePolicyTypeType,
    IAMUserAccessToBillingType,
    OrganizationFeatureSetType,
    PolicyTypeType,
)
from .paginator import (
    ListAccountsForParentPaginator,
    ListAccountsPaginator,
    ListAWSServiceAccessForOrganizationPaginator,
    ListChildrenPaginator,
    ListCreateAccountStatusPaginator,
    ListDelegatedAdministratorsPaginator,
    ListDelegatedServicesForAccountPaginator,
    ListHandshakesForAccountPaginator,
    ListHandshakesForOrganizationPaginator,
    ListOrganizationalUnitsForParentPaginator,
    ListParentsPaginator,
    ListPoliciesForTargetPaginator,
    ListPoliciesPaginator,
    ListRootsPaginator,
    ListTagsForResourcePaginator,
    ListTargetsForPolicyPaginator,
)
from .type_defs import (
    AcceptHandshakeResponseTypeDef,
    CancelHandshakeResponseTypeDef,
    CreateAccountResponseTypeDef,
    CreateGovCloudAccountResponseTypeDef,
    CreateOrganizationalUnitResponseTypeDef,
    CreateOrganizationResponseTypeDef,
    CreatePolicyResponseTypeDef,
    DeclineHandshakeResponseTypeDef,
    DescribeAccountResponseTypeDef,
    DescribeCreateAccountStatusResponseTypeDef,
    DescribeEffectivePolicyResponseTypeDef,
    DescribeHandshakeResponseTypeDef,
    DescribeOrganizationalUnitResponseTypeDef,
    DescribeOrganizationResponseTypeDef,
    DescribePolicyResponseTypeDef,
    DisablePolicyTypeResponseTypeDef,
    EnableAllFeaturesResponseTypeDef,
    EnablePolicyTypeResponseTypeDef,
    HandshakeFilterTypeDef,
    HandshakePartyTypeDef,
    InviteAccountToOrganizationResponseTypeDef,
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
    TagTypeDef,
    UpdateOrganizationalUnitResponseTypeDef,
    UpdatePolicyResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("OrganizationsClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AWSOrganizationsNotInUseException: Type[BotocoreClientError]
    AccessDeniedException: Type[BotocoreClientError]
    AccessDeniedForDependencyException: Type[BotocoreClientError]
    AccountAlreadyRegisteredException: Type[BotocoreClientError]
    AccountNotFoundException: Type[BotocoreClientError]
    AccountNotRegisteredException: Type[BotocoreClientError]
    AccountOwnerNotVerifiedException: Type[BotocoreClientError]
    AlreadyInOrganizationException: Type[BotocoreClientError]
    ChildNotFoundException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConcurrentModificationException: Type[BotocoreClientError]
    ConstraintViolationException: Type[BotocoreClientError]
    CreateAccountStatusNotFoundException: Type[BotocoreClientError]
    DestinationParentNotFoundException: Type[BotocoreClientError]
    DuplicateAccountException: Type[BotocoreClientError]
    DuplicateHandshakeException: Type[BotocoreClientError]
    DuplicateOrganizationalUnitException: Type[BotocoreClientError]
    DuplicatePolicyAttachmentException: Type[BotocoreClientError]
    DuplicatePolicyException: Type[BotocoreClientError]
    EffectivePolicyNotFoundException: Type[BotocoreClientError]
    FinalizingOrganizationException: Type[BotocoreClientError]
    HandshakeAlreadyInStateException: Type[BotocoreClientError]
    HandshakeConstraintViolationException: Type[BotocoreClientError]
    HandshakeNotFoundException: Type[BotocoreClientError]
    InvalidHandshakeTransitionException: Type[BotocoreClientError]
    InvalidInputException: Type[BotocoreClientError]
    MalformedPolicyDocumentException: Type[BotocoreClientError]
    MasterCannotLeaveOrganizationException: Type[BotocoreClientError]
    OrganizationNotEmptyException: Type[BotocoreClientError]
    OrganizationalUnitNotEmptyException: Type[BotocoreClientError]
    OrganizationalUnitNotFoundException: Type[BotocoreClientError]
    ParentNotFoundException: Type[BotocoreClientError]
    PolicyChangesInProgressException: Type[BotocoreClientError]
    PolicyInUseException: Type[BotocoreClientError]
    PolicyNotAttachedException: Type[BotocoreClientError]
    PolicyNotFoundException: Type[BotocoreClientError]
    PolicyTypeAlreadyEnabledException: Type[BotocoreClientError]
    PolicyTypeNotAvailableForOrganizationException: Type[BotocoreClientError]
    PolicyTypeNotEnabledException: Type[BotocoreClientError]
    RootNotFoundException: Type[BotocoreClientError]
    ServiceException: Type[BotocoreClientError]
    SourceParentNotFoundException: Type[BotocoreClientError]
    TargetNotFoundException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]
    UnsupportedAPIEndpointException: Type[BotocoreClientError]


class OrganizationsClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        OrganizationsClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/#exceptions)
        """

    async def accept_handshake(self, *, HandshakeId: str) -> AcceptHandshakeResponseTypeDef:
        """
        Sends a response to the originator of a handshake agreeing to the action
        proposed by the handshake request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.accept_handshake)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/#accept_handshake)
        """

    async def attach_policy(self, *, PolicyId: str, TargetId: str) -> None:
        """
        Attaches a policy to a root, an organizational unit (OU), or an individual
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.attach_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/#attach_policy)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/#can_paginate)
        """

    async def cancel_handshake(self, *, HandshakeId: str) -> CancelHandshakeResponseTypeDef:
        """
        Cancels a handshake.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.cancel_handshake)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/#cancel_handshake)
        """

    async def create_account(
        self,
        *,
        Email: str,
        AccountName: str,
        RoleName: str = ...,
        IamUserAccessToBilling: IAMUserAccessToBillingType = ...,
        Tags: Sequence["TagTypeDef"] = ...
    ) -> CreateAccountResponseTypeDef:
        """
        Creates an AWS account that is automatically a member of the organization whose
        credentials made the request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.create_account)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/#create_account)
        """

    async def create_gov_cloud_account(
        self,
        *,
        Email: str,
        AccountName: str,
        RoleName: str = ...,
        IamUserAccessToBilling: IAMUserAccessToBillingType = ...,
        Tags: Sequence["TagTypeDef"] = ...
    ) -> CreateGovCloudAccountResponseTypeDef:
        """
        This action is available if all of the following are true * You're authorized to
        create accounts in the AWS GovCloud (US) Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.create_gov_cloud_account)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/#create_gov_cloud_account)
        """

    async def create_organization(
        self, *, FeatureSet: OrganizationFeatureSetType = ...
    ) -> CreateOrganizationResponseTypeDef:
        """
        Creates an AWS organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.create_organization)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/#create_organization)
        """

    async def create_organizational_unit(
        self, *, ParentId: str, Name: str, Tags: Sequence["TagTypeDef"] = ...
    ) -> CreateOrganizationalUnitResponseTypeDef:
        """
        Creates an organizational unit (OU) within a root or parent OU.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.create_organizational_unit)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/#create_organizational_unit)
        """

    async def create_policy(
        self,
        *,
        Content: str,
        Description: str,
        Name: str,
        Type: PolicyTypeType,
        Tags: Sequence["TagTypeDef"] = ...
    ) -> CreatePolicyResponseTypeDef:
        """
        Creates a policy of a specified type that you can attach to a root, an
        organizational unit (OU), or an individual AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.create_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/#create_policy)
        """

    async def decline_handshake(self, *, HandshakeId: str) -> DeclineHandshakeResponseTypeDef:
        """
        Declines a handshake request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.decline_handshake)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/#decline_handshake)
        """

    async def delete_organization(self) -> None:
        """
        Deletes the organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.delete_organization)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/#delete_organization)
        """

    async def delete_organizational_unit(self, *, OrganizationalUnitId: str) -> None:
        """
        Deletes an organizational unit (OU) from a root or another OU.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.delete_organizational_unit)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/#delete_organizational_unit)
        """

    async def delete_policy(self, *, PolicyId: str) -> None:
        """
        Deletes the specified policy from your organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.delete_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/#delete_policy)
        """

    async def deregister_delegated_administrator(
        self, *, AccountId: str, ServicePrincipal: str
    ) -> None:
        """
        Removes the specified member AWS account as a delegated administrator for the
        specified AWS service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.deregister_delegated_administrator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/#deregister_delegated_administrator)
        """

    async def describe_account(self, *, AccountId: str) -> DescribeAccountResponseTypeDef:
        """
        Retrieves AWS Organizations-related information about the specified account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.describe_account)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/#describe_account)
        """

    async def describe_create_account_status(
        self, *, CreateAccountRequestId: str
    ) -> DescribeCreateAccountStatusResponseTypeDef:
        """
        Retrieves the current status of an asynchronous request to create an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.describe_create_account_status)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/#describe_create_account_status)
        """

    async def describe_effective_policy(
        self, *, PolicyType: EffectivePolicyTypeType, TargetId: str = ...
    ) -> DescribeEffectivePolicyResponseTypeDef:
        """
        Returns the contents of the effective policy for specified policy type and
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.describe_effective_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/#describe_effective_policy)
        """

    async def describe_handshake(self, *, HandshakeId: str) -> DescribeHandshakeResponseTypeDef:
        """
        Retrieves information about a previously requested handshake.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.describe_handshake)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/#describe_handshake)
        """

    async def describe_organization(self) -> DescribeOrganizationResponseTypeDef:
        """
        Retrieves information about the organization that the user's account belongs to.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.describe_organization)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/#describe_organization)
        """

    async def describe_organizational_unit(
        self, *, OrganizationalUnitId: str
    ) -> DescribeOrganizationalUnitResponseTypeDef:
        """
        Retrieves information about an organizational unit (OU).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.describe_organizational_unit)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/#describe_organizational_unit)
        """

    async def describe_policy(self, *, PolicyId: str) -> DescribePolicyResponseTypeDef:
        """
        Retrieves information about a policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.describe_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/#describe_policy)
        """

    async def detach_policy(self, *, PolicyId: str, TargetId: str) -> None:
        """
        Detaches a policy from a target root, organizational unit (OU), or account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.detach_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/#detach_policy)
        """

    async def disable_aws_service_access(self, *, ServicePrincipal: str) -> None:
        """
        Disables the integration of an AWS service (the service that is specified by
        `ServicePrincipal` ) with AWS Organizations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.disable_aws_service_access)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/#disable_aws_service_access)
        """

    async def disable_policy_type(
        self, *, RootId: str, PolicyType: PolicyTypeType
    ) -> DisablePolicyTypeResponseTypeDef:
        """
        Disables an organizational policy type in a root.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.disable_policy_type)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/#disable_policy_type)
        """

    async def enable_all_features(self) -> EnableAllFeaturesResponseTypeDef:
        """
        Enables all features in an organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.enable_all_features)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/#enable_all_features)
        """

    async def enable_aws_service_access(self, *, ServicePrincipal: str) -> None:
        """
        Enables the integration of an AWS service (the service that is specified by
        `ServicePrincipal` ) with AWS Organizations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.enable_aws_service_access)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/#enable_aws_service_access)
        """

    async def enable_policy_type(
        self, *, RootId: str, PolicyType: PolicyTypeType
    ) -> EnablePolicyTypeResponseTypeDef:
        """
        Enables a policy type in a root.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.enable_policy_type)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/#enable_policy_type)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/#generate_presigned_url)
        """

    async def invite_account_to_organization(
        self,
        *,
        Target: "HandshakePartyTypeDef",
        Notes: str = ...,
        Tags: Sequence["TagTypeDef"] = ...
    ) -> InviteAccountToOrganizationResponseTypeDef:
        """
        Sends an invitation to another account to join your organization as a member
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.invite_account_to_organization)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/#invite_account_to_organization)
        """

    async def leave_organization(self) -> None:
        """
        Removes a member account from its parent organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.leave_organization)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/#leave_organization)
        """

    async def list_accounts(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> ListAccountsResponseTypeDef:
        """
        Lists all the accounts in the organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.list_accounts)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/#list_accounts)
        """

    async def list_accounts_for_parent(
        self, *, ParentId: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListAccountsForParentResponseTypeDef:
        """
        Lists the accounts in an organization that are contained by the specified target
        root or organizational unit (OU).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.list_accounts_for_parent)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/#list_accounts_for_parent)
        """

    async def list_aws_service_access_for_organization(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> ListAWSServiceAccessForOrganizationResponseTypeDef:
        """
        Returns a list of the AWS services that you enabled to integrate with your
        organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.list_aws_service_access_for_organization)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/#list_aws_service_access_for_organization)
        """

    async def list_children(
        self,
        *,
        ParentId: str,
        ChildType: ChildTypeType,
        NextToken: str = ...,
        MaxResults: int = ...
    ) -> ListChildrenResponseTypeDef:
        """
        Lists all of the organizational units (OUs) or accounts that are contained in
        the specified parent OU or root.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.list_children)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/#list_children)
        """

    async def list_create_account_status(
        self,
        *,
        States: Sequence[CreateAccountStateType] = ...,
        NextToken: str = ...,
        MaxResults: int = ...
    ) -> ListCreateAccountStatusResponseTypeDef:
        """
        Lists the account creation requests that match the specified status that is
        currently being tracked for the organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.list_create_account_status)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/#list_create_account_status)
        """

    async def list_delegated_administrators(
        self, *, ServicePrincipal: str = ..., NextToken: str = ..., MaxResults: int = ...
    ) -> ListDelegatedAdministratorsResponseTypeDef:
        """
        Lists the AWS accounts that are designated as delegated administrators in this
        organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.list_delegated_administrators)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/#list_delegated_administrators)
        """

    async def list_delegated_services_for_account(
        self, *, AccountId: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListDelegatedServicesForAccountResponseTypeDef:
        """
        List the AWS services for which the specified account is a delegated
        administrator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.list_delegated_services_for_account)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/#list_delegated_services_for_account)
        """

    async def list_handshakes_for_account(
        self, *, Filter: "HandshakeFilterTypeDef" = ..., NextToken: str = ..., MaxResults: int = ...
    ) -> ListHandshakesForAccountResponseTypeDef:
        """
        Lists the current handshakes that are associated with the account of the
        requesting user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.list_handshakes_for_account)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/#list_handshakes_for_account)
        """

    async def list_handshakes_for_organization(
        self, *, Filter: "HandshakeFilterTypeDef" = ..., NextToken: str = ..., MaxResults: int = ...
    ) -> ListHandshakesForOrganizationResponseTypeDef:
        """
        Lists the handshakes that are associated with the organization that the
        requesting user is part of.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.list_handshakes_for_organization)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/#list_handshakes_for_organization)
        """

    async def list_organizational_units_for_parent(
        self, *, ParentId: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListOrganizationalUnitsForParentResponseTypeDef:
        """
        Lists the organizational units (OUs) in a parent organizational unit or root.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.list_organizational_units_for_parent)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/#list_organizational_units_for_parent)
        """

    async def list_parents(
        self, *, ChildId: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListParentsResponseTypeDef:
        """
        Lists the root or organizational units (OUs) that serve as the immediate parent
        of the specified child OU or account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.list_parents)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/#list_parents)
        """

    async def list_policies(
        self, *, Filter: PolicyTypeType, NextToken: str = ..., MaxResults: int = ...
    ) -> ListPoliciesResponseTypeDef:
        """
        Retrieves the list of all policies in an organization of a specified type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.list_policies)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/#list_policies)
        """

    async def list_policies_for_target(
        self, *, TargetId: str, Filter: PolicyTypeType, NextToken: str = ..., MaxResults: int = ...
    ) -> ListPoliciesForTargetResponseTypeDef:
        """
        Lists the policies that are directly attached to the specified target root,
        organizational unit (OU), or account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.list_policies_for_target)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/#list_policies_for_target)
        """

    async def list_roots(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> ListRootsResponseTypeDef:
        """
        Lists the roots that are defined in the current organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.list_roots)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/#list_roots)
        """

    async def list_tags_for_resource(
        self, *, ResourceId: str, NextToken: str = ...
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists tags that are attached to the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/#list_tags_for_resource)
        """

    async def list_targets_for_policy(
        self, *, PolicyId: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListTargetsForPolicyResponseTypeDef:
        """
        Lists all the roots, organizational units (OUs), and accounts that the specified
        policy is attached to.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.list_targets_for_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/#list_targets_for_policy)
        """

    async def move_account(
        self, *, AccountId: str, SourceParentId: str, DestinationParentId: str
    ) -> None:
        """
        Moves an account from its current source parent root or organizational unit (OU)
        to the specified destination parent root or OU.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.move_account)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/#move_account)
        """

    async def register_delegated_administrator(
        self, *, AccountId: str, ServicePrincipal: str
    ) -> None:
        """
        Enables the specified member account to administer the Organizations features of
        the specified AWS service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.register_delegated_administrator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/#register_delegated_administrator)
        """

    async def remove_account_from_organization(self, *, AccountId: str) -> None:
        """
        Removes the specified account from the organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.remove_account_from_organization)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/#remove_account_from_organization)
        """

    async def tag_resource(self, *, ResourceId: str, Tags: Sequence["TagTypeDef"]) -> None:
        """
        Adds one or more tags to the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/#tag_resource)
        """

    async def untag_resource(self, *, ResourceId: str, TagKeys: Sequence[str]) -> None:
        """
        Removes any tags with the specified keys from the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/#untag_resource)
        """

    async def update_organizational_unit(
        self, *, OrganizationalUnitId: str, Name: str = ...
    ) -> UpdateOrganizationalUnitResponseTypeDef:
        """
        Renames the specified organizational unit (OU).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.update_organizational_unit)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/#update_organizational_unit)
        """

    async def update_policy(
        self, *, PolicyId: str, Name: str = ..., Description: str = ..., Content: str = ...
    ) -> UpdatePolicyResponseTypeDef:
        """
        Updates an existing policy with a new name, description, or content.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.update_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/#update_policy)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_aws_service_access_for_organization"]
    ) -> ListAWSServiceAccessForOrganizationPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_accounts"]) -> ListAccountsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_accounts_for_parent"]
    ) -> ListAccountsForParentPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_children"]) -> ListChildrenPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_create_account_status"]
    ) -> ListCreateAccountStatusPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_delegated_administrators"]
    ) -> ListDelegatedAdministratorsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_delegated_services_for_account"]
    ) -> ListDelegatedServicesForAccountPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_handshakes_for_account"]
    ) -> ListHandshakesForAccountPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_handshakes_for_organization"]
    ) -> ListHandshakesForOrganizationPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_organizational_units_for_parent"]
    ) -> ListOrganizationalUnitsForParentPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_parents"]) -> ListParentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_policies"]) -> ListPoliciesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_policies_for_target"]
    ) -> ListPoliciesForTargetPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_roots"]) -> ListRootsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_tags_for_resource"]
    ) -> ListTagsForResourcePaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_targets_for_policy"]
    ) -> ListTargetsForPolicyPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/#get_paginator)
        """

    async def __aenter__(self) -> "OrganizationsClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_organizations/client/)
        """
