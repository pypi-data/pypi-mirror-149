"""
Type annotations for ram service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_ram.client import RAMClient
    from types_aiobotocore_ram.paginator import (
        GetResourcePoliciesPaginator,
        GetResourceShareAssociationsPaginator,
        GetResourceShareInvitationsPaginator,
        GetResourceSharesPaginator,
        ListPrincipalsPaginator,
        ListResourcesPaginator,
    )

    session = get_session()
    with session.create_client("ram") as client:
        client: RAMClient

        get_resource_policies_paginator: GetResourcePoliciesPaginator = client.get_paginator("get_resource_policies")
        get_resource_share_associations_paginator: GetResourceShareAssociationsPaginator = client.get_paginator("get_resource_share_associations")
        get_resource_share_invitations_paginator: GetResourceShareInvitationsPaginator = client.get_paginator("get_resource_share_invitations")
        get_resource_shares_paginator: GetResourceSharesPaginator = client.get_paginator("get_resource_shares")
        list_principals_paginator: ListPrincipalsPaginator = client.get_paginator("list_principals")
        list_resources_paginator: ListResourcesPaginator = client.get_paginator("list_resources")
    ```
"""
import sys
from typing import Generic, Iterator, Sequence, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .literals import (
    ResourceOwnerType,
    ResourceRegionScopeFilterType,
    ResourceShareAssociationStatusType,
    ResourceShareAssociationTypeType,
    ResourceShareStatusType,
)
from .type_defs import (
    GetResourcePoliciesResponseTypeDef,
    GetResourceShareAssociationsResponseTypeDef,
    GetResourceShareInvitationsResponseTypeDef,
    GetResourceSharesResponseTypeDef,
    ListPrincipalsResponseTypeDef,
    ListResourcesResponseTypeDef,
    PaginatorConfigTypeDef,
    TagFilterTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import AsyncIterator
else:
    from typing_extensions import AsyncIterator


__all__ = (
    "GetResourcePoliciesPaginator",
    "GetResourceShareAssociationsPaginator",
    "GetResourceShareInvitationsPaginator",
    "GetResourceSharesPaginator",
    "ListPrincipalsPaginator",
    "ListResourcesPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class GetResourcePoliciesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram.html#RAM.Paginator.GetResourcePolicies)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/paginators/#getresourcepoliciespaginator)
    """

    def paginate(
        self,
        *,
        resourceArns: Sequence[str],
        principal: str = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[GetResourcePoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram.html#RAM.Paginator.GetResourcePolicies.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/paginators/#getresourcepoliciespaginator)
        """


class GetResourceShareAssociationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram.html#RAM.Paginator.GetResourceShareAssociations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/paginators/#getresourceshareassociationspaginator)
    """

    def paginate(
        self,
        *,
        associationType: ResourceShareAssociationTypeType,
        resourceShareArns: Sequence[str] = ...,
        resourceArn: str = ...,
        principal: str = ...,
        associationStatus: ResourceShareAssociationStatusType = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[GetResourceShareAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram.html#RAM.Paginator.GetResourceShareAssociations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/paginators/#getresourceshareassociationspaginator)
        """


class GetResourceShareInvitationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram.html#RAM.Paginator.GetResourceShareInvitations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/paginators/#getresourceshareinvitationspaginator)
    """

    def paginate(
        self,
        *,
        resourceShareInvitationArns: Sequence[str] = ...,
        resourceShareArns: Sequence[str] = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[GetResourceShareInvitationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram.html#RAM.Paginator.GetResourceShareInvitations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/paginators/#getresourceshareinvitationspaginator)
        """


class GetResourceSharesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram.html#RAM.Paginator.GetResourceShares)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/paginators/#getresourcesharespaginator)
    """

    def paginate(
        self,
        *,
        resourceOwner: ResourceOwnerType,
        resourceShareArns: Sequence[str] = ...,
        resourceShareStatus: ResourceShareStatusType = ...,
        name: str = ...,
        tagFilters: Sequence["TagFilterTypeDef"] = ...,
        permissionArn: str = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[GetResourceSharesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram.html#RAM.Paginator.GetResourceShares.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/paginators/#getresourcesharespaginator)
        """


class ListPrincipalsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram.html#RAM.Paginator.ListPrincipals)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/paginators/#listprincipalspaginator)
    """

    def paginate(
        self,
        *,
        resourceOwner: ResourceOwnerType,
        resourceArn: str = ...,
        principals: Sequence[str] = ...,
        resourceType: str = ...,
        resourceShareArns: Sequence[str] = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListPrincipalsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram.html#RAM.Paginator.ListPrincipals.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/paginators/#listprincipalspaginator)
        """


class ListResourcesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram.html#RAM.Paginator.ListResources)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/paginators/#listresourcespaginator)
    """

    def paginate(
        self,
        *,
        resourceOwner: ResourceOwnerType,
        principal: str = ...,
        resourceType: str = ...,
        resourceArns: Sequence[str] = ...,
        resourceShareArns: Sequence[str] = ...,
        resourceRegionScope: ResourceRegionScopeFilterType = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListResourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram.html#RAM.Paginator.ListResources.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/paginators/#listresourcespaginator)
        """
