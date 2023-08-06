"""
Type annotations for acm service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_acm.client import ACMClient

    session = get_session()
    async with session.create_client("acm") as client:
        client: ACMClient
    ```
"""
import sys
from typing import IO, Any, Dict, Mapping, Sequence, Type, Union

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.response import StreamingBody

from .literals import CertificateStatusType, ValidationMethodType
from .paginator import ListCertificatesPaginator
from .type_defs import (
    CertificateOptionsTypeDef,
    DescribeCertificateResponseTypeDef,
    DomainValidationOptionTypeDef,
    ExpiryEventsConfigurationTypeDef,
    ExportCertificateResponseTypeDef,
    FiltersTypeDef,
    GetAccountConfigurationResponseTypeDef,
    GetCertificateResponseTypeDef,
    ImportCertificateResponseTypeDef,
    ListCertificatesResponseTypeDef,
    ListTagsForCertificateResponseTypeDef,
    RequestCertificateResponseTypeDef,
    TagTypeDef,
)
from .waiter import CertificateValidatedWaiter

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("ACMClient",)

class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InvalidArgsException: Type[BotocoreClientError]
    InvalidArnException: Type[BotocoreClientError]
    InvalidDomainValidationOptionsException: Type[BotocoreClientError]
    InvalidParameterException: Type[BotocoreClientError]
    InvalidStateException: Type[BotocoreClientError]
    InvalidTagException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    RequestInProgressException: Type[BotocoreClientError]
    ResourceInUseException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    TagPolicyException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    TooManyTagsException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class ACMClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm.html#ACM.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ACMClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm.html#ACM.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#exceptions)
        """
    async def add_tags_to_certificate(
        self, *, CertificateArn: str, Tags: Sequence["TagTypeDef"]
    ) -> None:
        """
        Adds one or more tags to an ACM certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm.html#ACM.Client.add_tags_to_certificate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#add_tags_to_certificate)
        """
    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm.html#ACM.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#can_paginate)
        """
    async def delete_certificate(self, *, CertificateArn: str) -> None:
        """
        Deletes a certificate and its associated private key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm.html#ACM.Client.delete_certificate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#delete_certificate)
        """
    async def describe_certificate(
        self, *, CertificateArn: str
    ) -> DescribeCertificateResponseTypeDef:
        """
        Returns detailed metadata about the specified ACM certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm.html#ACM.Client.describe_certificate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#describe_certificate)
        """
    async def export_certificate(
        self, *, CertificateArn: str, Passphrase: Union[str, bytes, IO[Any], StreamingBody]
    ) -> ExportCertificateResponseTypeDef:
        """
        Exports a private certificate issued by a private certificate authority (CA) for
        use anywhere.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm.html#ACM.Client.export_certificate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#export_certificate)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm.html#ACM.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#generate_presigned_url)
        """
    async def get_account_configuration(self) -> GetAccountConfigurationResponseTypeDef:
        """
        Returns the account configuration options associated with an Amazon Web Services
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm.html#ACM.Client.get_account_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#get_account_configuration)
        """
    async def get_certificate(self, *, CertificateArn: str) -> GetCertificateResponseTypeDef:
        """
        Retrieves an Amazon-issued certificate and its certificate chain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm.html#ACM.Client.get_certificate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#get_certificate)
        """
    async def import_certificate(
        self,
        *,
        Certificate: Union[str, bytes, IO[Any], StreamingBody],
        PrivateKey: Union[str, bytes, IO[Any], StreamingBody],
        CertificateArn: str = ...,
        CertificateChain: Union[str, bytes, IO[Any], StreamingBody] = ...,
        Tags: Sequence["TagTypeDef"] = ...
    ) -> ImportCertificateResponseTypeDef:
        """
        Imports a certificate into Amazon Web Services Certificate Manager (ACM) to use
        with services that are integrated with ACM.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm.html#ACM.Client.import_certificate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#import_certificate)
        """
    async def list_certificates(
        self,
        *,
        CertificateStatuses: Sequence[CertificateStatusType] = ...,
        Includes: "FiltersTypeDef" = ...,
        NextToken: str = ...,
        MaxItems: int = ...
    ) -> ListCertificatesResponseTypeDef:
        """
        Retrieves a list of certificate ARNs and domain names.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm.html#ACM.Client.list_certificates)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#list_certificates)
        """
    async def list_tags_for_certificate(
        self, *, CertificateArn: str
    ) -> ListTagsForCertificateResponseTypeDef:
        """
        Lists the tags that have been applied to the ACM certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm.html#ACM.Client.list_tags_for_certificate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#list_tags_for_certificate)
        """
    async def put_account_configuration(
        self, *, IdempotencyToken: str, ExpiryEvents: "ExpiryEventsConfigurationTypeDef" = ...
    ) -> None:
        """
        Adds or modifies account-level configurations in ACM.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm.html#ACM.Client.put_account_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#put_account_configuration)
        """
    async def remove_tags_from_certificate(
        self, *, CertificateArn: str, Tags: Sequence["TagTypeDef"]
    ) -> None:
        """
        Remove one or more tags from an ACM certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm.html#ACM.Client.remove_tags_from_certificate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#remove_tags_from_certificate)
        """
    async def renew_certificate(self, *, CertificateArn: str) -> None:
        """
        Renews an eligible ACM certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm.html#ACM.Client.renew_certificate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#renew_certificate)
        """
    async def request_certificate(
        self,
        *,
        DomainName: str,
        ValidationMethod: ValidationMethodType = ...,
        SubjectAlternativeNames: Sequence[str] = ...,
        IdempotencyToken: str = ...,
        DomainValidationOptions: Sequence["DomainValidationOptionTypeDef"] = ...,
        Options: "CertificateOptionsTypeDef" = ...,
        CertificateAuthorityArn: str = ...,
        Tags: Sequence["TagTypeDef"] = ...
    ) -> RequestCertificateResponseTypeDef:
        """
        Requests an ACM certificate for use with other Amazon Web Services services.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm.html#ACM.Client.request_certificate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#request_certificate)
        """
    async def resend_validation_email(
        self, *, CertificateArn: str, Domain: str, ValidationDomain: str
    ) -> None:
        """
        Resends the email that requests domain ownership validation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm.html#ACM.Client.resend_validation_email)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#resend_validation_email)
        """
    async def update_certificate_options(
        self, *, CertificateArn: str, Options: "CertificateOptionsTypeDef"
    ) -> None:
        """
        Updates a certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm.html#ACM.Client.update_certificate_options)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#update_certificate_options)
        """
    def get_paginator(
        self, operation_name: Literal["list_certificates"]
    ) -> ListCertificatesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm.html#ACM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#get_paginator)
        """
    def get_waiter(
        self, waiter_name: Literal["certificate_validated"]
    ) -> CertificateValidatedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm.html#ACM.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#get_waiter)
        """
    async def __aenter__(self) -> "ACMClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm.html#ACM.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/)
        """
    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm.html#ACM.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/)
        """
