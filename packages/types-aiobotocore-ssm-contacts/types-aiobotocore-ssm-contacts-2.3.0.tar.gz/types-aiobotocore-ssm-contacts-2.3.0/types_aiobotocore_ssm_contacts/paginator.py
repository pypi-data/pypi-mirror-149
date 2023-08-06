"""
Type annotations for ssm-contacts service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_ssm_contacts.client import SSMContactsClient
    from types_aiobotocore_ssm_contacts.paginator import (
        ListContactChannelsPaginator,
        ListContactsPaginator,
        ListEngagementsPaginator,
        ListPageReceiptsPaginator,
        ListPagesByContactPaginator,
        ListPagesByEngagementPaginator,
    )

    session = get_session()
    with session.create_client("ssm-contacts") as client:
        client: SSMContactsClient

        list_contact_channels_paginator: ListContactChannelsPaginator = client.get_paginator("list_contact_channels")
        list_contacts_paginator: ListContactsPaginator = client.get_paginator("list_contacts")
        list_engagements_paginator: ListEngagementsPaginator = client.get_paginator("list_engagements")
        list_page_receipts_paginator: ListPageReceiptsPaginator = client.get_paginator("list_page_receipts")
        list_pages_by_contact_paginator: ListPagesByContactPaginator = client.get_paginator("list_pages_by_contact")
        list_pages_by_engagement_paginator: ListPagesByEngagementPaginator = client.get_paginator("list_pages_by_engagement")
    ```
"""
import sys
from typing import Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .literals import ContactTypeType
from .type_defs import (
    ListContactChannelsResultTypeDef,
    ListContactsResultTypeDef,
    ListEngagementsResultTypeDef,
    ListPageReceiptsResultTypeDef,
    ListPagesByContactResultTypeDef,
    ListPagesByEngagementResultTypeDef,
    PaginatorConfigTypeDef,
    TimeRangeTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import AsyncIterator
else:
    from typing_extensions import AsyncIterator


__all__ = (
    "ListContactChannelsPaginator",
    "ListContactsPaginator",
    "ListEngagementsPaginator",
    "ListPageReceiptsPaginator",
    "ListPagesByContactPaginator",
    "ListPagesByEngagementPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListContactChannelsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Paginator.ListContactChannels)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/paginators/#listcontactchannelspaginator)
    """

    def paginate(
        self, *, ContactId: str, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListContactChannelsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Paginator.ListContactChannels.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/paginators/#listcontactchannelspaginator)
        """


class ListContactsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Paginator.ListContacts)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/paginators/#listcontactspaginator)
    """

    def paginate(
        self,
        *,
        AliasPrefix: str = ...,
        Type: ContactTypeType = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListContactsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Paginator.ListContacts.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/paginators/#listcontactspaginator)
        """


class ListEngagementsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Paginator.ListEngagements)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/paginators/#listengagementspaginator)
    """

    def paginate(
        self,
        *,
        IncidentId: str = ...,
        TimeRangeValue: "TimeRangeTypeDef" = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListEngagementsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Paginator.ListEngagements.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/paginators/#listengagementspaginator)
        """


class ListPageReceiptsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Paginator.ListPageReceipts)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/paginators/#listpagereceiptspaginator)
    """

    def paginate(
        self, *, PageId: str, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListPageReceiptsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Paginator.ListPageReceipts.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/paginators/#listpagereceiptspaginator)
        """


class ListPagesByContactPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Paginator.ListPagesByContact)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/paginators/#listpagesbycontactpaginator)
    """

    def paginate(
        self, *, ContactId: str, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListPagesByContactResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Paginator.ListPagesByContact.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/paginators/#listpagesbycontactpaginator)
        """


class ListPagesByEngagementPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Paginator.ListPagesByEngagement)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/paginators/#listpagesbyengagementpaginator)
    """

    def paginate(
        self, *, EngagementId: str, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListPagesByEngagementResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Paginator.ListPagesByEngagement.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/paginators/#listpagesbyengagementpaginator)
        """
