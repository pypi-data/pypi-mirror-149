"""
Type annotations for ram service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ram/type_defs/)

Usage::

    ```python
    from mypy_boto3_ram.type_defs import AcceptResourceShareInvitationRequestRequestTypeDef

    data: AcceptResourceShareInvitationRequestRequestTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence

from .literals import (
    ResourceOwnerType,
    ResourceRegionScopeFilterType,
    ResourceRegionScopeType,
    ResourceShareAssociationStatusType,
    ResourceShareAssociationTypeType,
    ResourceShareFeatureSetType,
    ResourceShareInvitationStatusType,
    ResourceShareStatusType,
    ResourceStatusType,
)

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "AcceptResourceShareInvitationRequestRequestTypeDef",
    "AcceptResourceShareInvitationResponseTypeDef",
    "AssociateResourceSharePermissionRequestRequestTypeDef",
    "AssociateResourceSharePermissionResponseTypeDef",
    "AssociateResourceShareRequestRequestTypeDef",
    "AssociateResourceShareResponseTypeDef",
    "CreateResourceShareRequestRequestTypeDef",
    "CreateResourceShareResponseTypeDef",
    "DeleteResourceShareRequestRequestTypeDef",
    "DeleteResourceShareResponseTypeDef",
    "DisassociateResourceSharePermissionRequestRequestTypeDef",
    "DisassociateResourceSharePermissionResponseTypeDef",
    "DisassociateResourceShareRequestRequestTypeDef",
    "DisassociateResourceShareResponseTypeDef",
    "EnableSharingWithAwsOrganizationResponseTypeDef",
    "GetPermissionRequestRequestTypeDef",
    "GetPermissionResponseTypeDef",
    "GetResourcePoliciesRequestGetResourcePoliciesPaginateTypeDef",
    "GetResourcePoliciesRequestRequestTypeDef",
    "GetResourcePoliciesResponseTypeDef",
    "GetResourceShareAssociationsRequestGetResourceShareAssociationsPaginateTypeDef",
    "GetResourceShareAssociationsRequestRequestTypeDef",
    "GetResourceShareAssociationsResponseTypeDef",
    "GetResourceShareInvitationsRequestGetResourceShareInvitationsPaginateTypeDef",
    "GetResourceShareInvitationsRequestRequestTypeDef",
    "GetResourceShareInvitationsResponseTypeDef",
    "GetResourceSharesRequestGetResourceSharesPaginateTypeDef",
    "GetResourceSharesRequestRequestTypeDef",
    "GetResourceSharesResponseTypeDef",
    "ListPendingInvitationResourcesRequestRequestTypeDef",
    "ListPendingInvitationResourcesResponseTypeDef",
    "ListPermissionVersionsRequestRequestTypeDef",
    "ListPermissionVersionsResponseTypeDef",
    "ListPermissionsRequestRequestTypeDef",
    "ListPermissionsResponseTypeDef",
    "ListPrincipalsRequestListPrincipalsPaginateTypeDef",
    "ListPrincipalsRequestRequestTypeDef",
    "ListPrincipalsResponseTypeDef",
    "ListResourceSharePermissionsRequestRequestTypeDef",
    "ListResourceSharePermissionsResponseTypeDef",
    "ListResourceTypesRequestRequestTypeDef",
    "ListResourceTypesResponseTypeDef",
    "ListResourcesRequestListResourcesPaginateTypeDef",
    "ListResourcesRequestRequestTypeDef",
    "ListResourcesResponseTypeDef",
    "PaginatorConfigTypeDef",
    "PrincipalTypeDef",
    "PromoteResourceShareCreatedFromPolicyRequestRequestTypeDef",
    "PromoteResourceShareCreatedFromPolicyResponseTypeDef",
    "RejectResourceShareInvitationRequestRequestTypeDef",
    "RejectResourceShareInvitationResponseTypeDef",
    "ResourceShareAssociationTypeDef",
    "ResourceShareInvitationTypeDef",
    "ResourceSharePermissionDetailTypeDef",
    "ResourceSharePermissionSummaryTypeDef",
    "ResourceShareTypeDef",
    "ResourceTypeDef",
    "ResponseMetadataTypeDef",
    "ServiceNameAndResourceTypeTypeDef",
    "TagFilterTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateResourceShareRequestRequestTypeDef",
    "UpdateResourceShareResponseTypeDef",
)

_RequiredAcceptResourceShareInvitationRequestRequestTypeDef = TypedDict(
    "_RequiredAcceptResourceShareInvitationRequestRequestTypeDef",
    {
        "resourceShareInvitationArn": str,
    },
)
_OptionalAcceptResourceShareInvitationRequestRequestTypeDef = TypedDict(
    "_OptionalAcceptResourceShareInvitationRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class AcceptResourceShareInvitationRequestRequestTypeDef(
    _RequiredAcceptResourceShareInvitationRequestRequestTypeDef,
    _OptionalAcceptResourceShareInvitationRequestRequestTypeDef,
):
    pass


AcceptResourceShareInvitationResponseTypeDef = TypedDict(
    "AcceptResourceShareInvitationResponseTypeDef",
    {
        "resourceShareInvitation": "ResourceShareInvitationTypeDef",
        "clientToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredAssociateResourceSharePermissionRequestRequestTypeDef = TypedDict(
    "_RequiredAssociateResourceSharePermissionRequestRequestTypeDef",
    {
        "resourceShareArn": str,
        "permissionArn": str,
    },
)
_OptionalAssociateResourceSharePermissionRequestRequestTypeDef = TypedDict(
    "_OptionalAssociateResourceSharePermissionRequestRequestTypeDef",
    {
        "replace": bool,
        "clientToken": str,
        "permissionVersion": int,
    },
    total=False,
)


class AssociateResourceSharePermissionRequestRequestTypeDef(
    _RequiredAssociateResourceSharePermissionRequestRequestTypeDef,
    _OptionalAssociateResourceSharePermissionRequestRequestTypeDef,
):
    pass


AssociateResourceSharePermissionResponseTypeDef = TypedDict(
    "AssociateResourceSharePermissionResponseTypeDef",
    {
        "returnValue": bool,
        "clientToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredAssociateResourceShareRequestRequestTypeDef = TypedDict(
    "_RequiredAssociateResourceShareRequestRequestTypeDef",
    {
        "resourceShareArn": str,
    },
)
_OptionalAssociateResourceShareRequestRequestTypeDef = TypedDict(
    "_OptionalAssociateResourceShareRequestRequestTypeDef",
    {
        "resourceArns": Sequence[str],
        "principals": Sequence[str],
        "clientToken": str,
    },
    total=False,
)


class AssociateResourceShareRequestRequestTypeDef(
    _RequiredAssociateResourceShareRequestRequestTypeDef,
    _OptionalAssociateResourceShareRequestRequestTypeDef,
):
    pass


AssociateResourceShareResponseTypeDef = TypedDict(
    "AssociateResourceShareResponseTypeDef",
    {
        "resourceShareAssociations": List["ResourceShareAssociationTypeDef"],
        "clientToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateResourceShareRequestRequestTypeDef = TypedDict(
    "_RequiredCreateResourceShareRequestRequestTypeDef",
    {
        "name": str,
    },
)
_OptionalCreateResourceShareRequestRequestTypeDef = TypedDict(
    "_OptionalCreateResourceShareRequestRequestTypeDef",
    {
        "resourceArns": Sequence[str],
        "principals": Sequence[str],
        "tags": Sequence["TagTypeDef"],
        "allowExternalPrincipals": bool,
        "clientToken": str,
        "permissionArns": Sequence[str],
    },
    total=False,
)


class CreateResourceShareRequestRequestTypeDef(
    _RequiredCreateResourceShareRequestRequestTypeDef,
    _OptionalCreateResourceShareRequestRequestTypeDef,
):
    pass


CreateResourceShareResponseTypeDef = TypedDict(
    "CreateResourceShareResponseTypeDef",
    {
        "resourceShare": "ResourceShareTypeDef",
        "clientToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredDeleteResourceShareRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteResourceShareRequestRequestTypeDef",
    {
        "resourceShareArn": str,
    },
)
_OptionalDeleteResourceShareRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteResourceShareRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class DeleteResourceShareRequestRequestTypeDef(
    _RequiredDeleteResourceShareRequestRequestTypeDef,
    _OptionalDeleteResourceShareRequestRequestTypeDef,
):
    pass


DeleteResourceShareResponseTypeDef = TypedDict(
    "DeleteResourceShareResponseTypeDef",
    {
        "returnValue": bool,
        "clientToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredDisassociateResourceSharePermissionRequestRequestTypeDef = TypedDict(
    "_RequiredDisassociateResourceSharePermissionRequestRequestTypeDef",
    {
        "resourceShareArn": str,
        "permissionArn": str,
    },
)
_OptionalDisassociateResourceSharePermissionRequestRequestTypeDef = TypedDict(
    "_OptionalDisassociateResourceSharePermissionRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class DisassociateResourceSharePermissionRequestRequestTypeDef(
    _RequiredDisassociateResourceSharePermissionRequestRequestTypeDef,
    _OptionalDisassociateResourceSharePermissionRequestRequestTypeDef,
):
    pass


DisassociateResourceSharePermissionResponseTypeDef = TypedDict(
    "DisassociateResourceSharePermissionResponseTypeDef",
    {
        "returnValue": bool,
        "clientToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredDisassociateResourceShareRequestRequestTypeDef = TypedDict(
    "_RequiredDisassociateResourceShareRequestRequestTypeDef",
    {
        "resourceShareArn": str,
    },
)
_OptionalDisassociateResourceShareRequestRequestTypeDef = TypedDict(
    "_OptionalDisassociateResourceShareRequestRequestTypeDef",
    {
        "resourceArns": Sequence[str],
        "principals": Sequence[str],
        "clientToken": str,
    },
    total=False,
)


class DisassociateResourceShareRequestRequestTypeDef(
    _RequiredDisassociateResourceShareRequestRequestTypeDef,
    _OptionalDisassociateResourceShareRequestRequestTypeDef,
):
    pass


DisassociateResourceShareResponseTypeDef = TypedDict(
    "DisassociateResourceShareResponseTypeDef",
    {
        "resourceShareAssociations": List["ResourceShareAssociationTypeDef"],
        "clientToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

EnableSharingWithAwsOrganizationResponseTypeDef = TypedDict(
    "EnableSharingWithAwsOrganizationResponseTypeDef",
    {
        "returnValue": bool,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredGetPermissionRequestRequestTypeDef = TypedDict(
    "_RequiredGetPermissionRequestRequestTypeDef",
    {
        "permissionArn": str,
    },
)
_OptionalGetPermissionRequestRequestTypeDef = TypedDict(
    "_OptionalGetPermissionRequestRequestTypeDef",
    {
        "permissionVersion": int,
    },
    total=False,
)


class GetPermissionRequestRequestTypeDef(
    _RequiredGetPermissionRequestRequestTypeDef, _OptionalGetPermissionRequestRequestTypeDef
):
    pass


GetPermissionResponseTypeDef = TypedDict(
    "GetPermissionResponseTypeDef",
    {
        "permission": "ResourceSharePermissionDetailTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredGetResourcePoliciesRequestGetResourcePoliciesPaginateTypeDef = TypedDict(
    "_RequiredGetResourcePoliciesRequestGetResourcePoliciesPaginateTypeDef",
    {
        "resourceArns": Sequence[str],
    },
)
_OptionalGetResourcePoliciesRequestGetResourcePoliciesPaginateTypeDef = TypedDict(
    "_OptionalGetResourcePoliciesRequestGetResourcePoliciesPaginateTypeDef",
    {
        "principal": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class GetResourcePoliciesRequestGetResourcePoliciesPaginateTypeDef(
    _RequiredGetResourcePoliciesRequestGetResourcePoliciesPaginateTypeDef,
    _OptionalGetResourcePoliciesRequestGetResourcePoliciesPaginateTypeDef,
):
    pass


_RequiredGetResourcePoliciesRequestRequestTypeDef = TypedDict(
    "_RequiredGetResourcePoliciesRequestRequestTypeDef",
    {
        "resourceArns": Sequence[str],
    },
)
_OptionalGetResourcePoliciesRequestRequestTypeDef = TypedDict(
    "_OptionalGetResourcePoliciesRequestRequestTypeDef",
    {
        "principal": str,
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class GetResourcePoliciesRequestRequestTypeDef(
    _RequiredGetResourcePoliciesRequestRequestTypeDef,
    _OptionalGetResourcePoliciesRequestRequestTypeDef,
):
    pass


GetResourcePoliciesResponseTypeDef = TypedDict(
    "GetResourcePoliciesResponseTypeDef",
    {
        "policies": List[str],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredGetResourceShareAssociationsRequestGetResourceShareAssociationsPaginateTypeDef = TypedDict(
    "_RequiredGetResourceShareAssociationsRequestGetResourceShareAssociationsPaginateTypeDef",
    {
        "associationType": ResourceShareAssociationTypeType,
    },
)
_OptionalGetResourceShareAssociationsRequestGetResourceShareAssociationsPaginateTypeDef = TypedDict(
    "_OptionalGetResourceShareAssociationsRequestGetResourceShareAssociationsPaginateTypeDef",
    {
        "resourceShareArns": Sequence[str],
        "resourceArn": str,
        "principal": str,
        "associationStatus": ResourceShareAssociationStatusType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class GetResourceShareAssociationsRequestGetResourceShareAssociationsPaginateTypeDef(
    _RequiredGetResourceShareAssociationsRequestGetResourceShareAssociationsPaginateTypeDef,
    _OptionalGetResourceShareAssociationsRequestGetResourceShareAssociationsPaginateTypeDef,
):
    pass


_RequiredGetResourceShareAssociationsRequestRequestTypeDef = TypedDict(
    "_RequiredGetResourceShareAssociationsRequestRequestTypeDef",
    {
        "associationType": ResourceShareAssociationTypeType,
    },
)
_OptionalGetResourceShareAssociationsRequestRequestTypeDef = TypedDict(
    "_OptionalGetResourceShareAssociationsRequestRequestTypeDef",
    {
        "resourceShareArns": Sequence[str],
        "resourceArn": str,
        "principal": str,
        "associationStatus": ResourceShareAssociationStatusType,
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class GetResourceShareAssociationsRequestRequestTypeDef(
    _RequiredGetResourceShareAssociationsRequestRequestTypeDef,
    _OptionalGetResourceShareAssociationsRequestRequestTypeDef,
):
    pass


GetResourceShareAssociationsResponseTypeDef = TypedDict(
    "GetResourceShareAssociationsResponseTypeDef",
    {
        "resourceShareAssociations": List["ResourceShareAssociationTypeDef"],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetResourceShareInvitationsRequestGetResourceShareInvitationsPaginateTypeDef = TypedDict(
    "GetResourceShareInvitationsRequestGetResourceShareInvitationsPaginateTypeDef",
    {
        "resourceShareInvitationArns": Sequence[str],
        "resourceShareArns": Sequence[str],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

GetResourceShareInvitationsRequestRequestTypeDef = TypedDict(
    "GetResourceShareInvitationsRequestRequestTypeDef",
    {
        "resourceShareInvitationArns": Sequence[str],
        "resourceShareArns": Sequence[str],
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

GetResourceShareInvitationsResponseTypeDef = TypedDict(
    "GetResourceShareInvitationsResponseTypeDef",
    {
        "resourceShareInvitations": List["ResourceShareInvitationTypeDef"],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredGetResourceSharesRequestGetResourceSharesPaginateTypeDef = TypedDict(
    "_RequiredGetResourceSharesRequestGetResourceSharesPaginateTypeDef",
    {
        "resourceOwner": ResourceOwnerType,
    },
)
_OptionalGetResourceSharesRequestGetResourceSharesPaginateTypeDef = TypedDict(
    "_OptionalGetResourceSharesRequestGetResourceSharesPaginateTypeDef",
    {
        "resourceShareArns": Sequence[str],
        "resourceShareStatus": ResourceShareStatusType,
        "name": str,
        "tagFilters": Sequence["TagFilterTypeDef"],
        "permissionArn": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class GetResourceSharesRequestGetResourceSharesPaginateTypeDef(
    _RequiredGetResourceSharesRequestGetResourceSharesPaginateTypeDef,
    _OptionalGetResourceSharesRequestGetResourceSharesPaginateTypeDef,
):
    pass


_RequiredGetResourceSharesRequestRequestTypeDef = TypedDict(
    "_RequiredGetResourceSharesRequestRequestTypeDef",
    {
        "resourceOwner": ResourceOwnerType,
    },
)
_OptionalGetResourceSharesRequestRequestTypeDef = TypedDict(
    "_OptionalGetResourceSharesRequestRequestTypeDef",
    {
        "resourceShareArns": Sequence[str],
        "resourceShareStatus": ResourceShareStatusType,
        "name": str,
        "tagFilters": Sequence["TagFilterTypeDef"],
        "nextToken": str,
        "maxResults": int,
        "permissionArn": str,
    },
    total=False,
)


class GetResourceSharesRequestRequestTypeDef(
    _RequiredGetResourceSharesRequestRequestTypeDef, _OptionalGetResourceSharesRequestRequestTypeDef
):
    pass


GetResourceSharesResponseTypeDef = TypedDict(
    "GetResourceSharesResponseTypeDef",
    {
        "resourceShares": List["ResourceShareTypeDef"],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredListPendingInvitationResourcesRequestRequestTypeDef = TypedDict(
    "_RequiredListPendingInvitationResourcesRequestRequestTypeDef",
    {
        "resourceShareInvitationArn": str,
    },
)
_OptionalListPendingInvitationResourcesRequestRequestTypeDef = TypedDict(
    "_OptionalListPendingInvitationResourcesRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
        "resourceRegionScope": ResourceRegionScopeFilterType,
    },
    total=False,
)


class ListPendingInvitationResourcesRequestRequestTypeDef(
    _RequiredListPendingInvitationResourcesRequestRequestTypeDef,
    _OptionalListPendingInvitationResourcesRequestRequestTypeDef,
):
    pass


ListPendingInvitationResourcesResponseTypeDef = TypedDict(
    "ListPendingInvitationResourcesResponseTypeDef",
    {
        "resources": List["ResourceTypeDef"],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredListPermissionVersionsRequestRequestTypeDef = TypedDict(
    "_RequiredListPermissionVersionsRequestRequestTypeDef",
    {
        "permissionArn": str,
    },
)
_OptionalListPermissionVersionsRequestRequestTypeDef = TypedDict(
    "_OptionalListPermissionVersionsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class ListPermissionVersionsRequestRequestTypeDef(
    _RequiredListPermissionVersionsRequestRequestTypeDef,
    _OptionalListPermissionVersionsRequestRequestTypeDef,
):
    pass


ListPermissionVersionsResponseTypeDef = TypedDict(
    "ListPermissionVersionsResponseTypeDef",
    {
        "permissions": List["ResourceSharePermissionSummaryTypeDef"],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListPermissionsRequestRequestTypeDef = TypedDict(
    "ListPermissionsRequestRequestTypeDef",
    {
        "resourceType": str,
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

ListPermissionsResponseTypeDef = TypedDict(
    "ListPermissionsResponseTypeDef",
    {
        "permissions": List["ResourceSharePermissionSummaryTypeDef"],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredListPrincipalsRequestListPrincipalsPaginateTypeDef = TypedDict(
    "_RequiredListPrincipalsRequestListPrincipalsPaginateTypeDef",
    {
        "resourceOwner": ResourceOwnerType,
    },
)
_OptionalListPrincipalsRequestListPrincipalsPaginateTypeDef = TypedDict(
    "_OptionalListPrincipalsRequestListPrincipalsPaginateTypeDef",
    {
        "resourceArn": str,
        "principals": Sequence[str],
        "resourceType": str,
        "resourceShareArns": Sequence[str],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListPrincipalsRequestListPrincipalsPaginateTypeDef(
    _RequiredListPrincipalsRequestListPrincipalsPaginateTypeDef,
    _OptionalListPrincipalsRequestListPrincipalsPaginateTypeDef,
):
    pass


_RequiredListPrincipalsRequestRequestTypeDef = TypedDict(
    "_RequiredListPrincipalsRequestRequestTypeDef",
    {
        "resourceOwner": ResourceOwnerType,
    },
)
_OptionalListPrincipalsRequestRequestTypeDef = TypedDict(
    "_OptionalListPrincipalsRequestRequestTypeDef",
    {
        "resourceArn": str,
        "principals": Sequence[str],
        "resourceType": str,
        "resourceShareArns": Sequence[str],
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class ListPrincipalsRequestRequestTypeDef(
    _RequiredListPrincipalsRequestRequestTypeDef, _OptionalListPrincipalsRequestRequestTypeDef
):
    pass


ListPrincipalsResponseTypeDef = TypedDict(
    "ListPrincipalsResponseTypeDef",
    {
        "principals": List["PrincipalTypeDef"],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredListResourceSharePermissionsRequestRequestTypeDef = TypedDict(
    "_RequiredListResourceSharePermissionsRequestRequestTypeDef",
    {
        "resourceShareArn": str,
    },
)
_OptionalListResourceSharePermissionsRequestRequestTypeDef = TypedDict(
    "_OptionalListResourceSharePermissionsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class ListResourceSharePermissionsRequestRequestTypeDef(
    _RequiredListResourceSharePermissionsRequestRequestTypeDef,
    _OptionalListResourceSharePermissionsRequestRequestTypeDef,
):
    pass


ListResourceSharePermissionsResponseTypeDef = TypedDict(
    "ListResourceSharePermissionsResponseTypeDef",
    {
        "permissions": List["ResourceSharePermissionSummaryTypeDef"],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListResourceTypesRequestRequestTypeDef = TypedDict(
    "ListResourceTypesRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
        "resourceRegionScope": ResourceRegionScopeFilterType,
    },
    total=False,
)

ListResourceTypesResponseTypeDef = TypedDict(
    "ListResourceTypesResponseTypeDef",
    {
        "resourceTypes": List["ServiceNameAndResourceTypeTypeDef"],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredListResourcesRequestListResourcesPaginateTypeDef = TypedDict(
    "_RequiredListResourcesRequestListResourcesPaginateTypeDef",
    {
        "resourceOwner": ResourceOwnerType,
    },
)
_OptionalListResourcesRequestListResourcesPaginateTypeDef = TypedDict(
    "_OptionalListResourcesRequestListResourcesPaginateTypeDef",
    {
        "principal": str,
        "resourceType": str,
        "resourceArns": Sequence[str],
        "resourceShareArns": Sequence[str],
        "resourceRegionScope": ResourceRegionScopeFilterType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListResourcesRequestListResourcesPaginateTypeDef(
    _RequiredListResourcesRequestListResourcesPaginateTypeDef,
    _OptionalListResourcesRequestListResourcesPaginateTypeDef,
):
    pass


_RequiredListResourcesRequestRequestTypeDef = TypedDict(
    "_RequiredListResourcesRequestRequestTypeDef",
    {
        "resourceOwner": ResourceOwnerType,
    },
)
_OptionalListResourcesRequestRequestTypeDef = TypedDict(
    "_OptionalListResourcesRequestRequestTypeDef",
    {
        "principal": str,
        "resourceType": str,
        "resourceArns": Sequence[str],
        "resourceShareArns": Sequence[str],
        "nextToken": str,
        "maxResults": int,
        "resourceRegionScope": ResourceRegionScopeFilterType,
    },
    total=False,
)


class ListResourcesRequestRequestTypeDef(
    _RequiredListResourcesRequestRequestTypeDef, _OptionalListResourcesRequestRequestTypeDef
):
    pass


ListResourcesResponseTypeDef = TypedDict(
    "ListResourcesResponseTypeDef",
    {
        "resources": List["ResourceTypeDef"],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": int,
        "PageSize": int,
        "StartingToken": str,
    },
    total=False,
)

PrincipalTypeDef = TypedDict(
    "PrincipalTypeDef",
    {
        "id": str,
        "resourceShareArn": str,
        "creationTime": datetime,
        "lastUpdatedTime": datetime,
        "external": bool,
    },
    total=False,
)

PromoteResourceShareCreatedFromPolicyRequestRequestTypeDef = TypedDict(
    "PromoteResourceShareCreatedFromPolicyRequestRequestTypeDef",
    {
        "resourceShareArn": str,
    },
)

PromoteResourceShareCreatedFromPolicyResponseTypeDef = TypedDict(
    "PromoteResourceShareCreatedFromPolicyResponseTypeDef",
    {
        "returnValue": bool,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredRejectResourceShareInvitationRequestRequestTypeDef = TypedDict(
    "_RequiredRejectResourceShareInvitationRequestRequestTypeDef",
    {
        "resourceShareInvitationArn": str,
    },
)
_OptionalRejectResourceShareInvitationRequestRequestTypeDef = TypedDict(
    "_OptionalRejectResourceShareInvitationRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class RejectResourceShareInvitationRequestRequestTypeDef(
    _RequiredRejectResourceShareInvitationRequestRequestTypeDef,
    _OptionalRejectResourceShareInvitationRequestRequestTypeDef,
):
    pass


RejectResourceShareInvitationResponseTypeDef = TypedDict(
    "RejectResourceShareInvitationResponseTypeDef",
    {
        "resourceShareInvitation": "ResourceShareInvitationTypeDef",
        "clientToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ResourceShareAssociationTypeDef = TypedDict(
    "ResourceShareAssociationTypeDef",
    {
        "resourceShareArn": str,
        "resourceShareName": str,
        "associatedEntity": str,
        "associationType": ResourceShareAssociationTypeType,
        "status": ResourceShareAssociationStatusType,
        "statusMessage": str,
        "creationTime": datetime,
        "lastUpdatedTime": datetime,
        "external": bool,
    },
    total=False,
)

ResourceShareInvitationTypeDef = TypedDict(
    "ResourceShareInvitationTypeDef",
    {
        "resourceShareInvitationArn": str,
        "resourceShareName": str,
        "resourceShareArn": str,
        "senderAccountId": str,
        "receiverAccountId": str,
        "invitationTimestamp": datetime,
        "status": ResourceShareInvitationStatusType,
        "resourceShareAssociations": List["ResourceShareAssociationTypeDef"],
        "receiverArn": str,
    },
    total=False,
)

ResourceSharePermissionDetailTypeDef = TypedDict(
    "ResourceSharePermissionDetailTypeDef",
    {
        "arn": str,
        "version": str,
        "defaultVersion": bool,
        "name": str,
        "resourceType": str,
        "permission": str,
        "creationTime": datetime,
        "lastUpdatedTime": datetime,
        "isResourceTypeDefault": bool,
    },
    total=False,
)

ResourceSharePermissionSummaryTypeDef = TypedDict(
    "ResourceSharePermissionSummaryTypeDef",
    {
        "arn": str,
        "version": str,
        "defaultVersion": bool,
        "name": str,
        "resourceType": str,
        "status": str,
        "creationTime": datetime,
        "lastUpdatedTime": datetime,
        "isResourceTypeDefault": bool,
    },
    total=False,
)

ResourceShareTypeDef = TypedDict(
    "ResourceShareTypeDef",
    {
        "resourceShareArn": str,
        "name": str,
        "owningAccountId": str,
        "allowExternalPrincipals": bool,
        "status": ResourceShareStatusType,
        "statusMessage": str,
        "tags": List["TagTypeDef"],
        "creationTime": datetime,
        "lastUpdatedTime": datetime,
        "featureSet": ResourceShareFeatureSetType,
    },
    total=False,
)

ResourceTypeDef = TypedDict(
    "ResourceTypeDef",
    {
        "arn": str,
        "type": str,
        "resourceShareArn": str,
        "resourceGroupArn": str,
        "status": ResourceStatusType,
        "statusMessage": str,
        "creationTime": datetime,
        "lastUpdatedTime": datetime,
        "resourceRegionScope": ResourceRegionScopeType,
    },
    total=False,
)

ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HostId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
    },
)

ServiceNameAndResourceTypeTypeDef = TypedDict(
    "ServiceNameAndResourceTypeTypeDef",
    {
        "resourceType": str,
        "serviceName": str,
        "resourceRegionScope": ResourceRegionScopeType,
    },
    total=False,
)

TagFilterTypeDef = TypedDict(
    "TagFilterTypeDef",
    {
        "tagKey": str,
        "tagValues": Sequence[str],
    },
    total=False,
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "resourceShareArn": str,
        "tags": Sequence["TagTypeDef"],
    },
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "key": str,
        "value": str,
    },
    total=False,
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "resourceShareArn": str,
        "tagKeys": Sequence[str],
    },
)

_RequiredUpdateResourceShareRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateResourceShareRequestRequestTypeDef",
    {
        "resourceShareArn": str,
    },
)
_OptionalUpdateResourceShareRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateResourceShareRequestRequestTypeDef",
    {
        "name": str,
        "allowExternalPrincipals": bool,
        "clientToken": str,
    },
    total=False,
)


class UpdateResourceShareRequestRequestTypeDef(
    _RequiredUpdateResourceShareRequestRequestTypeDef,
    _OptionalUpdateResourceShareRequestRequestTypeDef,
):
    pass


UpdateResourceShareResponseTypeDef = TypedDict(
    "UpdateResourceShareResponseTypeDef",
    {
        "resourceShare": "ResourceShareTypeDef",
        "clientToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)
