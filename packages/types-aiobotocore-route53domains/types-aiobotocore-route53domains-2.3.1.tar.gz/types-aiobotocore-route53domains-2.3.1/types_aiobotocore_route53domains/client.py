"""
Type annotations for route53domains service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_route53domains.client import Route53DomainsClient

    session = get_session()
    async with session.create_client("route53domains") as client:
        client: Route53DomainsClient
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, Mapping, Sequence, Type, Union, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import (
    ListDomainsPaginator,
    ListOperationsPaginator,
    ListPricesPaginator,
    ViewBillingPaginator,
)
from .type_defs import (
    AcceptDomainTransferFromAnotherAwsAccountResponseTypeDef,
    CancelDomainTransferToAnotherAwsAccountResponseTypeDef,
    CheckDomainAvailabilityResponseTypeDef,
    CheckDomainTransferabilityResponseTypeDef,
    ContactDetailTypeDef,
    DeleteDomainResponseTypeDef,
    DisableDomainTransferLockResponseTypeDef,
    EnableDomainTransferLockResponseTypeDef,
    FilterConditionTypeDef,
    GetContactReachabilityStatusResponseTypeDef,
    GetDomainDetailResponseTypeDef,
    GetDomainSuggestionsResponseTypeDef,
    GetOperationDetailResponseTypeDef,
    ListDomainsResponseTypeDef,
    ListOperationsResponseTypeDef,
    ListPricesResponseTypeDef,
    ListTagsForDomainResponseTypeDef,
    NameserverTypeDef,
    RegisterDomainResponseTypeDef,
    RejectDomainTransferFromAnotherAwsAccountResponseTypeDef,
    RenewDomainResponseTypeDef,
    ResendContactReachabilityEmailResponseTypeDef,
    RetrieveDomainAuthCodeResponseTypeDef,
    SortConditionTypeDef,
    TagTypeDef,
    TransferDomainResponseTypeDef,
    TransferDomainToAnotherAwsAccountResponseTypeDef,
    UpdateDomainContactPrivacyResponseTypeDef,
    UpdateDomainContactResponseTypeDef,
    UpdateDomainNameserversResponseTypeDef,
    ViewBillingResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("Route53DomainsClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    DomainLimitExceeded: Type[BotocoreClientError]
    DuplicateRequest: Type[BotocoreClientError]
    InvalidInput: Type[BotocoreClientError]
    OperationLimitExceeded: Type[BotocoreClientError]
    TLDRulesViolation: Type[BotocoreClientError]
    UnsupportedTLD: Type[BotocoreClientError]


class Route53DomainsClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains.html#Route53Domains.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        Route53DomainsClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains.html#Route53Domains.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#exceptions)
        """

    async def accept_domain_transfer_from_another_aws_account(
        self, *, DomainName: str, Password: str
    ) -> AcceptDomainTransferFromAnotherAwsAccountResponseTypeDef:
        """
        Accepts the transfer of a domain from another Amazon Web Services account to the
        currentAmazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains.html#Route53Domains.Client.accept_domain_transfer_from_another_aws_account)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#accept_domain_transfer_from_another_aws_account)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains.html#Route53Domains.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#can_paginate)
        """

    async def cancel_domain_transfer_to_another_aws_account(
        self, *, DomainName: str
    ) -> CancelDomainTransferToAnotherAwsAccountResponseTypeDef:
        """
        Cancels the transfer of a domain from the current Amazon Web Services account to
        another Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains.html#Route53Domains.Client.cancel_domain_transfer_to_another_aws_account)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#cancel_domain_transfer_to_another_aws_account)
        """

    async def check_domain_availability(
        self, *, DomainName: str, IdnLangCode: str = ...
    ) -> CheckDomainAvailabilityResponseTypeDef:
        """
        This operation checks the availability of one domain name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains.html#Route53Domains.Client.check_domain_availability)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#check_domain_availability)
        """

    async def check_domain_transferability(
        self, *, DomainName: str, AuthCode: str = ...
    ) -> CheckDomainTransferabilityResponseTypeDef:
        """
        Checks whether a domain name can be transferred to Amazon Route 53.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains.html#Route53Domains.Client.check_domain_transferability)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#check_domain_transferability)
        """

    async def delete_domain(self, *, DomainName: str) -> DeleteDomainResponseTypeDef:
        """
        This operation deletes the specified domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains.html#Route53Domains.Client.delete_domain)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#delete_domain)
        """

    async def delete_tags_for_domain(
        self, *, DomainName: str, TagsToDelete: Sequence[str]
    ) -> Dict[str, Any]:
        """
        This operation deletes the specified tags for a domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains.html#Route53Domains.Client.delete_tags_for_domain)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#delete_tags_for_domain)
        """

    async def disable_domain_auto_renew(self, *, DomainName: str) -> Dict[str, Any]:
        """
        This operation disables automatic renewal of domain registration for the
        specified domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains.html#Route53Domains.Client.disable_domain_auto_renew)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#disable_domain_auto_renew)
        """

    async def disable_domain_transfer_lock(
        self, *, DomainName: str
    ) -> DisableDomainTransferLockResponseTypeDef:
        """
        This operation removes the transfer lock on the domain (specifically the
        `clientTransferProhibited` status) to allow domain transfers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains.html#Route53Domains.Client.disable_domain_transfer_lock)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#disable_domain_transfer_lock)
        """

    async def enable_domain_auto_renew(self, *, DomainName: str) -> Dict[str, Any]:
        """
        This operation configures Amazon Route 53 to automatically renew the specified
        domain before the domain registration expires.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains.html#Route53Domains.Client.enable_domain_auto_renew)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#enable_domain_auto_renew)
        """

    async def enable_domain_transfer_lock(
        self, *, DomainName: str
    ) -> EnableDomainTransferLockResponseTypeDef:
        """
        This operation sets the transfer lock on the domain (specifically the
        `clientTransferProhibited` status) to prevent domain transfers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains.html#Route53Domains.Client.enable_domain_transfer_lock)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#enable_domain_transfer_lock)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains.html#Route53Domains.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#generate_presigned_url)
        """

    async def get_contact_reachability_status(
        self, *, domainName: str = ...
    ) -> GetContactReachabilityStatusResponseTypeDef:
        """
        For operations that require confirmation that the email address for the
        registrant contact is valid, such as registering a new domain, this operation
        returns information about whether the registrant contact has responded.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains.html#Route53Domains.Client.get_contact_reachability_status)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#get_contact_reachability_status)
        """

    async def get_domain_detail(self, *, DomainName: str) -> GetDomainDetailResponseTypeDef:
        """
        This operation returns detailed information about a specified domain that is
        associated with the current Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains.html#Route53Domains.Client.get_domain_detail)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#get_domain_detail)
        """

    async def get_domain_suggestions(
        self, *, DomainName: str, SuggestionCount: int, OnlyAvailable: bool
    ) -> GetDomainSuggestionsResponseTypeDef:
        """
        The GetDomainSuggestions operation returns a list of suggested domain names.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains.html#Route53Domains.Client.get_domain_suggestions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#get_domain_suggestions)
        """

    async def get_operation_detail(self, *, OperationId: str) -> GetOperationDetailResponseTypeDef:
        """
        This operation returns the current status of an operation that is not completed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains.html#Route53Domains.Client.get_operation_detail)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#get_operation_detail)
        """

    async def list_domains(
        self,
        *,
        FilterConditions: Sequence["FilterConditionTypeDef"] = ...,
        SortCondition: "SortConditionTypeDef" = ...,
        Marker: str = ...,
        MaxItems: int = ...
    ) -> ListDomainsResponseTypeDef:
        """
        This operation returns all the domain names registered with Amazon Route 53 for
        the current Amazon Web Services account if no filtering conditions are used.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains.html#Route53Domains.Client.list_domains)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#list_domains)
        """

    async def list_operations(
        self, *, SubmittedSince: Union[datetime, str] = ..., Marker: str = ..., MaxItems: int = ...
    ) -> ListOperationsResponseTypeDef:
        """
        Returns information about all of the operations that return an operation ID and
        that have ever been performed on domains that were registered by the current
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains.html#Route53Domains.Client.list_operations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#list_operations)
        """

    async def list_prices(
        self, *, Tld: str = ..., Marker: str = ..., MaxItems: int = ...
    ) -> ListPricesResponseTypeDef:
        """
        Lists the following prices for either all the TLDs supported by Route 53, or the
        specified TLD * Registration * Transfer * Owner change * Domain renewal * Domain
        restoration See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/route53domains-2014-05-1...`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains.html#Route53Domains.Client.list_prices)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#list_prices)
        """

    async def list_tags_for_domain(self, *, DomainName: str) -> ListTagsForDomainResponseTypeDef:
        """
        This operation returns all of the tags that are associated with the specified
        domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains.html#Route53Domains.Client.list_tags_for_domain)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#list_tags_for_domain)
        """

    async def register_domain(
        self,
        *,
        DomainName: str,
        DurationInYears: int,
        AdminContact: "ContactDetailTypeDef",
        RegistrantContact: "ContactDetailTypeDef",
        TechContact: "ContactDetailTypeDef",
        IdnLangCode: str = ...,
        AutoRenew: bool = ...,
        PrivacyProtectAdminContact: bool = ...,
        PrivacyProtectRegistrantContact: bool = ...,
        PrivacyProtectTechContact: bool = ...
    ) -> RegisterDomainResponseTypeDef:
        """
        This operation registers a domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains.html#Route53Domains.Client.register_domain)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#register_domain)
        """

    async def reject_domain_transfer_from_another_aws_account(
        self, *, DomainName: str
    ) -> RejectDomainTransferFromAnotherAwsAccountResponseTypeDef:
        """
        Rejects the transfer of a domain from another Amazon Web Services account to the
        current Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains.html#Route53Domains.Client.reject_domain_transfer_from_another_aws_account)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#reject_domain_transfer_from_another_aws_account)
        """

    async def renew_domain(
        self, *, DomainName: str, CurrentExpiryYear: int, DurationInYears: int = ...
    ) -> RenewDomainResponseTypeDef:
        """
        This operation renews a domain for the specified number of years.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains.html#Route53Domains.Client.renew_domain)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#renew_domain)
        """

    async def resend_contact_reachability_email(
        self, *, domainName: str = ...
    ) -> ResendContactReachabilityEmailResponseTypeDef:
        """
        For operations that require confirmation that the email address for the
        registrant contact is valid, such as registering a new domain, this operation
        resends the confirmation email to the current email address for the registrant
        contact.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains.html#Route53Domains.Client.resend_contact_reachability_email)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#resend_contact_reachability_email)
        """

    async def retrieve_domain_auth_code(
        self, *, DomainName: str
    ) -> RetrieveDomainAuthCodeResponseTypeDef:
        """
        This operation returns the AuthCode for the domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains.html#Route53Domains.Client.retrieve_domain_auth_code)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#retrieve_domain_auth_code)
        """

    async def transfer_domain(
        self,
        *,
        DomainName: str,
        DurationInYears: int,
        AdminContact: "ContactDetailTypeDef",
        RegistrantContact: "ContactDetailTypeDef",
        TechContact: "ContactDetailTypeDef",
        IdnLangCode: str = ...,
        Nameservers: Sequence["NameserverTypeDef"] = ...,
        AuthCode: str = ...,
        AutoRenew: bool = ...,
        PrivacyProtectAdminContact: bool = ...,
        PrivacyProtectRegistrantContact: bool = ...,
        PrivacyProtectTechContact: bool = ...
    ) -> TransferDomainResponseTypeDef:
        """
        Transfers a domain from another registrar to Amazon Route 53.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains.html#Route53Domains.Client.transfer_domain)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#transfer_domain)
        """

    async def transfer_domain_to_another_aws_account(
        self, *, DomainName: str, AccountId: str
    ) -> TransferDomainToAnotherAwsAccountResponseTypeDef:
        """
        Transfers a domain from the current Amazon Web Services account to another
        Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains.html#Route53Domains.Client.transfer_domain_to_another_aws_account)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#transfer_domain_to_another_aws_account)
        """

    async def update_domain_contact(
        self,
        *,
        DomainName: str,
        AdminContact: "ContactDetailTypeDef" = ...,
        RegistrantContact: "ContactDetailTypeDef" = ...,
        TechContact: "ContactDetailTypeDef" = ...
    ) -> UpdateDomainContactResponseTypeDef:
        """
        This operation updates the contact information for a particular domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains.html#Route53Domains.Client.update_domain_contact)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#update_domain_contact)
        """

    async def update_domain_contact_privacy(
        self,
        *,
        DomainName: str,
        AdminPrivacy: bool = ...,
        RegistrantPrivacy: bool = ...,
        TechPrivacy: bool = ...
    ) -> UpdateDomainContactPrivacyResponseTypeDef:
        """
        This operation updates the specified domain contact's privacy setting.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains.html#Route53Domains.Client.update_domain_contact_privacy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#update_domain_contact_privacy)
        """

    async def update_domain_nameservers(
        self, *, DomainName: str, Nameservers: Sequence["NameserverTypeDef"], FIAuthKey: str = ...
    ) -> UpdateDomainNameserversResponseTypeDef:
        """
        This operation replaces the current set of name servers for the domain with the
        specified set of name servers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains.html#Route53Domains.Client.update_domain_nameservers)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#update_domain_nameservers)
        """

    async def update_tags_for_domain(
        self, *, DomainName: str, TagsToUpdate: Sequence["TagTypeDef"] = ...
    ) -> Dict[str, Any]:
        """
        This operation adds or updates tags for a specified domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains.html#Route53Domains.Client.update_tags_for_domain)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#update_tags_for_domain)
        """

    async def view_billing(
        self,
        *,
        Start: Union[datetime, str] = ...,
        End: Union[datetime, str] = ...,
        Marker: str = ...,
        MaxItems: int = ...
    ) -> ViewBillingResponseTypeDef:
        """
        Returns all the domain-related billing records for the current Amazon Web
        Services account for a specified period See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/route53domains-2014-05-15/ViewBilling).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains.html#Route53Domains.Client.view_billing)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#view_billing)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_domains"]) -> ListDomainsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains.html#Route53Domains.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_operations"]) -> ListOperationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains.html#Route53Domains.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_prices"]) -> ListPricesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains.html#Route53Domains.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["view_billing"]) -> ViewBillingPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains.html#Route53Domains.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#get_paginator)
        """

    async def __aenter__(self) -> "Route53DomainsClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains.html#Route53Domains.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains.html#Route53Domains.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/)
        """
