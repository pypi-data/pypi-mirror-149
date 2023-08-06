"""
Type annotations for ssm-contacts service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_ssm_contacts.client import SSMContactsClient

    session = get_session()
    async with session.create_client("ssm-contacts") as client:
        client: SSMContactsClient
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import AcceptCodeValidationType, AcceptTypeType, ChannelTypeType, ContactTypeType
from .paginator import (
    ListContactChannelsPaginator,
    ListContactsPaginator,
    ListEngagementsPaginator,
    ListPageReceiptsPaginator,
    ListPagesByContactPaginator,
    ListPagesByEngagementPaginator,
)
from .type_defs import (
    ContactChannelAddressTypeDef,
    CreateContactChannelResultTypeDef,
    CreateContactResultTypeDef,
    DescribeEngagementResultTypeDef,
    DescribePageResultTypeDef,
    GetContactChannelResultTypeDef,
    GetContactPolicyResultTypeDef,
    GetContactResultTypeDef,
    ListContactChannelsResultTypeDef,
    ListContactsResultTypeDef,
    ListEngagementsResultTypeDef,
    ListPageReceiptsResultTypeDef,
    ListPagesByContactResultTypeDef,
    ListPagesByEngagementResultTypeDef,
    ListTagsForResourceResultTypeDef,
    PlanTypeDef,
    StartEngagementResultTypeDef,
    TagTypeDef,
    TimeRangeTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("SSMContactsClient",)

class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    DataEncryptionException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class SSMContactsClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SSMContactsClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/client/#exceptions)
        """
    async def accept_page(
        self,
        *,
        PageId: str,
        AcceptType: AcceptTypeType,
        AcceptCode: str,
        ContactChannelId: str = ...,
        Note: str = ...,
        AcceptCodeValidation: AcceptCodeValidationType = ...
    ) -> Dict[str, Any]:
        """
        Used to acknowledge an engagement to a contact channel during an incident.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.accept_page)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/client/#accept_page)
        """
    async def activate_contact_channel(
        self, *, ContactChannelId: str, ActivationCode: str
    ) -> Dict[str, Any]:
        """
        Activates a contact's contact channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.activate_contact_channel)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/client/#activate_contact_channel)
        """
    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/client/#can_paginate)
        """
    async def create_contact(
        self,
        *,
        Alias: str,
        Type: ContactTypeType,
        Plan: "PlanTypeDef",
        DisplayName: str = ...,
        Tags: Sequence["TagTypeDef"] = ...,
        IdempotencyToken: str = ...
    ) -> CreateContactResultTypeDef:
        """
        Contacts are either the contacts that Incident Manager engages during an
        incident or the escalation plans that Incident Manager uses to engage contacts
        in phases during an incident.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.create_contact)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/client/#create_contact)
        """
    async def create_contact_channel(
        self,
        *,
        ContactId: str,
        Name: str,
        Type: ChannelTypeType,
        DeliveryAddress: "ContactChannelAddressTypeDef",
        DeferActivation: bool = ...,
        IdempotencyToken: str = ...
    ) -> CreateContactChannelResultTypeDef:
        """
        A contact channel is the method that Incident Manager uses to engage your
        contact.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.create_contact_channel)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/client/#create_contact_channel)
        """
    async def deactivate_contact_channel(self, *, ContactChannelId: str) -> Dict[str, Any]:
        """
        To no longer receive Incident Manager engagements to a contact channel, you can
        deactivate the channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.deactivate_contact_channel)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/client/#deactivate_contact_channel)
        """
    async def delete_contact(self, *, ContactId: str) -> Dict[str, Any]:
        """
        To remove a contact from Incident Manager, you can delete the contact.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.delete_contact)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/client/#delete_contact)
        """
    async def delete_contact_channel(self, *, ContactChannelId: str) -> Dict[str, Any]:
        """
        To no longer receive engagements on a contact channel, you can delete the
        channel from a contact.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.delete_contact_channel)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/client/#delete_contact_channel)
        """
    async def describe_engagement(self, *, EngagementId: str) -> DescribeEngagementResultTypeDef:
        """
        Incident Manager uses engagements to engage contacts and escalation plans during
        an incident.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.describe_engagement)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/client/#describe_engagement)
        """
    async def describe_page(self, *, PageId: str) -> DescribePageResultTypeDef:
        """
        Lists details of the engagement to a contact channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.describe_page)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/client/#describe_page)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/client/#generate_presigned_url)
        """
    async def get_contact(self, *, ContactId: str) -> GetContactResultTypeDef:
        """
        Retrieves information about the specified contact or escalation plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.get_contact)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/client/#get_contact)
        """
    async def get_contact_channel(self, *, ContactChannelId: str) -> GetContactChannelResultTypeDef:
        """
        List details about a specific contact channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.get_contact_channel)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/client/#get_contact_channel)
        """
    async def get_contact_policy(self, *, ContactArn: str) -> GetContactPolicyResultTypeDef:
        """
        Retrieves the resource policies attached to the specified contact or escalation
        plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.get_contact_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/client/#get_contact_policy)
        """
    async def list_contact_channels(
        self, *, ContactId: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListContactChannelsResultTypeDef:
        """
        Lists all contact channels for the specified contact.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.list_contact_channels)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/client/#list_contact_channels)
        """
    async def list_contacts(
        self,
        *,
        NextToken: str = ...,
        MaxResults: int = ...,
        AliasPrefix: str = ...,
        Type: ContactTypeType = ...
    ) -> ListContactsResultTypeDef:
        """
        Lists all contacts and escalation plans in Incident Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.list_contacts)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/client/#list_contacts)
        """
    async def list_engagements(
        self,
        *,
        NextToken: str = ...,
        MaxResults: int = ...,
        IncidentId: str = ...,
        TimeRangeValue: "TimeRangeTypeDef" = ...
    ) -> ListEngagementsResultTypeDef:
        """
        Lists all engagements that have happened in an incident.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.list_engagements)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/client/#list_engagements)
        """
    async def list_page_receipts(
        self, *, PageId: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListPageReceiptsResultTypeDef:
        """
        Lists all of the engagements to contact channels that have been acknowledged.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.list_page_receipts)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/client/#list_page_receipts)
        """
    async def list_pages_by_contact(
        self, *, ContactId: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListPagesByContactResultTypeDef:
        """
        Lists the engagements to a contact's contact channels.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.list_pages_by_contact)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/client/#list_pages_by_contact)
        """
    async def list_pages_by_engagement(
        self, *, EngagementId: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListPagesByEngagementResultTypeDef:
        """
        Lists the engagements to contact channels that occurred by engaging a contact.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.list_pages_by_engagement)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/client/#list_pages_by_engagement)
        """
    async def list_tags_for_resource(self, *, ResourceARN: str) -> ListTagsForResourceResultTypeDef:
        """
        Lists the tags of an escalation plan or contact.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/client/#list_tags_for_resource)
        """
    async def put_contact_policy(self, *, ContactArn: str, Policy: str) -> Dict[str, Any]:
        """
        Adds a resource to the specified contact or escalation plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.put_contact_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/client/#put_contact_policy)
        """
    async def send_activation_code(self, *, ContactChannelId: str) -> Dict[str, Any]:
        """
        Sends an activation code to a contact channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.send_activation_code)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/client/#send_activation_code)
        """
    async def start_engagement(
        self,
        *,
        ContactId: str,
        Sender: str,
        Subject: str,
        Content: str,
        PublicSubject: str = ...,
        PublicContent: str = ...,
        IncidentId: str = ...,
        IdempotencyToken: str = ...
    ) -> StartEngagementResultTypeDef:
        """
        Starts an engagement to a contact or escalation plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.start_engagement)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/client/#start_engagement)
        """
    async def stop_engagement(self, *, EngagementId: str, Reason: str = ...) -> Dict[str, Any]:
        """
        Stops an engagement before it finishes the final stage of the escalation plan or
        engagement plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.stop_engagement)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/client/#stop_engagement)
        """
    async def tag_resource(
        self, *, ResourceARN: str, Tags: Sequence["TagTypeDef"]
    ) -> Dict[str, Any]:
        """
        Tags a contact or escalation plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/client/#tag_resource)
        """
    async def untag_resource(self, *, ResourceARN: str, TagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes tags from the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/client/#untag_resource)
        """
    async def update_contact(
        self, *, ContactId: str, DisplayName: str = ..., Plan: "PlanTypeDef" = ...
    ) -> Dict[str, Any]:
        """
        Updates the contact or escalation plan specified.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.update_contact)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/client/#update_contact)
        """
    async def update_contact_channel(
        self,
        *,
        ContactChannelId: str,
        Name: str = ...,
        DeliveryAddress: "ContactChannelAddressTypeDef" = ...
    ) -> Dict[str, Any]:
        """
        Updates a contact's contact channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.update_contact_channel)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/client/#update_contact_channel)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_contact_channels"]
    ) -> ListContactChannelsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/client/#get_paginator)
        """
    @overload
    def get_paginator(self, operation_name: Literal["list_contacts"]) -> ListContactsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_engagements"]
    ) -> ListEngagementsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_page_receipts"]
    ) -> ListPageReceiptsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_pages_by_contact"]
    ) -> ListPagesByContactPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_pages_by_engagement"]
    ) -> ListPagesByEngagementPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/client/#get_paginator)
        """
    async def __aenter__(self) -> "SSMContactsClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/client/)
        """
    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-contacts.html#SSMContacts.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_contacts/client/)
        """
