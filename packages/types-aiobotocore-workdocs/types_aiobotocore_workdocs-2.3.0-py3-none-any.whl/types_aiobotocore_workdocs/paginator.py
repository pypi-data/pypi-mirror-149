"""
Type annotations for workdocs service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_workdocs.client import WorkDocsClient
    from types_aiobotocore_workdocs.paginator import (
        DescribeActivitiesPaginator,
        DescribeCommentsPaginator,
        DescribeDocumentVersionsPaginator,
        DescribeFolderContentsPaginator,
        DescribeGroupsPaginator,
        DescribeNotificationSubscriptionsPaginator,
        DescribeResourcePermissionsPaginator,
        DescribeRootFoldersPaginator,
        DescribeUsersPaginator,
    )

    session = get_session()
    with session.create_client("workdocs") as client:
        client: WorkDocsClient

        describe_activities_paginator: DescribeActivitiesPaginator = client.get_paginator("describe_activities")
        describe_comments_paginator: DescribeCommentsPaginator = client.get_paginator("describe_comments")
        describe_document_versions_paginator: DescribeDocumentVersionsPaginator = client.get_paginator("describe_document_versions")
        describe_folder_contents_paginator: DescribeFolderContentsPaginator = client.get_paginator("describe_folder_contents")
        describe_groups_paginator: DescribeGroupsPaginator = client.get_paginator("describe_groups")
        describe_notification_subscriptions_paginator: DescribeNotificationSubscriptionsPaginator = client.get_paginator("describe_notification_subscriptions")
        describe_resource_permissions_paginator: DescribeResourcePermissionsPaginator = client.get_paginator("describe_resource_permissions")
        describe_root_folders_paginator: DescribeRootFoldersPaginator = client.get_paginator("describe_root_folders")
        describe_users_paginator: DescribeUsersPaginator = client.get_paginator("describe_users")
    ```
"""
import sys
from datetime import datetime
from typing import Generic, Iterator, TypeVar, Union

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .literals import (
    FolderContentTypeType,
    OrderTypeType,
    ResourceSortTypeType,
    UserFilterTypeType,
    UserSortTypeType,
)
from .type_defs import (
    DescribeActivitiesResponseTypeDef,
    DescribeCommentsResponseTypeDef,
    DescribeDocumentVersionsResponseTypeDef,
    DescribeFolderContentsResponseTypeDef,
    DescribeGroupsResponseTypeDef,
    DescribeNotificationSubscriptionsResponseTypeDef,
    DescribeResourcePermissionsResponseTypeDef,
    DescribeRootFoldersResponseTypeDef,
    DescribeUsersResponseTypeDef,
    PaginatorConfigTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import AsyncIterator
else:
    from typing_extensions import AsyncIterator


__all__ = (
    "DescribeActivitiesPaginator",
    "DescribeCommentsPaginator",
    "DescribeDocumentVersionsPaginator",
    "DescribeFolderContentsPaginator",
    "DescribeGroupsPaginator",
    "DescribeNotificationSubscriptionsPaginator",
    "DescribeResourcePermissionsPaginator",
    "DescribeRootFoldersPaginator",
    "DescribeUsersPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeActivitiesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Paginator.DescribeActivities)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/paginators/#describeactivitiespaginator)
    """

    def paginate(
        self,
        *,
        AuthenticationToken: str = ...,
        StartTime: Union[datetime, str] = ...,
        EndTime: Union[datetime, str] = ...,
        OrganizationId: str = ...,
        ActivityTypes: str = ...,
        ResourceId: str = ...,
        UserId: str = ...,
        IncludeIndirectActivities: bool = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DescribeActivitiesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Paginator.DescribeActivities.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/paginators/#describeactivitiespaginator)
        """


class DescribeCommentsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Paginator.DescribeComments)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/paginators/#describecommentspaginator)
    """

    def paginate(
        self,
        *,
        DocumentId: str,
        VersionId: str,
        AuthenticationToken: str = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DescribeCommentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Paginator.DescribeComments.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/paginators/#describecommentspaginator)
        """


class DescribeDocumentVersionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Paginator.DescribeDocumentVersions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/paginators/#describedocumentversionspaginator)
    """

    def paginate(
        self,
        *,
        DocumentId: str,
        AuthenticationToken: str = ...,
        Include: str = ...,
        Fields: str = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DescribeDocumentVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Paginator.DescribeDocumentVersions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/paginators/#describedocumentversionspaginator)
        """


class DescribeFolderContentsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Paginator.DescribeFolderContents)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/paginators/#describefoldercontentspaginator)
    """

    def paginate(
        self,
        *,
        FolderId: str,
        AuthenticationToken: str = ...,
        Sort: ResourceSortTypeType = ...,
        Order: OrderTypeType = ...,
        Type: FolderContentTypeType = ...,
        Include: str = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DescribeFolderContentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Paginator.DescribeFolderContents.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/paginators/#describefoldercontentspaginator)
        """


class DescribeGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Paginator.DescribeGroups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/paginators/#describegroupspaginator)
    """

    def paginate(
        self,
        *,
        SearchQuery: str,
        AuthenticationToken: str = ...,
        OrganizationId: str = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DescribeGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Paginator.DescribeGroups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/paginators/#describegroupspaginator)
        """


class DescribeNotificationSubscriptionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Paginator.DescribeNotificationSubscriptions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/paginators/#describenotificationsubscriptionspaginator)
    """

    def paginate(
        self, *, OrganizationId: str, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DescribeNotificationSubscriptionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Paginator.DescribeNotificationSubscriptions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/paginators/#describenotificationsubscriptionspaginator)
        """


class DescribeResourcePermissionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Paginator.DescribeResourcePermissions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/paginators/#describeresourcepermissionspaginator)
    """

    def paginate(
        self,
        *,
        ResourceId: str,
        AuthenticationToken: str = ...,
        PrincipalId: str = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DescribeResourcePermissionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Paginator.DescribeResourcePermissions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/paginators/#describeresourcepermissionspaginator)
        """


class DescribeRootFoldersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Paginator.DescribeRootFolders)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/paginators/#describerootfolderspaginator)
    """

    def paginate(
        self, *, AuthenticationToken: str, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DescribeRootFoldersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Paginator.DescribeRootFolders.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/paginators/#describerootfolderspaginator)
        """


class DescribeUsersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Paginator.DescribeUsers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/paginators/#describeuserspaginator)
    """

    def paginate(
        self,
        *,
        AuthenticationToken: str = ...,
        OrganizationId: str = ...,
        UserIds: str = ...,
        Query: str = ...,
        Include: UserFilterTypeType = ...,
        Order: OrderTypeType = ...,
        Sort: UserSortTypeType = ...,
        Fields: str = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DescribeUsersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Paginator.DescribeUsers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/paginators/#describeuserspaginator)
        """
