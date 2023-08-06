"""
Type annotations for support service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_support.client import SupportClient

    session = get_session()
    async with session.create_client("support") as client:
        client: SupportClient
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import DescribeCasesPaginator, DescribeCommunicationsPaginator
from .type_defs import (
    AddAttachmentsToSetResponseTypeDef,
    AddCommunicationToCaseResponseTypeDef,
    AttachmentTypeDef,
    CreateCaseResponseTypeDef,
    DescribeAttachmentResponseTypeDef,
    DescribeCasesResponseTypeDef,
    DescribeCommunicationsResponseTypeDef,
    DescribeServicesResponseTypeDef,
    DescribeSeverityLevelsResponseTypeDef,
    DescribeTrustedAdvisorCheckRefreshStatusesResponseTypeDef,
    DescribeTrustedAdvisorCheckResultResponseTypeDef,
    DescribeTrustedAdvisorChecksResponseTypeDef,
    DescribeTrustedAdvisorCheckSummariesResponseTypeDef,
    RefreshTrustedAdvisorCheckResponseTypeDef,
    ResolveCaseResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("SupportClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AttachmentIdNotFound: Type[BotocoreClientError]
    AttachmentLimitExceeded: Type[BotocoreClientError]
    AttachmentSetExpired: Type[BotocoreClientError]
    AttachmentSetIdNotFound: Type[BotocoreClientError]
    AttachmentSetSizeLimitExceeded: Type[BotocoreClientError]
    CaseCreationLimitExceeded: Type[BotocoreClientError]
    CaseIdNotFound: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    DescribeAttachmentLimitExceeded: Type[BotocoreClientError]
    InternalServerError: Type[BotocoreClientError]


class SupportClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support.html#Support.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SupportClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support.html#Support.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support/client/#exceptions)
        """

    async def add_attachments_to_set(
        self, *, attachments: Sequence["AttachmentTypeDef"], attachmentSetId: str = ...
    ) -> AddAttachmentsToSetResponseTypeDef:
        """
        Adds one or more attachments to an attachment set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support.html#Support.Client.add_attachments_to_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support/client/#add_attachments_to_set)
        """

    async def add_communication_to_case(
        self,
        *,
        communicationBody: str,
        caseId: str = ...,
        ccEmailAddresses: Sequence[str] = ...,
        attachmentSetId: str = ...
    ) -> AddCommunicationToCaseResponseTypeDef:
        """
        Adds additional customer communication to an Amazon Web Services Support case.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support.html#Support.Client.add_communication_to_case)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support/client/#add_communication_to_case)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support.html#Support.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support/client/#can_paginate)
        """

    async def create_case(
        self,
        *,
        subject: str,
        communicationBody: str,
        serviceCode: str = ...,
        severityCode: str = ...,
        categoryCode: str = ...,
        ccEmailAddresses: Sequence[str] = ...,
        language: str = ...,
        issueType: str = ...,
        attachmentSetId: str = ...
    ) -> CreateCaseResponseTypeDef:
        """
        Creates a case in the Amazon Web Services Support Center.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support.html#Support.Client.create_case)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support/client/#create_case)
        """

    async def describe_attachment(self, *, attachmentId: str) -> DescribeAttachmentResponseTypeDef:
        """
        Returns the attachment that has the specified ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support.html#Support.Client.describe_attachment)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support/client/#describe_attachment)
        """

    async def describe_cases(
        self,
        *,
        caseIdList: Sequence[str] = ...,
        displayId: str = ...,
        afterTime: str = ...,
        beforeTime: str = ...,
        includeResolvedCases: bool = ...,
        nextToken: str = ...,
        maxResults: int = ...,
        language: str = ...,
        includeCommunications: bool = ...
    ) -> DescribeCasesResponseTypeDef:
        """
        Returns a list of cases that you specify by passing one or more case IDs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support.html#Support.Client.describe_cases)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support/client/#describe_cases)
        """

    async def describe_communications(
        self,
        *,
        caseId: str,
        beforeTime: str = ...,
        afterTime: str = ...,
        nextToken: str = ...,
        maxResults: int = ...
    ) -> DescribeCommunicationsResponseTypeDef:
        """
        Returns communications and attachments for one or more support cases.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support.html#Support.Client.describe_communications)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support/client/#describe_communications)
        """

    async def describe_services(
        self, *, serviceCodeList: Sequence[str] = ..., language: str = ...
    ) -> DescribeServicesResponseTypeDef:
        """
        Returns the current list of Amazon Web Services services and a list of service
        categories for each service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support.html#Support.Client.describe_services)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support/client/#describe_services)
        """

    async def describe_severity_levels(
        self, *, language: str = ...
    ) -> DescribeSeverityLevelsResponseTypeDef:
        """
        Returns the list of severity levels that you can assign to a support case.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support.html#Support.Client.describe_severity_levels)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support/client/#describe_severity_levels)
        """

    async def describe_trusted_advisor_check_refresh_statuses(
        self, *, checkIds: Sequence[str]
    ) -> DescribeTrustedAdvisorCheckRefreshStatusesResponseTypeDef:
        """
        Returns the refresh status of the Trusted Advisor checks that have the specified
        check IDs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support.html#Support.Client.describe_trusted_advisor_check_refresh_statuses)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support/client/#describe_trusted_advisor_check_refresh_statuses)
        """

    async def describe_trusted_advisor_check_result(
        self, *, checkId: str, language: str = ...
    ) -> DescribeTrustedAdvisorCheckResultResponseTypeDef:
        """
        Returns the results of the Trusted Advisor check that has the specified check
        ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support.html#Support.Client.describe_trusted_advisor_check_result)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support/client/#describe_trusted_advisor_check_result)
        """

    async def describe_trusted_advisor_check_summaries(
        self, *, checkIds: Sequence[str]
    ) -> DescribeTrustedAdvisorCheckSummariesResponseTypeDef:
        """
        Returns the results for the Trusted Advisor check summaries for the check IDs
        that you specified.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support.html#Support.Client.describe_trusted_advisor_check_summaries)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support/client/#describe_trusted_advisor_check_summaries)
        """

    async def describe_trusted_advisor_checks(
        self, *, language: str
    ) -> DescribeTrustedAdvisorChecksResponseTypeDef:
        """
        Returns information about all available Trusted Advisor checks, including the
        name, ID, category, description, and metadata.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support.html#Support.Client.describe_trusted_advisor_checks)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support/client/#describe_trusted_advisor_checks)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support.html#Support.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support/client/#generate_presigned_url)
        """

    async def refresh_trusted_advisor_check(
        self, *, checkId: str
    ) -> RefreshTrustedAdvisorCheckResponseTypeDef:
        """
        Refreshes the Trusted Advisor check that you specify using the check ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support.html#Support.Client.refresh_trusted_advisor_check)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support/client/#refresh_trusted_advisor_check)
        """

    async def resolve_case(self, *, caseId: str = ...) -> ResolveCaseResponseTypeDef:
        """
        Resolves a support case.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support.html#Support.Client.resolve_case)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support/client/#resolve_case)
        """

    @overload
    def get_paginator(self, operation_name: Literal["describe_cases"]) -> DescribeCasesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support.html#Support.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_communications"]
    ) -> DescribeCommunicationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support.html#Support.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support/client/#get_paginator)
        """

    async def __aenter__(self) -> "SupportClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support.html#Support.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/support.html#Support.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support/client/)
        """
