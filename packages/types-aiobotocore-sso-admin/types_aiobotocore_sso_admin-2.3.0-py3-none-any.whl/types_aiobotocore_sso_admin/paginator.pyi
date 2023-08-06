"""
Type annotations for sso-admin service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_sso_admin.client import SSOAdminClient
    from types_aiobotocore_sso_admin.paginator import (
        ListAccountAssignmentCreationStatusPaginator,
        ListAccountAssignmentDeletionStatusPaginator,
        ListAccountAssignmentsPaginator,
        ListAccountsForProvisionedPermissionSetPaginator,
        ListInstancesPaginator,
        ListManagedPoliciesInPermissionSetPaginator,
        ListPermissionSetProvisioningStatusPaginator,
        ListPermissionSetsPaginator,
        ListPermissionSetsProvisionedToAccountPaginator,
        ListTagsForResourcePaginator,
    )

    session = get_session()
    with session.create_client("sso-admin") as client:
        client: SSOAdminClient

        list_account_assignment_creation_status_paginator: ListAccountAssignmentCreationStatusPaginator = client.get_paginator("list_account_assignment_creation_status")
        list_account_assignment_deletion_status_paginator: ListAccountAssignmentDeletionStatusPaginator = client.get_paginator("list_account_assignment_deletion_status")
        list_account_assignments_paginator: ListAccountAssignmentsPaginator = client.get_paginator("list_account_assignments")
        list_accounts_for_provisioned_permission_set_paginator: ListAccountsForProvisionedPermissionSetPaginator = client.get_paginator("list_accounts_for_provisioned_permission_set")
        list_instances_paginator: ListInstancesPaginator = client.get_paginator("list_instances")
        list_managed_policies_in_permission_set_paginator: ListManagedPoliciesInPermissionSetPaginator = client.get_paginator("list_managed_policies_in_permission_set")
        list_permission_set_provisioning_status_paginator: ListPermissionSetProvisioningStatusPaginator = client.get_paginator("list_permission_set_provisioning_status")
        list_permission_sets_paginator: ListPermissionSetsPaginator = client.get_paginator("list_permission_sets")
        list_permission_sets_provisioned_to_account_paginator: ListPermissionSetsProvisionedToAccountPaginator = client.get_paginator("list_permission_sets_provisioned_to_account")
        list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
    ```
"""
import sys
from typing import Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .literals import ProvisioningStatusType
from .type_defs import (
    ListAccountAssignmentCreationStatusResponseTypeDef,
    ListAccountAssignmentDeletionStatusResponseTypeDef,
    ListAccountAssignmentsResponseTypeDef,
    ListAccountsForProvisionedPermissionSetResponseTypeDef,
    ListInstancesResponseTypeDef,
    ListManagedPoliciesInPermissionSetResponseTypeDef,
    ListPermissionSetProvisioningStatusResponseTypeDef,
    ListPermissionSetsProvisionedToAccountResponseTypeDef,
    ListPermissionSetsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    OperationStatusFilterTypeDef,
    PaginatorConfigTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import AsyncIterator
else:
    from typing_extensions import AsyncIterator

__all__ = (
    "ListAccountAssignmentCreationStatusPaginator",
    "ListAccountAssignmentDeletionStatusPaginator",
    "ListAccountAssignmentsPaginator",
    "ListAccountsForProvisionedPermissionSetPaginator",
    "ListInstancesPaginator",
    "ListManagedPoliciesInPermissionSetPaginator",
    "ListPermissionSetProvisioningStatusPaginator",
    "ListPermissionSetsPaginator",
    "ListPermissionSetsProvisionedToAccountPaginator",
    "ListTagsForResourcePaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListAccountAssignmentCreationStatusPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Paginator.ListAccountAssignmentCreationStatus)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/paginators/#listaccountassignmentcreationstatuspaginator)
    """

    def paginate(
        self,
        *,
        InstanceArn: str,
        Filter: "OperationStatusFilterTypeDef" = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListAccountAssignmentCreationStatusResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Paginator.ListAccountAssignmentCreationStatus.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/paginators/#listaccountassignmentcreationstatuspaginator)
        """

class ListAccountAssignmentDeletionStatusPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Paginator.ListAccountAssignmentDeletionStatus)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/paginators/#listaccountassignmentdeletionstatuspaginator)
    """

    def paginate(
        self,
        *,
        InstanceArn: str,
        Filter: "OperationStatusFilterTypeDef" = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListAccountAssignmentDeletionStatusResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Paginator.ListAccountAssignmentDeletionStatus.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/paginators/#listaccountassignmentdeletionstatuspaginator)
        """

class ListAccountAssignmentsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Paginator.ListAccountAssignments)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/paginators/#listaccountassignmentspaginator)
    """

    def paginate(
        self,
        *,
        InstanceArn: str,
        AccountId: str,
        PermissionSetArn: str,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListAccountAssignmentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Paginator.ListAccountAssignments.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/paginators/#listaccountassignmentspaginator)
        """

class ListAccountsForProvisionedPermissionSetPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Paginator.ListAccountsForProvisionedPermissionSet)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/paginators/#listaccountsforprovisionedpermissionsetpaginator)
    """

    def paginate(
        self,
        *,
        InstanceArn: str,
        PermissionSetArn: str,
        ProvisioningStatus: ProvisioningStatusType = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListAccountsForProvisionedPermissionSetResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Paginator.ListAccountsForProvisionedPermissionSet.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/paginators/#listaccountsforprovisionedpermissionsetpaginator)
        """

class ListInstancesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Paginator.ListInstances)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/paginators/#listinstancespaginator)
    """

    def paginate(
        self, *, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListInstancesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Paginator.ListInstances.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/paginators/#listinstancespaginator)
        """

class ListManagedPoliciesInPermissionSetPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Paginator.ListManagedPoliciesInPermissionSet)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/paginators/#listmanagedpoliciesinpermissionsetpaginator)
    """

    def paginate(
        self,
        *,
        InstanceArn: str,
        PermissionSetArn: str,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListManagedPoliciesInPermissionSetResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Paginator.ListManagedPoliciesInPermissionSet.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/paginators/#listmanagedpoliciesinpermissionsetpaginator)
        """

class ListPermissionSetProvisioningStatusPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Paginator.ListPermissionSetProvisioningStatus)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/paginators/#listpermissionsetprovisioningstatuspaginator)
    """

    def paginate(
        self,
        *,
        InstanceArn: str,
        Filter: "OperationStatusFilterTypeDef" = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListPermissionSetProvisioningStatusResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Paginator.ListPermissionSetProvisioningStatus.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/paginators/#listpermissionsetprovisioningstatuspaginator)
        """

class ListPermissionSetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Paginator.ListPermissionSets)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/paginators/#listpermissionsetspaginator)
    """

    def paginate(
        self, *, InstanceArn: str, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListPermissionSetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Paginator.ListPermissionSets.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/paginators/#listpermissionsetspaginator)
        """

class ListPermissionSetsProvisionedToAccountPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Paginator.ListPermissionSetsProvisionedToAccount)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/paginators/#listpermissionsetsprovisionedtoaccountpaginator)
    """

    def paginate(
        self,
        *,
        InstanceArn: str,
        AccountId: str,
        ProvisioningStatus: ProvisioningStatusType = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListPermissionSetsProvisionedToAccountResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Paginator.ListPermissionSetsProvisionedToAccount.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/paginators/#listpermissionsetsprovisionedtoaccountpaginator)
        """

class ListTagsForResourcePaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Paginator.ListTagsForResource)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/paginators/#listtagsforresourcepaginator)
    """

    def paginate(
        self,
        *,
        InstanceArn: str,
        ResourceArn: str,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListTagsForResourceResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Paginator.ListTagsForResource.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/paginators/#listtagsforresourcepaginator)
        """
